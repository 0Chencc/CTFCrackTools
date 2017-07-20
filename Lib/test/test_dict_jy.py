from test import test_support
from java.util import HashMap, Hashtable
import unittest
from collections import defaultdict
import test_dict

class DictInitTest(unittest.TestCase):
    def testInternalSetitemInInit(self):
        """Test for http://jython.org/bugs/1816134

        CPython's dict uses an internal setitem method to initialize itself
        rather than the one on its subclasses, and this tests that Jython does
        as well.
        """
        class Subdict(dict):
            def __init__(self):
                super(Subdict, self).__init__([('a',1)])
                self.createdInInit = 1

            def __setitem__(self, key, value):
                super(Subdict, self).__setitem__(key, value)
                assert hasattr(self, 'createdInInit')
                self.createdInInit = value

        s = Subdict()
        s[7] = 'called'
        self.assertEquals('called', s.createdInInit)

    def testUnhashableKeys(self):
        try:
            a = {[1]:2}
        except TypeError:
            pass
        else:
            self.fail("list as dict key should raise TypeError")

        try:
            a = {{1:2}:3}
        except TypeError:
            pass
        else:
            self.fail("dict as dict key should raise TypeError")

class DictCmpTest(unittest.TestCase):
    "Test for http://bugs.jython.org/issue1031"
    def testDictCmp(self):
        # 'Implicit' comparision of dicts against other types instances
        # shouldn't raise exception:
        self.assertNotEqual({}, '')
        # The same, but explicitly calling __cmp__ should raise TypeError:
        self.assertRaises(TypeError, {}.__cmp__, '')
    def testDictDerivedCmp(self):
        # With derived classes that doesn't override __cmp__, the behaviour
        # should be the same that with dicts:
        class derived_dict(dict): pass
        self.assertEqual(derived_dict(), {})
        self.assertNotEqual(derived_dict(), '')
        self.assertRaises(TypeError, derived_dict().__cmp__, '')
        # But, if they *override* __cmp__ and raise TypeError from there, we
        # have exception raised when checking for equality...
        class non_comparable_dict(dict):
            def __cmp__(self, other):
                raise TypeError, "I always raise TypeError"
        self.assertRaises(TypeError, lambda: non_comparable_dict() == '')
        self.assertRaises(TypeError, non_comparable_dict().__cmp__, '')
        # ...unless you compare it with other dicts:
        # self.assertEqual(non_comparable_dict(), {})

        # The same happens even if the overridden __cmp__ doesn't nothing apart
        # from calling super:
        class dummy_dict_with_cmp(dict):
            def __cmp__(self, other):
                return super(dummy_dict_with_cmp, self).__cmp__(other)

        self.assertEqual(dummy_dict_with_cmp(), {})
        # But TypeError is raised when comparing against other types
        self.assertRaises(TypeError, lambda: dummy_dict_with_cmp() == '')
        self.assertRaises(TypeError, dummy_dict_with_cmp().__cmp__, '')
        # Finally, the Python implementation shouldn't be tricked by not
        # implementing __cmp__ on the actual type of the dict-derived instance,
        # but implementing it on a superclass.
        class derived_dict_with_custom_cmp(dict):
            def __cmp__(self, other):
                return 0
        class yet_another_dict(derived_dict_with_custom_cmp): pass
        self.assertEqual(derived_dict_with_custom_cmp(), '')
        self.assertEqual(yet_another_dict(), '')

class DictMiscTest(unittest.TestCase):
    def test_pop_key_error(self):
        # tests http://bugs.jython.org/issue2247
        with self.assertRaisesRegexp(KeyError, r"^1$"):
            {}.pop(1)
        with self.assertRaisesRegexp(KeyError, r"^\(\)$"):
            {}.pop(())
        with self.assertRaisesRegexp(KeyError, r"^frozenset\(\[\]\)$"):
            {}.pop(frozenset())

class DerivedDictTest(unittest.TestCase):
    "Tests for derived dict behaviour"
    def test_raising_custom_key_error(self):
        class CustomKeyError(KeyError):
            pass
        class DerivedDict(dict):
            def __getitem__(self, key):
                raise CustomKeyError("custom message")
        self.assertRaises(CustomKeyError, lambda: DerivedDict()['foo'])
    
    def test_issue1676(self):
        #See http://bugs.jython.org/issue1676
        x=defaultdict()
        #This formerly caused an NPE.
        self.assertEqual(None, x.pop(None,None))

    def test_big_dict(self):
        """Verify that fairly large collection literals of primitives can be constructed."""
        # use \n to separate to avoid parser problems

        d = eval("{" + ",\n".join(("'key{}': {}".format(x, x) for x in xrange(16000))) +"}")
        self.assertEqual(len(d), 16000)
        self.assertEqual(sum(d.itervalues()), 127992000)


