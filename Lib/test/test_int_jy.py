"""Int tests

Additional tests for Jython.
"""
import unittest
import types
from test import test_support

class IntTestCase(unittest.TestCase):

    def test_type_matches(self):
        self.assert_(isinstance(1, types.IntType))

    def test_int_pow(self):
        self.assertEquals(pow(10, 10, None), 10000000000L)
        self.assertEquals(int.__pow__(10, 10, None), 10000000000L)
        self.assertEquals((10).__pow__(10, None), 10000000000L)

def test_main():
    test_support.run_unittest(IntTestCase)

if __name__ == '__main__':
    test_main()
