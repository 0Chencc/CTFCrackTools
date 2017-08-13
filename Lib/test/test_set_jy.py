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

class SetSubclassCallsSuperMethods(set):

    # Used to verify all call paths where there is more than one way
    # to call the super method, such as (union, __or__), etc
    
    def _valid_op_args(f):
        def _screener(*args):
            if len(args) != 2:
                raise TypeError()
            for arg in args:
                if not (isinstance(arg, set) or isinstance(arg, frozenset)):
                    raise TypeError()
            return f(*args)
        return _screener

    def _call_for_side_effects(f):
        def _mutating_convention(*args):
            f(*args)
            return None
        return _mutating_convention

    def issubset(self, other):
        return super(SetSubclassCallsSuperMethods, self).issubset(other)
        
    __le__ = issubset

    def issuperset(self, other):
        return super(SetSubclassCallsSuperMethods, self).issuperset(other)
        
    __ge__ = issuperset

    def union(self, *others):
        return super(SetSubclassCallsSuperMethods, self).union(*others)

    __or__ = _valid_op_args(union)

    def intersection(self, *others):
        return super(SetSubclassCallsSuperMethods, self).intersection(*others)

    __and__ = _valid_op_args(intersection)

    def difference(self, *others):
        return super(SetSubclassCallsSuperMethods, self).difference(*others)

    __sub__ = _valid_op_args(difference)

    def symmetric_difference(self, *others):
        return super(SetSubclassCallsSuperMethods, self).symmetric_difference(*others)

    __xor__ = _valid_op_args(symmetric_difference)

    def _update(self, *others):
        super(SetSubclassCallsSuperMethods, self).update(*others)
        return self

    update = _call_for_side_effects(_update)
    __ior__ = _update
        
    def _difference_update(self, *others):
        super(SetSubclassCallsSuperMethods, self).difference_update(*others)
        return self

    difference_update = _call_for_side_effects(_difference_update)
    __isub__ = _difference_update

    def _intersection_update(self, *others):
        super(SetSubclassCallsSuperMethods, self).intersection_update(*others)
        return self

    intersection_update = _call_for_side_effects(_intersection_update)
    __iand__ = _intersection_update

    def _symmetric_difference_update(self, other):
        super(SetSubclassCallsSuperMethods, self).symmetric_difference_update(other)
        return self

    symmetric_difference_update = _call_for_side_effects(_symmetric_difference_update)
    __ixor__ = _symmetric_difference_update


class TestSetSubclassCallsSuperMethods(test_set.TestSet):
    # verifies fix for http://bugs.jython.org/issue2357
    thetype = SetSubclassCallsSuperMethods


def test_main():
    tests = [
        SetTestCase,
        SetInJavaTestCase,
        TestJavaHashSet,
        TestJavaLinkedHashSet,
        TestSetSubclassCallsSuperMethods
    ]
    test_support.run_unittest(*tests)


if __name__ == '__main__':
    test_main()
