# test overloaded java methods dispatch logic in PyReflectedFunction
# needs to grow more tests. Uses javatests.JOverload as a bag of overloaded methods.
# (can be adapted to test alternative re-implemations even while they are developed
# write a *Envl class and change/add to to_test for that)

import sys
import unittest

import java
from java.util import ArrayList
from javatests import JOverload, Reflection
from org.python.core import PyReflectedFunction

class PyReflFuncEnvl:

    def __init__(self,name,meths):
        self.reflfunc = PyReflectedFunction(meths)

    def __call__(self,inst,args):
        return self.reflfunc(inst,*args)

def extract_ov_meths(jcl,envl_class):
    meths = java.lang.Class.getDeclaredMethods(jcl)
    names = [ m.name for m in meths]
    meth_dict = {}
    for name in names:
        if name.startswith('ov_') and not meth_dict.has_key(name):
            meth_dict[name] = envl_class(name,[ m for m in meths if m.name == name ])
    return meth_dict

jo = JOverload()

to_test = [extract_ov_meths(JOverload,PyReflFuncEnvl)]

class OverloadedDispatchTests(unittest.TestCase):

    def check(self,lbl,rng,args,expected):
        expected = expected.split()
        for meth_dict in to_test:
            for i,expect in zip(rng,expected):
                self.assertEqual(meth_dict['ov_%s%s' % (lbl,i)](jo,args),expect)

    def test_posprec(self):
        self.check('posprec',[1,2],[0,0],
                   "(int,long) (long,int)")

    def test_scal_int_zero(self):
        self.check('scal',xrange(1,15),[0],
                   """
(long)
(int)
(short)
(byte)
(byte)
(double)
(float)
(boolean)
(java.io.Serializable)
(java.io.Serializable)
(java.io.Serializable)
(java.io.Serializable)
(java.io.Serializable)
(java.lang.Object)
                   """)

    def test_scal_string(self):
        self.check('scal',xrange(1,15),['str'],
                   """
(java.lang.String)
(java.lang.String)
(java.lang.String)
(java.lang.String)
(java.lang.String)
(java.lang.String)
(java.lang.String)
(java.lang.String)
(java.lang.String)
(java.io.Serializable)
(java.io.Serializable)
(java.io.Serializable)
(java.io.Serializable)
(java.lang.Object)
                   """)

    def test_scal_char(self):
        self.check('scal',xrange(1,15),['c'],
                   """
(char)
(char)
(char)
(char)
(java.lang.String)
(java.lang.String)
(java.lang.String)
(java.lang.String)
(java.lang.String)
(java.io.Serializable)
(java.io.Serializable)
(java.io.Serializable)
(java.io.Serializable)
(java.lang.Object)
                   """)

    def test_scal_float_one(self):
        self.check('scal',xrange(1,15),[1.0],
                   """
(double)
(double)
(double)
(double)
(double)
(double)
(float)
(java.io.Serializable)
(java.io.Serializable)
(java.io.Serializable)
(java.io.Serializable)
(java.io.Serializable)
(java.io.Serializable)
(java.lang.Object)
                   """)


class VarargsDispatchTests(unittest.TestCase):

    def test_strings(self):
        t = Reflection.StringVarargs()
        self.assertEqual(t.test("abc", "xyz"),
                         "String...:[abc, xyz]")
        self.assertEqual(t.test("abc"),
                         "String...:[abc]")
        self.assertEqual(t.test(),
                         "String...:[]")

        self.assertEqual(t.test(["abc", "xyz"]),
                         "String...:[abc, xyz]")
        self.assertEqual(t.test(["abc"]),
                         "String...:[abc]")
        self.assertEqual(t.test([]),
                         "String...:[]")


    def test_lists(self):
        t = Reflection.ListVarargs()
        self.assertEqual(t.test(ArrayList([1,2,3]), ArrayList([4,5,6])),
                         "List...:[[1, 2, 3], [4, 5, 6]]")
        self.assertEqual(t.test(ArrayList([1,2,3])),
                         "List...:[[1, 2, 3]]")
        self.assertEqual(t.test(),
                         "List...:[]")

        self.assertEqual(t.test([ArrayList([1,2,3]), ArrayList([4,5,6])]),
                         "List...:[[1, 2, 3], [4, 5, 6]]")
        self.assertEqual(t.test([ArrayList([1,2,3])]),
                         "List...:[[1, 2, 3]]")
        self.assertEqual(t.test([]),
                         "List...:[]")


class ComplexOverloadingTests(unittest.TestCase):

    def test_complex(self):
        o = Reflection.Overloaded()
        self.assertEqual(o(2.), "class java.lang.Double=2.0")
        self.assertEqual(o(1+2j), "class org.python.core.PyComplex=(1+2j)")



def printout(meth_dict,lbl,rng,args):
    for i in rng:
        print meth_dict['ov_%s%s' % (lbl,i)](jo,args)


if __name__ == '__main__' and not sys.argv[1:] == ['break-out']:
    try:
        import test_support
    except ImportError:
        unittest.main()
    else:
        test_support.run_unittest(OverloadedDispatchTests, VarargsDispatchTests, ComplexOverloadingTests)
