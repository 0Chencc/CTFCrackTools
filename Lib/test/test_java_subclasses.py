'''Tests subclassing Java classes in Python'''
import os
import sys
import threading
import unittest

from test import test_support

from java.lang import (Boolean, Class, ClassLoader, Comparable,Integer, Object, Runnable, String,
                       Thread, ThreadGroup, InterruptedException, UnsupportedOperationException)
from java.util import AbstractList, ArrayList, Date, Hashtable, HashSet, Vector
from java.util.concurrent import Callable, Executors

from java.awt import Color, Component, Dimension, Rectangle
from javax.swing import ComboBoxModel, ListModel
from javax.swing.table import AbstractTableModel
from javax.swing.tree import DefaultTreeModel, DefaultMutableTreeNode

from org.python.tests import BeanInterface, Callbacker, Coercions, OwnMethodCaller
from javatests import (
    InheritanceA, InheritanceB, InheritanceC, InheritanceD,
    ExtendedInterface, UseExtendedInterface)


class InterfaceTest(unittest.TestCase):
    def test_java_calling_python_interface_implementation(self):
        called = []
        class PyCallback(Callbacker.Callback):
            def call(self, extraarg=None):
                called.append(extraarg)
        Callbacker.callNoArg(PyCallback())
        Callbacker.callOneArg(PyCallback(), 4294967295L)
        self.assertEquals(None, called[0])
        self.assertEquals(4294967295L, called[1])
        class PyBadCallback(Callbacker.Callback):
            def call(pyself, extraarg):
                self.fail("Shouldn't be callable with a no args")
        self.assertRaises(TypeError, Callbacker.callNoArg, PyBadCallback())

    def test_inheriting_from_python_and_java_interface(self):
        calls = []
        class Runner(Runnable):
            def run(self):
                calls.append("Runner.run")

        class ComparableRunner(Comparable, Runner):
            def compareTo(self, other):
                calls.append("ComparableRunner.compareTo")
                return 0

        c = ComparableRunner()
        c.compareTo(None)
        c.run()
        self.assertEquals(calls, ["ComparableRunner.compareTo", "Runner.run"])

    def test_inherit_interface_twice(self):
        # http://bugs.jython.org/issue1504
        class A(ListModel): pass
        class B(A, ComboBoxModel): pass
        # Regression caused B's proxy to occur in B's mro twice. That
        # caused the declaration of C to fail with an inconsistent mro
        class C(B): pass
        

class TableModelTest(unittest.TestCase):
    def test_class_coercion(self):
        '''Python type instances coerce to a corresponding Java wrapper type in Object.getClass'''
        class TableModel(AbstractTableModel):
            columnNames = "First Name", "Last Name","Sport","# of Years","Vegetarian"
            data = [("Mary", "Campione", "Snowboarding", 5, False)]

            def getColumnCount(self):
                return len(self.columnNames)

            def getRowCount(self):
                return len(self.data)

            def getColumnName(self, col):
                return self.columnNames[col]

            def getValueAt(self, row, col):
                return self.data[row][col]

            def getColumnClass(self, c):
                return Object.getClass(self.getValueAt(0, c))

            def isCellEditable(self, row, col):
                return col >= 2

        model = TableModel()
        for i, expectedClass in enumerate([String, String, String, Integer, Boolean]):
            self.assertEquals(expectedClass, model.getColumnClass(i))

class AutoSuperTest(unittest.TestCase):
    def test_auto_super(self):
        class Implicit(Rectangle):
            def __init__(self):
                self.size = Dimension(6, 7)
        class Explicit(Rectangle):
            def __init__(self):
                Rectangle.__init__(self, 6, 7)
        self.assert_("width=6,height=7" in Implicit().toString())
        self.assert_("width=6,height=7" in Explicit().toString())

    def test_no_default_constructor(self):
        "Check autocreation when java superclass misses a default constructor."
        class A(ThreadGroup):
            def __init__(self):
                print self.name
        self.assertRaises(TypeError, A)

# The no-arg constructor for proxies attempts to look up its Python class by the Python class' name,
# so the class needs to be visible at the module level or the import will fail
class ModuleVisibleJavaSubclass(Object):
    pass
