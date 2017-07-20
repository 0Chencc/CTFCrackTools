import unittest
from test import test_support, test_set

import pickle
import threading

from java.io import (ByteArrayInputStream, ByteArrayOutputStream,
                     ObjectInputStream, ObjectOutputStream)
from java.util import Random, HashSet, LinkedHashSet
from javatests import PySetInJavaTest


class SetTestCase(unittest.TestCase):

    def test_binops(self):
        class Foo(object):
            __rsub__ = lambda self, other: 'rsub'
            __ror__ = lambda self, other: 'ror'
            __rand__ = lambda self, other: 'rand'
            __rxor__ = lambda self, other: 'rxor'
        foo = Foo()
        s = set()
        self.assertEqual(s - foo, 'rsub')
        self.assertEqual(s | foo, 'ror')
        self.assertEqual(s & foo, 'rand')
        self.assertEqual(s ^ foo, 'rxor')

    def test_pop_race(self):
        # issue 1854
        nthreads = 200
        # the race might not happen the first time so we try a few just in case
        for i in xrange(4):
            s = set(range(200))
            threads = [threading.Thread(target=s.pop) for i in range(nthreads)]
            for t in threads: t.start()
            for t in threads: t.join()
            self.assertEqual(len(s), 0)

    def test_big_set(self):
        """Verify that fairly large collection literals of primitives can be constructed."""
        # use \n to separate to avoid parser problems
        s = eval("{" + ",\n".join((str(x) for x in xrange(64000))) +"}")
        self.assertEqual(len(s), 64000)
        self.assertEqual(sum(s), 2047968000)


class SetInJavaTestCase(unittest.TestCase):

    """Tests for derived dict behaviour"""

    def test_using_PySet_as_Java_Set(self):
        PySetInJavaTest.testPySetAsJavaSet()

    def test_accessing_items_added_in_java(self):
        s = PySetInJavaTest.createPySetContainingJavaObjects()
        for v in s:
            self.assert_(v in s)
            if isinstance(v, unicode):
                self.assertEquals("value", v)
            else:
                # Should be a java.util.Random; ensure we can call it
                v.nextInt()

    def test_java_accessing_items_added_in_python(self):
        # Test a type that should be coerced into a Java type, a Java
        # instance that should be wrapped, and a Python instance that
        # should pass through as itself with str, Random and tuple
        # respectively.
        s = set(["value", Random(), ("tuple", "of", "stuff")])
        PySetInJavaTest.accessAndRemovePySetItems(s)
        # Check that the Java removal affected the underlying set
        self.assertEquals(0, len(s))

    def test_serialization(self):
        s = set(range(5, 10))
        output = ByteArrayOutputStream()
        serializer = ObjectOutputStream(output)
        serializer.writeObject(s)
        serializer.close()

        input = ByteArrayInputStream(output.toByteArray())
        unserializer = ObjectInputStream(input)
        self.assertEqual(s, unserializer.readObject())


class TestJavaSet(test_set.TestSet):
    thetype = HashSet

    def test_init(self):
        # Instances of Java types cannot be re-initialized
        pass

    def test_cyclical_repr(self):
        pass

    def test_cyclical_print(self):
        pass

    def test_pickling(self):
        for i in range(pickle.HIGHEST_PROTOCOL + 1):
            p = pickle.dumps(self.s, i)
            dup = pickle.loads(p)
            self.assertEqual(self.s, dup, "%s != %s" % (self.s, dup))


class TestJavaHashSet(TestJavaSet):
    thetype = HashSet

class TestJavaLinkedHashSet(TestJavaSet):
    thetype = LinkedHashSet


def test_main():
    tests = [
        SetTestCase,
        SetInJavaTestCase,
        TestJavaHashSet,
        TestJavaLinkedHashSet,
    ]
    test_support.run_unittest(*tests)


if __name__ == '__main__':
    test_main()
