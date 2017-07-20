"""Misc weakref tests

Made for Jython.
"""
import unittest
import weakref
from test import test_support
from test_weakref import extra_collect

class ReferencesTestCase(unittest.TestCase):

    def test___eq__(self):
        class Foo(object):
            def __eq__(self, other):
                return True
            def __hash__(self):
                return hash('foo')
        foo1, foo2 = Foo(), Foo()
        ref1, ref2 = weakref.ref(foo1), weakref.ref(foo2)
        self.assertTrue(ref1() is foo1)
        self.assertTrue(ref2() is foo2)

    def test___hash__call(self):
        hash_called = []
        class Bar(object):
            def __hash__(self):
                hash = object.__hash__(self)
                hash_called.append(hash)
                return hash
        bar = Bar()
        ref = weakref.ref(bar)
        self.assertFalse(hash_called)

        hash(ref)
        self.assertEqual(len(hash_called), 1)
        hash(ref)
        self.assertEqual(len(hash_called), 1)
        self.assertEqual(hash(bar), hash(ref))
        self.assertEqual(len(hash_called), 2)


class ArgsTestCase(unittest.TestCase):

    # XXX consider adding other tests for dict, list, etc

    def test_python_fn_kwargs(self):

        weakrefs = []
        sentinel = []

        def watch(obj, kwarg=True):
            self.assertEqual(kwarg, True)
            # log the death of the reference by appending to the sentinel
            ref = weakref.ref(obj, sentinel.append)
            weakrefs.append(ref)

        self.assert_(not sentinel)

        thunk1 = lambda: None
        watch(thunk1)
        self.assert_(not sentinel)

        del thunk1
        extra_collect()
        self.assert_(sentinel)

        del sentinel[:]

        thunk2 = lambda: None
        watch(thunk2, kwarg=True)  # <--- only difference: called with a kwarg
        self.assert_(not sentinel)

        del thunk2
        extra_collect()
        self.assert_(sentinel)



def test_main():
    test_support.run_unittest(ReferencesTestCase, ArgsTestCase)


if __name__ == '__main__':
    test_main()
