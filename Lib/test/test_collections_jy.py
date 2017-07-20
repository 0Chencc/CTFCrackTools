from test import test_support
from test.test_collections import ABCTestCase
from collections import (
    Hashable, Iterable, Iterator,
    Sized, Container, Callable,
    Set, MutableSet,
    Mapping, MutableMapping,
    Sequence, MutableSequence)
import sys

import java


class TestJavaInterfaces(ABCTestCase):

    def test_Iterable(self):
        # Check some non-iterables
        non_samples = [
            java.lang.Integer(42),
            java.lang.Long(sys.maxint+1)]
        for x in non_samples:
            self.assertNotIsInstance(x, Iterable)
            self.assertFalse(issubclass(type(x), Iterable), repr(type(x)))
        # Check some iterables
        samples = [
            java.util.HashMap(),
            java.util.ArrayList(),
            java.util.LinkedList(),
            java.util.HashMap().keys(),
            java.util.HashMap().items(),
            java.util.HashMap().values()]
        for x in samples:
            self.assertIsInstance(x, Iterable)
            self.assertTrue(issubclass(type(x), Iterable), repr(type(x)))

    def test_Container(self):
        # Check some objects that are not containers
        non_samples = [
            java.lang.String(),
            java.lang.Integer(42),
            java.lang.Long(sys.maxint+1)]
        for x in non_samples:
            self.assertNotIsInstance(x, Container)
            self.assertFalse(issubclass(type(x), Container), repr(type(x)))
        # Check some containers
        samples = [
            java.util.HashMap(),
            java.util.ArrayList(),
            java.util.LinkedList(),
            java.util.HashMap().keys(),
            java.util.HashMap().items(),
            java.util.HashMap().values()]
        for x in samples:
            self.assertIsInstance(x, Container)
            self.assertTrue(issubclass(type(x), Container), repr(type(x)))

    def test_MutableMapping(self):
        # Check some objects that do not support MutableMapping 
        non_samples = [
            java.util.ArrayList(),
            java.util.HashMap().keys(),
            java.util.HashSet(),
            java.util.LinkedList(),
            java.util.TreeSet(),
        ]
        for x in non_samples:
            self.assertNotIsInstance(x, MutableMapping)
            self.assertFalse(issubclass(type(x), MutableMapping), repr(type(x)))
        # Check some mappables
        samples = [
            java.util.HashMap(),
            java.util.concurrent.ConcurrentSkipListMap(),
        ]
        for x in samples:
            self.assertIsInstance(x, MutableMapping)
            self.assertTrue(issubclass(type(x), MutableMapping), repr(type(x)))

    def test_MutableSequence(self):
        # Check some objects that do not support MutableSequence
        non_samples = [
            java.util.HashMap(),
            java.util.HashSet(),
            java.util.TreeSet(),
            java.util.concurrent.ConcurrentSkipListMap(),
        ]
        for x in non_samples:
            self.assertNotIsInstance(x, MutableSequence)
            self.assertFalse(issubclass(type(x), MutableSequence), repr(type(x)))
        # Check some mappables
        samples = [
            java.util.ArrayList(),
            java.util.LinkedList(),
            java.util.HashMap().keys(),
        ]
        for x in samples:
            self.assertIsInstance(x, MutableSequence)
            self.assertTrue(issubclass(type(x), MutableSequence), repr(type(x)))

    def test_MutableSet(self):
        # Check some objects that are not sets
        non_samples = [
            java.util.ArrayList(),
            java.util.LinkedList(),
            java.util.HashMap(),
            java.util.concurrent.ConcurrentSkipListMap(),
        ]
        for x in non_samples:
            self.assertNotIsInstance(x, MutableSet)
            self.assertFalse(issubclass(type(x), MutableSet), repr(type(x)))
        # Check some sets
        samples = [
            java.util.HashSet(),
            java.util.TreeSet(),
        ]
        for x in samples:
            self.assertIsInstance(x, MutableSet)
            self.assertTrue(issubclass(type(x), MutableSet), repr(type(x)))


def test_main():
    test_classes = [TestJavaInterfaces]
    test_support.run_unittest(*test_classes)

if __name__ == "__main__":
    test_main()
