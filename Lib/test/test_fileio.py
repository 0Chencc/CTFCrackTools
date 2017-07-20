# Adapted from test_file.py by Daniel Stutzbach

from __future__ import unicode_literals

import sys
import os
import errno
import unittest
from array import array
from weakref import proxy
from functools import wraps

from test.test_support import (TESTFN, check_warnings, run_unittest,
                               make_bad_fd, is_jython, gc_collect)
from test.test_support import py3k_bytes as bytes
from test.script_helper import run_python

from _io import FileIO as _FileIO

"""
XXX: ignoring ValueError on Jython for now as the ValueError/IOError thing is
     too mixed up right now. Needs investigation especially in Jython3 -- we
     should get this cleaned up if possible.
"""

class AutoFileTests(unittest.TestCase):
    # file tests for which a test file is automatically set up

    def setUp(self):
        self.f = _FileIO(TESTFN, 'w')

    def tearDown(self):
        if self.f:
            self.f.close()
        os.remove(TESTFN)

    def testWeakRefs(self):
        # verify weak references
        p = proxy(self.f)
        p.write(bytes(range(10)))
        self.assertEqual(self.f.tell(), p.tell())
        self.f.close()
        self.f = None
        gc_collect()
        self.assertRaises(ReferenceError, getattr, p, 'tell')

    def testSeekTell(self):
        self.f.write(bytes(range(20)))
        self.assertEqual(self.f.tell(), 20)
        self.f.seek(0)
        self.assertEqual(self.f.tell(), 0)
        self.f.seek(10)
        self.assertEqual(self.f.tell(), 10)
        self.f.seek(5, 1)
        self.assertEqual(self.f.tell(), 15)
        self.f.seek(-5, 1)
        self.assertEqual(self.f.tell(), 10)
        self.f.seek(-5, 2)
        self.assertEqual(self.f.tell(), 15)

    def testAttributes(self):
        # verify expected attributes exist
        f = self.f

        self.assertEqual(f.mode, "wb")
        self.assertEqual(f.closed, False)

        # verify the attributes are readonly
        for attr in 'mode', 'closed':
            self.assertRaises((AttributeError, TypeError),
                              setattr, f, attr, 'oops')

    def testReadinto(self):
        # verify readinto
        self.f.write(b"\x01\x02")
        self.f.close()
        a = array(b'b', b'x'*10)
        self.f = _FileIO(TESTFN, 'r')
        n = self.f.readinto(a)
        self.assertEqual(array(b'b', [1, 2]), a[:n])

    def test_none_args(self):
        self.f.write(b"hi\nbye\nabc")
        self.f.close()
        self.f = _FileIO(TESTFN, 'r')
        self.assertEqual(self.f.read(None), b"hi\nbye\nabc")
        self.f.seek(0)
        self.assertEqual(self.f.readline(None), b"hi\n")
        self.assertEqual(self.f.readlines(None), [b"bye\n", b"abc"])

    def testRepr(self):
        self.assertEqual(repr(self.f), "<_io.FileIO name=%r mode='%s'>"
                                       % (self.f.name, self.f.mode))
        del self.f.name
        self.assertEqual(repr(self.f), "<_io.FileIO fd=%r mode='%s'>"
                                       % (self.f.fileno(), self.f.mode))
        self.f.close()
        self.assertEqual(repr(self.f), "<_io.FileIO [closed]>")

    def testErrors(self):
        f = self.f
        self.assertTrue(not f.isatty())
        self.assertTrue(not f.closed)
        #self.assertEqual(f.name, TESTFN)
        self.assertRaises(ValueError, f.read, 10) # Open for writing
        f.close()
        self.assertTrue(f.closed)
        f = self.f = _FileIO(TESTFN, 'r')
        self.assertRaises(TypeError, f.readinto, "")
        self.assertTrue(not f.closed)
        f.close()
        self.assertTrue(f.closed)

        # These methods all accept a call with 0 arguments
        methods = ['fileno', 'isatty', 'read', 
                   'tell', 'truncate', 'seekable',
                   'readable', 'writable']
        if sys.platform.startswith('atheos'):
            methods.remove('truncate')

        self.f.close()
        self.assertTrue(self.f.closed)

        for methodname in methods:
            method = getattr(self.f, methodname)
            # should raise on closed file
            self.assertRaises(ValueError, method)

        # These other methods should be tested using a specific call
        # in case the test for number of arguments comes first.
        b = bytearray()
        self.assertRaises(ValueError, self.f.readinto, b )
        self.assertRaises(ValueError, self.f.seek, 0)
        self.assertRaises(ValueError, self.f.write, b )

    def testOpendir(self):
        # Issue 3703: opening a directory should fill the errno
        # Windows always returns "[Errno 13]: Permission denied
        # Unix calls dircheck() and returns "[Errno 21]: Is a directory"
        try:
            _FileIO('.', 'r')
        except IOError as e:
            self.assertNotEqual(e.errno, 0)
            self.assertEqual(e.filename, ".")
        else:
            self.fail("Should have raised IOError")

    #A set of functions testing that we get expected behaviour if someone has
    #manually closed the internal file descriptor.  First, a decorator:
    def ClosedFD(func):
        @wraps(func)
        def wrapper(self):
            #forcibly close the fd before invoking the problem function
            f = self.f
            os.close(f.fileno())
            try:
                func(self, f)
            except ValueError:
                if not is_jython:
                    self.fail("ValueError only on Jython")
            finally:
                try:
                    self.f.close()
                except IOError:
                    pass
                except ValueError:
                    if not is_jython:
                        self.fail("ValueError only on Jython")
        return wrapper

    def ClosedFDRaises(func):
        @wraps(func)
        def wrapper(self):
            #forcibly close the fd before invoking the problem function
            f = self.f
            os.close(f.fileno())
            try:
                func(self, f)
            except IOError as e:
                self.assertEqual(e.errno, errno.EBADF)
            except ValueError as e:
                if not is_jython:
                    self.fail("ValueError only on Jython")
            else:
                self.fail("Should have raised IOError")
            finally:
                try:
                    self.f.close()
                except IOError:
                    pass
                except ValueError:
                    if not is_jython:
                        self.fail("ValueError only on Jython")

        return wrapper

    @ClosedFDRaises
    def testErrnoOnClose(self, f):
        f.close()

    @ClosedFDRaises
    def testErrnoOnClosedWrite(self, f):
        f.write('a')

    @ClosedFDRaises
    def testErrnoOnClosedSeek(self, f):
        f.seek(0)

    @ClosedFDRaises
    def testErrnoOnClosedTell(self, f):
        f.tell()

    @ClosedFDRaises
    def testErrnoOnClosedTruncate(self, f):
        f.truncate(0)

    @ClosedFD
    def testErrnoOnClosedSeekable(self, f):
        f.seekable()

    @ClosedFD
    def testErrnoOnClosedReadable(self, f):
        f.readable()

    @ClosedFD
    def testErrnoOnClosedWritable(self, f):
        f.writable()

    @ClosedFD
    def testErrnoOnClosedFileno(self, f):
        f.fileno()

    @ClosedFD
    def testErrnoOnClosedIsatty(self, f):
        self.assertEqual(f.isatty(), False)

    def ReopenForRead(self):
        try:
            self.f.close()
        except IOError:
            pass
        self.f = _FileIO(TESTFN, 'r')
        os.close(self.f.fileno())
        return self.f

    @ClosedFDRaises
    def testErrnoOnClosedRead(self, f):
        f = self.ReopenForRead()
        f.read(1)

    @ClosedFDRaises
    def testErrnoOnClosedReadall(self, f):
        f = self.ReopenForRead()
        f.readall()

    @ClosedFDRaises
    def testErrnoOnClosedReadinto(self, f):
        f = self.ReopenForRead()
        a = array(b'b', b'x'*10)
        f.readinto(a)

