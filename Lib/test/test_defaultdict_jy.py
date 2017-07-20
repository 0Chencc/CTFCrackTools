"""Misc defaultdict tests.

Made for Jython.
"""
import pickle
import time
import threading
import unittest
from collections import defaultdict
from test import test_support
from random import randint

from java.util.concurrent.atomic import AtomicInteger

class PickleTestCase(unittest.TestCase):

    def test_pickle(self):
        d = defaultdict(str, a='foo', b='bar')
        for proto in range(pickle.HIGHEST_PROTOCOL + 1):
            self.assertEqual(pickle.loads(pickle.dumps(d, proto)), d)


# TODO push into test_support or some other common module - run_threads
# is originally from test_list_jy.py

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

    class Counter(object):
        def __init__(self, initial=0):
            self.atomic = AtomicInteger(initial)
             # waiting is important here to ensure that
             # defaultdict factories can step on each other
            time.sleep(0.001)

        def decrementAndGet(self):
            return self.atomic.decrementAndGet()

        def incrementAndGet(self):
            return self.atomic.incrementAndGet()

        def get(self):
            return self.atomic.get()

        def __repr__(self):
            return "Counter<%s>" % (self.atomic.get())

    def test_inc_dec(self):
        counters = defaultdict(ThreadSafetyTestCase.Counter)
        size = 17

        def tester():
            for i in xrange(1000):
                j = (i + randint(0, size)) % size
                counters[j].decrementAndGet()
                time.sleep(0.0001)
                counters[j].incrementAndGet()

        self.run_threads(tester, 20)

        for i in xrange(size):
            self.assertEqual(counters[i].get(), 0, counters)

    def test_derived_inc_dec(self):
        class DerivedDefaultDict(defaultdict):
            def __missing__(self, key):
                if self.default_factory is None:
                    raise KeyError("Invalid key '{0}' and no default factory was set")

                val = self.default_factory(key)

                self[key] = val
                return val

        counters = DerivedDefaultDict(lambda key: ThreadSafetyTestCase.Counter(key))
        size = 17

        def tester():
            for i in xrange(1000):
                j = (i + randint(0, size)) % size
                counters[j].decrementAndGet()
                time.sleep(0.0001)
                counters[j].incrementAndGet()

        self.run_threads(tester, 20)

        for i in xrange(size):
            self.assertEqual(counters[i].get(), i, counters)

class GetVariantsTestCase(unittest.TestCase):

    #http://bugs.jython.org/issue2133

    def test_get_does_not_vivify(self):
        d = defaultdict(list)
        self.assertEquals(d.get("foo"), None)
        self.assertEquals(d.items(), [])

    def test_get_default_does_not_vivify(self):
        d = defaultdict(list)
        self.assertEquals(d.get("foo", 42), 42)
        self.assertEquals(d.items(), [])

    def test_getitem_does_vivify(self):
        d = defaultdict(list)
        self.assertEquals(d["vivify"], [])
        self.assertEquals(d.items(), [("vivify", [])]) 



class OverrideMissingTestCase(unittest.TestCase):
    class KeyDefaultDict(defaultdict):
        """defaultdict to pass the requested key to factory function."""
        def __missing__(self, key):
            if self.default_factory is None:
                raise KeyError("Invalid key '{0}' and no default factory was set")
            else:
                val = self.default_factory(key)

            self[key] = val
            return val

        @classmethod
        def double(cls, k):
            return k + k

    def setUp(self):
        self.kdd = OverrideMissingTestCase.KeyDefaultDict(OverrideMissingTestCase.KeyDefaultDict.double)

    def test_dont_call_derived_missing(self):
        self.kdd[3] = 5
        self.assertEquals(self.kdd[3], 5)

    #http://bugs.jython.org/issue2088
    def test_override_missing(self):
        # line below causes KeyError in Jython, ignoring overridden __missing__ method
        self.assertEquals(self.kdd[3], 6)
        self.assertEquals(self.kdd['ab'], 'abab')


def test_main():
    test_support.run_unittest(PickleTestCase, ThreadSafetyTestCase, GetVariantsTestCase, OverrideMissingTestCase)


if __name__ == '__main__':
    test_main()
