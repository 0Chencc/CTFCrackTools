# The jarray module is mostly phased out, but it is still has one
# constructor function - zeros - that is not directly available in the
# array module.
#
# The equivalent of
# jarray.zeros(n, typecode)
# is
# array.array(typecode, itertools.repeat(0, n))
#
# however itertools.repeat does not define __len__ and therefore we
# have to first build out the zero sequence separately, then copy
# over. This overhead could be significant for large arrays.

import jarray
import itertools
import os
import unittest
from array import array
from test import test_support
from java.lang import String as JString
from java.util import Arrays


class ArrayJyTestCase(unittest.TestCase):

    def test_jarray(self):
        from java.lang import String
        
        self.assertEqual(sum(jarray.array(range(5), 'i')), 10)
        self.assertEqual(','.join(jarray.array([String("a"), String("b"), String("c")], String)), u'a,b,c')
        self.assertEqual(sum(jarray.zeros(5, 'i')), 0)
        self.assertEqual([x for x in jarray.zeros(5, String)], [None, None, None, None, None])

    def test_java_object_arrays(self):
        from array import zeros
        from java.lang import String
        from java.lang.reflect import Array
        jStringArr = array(String, [String("a"), String("b"), String("c")])
        self.assert_(
            Arrays.equals(jStringArr.typecode, 'java.lang.String'),
               "String array typecode of wrong type, expected %s, found %s" %
               (jStringArr.typecode, str(String)))
        self.assertEqual(zeros(String, 5), Array.newInstance(String, 5))

        import java.lang.String # require for eval to work
        self.assertEqual(jStringArr, eval(str(jStringArr)))

    def test_java_compat(self):
        from array import zeros
        from java.awt import Color
        hsb = Color.RGBtoHSB(0,255,255, None)
        self.assertEqual(hsb, array('f', [0.5,1,1]),
                         "output hsb float array does not correspond to input rgb values")

        rgb = apply(Color.HSBtoRGB, tuple(hsb))
        self.assertEqual(rgb, -0xff0001,
                         "output rgb bytes don't match input hsb floats")
        hsb1 = zeros('f', 3)
        Color.RGBtoHSB(0, 255, 255, hsb1)
        self.assertEqual(hsb, hsb1, "hsb float arrays were not equal")

    def test_java_roundtrip(self):
        # bug 1543
        from java.lang import Object
        x = array(Object, [0,1,2])
        x.append(3)
        y = array(Object, [x]) # forces an implicit __tojava__
        self.assertEqual(x, y[0], "Did not shrink to fit")


class ToFromfileTestCase(unittest.TestCase):

    def tearDown(self):
        if os.path.exists(test_support.TESTFN):
            os.remove(test_support.TESTFN)

    def test_tofromfile(self):
        # http://bugs.jython.org/issue1457
        x = array('i', range(5))
        with open(test_support.TESTFN, 'wb') as f:
            x.tofile(f)

        x = array('i', [])
        with open(test_support.TESTFN, 'r+b') as f:
            x.fromfile(f, 5)
            x *= 2
            x.tofile(f)

        with open(test_support.TESTFN, 'rb') as f:
            x.fromfile(f, 10)
            self.assertEqual(x, array('i', range(5) * 4))


class ArrayOpsTestCase(unittest.TestCase):

    def test_ops(self):
        # http://bugs.jython.org/issue1622
        class Foo(object):
            def __radd__(self, that):
                return '__radd__'
        ar = array('i', range(5))
        self.assertEqual('__radd__', ar + Foo())
        ar += Foo()
        self.assertEqual('__radd__', ar)

    def test_nonhashability(self):
        "array.array objects are not hashable"
        # http://bugs.jython.org/issue2451
        a = array('b', itertools.repeat(0, 100))
        with self.assertRaisesRegexp(TypeError, r"unhashable type: 'array.array'"):
            hash(a)


class ArrayConversionTestCase(unittest.TestCase):
    
    # Covers bugs raised in
    # http://bugs.jython.org/issue1780,
    # http://bugs.jython.org/issue2423

    def assertAsList(self, a, b):
        self.assertEqual(Arrays.asList(a), b)

    def test_boxing_conversion(self):
        "array objects support boxing, as they did in Jython 2.1"
        from java.lang import Integer

        self.assertAsList(jarray.array([1, 2, 3, 4, 5], Integer), [1, 2, 3, 4, 5])
        self.assertAsList(array(Integer, [1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])
        self.assertAsList(jarray.array([1, 2, 3, 4, 5], "i"), [1, 2, 3, 4, 5])
        self.assertAsList(array("i", [1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_auxillary_boxing(self):
        "PyArray is internally used to support boxing of iterators/iterables"
        self.assertAsList(xrange(5), [0, 1, 2, 3, 4])
        self.assertAsList(iter(xrange(5)), [0, 1, 2, 3, 4])
        self.assertAsList(list(xrange(5)), [0, 1, 2, 3, 4])
        self.assertAsList((i * 2 for i in xrange(5)), [0, 2, 4, 6, 8])
        self.assertAsList(iter((i * 2 for i in xrange(5))), [0, 2, 4, 6, 8])
        self.assertAsList(iter((i * 2 for i in xrange(5))), [0, 2, 4, 6, 8])
        self.assertAsList(itertools.chain('ABC', 'DEF'), ['A', 'B', 'C', 'D', 'E', 'F'])

    def test_object_varargs(self):
        "array.array objects can be used in the varargs position, with primitive boxing"
        a = array('i', range(5, 10))
        self.assertEqual(
            'arg 0=5, arg 1=6, arg 2=7, arg 3=8, arg 4=9',
            JString.format('arg 0=%d, arg 1=%d, arg 2=%d, arg 3=%d, arg 4=%d', [5, 6, 7, 8, 9]))

    def test_assignable_varargs(self):
        "array.array objects can be used in the varargs position"
        # modified from test case in http://bugs.jython.org/issue2423;
        from java.lang import Class
        from java.net import URL, URLClassLoader
        params = jarray.array([URL], Class)
        # URLClassLoader.addURL is protected, so workaround via reflection
        method = URLClassLoader.getDeclaredMethod('addURL', params)
        # and verify we got the right method after all
        self.assertEqual(method.name, "addURL")


def test_main():
    tests = [ToFromfileTestCase, ArrayOpsTestCase, ArrayConversionTestCase]
    if test_support.is_jython:
        tests.extend([ArrayJyTestCase])
    test_support.run_unittest(*tests)


if __name__ == "__main__":
    test_main()
