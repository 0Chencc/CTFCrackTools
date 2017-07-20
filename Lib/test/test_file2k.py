import sys
import os
import errno
import unittest
import time
from array import array
from weakref import proxy
try:
    import threading
except ImportError:
    threading = None

from test import test_support
from test.test_support import TESTFN, run_unittest
from UserList import UserList

class AutoFileTests(unittest.TestCase):
    # file tests for which a test file is automatically set up

    def setUp(self):
        self.f = open(TESTFN, 'wb')

    def tearDown(self):
        if self.f:
            self.f.close()
        os.remove(TESTFN)

    def testWeakRefs(self):
        # verify weak references
        p = proxy(self.f)
        p.write('teststring')
        self.assertEqual(self.f.tell(), p.tell())
        self.f.close()
        self.f = None
        if test_support.is_jython: # GC is not immediate: borrow a trick
            from test_weakref import extra_collect
            extra_collect()
        self.assertRaises(ReferenceError, getattr, p, 'tell')

    def testAttributes(self):
        # verify expected attributes exist
        f = self.f
        with test_support.check_py3k_warnings():
            softspace = f.softspace
        f.name     # merely shouldn't blow up
        f.mode     # ditto
        f.closed   # ditto

        with test_support.check_py3k_warnings():
            # verify softspace is writable
            f.softspace = softspace    # merely shouldn't blow up

        # verify the others aren't
        for attr in 'name', 'mode', 'closed':
            self.assertRaises((AttributeError, TypeError), setattr, f, attr, 'oops')

    def testReadinto(self):
        # verify readinto
        self.f.write('12')
        self.f.close()
        a = array('c', 'x'*10)
        self.f = open(TESTFN, 'rb')
        n = self.f.readinto(a)
        self.assertEqual('12', a.tostring()[:n])

    def testWritelinesUserList(self):
        # verify writelines with instance sequence
        l = UserList(['1', '2'])
        self.f.writelines(l)
        self.f.close()
        self.f = open(TESTFN, 'rb')
        buf = self.f.read()
        self.assertEqual(buf, '12')

    def testWritelinesIntegers(self):
        # verify writelines with integers
        self.assertRaises(TypeError, self.f.writelines, [1, 2, 3])

    def testWritelinesIntegersUserList(self):
        # verify writelines with integers in UserList
        l = UserList([1,2,3])
        self.assertRaises(TypeError, self.f.writelines, l)

    def testWritelinesNonString(self):
        # verify writelines with non-string object
        class NonString:
            pass

        self.assertRaises(TypeError, self.f.writelines,
                          [NonString(), NonString()])

    def testRepr(self):
        # verify repr works
        self.assertTrue(repr(self.f).startswith("<open file '" + TESTFN))
        # see issue #14161
        if sys.platform == "win32" or (test_support.is_jython and os._name == "nt"):
            # Windows doesn't like \r\n\t" in the file name, but ' is ok
            fname = "xx'xx"
        else:
            fname = 'xx\rxx\nxx\'xx"xx'
        with open(fname, 'w') as f:
            self.addCleanup(os.remove, fname)
            self.assertTrue(repr(f).startswith(
                    "<open file %r, mode 'w' at" % fname))

    def testErrors(self):
        self.f.close()
        self.f = open(TESTFN, 'rb')
        f = self.f
        self.assertEqual(f.name, TESTFN)
        self.assertTrue(not f.isatty())
        self.assertTrue(not f.closed)

        self.assertRaises(TypeError, f.readinto, "")
        f.close()
        self.assertTrue(f.closed)

    def testMethods(self):
        methods = ['fileno', 'flush', 'isatty', 'next', 'read', 'readinto',
                   'readline', 'readlines', 'seek', 'tell', 'truncate',
                   'write', '__iter__']
        deprecated_methods = ['xreadlines']
        if sys.platform.startswith('atheos'):
            methods.remove('truncate')

        # __exit__ should close the file
        self.f.__exit__(None, None, None)
        self.assertTrue(self.f.closed)

        for methodname in methods:
            method = getattr(self.f, methodname)
            # should raise on closed file
            self.assertRaises((TypeError, ValueError), method)
        with test_support.check_py3k_warnings():
            for methodname in deprecated_methods:
                method = getattr(self.f, methodname)
                self.assertRaises(ValueError, method)
        self.assertRaises(ValueError, self.f.writelines, [])

        # file is closed, __exit__ shouldn't do anything
        self.assertEqual(self.f.__exit__(None, None, None), None)
        # it must also return None if an exception was given
        try:
            1 // 0
        except:
            self.assertEqual(self.f.__exit__(*sys.exc_info()), None)

    def testReadWhenWriting(self):
        self.assertRaises(IOError, self.f.read)

    def testNastyWritelinesGenerator(self):
        def nasty():
            for i in range(5):
                if i == 3:
                    self.f.close()
                yield str(i)
        self.assertRaises(ValueError, self.f.writelines, nasty())

    def testIssue5677(self):
        # We don't use the already-open file.
        self.f.close()

        # Remark: Do not perform more than one test per open file,
        # since that does NOT catch the readline error on Windows.
        data = 'xxx'
        for mode in ['w', 'wb', 'a', 'ab']:
            for attr in ['read', 'readline', 'readlines']:
                self.f = open(TESTFN, mode)
                self.f.write(data)
                self.assertRaises(IOError, getattr(self.f, attr))
                self.f.close()

            self.f = open(TESTFN, mode)
            self.f.write(data)
            self.assertRaises(IOError, lambda: [line for line in self.f])
            self.f.close()

            self.f = open(TESTFN, mode)
            self.f.write(data)
            self.assertRaises(IOError, self.f.readinto, bytearray(len(data)))
            self.f.close()

        for mode in ['r', 'rb', 'U', 'Ub', 'Ur', 'rU', 'rbU', 'rUb']:
            self.f = open(TESTFN, mode)
            self.assertRaises(IOError, self.f.write, data)
            self.f.close()

            self.f = open(TESTFN, mode)
            self.assertRaises(IOError, self.f.writelines, [data, data])
            self.f.close()

            self.f = open(TESTFN, mode)
            self.assertRaises(IOError, self.f.truncate)
            self.f.close()