class OtherFileTests(unittest.TestCase):
    # file tests for which a test file is not created but cleaned up
    # This introduced by Jython, to prevent the cascade of errors when
    # a test exits leaving an open file. Also a CPython problem.

    def setUp(self):
        self.f = None

    def tearDown(self):
        if self.f:
            self.f.close()
        if os.path.exists(TESTFN):
            os.remove(TESTFN)

    def testAbles(self):

        f = self.f = _FileIO(TESTFN, "w")
        self.assertEqual(f.readable(), False)
        self.assertEqual(f.writable(), True)
        self.assertEqual(f.seekable(), True)
        f.close()

        f = self.f = _FileIO(TESTFN, "r")
        self.assertEqual(f.readable(), True)
        self.assertEqual(f.writable(), False)
        self.assertEqual(f.seekable(), True)
        f.close()

        f = self.f = _FileIO(TESTFN, "a+")
        self.assertEqual(f.readable(), True)
        self.assertEqual(f.writable(), True)
        self.assertEqual(f.seekable(), True)
        self.assertEqual(f.isatty(), False)
        f.close()

        # Jython specific issues:
        # On OSX, FileIO("/dev/tty", "w").isatty() is False
        # On Ubuntu, FileIO("/dev/tty", "w").isatty() throws IOError: Illegal seek
        #
        # Much like we see on other platforms, we cannot reliably
        # determine it is not seekable (or special).
        #
        # Related bug: http://bugs.jython.org/issue1945
        if sys.platform != "win32" and not is_jython:
            try:
                f = self.f = _FileIO("/dev/tty", "a")
            except EnvironmentError:
                # When run in a cron job there just aren't any
                # ttys, so skip the test.  This also handles other
                # OS'es that don't support /dev/tty.
                pass
            else:
                self.assertEqual(f.readable(), False)
                self.assertEqual(f.writable(), True)
                if sys.platform != "darwin" and \
                   'bsd' not in sys.platform and \
                   not sys.platform.startswith('sunos'):
                    # Somehow /dev/tty appears seekable on some BSDs
                    self.assertEqual(f.seekable(), False)
                self.assertEqual(f.isatty(), True)

    def testModeStrings(self):
        # check invalid mode strings
        for mode in ("", "aU", "wU+", "rw", "rt"):
            try:
                f = self.f = _FileIO(TESTFN, mode)
            except ValueError:
                pass
            else:
                self.fail('%r is an invalid file mode' % mode)

    def testUnicodeOpen(self):
        # verify repr works for unicode too
        f = self.f = _FileIO(str(TESTFN), "w")

    def testBytesOpen(self):
        # Opening a bytes filename
        try:
            fn = TESTFN.encode("ascii")
        except UnicodeEncodeError:
            # Skip test
            return
        f = self.f = _FileIO(fn, "w")
        f.write(b"abc")
        f.close()
        with open(TESTFN, "rb") as f:
            self.f = f
            self.assertEqual(f.read(), b"abc")

    def testInvalidFd(self):
        if is_jython:
            self.assertRaises(TypeError, _FileIO, -10)  # file descriptor not int in Jython
        else:
            self.assertRaises(ValueError, _FileIO, -10)
        self.assertRaises(OSError, _FileIO, make_bad_fd())
        if sys.platform == 'win32':
            import msvcrt
            self.assertRaises(IOError, msvcrt.get_osfhandle, make_bad_fd())

    def testBadModeArgument(self):
        # verify that we get a sensible error message for bad mode argument
        bad_mode = "qwerty"
        try:
            f = self.f = _FileIO(TESTFN, bad_mode)
        except ValueError as msg:
            if msg.args[0] != 0:
                s = str(msg)
                if TESTFN in s or bad_mode not in s:
                    self.fail("bad error message for invalid mode: %s" % s)
            # if msg.args[0] == 0, we're probably on Windows where there may be
            # no obvious way to discover why open() failed.
        else:
            f.close()
            self.fail("no error for invalid mode: %s" % bad_mode)

    def testTruncate(self):
        f = self.f = _FileIO(TESTFN, 'w')
        f.write(bytes(bytearray(range(10))))
        self.assertEqual(f.tell(), 10)
        f.truncate(5)
        self.assertEqual(f.tell(), 10)
        self.assertEqual(f.seek(0, os.SEEK_END), 5)
        f.truncate(15)
        self.assertEqual(f.tell(), 5)
        #XXX: next assert not working in Jython:
        #self.assertEqual(f.seek(0, os.SEEK_END), 15)
        f.close()

    def testTruncateOnWindows(self):
        def bug801631():
            # SF bug <http://www.python.org/sf/801631>
            # "file.truncate fault on windows"
            f = self.f = _FileIO(TESTFN, 'w')
            f.write(bytes(range(11)))
            f.close()

            f = self.f = _FileIO(TESTFN,'r+')
            data = f.read(5)
            if data != bytes(range(5)):
                self.fail("Read on file opened for update failed %r" % data)
            if f.tell() != 5:
                self.fail("File pos after read wrong %d" % f.tell())

            f.truncate()
            if f.tell() != 5:
                self.fail("File pos after ftruncate wrong %d" % f.tell())

            f.close()
            size = os.path.getsize(TESTFN)
            if size != 5:
                self.fail("File size after ftruncate wrong %d" % size)

        # Test for bug 801631
        bug801631()

    def testAppend(self):

        f = self.f = open(TESTFN, 'wb')
        f.write(b'spam')
        f.close()
        f = self.f = open(TESTFN, 'ab')
        f.write(b'eggs')
        f.close()
        f = self.f = open(TESTFN, 'rb')
        d = f.read()
        f.close()
        self.assertEqual(d, b'spameggs')

    def testInvalidInit(self):
        self.assertRaises(TypeError, _FileIO, "1", 0, 0)

    def testWarnings(self):
        with check_warnings(quiet=True) as w:
            self.assertEqual(w.warnings, [])
            self.assertRaises(TypeError, _FileIO, [])
            self.assertEqual(w.warnings, [])
            self.assertRaises(ValueError, _FileIO, "/some/invalid/name", "rt")
            self.assertEqual(w.warnings, [])

def test_main():
    # Historically, these tests have been sloppy about removing TESTFN.
    # So get rid of it no matter what.
    try:
        run_unittest(AutoFileTests, OtherFileTests)
    finally:
        if os.path.exists(TESTFN):
            os.unlink(TESTFN)

if __name__ == '__main__':
    test_main()
