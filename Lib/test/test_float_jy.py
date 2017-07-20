"""Float tests

Made for Jython.
"""
import math
import sys
import unittest
from test import test_support

jython = test_support.is_jython

class FloatTestCase(unittest.TestCase):

    def test_float_repr(self):
        self.assertEqual(repr(12345678.000000005), '12345678.000000006')
        self.assertEqual(repr(12345678.0000000005), '12345678.0')
        self.assertRegexpMatches(repr(math.pi**-100), '1.927581416056020[0-9]e-50')
        self.assertEqual(repr(-1.0), '-1.0')
        self.assertEqual(repr(-9876.543210), '-9876.54321')
        self.assertEqual(repr(0.123456789e+35), '1.23456789e+34')

    def test_float_repr2(self):
        # Quite possibly these divergences result from JDK bug JDK-4511638:
        self.assertEqual(repr(9876.543210e+15),
                              jython and '9.876543209999999e+18' or '9.87654321e+18')
        self.assertEqual(repr(1235235235235240000.0),
                              jython and '1.2352352352352399e+18' or '1.23523523523524e+18')

    def test_float_str(self):
        self.assertEqual(str(12345678.000005), '12345678.0')
        self.assertEqual(str(12345678.00005), '12345678.0001')
        self.assertEqual(str(12345678.00005), '12345678.0001')
        self.assertEqual(str(12345678.0005), '12345678.0005')
        self.assertEqual(str(math.pi**-100), '1.92758141606e-50')
        self.assertEqual(str(0.0), '0.0')
        self.assertEqual(str(-1.0), '-1.0')
        self.assertEqual(str(-9876.543210), '-9876.54321')
        self.assertEqual(str(23456789012E666), 'inf')
        self.assertEqual(str(-23456789012E666), '-inf')

    def test_float_str_formatting(self):
        self.assertEqual('%.13g' % 12345678.00005, '12345678.00005')
        self.assertEqual('%.12g' % 12345678.00005, '12345678.0001')
        self.assertEqual('%.11g' % 12345678.00005, '12345678')
        self.assertEqual('%.12g' % math.pi**-100, '1.92758141606e-50')
        self.assertEqual('%.5g' % 123.005, '123')
        self.assertEqual('%#.5g' % 123.005, '123.00')
        self.assertEqual('%#g' % 0.001, '0.00100000')
        self.assertEqual('%#.5g' % 0.001, '0.0010000')
        self.assertEqual('%#.1g' % 0.0001, '0.0001')
        self.assertEqual('%#.4g' % 100, '100.0')
        self.assertEqual('%#.4g' % 100.25, '100.2')
        self.assertEqual('%g' % 0.00001, '1e-05')
        self.assertEqual('%#g' % 0.00001, '1.00000e-05')
        self.assertEqual('%e' % -400.0, '-4.000000e+02')
        self.assertEqual('%.2g' % 99, '99')
        self.assertEqual('%.2g' % 100, '1e+02')

    def test_overflow(self):
        shuge = '12345' * 120
        shuge_float = float(shuge)
        shuge_int = int(shuge)
        self.assertRaises(OverflowError, float, shuge_int)
        self.assertRaises(OverflowError, int, shuge_float)
        # and cmp should not overflow
        self.assertNotEqual(0.1, shuge_int)

    def test_nan(self):
        nan = float('nan')
        self.assert_(type(nan), float)
        if jython:
            # support Java syntax
            self.assert_(type(float('NaN')), float)

        self.assertNotEqual(nan, float('nan'))
        self.assertNotEqual(nan, nan)
        self.assertEqual(cmp(nan, float('nan')), 1)
        self.assertEqual(cmp(nan, nan), 0)
        for i in (-1, 1, -1.0, 1.0):
            self.assertEqual(cmp(nan, i), -1)
            self.assertEqual(cmp(i, nan), 1)

    def test_infinity(self):
        self.assert_(type(float('Infinity')), float)
        self.assert_(type(float('inf')), float)
        self.assertRaises(OverflowError, long, float('Infinity'))

    def test_minus_zero(self):
        # Some operations confused by -0.0
        mz = float('-0.0')
        self.assertEquals(mz, 0.)
        self.assertEquals(repr(mz)[0], '-')
        self.assertEquals(repr(abs(mz))[0], '0')

    def test_float_none(self):
        self.assertRaises(TypeError, float, None)

    def test_pow(self):
        class Foo(object):
            def __rpow__(self, other):
                return other ** 2

        self.assertEqual(4.0 ** Foo(), 16.0)  # regression in 2.5 alphas
        self.assertEqual((4.0).__pow__(2, None), 16.0)

    def test_faux(self):
        class F(object):
            def __float__(self):
                return 1.6
        self.assertEqual(math.cos(1.6), math.cos(F()))


def test_main():
    test_support.run_unittest(FloatTestCase)

if __name__ == '__main__':
    test_main()
