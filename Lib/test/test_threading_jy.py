"""Misc threading module tests

Made for Jython.
"""
from __future__ import with_statement

import random
import subprocess
import sys
import threading
import time
import unittest

from subprocess import PIPE, Popen
from test import test_support
from threading import Condition, Lock, Thread
from java.lang import Thread as JThread, InterruptedException


class ThreadingTestCase(unittest.TestCase):

    def test_str_name(self):
        t = Thread(name=1)
        self.assertEqual(t.getName(), '1')
        t.setName(2)
        self.assertEqual(t.getName(), '2')

    # make sure activeCount() gets decremented (see issue 1348)
    def test_activeCount(self):
        activeBefore = threading.activeCount()
        activeCount = 10
        for i in range(activeCount):
            t = Thread(target=self._sleep, args=(i,))
            t.setDaemon(0)
            t.start()
        polls = activeCount
        while activeCount > activeBefore and polls > 0:
            time.sleep(1)
            activeCount = threading.activeCount()
            polls -= 1
        self.assertTrue(activeCount <= activeBefore, 'activeCount should to be <= %s, instead of %s' % (activeBefore, activeCount))

    def _sleep(self, n):
        time.sleep(random.random())

    def test_issue1988(self):
        cond = threading.Condition(threading.Lock())
        locked = False
        try:
            locked = cond.acquire(False)
        finally:
            if locked:
                cond.release()


class TwistedTestCase(unittest.TestCase):
    
    def test_needs_underscored_versions(self):
        self.assertEqual(threading.Lock, threading._Lock)
        self.assertEqual(threading.RLock, threading._RLock)


class JavaIntegrationTestCase(unittest.TestCase):
    """Verifies that Thread.__tojava__ correctly gets the underlying Java thread"""

    def test_interruptible(self):

        def wait_until_interrupted(cv):
            name = threading.currentThread().getName()
            with cv:
                while not JThread.currentThread().isInterrupted():
                    try:
                        cv.wait()
                    except InterruptedException, e:
                        break

        num_threads = 5
        unfair_condition = Condition()
        threads = [
            Thread(
                name="thread #%d" % i,
                target=wait_until_interrupted,
                args=(unfair_condition,)) 
            for i in xrange(num_threads)]

        for thread in threads:
            thread.start()
        time.sleep(0.1)

        for thread in threads:
            JThread.interrupt(thread)

        joined_threads = 0
        for thread in threads:
            thread.join(1.) # timeout just in case so we don't stall regrtest
            joined_threads += 1
        self.assertEqual(joined_threads, num_threads)


class ReprTestCase(unittest.TestCase):

    def test_condition(self):
        l = Lock()
        c = Condition(l)
        self.assertEqual(repr(c), "<_threading.Condition(<_threading.Lock owner=None locked=False>), 0")
        l.acquire()
        self.assertEqual(repr(c), "<_threading.Condition(<_threading.Lock owner='MainThread' locked=True>), 0")
    
    def test_lock(self):
        l = Lock()
        self.assertEqual(repr(l), "<_threading.Lock owner=None locked=False>")
        r.acquire()
        self.assertEqual(repr(r), "<_threading.RLock owner='MainThread' locked=True>")
        r.release()
        self.assertEqual(repr(r), "<_threading.RLock owner=None locked=False>")

    def test_rlock(self):
        r = RLock()
        self.assertEqual(repr(r), "<_threading.RLock owner=None count=0>")
        r.acquire()
        self.assertEqual(repr(r), "<_threading.RLock owner='MainThread' count=1>")
        r.acquire()
        self.assertEqual(repr(r), "<_threading.RLock owner='MainThread' count=2>")
        r.release(); r.release()
        self.assertEqual(repr(r), "<_threading.RLock owner=None count=0>")


def test_main():
    test_support.run_unittest(
        JavaIntegrationTestCase,
        ThreadingTestCase,
        TwistedTestCase)


if __name__ == "__main__":
    test_main()
