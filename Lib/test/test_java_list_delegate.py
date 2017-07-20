from java.util import ArrayList, List, Vector

from copy import copy

import unittest
import test.test_support

class CollectionProxyTest(unittest.TestCase):
    def _perform_op(self, value, op_func):
        """
        Perform an operation

            value - the value to operate on
            op_func - the function that applies the operation to value

        Returns:
            the result of calling op_func, OR the exception that was raised in op_func
        """
        try:
            return op_func(value)
        except Exception, e:
            return type(e)

    def _arraylist_of(self, xs):
        """
        Converts a python list to a java.util.ArrayList
        """
        a = ArrayList()
        a.addAll( xs )
        return a

    def check_list(self, control, results, list_type_names, initial, test_name):
        for result, type_name in zip(results, list_type_names):
            try:
                len(result)
            except:
                print result
            self.assertEquals(len(control), len(result), "%s: length for %s does not match that of list" % (test_name, type_name))
            for control_value, result_value in zip(control, result):
                self.assertEquals(control_value, result_value, "%s: values from %s do not match those from list" % (test_name, type_name))

    def _list_op_test(self, initial_value, op_func, test_name):
        """
        Tests a list operation

        Ensures that performing an operation on:
            - a python list
            - a java.util.List instance

        gives the same result in both cases
        """
        lists = [list(initial_value), ArrayList(initial_value), Vector(initial_value)]
        list_type_names = ['list', 'ArrayList', 'Vector']

        results = [self._perform_op(l, op_func) for l in lists]
        self.check_list(lists[0], lists[1:], list_type_names[1:], initial_value, test_name)
        if not isinstance(results[0], list):
            for r,n in zip(results[1:], list_type_names[1:]):
                self.assertEquals(results[0], r, '%s: result for list does not match result for java type %s' % (test_name,n) )
        else:
            self.check_list(results[0], results[1:], list_type_names[1:], initial_value, test_name)

    def test_get_integer(self):
        initial_value = range(0, 5)

        for i in xrange(-7, 7):
            self._list_op_test(initial_value, lambda xs: xs[i], 'get_integer [%d]' % (i,))

    def test_get_slice(self):
        initial_value = range(0, 5)
        
        for i in [None] + range(-7, 7):
            for j in [None] + range(-7, 7):
                for k in [None] + range(-7, 7):
                    self._list_op_test(initial_value, lambda xs: xs[i:j:k], 'get_slice [%s:%s:%s]' % (i,j,k))

    def test_set_integer(self):
        initial_value = range(0, 5)

        def make_op_func(index):
            def _f(xs):
                xs[index] = 100
            return _f

        for i in xrange(-7, 7):
            self._list_op_test(initial_value, make_op_func(i), 'set_integer [%d]' % (i,))

    def test_set_slice(self):
        initial_value = range(0, 5)

        def make_op_func(i, j, k, v):
            def _f(xs):
                xs[i:j:k] = v
            return _f
        
        for i in [None] + range(-7, 7):
            for j in [None] + range(-7, 7):
                for k in [None] + range(-7, 7):
                    self._list_op_test(initial_value, make_op_func(i, j, k, []), 'set_slice [%s:%s:%s]=[]' % (i,j,k))
                    self._list_op_test(initial_value, make_op_func(i, j, k, range(0,2)), 'set_slice [%s:%s:%s]=range(0,2)' % (i,j,k))
                    self._list_op_test(initial_value, make_op_func(i, j, k, range(0,4)), 'set_slice [%s:%s:%s]=range(0,4)' % (i,j,k))
                    self._list_op_test(initial_value, make_op_func(i, j, k, xrange(0,2)), 'set_slice [%s:%s:%s]=xrange(0,2)' % (i,j,k))
                    self._list_op_test(initial_value, make_op_func(i, j, k, self._arraylist_of(range(0,2))), 'set_slice [%s:%s:%s]=ArrayList(range(0,2))' % (i,j,k))
 
        self._list_op_test([1,2,3,4,5], make_op_func(1, None, None, [1,2,3,4,5]), 'set_slice [1:]=[1,2,3,4,5]')

    def test_del_integer(self):
        initial_value = range(0,5)

        def make_op_func(index):
            def _f(xs):
                del xs[index]
            return _f

        for i in xrange(-7, 7):
            self._list_op_test(initial_value, make_op_func(i), 'del_integer [%d]' % (i,))

    def test_del_slice(self):
        initial_value = range(0,5)

        def make_op_func(i, j, k):
            def _f(xs):
                del xs[i:j:k]
            return _f

        for i in [None] + range(-7, 7):
            for j in [None] + range(-7, 7):
                for k in [None] + range(-7, 7):
                    self._list_op_test(initial_value, make_op_func(i, j, k), 'del_slice [%s:%s:%s]' % (i,j,k))

    def test_len(self):
        jlist = ArrayList()
        jlist.addAll(range(0, 10))

        self.assert_(len(jlist) == 10)

    def test_iter(self):
        jlist = ArrayList()
        jlist.addAll(range(0, 10))

        i = iter(jlist)

        x = list(i)

        self.assert_(x == range(0, 10))

    def test_override_len(self):
        class MyList (ArrayList):
            def __len__(self):
                return self.size() + 1;

        m = MyList()
        m.addAll(range(0,10))

        self.assert_(len(m) == 11)

    def test_override_iter(self):
        class MyList (ArrayList):
            def __iter__(self):
                return iter(self.subList(0, self.size() - 1));


        m = MyList()
        m.addAll(range(0,10))
        i = iter(m)
        x = list(i)

        self.assert_(x == range(0, 9))

    def test_override_getsetdelitem(self):
        # Create an ArrayList subclass that provides some silly overrides for get/set/del item
        class MyList (ArrayList):
            def __getitem__(self, key):
                return self.get(key) * 2;

            def __setitem__(self, key, value):
                return self.set(key, value * 2);

            def __delitem__(self, key):
                self.add(84)


        m = MyList()
        m.addAll(range(0,10))

        self.assert_(m[1] == 2)
        self.assert_(m.get(1) == 1)

        m[0] = 3
        self.assert_(m.get(0) == 6)
        self.assert_(m[0] == 12)

        del m[0]
        self.assert_(m.size() == 11)
        self.assert_(m.get(10) == 84)

        
        
    def test_set_slice_from_input_types(self):
        """
        Tests the slice setting functionality of Python lists
        Ensures that the results are all the same, whether the source list is a Python list, a java.util.List or an iterator
        """
        initial_value = range(0, 5)
        
        def make_op_func(i, j, k, v):
            def _f(xs):
                xs[i:j:k] = v
            return _f
        
        for i in [None] + range(-7, 7):
            for j in [None] + range(-7, 7):
                for k in [None] + range(-7, 7):
                    destPy = copy(initial_value)
                    destJUL = copy(initial_value)
                    destIter = copy(initial_value)
                    
                    sourcePy = range(0, 2)
                    sourceJUL = self._arraylist_of(range(0, 2))
                    sourceIter = xrange(0, 2)
                    
                    resultPy = self._perform_op(destPy, make_op_func(i, j, k, sourcePy))
                    resultJUL = self._perform_op(destJUL, make_op_func(i, j, k, sourceJUL))
                    resultIter = self._perform_op(destIter, make_op_func(i, j, k, sourceIter))
                    
                    self.assertEquals(resultPy, resultJUL)
                    self.assertEquals(resultPy, resultIter)

                    self.assertEquals(destPy, destJUL)
                    self.assertEquals(destPy, destIter)



def test_main():
    test.test_support.run_unittest(CollectionProxyTest)

if __name__ == "__main__":
    test_main()
