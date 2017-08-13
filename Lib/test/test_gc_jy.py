"""
Tests some Jython-specific gc aspects and debugging
features.
Skips and try-blocks assure that this test-script is
still runnable with CPython and passes there as far
as not skipped.
"""

import unittest
from test import test_support
import time
import gc
import weakref
from Queue import Queue

try:
    from java.lang import System, Runnable, Class, Object
    from javatests import GCTestHelper
except ImportError:
    #i.e. not Jython is running
    pass


class GCTests_Jy_CyclicGarbage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #Jython-specific block:
        try:
            cls.savedJythonGCFlags = gc.getJythonGCFlags()
            #the finalizer-related tests need this flag to pass in Jython:
            gc.addJythonGCFlags(gc.DONT_FINALIZE_CYCLIC_GARBAGE)
            gc.stopMonitoring()
        except Exception:
            pass
     
    @classmethod
    def tearDownClass(cls):
        try:
            gc.setJythonGCFlags(cls.savedJythonGCFlags)
        except Exception:
            pass

    # In contrast to the tests in test_gc, these finalizer tests shall work
    # even if gc-monitoring is disabled.
    def test_finalizer(self):
        # A() is uncollectable if it is part of a cycle, make sure it shows up
        # in gc.garbage.
        class A:
            def __del__(self): pass
        class B:
            pass
        a = A()
        a.a = a
        id_a = id(a)
        b = B()
        b.b = b
        gc.collect()
        del a
        del b
        self.assertNotEqual(gc.collect(), 0)
        time.sleep(4)
        for obj in gc.garbage:
            if id(obj) == id_a:
                del obj.a
                break
        else:
            self.fail("didn't find obj in garbage (finalizer)")
        gc.garbage.remove(obj)

    def test_finalizer_newclass(self):
        # A() is uncollectable if it is part of a cycle, make sure it shows up
        # in gc.garbage.
        class A(object):
            def __del__(self): pass
        class B(object):
            pass
        a = A()
        a.a = a
        id_a = id(a)
        b = B()
        b.b = b
        gc.collect()
        del a
        del b
        self.assertNotEqual(gc.collect(), 0)
        time.sleep(1)
        for obj in gc.garbage:
            if id(obj) == id_a:
                del obj.a
                break
        else:
            self.fail("didn't find obj in garbage (finalizer)")
        gc.garbage.remove(obj)

    @unittest.skipUnless(test_support.is_jython,
        'CPython has no monitor state')
    def test_manual_monitoring(self):
        # since tuples are immutable we close the loop with a list
        l = []
        t = (l,)
        l.append(t)
        gc.monitorObject(l)
        #gc.monitorObject(t) <- intentionally only monitor one of them
        gc.collect()
        del t
        del l
        # Note that usually two collected objects would be expected - l and t.
        # But we intentionally only monitored one of them, so only one should
        # be counted.
        self.assertEqual(gc.collect(), 1)


@unittest.skipUnless(test_support.is_jython,
        'CPython has no gc preprocess and postprocess features')
