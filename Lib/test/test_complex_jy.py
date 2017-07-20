"""Misc complex tests

Made for Jython.
"""
import unittest
from test import test_support

INF, NINF, NAN = map(float, ("inf", "-inf", "nan"))

class ComplexTest(unittest.TestCase):

    def test_dunder_coerce(self):
        self.assertEqual(complex.__coerce__(1+1j, None), NotImplemented)
        self.assertRaises(TypeError, complex.__coerce__, None, 1+2j)

    def test_pow(self):
        class Foo(object):
            def __rpow__(self, other):
                return other ** 2
        # regression in 2.5 alphas
        self.assertEqual((4+0j) ** Foo(), (16+0j))

    def test___nonzero__(self):
        self.assertTrue(0.25+0j)
        self.assertTrue(25j)

    def test_abs_big(self):
        # These are close to overflow but don't
        close = [   complex( 1.794e+308, 0.000e+00),
                    complex( 1.119e+308, 1.403e+308),
                    complex(-3.992e+307, 1.749e+308),
                    complex(-1.617e+308, 7.785e+307),
                    complex(-1.617e+308,-7.785e+307),
                    complex(-3.992e+307,-1.749e+308) ]
        # These are a little bigger and do overflow
        over =  [   complex( 1.130e+308, 1.417e+308),
                    complex(-4.032e+307, 1.767e+308),
                    complex(-1.633e+308, 7.863e+307),
                    complex(-1.633e+308,-7.863e+307),
                    complex(-4.032e+307,-1.767e+308) ]
        # If you start with infinity, the return is infinity, no overflow
        infinities = [ complex(INF, 1), complex(NINF, 2), complex(3, INF), complex(4, NINF) ]

        for z in close :
            self.assertAlmostEquals(abs(z), 1.794e+308, delta=0.01e+308)
        for z in over :
            self.assertRaises(OverflowError, abs, z)
        for z in infinities :
            self.assertEqual(abs(z), INF)

def test_main():
    test_support.run_unittest(ComplexTest)

if __name__ == "__main__":
    test_main()
