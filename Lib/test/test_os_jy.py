# -*- coding: utf-8 -*-

"""Misc os module tests

Made for Jython.
"""
import os
import sys
import glob
import array
import errno
import struct
import unittest
import subprocess

from test import test_support
from java.io import File


class OSFileTestCase(unittest.TestCase):

    def setUp(self):
        open(test_support.TESTFN, 'w').close()

    def tearDown(self):
        if os.path.exists(test_support.TESTFN):
            os.remove(test_support.TESTFN)

    def test_issue1727(self):
        os.stat(*(test_support.TESTFN,))

    def test_issue1755(self):
        os.remove(test_support.TESTFN)
        self.assertRaises(OSError, os.utime, test_support.TESTFN, None)

    @unittest.skipUnless(hasattr(os, 'link'), "os.link not available")
    def test_issue1824(self):
        os.remove(test_support.TESTFN)
        self.assertRaises(OSError, os.link,
                          test_support.TESTFN, test_support.TESTFN)

    def test_issue1825(self):
        os.remove(test_support.TESTFN)
        testfnu = unicode(test_support.TESTFN)
        try:
            os.open(testfnu, os.O_RDONLY)
        except OSError, e:
            self.assertTrue(isinstance(e.filename, unicode))
            self.assertEqual(e.filename, testfnu)
        else:
            self.assertTrue(False)

        # XXX: currently fail
        #for fn in os.chdir, os.listdir, os.rmdir:
        for fn in (os.rmdir,):
            try:
                fn(testfnu)
            except OSError, e:
                self.assertTrue(isinstance(e.filename, unicode))
                self.assertEqual(e.filename, testfnu)
            else:
                self.assertTrue(False)

    def test_issue2068(self):
        os.remove(test_support.TESTFN)
        for i in range(2):
            fd = os.open(test_support.TESTFN, os.O_RDWR | os.O_CREAT | os.O_APPEND)
            try:
                os.write(fd, bytes('one'))
                os.write(fd, bytes('two'))
                os.write(fd, bytes('three'))
            finally:
                fd.close()

        with open(test_support.TESTFN, 'rb') as f:
            content = f.read()
        self.assertEqual(content, 2 * b'onetwothree')

    def test_issue1793(self):
        # prepare the input file containing 256 bytes of sorted byte-sized numbers
        fd = file(test_support.TESTFN, 'wb')
        try:
            for x in range(256):
                fd.write(chr(x))
        finally:
            fd.close()

        # reopen in read/append mode
        fd = file(test_support.TESTFN, 'rb+')
        try:
            # read forward from the beginning
            for x in range(256):
                pos = fd.tell()
                self.assertEqual(pos, x,
                        '[forward] before read: pos should be %d but is %d' % (x, pos))

                # read just one byte
                c = struct.unpack('B', fd.read(1))[0]

                pos = fd.tell()
                self.assertEqual(pos, x + 1,
                        '[forward] after read: pos should be %d but is %d' % (x + 1, pos))
                
                self.assertEqual(c, x)

            # read backward from the end
            fd.seek(-1, os.SEEK_END)
            for x in range(255, -1, -1):
                pos = fd.tell()
                self.assertEqual(pos, x,
                        '[backward] before read: pos should be %d but is %d' % (x, pos))

                # read just one byte
                c = ord(fd.read(1))

                pos = fd.tell()
                self.assertEqual(pos, x + 1,
                        '[backward] after read: pos should be %d but is %d' % (x + 1, pos))
                
                self.assertEqual(c, x)

                if x > 0:
                    fd.seek(-2, os.SEEK_CUR)
        finally:
            fd.close()


class OSDirTestCase(unittest.TestCase):

    def setUp(self):
        self.base = test_support.TESTFN
        self.path = os.path.join(self.base, 'dir1', 'dir2', 'dir3')
        os.makedirs(self.path)

    def test_rmdir(self):
        # Remove end directory
        os.rmdir(self.path)
        # Fail to remove a chain of directories
        self.assertRaises(OSError, os.rmdir, self.base)

    def test_issue2083(self):
        # Should fail to remove/unlink directory
        self.assertRaises(OSError, os.remove, self.path)
        self.assertRaises(OSError, os.unlink, self.path)

    def tearDown(self):
        # Some dirs may have been deleted. Find the longest that exists.
        p = self.path
        while not os.path.exists(p) and p != self.base:
            p = os.path.dirname(p)
        os.removedirs(p)


