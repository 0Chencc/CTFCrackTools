"""Tests for scripts in the Tools directory.

This file contains regression tests for some of the scripts found in the
Tools directory of a Python checkout or tarball, such as reindent.py.
"""

import os
import sys
import unittest
import shutil
import subprocess
import sysconfig
import tempfile
import textwrap
from test import test_support
from test.script_helper import assert_python_ok, temp_dir

if not sysconfig.is_python_build():
    # XXX some installers do contain the tools, should we detect that
    # and run the tests in that case too?
    raise unittest.SkipTest('test irrelevant for an installed Python')

basepath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                        'Tools')
scriptsdir = os.path.join(basepath, 'scripts')


class ReindentTests(unittest.TestCase):
    script = os.path.join(scriptsdir, 'reindent.py')

    def test_noargs(self):
        assert_python_ok(self.script)

    def test_help(self):
        rc, out, err = assert_python_ok(self.script, '-h')
        self.assertEqual(out, b'')
        self.assertGreater(err, b'')


class PindentTests(unittest.TestCase):
    script = os.path.join(scriptsdir, 'pindent.py')

    def assertFileEqual(self, fn1, fn2):
        with open(fn1) as f1, open(fn2) as f2:
            self.assertEqual(f1.readlines(), f2.readlines())

    def pindent(self, source, *args):
        proc = subprocess.Popen(
                (sys.executable, self.script) + args,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                universal_newlines=True)
        out, err = proc.communicate(source)
        self.assertIsNone(err)
        return out

    def lstriplines(self, data):
        return '\n'.join(line.lstrip() for line in data.splitlines()) + '\n'

    def test_selftest(self):
        self.maxDiff = None
        with temp_dir() as directory:
            data_path = os.path.join(directory, '_test.py')
            with open(self.script) as f:
                closed = f.read()
            with open(data_path, 'w') as f:
                f.write(closed)

            rc, out, err = assert_python_ok(self.script, '-d', data_path)
            self.assertEqual(out, b'')
            self.assertEqual(err, b'')
            backup = data_path + '~'
            self.assertTrue(os.path.exists(backup))
            with open(backup) as f:
                self.assertEqual(f.read(), closed)
            with open(data_path) as f:
                clean = f.read()
            compile(clean, '_test.py', 'exec')
            self.assertEqual(self.pindent(clean, '-c'), closed)
            self.assertEqual(self.pindent(closed, '-d'), clean)

            rc, out, err = assert_python_ok(self.script, '-c', data_path)
            self.assertEqual(out, b'')
            self.assertEqual(err, b'')
            with open(backup) as f:
                self.assertEqual(f.read(), clean)
            with open(data_path) as f:
                self.assertEqual(f.read(), closed)

            broken = self.lstriplines(closed)
            with open(data_path, 'w') as f:
                f.write(broken)
            rc, out, err = assert_python_ok(self.script, '-r', data_path)
            self.assertEqual(out, b'')
            self.assertEqual(err, b'')
            with open(backup) as f:
                self.assertEqual(f.read(), broken)
            with open(data_path) as f:
                indented = f.read()
            compile(indented, '_test.py', 'exec')
            self.assertEqual(self.pindent(broken, '-r'), indented)

    def pindent_test(self, clean, closed):
        self.assertEqual(self.pindent(clean, '-c'), closed)
        self.assertEqual(self.pindent(closed, '-d'), clean)
        broken = self.lstriplines(closed)
        self.assertEqual(self.pindent(broken, '-r', '-e', '-s', '4'), closed)

    def test_statements(self):
        clean = textwrap.dedent("""\
            if a:
                pass

            if a:
                pass
            else:
                pass

            if a:
                pass
            elif:
                pass
            else:
                pass

            while a:
                break

            while a:
                break
            else:
                pass

            for i in a:
                break

            for i in a:
                break
            else:
                pass

            try:
                pass
            finally:
                pass

            try:
                pass
            except TypeError:
                pass
            except ValueError:
                pass
            else:
                pass

            try:
                pass
            except TypeError:
                pass
            except ValueError:
                pass
            finally:
                pass

            with a:
                pass

            class A:
                pass

            def f():
                pass
            """)

        closed = textwrap.dedent("""\
            if a:
                pass
            # end if

            if a:
                pass
            else:
                pass
            # end if

            if a:
                pass
            elif:
                pass
            else:
                pass
            # end if

            while a:
                break
            # end while

            while a:
                break
            else:
                pass
            # end while

            for i in a:
                break
            # end for

            for i in a:
                break
            else:
                pass
            # end for

            try:
                pass
            finally:
                pass
            # end try

            try:
                pass
            except TypeError:
                pass
            except ValueError:
                pass
            else:
                pass
            # end try

            try:
                pass
            except TypeError:
                pass
            except ValueError:
                pass
            finally:
                pass
            # end try

            with a:
                pass
            # end with

            class A:
                pass
            # end class A

            def f():
                pass
            # end def f
            """)
        self.pindent_test(clean, closed)

    def test_multilevel(self):
        clean = textwrap.dedent("""\
            def foobar(a, b):
                if a == b:
                    a = a+1
                elif a < b:
                    b = b-1
                    if b > a: a = a-1
                else:
                    print 'oops!'
            """)
        closed = textwrap.dedent("""\
            def foobar(a, b):
                if a == b:
                    a = a+1
                elif a < b:
                    b = b-1
                    if b > a: a = a-1
                    # end if
                else:
                    print 'oops!'
                # end if
            # end def foobar
            """)
        self.pindent_test(clean, closed)

    def test_preserve_indents(self):
        clean = textwrap.dedent("""\
            if a:
                     if b:
                              pass
            """)
        closed = textwrap.dedent("""\
            if a:
                     if b:
                              pass
                     # end if
            # end if
            """)
        self.assertEqual(self.pindent(clean, '-c'), closed)
        self.assertEqual(self.pindent(closed, '-d'), clean)
        broken = self.lstriplines(closed)
        self.assertEqual(self.pindent(broken, '-r', '-e', '-s', '9'), closed)
        clean = textwrap.dedent("""\
            if a:
            \tif b:
            \t\tpass
            """)
        closed = textwrap.dedent("""\
            if a:
            \tif b:
            \t\tpass
            \t# end if
            # end if
            """)
        self.assertEqual(self.pindent(clean, '-c'), closed)
        self.assertEqual(self.pindent(closed, '-d'), clean)
        broken = self.lstriplines(closed)
        self.assertEqual(self.pindent(broken, '-r'), closed)

    def test_escaped_newline(self):
        clean = textwrap.dedent("""\
            class\\
            \\
             A:
               def\
            \\
            f:
                  pass
            """)
        closed = textwrap.dedent("""\
            class\\
            \\
             A:
               def\
            \\
            f:
                  pass
               # end def f
            # end class A
            """)
        self.assertEqual(self.pindent(clean, '-c'), closed)
        self.assertEqual(self.pindent(closed, '-d'), clean)

    def test_empty_line(self):
        clean = textwrap.dedent("""\
            if a:

                pass
            """)
        closed = textwrap.dedent("""\
            if a:

                pass
            # end if
            """)
        self.pindent_test(clean, closed)

    def test_oneline(self):
        clean = textwrap.dedent("""\
            if a: pass
            """)
        closed = textwrap.dedent("""\
            if a: pass
            # end if
            """)
        self.pindent_test(clean, closed)


def test_main():
    test_support.run_unittest(*[obj for obj in globals().values()
                                    if isinstance(obj, type)])


if __name__ == '__main__':
    unittest.main()