class PythonSubclassesTest(unittest.TestCase):
    def test_multiple_inheritance_prohibited(self):
        try:
            class MultiJava(Dimension, Color):
                pass
            self.fail("Shouldn't be able to subclass more than one concrete java class")
        except TypeError:
            pass

        class PyDim(Dimension):
            pass
        class PyDimRun(PyDim, Runnable):
            pass
        try:
            class PyDimRunCol(PyDimRun, Color):
                pass
            self.fail("Shouldn't be able to subclass more than one concrete java class")
        except TypeError:
            pass

    def test_multilevel_override(self):
        runs = []
        class SubDate(Date):
            def run(self):
                runs.append("SubDate")

            def method(self):
                return "SubDateMethod"

            def toString(self):
                s = Date.toString(self)
                return 'SubDate -> Date'

        class SubSubDate(SubDate, Runnable):
            def toString(self):
                return 'SubSubDate -> ' + SubDate.toString(self)

        self.assertEquals("SubDate -> Date", SubDate().toString())
        self.assertEquals("SubSubDate -> SubDate -> Date", SubSubDate().toString())
        self.assertEquals("SubDateMethod", SubSubDate().method())
        Coercions.runRunnable(SubSubDate())
        self.assertEquals(["SubDate"], runs)

    def test_passthrough(self):
        class CallbackPassthrough(Callbacker.Callback):
            def __init__(self, worker):
                self.worker = worker

            def __getattribute__(self, name):
                if name == 'call':
                    return getattr(self.worker, name)
                return object.__getattribute__(self, name)

        collector = Callbacker.CollectingCallback()
        c = CallbackPassthrough(collector)
        Callbacker.callNoArg(c)
        self.assertEquals("call()", collector.calls[0])
        c.call(7)
        self.assertEquals("call(7)", collector.calls[1])

    def test_Class_newInstance_works_on_proxies(self):
        Class.newInstance(ModuleVisibleJavaSubclass)

    def test_override(self):
        class Foo(Runnable):
            def toString(self): return "Foo"
        self.assertEquals(String.valueOf(Foo()), "Foo", "toString not overridden in interface")

        class A(Object):
            def toString(self):
                return 'name'
        self.assertEquals('name', String.valueOf(A()), 'toString not overriden in subclass')

    def test_can_subclass_abstract(self):
        class A(Component):
            pass
        A()

    def test_return_proxy(self):
        "Jython proxies properly return back from Java code"
        class FooVector(Vector):
            bar = 99

        ht = Hashtable()
        fv = FooVector()
        ht.put("a", fv)
        self.failUnless(fv is ht.get("a"))

    def test_proxy_generates_protected_methods(self):
        """Jython proxies should generate methods for protected methods on their superclasses

        Tests for bug #416871"""
        output = []
        class RegularBean(BeanInterface):
            def __init__(self):
                output.append("init")

            def getName(self):
                output.append("getName")
        class FinalizingBean(RegularBean):
            def finalize(self):
                pass
            def clone(self):
                return self.__class__()

        for a in FinalizingBean(), RegularBean():
            self.assertEquals("init", output.pop())
            a.getName()
            self.assertEquals("getName", output.pop())
            aa = a.clone()
            if isinstance(a, FinalizingBean):
                self.assertEquals("init", output.pop())
            aa.name
            self.assertEquals("getName", output.pop())

    def test_python_subclass_of_python_subclass_of_java_class_overriding(self):
        '''Test for http://bugs.jython.org/issue1297.

        Checks that getValue on SecondSubclass is overriden correctly when called from Java.'''
        class FirstSubclass(OwnMethodCaller):
            pass

        class SecondSubclass(FirstSubclass):
            def getValue(self):
                return 10

        self.assertEquals(10, SecondSubclass().callGetValue())


    def test_deep_subclasses(self):
        '''Checks for http://bugs.jython.org/issue1363.

        Inheriting several classes deep from a Java class caused inconsistent MROs.'''
        class A(Object): pass
        class B(A): pass
        class C(B): pass
        class D(C): pass
        d = D()

"""
public abstract class Abstract {
    public Abstract() {
        method();
    }

    public abstract void method();
}
"""
# The following is the correspoding bytecode for Abstract compiled with javac 1.5
ABSTRACT_CLASS = """\
eJw1TrsKwkAQnI1nEmMe/oKdSaHYiyCClWih2F+SQyOaQDz9LxsFCz/AjxL3Am6xw8zs7O7n+3oD
GKPnQcD30ELgIHQQEexJURZ6SmgN4h1BzKtcEaJlUarV9ZyqeivTEyv2WelDlRO8TXWtM7UojBrM
0ouuZaaHR3mTPtqwfXRgE9y/Q+gZb3SS5X60To8q06LPHwiYskAmxN1hFjMSYyd5gpIHrDsT3sU9
5IgZF4wuhCBzpnG9Ru/+AF4RJn8=
""".decode('base64').decode('zlib')

