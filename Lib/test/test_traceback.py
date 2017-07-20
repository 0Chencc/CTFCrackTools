"""Test cases for traceback module"""

from __future__ import with_statement
import unittest
from test.test_support import run_unittest, is_jython

import traceback

class TracebackCases(unittest.TestCase):
    # For now, a very minimal set of tests.  I want to be sure that
    # formatting of SyntaxErrors works based on changes for 2.1.

    def get_exception_format(self, func, exc):
        try:
            func()
        except exc, value:
            return traceback.format_exception_only(exc, value)
        else:
            raise ValueError, "call did not raise exception"

    def syntax_error_with_caret(self):
        compile("def fact(x):\n\treturn x!\n", "?", "exec")

    def syntax_error_without_caret(self):
        # XXX why doesn't compile raise the same traceback?
        import test.badsyntax_nocaret

    def syntax_error_bad_indentation(self):
        compile("def spam():\n  print 1\n print 2", "?", "exec")

    @unittest.skipIf(is_jython, "FIXME: Jython lexer not catching bad '!'")
    def test_caret(self):
        err = self.get_exception_format(self.syntax_error_with_caret,
                                        SyntaxError)
        self.assert_(len(err) == 4)
        self.assert_(err[1].strip() == "return x!")
        self.assert_("^" in err[2]) # third line has caret
        self.assert_(err[1].find("!") == err[2].find("^")) # in the right place

    def test_nocaret(self):
        if is_jython:
            # jython adds a caret in this case (why shouldn't it?)
            return
        err = self.get_exception_format(self.syntax_error_without_caret,
                                        SyntaxError)
        self.assert_(len(err) == 3)
        self.assert_(err[1].strip() == "[x for x in x] = x")

    def test_bad_indentation(self):
        err = self.get_exception_format(self.syntax_error_bad_indentation,
                                        IndentationError)
        self.assert_(len(err) == 4)
        self.assert_(err[1].strip() == "print 2")
        self.assert_("^" in err[2])
        # Antlr thinks the error is at the indentation, while CPython points at
        # the end of the line.  I am agreeing with Antlr over CPython here.
        self.assert_(err[1].find("p") -1 == err[2].find("^"))

    def test_bug737473(self):
        import sys, os, tempfile, time

        savedpath = sys.path[:]
        testdir = tempfile.mkdtemp()
        try:
            sys.path.insert(0, testdir)
            testfile = os.path.join(testdir, 'test_bug737473.py')
            with open(testfile, 'w') as fp:
                print >> fp, """
def test():
    raise ValueError"""

            if 'test_bug737473' in sys.modules:
                del sys.modules['test_bug737473']
            import test_bug737473

            try:
                test_bug737473.test()
            except ValueError:
                # this loads source code to linecache
                traceback.extract_tb(sys.exc_traceback)

            # If this test runs too quickly, test_bug737473.py's mtime
            # attribute will remain unchanged even if the file is rewritten.
            # Consequently, the file would not reload.  So, added a sleep()
            # delay to assure that a new, distinct timestamp is written.
            # Since WinME with FAT32 has multisecond resolution, more than
            # three seconds are needed for this test to pass reliably :-(
            time.sleep(4)

            with open(testfile, 'w') as fp:
                print >> fp, """
def test():
    raise NotImplementedError"""
            reload(test_bug737473)
            try:
                test_bug737473.test()
            except NotImplementedError:
                src = traceback.extract_tb(sys.exc_traceback)[-1][-1]
                self.failUnlessEqual(src, 'raise NotImplementedError')
        finally:
            sys.path[:] = savedpath
            for f in os.listdir(testdir):
                os.unlink(os.path.join(testdir, f))
            os.rmdir(testdir)

    # sys.exc_traceback has been depecrated since 1.5, and is not supported on jython,
    # because these are global variables/not threadsafe

    def na_jython_test_members(self):
        # Covers Python/structmember.c::listmembers()
        try:
            1/0
        except:
            import sys
            sys.exc_traceback.__members__

    def test_base_exception(self):
        # Test that exceptions derived from BaseException are formatted right
        e = KeyboardInterrupt()
        lst = traceback.format_exception_only(e.__class__, e)
        self.assertEqual(lst, ['KeyboardInterrupt\n'])

    # String exceptions are deprecated, but legal.  The quirky form with
    # separate "type" and "value" tends to break things, because
    #     not isinstance(value, type)
    # and a string cannot be the first argument to issubclass.
    #
    # Note that sys.last_type and sys.last_value do not get set if an
    # exception is caught, so we sort of cheat and just emulate them.
    #
    # test_string_exception1 is equivalent to
    #
    # >>> raise "String Exception"
    #
    # test_string_exception2 is equivalent to
    #
    # >>> raise "String Exception", "String Value"
    #
    def test_string_exception1(self):
        str_type = "String Exception"
        err = traceback.format_exception_only(str_type, None)
        self.assertEqual(len(err), 1)
        self.assertEqual(err[0], str_type + '\n')

    def test_string_exception2(self):
        str_type = "String Exception"
        str_value = "String Value"
        err = traceback.format_exception_only(str_type, str_value)
        self.assertEqual(len(err), 1)
        self.assertEqual(err[0], str_type + ': ' + str_value + '\n')

    def test_format_exception_only_bad__str__(self):
        class X(Exception):
            def __str__(self):
                1/0
        err = traceback.format_exception_only(X, X())
        self.assertEqual(len(err), 1)
        str_value = '<unprintable %s object>' % X.__name__
        self.assertEqual(err[0], X.__name__ + ': ' + str_value + '\n')

    def test_without_exception(self):
        err = traceback.format_exception_only(None, None)
        self.assertEqual(err, ['None\n'])

def test_main():
    run_unittest(TracebackCases)


if __name__ == "__main__":
    test_main()
