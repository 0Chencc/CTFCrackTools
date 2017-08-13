"""Basic coerce tests cases

Made for Jython.
"""
import unittest
from test import test_support
from javatests import Coercion
from collections import Sequence

class MySeqClass1(Sequence):
    def __init__(self, l):
        self.l = l
    def __getitem__(self, i):
        return self.l[i]
    def __len__(self):
        return len(self.l)

class MySeqClass2(object):
    def __init__(self, l):
        self.l = l
    def __getitem__(self, i):
        return self.l[i]
    def __len__(self):
        return len(self.l)

class MySeqClass3(MySeqClass2):
    pass

class CoerceTestCase(unittest.TestCase):

    def test_int_coerce__(self):
        self.assertEqual(int.__coerce__(1, None), NotImplemented)
        self.assertRaises(TypeError, int.__coerce__, None, 1)

    def test_long_coerce__(self):
        self.assertEqual(long.__coerce__(1L, None), NotImplemented)
        self.assertRaises(TypeError, long.__coerce__, None, 1)

    def test_float_coerce__(self):
        self.assertRaises(TypeError, float.__coerce__, None, 1)
        self.assertEqual(float.__coerce__(10.23, None), NotImplemented)

    def test_sequence_coerce__(self):
        l0 = ['a', 'b']
        l1 = MySeqClass1(['c', 'd'])
        l2 = MySeqClass2(['e', 'f'])
        l3 = MySeqClass3(['g', 'h'])
        Coercion.string_array(l0)
        Coercion.string_array(l1)
        Coercion.string_array(l2)
        Coercion.string_array(l3)

def test_main():
    test_support.run_unittest(CoerceTestCase)

if __name__ == "__main__":
    test_main()