class GCTests_Jy_preprocess_and_postprocess(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #Jython-specific block:
        try:
            cls.savedJythonGCFlags = gc.getJythonGCFlags()
            gc.setMonitorGlobal(True)
        except Exception:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            gc.setJythonGCFlags(cls.savedJythonGCFlags)
        except Exception:
            pass

    def test_finalization_preprocess_and_postprocess(self):
        # Note that this test is done here again (already was in another class
        # in this module), to see that everything works as it should also with
        # a different flag-context.
        comments = []
        self0 = self
        class A:
            def __del__(self):
                self0.assertIn("run PreProcess", comments)
                comments.append("A del")
                # let's simulate a time-consuming finalizer
                # to ensure that post finalization processing
                # is sensitive to this
                time.sleep(0.5)
                comments.append("A del done")

        class PreProcess(Runnable):
            def run(self):
                self0.assertEqual(comments, [])
                comments.append("run PreProcess")

        class PostProcess(Runnable):
            def run(self):
                self0.assertIn("run PreProcess", comments)
                self0.assertIn("A del", comments)
                self0.assertIn("A del done", comments)
                comments.append("run PostProcess")

        a = A()
        a = None
        prePr = PreProcess()
        postPr = PostProcess()
        time.sleep(1) #   <- to avoid that the newly registered processes
                      #      become subject to previous run (remember: We
                      #      are not in monitor-mode, i.e. gc runs async.
        gc.registerPreFinalizationProcess(prePr)
        gc.registerPostFinalizationProcess(postPr)
        # Note that order matters here:
        # If the flag gc.DONT_FINALIZE_RESURRECTED_OBJECTS is used,
        # gc.registerPostFinalizationProcess(postPr, 0) would lead to failure,
        # because postPr asserts that a's finalizer already ran. Since
        # DONT_FINALIZE_RESURRECTED_OBJECTS also inserted a postprocess,
        # to perform delayed finalization, the 0-index would prepend postPr
        # before the process that actually runs the finalizers.
        System.gc()
        # we wait a bit longer here, since PostProcess runs asynchronous
        # and must wait for the finalizer of A
        time.sleep(2)
        self.assertIn("run PostProcess", comments)
        comments = []
        gc.unregisterPreFinalizationProcess(prePr)
        gc.unregisterPostFinalizationProcess(postPr)

    def test_with_extern_NonPyObjectFinalizer_that_notifies_gc(self):
        comments = []
        class A:
            def __init__(self, index):
                self.index = index

            def __del__(self):
                comments.append("A_del_"+str(self.index))

        class PreProcess(Runnable):
            preCount = 0
            def run(self):
                PreProcess.preCount += 1

        class PostProcess(Runnable):
            postCount = 0
            def run(self):
                PostProcess.postCount += 1

        prePr = PreProcess()
        postPr = PostProcess()
        time.sleep(1) #   <- to avoid that the newly registered processes
                      #      become subject to previous run (remember: We
                      #      are not in monitor-mode, i.e. gc runs async.
        gc.registerPreFinalizationProcess(prePr)
        gc.registerPostFinalizationProcess(postPr)
        for i in range(4):
            f = A(i)
            del f
        #NastyFinalizer would cause this test occasionally to fail
        externFinalizer = GCTestHelper.NotSoNastyFinalizer()
        del externFinalizer
        for i in range(4, 8):
            f = A(i)
            del f
        System.gc()
        # we wait a bit longer here, since PostProcess runs asynchronous
        # and must wait for the finalizer of A
        time.sleep(4)
        self.assertEqual(len(comments), 8)
        self.assertEqual(PreProcess.preCount, 1)
        self.assertEqual(PostProcess.postCount, 1)
        comments = []
        gc.unregisterPreFinalizationProcess(prePr)
        gc.unregisterPostFinalizationProcess(postPr)


@unittest.skipUnless(test_support.is_jython,
        'This class tests detailed Jython-specific behavior.')
class GCTests_Jy_Delayed_Finalization(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #Jython-specific block:
        try:
            cls.savedJythonGCFlags = gc.getJythonGCFlags()
            #the finalizer-related tests need this flag to pass in Jython:
            gc.addJythonGCFlags(gc.DONT_FINALIZE_RESURRECTED_OBJECTS)
            gc.stopMonitoring()
        except Exception:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            gc.setJythonGCFlags(cls.savedJythonGCFlags)
        except Exception:
            pass

    # Tests from GCTests_Jy_preprocess_and_postprocess are repeated here
    # without monitoring.
    def test_finalization_preprocess_and_postprocess(self):
        # Note that this test is done here again (already was in another class
        # in this module), to see that everything works as it should also with
        # a different flag-context.
        comments = []
        self0 = self
        class A:
            def __del__(self):
                self0.assertIn("run PreProcess", comments)
                comments.append("A del")
                # let's simulate a time-consuming finalizer
                # to ensure that post finalization processing
                # is sensitive to this
                time.sleep(0.5)
                comments.append("A del done")

        class PreProcess(Runnable):
            def run(self):
                self0.assertEqual(comments, [])
                comments.append("run PreProcess")

        class PostProcess(Runnable):
            def run(self):
                self0.assertIn("run PreProcess", comments)
                self0.assertIn("A del", comments)
                self0.assertIn("A del done", comments)
                comments.append("run PostProcess")

        a = A()
        a = None
        prePr = PreProcess()
        postPr = PostProcess()
        time.sleep(2) #   <- to avoid that the newly registered processes
                      #      become subject to previous run
        gc.registerPreFinalizationProcess(prePr)
        gc.registerPostFinalizationProcess(postPr)
        # Note that order matters here:
        # If the flag gc.DONT_FINALIZE_RESURRECTED_OBJECTS is used,
        # gc.registerPostFinalizationProcess(postPr, 0) would lead to failure,
        # because postPr asserts that a's finalizer already ran. Since
        # DONT_FINALIZE_RESURRECTED_OBJECTS also inserted a postprocess,
        # to perform delayed finalization, the 0-index would prepend postPr
        # before the process that actually runs the finalizers.
        System.gc()
        # we wait a bit longer here, since PostProcess runs asynchronous
        # and must wait for the finalizer of A
        time.sleep(2)
        self.assertIn("run PostProcess", comments)
        comments = []
        gc.unregisterPreFinalizationProcess(prePr)
        gc.unregisterPostFinalizationProcess(postPr)

    def test_with_extern_NonPyObjectFinalizer_that_notifies_gc(self):
        comments = []
        class A:
            def __init__(self, index):
                self.index = index

            def __del__(self):
                comments.append("A_del_"+str(self.index))

        class PreProcess(Runnable):
            preCount = 0
            def run(self):
                PreProcess.preCount += 1

        class PostProcess(Runnable):
            postCount = 0
            def run(self):
                PostProcess.postCount += 1

        prePr = PreProcess()
        postPr = PostProcess()
        time.sleep(1) #   <- to avoid that the newly registered processes
                      #      become subject to previous run (remember: We
                      #      are not in monitor-mode, i.e. gc runs async.
        gc.registerPreFinalizationProcess(prePr)
        gc.registerPostFinalizationProcess(postPr)
        for i in range(4):
            f = A(i)
            del f
        # NastyFinalizer would cause this test occasionally to fail
        externFinalizer = GCTestHelper.NotSoNastyFinalizer()
        del externFinalizer
        for i in range(4, 8):
            f = A(i)
            del f
        System.gc()
        # we wait a bit longer here, since PostProcess runs asynchronous
        # and must wait for the finalizer of A
        time.sleep(4)
        self.assertEqual(len(comments), 8)
        self.assertEqual(PreProcess.preCount, 1)
        self.assertEqual(PostProcess.postCount, 1)
        comments = []
        gc.unregisterPreFinalizationProcess(prePr)
        gc.unregisterPostFinalizationProcess(postPr)

    def test_delayedFinalization(self):
        #time.sleep(2)
        resurrect = []
        comments = []

        class Test_Finalizable(object):
            def __init__(self, name):
                self.name = name

            def __repr__(self):
                return "<"+self.name+">"

            def __del__(self):
                comments.append("del "+self.name)

        class Test_Resurrection(object):
            def __init__(self, name):
                self.name = name
            
            def __repr__(self):
                return "<"+self.name+">"

            def __del__(self):
                comments.append("del "+self.name)
                if hasattr(self, "toResurrect"):
                    resurrect.append(self.toResurrect)

        a = Test_Finalizable("a")
        a.b = Test_Finalizable("b")
        c = Test_Resurrection("c")
        c.a = a
        c.toResurrect = Test_Finalizable("d")
         
        del a
        del c
        self.assertNotEqual(gc.collect(), 0)
        time.sleep(2)
        # Note that CPython would collect a, b and c in one run.
        # With gc.DONT_FINALIZE_RESURRECTED_OBJECTS set, Jython
        # Would not collect a and b in the same run with c
        # because a and b might have been resurrected by c and
        # Java allows not to detect such resurrection in any
        # other way than waiting for the next gc-run.
        self.assertIn('del c', comments)
        self.assertEqual(1, len(comments))
        comments = []
        self.assertNotEqual(gc.collect(), 0)
        time.sleep(2)
        self.assertIn('del a', comments)
        self.assertEqual(1, len(comments))
        comments = []
        self.assertNotEqual(gc.collect(), 0)
        time.sleep(2)
        self.assertIn('del b', comments)
        self.assertEqual(1, len(comments))


@unittest.skipUnless(test_support.is_jython,
        'This class tests detailed Jython-specific behavior.')
class GCTests_Jy_Forced_Delayed_Finalization(unittest.TestCase):
# Here we basically reproduce the ordinary delayed finalization test, but ensure
# that the FORCE_DELAYED_FINALIZATION-flag does not cause regressions with this.
    @classmethod
    def setUpClass(cls):
        #Jython-specific block:
        try:
            cls.savedJythonGCFlags = gc.getJythonGCFlags()
            #the finalizer-related tests need this flag to pass in Jython:
            gc.addJythonGCFlags(gc.DONT_FINALIZE_RESURRECTED_OBJECTS)
            gc.addJythonGCFlags(gc.FORCE_DELAYED_FINALIZATION)
            gc.stopMonitoring()
        except Exception:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            gc.setJythonGCFlags(cls.savedJythonGCFlags)
        except Exception:
            pass

    # Tests from GCTests_Jy_preprocess_and_postprocess are repeated here
    # without monitoring but with forced flag.
    def test_forced_finalization_preprocess_and_postprocess(self):
        # Note that this test is done here again (already was in another class
        # in this module), to see that everything works as it should also with
        # a different flag-context.
        comments = []
        self0 = self
        class A:
            def __del__(self):
                self0.assertIn("run PreProcess", comments)
                comments.append("A del")
                # let's simulate a time-consuming finalizer
                # to ensure that post finalization processing
                # is sensitive to this
                time.sleep(0.5)
                comments.append("A del done")

        class PreProcess(Runnable):
            def run(self):
                self0.assertEqual(comments, [])
                comments.append("run PreProcess")

        class PostProcess(Runnable):
            def run(self):
                self0.assertIn("run PreProcess", comments)
                self0.assertIn("A del", comments)
                self0.assertIn("A del done", comments)
                comments.append("run PostProcess")

        a = A()
        a = None
        prePr = PreProcess()
        postPr = PostProcess()
        time.sleep(1) #   <- to avoid that the newly registered processes
                      #      become subject to previous run
        gc.registerPreFinalizationProcess(prePr)
        gc.registerPostFinalizationProcess(postPr)
        # Note that order matters here:
        # If the flag gc.DONT_FINALIZE_RESURRECTED_OBJECTS is used,
        # gc.registerPostFinalizationProcess(postPr, 0) would lead to failure,
        # because postPr asserts that a's finalizer already ran. Since
        # DONT_FINALIZE_RESURRECTED_OBJECTS also inserted a postprocess,
        # to perform delayed finalization, the 0-index would prepend postPr
        # before the process that actually runs the finalizers.
        System.gc()
        # we wait a bit longer here, since PostProcess runs asynchronous
        # and must wait for the finalizer of A
        time.sleep(2)
        self.assertIn("run PostProcess", comments)
        comments = []
        gc.unregisterPreFinalizationProcess(prePr)
        gc.unregisterPostFinalizationProcess(postPr)

    def test_forced_with_extern_NonPyObjectFinalizer_that_notifies_gc(self):
        comments = []
        class A:
            def __init__(self, index):
                self.index = index

            def __del__(self):
                comments.append("A_del_"+str(self.index))

        class PreProcess(Runnable):
            preCount = 0
            def run(self):
                PreProcess.preCount += 1

        class PostProcess(Runnable):
            postCount = 0
            def run(self):
                PostProcess.postCount += 1

        prePr = PreProcess()
        postPr = PostProcess()
        time.sleep(1) #   <- to avoid that the newly registered processes
                      #      become subject to previous run (remember: We
                      #      are not in monitor-mode, i.e. gc runs async.
        gc.registerPreFinalizationProcess(prePr)
        gc.registerPostFinalizationProcess(postPr)
        for i in range(4):
            f = A(i)
            del f
        #NastyFinalizer would cause this test occasionally to fail
        externFinalizer = GCTestHelper.NotSoNastyFinalizer()
        del externFinalizer
        for i in range(4, 8):
            f = A(i)
            del f
        System.gc()
        # we wait a bit longer here, since PostProcess runs asynchronous
        # and must wait for the finalizer of A
        time.sleep(4)
        self.assertEqual(len(comments), 8)
        self.assertEqual(PreProcess.preCount, 1)
        self.assertEqual(PostProcess.postCount, 1)
        comments = []
        gc.unregisterPreFinalizationProcess(prePr)
        gc.unregisterPostFinalizationProcess(postPr)

    def test_forced_delayedFinalization(self):
        #time.sleep(2)
        resurrect = []
        comments = []

        class Test_Finalizable(object):
            def __init__(self, name):
                self.name = name

            def __repr__(self):
                return "<"+self.name+">"

            def __del__(self):
                comments.append("del "+self.name)

        class Test_Resurrection(object):
            def __init__(self, name):
                self.name = name
            
            def __repr__(self):
                return "<"+self.name+">"

            def __del__(self):
                comments.append("del "+self.name)
                if hasattr(self, "toResurrect"):
                    resurrect.append(self.toResurrect)

        a = Test_Finalizable("a")
        a.b = Test_Finalizable("b")
        c = Test_Resurrection("c")
        c.a = a
        c.toResurrect = Test_Finalizable("d")
         
        del a
        del c
        self.assertNotEqual(gc.collect(), 0)
        time.sleep(1)
        # Note that CPython would collect a, b and c in one run.
        # With gc.DONT_FINALIZE_RESURRECTED_OBJECTS set, Jython
        # Would not collect a and b in the same run with c
        # because a and b might have been resurrected by c and
        # Java allows not to detect such resurrection in any
        # other way than waiting for the next gc-run.
        self.assertIn('del c', comments)
        self.assertEqual(1, len(comments))
        comments = []
        self.assertNotEqual(gc.collect(), 0)
        time.sleep(1)
        self.assertIn('del a', comments)
        self.assertEqual(1, len(comments))
        comments = []
        self.assertNotEqual(gc.collect(), 0)
        time.sleep(1)
        self.assertIn('del b', comments)
        self.assertEqual(1, len(comments))


@unittest.skipUnless(test_support.is_jython,
        'This class tests detailed Jython-specific behavior.')
class GCTests_Jy_Raw_Forced_Delayed_Finalization(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #Jython-specific block:
        try:
            cls.savedJythonGCFlags = gc.getJythonGCFlags()
            #the finalizer-related tests need this flag to pass in Jython:
            gc.stopMonitoring()
            #gc.addJythonGCFlags(gc.VERBOSE_DELAYED)
        except Exception:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            gc.setJythonGCFlags(cls.savedJythonGCFlags)
        except Exception:
            pass

    def test_raw_forced_delayedFinalization(self):
        #print "test_raw_forced_delayedFinalization"
        comments = []
    
        class Test_JavaAbortFinalizable(Object):
            def __init__(self, name, toAbort):
                self.name = name
                self.toAbort = toAbort
    
            def __repr__(self):
                return "<"+self.name+">"
    
            def finalize(self):
                gc.notifyPreFinalization()
                comments.append("del "+self.name)
                gc.abortDelayedFinalization(self.toAbort)
                gc.notifyPostFinalization()
    
        class Test_Finalizable(object):
            def __init__(self, name):
                self.name = name
    
            def __repr__(self):
                return "<"+self.name+">"
    
            def __del__(self):
                comments.append("del "+self.name)
        
        def callback(obj):
            comments.append("callback0")

        a = Test_Finalizable("a")
        wa = weakref.ref(a, callback)
        b = Test_JavaAbortFinalizable("b", a)
        gc.removeJythonGCFlags(gc.FORCE_DELAYED_WEAKREF_CALLBACKS)
        gc.addJythonGCFlags(gc.FORCE_DELAYED_FINALIZATION)
        self.assertTrue(gc.delayedFinalizationEnabled())
        self.assertFalse(gc.delayedWeakrefCallbacksEnabled())
        del a
        del b
        System.gc()
        time.sleep(2)

        self.assertIn('del b', comments)
        self.assertEqual(2, len(comments))
        self.assertIn('callback0', comments)
        self.assertNotIn('del a', comments)
        self.assertIsNone(wa())
        gc.removeJythonGCFlags(gc.FORCE_DELAYED_FINALIZATION)

    def test_raw_forced_delayedWeakrefCallback(self):
        comments = []
        resurrected = []
         
        class Test_JavaResurrectFinalizable(Object):
            def __init__(self, name, toResurrect):
                self.name = name
                self.toResurrect = toResurrect
         
            def __repr__(self):
                return "<"+self.name+">"

            # Note that this type of finalizer is usually not recommended
            # as it gets lost in case of resurrection.
            def finalize(self):
                gc.notifyPreFinalization()
                comments.append("del "+self.name)
                resurrected.append(self.toResurrect)
                # We manually restore weak references:
                gc.restoreWeakReferences(self.toResurrect)
                gc.notifyPostFinalization()
    
        class Test_Finalizable(object):
            def __init__(self, name):
                self.name = name
    
            def __repr__(self):
                return "<"+self.name+">"
    
            def __del__(self):
                comments.append("del "+self.name)
    
        def callback(obj):
            comments.append("callback")
    
        a = Test_Finalizable("a")
        b = Test_JavaResurrectFinalizable("b", a)
        wa = weakref.ref(a, callback)
        gc.removeJythonGCFlags(gc.FORCE_DELAYED_FINALIZATION)
        gc.addJythonGCFlags(gc.FORCE_DELAYED_WEAKREF_CALLBACKS)
        self.assertFalse(gc.delayedFinalizationEnabled())
        self.assertTrue(gc.delayedWeakrefCallbacksEnabled())
        self.assertEqual(len(comments), 0)
        aStr = str(a)
        del a
        del b
        System.gc()
        time.sleep(2)
        self.assertIn("del a", comments)
        self.assertIn("del b", comments)
        self.assertEqual(1, len(resurrected))
        self.assertEqual(str(resurrected[0]), aStr)
        self.assertIsNotNone(wa())
        self.assertEqual(resurrected[0], wa())
        self.assertNotIn("callback", comments)
        self.assertEqual(2, len(comments))
        gc.removeJythonGCFlags(gc.FORCE_DELAYED_WEAKREF_CALLBACKS)

    def test_raw_forced_delayed(self):
        comments = []
    
        class Test_JavaAbortFinalizable(Object):
            def __init__(self, name, toAbort):
                self.name = name
                self.toAbort = toAbort
    
            def __repr__(self):
                return "<"+self.name+">"
    
            def finalize(self):
                gc.notifyPreFinalization()
                comments.append("del "+self.name)
                gc.abortDelayedFinalization(self.toAbort)
                # We manually restore weak references:
                gc.restoreWeakReferences(self.toAbort)
                gc.notifyPostFinalization()

        class Test_Finalizable(object):
            def __init__(self, name):
                self.name = name

            def __repr__(self):
                return "<"+self.name+">"

            def __del__(self):
                comments.append("del "+self.name)

        def callback_a(obj):
            comments.append("callback_a")

        def callback_b(obj):
            comments.append("callback_b")

        a = Test_Finalizable("a")
        wa = weakref.ref(a, callback_a)
        b = Test_JavaAbortFinalizable("b", a)
        wb = weakref.ref(b, callback_b)
        gc.addJythonGCFlags(gc.FORCE_DELAYED_FINALIZATION)
        gc.addJythonGCFlags(gc.FORCE_DELAYED_WEAKREF_CALLBACKS)
        self.assertTrue(gc.delayedFinalizationEnabled())
        self.assertTrue(gc.delayedWeakrefCallbacksEnabled())
        self.assertEqual(len(comments), 0)
        del a
        del b
        System.gc()
        time.sleep(2)

        self.assertIsNotNone(wa())
        self.assertIsNone(wb())
        self.assertIn('del b', comments)
        self.assertNotIn('callback_a', comments)
        self.assertIn('callback_b', comments)
        self.assertNotIn('del a', comments)
        self.assertEqual(2, len(comments))

        gc.removeJythonGCFlags(gc.FORCE_DELAYED_FINALIZATION)
        gc.removeJythonGCFlags(gc.FORCE_DELAYED_WEAKREF_CALLBACKS)


@unittest.skipIf(__name__ != "__main__", 'Hangs under regrtest')
class GCTests_Jy_Monitoring(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #Jython-specific block:
        try:
            cls.savedJythonGCFlags = gc.getJythonGCFlags()
            gc.setMonitorGlobal(True)
            gc.addJythonGCFlags(gc.DONT_FINALIZE_RESURRECTED_OBJECTS)
            # since gc module already exists, it would not be caught by monitorGlobal.
            # so we have to monitor it manually:
            gc.monitorObject(gc)
            # the finalizer-related tests need this flag to pass in Jython:
            # gc.addJythonGCFlags(gc.DONT_FINALIZE_CYCLIC_GARBAGE)
        except Exception:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            gc.setJythonGCFlags(cls.savedJythonGCFlags)
            gc.stopMonitoring()
        except Exception:
            pass

    @unittest.skipUnless(test_support.is_jython, 'CPython has no monitor-state.')
    def test_monitor_status_after_delayed_finalization(self):
        resurrect = []
        comments = []

        class Test_Finalizable(object):
            def __init__(self, name):
                self.name = name

            def __repr__(self):
                return "<"+self.name+">"

            def __del__(self):
                comments.append("del "+self.name)

        class Test_Resurrection(object):
            def __init__(self, name):
                self.name = name
            
            def __repr__(self):
                return "<"+self.name+">"

            def __del__(self):
                comments.append("del "+self.name)
                if hasattr(self, "toResurrect"):
                    resurrect.append(self.toResurrect)

        a = Test_Finalizable("a")
        a.b = Test_Finalizable("b")
        c = Test_Resurrection("c")
        c.toResurrect = a
        a.b.a = a
        self.assertTrue(gc.isMonitored(a))
        self.assertTrue(gc.isMonitored(a.b))
        self.assertTrue(gc.isMonitored(c))
        gc.collect()
        del a
        del c
        #gc.set_debug(gc.DEBUG_SAVEALL)
        self.assertEqual(gc.collect(), 0) #c is not cyclic and a, b are resurrected,
                                          #so nothing to count here
        #self.asserEqual(len(gc.garbage), 0)
            # if we called gc.set_debug(gc.DEBUG_SAVEALL) above, it would
            # be okay for gc.garbage to be empty, because a and b
            # are not finalized and c is not cyclic.
        self.assertEqual(comments, ['del c'])
        self.assertEqual(str(resurrect), "[<a>]")
        self.assertTrue(gc.isMonitored(resurrect[0]))
        self.assertTrue(gc.isMonitored(resurrect[0].b))

    def test_notifyRerun_for_delayed_finalization(self):
        gc.collect()
        comments = []

        class Test_Finalizable(object):
            def __init__(self, name):
                self.name = name

            def __repr__(self):
                return "<"+self.name+">"

            def __del__(self):
                comments.append("del "+self.name)

        a = Test_Finalizable("a")
        lst = []
        lst1 = [lst]
        lst.append(lst1)
        a.b = Test_Finalizable("b")
        a.b.lst = lst
        del lst
        del lst1
        try:
            self.assertTrue(gc.isMonitored(a))
            self.assertTrue(gc.isMonitored(a.b))
        except AttributeError:
            pass
        del a
        self.assertEqual(gc.collect(), 2) # c is not cyclic and a, b are resurrected,
                                          # the cycle of two lists is counted here
        self.assertEqual(comments, ['del a', 'del b'])


class GCTests_Jy_Weakref(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #Jython-specific block:
        try:
            cls.savedJythonGCFlags = gc.getJythonGCFlags()
            gc.addJythonGCFlags(gc.PRESERVE_WEAKREFS_ON_RESURRECTION)
        except Exception:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            gc.setJythonGCFlags(cls.savedJythonGCFlags)
            gc.stopMonitoring()
        except Exception:
            pass

    def test_weakref_after_resurrection(self):
        resurrect = []
        comments = []
        class Test_Finalizable(object):
            def __init__(self, name):
                self.name = name

            def __repr__(self):
                return "<"+self.name+">"

            def __del__(self):
                comments.append("del "+self.name)

        class Test_Resurrection(object):
            def __init__(self, name):
                self.name = name
            
            def __repr__(self):
                return "<"+self.name+">"

            def __del__(self):
                comments.append("del "+self.name)
                if hasattr(self, "toResurrect"):
                    resurrect.append(self)

        def clb(ref):
            comments.append("clb")

        def clb2(ref):
            comments.append("clb2 "+str(comments))

        a = Test_Finalizable("a")
        wa = weakref.ref(a, clb)
        self.assertEqual(wa(), a)
        c = Test_Resurrection("c")
        c.toResurrect = a
        wc = weakref.ref(c, clb2)
        try:
            gc.monitorObject(c)
        except Exception:
            pass
        del a
        del c
        gc.collect()
        self.assertIn('clb2 []', comments)
        self.assertNotIn("clb", comments)
        self.assertEqual(str(resurrect), "[<c>]")
        self.assertEqual(str(wa()), "<a>")
        self.assertEqual(wc(), None)

    def test_weakref_after_resurrection_and_delayed_finalize(self):
        resurrect = []
        comments = []
        class Test_Finalizable(object):
            def __init__(self, name):
                self.name = name

            def __repr__(self):
                return "<"+self.name+">"

            def __del__(self):
                comments.append("del "+self.name)

        class Test_Resurrection(object):
            def __init__(self, name):
                self.name = name
            
            def __repr__(self):
                return "<"+self.name+">"

            def __del__(self):
                comments.append("del "+self.name)
                if hasattr(self, "toResurrect"):
                    resurrect.append(self)

        def clb(ref):
            comments.append("clb")

        def clb2(ref):
            comments.append("clb2 "+str(comments))

        a = Test_Finalizable("a")
        wa = weakref.ref(a, clb)
        self.assertEqual(wa(), a)
        c = Test_Resurrection("c")
        c.toResurrect = a
        wc = weakref.ref(c, clb2)
        try:
            gc.monitorObject(c)
            gc.addJythonGCFlags(gc.DONT_FINALIZE_RESURRECTED_OBJECTS)
        except Exception:
            pass
        del a
        del c
        gc.collect()
        self.assertIn('del c', comments)
        self.assertNotIn('del a', comments)
        self.assertIn('clb2 []', comments)
        self.assertNotIn("clb", comments)
        self.assertEqual(str(resurrect), "[<c>]")
        self.assertEqual(str(wa()), "<a>")
        self.assertEqual(wc(), None)
        try:
            gc.removeJythonGCFlags(gc.DONT_FINALIZE_RESURRECTED_OBJECTS)
        except Exception:
            pass

    @unittest.skipUnless(test_support.is_jython, '')
    def test_weakref_after_resurrection_threadsafe(self):
        resurrect = []
        comments = []

        class Test_Finalizable(object):
            def __init__(self, name):
                self.name = name

            def __repr__(self):
                return "<"+self.name+">"

            def __del__(self):
                comments.append("del "+self.name)

        class Test_Resurrection(object):
            def __init__(self, name):
                self.name = name
            
            def __repr__(self):
                return "<"+self.name+">"

            def __del__(self):
                comments.append("del "+self.name)
                if hasattr(self, "toResurrect"):
                    resurrect.append(self)

        a = Test_Finalizable("a")
        wa = weakref.ref(a)
        c = Test_Resurrection("c")
        c.toResurrect = a
        wc = weakref.ref(c)
        del a
        del c
        try:
            gc.addJythonGCFlags(gc.PRESERVE_WEAKREFS_ON_RESURRECTION)
            System.gc()
            # We intentionally don't wait here, but want to observe
            # the situation with gc unfinnished. Note that wa() preserves
            # its result right away, due to thread-safe implementation.
            # Technically, the weak reference breaks and is restored after
            # gc-run finishes. However wa() blocks until the referent is
            # restored or the deletion is confirmed.
        except Exception:
            pass
        self.assertEqual(comments, [])
        self.assertEqual(resurrect, [])
        while comments == [] or resurrect == []:
            self.assertEqual(str(wa()), '<a>')
            self.assertEqual(wc(), None)
        self.assertEqual(str(wa()), '<a>')
        self.assertEqual(wc(), None)


@unittest.skipUnless(test_support.is_jython,
        '''
        The test involves Java-classes and is thus not supported by
        non-Jython interpreters.
        ''')
class GCTests_Jy_TraverseByReflection(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #Jython-specific block:
        try:
            cls.savedJythonGCFlags = gc.getJythonGCFlags()
            gc.addJythonGCFlags(gc.SUPPRESS_TRAVERSE_BY_REFLECTION_WARNING)
            gc.setMonitorGlobal(True)
        except Exception:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            gc.setJythonGCFlags(cls.savedJythonGCFlags)
            gc.stopMonitoring()
        except Exception:
            pass

    def test_TraverseByReflection(self):
        gc.collect()

        prt = GCTestHelper.reflectionTraverseTestField()
        del prt
        self.assertEqual(gc.collect(), 1)

        prt = GCTestHelper.reflectionTraverseTestList()
        del prt
        self.assertEqual(gc.collect(), 1)

        prt = GCTestHelper.reflectionTraverseTestArray()
        del prt
        self.assertEqual(gc.collect(), 1)

        prt = GCTestHelper.reflectionTraverseTestPyList()
        del prt
        self.assertEqual(gc.collect(), 2)

        prt = GCTestHelper.reflectionTraverseTestCycle()
        del prt
        self.assertEqual(gc.collect(), 0)


@unittest.skipUnless(test_support.is_jython,
        '''
        The test involves Jython-specifics and is thus not supported by
        non-Jython interpreters.
        ''')
class GCTests_Misc(unittest.TestCase):

    # Test for issue 2337
    def test_queue(self):
        class X(object):
            def __init__(self, q):
                self.q = q
        x = X(Queue())
        gc.monitorObject(x)
        gc.collect()

    # Test for issue 2336
    def test_gc_null(self):
        WeakReferenceGC = Class.forName('org.python.modules.gc$WeakReferenceGC')
        # We have to actually construct the right type, the constructor is protected
        # and Jython doesn't expose that to us; we'd get a plain WeakReference
        # if we tried WeakReferenceGC()
        con = WeakReferenceGC.getDeclaredConstructors()[0]
        con.setAccessible(True)
        x = object()
        ref = con.newInstance(x)
        # It works to start with
        self.assertTrue(ref == ref)
        self.assertTrue(ref.get() is x)
        # Now clean up the referent
        del x
        while ref.get():
            gc.collect()
        self.assertIsNone(ref.get())
        # Boom!
        self.assertTrue(ref == ref)


def test_main():
    tests = (
        GCTests_Jy_CyclicGarbage,
        GCTests_Jy_preprocess_and_postprocess,
        GCTests_Jy_Delayed_Finalization,
        GCTests_Jy_Forced_Delayed_Finalization,
        GCTests_Jy_Raw_Forced_Delayed_Finalization,
        GCTests_Jy_Monitoring,
        GCTests_Jy_Weakref,
        GCTests_Jy_TraverseByReflection,
        GCTests_Misc,
        )
    test_support.run_unittest(*tests)

if __name__ == "__main__":
    unittest.main()

