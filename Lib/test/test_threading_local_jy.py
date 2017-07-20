"""Test for thread locals"""
import random
import sys
import threading
import time
import unittest
from test import test_support
from threading import local

class LocalStuff(local):
    def __init__(self, stuff, foo=1):
        local.__init__(self)
        self.stuff = stuff
        self.foo = foo

class TestThread(threading.Thread):
    def __init__(self, stuff, name):
        threading.Thread.__init__(self)
        self.stuff = stuff
        self.name = name
        self.errors = []

    def run(self):
        for i in xrange(10):
            try:
                self.stuff.stuff = self.name
                myStuff = self.stuff.stuff
                time.sleep(random.random() * 2)
                if myStuff != self.stuff.stuff:
                    self.errors.append("myStuff should equal self.stuff.stuff")
                if self.stuff.foo != 1:
                    self.errors.append("foo should be 1")
            except TypeError, te:
                self.errors.append("TypeError: %s" % te)
            except:
                self.errors.append("unexpected error: %s" % sys.exc_info()[0] )

    def getErrors(self):
        return self.errors

class ThreadLocalConstructorTestCase(unittest.TestCase):

    def test_construct_locals(self):
        """Ensures that constructing a local can have arguments"""
        stuff = LocalStuff("main stuff")
        threads = []
        for i in xrange(20):
            threads.append(TestThread(stuff, name=("thread-%d" % i)))
            threads[i].start()
        for i in xrange(20):
            threads[i].join()
            errors = threads[i].getErrors()
            self.assertEquals(0, len(errors), errors)


def test_main():
    test_support.run_unittest(ThreadLocalConstructorTestCase)


if __name__ == "__main__":
    test_main()