class OSStatTestCase(unittest.TestCase):

    def setUp(self):
        open(test_support.TESTFN, 'w').close()

    def tearDown(self):
        if os.path.exists(test_support.TESTFN):
            os.remove(test_support.TESTFN)

    def test_stat_with_trailing_slash(self):
        self.assertRaises(OSError, os.stat, test_support.TESTFN + os.path.sep)
        self.assertRaises(OSError, os.lstat, test_support.TESTFN + os.path.sep)


class OSWriteTestCase(unittest.TestCase):

    def setUp(self):
        self.fd = os.open(test_support.TESTFN, os.O_WRONLY | os.O_CREAT)

    def tearDown(self):
        if self.fd :
            os.close(self.fd)
            if os.path.exists(test_support.TESTFN):
                os.remove(test_support.TESTFN)

    def do_write(self, b, nx=None):
        if nx is None : nx = len(b)
        n = os.write(self.fd, b)
        self.assertEqual(n, nx, "os.write length error: " + repr(b))

    def test_write_buffer(self): # Issue 2062
        s = b"Big Red Book"
        for type2test in (str, buffer, bytearray, (lambda x : array.array('b',x))) :
            self.do_write(type2test(s))

        with memoryview(s) as m :
            self.do_write(m)
            # not contiguous:
            self.assertRaises(BufferError, self.do_write, m[1::2])

        # lacks buffer api:
        self.assertRaises(TypeError, self.do_write, 1.5, 4)

class UnicodeTestCase(unittest.TestCase):

    def test_env(self):
        with test_support.temp_cwd(name=u"tempcwd-中文"):
            newenv = os.environ.copy()
            newenv["TEST_HOME"] = u"首页"
            p = subprocess.Popen([sys.executable, "-c",
                                  'import sys,os;' \
                                  'sys.stdout.write(os.getenv("TEST_HOME").encode("utf-8"))'],
                                 stdout=subprocess.PIPE,
                                 env=newenv)
            self.assertEqual(p.stdout.read().decode("utf-8"), u"首页")
    
    def test_getcwd(self):
        with test_support.temp_cwd(name=u"tempcwd-中文") as temp_cwd:
            p = subprocess.Popen([sys.executable, "-c",
                                  'import sys,os;' \
                                  'sys.stdout.write(os.getcwd().encode("utf-8"))'],
                                 stdout=subprocess.PIPE)
            self.assertEqual(p.stdout.read().decode("utf-8"), temp_cwd)

    def test_listdir(self):
        # It is hard to avoid Unicode paths on systems like OS X. Use
        # relative paths from a temp CWD to work around this
        with test_support.temp_cwd() as new_cwd:
            unicode_path = os.path.join(".", "unicode")
            self.assertIs(type(unicode_path), str)
            chinese_path = os.path.join(unicode_path, u"中文")
            self.assertIs(type(chinese_path), unicode)
            home_path = os.path.join(chinese_path, u"首页")
            os.makedirs(home_path)
            
            with open(os.path.join(home_path, "test.txt"), "w") as test_file:
                test_file.write("42\n")

            # Verify works with str paths, returning Unicode as necessary
            entries = os.listdir(unicode_path)
            self.assertIn(u"中文", entries)

            # Verify works with Unicode paths
            entries = os.listdir(chinese_path)
            self.assertIn(u"首页", entries)
           
            # glob.glob builds on os.listdir; note that we don't use
            # Unicode paths in the arg to glob
            self.assertEqual(
                glob.glob(os.path.join("unicode", "*")),
                [os.path.join(u"unicode", u"中文")])
            self.assertEqual(
                glob.glob(os.path.join("unicode", "*", "*")),
                [os.path.join(u"unicode", u"中文", u"首页")])
            self.assertEqual(
                glob.glob(os.path.join("unicode", "*", "*", "*")),
                [os.path.join(u"unicode", u"中文", u"首页", "test.txt")])

            # Now use a Unicode path as well as in the glob arg
            self.assertEqual(
                glob.glob(os.path.join(u"unicode", "*")),
                [os.path.join(u"unicode", u"中文")])
            self.assertEqual(
                glob.glob(os.path.join(u"unicode", "*", "*")),
                [os.path.join(u"unicode", u"中文", u"首页")])
            self.assertEqual(
                glob.glob(os.path.join(u"unicode", "*", "*", "*")),
                [os.path.join(u"unicode", u"中文", u"首页", "test.txt")])
 
            # Verify Java integration. But we will need to construct
            # an absolute path since chdir doesn't work with Java
            # (except for subprocesses, like below in test_env)
            for entry in entries:
                entry_path = os.path.join(new_cwd, chinese_path, entry)
                f = File(entry_path)
                self.assertTrue(f.exists(), "File %r (%r) should be testable for existence" % (
                    f, entry_path))

