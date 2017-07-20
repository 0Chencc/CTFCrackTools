"""Misc. exception related tests

Made for Jython.
"""
import sys
import unittest
from javatests import StackOverflowErrorTest
from test import test_support


class C:
    def __str__(self):
        raise Exception("E")
    def __repr__(self):
        raise Exception("S")

class ExceptionsTestCase(unittest.TestCase):

    def test_keyerror_str(self):
        self.assertEquals(str(KeyError()), '')
        # Is actually repr(args[0])
        self.assertEquals(str(KeyError('')), "''")
        self.assertEquals(str(KeyError('', '')), "('', '')")

    #From bugtests/test076.py
    def test_raise_no_arg(self):
        r = None
        try:
            try:
                raise RuntimeError("dummy")
            except RuntimeError:
                raise
        except RuntimeError, e:
            r = str(e)

        self.assertEquals(r, "dummy")

    def testBugFix1149372(self):
        try:
            c = C()
            str(c)
        except Exception, e:
            assert e.args[0] == "E"
            return
        unittest.fail("if __str__ raises an exception, re-raise")

    def test_wrap_StackOverflowError(self):
        with self.assertRaises(RuntimeError) as cm:
            StackOverflowErrorTest.throwStackOverflowError()
        self.assertEqual(
            cm.exception.message,
            "maximum recursion depth exceeded (Java StackOverflowError)")

        with self.assertRaises(RuntimeError) as cm:
            StackOverflowErrorTest.causeStackOverflowError()
        self.assertEqual(
            cm.exception.message,
            "maximum recursion depth exceeded (Java StackOverflowError)")

    def test_unicode_args(self):
        e = RuntimeError(u"Drink \u2615")  # coffee emoji
        # Can take the repr of any object
        self.assertEqual(repr(e), "RuntimeError(u'Drink \u2615',)")
        # Cannot of course turn a non-ascii Unicode object into a str, even if it's an exception object
        with self.assertRaises(UnicodeEncodeError) as cm:
            str(e)
        self.assertEqual(
            str(cm.exception),
            "'ascii' codec can't encode character u'\u2615' in position 6: ordinal not in range(128)")
        # But the exception hook, via Py#displayException, does not fail when attempting to __str__ the exception args
        with test_support.captured_stderr() as s:
            sys.excepthook(RuntimeError, u"Drink \u2615", None)
        self.assertEqual(s.getvalue(), "RuntimeError\n")  
        # It is fine with ascii values, of course
        with test_support.captured_stderr() as s:
            sys.excepthook(RuntimeError, u"Drink java", None)
        self.assertEqual(s.getvalue(), "RuntimeError: Drink java\n")  


def test_main():
    test_support.run_unittest(ExceptionsTestCase)

if __name__ == '__main__':
    test_main()
