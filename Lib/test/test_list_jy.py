import unittest
import random
import threading
import time
from test import test_support
import test_list

if test_support.is_jython:
    from java.util import ArrayList
    from java.lang import String

class ListTestCase(unittest.TestCase):

    def test_recursive_list_slices(self):
        x = [1,2,3,4,5]
        x[1:] = x
        self.assertEquals(x, [1, 1, 2, 3, 4, 5],
                          "Recursive assignment to list slices failed")

    def test_subclass_richcmp(self):
        # http://bugs.jython.org/issue1115
        class Foo(list):
            def __init__(self, dotstring):
                list.__init__(self, map(int, dotstring.split(".")))
        bar1 = Foo('1.2.3')
        bar2 = Foo('1.2.4')
        self.assert_(bar1 < bar2)
        self.assert_(bar1 <= bar2)
        self.assert_(bar2 > bar1)
        self.assert_(bar2 >= bar1)

    def test_setget_override(self):
        if not test_support.is_jython:
            return

        # http://bugs.jython.org/issue600790
        class GoofyListMapThing(ArrayList):
            def __init__(self):
                self.silly = "Nothing"

            def __setitem__(self, key, element):
                self.silly = "spam"

            def __getitem__(self, key):
                self.silly = "eggs"

        glmt = GoofyListMapThing()
        glmt['my-key'] = String('el1')
        self.assertEquals(glmt.silly, "spam")
        glmt['my-key']
        self.assertEquals(glmt.silly, "eggs")

    def test_tuple_equality(self):
        self.assertEqual([(1,), [1]].count([1]), 1) # http://bugs.jython.org/issue1317
 
    def test_big_list(self):
        """Verify that fairly large collection literals of primitives can be constructed."""
        # use \n to separate to avoid parser problems
        lst = eval("[" + ",\n".join((str(x) for x in xrange(64000))) +"]")
        self.assertEqual(len(lst), 64000)
        self.assertEqual(sum(lst), 2047968000)

class ThreadSafetyTestCase(unittest.TestCase):

    def run_threads(self, f, num=10):
        threads = []
        for i in xrange(num):
            t = threading.Thread(target=f)
            t.start()
            threads.append(t)
        timeout = 10. # be especially generous
        for t in threads:
            t.join(timeout)
            timeout = 0.
        for t in threads:
            self.assertFalse(t.isAlive())

    def test_append_remove(self):
        # derived from Itamar Shtull-Trauring's test for issue 521701
        lst = []
        def tester():
            ct = threading.currentThread()
            for i in range(1000):
                lst.append(ct)
                time.sleep(0.0001)
                lst.remove(ct)
        self.run_threads(tester)
        self.assertEqual(lst, [])

    def test_sort(self):
        lst = []
        def tester():
            ct = threading.currentThread()
            for i in range(1000):
                lst.append(ct)
                lst.sort()
                lst.remove(ct)
                time.sleep(0.0001)
        self.run_threads(tester)
        self.assertEqual(lst, [])

    def test_count_reverse(self):
        lst = [0,1,2,3,4,5,6,7,8,9,10,0]
        def tester():
            ct = threading.currentThread()
            for i in range(1000):
                self.assertEqual(lst[0], 0)
                if random.random() > 0.5:
                    time.sleep(0.0001)
                lst.reverse()
                self.assertEqual(lst.count(0), 2)
                self.assert_(lst[1] in (1,10))
        self.run_threads(tester)

