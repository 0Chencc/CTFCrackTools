import time
import random
import unittest
import threading
from test import test_support
from collections import deque


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
        d = deque(['sentinel'])
        def tester():
            ct = threading.currentThread()
            for i in range(1000):
                d.append(ct)
                time.sleep(0.0001)
                d.remove(ct)
        self.run_threads(tester)
        self.assertEqual(d, deque(['sentinel']))

    def test_append_pop(self):
        d = deque(['sentinel'])
        def tester():
            ct = threading.currentThread()
            for i in range(1000):
                d.append(ct)
                time.sleep(0.0001)
                d.pop()
        self.run_threads(tester)
        self.assertEqual(d, deque(['sentinel']))

    def test_appendleft_popleft(self):
        d = deque()
        def tester():
            ct = threading.currentThread()
            for i in range(1000):
                d.appendleft(ct)
                time.sleep(0.0001)
                d.popleft()
        self.run_threads(tester)
        self.assertEqual(d, deque())

    def test_count_reverse(self):
        d = deque([0,1,2,3,4,5,6,7,8,9,10,0])
        def tester():
            ct = threading.currentThread()
            for i in range(1000):
                self.assertEqual(d[0], 0)
                if random.random() > 0.5:
                    time.sleep(0.0001)
                d.reverse()
                self.assertEqual(d.count(0), 2)
                self.assert_(d[1] in (1,10))
        self.run_threads(tester)


def test_main():
    test_support.run_unittest(ThreadSafetyTestCase)

if __name__ == "__main__":
    test_main()