class OtherFileTests(unittest.TestCase):

    def setUp(self):
        # (Jython addition) track open file so we can clean up
        self.f = None
        self.filename = TESTFN

    def tearDown(self):
        # (Jython addition) clean up to prevent errors cascading
        if self.f:
            self.f.close()
        try:
            os.remove(self.filename)
        except EnvironmentError as ee:
            if ee.errno != errno.ENOENT:
                raise ee

    def testOpenDir(self):
        this_dir = os.path.dirname(__file__) or os.curdir
        for mode in (None, "w"):
            try:
                if mode:
                    self.f = open(this_dir, mode)
                else:
                    self.f = open(this_dir)
            except IOError as e:
                self.assertEqual(e.filename, this_dir)
            else:
                self.fail("opening a directory didn't raise an IOError")

    def testModeStrings(self):
        # check invalid mode strings
        for mode in ("", "aU", "wU+"):
            try:
                self.f = f = open(TESTFN, mode)
            except ValueError:
                pass
            else:
                f.close()
                self.fail('%r is an invalid file mode' % mode)

        # Some invalid modes fail on Windows, but pass on Unix
        # Issue3965: avoid a crash on Windows when filename is unicode
        for name in (TESTFN, unicode(TESTFN), unicode(TESTFN + '\t')):
            try:
                self.f = f = open(name, "rr")
            except (IOError, ValueError):
                pass
            else:
                f.close()

    def testStdin(self):
        # This causes the interpreter to exit on OSF1 v5.1.
        if sys.platform != 'osf1V5':
            self.assertRaises(IOError, sys.stdin.seek, -1)
        else:
            print >>sys.__stdout__, (
                '  Skipping sys.stdin.seek(-1), it may crash the interpreter.'
                ' Test manually.')
        self.assertRaises(IOError, sys.stdin.truncate)

    def testUnicodeOpen(self):
        # verify repr works for unicode too
        self.f = f = open(unicode(TESTFN), "w")
        self.assertTrue(repr(f).startswith("<open file u'" + TESTFN))
        f.close()
        os.unlink(TESTFN)

    def testBadModeArgument(self):
        # verify that we get a sensible error message for bad mode argument
        bad_mode = "qwerty"
        try:
            self.f = f = open(TESTFN, bad_mode)
        except ValueError, msg:
            if msg.args[0] != 0:
                s = str(msg)
                if TESTFN in s or bad_mode not in s:
                    self.fail("bad error message for invalid mode: %s" % s)
            # if msg.args[0] == 0, we're probably on Windows where there may
            # be no obvious way to discover why open() failed.
        else:
            f.close()
            self.fail("no error for invalid mode: %s" % bad_mode)

    def testSetBufferSize(self):
        # make sure that explicitly setting the buffer size doesn't cause
        # misbehaviour especially with repeated close() calls
        for s in (-1, 0, 1, 512):
            try:
                self.f = f = open(TESTFN, 'w', s)
                f.write(str(s))
                f.close()
                f.close()
                self.f = f = open(TESTFN, 'r', s)
                d = int(f.read())
                f.close()
                f.close()
            except IOError, msg:
                self.fail('error setting buffer size %d: %s' % (s, str(msg)))
            self.assertEqual(d, s)

    def testTruncateOnWindows(self):

        def bug801631():
            # SF bug <http://www.python.org/sf/801631>
            # "file.truncate fault on windows"
            self.f = f = open(TESTFN, 'wb')
            f.write('12345678901')   # 11 bytes
            f.close()

            self.f = f = open(TESTFN,'rb+')
            data = f.read(5)
            if data != '12345':
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

        try:
            bug801631()
        finally:
            os.unlink(TESTFN)

    @unittest.skipIf(test_support.is_jython, "Specific to CPython")
    def testIteration(self):
        # Test the complex interaction when mixing file-iteration and the
        # various read* methods. Ostensibly, the mixture could just be tested
        # to work when it should work according to the Python language,
        # instead of fail when it should fail according to the current CPython
        # implementation.  People don't always program Python the way they
        # should, though, and the implemenation might change in subtle ways,
        # so we explicitly test for errors, too; the test will just have to
        # be updated when the implementation changes.
        dataoffset = 16384
        filler = "ham\n"
        assert not dataoffset % len(filler), \
            "dataoffset must be multiple of len(filler)"
        nchunks = dataoffset // len(filler)
        testlines = [
            "spam, spam and eggs\n",
            "eggs, spam, ham and spam\n",
            "saussages, spam, spam and eggs\n",
            "spam, ham, spam and eggs\n",
            "spam, spam, spam, spam, spam, ham, spam\n",
            "wonderful spaaaaaam.\n"
        ]
        methods = [("readline", ()), ("read", ()), ("readlines", ()),
                   ("readinto", (array("c", " "*100),))]

        try:
            # Prepare the testfile
            bag = open(TESTFN, "w")
            bag.write(filler * nchunks)
            bag.writelines(testlines)
            bag.close()
            # Test for appropriate errors mixing read* and iteration
            for methodname, args in methods:
                self.f = f = open(TESTFN)
                if f.next() != filler:
                    self.fail, "Broken testfile"
                meth = getattr(f, methodname)
                try:
                    meth(*args)
                except ValueError:
                    pass
                else:
                    self.fail("%s%r after next() didn't raise ValueError" %
                                     (methodname, args))
                f.close()

            # Test to see if harmless (by accident) mixing of read* and
            # iteration still works. This depends on the size of the internal
            # iteration buffer (currently 8192,) but we can test it in a
            # flexible manner.  Each line in the bag o' ham is 4 bytes
            # ("h", "a", "m", "\n"), so 4096 lines of that should get us
            # exactly on the buffer boundary for any power-of-2 buffersize
            # between 4 and 16384 (inclusive).
            self.f = f = open(TESTFN)
            for i in range(nchunks):
                f.next()
            testline = testlines.pop(0)
            try:
                line = f.readline()
            except ValueError:
                self.fail("readline() after next() with supposedly empty "
                          "iteration-buffer failed anyway")
            if line != testline:
                self.fail("readline() after next() with empty buffer "
                          "failed. Got %r, expected %r" % (line, testline))
            testline = testlines.pop(0)
            buf = array("c", "\x00" * len(testline))
            try:
                f.readinto(buf)
            except ValueError:
                self.fail("readinto() after next() with supposedly empty "
                          "iteration-buffer failed anyway")
            line = buf.tostring()
            if line != testline:
                self.fail("readinto() after next() with empty buffer "
                          "failed. Got %r, expected %r" % (line, testline))

            testline = testlines.pop(0)
            try:
                line = f.read(len(testline))
            except ValueError:
                self.fail("read() after next() with supposedly empty "
                          "iteration-buffer failed anyway")
            if line != testline:
                self.fail("read() after next() with empty buffer "
                          "failed. Got %r, expected %r" % (line, testline))
            try:
                lines = f.readlines()
            except ValueError:
                self.fail("readlines() after next() with supposedly empty "
                          "iteration-buffer failed anyway")
            if lines != testlines:
                self.fail("readlines() after next() with empty buffer "
                          "failed. Got %r, expected %r" % (line, testline))
            # Reading after iteration hit EOF shouldn't hurt either
            self.f = f = open(TESTFN)
            try:
                for line in f:
                    pass
                try:
                    f.readline()
                    f.readinto(buf)
                    f.read()
                    f.readlines()
                except ValueError:
                    self.fail("read* failed after next() consumed file")
            finally:
                f.close()
        finally:
            os.unlink(TESTFN)

    @unittest.skipUnless(test_support.is_jython, "Applicable to Jython")
    def testIterationMixes(self):
        # And now for something completely different. An implementation where
        # various read* methods mix happily with iteration over the lines of
        # a file using next().

        sheep = [
            "It's my belief that these sheep\n",
            "are labouring under the\n",
            "mis-apprehension that they're birds.\n",
            "Now witness their attempts\n",
            "to fly from tree to tree.\n",
            "Notice that they do not so much fly\n",
            "as plummet.\n"
        ]

        # Prepare the testfile
        self.f = f = open(TESTFN, "w")
        f.writelines(sheep)
        f.close()

        # Test for appropriate results mixing read* and iteration
        self.f = f = open(TESTFN)
        self.assertEqual(f.next(), sheep[0])
        self.assertEqual(f.readline(), sheep[1])
        self.assertEqual(f.next(), sheep[2])
        self.assertEqual(f.read(5), sheep[3][:5])

        r = array('c', "1234567")
        f.readinto(r)
        self.assertEqual(r, array('c', sheep[3][5:12]))

        self.assertEqual(f.next(), sheep[3][12:])
        r = f.readlines()
        self.assertEqual(r, sheep[4:])
        self.assertRaises(StopIteration, f.next)

        f.close()