class ExtendedSliceTestCase(unittest.TestCase):
    '''Really thrash extended slice operations on list.'''
    type2test = list

    def test_extended_slice_delete(self):
        # Based on list_tests.CommonTest.test_extendedslicing .
        # In the cited test case, the stop value is nearly always the default
        # (None), meaning the end of the list, and often the start value is too.
        # This contributed to the release of http://bugs.jython.org/issue1873 .
        # This is a supplementary test focused on correct stopping.

        initial =                  [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13]
        expected1 = self.type2test([ 0, 1, 2, 3, 4, 5,            10,11,12,13])
        expected2 = self.type2test([ 0, 1, 2,    4,    6,    8,   10,   12,13])
        expected4 = self.type2test([ 0, 1,    3, 4, 5,    7, 8, 9,   11,12,13])

        # Positive step
        a = self.type2test(initial)
        del a[6:10:1]
        self.assertEqual(a, expected1)
        a = self.type2test(initial)
        del a[3:13:2]
        self.assertEqual(a, expected2)
        a = self.type2test(initial)
        del a[3:12:2]
        self.assertEqual(a, expected2)
        a = self.type2test(initial)
        del a[2:11:4]
        self.assertEqual(a, expected4)
        a = self.type2test(initial)
        del a[2::4]
        self.assertEqual(a, expected4)

        # Negative step (same results)
        a = self.type2test(initial)
        del a[9:5:-1]
        self.assertEqual(a, expected1)
        a = self.type2test(initial)
        del a[11:1:-2]
        self.assertEqual(a, expected2)
        a = self.type2test(initial)
        del a[11:2:-2]
        self.assertEqual(a, expected2)
        a = self.type2test(initial)
        del a[10:1:-4]
        self.assertEqual(a, expected4)
        a = self.type2test(initial)
        del a[10::-4]
        self.assertEqual(a, expected4)

    def test_extended_slice_assign(self):
        # Based on list_tests.CommonTest.test_extendedslicing .
        # In the cited test case, the stop value is nearly always the default.
        # This is a supplementary test focused on correct stopping.

        aa, bb, cc = 91, 92, 93
        src = self.type2test([aa,bb,cc])
        initial =                  [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13]
        expected1 = self.type2test([ 0, 1, 2, 3, 4, 5,aa,bb,cc, 9,10,11,12,13])
        expected2 = self.type2test([ 0, 1, 2,aa, 4,bb, 6,cc, 8, 9,10,11,12,13])
        expected4 = self.type2test([ 0, 1,aa, 3, 4, 5,bb, 7, 8, 9,cc,11,12,13])

        # Positive step
        a = self.type2test(initial)
        a[6:9:1] = src
        self.assertEqual(a, expected1)
        a = self.type2test(initial)
        a[3:9:2] = src
        self.assertEqual(a, expected2)
        a = self.type2test(initial)
        a[3:8:2] = src
        self.assertEqual(a, expected2)
        a = self.type2test(initial)
        a[2:11:4] = src
        self.assertEqual(a, expected4)
        a = self.type2test(initial)
        a[2::4] = src
        self.assertEqual(a, expected4)

        # Negative step (same results, as src is reversed)
        src.reverse()
        a = self.type2test(initial)
        a[8:5:-1] = src
        self.assertEqual(a, expected1)
        a = self.type2test(initial)
        a[7:2:-2] = src
        self.assertEqual(a, expected2)
        a = self.type2test(initial)
        a[7:1:-2] = src
        self.assertEqual(a, expected2)
        a = self.type2test(initial)
        a[10:1:-4] = src
        self.assertEqual(a, expected4)
        a = self.type2test(initial)
        a[10::-4] = src
        self.assertEqual(a, expected4)


class JavaListTestCase(test_list.ListTest):

    type2test = ArrayList

    def test_init(self):
        # Iterable arg is optional
        self.assertEqual(self.type2test([]), self.type2test())

        # Unlike with builtin types, we do not guarantee objects can
        # be overwritten; see corresponding tests

        # Mutables always return a new object
        a = self.type2test([1, 2, 3])
        b = self.type2test(a)
        self.assertNotEqual(id(a), id(b))
        self.assertEqual(a, b)


    def test_extend_java_ArrayList(self):
        jl = ArrayList([])
        jl.extend([1,2])
        self.assertEqual(jl, ArrayList([1,2]))
        jl.extend(ArrayList([3,4]))
        self.assertEqual(jl, [1,2,3,4])


def test_main():
    test_support.run_unittest(ListTestCase,
                              ThreadSafetyTestCase,
                              ExtendedSliceTestCase,
                              JavaListTestCase)

if __name__ == "__main__":
    test_main()