class JavaIntegrationTest(unittest.TestCase):
    "Tests for instantiating dicts from Java maps and hashtables"
    def test_hashmap(self):
        x = HashMap()
        x.put('a', 1)
        x.put('b', 2)
        x.put('c', 3)
        x.put((1,2), "xyz")
        y = dict(x)
        self.assertEqual(set(y.items()), set([('a', 1), ('b', 2), ('c', 3), ((1,2), "xyz")]))

    def test_hashmap_builtin_pymethods(self):
        x = HashMap()
        x['a'] = 1
        x[(1, 2)] = 'xyz'
        self.assertEqual({tup for tup in x.iteritems()}, {('a', 1), ((1, 2), 'xyz')})
        self.assertEqual(str(x), repr(x))
        self.assertEqual(type(str(x)), type(repr(x)))

    def test_hashtable_equal(self):
        for d in ({}, {1:2}):
            x = Hashtable(d)
            self.assertEqual(x, d)
            self.assertEqual(d, x)
            self.assertEqual(x, HashMap(d))

    def test_hashtable_remove(self):
        x = Hashtable({})
        with self.assertRaises(KeyError):
            del x[0]

    def test_hashtable(self):
        x = Hashtable()
        x.put('a', 1)
        x.put('b', 2)
        x.put('c', 3)
        x.put((1,2), "xyz")
        y = dict(x)
        self.assertEqual(set(y.items()), set([('a', 1), ('b', 2), ('c', 3), ((1,2), "xyz")]))


class JavaDictTest(test_dict.DictTest):

    _class = HashMap

    def test_copy_java_hashtable(self):
        x = Hashtable()
        xc = x.copy()
        self.assertEqual(type(x), type(xc))

    def test_fromkeys(self):
        super(JavaDictTest, self).test_fromkeys()
        self.assertEqual(self._class.fromkeys('abc'), {'a':None, 'b':None, 'c':None})

    def test_repr_value_None(self):
        x = self._class({1:None})
        self.assertEqual(repr(x), '{1: None}')

    def test_set_return_None(self):
        x = self._class({1:2})
        self.assertEqual(x.__setitem__(1, 3), None)
        self.assertEqual(x.__getitem__(1), 3)

    def test_del_return_None(self):
        x = self._class({1:2})
        self.assertEqual(x.__delitem__(1), None)
        self.assertEqual(len(x), 0)

    def assert_property(self, prop, a, b):
        prop(self._make_dict(a), self._make_dict(b))
        prop(a, self._make_dict(b))
        prop(self._make_dict(a), b)

    def assert_not_property(self, prop, a, b):
        with self.assertRaises(AssertionError):
            prop(self._make_dict(a), self._make_dict(b))
        with self.assertRaises(AssertionError):
            prop(a, self._make_dict(b))
        with self.assertRaises(AssertionError):
            prop(self._make_dict(a), b)

    # NOTE: when comparing dictionaries below exclusively in Java
    # space, keys like 1 and 1L are different objects. Only when they
    # are brought into Python space by Py.java2py, as is needed when
    # comparing a Python dict with a Java Map, do we see them become
    # equal.

    def test_le(self):
        self.assert_property(self.assertLessEqual, {}, {})
        self.assert_property(self.assertLessEqual, {1: 2}, {1: 2})
        self.assert_not_property(self.assertLessEqual, {1: 2, 3: 4}, {1: 2})
        self.assert_property(self.assertLessEqual, {}, {1: 2})
        self.assertLessEqual(self._make_dict({1: 2}), {1L: 2L, 3L: 4L})
        self.assertLessEqual({1L: 2L}, self._make_dict({1: 2, 3L: 4L}))

    def test_lt(self):
        self.assert_not_property(self.assertLess, {}, {})
        self.assert_not_property(self.assertLess, {1: 2}, {1: 2})
        self.assert_not_property(self.assertLessEqual, {1: 2, 3: 4}, {1: 2})
        self.assert_property(self.assertLessEqual, {}, {1: 2})
        self.assertLess(self._make_dict({1: 2}), {1L: 2L, 3L: 4L})
        self.assertLess({1L: 2L}, self._make_dict({1: 2, 3L: 4L}))

    def test_ge(self):
        self.assert_property(self.assertGreaterEqual, {}, {})
        self.assert_property(self.assertGreaterEqual, {1: 2}, {1: 2})
        self.assert_not_property(self.assertLessEqual, {1: 2, 3: 4}, {1: 2})
        self.assert_property(self.assertLessEqual, {}, {1: 2})
        self.assertGreaterEqual(self._make_dict({1: 2, 3: 4}), {1L: 2L})
        self.assertGreaterEqual({1L: 2L, 3L: 4L}, self._make_dict({1: 2}))

    def test_gt(self):
        self.assert_not_property(self.assertGreater, {}, {})
        self.assert_not_property(self.assertGreater, {1: 2}, {1: 2})
        self.assert_not_property(self.assertLessEqual, {1: 2, 3: 4}, {1: 2})
        self.assert_property(self.assertLessEqual, {}, {1: 2})
        self.assertGreater(self._make_dict({1: 2, 3: 4}), {1L: 2L})
        self.assertGreater({1L: 2L, 3L: 4L}, self._make_dict({1: 2}))


class PyStringMapTest(test_dict.DictTest):
    # __dict__ for objects uses PyStringMap for historical reasons, so
    # we have to test separately

    def _class(self, d):
        # PyStringMap pretends to be a regular dict, so doing
        # type(C().__dict__)() will not be helpful - it creates a
        # regular dict. So explicitly create new objects and return
        # their __dict__
        class C(object):
            pass
        newdict = C().__dict__
        newdict.update(d)
        return newdict


def test_main():
    test_support.run_unittest(
        DictInitTest,
        DictCmpTest,
        DictMiscTest,
        DerivedDictTest,
        JavaIntegrationTest,
        JavaDictTest,
        PyStringMapTest)

if __name__ == '__main__':
    test_main()