class AbstractOnSyspathTest(unittest.TestCase):
    '''Subclasses an abstract class that isn't on the startup classpath.

    Checks for http://jython.org/bugs/1861985
    '''
    def setUp(self):
        out = open('Abstract.class', 'wb')
        out.write(ABSTRACT_CLASS)
        out.close()
        self.orig_syspath = sys.path[:]
        sys.path.append('')

    def tearDown(self):
        os.unlink('Abstract.class')
        sys.path = self.orig_syspath

    def test_can_subclass_abstract(self):
        import Abstract

        class A(Abstract):
            def method(self):
                pass
        A()

"""
public abstract class ContextAbstract {
    public ContextAbstract() {
        method();
    }

    public abstract void method();
}
"""
# The following is the correspoding bytecode for ContextAbstract compiled with javac 1.5
# Needs to be named differently than Abstract above so the class loader won't just use it
CONTEXT_ABSTRACT = """\
eJxdTsEOwVAQnK2n1aq2Bz/ghgNxF4lInIQDcX9tX6jQJvWI33IhcfABPkrs69EedjKzM7v7+b7e
AEaIPAj4HmpoOQgchAR7nOWZnhBq3d6WIGZFqgjhIsvV8nKKVbmR8ZEV+6T0vkgJ3rq4lImaZ0Zt
z4pcq5uexmddykQPDvIqfdRh+3Bh86I/AyEyluFR5rvhKj6oRIsO/yNgygKZLHeHWY+RGN3+E9R/
wLozITS4BxwxdsHYgBBkrlVTr9KbP6qaLFc=
""".decode('base64').decode('zlib')
class ContextClassloaderTest(unittest.TestCase):
    '''Classes on the context classloader should be importable and subclassable.

    http://bugs.jython.org/issue1216'''
    def setUp(self):
        self.orig_context = Thread.currentThread().contextClassLoader
        class AbstractLoader(ClassLoader):
            def __init__(self):
                ClassLoader.__init__(self)
                c = self.super__defineClass("ContextAbstract", CONTEXT_ABSTRACT, 0,
                        len(CONTEXT_ABSTRACT), ClassLoader.protectionDomain)
                self.super__resolveClass(c)
        Thread.currentThread().contextClassLoader = AbstractLoader()

    def tearDown(self):
        Thread.currentThread().contextClassLoader = self.orig_context

    def test_can_subclass_abstract(self):
        import ContextAbstract

        called = []
        class A(ContextAbstract):
            def method(self):
                called.append(True)
        A()
        self.assertEquals(len(called), 1)


class MetaClass(type):
    def __new__(meta, name, bases, d):

        # Insert the method to be called from Java
        def call(self):
            return self.x

        d["call"] = call
        d["foo"] = 99
        return super(MetaClass, meta).__new__(meta, name, bases, d)


class MetaBase(object):
    __metaclass__ = MetaClass


class MetaClassTest(unittest.TestCase):

    def test_java_with_metaclass_base(self):
        """Java classes can be mixed with Python bases using metaclasses"""
        
        # Permute mixin order
        class Bar(MetaBase, Callable):
            def __init__(self, x):
                self.x = x

        class Baz(Callable, MetaBase):
            def __init__(self, x):
                self.x = x

        # Go through {bar|baz}.call indirectly through a Java path,
        # just to ensure this mixin provided by the metaclass is available
        pool = Executors.newSingleThreadExecutor()
        bar = Bar(42)
        self.assertEqual(bar.foo, 99)
        self.assertEqual(42, pool.submit(bar).get())
        baz = Baz(47)
        self.assertEqual(baz.foo, 99)
        self.assertEqual(47, pool.submit(baz).get())
        pool.shutdown()


