'''
Created on 06.08.2014
'''

import unittest
import types
import time
try:
    from java.lang import System
except:
    pass

class GCDetector():
    gcIndex = 0
    
    def __del__(self):
        GCDetector.gcIndex += 1

maxGCRun = 10

def runGCIfJython():
    try:
        currentIndex = GCDetector.gcIndex
        gcCount = 0
        detector = GCDetector()
        detector = None
        while currentIndex == GCDetector.gcIndex and gcCount < maxGCRun:
            System.gc()
            gcCount += 1
            time.sleep(0.1)
    except:
        pass

finalizeMsgList = []
verbose = False
resurrectedObject_I = None
resurrectedObject_J = None
resurrectedObject_K = None
resurrectedObject_L = None
resurrectedObject_M = None
resurrectedObject_N = None

class ResurrectableDummyClass():

    def __init__(self, name):
        self.name = name
        self.doResurrection = True

    def __str__(self):
        return self.name


class ResurrectableDummyClassNew(object):

    def __init__(self, name):
        self.name = name
        self.doResurrection = True

    def __str__(self):
        return self.name


def __del__I(self):
    global resurrectedObject_I
    finalizeMsgList.append(str(self)+" finalized (ResurrectableDummyClass)")
    if verbose:
        print str(self)+" finalized (ResurrectableDummyClass)"
    if self.doResurrection:
        resurrectedObject_I = self

def __del__J(self):
    global resurrectedObject_J
    finalizeMsgList.append(str(self)+" finalized (ResurrectableDummyClass)")
    if verbose:
        print str(self)+" finalized (ResurrectableDummyClass)"
    if self.doResurrection:
        resurrectedObject_J = self

def __del__K(self):
    global resurrectedObject_K
    finalizeMsgList.append(str(self)+" finalized (ResurrectableDummyClass)")
    if verbose:
        print str(self)+" finalized (ResurrectableDummyClass)"
    if self.doResurrection:
        resurrectedObject_K = self

def __del__L(self):
    global resurrectedObject_L
    finalizeMsgList.append(str(self)+" finalized (ResurrectableDummyClass)")
    if verbose:
        print str(self)+" finalized (ResurrectableDummyClass)"
    if self.doResurrection:
        resurrectedObject_L = self

def __del__M(self):
    global resurrectedObject_M
    finalizeMsgList.append(str(self)+" finalized (ResurrectableDummyClass)")
    if verbose:
        print str(self)+" finalized (ResurrectableDummyClass)"
    if self.doResurrection:
        resurrectedObject_M = self

def __del__N(self):
    global resurrectedObject_N
    finalizeMsgList.append(str(self)+" finalized (ResurrectableDummyClass)")
    if verbose:
        print str(self)+" finalized (ResurrectableDummyClass)"
    if self.doResurrection:
        resurrectedObject_N = self

delI = __del__I
delJ = __del__J
delK = __del__K
delL = __del__L
delM = __del__M
delN = __del__N


class DummyClass():
    
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return self.name


class DummyClassDel():
    
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return self.name
    
    def __del__(self):
        finalizeMsgList.append(str(self)+" finalized (DummyClassDel)")
        if verbose:
            print str(self)+" finalized (DummyClassDel)"


class DummyClassNew(object):
    
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return self.name

class DummyClassDelNew(object):
    
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return self.name
    
    def __del__(self):
        finalizeMsgList.append(str(self)+" finalized (DummyClassDelNew)")
        if verbose:
            print str(self)+" finalized (DummyClassDelNew)"

class DummyFileClassNew(file):
    
    def __init__(self, name):
        self.name0 = name
    
    def __str__(self):
        return self.name0

    def __del__(self):
        finalizeMsgList.append(str(self)+" finalized (DummyFileClassNew)")
        if verbose:
            print str(self)+" finalized (DummyFileClassNew)"


def __del__class(self):
    finalizeMsgList.append(str(self)+" finalized (acquired by class)")
    if verbose:
        print str(self)+" finalized (acquired by class)"

def __del__object(self):
    finalizeMsgList.append(str(self)+" finalized (acquired by object)")
    if verbose:
        print str(self)+" finalized (acquired by object)"

def __del__object0():
    finalizeMsgList.append("_ finalized (acquired by object)")
    if verbose:
        print "_ finalized (acquired by object)"