class LocaleTestCase(unittest.TestCase):

    def get_installed_locales(self, codes, msg=None):
        def normalize(code):
            # OS X and Ubuntu (at the very least) differ slightly in locale code formatting
            return code.strip().replace("-", "").lower()

        try:
            installed_codes = dict(((normalize(code), code) for 
                                    code in subprocess.check_output(["locale", "-a"]).split()))
        except (subprocess.CalledProcessError, OSError):
            raise unittest.SkipTest("locale command not available, cannot test")

        if msg is None:
            msg = "One of %s tested locales is not installed" % (codes,)
        available_codes = []
        for code in codes:
            if normalize(code) in installed_codes:
                available_codes.append(installed_codes[normalize(code)])
        unittest.skipUnless(available_codes, msg)
        return available_codes

    # must be on posix and turkish locale supported
    def test_turkish_locale_posix_module(self):
        # Verifies fix of http://bugs.jython.org/issue1874
        self.get_installed_locales(["tr_TR.UTF-8"], "Turkish locale not installed, cannot test")
        newenv = os.environ.copy()
        newenv["LC_ALL"] = "tr_TR.UTF-8"  # set to Turkish locale
        self.assertEqual(
            subprocess.check_output(
                [sys.executable, "-c",
                 "import sys; assert 'posix' in sys.builtin_module_names"],
                env=newenv),
            "")

    def test_turkish_locale_string_lower_upper(self):
        # Verifies fix of http://bugs.jython.org/issue1874
        self.get_installed_locales(["tr_TR.UTF-8"], "Turkish locale not installed, cannot test")
        newenv = os.environ.copy()
        newenv["LC_ALL"] = "tr_TR.UTF-8"  # set to Turkish locale
        self.assertIn(
            subprocess.check_output(
                [sys.executable, "-c",
                 'print repr(["I".lower(), u"I".lower(), "i".upper(), u"i".upper()])'],
                env=newenv),
            # Should not convert str for 'i'/'I', but should convert
            # unicode if in Turkish locale; this behavior intentionally is
            # different than CPython; see also http://bugs.python.org/issue17252
            # 
            # Note that JVMs seem to have some latitude here however, so support
            # either for now.
            ["['i', u'\\u0131', 'I', u'\\u0130']\n",
             "['i', u'i', 'I', u'I']\n"])

    def test_strptime_locale(self):
        # Verifies fix of http://bugs.jython.org/issue2261
        newenv = os.environ.copy()
        codes = [
            "cs_CZ.UTF-8", "pl_PL.UTF-8", "ru_RU.UTF-8",
            "sk_SK.UTF-8", "uk_UA.UTF-8", "zh_CN.UTF-8"]
        for code in self.get_installed_locales(codes):
            newenv["LC_ALL"] = code
            self.assertEqual(
                subprocess.check_output(
                    [sys.executable, "-c",
                     'import datetime; print(datetime.datetime.strptime("2015-01-22", "%Y-%m-%d"))'],
                    env=newenv),
                "2015-01-22 00:00:00\n")

    def test_strftime_japanese_locale(self):
        # Verifies fix of http://bugs.jython.org/issue2301 - produces
        # UTF-8 encoded output per what CPython does, rather than Unicode.
        # We will revisit in Jython 3.x!
        self.get_installed_locales("ja_JP.UTF-8")
        self.assertEqual(
            subprocess.check_output(
                [sys.executable, 
                 "-J-Duser.country=JP", "-J-Duser.language=ja",
                 "-c",
                 "import time; print repr(time.strftime('%c', (2015, 3, 29, 14, 55, 13, 6, 88, 0)))"]),
            "'\\xe6\\x97\\xa5 3 29 14:55:13 2015'\n")
        