class AbstractMethodTest(unittest.TestCase):

    def test_abstract_method_implemented(self):
        class C(AbstractList):
            def get(self, index):
                return index * 2
            def size(self):
                return 7

        c = C()
        self.assertEqual(c.size(), 7)
        self.assertEqual([c.get(i) for i in xrange(7)], range(0, 14, 2))

    def test_abstract_method_not_implemented(self):
        class C(AbstractList):
            def size(self):
                return 47

        # note that unlike ABCs in Python - or partial extensions
        # of abstract classes in Java - we allow such classes to
        # be instantiated. We may wish to change this in Jython
        # 3.x
        c = C()
        self.assertEqual(c.size(), 47)
        msg = r"^'C' object does not implement abstract method 'get' from 'java.util.AbstractList'$"
        with self.assertRaisesRegexp(NotImplementedError, msg):
            C().get(42)

    def test_concrete_method(self):
        class H(HashSet):
            def __init__(self):
                self.added = 0
                HashSet.__init__(self)

            def add(self, value):
                self.added += 1
                HashSet.add(self, value)

        h = H()
        h.add(42)
        h.add(47)
        h.discard(47)
        self.assertEqual(list(h), [42])
        self.assertEqual(h.added, 2)

    def test_interface_method_implemented(self):
        class C(Callable):
            def call(self):
                return 42

        self.assertEqual(C().call(), 42)

    def test_interface_method_not_implemented(self):
        class C(Callable):
            pass
        
        msg = r"^'C' object does not implement abstract method 'call' from 'java.util.concurrent.Callable'$"
        with self.assertRaisesRegexp(NotImplementedError, msg):
            C().call()


class SuperIsSuperTest(unittest.TestCase):
    # Testing how the vision described in Raymond Hettinger's blog
    # https://rhettinger.wordpress.com/2011/05/26/super-considered-super/
    # - super in Python is really next-method - can be merged with
    # Java's super, which is a conventional super that dispatches up
    # the class inheritance hierarchy
    
    def test_super_dispatches_through_proxy(self):
        # Verify fix for http://bugs.jython.org/issue1540
        
        class MyList(ArrayList):

            def get(self, index):
                return super(MyList, self).get(index)

            def toString(self):
                return "MyList<<<" + super(MyList, self).toString() + ">>>"
        
        my_list = MyList([0, 1, 2, 3, 4, 5])
        self.assertEqual(my_list.get(5), 5)
        self.assertEqual(
            str(my_list),
            "MyList<<<[0, 1, 2, 3, 4, 5]>>>")
        self.assertEqual(my_list.size(), 6)


class HierarchyTest(unittest.TestCase):

    # Attempt to expand upon the inheritance hierarchy described as
    # being a bug in http://bugs.jython.org/issue2104, but this test
    # currently only confirms existing behavior.

    def assertB(self, b2, level, cls):
        self.assertIsInstance(b2, cls)
        self.assertEqual(b2.whoAmI(), level)
        self.assertEqual(b2.staticWhoAmI(), level)
        self.assertEqual(b2.root(), "A")
        self.assertEqual(b2.staticRoot(), "A")
        self.assertEqual(b2.everyOther(), "A")
        self.assertEqual(b2.notInAbstract(), "B")

    def test_b(self):
        b = InheritanceB()
        self.assertB(b.replicateMe(), "B", InheritanceB)
        self.assertB(b.build(), "B", InheritanceB)
        with self.assertRaises(UnsupportedOperationException):
            b.replicateParent()
        with self.assertRaises(UnsupportedOperationException):
            b.buildParent()

    def assertC(self, c2, level, cls):
        self.assertIsInstance(c2, cls)
        self.assertEqual(c2.whoAmI(), level)
        self.assertEqual(c2.staticWhoAmI(), level)
        self.assertEqual(c2.root(), "A")
        self.assertEqual(c2.staticRoot(), "A")
        self.assertEqual(c2.everyOther(),
                         "C" if isinstance(c2, InheritanceC) else "A")
        self.assertEqual(c2.notInAbstract(), "B")

    def test_c(self):
        c = InheritanceC()
        self.assertC(c.replicateMe(), "C", InheritanceC)
        self.assertC(c.replicateParent(), "B", InheritanceB)
        self.assertC(c.build(), "C", InheritanceC)
        self.assertC(c.buildParent(), "B", InheritanceB)

    def assertD(self, d2, level, cls):
        self.assertIsInstance(d2, cls)
        self.assertEqual(d2.whoAmI(), level)
        self.assertEqual(d2.staticWhoAmI(), level)
        self.assertEqual(d2.root(), "A")
        self.assertEqual(d2.staticRoot(), "A")
        self.assertEqual(d2.everyOther(), "C")
        self.assertEqual(d2.notInAbstract(), "B")

    def test_d(self):
        d = InheritanceD()
        self.assertD(d.replicateMe(), "D", InheritanceD)
        self.assertD(d.replicateParent(), "C", InheritanceC)
        self.assertD(d.build(), "D", InheritanceD)
        self.assertD(d.buildParent(), "C", InheritanceC)

    def assertE(self, e2, level, cls, tested):
        self.assertIsInstance(e2, cls)
        self.assertEqual(e2.whoAmI(), level)
        self.assertEqual(e2.staticWhoAmI(), level)
        self.assertEqual(e2.root(), "A")
        self.assertEqual(e2.staticRoot(), "A")
        self.assertEqual(e2.everyOther(),
                         "E" if isinstance(e2, tested) else "C")
        self.assertEqual(e2.notInAbstract(), "B")

    def test_e(self):
        class E(InheritanceD):
            def replicateMe(self):
                return E()
            def replicateParent(self):
                return InheritanceD()
            @staticmethod
            def build():
                return E()
            @staticmethod
            def buildParent():
                return InheritanceD()
            def whoAmI(self):
                return "E"
            @staticmethod
            def staticWhoAmI():
                return "E"
            def everyOther(self):
                return "E"

        e = E()
        self.assertE(e.replicateMe(), "E", E, E)
        self.assertE(e.replicateParent(), "D", InheritanceD, E)
        self.assertE(e.build(), "E", E, E)
        self.assertE(e.buildParent(), "D", InheritanceD, E)


