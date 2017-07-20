import unittest

from test import test_support

from java.awt import Dimension
from java.awt.event import ActionEvent
from java.lang import Integer, String
from java.lang.Math import abs
from java.math import BigInteger
from java.util import Vector
from javax import swing

from javatests import ListTest

class PyListTest(ListTest):

    def __init__(self):
        ListTest.__init__(self)

    def newInstance(self, coll):
        if coll is None:
            return list()
        else:
            return list(coll)

    def isReadOnly(self):
        return False


class PyTupleTest(ListTest):

    def __init__(self):
        ListTest.__init__(self)

    def newInstance(self, coll):
        if coll is None:
            return tuple()
        else:
            return tuple(coll)

    def isReadOnly(self):
        return True


class JythonBasicTests(unittest.TestCase):

    def test_numbers(self):
        self.assertEquals(abs(-2.), 2., 'Python float to Java double')
        self.assertEquals(abs(-2), 2l, 'Python int to Java long')
        self.assertEquals(abs(-2l), 2l, 'Python long to Java long')

        try:
            abs(-123456789123456789123l)
        except TypeError:
            pass

    def test_strings(self):
        self.assertEquals(Integer.valueOf('42'), 42,
                          'Python string to Java string')

    def test_arrays(self):
        chars = ['a', 'b', 'c']
        self.assertEquals(String.valueOf(chars), 'abc', 'char array')

    def test_enumerations(self):
        vec = Vector()
        items = range(10)
        for i in items:
            vec.addElement(i)

        expected = 0
        for i in vec:
            self.assertEquals(i, expected,
                              'testing __iter__ on java.util.Vector')
            expected = expected + 1

        expected = 0
        for i in iter(vec):
            self.assertEquals(i, expected, 'testing iter(java.util.Vector)')
            expected = expected + 1

    def test_java_objects(self):
        self.assertEquals(BigInteger('1234', 10).intValue(), 1234,
                                     'BigInteger(string)')
        self.assertEquals(BigInteger([0x11, 0x11, 0x11]).intValue(), 0x111111,
                                     'BigInteger(byte[])')
        self.assertEquals(BigInteger(-1, [0x11, 0x11, 0x11]).intValue(),
                                     -0x111111, 'BigInteger(int, byte[])')

    def test_call_static_methods(self):
        s1 = String.valueOf(['1', '2', '3'])
        s2 = String.valueOf('123')
        s3 = String.valueOf(123)
        s4 = String.valueOf(123l)
        s5 = String.valueOf(['0', '1', '2', '3', 'a', 'b'], 1, 3)
        self.assertEquals(s1, s2)
        self.assertEquals(s1, s3)
        self.assertEquals(s1, s4)
        self.assertEquals(s1, s5)

    def test_call_instance_methods(self):
        s = String('hello')
        self.assertTrue(s.regionMatches(1, 1, 'ell', 0, 3),
                        'method call with boolean true')
        self.assertTrue(s.regionMatches(0, 1, 'ell', 0, 3),
                        'method call with boolean false')
        self.assertTrue(s.regionMatches(1, 'ell', 0, 3),
                        'method call no boolean')

        self.assertTrue(s.regionMatches(1, 1, 'eLl', 0, 3),
                                        'method call ignore case')
        self.assertFalse(s.regionMatches(1, 'eLl', 0, 3), 'should ignore case')

    def test_get_set(self):
        d = Dimension(3, 9)
        self.assertEquals(d.width, 3)
        self.assertEquals(d.height, 9)
        d.width = 42
        self.assertEquals(d.width, 42)
        self.assertEquals(d.height, 9)

        try:
            d.foo
        except AttributeError:
            pass
        else:
            raise AssertionError('d.foo should throw type error')

    # Used in test_java_bean_properties.
    flag = 0

    def test_java_bean_properties(self):

        b1 = swing.JButton()
        b1.label = 'foo'
        b2 = swing.JButton(label='foo')
        self.assertEquals(b1.label, b2.label)
        self.assertEquals(b1.label, 'foo')

        # Test bean event properties - single and multiple
        def testAction(event):
            JythonBasicTests.flag += 1

        doit = ActionEvent(b1, ActionEvent.ACTION_PERFORMED, "")

        b1.actionPerformed = testAction
        JythonBasicTests.flag = 0
        b1.doClick()
        self.assertEquals(
            JythonBasicTests.flag, 1,
            'expected one action per event but got %s' % JythonBasicTests.flag)

        b1.actionPerformed.append(testAction)
        JythonBasicTests.flag = 0
        b1.doClick()
        self.assertEquals(JythonBasicTests.flag, 2, 'two actions per event')

        b1.actionPerformed = testAction
        JythonBasicTests.flag = 0
        b1.doClick()
        self.assertEquals(JythonBasicTests.flag, 1,
                          'one actions per event - again')

    def test_anonymous_inner_classes(self):
        import javatests.AnonInner
        x = javatests.AnonInner()
        self.assertEquals(x.doit(), 2000)

    def test_javalists(self):
        # these first two tests just verify that we have a good unit test
        alt = ListTest.getArrayListTest(False)
        alt.testAll()

        alt = ListTest.getArrayListTest(True)
        alt.testAll()

        # Now run the tests
        plt = PyListTest()
        plt.testAll()
        ptt = PyTupleTest()
        ptt.testAll()

def test_main():
    test_support.run_unittest(JythonBasicTests)

if __name__ == '__main__':
    test_main()
