"""Misc math module tests

Made for Jython.
"""
import math
import unittest
from test import test_support
from test.test_math import (MathTests, ulps_check,
                            parse_testfile, test_file)

from java.lang import Math

inf = float('inf')
ninf = float('-inf')
nan = float('nan')

# Optional tests use mpmath
try:
    import mpmath
    HAVE_MPMATH = True
except:
    HAVE_MPMATH = False


class MathTestCase(unittest.TestCase):

    def test_frexp(self):
        self.assertEqual(math.frexp(inf), (inf, 0))
        mantissa, exponent = math.frexp(nan)
        self.assertNotEqual(mantissa, mantissa)
        self.assertEqual(exponent, 0)

    def test_fmod(self):
        self.assertEqual(-1e-100, math.fmod(-1e-100, 1e100))

    def test_hypot(self):
        self.assert_(math.isnan(math.hypot(nan, nan)))
        self.assert_(math.isnan(math.hypot(4, nan)))
        self.assert_(math.isnan(math.hypot(nan, 4)))
        self.assertEqual(inf, math.hypot(inf, 4))
        self.assertEqual(inf, math.hypot(4, inf))
        self.assertEqual(inf, math.hypot(ninf, 4))
        self.assertEqual(inf, math.hypot(4, ninf))

    def test_math_domain_error(self):
        self.assertRaises(ValueError, math.sqrt, -1)
        self.assertRaises(ValueError, math.sqrt, -1.5)
        self.assertRaises(ValueError, math.sqrt, -0.5)
        self.assertRaises(ValueError, math.log, 0)
        self.assertRaises(ValueError, math.log, -1)
        self.assertRaises(ValueError, math.log, -1.5)
        self.assertRaises(ValueError, math.log, -0.5)


class MathAccuracy(MathTests):
    # Run the CPython tests but expect accurate results

    def ftest(self, name, value, expected, ulps_err=1):

        if expected != 0. :
            # Tolerate small deviation in proportion to expected
            ulp_unit = Math.ulp(expected)
        else :
            # On zero, allow 2**-52. Maybe allow different slack based on name
            ulp_unit = Math.ulp(1.)

        # Complex expressions accumulate errors
        if name in ('cosh(2)-2*cosh(1)**2', 'sinh(1)**2-cosh(1)**2') :
            # ... quite steeply in these cases
            ulps_err *= 5

        err = value-expected

        if abs(err) > ulps_err * ulp_unit:
            # Use %r to display full precision.
            message = '%s returned %r, expected %r (%r ulps)' % \
                (name, value, expected, round(err/ulp_unit, 1))
            self.fail(message)

    def testConstants(self):
        # Override MathTests.testConstants requiring equality with java.Math
        self.assertEqual(math.pi, Math.PI)
        self.assertEqual(math.e, Math.E)

    def test_testfile(self, math_module=math, ulps_err=None):
        # Rigorous variant of MathTests.test_testfile requiring accuracy in ulps.
        fail_fmt = "{}:{}({!r}): expected {!r}, got {!r}"
        failures = []

        for id, fn, ar, ai, er, ei, flags in parse_testfile(test_file):
            # Skip if either the input or result is complex, or if
            # flags is nonempty
            if ai != 0. or ei != 0. or flags:
                continue
            if fn in ['rect', 'polar']:
                # no real versions of rect, polar
                continue

            if ulps_err is not None :
                fn_ulps_err = ulps_err
            else :
                # java.Math mostly promises 1 ulp, except for:
                if fn in ['atan2'] :
                    fn_ulps_err = 2
                elif fn in ['cosh', 'sinh', 'tanh'] :
                    fn_ulps_err = 2.5
                else :
                    fn_ulps_err = 1

            func = getattr(math_module, fn)
            arg = ar
            expected = er

            if 'invalid' in flags or 'divide-by-zero' in flags:
                expected = 'ValueError'
            elif 'overflow' in flags:
                expected = 'OverflowError'

            try:
                got = float(func(arg))
            except ValueError:
                got = 'ValueError'
            except OverflowError:
                got = 'OverflowError'

            accuracy_failure = None
            if isinstance(got, float) and isinstance(expected, float):
                if math.isnan(expected) and math.isnan(got):
                    continue
                accuracy_failure = ulps_check(expected, got, fn_ulps_err)
                if accuracy_failure is None:
                    continue

            if isinstance(got, str) and isinstance(expected, str):
                if got == expected:
                    continue

            fail_msg = fail_fmt.format(id, fn, arg, expected, got)
            if accuracy_failure is not None:
                fail_msg += ' ({})'.format(accuracy_failure)
            failures.append(fail_msg)

        if failures:
            self.fail('Failures in test_testfile:\n  ' +
                      '\n  '.join(failures))

    @unittest.skipUnless(HAVE_MPMATH, "requires mpmath module")
    def test_testfile_mpmath(self):
        # Run the mpmath module on the same material: consistency check during development.
        with mpmath.workprec(100) :
            self.test_testfile(mpmath, 1, 1)


def test_main():
    test_support.run_unittest(
            MathTestCase,
            MathAccuracy,
        )


if __name__ == '__main__':
    test_main()