class ChooseCorrectToJavaTest(unittest.TestCase):

    # Verifies fix for http://bugs.jython.org/issue1795
    #
    # Note that we use threading.Thread because we have imported
    # java.lang.Thread as Thread

    def test_extended_thread(self):

        class ExtendedThread(threading.Thread, ExtendedInterface):
            def returnSomething(self):
                return "yo yo yo"

        result = [None]
        def f(r):
            r[0] = 47

        t = ExtendedThread(target=f, args=(result,))
        self.assertEqual(
            UseExtendedInterface().countWords(t),
            3)

        # Also verify that t still works as a regular thread
        t.start()
        t.join()
        self.assertFalse(t.isAlive())
        self.assertEqual(result[0], 47)

    def test_interruption(self):
        # based on this code http://www.jython.org/jythonbook/en/1.0/Concurrency.html#interruption,
        # which demonstrates __tojava__ works properly

        class ExtendedThread(threading.Thread, ExtendedInterface):
            def returnSomething(self):
                return "yo yo yo"

        def wait_until_interrupted(cv):
            with cv:
                while not Thread.currentThread().isInterrupted():
                    try:
                        # this condition variable is never notified, so will only
                        # succeed if interrupted
                        cv.wait()
                    except InterruptedException, e:
                        break

        unfair_condition = threading.Condition()
        threads = [
           ExtendedThread(
                name="thread #%d" % i,
                target=wait_until_interrupted,
                args=(unfair_condition,))
            for i in xrange(5)]

        for thread in threads:
            thread.start()
        for thread in threads:
            Thread.interrupt(thread)
        for thread in threads:
            thread.join(5)
        
        # this assertion only succeeds if threads terminated because
        # they were interrupted
        for thread in threads:
            self.assertFalse(thread.isAlive())


class OldAndNewStyleInitSuperTest(unittest.TestCase):
    """
    http://bugs.jython.org/issue2375
    """

    def test_new_style_init(self):
        class AModel(DefaultTreeModel):
            def __init__(self):
                super(AModel, self).__init__(DefaultMutableTreeNode())

        AModel()

    def test_old_style_init(self):
        class AModel(DefaultTreeModel):
            def __init__(self):
                DefaultTreeModel.__init__(self, DefaultMutableTreeNode())

        AModel()

def test_main():
    test_support.run_unittest(
        InterfaceTest,
        TableModelTest,
        AutoSuperTest,
        PythonSubclassesTest,
        AbstractOnSyspathTest,
        ContextClassloaderTest,
        MetaClassTest,
        AbstractMethodTest,
        SuperIsSuperTest,
        OldAndNewStyleInitSuperTest,
        HierarchyTest,
        ChooseCorrectToJavaTest)


if __name__ == '__main__':
    test_main()
