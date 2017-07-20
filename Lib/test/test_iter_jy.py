"""Misc iterator tests.

Made for Jython.
"""
import itertools
import operator
from test import test_support
import unittest

class IterTestCase(unittest.TestCase):

    def test_fastiter(self):
        class MyList(list):
            def __getitem__(self, index):
                return str(index) + '!'
        class MyTuple(tuple):
            def __getitem__(self, index):
                return str(index) + '!'
        self.assertEqual(iter(MyList(['a', 'b'])).next(), 'a')
        self.assertEqual(iter(MyTuple(['a', 'b'])).next(), 'a')

    def test_slowiter(self):
        class MyStr(str):
            def __getitem__(self, index):
                return str(index) + '!'
        self.assertEqual(iter(MyStr('ab')).next(), '0!')

    def test_chain(self):
        self.assertEqual(list(itertools.chain([], [], ['foo'])), ['foo'])


class ChainedIterationTest(unittest.TestCase):

    # Test http://bugs.jython.org/issue1991

    def test_chain(self):
        
        class TestChain(object):
            def __init__(self, data):
                self.data = data
            def __iter__(self):
                return itertools.chain(self.data)
        
        data = [1, 2, 3]
        obj = TestChain(data)
        self.assertEqual(list(obj), data)
        self.assertEqual(list(obj), list(obj.__iter__()))

    def test_compress(self):
        
        class TestCount(object):
            def __init__(self, data, selectors):
                self.data = data
                self.selectors = selectors
            def __iter__(self):
                return itertools.compress(self.data, self.selectors)
        
        obj = TestCount((1, 2, 3, 4, 5), (1, 0, 1, 0, 1))
        self.assertEqual(list(obj), [1, 3, 5])
        self.assertEqual(list(obj), list(obj.__iter__()))

    def test_count(self):
        
        class TestCount(object):
            def __init__(self, data):
                self.data = data
            def __iter__(self):
                return itertools.count(self.data)
        
        obj = TestCount(1)
        self.assertEqual(list(itertools.islice(obj, 5)), [1, 2, 3, 4, 5])
        self.assertEqual(list(itertools.islice(obj, 25)), list(itertools.islice(obj.__iter__(), 25)))

    def test_cycle(self):
        
        class TestCycle(object):
            def __init__(self, data):
                self.data = data
            def __iter__(self):
                return itertools.cycle(self.data)
        
        data = [1, 2, 3]
        obj = TestCycle(data)
        self.assertEqual(list(itertools.islice(obj, 6)), data * 2)
        self.assertEqual(list(itertools.islice(obj, 6)), list(itertools.islice(obj.__iter__(), 6)))

    def test_dropwhile(self):
        
        class TestCycle(object):
            def __init__(self, pred, data):
                self.pred = pred
                self.data = data
            def __iter__(self):
                return itertools.dropwhile(self.pred, self.data)
        
        obj = TestCycle(lambda x: x<5, [1, 4, 6, 4, 1])
        self.assertEqual(list(obj), [6, 4, 1])
        self.assertEqual(list(obj), list(obj.__iter__()))

    def test_groupby(self):

        def unique_justseen(iterable, key=None):
            "List unique elements, preserving order. Remember only the element just seen."
            # unique_justseen('AAAABBBCCDAABBB') --> A B C D A B
            # unique_justseen('ABBCcAD', str.lower) --> A B C A D
            return itertools.imap(
                next, 
                itertools.imap(operator.itemgetter(1),
                               itertools.groupby(iterable, key)))

        class TestGroupBy(object):
            def __init__(self, data, key):
                self.data = data
                self.key = key
            def __iter__(self):
                return unique_justseen(self.data, self.key)
        
        obj = TestGroupBy('ABBCcAD', str.lower)
        self.assertEqual(list(obj), list('ABCAD'))
        self.assertEqual(list(obj), list(obj.__iter__()))        

    def test_ifilter(self):

        class TestIFilter(object):
            def __init__(self, pred, data):
                self.pred = pred
                self.data = data
            def __iter__(self):
                return itertools.ifilter(self.pred, self.data)

        obj = TestIFilter(lambda x: x%2, range(10))
        self.assertEqual(list(obj), [1, 3, 5, 7, 9])
        self.assertEqual(list(obj), list(obj.__iter__()))

    def test_ifilterfalse(self):

        class TestIFilterFalse(object):
            def __init__(self, pred, data):
                self.pred = pred
                self.data = data
            def __iter__(self):
                return itertools.ifilterfalse(self.pred, self.data)

        obj = TestIFilterFalse(lambda x: x%2, range(10))
        self.assertEqual(list(obj), [0, 2, 4, 6, 8])
        self.assertEqual(list(obj), list(obj.__iter__()))

    def test_ifilterfalse(self):

        class TestIslice(object):
            def __init__(self, seq, start, stop):
                self.seq = seq
                self.start = start
                self.stop = stop
            def __iter__(self):
                return itertools.islice(self.seq, self.start, self.stop)

        obj = TestIslice('ABCDEFG', 2, None)
        self.assertEqual(list(obj), list('CDEFG'))
        self.assertEqual(list(obj), list(obj.__iter__()))

    def test_imap(self):

        class TestImap(object):
            def __init__(self, func, p, q):
                self.func = func
                self.p = p
                self.q = q
            def __iter__(self):
                return itertools.imap(self.func, self.p, self.q)

        obj = TestImap(pow, (2,3,10), (5,2,3))
        self.assertEqual(list(obj), [32, 9, 1000])
        self.assertEqual(list(obj), list(obj.__iter__()))

    def test_starmap(self):

        class TestStarmap(object):
            def __init__(self, func, seq):
                self.func = func
                self.seq = seq
            def __iter__(self):
                return itertools.starmap(self.func, self.seq)

        obj = TestStarmap(pow, [(2,5), (3,2), (10,3)])
        self.assertEqual(list(obj), [32, 9, 1000])
        self.assertEqual(list(obj), list(obj.__iter__()))

    def test_takewhile(self):

        class TestTakewhile(object):
            def __init__(self, pred, seq):
                self.pred = pred
                self.seq = seq
            def __iter__(self):
                return itertools.takewhile(self.pred, self.seq)

        obj = TestTakewhile(lambda x: x<5, [1, 4, 6, 4, 1])
        self.assertEqual(list(obj), [1, 4])
        self.assertEqual(list(obj), list(obj.__iter__()))

    def test_tee(self):

        def pairwise(iterable):
            "s -> (s0,s1), (s1,s2), (s2, s3), ..."
            a, b = itertools.tee(iterable)
            next(b, None)
            return itertools.izip(a, b)

        class TestTee(object):
            def __init__(self, func, it):
                self.func = func
                self.it = it
            def __iter__(self):
                return self.func(self.it)

        obj = TestTee(pairwise, range(6))
        self.assertEqual(list(obj), [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)])
        self.assertEqual(list(obj), list(obj.__iter__()))

    def test_izip(self):

        class TestIzip(object):
            def __init__(self, p, q):
                self.p = p
                self.q = q
            def __iter__(self):
                return itertools.izip(self.p, self.q)

        obj = TestIzip('ABCD', 'xy')
        self.assertEqual(list(obj), [('A', 'x'), ('B', 'y')])
        self.assertEqual(list(obj), list(obj.__iter__()))

    def test_izip_longest(self):

        class TestIzipLongest(object):
            def __init__(self, p, q):
                self.p = p
                self.q = q
            def __iter__(self):
                return itertools.izip_longest(self.p, self.q, fillvalue='-')

        obj = TestIzipLongest('ABCD', 'xy')
        self.assertEqual(list(obj), [('A', 'x'), ('B', 'y'), ('C', '-'), ('D', '-')])
        self.assertEqual(list(obj), list(obj.__iter__()))

    def test_combinations(self):

        class TestCombinations(object):
            def __init__(self, data):
                self.data = data
            def __iter__(self):
                return itertools.combinations(self.data, 2)

        obj = TestCombinations('ABCD')
        self.assertEqual(list(obj), list(itertools.combinations('ABCD', 2)))
        self.assertEqual(list(obj), list(obj.__iter__()))

    def test_combinations_with_replacement(self):

        class TestCombinationsWithReplacement(object):
            def __init__(self, data):
                self.data = data
            def __iter__(self):
                return itertools.combinations_with_replacement(self.data, 2)

        obj = TestCombinationsWithReplacement('ABCD')
        self.assertEqual(list(obj), list(itertools.combinations_with_replacement('ABCD', 2)))
        self.assertEqual(list(obj), list(obj.__iter__()))

    def test_permutations(self):

        class TestPermutations(object):
            def __init__(self, data):
                self.data = data
            def __iter__(self):
                return itertools.permutations(self.data, 2)

        obj = TestPermutations('ABCD')
        self.assertEqual(list(obj), list(itertools.permutations('ABCD', 2)))
        self.assertEqual(list(obj), list(obj.__iter__()))

    def test_product(self):

        class TestProduct(object):
            def __init__(self, data):
                self.data = data
            def __iter__(self):
                return itertools.product(self.data, repeat=2)

        obj = TestProduct('ABCD')
        self.assertEqual(list(obj), list(itertools.product('ABCD', repeat=2)))
        self.assertEqual(list(obj), list(obj.__iter__()))


def test_main():
    test_support.run_unittest(IterTestCase, ChainedIterationTest)


if __name__ == '__main__':
    test_main()
