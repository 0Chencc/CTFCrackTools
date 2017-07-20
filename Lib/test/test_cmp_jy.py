"Tests for cmp() compatibility with CPython"
import UserDict
import unittest
from test import test_support

class CmpGeneralTestCase(unittest.TestCase):

    def test_type_crash(self):
        # Used to throw ArrayStoreException:
        # http://bugs.jython.org/issue1382
        class Configuration(object, UserDict.DictMixin):
            pass
        self.assertNotEqual(Configuration(), None)


class UnicodeDerivedCmp(unittest.TestCase):
    "Test for http://bugs.jython.org/issue1889394"
    def testCompareWithString(self):
        class Test(unicode):
            pass
        test = Test('{1:1}')
        self.assertNotEqual(test, {1:1})
    def testCompareEmptyDerived(self):
        class A(unicode): pass
        class B(unicode): pass
        self.assertEqual(A(), B())


class LongDerivedCmp(unittest.TestCase):
    def testCompareWithString(self):
        class Test(long):
            pass
        self.assertNotEqual(Test(0), 'foo')
        self.assertTrue('foo' in [Test(12), 'foo'])


class IntStrCmp(unittest.TestCase):
    def testIntStrCompares(self):
        assert not (-1 > 'a')
        assert (-1 < 'a')
        assert not (4 > 'a')
        assert (4 < 'a')
        assert not (-2 > 'a')
        assert (-2 < 'a')
        assert not (-1 == 'a')


class ObjectCmp(unittest.TestCase):
    def testObjectListCompares(self):
        # Also applies to tuple objects given common PySequence implementation
        assert not object() == list()
        assert object() != list()
        assert not list() == object()
        assert list() != object() 

        # Note that <, > rich comparisons in 2.x are broken by the
        # lexicographic ordering of the type **name**. Example:
        # 'object' > 'list'
        assert not object() < list()
        assert not object() <= list()
        assert object() > list()
        assert object() >= list()
        assert list() < object()
        assert list() <= object()
        assert not list() > object()
        assert not list() >= object()

    def testObjectDictCompares(self):
        # Also applies to such objects as defaultdict and Counter
        assert not object() == dict()
        assert object() != dict()
        assert not dict() == object()
        assert dict() != object() 

        # Note that <, > rich comparisons in 2.x are broken by the
        # lexicographic ordering of the type **name**. Example:
        # 'object' > 'dict'
        assert not object() < dict()
        assert not object() <= dict()
        assert object() > dict()
        assert object() >= dict()
        assert dict() < object()
        assert dict() <= object()
        assert not dict() > object()
        assert not dict() >= object()


class CustomCmp(unittest.TestCase):
    def test___cmp___returns(self):
        class Foo(object):
            def __int__(self):
                return 0
        class Bar(object):
            def __int__(self):
                raise ValueError('doh')
        class Baz(object):
            def __cmp__(self, other):
                return self.cmp(other)
        baz = Baz()
        baz.cmp = lambda other : Foo()
        self.assertEqual(cmp(100, baz), 0)
        baz.cmp = lambda other : NotImplemented
        # CPython is faulty here (returns 1)
        self.assertEqual(cmp(100, baz), -1 if test_support.is_jython else 1)
        baz.cmp = lambda other: Bar()
        self.assertRaises(ValueError, cmp, 100, baz)
        baz.cmp = lambda other: 1 / 0
        self.assertRaises(ZeroDivisionError, cmp, 100, baz)
        del Baz.__cmp__
        self.assertEqual(cmp(100, baz), -1)

    def test_cmp_stops_short(self):
        class Foo(object):
            __eq__ = lambda self, other: False
        class Bar(object):
            __eq__ = lambda self, other: True
        self.assertEqual(cmp(Foo(), Bar()), 1)


def test_main():
    test_support.run_unittest(
            CmpGeneralTestCase,
            UnicodeDerivedCmp,
            LongDerivedCmp,
            IntStrCmp,
            ObjectCmp,
            CustomCmp,
            )


if __name__ == '__main__':
    test_main()