delClass = __del__class
delObject = __del__object
delObject0 = __del__object0

class TestFinalizers(unittest.TestCase):
    def test_finalizer_builtin_oldStyleClass(self):
        A = DummyClassDel("A")
        A = None
        runGCIfJython()
        self.assertIn("A finalized (DummyClassDel)", finalizeMsgList)

    def test_classAcquiresFinalizer_beforeInstanciation_oldStyleClass(self):
        DummyClass.__del__ = delClass
        B = DummyClass("B")
        B = None
        runGCIfJython()
        self.assertIn("B finalized (acquired by class)", finalizeMsgList)
        del DummyClass.__del__

    def test_classAcquiresFinalizer_afterInstanciation_oldStyleClass(self):
        #okay to fail in Jython without the manual __ensure_finalizer__ call
        C = DummyClass("C")
        DummyClass.__del__ = delClass
        try:
            C.__ensure_finalizer__()
        except:
            pass
        C = None
        runGCIfJython()
        self.assertIn("C finalized (acquired by class)", finalizeMsgList)
        del DummyClass.__del__

    def test_instanceAcquiresFinalizer_bound_oldStyleClass(self):
        D = DummyClassDel("D")
        dl = types.MethodType(delObject, D.name)
        D.__del__ = dl
        D = None
        runGCIfJython()
        self.assertNotIn("D finalized (DummyClassDel)", finalizeMsgList)
        self.assertIn("D finalized (acquired by object)", finalizeMsgList)

    def test_finalizer_builtin_newStyleClass(self):
        E = DummyClassDelNew("E")
        E = None
        runGCIfJython()
        self.assertIn("E finalized (DummyClassDelNew)", finalizeMsgList)

    def test_classAcquiresFinalizer_beforeInstanciation_newStyleClass(self):
        DummyClassNew.__del__ = delClass
        F = DummyClassNew("F")
        F = None
        runGCIfJython()
        self.assertIn("F finalized (acquired by class)", finalizeMsgList)
        del DummyClassNew.__del__

    def test_classAcquiresFinalizer_afterInstanciation_newStyleClass(self):
        #okay to fail in Jython without the manual __ensure_finalizer__ call
        G = DummyClassNew("G")
        DummyClassNew.__del__ = delClass
        try:
            G.__ensure_finalizer__()
        except:
            pass
        G = None
        runGCIfJython()
        self.assertIn("G finalized (acquired by class)", finalizeMsgList)
        del DummyClassNew.__del__

    def test_instanceAcquiresFinalizer_bound_newStyleClass(self):
        """
        It seems, CPython prohibits new style instances from acquiring a finalizer.
        """
        H = DummyClassDelNew("H")
        H.__del__ = types.MethodType(delObject, H.name)
        H = None
        runGCIfJython()
        self.assertIn("H finalized (DummyClassDelNew)", finalizeMsgList)
        self.assertNotIn("H finalized (acquired by object)", finalizeMsgList)

    def test_instanceAcquiresFinalizer_bound_newStyleClass2(self):
        """
        In CPython, new style instances can't acquire a finalizer.
        If one calls the instance-acquired __del__ manually, it works, but the gc
        will still call the old one.
        """
        H = DummyClassDelNew("H2")
        H.__del__ = types.MethodType(delObject, H.name)
        H.__del__()
        H = None
        runGCIfJython()
        self.assertIn("H2 finalized (DummyClassDelNew)", finalizeMsgList)
        self.assertIn("H2 finalized (acquired by object)", finalizeMsgList)

    def test_objectResurrection_oldStyleClass(self):
        ResurrectableDummyClass.__del__ = delI
        I = ResurrectableDummyClass("I")
        I = None
        runGCIfJython()
        self.assertIn("I finalized (ResurrectableDummyClass)", finalizeMsgList)
        self.assertEqual(str(resurrectedObject_I), "I")

    def test_objectDoubleResurrection_oldStyleClass(self):
        #okay to fail in Jython without the manual ensureFinalizer calls
        ResurrectableDummyClass.__del__ = delJ
        J = ResurrectableDummyClass("J")
        J = None
        
        runGCIfJython()
        self.assertIn("J finalized (ResurrectableDummyClass)", finalizeMsgList)
        global resurrectedObject_J
        self.assertEqual(str(resurrectedObject_J), "J")
        J = resurrectedObject_J
        resurrectedObject_J = None
        self.assertIsNone(resurrectedObject_J)
        try:
            #For Jython one can restore the finalizer manually.
            #This is offered as an easy fix if the CPython behavior
            #in this test should be needed for some reason.
            J.__ensure_finalizer__()
        except:
            pass
        J = None

        runGCIfJython()
        self.assertEqual(str(resurrectedObject_J), "J")
        resurrectedObject_J.doResurrection = False
        try:
            #again...
            resurrectedObject_J.__ensure_finalizer__()
        except:
            pass
        resurrectedObject_J = None
        
        runGCIfJython()
        self.assertIsNone(resurrectedObject_J)
        

    def test_objectDoubleResurrectionAndFinalize_oldStyleClass(self):
        #okay to fail in Jython without the manual __ensure_finalizer__ calls
        ResurrectableDummyClass.__del__ = delK
        K = ResurrectableDummyClass("K")
        K = None

        runGCIfJython()
        self.assertIn("K finalized (ResurrectableDummyClass)", finalizeMsgList)
        finalizeMsgList.remove("K finalized (ResurrectableDummyClass)")
        self.assertNotIn("K finalized (ResurrectableDummyClass)", finalizeMsgList)
        global resurrectedObject_K
        self.assertEqual(str(resurrectedObject_K), "K")
        K = resurrectedObject_K
        resurrectedObject_K = None
        self.assertIsNone(resurrectedObject_K)
        try:
            K.__ensure_finalizer__()
        except:
            pass
        K = None

        runGCIfJython()
        self.assertIn("K finalized (ResurrectableDummyClass)", finalizeMsgList)
        self.assertEqual(str(resurrectedObject_K), "K")

    def test_objectResurrection_newStyleClass(self):
        ResurrectableDummyClassNew.__del__ = delL
        L = ResurrectableDummyClassNew("L")
        L = None
        runGCIfJython()
        self.assertIn("L finalized (ResurrectableDummyClass)", finalizeMsgList)
        self.assertEqual(str(resurrectedObject_L), "L")

    def test_objectDoubleResurrection_newStyleClass(self):
        #okay to fail in Jython without the manual __ensure_finalizer__ calls
        ResurrectableDummyClassNew.__del__ = delM
        M = ResurrectableDummyClassNew("M")
        M = None

        runGCIfJython()
        self.assertIn("M finalized (ResurrectableDummyClass)", finalizeMsgList)
        global resurrectedObject_M
        self.assertEqual(str(resurrectedObject_M), "M")
        M = resurrectedObject_M
        resurrectedObject_M = None
        self.assertIsNone(resurrectedObject_M, None)
        try:
            M.__ensure_finalizer__()
        except:
            pass
        M = None

        runGCIfJython()
        self.assertEqual(str(resurrectedObject_M), "M")

    def test_objectDoubleResurrectionAndFinalize_newStyleClass(self):
        #okay to fail in Jython without the manual __ensure_finalizer__ calls
        ResurrectableDummyClassNew.__del__ = delN
        N = ResurrectableDummyClassNew("N")
        N = None

        runGCIfJython()
        self.assertIn("N finalized (ResurrectableDummyClass)", finalizeMsgList)
        finalizeMsgList.remove("N finalized (ResurrectableDummyClass)")
        self.assertNotIn("N finalized (ResurrectableDummyClass)", finalizeMsgList)
        global resurrectedObject_N
        self.assertEqual(str(resurrectedObject_N), "N")
        N = resurrectedObject_N
        resurrectedObject_N = None
        self.assertIsNone(resurrectedObject_N)
        try:
            N.__ensure_finalizer__()
        except:
            pass
        N = None

        runGCIfJython()
        self.assertIn("N finalized (ResurrectableDummyClass)", finalizeMsgList)
        self.assertEqual(str(resurrectedObject_N), "N")

    def test_file_overwrite_del(self):
        O = DummyFileClassNew("O")
        O = None

        runGCIfJython()
        self.assertIn("O finalized (DummyFileClassNew)", finalizeMsgList)

if __name__ == '__main__':
    unittest.main()

