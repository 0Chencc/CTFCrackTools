# -*- coding: iso-8859-1 -*-
from __future__ import with_statement
import os
import re
import subprocess
import sys
import tempfile
import unittest
from test import test_support
from test.test_support import is_jython, is_jython_nt

class SysTest(unittest.TestCase):

    def test_platform(self):
        self.assertEquals(sys.platform[:4], "java",
                          "sys.platform is not java")

    def test_exit_arg(self):
        "sys.exit can be called with args"
        try:
            sys.exit("leaving now")
        except SystemExit, e:
            self.assertEquals(str(e), "leaving now")

    def test_tuple_args(self):
        # Exceptions raised unpacking tuple args have right line number
        def tuple_args( (x,y) ): pass
        try:
            tuple_args( 10 )
        except TypeError:
            tb = sys.exc_info()[2]
            if tb.tb_lineno == 0:
                self.fail("Traceback lineno was zero")

    def test_name(self):
        "sys.__name__ can be reassigned/deleted"
        self.assertEquals(sys.__name__, 'sys')
        sys.__name__ = 'foo'
        self.assert_('foo' in str(sys))
        del sys.__name__
        self.assert_('foo' not in str(sys))
        sys.__name__ = 'sys'

    def test_readonly(self):
        def deleteClass(): del sys.__class__
        self.assertRaises(TypeError, deleteClass)

        def deleteDict(): del sys.__dict__
        self.assertRaises(TypeError, deleteDict)

        def assignClass(): sys.__class__ = object
        self.assertRaises(TypeError, assignClass)

        def assignDict(): sys.__dict__ = {}
        self.assertRaises(TypeError, assignDict)

    def test_resetmethod(self):
        gde = sys.getdefaultencoding
        sys.getdefaultencoding = 5
        self.assertEquals(sys.getdefaultencoding, 5)
        del sys.getdefaultencoding
        self.assertRaises(AttributeError, getattr, sys, 'getdefaultencoding')
        sys.getdefaultencoding = gde

    def test_reload(self):
        gde = sys.getdefaultencoding
        del sys.getdefaultencoding
        reload(sys)
        self.assert_(type(sys.getdefaultencoding) == type(gde))

    def test_get_tuple_from_version_info(self):
        self.assertEqual(type(tuple(sys.version_info)), tuple)

    def test_float_info_tuple(self):
        self.assertEqual(tuple(sys.float_info), sys.float_info)

    def test_long_info_tuple(self):
        self.assertEqual(tuple(sys.long_info), sys.long_info)

    def test_version_info_gt_lt(self):
        self.assertTrue(sys.version_info > (0, 0))
        self.assertTrue(sys.version_info < (99, 99))



def exec_code_separately(function, sharing=False):
    """Runs code in a separate context: (thread, PySystemState, PythonInterpreter)

    A PySystemState is used in conjunction with its thread
    context. This is not so desirable - at the very least it means
    that a thread pool cannot be shared. But this is not the place to
    revisit ancient design decisions."""

    def function_context():
        from org.python.core import Py
        from org.python.util import PythonInterpreter
        from org.python.core import PySystemState

        ps = PySystemState()
        pi = PythonInterpreter({}, ps)
        if not sharing:
            ps.shadow()
            ps.builtins = ps.builtins.copy()
        pi.exec(function.func_code)

    import threading
    context = threading.Thread(target=function_context)
    context.start()
    context.join()


def set_globally():
    import sys
    import test.sys_jy_test_module # used as a probe

    # can't use 'foo', test_with wants to have that undefined
    sys.builtins['test_sys_jy_foo'] = 42


def set_shadow():
    import sys
    sys.builtins['fum'] = 24

class ShadowingTest(unittest.TestCase):

    def setUp(self):
        exec_code_separately(set_globally, sharing=True)
        exec_code_separately(set_shadow)

    def test_super_globals(self):
        import sys, __builtin__

        def get_sym(sym):
            return sys.builtins.get(sym)
        def get_sym_attr(sym):
            return hasattr(__builtin__, sym)

        self.assertEqual(test_sys_jy_foo, 42, "should be able to install a new builtin ('super global')")
        self.assertEqual(get_sym('test_sys_jy_foo'), 42)
        self.assertTrue(get_sym_attr('test_sys_jy_foo'))

        def is_fum_there(): fum
        self.assertRaises(NameError, is_fum_there) # shadowed global ('fum') should not be visible
        self.assertEqual(get_sym('fum'), None)
        self.assertTrue(not(get_sym_attr('fum')))

    def test_sys_modules_per_instance(self):
        import sys
        self.assertTrue('sys_jy_test_module' not in sys.modules, "sys.modules should be per PySystemState instance")


class SyspathResourceTest(unittest.TestCase):
    def setUp(self):
        self.orig_path = sys.path
        sys.path.insert(0, test_support.findfile("bug1373.jar"))

    def tearDown(self):
        sys.path = self.orig_path

    def test_resource_stream_from_syspath(self):
        from pck import Main
        self.assert_(Main.getResourceAsStream('Main.txt'))

    def test_resource_url_from_syspath(self):
        from pck import Main
        self.assert_(Main.getResource('Main.txt'))

    def test_url_from_resource_from_syspath(self):
        from pck import Main
        # Need to test this doesn't fail because of '\' chars in the path
        # Really only a problem on Windows
        self.assert_(Main.getResource('Main.txt').toURI())