class FileSubclassTests(unittest.TestCase):

    def testExit(self):
        # test that exiting with context calls subclass' close
        class C(file):
            def __init__(self, *args):
                self.subclass_closed = False
                file.__init__(self, *args)
            def close(self):
                self.subclass_closed = True
                file.close(self)

        with C(TESTFN, 'w') as f:
            pass
        self.assertTrue(f.subclass_closed)


@unittest.skipUnless(threading, 'Threading required for this test.')
class FileThreadingTests(unittest.TestCase):
    # These tests check the ability to call various methods of file objects
    # (including close()) concurrently without crashing the Python interpreter.
    # See #815646, #595601

    # Modified for Jython so that each worker thread holds *and closes* its own
    # file object, since we cannot rely on immediate garbage collection closing
    # files. (Open file objects prevent deletion of TESTFN on Windows at least.)

    def setUp(self):
        self._threads = test_support.threading_setup()
        self.filename = TESTFN
        self.exc_info = None
        with open(self.filename, "w") as f:
            f.write("\n".join("0123456789"))
        self._count_lock = threading.Lock()
        self.close_count = 0
        self.close_success_count = 0
        self.use_buffering = False

    def tearDown(self):
        try:
            os.remove(self.filename)
        except EnvironmentError as ee:
            # (Jython addition) detect failure common on Windows, on missing
            # close, that creates spurious errors in subsequent tests.
            if ee.errno != errno.ENOENT:
                raise ee
        test_support.threading_cleanup(*self._threads)

    def _create_file(self):
        if self.use_buffering:
            return open(self.filename, "w+", buffering=1024*16)
        else:
            return open(self.filename, "w+")

    def _close_file(self, f):
        with self._count_lock:
            self.close_count += 1
        f.close()
        with self._count_lock:
            self.close_success_count += 1

    # Close one file object and return a new one
    def _close_and_reopen_file(self, f):
        self._close_file(f)
        return self._create_file()

    def _run_workers(self, func, nb_workers, duration=0.2):
        with self._count_lock:
            self.close_count = 0
            self.close_success_count = 0
        self.do_continue = True
        threads = []
        try:
            for i in range(nb_workers):
                t = threading.Thread(target=func)
                t.start()
                threads.append(t)
            for _ in xrange(100):
                time.sleep(duration/100)
                with self._count_lock:
                    if self.close_count-self.close_success_count > nb_workers+1:
                        if test_support.verbose:
                            print 'Q',
                        break
            time.sleep(duration)
        finally:
            self.do_continue = False
            for t in threads:
                t.join()

    def _test_close_open_io(self, io_func, nb_workers=5):

        def worker():
            # Each worker has its own currently open file object
            myfile = None
            try:
                myfile = self._create_file()
                while self.do_continue:
                    io_func(myfile)
                    myfile = self._close_and_reopen_file(myfile)
            except Exception as e:
                # Stop the test (other threads) and remember why
                self.do_continue = False
                self.exc_info = sys.exc_info()
            # Finally close the last file object
            if myfile:
                self._close_file(myfile)

        self._run_workers(worker, nb_workers)
        if self.exc_info:
            # Some worker saved an exception: re-raise it now
            raise self.exc_info[0], self.exc_info[1], self.exc_info[2]

        if test_support.verbose:
            # Useful verbose statistics when tuning this test to take
            # less time to run but still ensuring that its still useful.
            #
            # the percent of close calls that raised an error
            percent = 100.
            if self.close_count > 0:
                percent -= 100.*self.close_success_count/self.close_count
            print self.close_count, ('%.4f ' % percent),

    # Each test function defines an operation on the worker's file object

    def test_close_open(self):
        def io_func(f):
            pass
        self._test_close_open_io(io_func)

    def test_close_open_flush(self):
        def io_func(f):
            f.flush()
        self._test_close_open_io(io_func)

    def test_close_open_iter(self):
        def io_func(f):
            list(iter(f))
        self._test_close_open_io(io_func)

    def test_close_open_isatty(self):
        def io_func(f):
            f.isatty()
        self._test_close_open_io(io_func)

    def test_close_open_print(self):
        def io_func(f):
            print >> f, ''
        self._test_close_open_io(io_func)

    def test_close_open_print_buffered(self):
        self.use_buffering = True
        def io_func(f):
            print >> f, ''
        self._test_close_open_io(io_func)

    def test_close_open_read(self):
        def io_func(f):
            f.read(0)
        self._test_close_open_io(io_func)

    def test_close_open_readinto(self):
        def io_func(f):
            a = array('c', 'xxxxx')
            f.readinto(a)
        self._test_close_open_io(io_func)

    def test_close_open_readline(self):
        def io_func(f):
            f.readline()
        self._test_close_open_io(io_func)

    def test_close_open_readlines(self):
        def io_func(f):
            f.readlines()
        self._test_close_open_io(io_func)

    def test_close_open_seek(self):
        def io_func(f):
            f.seek(0, 0)
        self._test_close_open_io(io_func)

    def test_close_open_tell(self):
        def io_func(f):
            f.tell()
        self._test_close_open_io(io_func)

    def test_close_open_truncate(self):
        def io_func(f):
            f.truncate()
        self._test_close_open_io(io_func)

    def test_close_open_write(self):
        def io_func(f):
            f.write('')
        self._test_close_open_io(io_func)

    def test_close_open_writelines(self):
        def io_func(f):
            f.writelines('')
        self._test_close_open_io(io_func)