class SystemTestCase(unittest.TestCase):

    def test_system_no_site_import(self):
        # If not importing site (-S), importing traceback previously
        # would fail with an import error due to creating a circular
        # import chain. This root cause is because the os module
        # imports the subprocess module for the system function; but
        # the subprocess module imports from os. Verrifies that this
        # managed by making the import late; also verify the
        # monkeypatching optimization is successful by calling
        # os.system twice.
        with test_support.temp_cwd() as temp_cwd:
            self.assertEqual(
                subprocess.check_output(
                    [sys.executable, "-S", "-c",
                     "import traceback; import os; os.system('echo 42'); os.system('echo 47')"])\
                .replace("\r", ""),  # in case of running on Windows
                "42\n47\n")


@unittest.skipUnless(hasattr(os, 'link'), "os.link not available")
class LinkTestCase(unittest.TestCase):

    def test_bad_link(self):
        with test_support.temp_cwd() as new_cwd:
            target = os.path.join(new_cwd, "target")
            with open(target, "w") as f:
                f.write("TARGET")
            source = os.path.join(new_cwd, "source")
            with self.assertRaises(OSError) as cm:
                os.link(target, target)
            self.assertEqual(cm.exception.errno, errno.EEXIST)

            with self.assertRaises(OSError) as cm:
                os.link("nonexistent-file", source)
            self.assertEqual(cm.exception.errno, errno.ENOENT)

    def test_link(self):
        with test_support.temp_cwd() as new_cwd:
            target = os.path.join(new_cwd, "target")
            with open(target, "w") as f:
                f.write("TARGET")
            source = os.path.join(new_cwd, "source")
            os.link(target, source)
            with open(source, "r") as f:
                self.assertEqual(f.read(), "TARGET")


@unittest.skipUnless(hasattr(os, 'symlink'), "symbolic link support  not available")
class SymbolicLinkTestCase(unittest.TestCase):

    def test_bad_symlink(self):
        with test_support.temp_cwd() as new_cwd:
            target = os.path.join(new_cwd, "target")
            with open(target, "w") as f:
                f.write("TARGET")
            source = os.path.join(new_cwd, "source")
            with self.assertRaises(OSError) as cm:
                os.symlink(source, target)  # reversed args!
            self.assertEqual(cm.exception.errno, errno.EEXIST)

    def test_readlink(self):
        with test_support.temp_cwd() as new_cwd:
            target = os.path.join(new_cwd, "target")
            with open(target, "w") as f:
                f.write("TARGET")
            source = os.path.join(new_cwd, "source")
            os.symlink(target, source)
            self.assertEqual(os.readlink(source), target)
            self.assertEqual(os.readlink(unicode(source)), unicode(target))
            self.assertIsInstance(os.readlink(unicode(source)), unicode)
            
    def test_readlink_non_symlink(self):
        """os.readlink of a non symbolic link should raise an error"""
        # test for http://bugs.jython.org/issue2292
        with test_support.temp_cwd() as new_cwd:
            target = os.path.join(new_cwd, "target")
            with open(target, "w") as f:
                f.write("TARGET")
            with self.assertRaises(OSError) as cm:
                os.readlink(target)
            self.assertEqual(cm.exception.errno, errno.EINVAL)
            self.assertEqual(cm.exception.filename, target)

    def test_readlink_nonexistent(self):
        with test_support.temp_cwd() as new_cwd:
            nonexistent_file = os.path.join(new_cwd, "nonexistent-file")
            with self.assertRaises(OSError) as cm:
                os.readlink(nonexistent_file)
            self.assertEqual(cm.exception.errno, errno.ENOENT)
            self.assertEqual(cm.exception.filename, nonexistent_file)


def test_main():
    test_support.run_unittest(
        OSFileTestCase, 
        OSDirTestCase,
        OSStatTestCase,
        OSWriteTestCase,
        UnicodeTestCase,
        LocaleTestCase,
        SystemTestCase,
        LinkTestCase,
        SymbolicLinkTestCase,
    )

if __name__ == '__main__':
    test_main()
