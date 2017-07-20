"""Misc decorator related tests

Made for Jython.
"""
from test import test_support
import unittest


def funcattrs(**kwds):
    def decorate(func):
        func.__dict__.update(kwds)
        return func
    return decorate

def classattrs(**kwds):
    def decorate(cls):
        for k, v in kwds.iteritems():
            setattr(cls, k, v)
        return cls
    return decorate


class TestDecorators(unittest.TestCase):

    def test_lookup_order(self):
        class Foo(object):
            foo = 'bar'
            @property
            def property(self):
                return self.foo
        self.assertEqual(Foo().property, 'bar')

    def test_lambda_in_class_decorator(self):
        # Tests fix for http://bugs.jython.org/issue2232
        @classattrs(abc=42, xyz=lambda self: 47)
        class C(object):
            pass

        c = C()
        self.assertEqual(c.abc, 42)
        self.assertEqual(c.xyz(), 47)

    def test_lambda_in_function_decorator(self):
        class C(object):
            @funcattrs(abc=1, xyz=lambda: 47)
            def foo(self): return 42

        self.assertEqual(C().foo(), 42)
        self.assertEqual(C().foo.abc, 1)
        self.assertEqual(C().foo.xyz(), 47)


def test_main():
    test_support.run_unittest(TestDecorators)


if __name__ == '__main__':
    test_main()