class StdoutTests(unittest.TestCase):

    def test_move_stdout_on_write(self):
        # Issue 3242: sys.stdout can be replaced (and freed) during a
        # print statement; prevent a segfault in this case
        save_stdout = sys.stdout

        class File:
            def write(self, data):
                if '\n' in data:
                    sys.stdout = save_stdout

        try:
            sys.stdout = File()
            print "some text"
        finally:
            sys.stdout = save_stdout

    def test_del_stdout_before_print(self):
        # Issue 4597: 'print' with no argument wasn't reporting when
        # sys.stdout was deleted.
        save_stdout = sys.stdout
        del sys.stdout
        try:
            print
        except RuntimeError as e:
            self.assertEqual(str(e), "lost sys.stdout")
        else:
            self.fail("Expected RuntimeError")
        finally:
            sys.stdout = save_stdout

    def test_unicode(self):
        import subprocess

        def get_message(encoding, *code):
            code = ';'.join(code)   # jython.bat cannot cope with '\n' in arguments
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = encoding
            process = subprocess.Popen([sys.executable, "-c", code],
                                       stdout=subprocess.PIPE, env=env)
            stdout, stderr = process.communicate()
            self.assertEqual(process.returncode, 0)
            return stdout

        def check_message(text, encoding, expected):
            stdout = get_message(encoding,
                "import sys",
                "sys.stdout.write(%r)" % text,
                "sys.stdout.flush()")
            self.assertEqual(stdout, expected)

        # test the encoding
        check_message(u'15\u20ac', "iso-8859-15", "15\xa4")
        check_message(u'15\u20ac', "utf-8", '15\xe2\x82\xac')
        check_message(u'15\u20ac', "utf-16-le", '1\x005\x00\xac\x20')

        # test the error handler
        check_message(u'15\u20ac', "iso-8859-1:ignore", "15")
        check_message(u'15\u20ac', "iso-8859-1:replace", "15?")
        check_message(u'15\u20ac', "iso-8859-1:backslashreplace", "15\\u20ac")

        # test the buffer API
        for objtype in ('buffer', 'bytearray'):
            stdout = get_message('ascii',
                'import sys',
                r'sys.stdout.write(%s("\xe9"))' % objtype,
                'sys.stdout.flush()')
            self.assertEqual(stdout, "\xe9")


def test_main():
    run_unittest(
             AutoFileTests,
             OtherFileTests,
             FileSubclassTests,
             FileThreadingTests,
             StdoutTests
         )

if __name__ == '__main__':
    test_main()