class SyspathUnicodeTest(unittest.TestCase):
    """bug 1693: importing from a unicode path threw a unicode encoding
    error"""

    def test_nonexisting_import_from_unicodepath(self):
        # \xf6 = german o umlaut
        sys.path.append(u'/home/tr\xf6\xf6t')
        self.assertRaises(ImportError, __import__, 'non_existing_module')

    def test_import_from_unicodepath(self):
        # \xf6 = german o umlaut
        moduleDir = tempfile.mkdtemp(suffix=u'tr\xf6\xf6t')
        try:
            self.assertTrue(os.path.exists(moduleDir))
            module = 'unicodetempmodule'
            moduleFile = '%s/%s.py' % (moduleDir, module)
            try:
                with open(moduleFile, 'w') as f:
                    f.write('# empty module')
                self.assertTrue(os.path.exists(moduleFile))
                sys.path.append(moduleDir)
                __import__(module)
                moduleClassFile = '%s/%s$py.class' % (moduleDir, module) 
                self.assertTrue(os.path.exists(moduleClassFile))
                os.remove(moduleClassFile)
            finally:
                os.remove(moduleFile)
        finally:
            os.rmdir(moduleDir)
        self.assertFalse(os.path.exists(moduleDir))        

class SysEncodingTest(unittest.TestCase):

    # Adapted from CPython 2.7 test_sys to exercise setting Jython registry
    # values related to encoding and error policy.

    @unittest.skipIf(is_jython_nt, "FIXME: fails probably due to issue 2312")
    def test_ioencoding(self):  # adapted from CPython v2.7 test_sys
        import subprocess, os
        env = dict(os.environ)

        def check(code, encoding=None, errors=None):
            # Execute with encoding and errors optionally set via Java properties
            command = [sys.executable]
            if (encoding):
                command.append('-Dpython.io.encoding={}'.format(encoding))
            if (errors):
                command.append('-Dpython.io.errors={}'.format(errors))
            command.append('-c')
            command.append('print unichr({:#x})'.format(code))
            #print "\n   ", " ".join(command), " ... ",
            p = subprocess.Popen(command, stdout = subprocess.PIPE, env=env)
            return p.stdout.read().strip()

        env.pop("PYTHONIOENCODING", None)
        self.assertEqual(check(ord(u'A')), b"A")

        # Test character: U+00a2 cent sign (¢) is:
        # not representable in ASCII.
        # xml: &#162
        # cp1252: a2
        # cp850: bd
        # cp424: 4a
        # utf-8: c2 a2

        self.assertEqual(check(0xa2, "iso-8859-1"), "¢") # same as this file

        # self.assertEqual(check(0xa2, "ascii"), "") # and an error message
        self.assertEqual(check(0xa2, "ascii", "ignore"),"")
        self.assertEqual(check(0xa2, "ascii", "replace"), "?")
        self.assertEqual(check(0xa2, "ascii", "backslashreplace"), r"\xa2")
        self.assertEqual(check(0xa2, "ascii", "xmlcharrefreplace"), "&#162;")

        self.assertEqual(check(0xa2, "Cp1252"), "\xa2")
        self.assertEqual(check(0xa2, "Cp424"), "\x4a")
        self.assertEqual(check(0xa2, "utf-8"), "\xc2\xa2")

        self.assertEqual(check(0xa2, "iso8859-5", "backslashreplace"), r"\xa2")

        # Now check that PYTHONIOENCODING can be superseded piecemeal
        env["PYTHONIOENCODING"] = "ascii:xmlcharrefreplace"
        self.assertEqual(check(0xa2, "iso8859-5"), "&#162;")
        self.assertEqual(check(0xa2, None, "backslashreplace"), r"\xa2")
        self.assertEqual(check(0xa2, "cp850"), "\xbd")

class SysArgvTest(unittest.TestCase):

    def test_unicode_argv(self):
        # Unicode roundtrips successfully through sys.argv arguments
        zhongwen = u'\u4e2d\u6587'
        with test_support.temp_cwd(name=u"tempcwd-%s" % zhongwen):
            p = subprocess.Popen(
                [sys.executable, '-c',
                 'import sys;' \
                 'sys.stdout.write(sys.argv[1].encode("utf-8"))',
                 zhongwen],
                stdout=subprocess.PIPE)
            self.assertEqual(p.stdout.read().decode("utf-8"), zhongwen)

class InteractivePromptTest(unittest.TestCase):
    # TODO ps1, ps2 being defined for interactive usage should be
    # captured by test_doctest, however, it would be ideal to add
    # pexpect tests (using CPython).

    def test_prompts_not_defined_if_noninteractive(self):
        p = subprocess.Popen(
            [sys.executable, '-c',
             'import sys;' \
             'print hasattr(sys, "ps1");' \
             'print hasattr(sys, "ps2");'],
            stdout=subprocess.PIPE)
        self.assertEqual(p.stdout.read(),
                         os.linesep.join(['False', 'False', '']))

    def test_prompts_not_printed_if_noninteractive(self):
        p = subprocess.Popen(
            [sys.executable],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)
        self.assertEqual(p.communicate('print 47'),
                         ('47' + os.linesep, None))


def test_main():
    test_support.run_unittest(
        SysTest,
        ShadowingTest,
        SyspathResourceTest,
        SyspathUnicodeTest,
        SysEncodingTest,
        SysArgvTest,
        InteractivePromptTest
    )

if __name__ == "__main__":
    test_main()
