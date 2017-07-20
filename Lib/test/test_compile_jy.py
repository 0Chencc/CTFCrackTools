import __builtin__
import compileall
import os
import py_compile
import shutil
import subprocess
import sys
import textwrap
import unittest
from test.test_support import TESTFN, is_jython, run_unittest, temp_cwd


class TestMtime(unittest.TestCase):

    def test_mtime_compile(self):
        """
        This test exercises the mtime annotation that is now stored in Jython
        compiled files.  CPython already stores an mtime in its pyc files. To
        exercise this functionality, I am writing a py file, compiling it,
        setting the os modified time to a very low value on the compiled file,
        then changing the py file after a small sleep.  On CPython, this would
        still cause a re-compile.  In Jython before this fix it would not.
        See http://bugs.jython.org/issue1024
        """

        import time
        os.mkdir(TESTFN)
        try:
            mod = "mod1"
            source_path = os.path.join(TESTFN, "%s.py" % mod)
            if is_jython:
                compiled_path = os.path.join(TESTFN, "%s$py.class" % mod)
            else:
                compiled_path = os.path.join(TESTFN, "%s.pyc" % mod)
            fp = open(source_path, "w")
            fp.write("def foo(): return 'first'\n")
            fp.close()
            py_compile.compile(source_path)

            #sleep so that the internal mtime is older for the next source write.
            time.sleep(1)

            fp = open(source_path, "w")
            fp.write("def foo(): return 'second'\n")
            fp.close()

            # make sure the source file's mtime is artificially younger than
            # the compiled path's mtime.
            os.utime(source_path, (1,1))

            sys.path.append(TESTFN)
            import mod1
            self.assertEquals(mod1.foo(), 'second')
        finally:
            shutil.rmtree(TESTFN)


class TestCompileall(unittest.TestCase):

    def write_code(self, package, name, code):
        with open(os.path.join(package, name), "w") as f:
            f.write(textwrap.dedent(code))

    def test_compileall(self):
        with temp_cwd():
            PACKAGE = os.path.realpath("./greetings")
            PYC_GREETER = os.path.join(PACKAGE, "greeter.pyc")
            PYCLASS_GREETER = os.path.join(PACKAGE, "greeter$py.class")
            PYCLASS_TEST = os.path.join(PACKAGE, "test$py.class")            

            os.mkdir(PACKAGE)
            self.write_code(
                PACKAGE, "greeter.py",
                """
                def greet():
                    print 'Hello world!'
                """)
            self.write_code(
                PACKAGE, "test.py",
                """
                from greeter import greet
                greet()
                """)

            # pretend we have a Python bytecode compiler by touching this file
            open(PYC_GREETER, "a").close()
            
            compileall.compile_dir(PACKAGE, quiet=True)
            self.assertTrue(os.path.exists(PYC_GREETER))     # still exists
            self.assertTrue(os.path.exists(PYCLASS_TEST))    # along with these new compiled files
            self.assertTrue(os.path.exists(PYCLASS_GREETER))

            # verify we can work with just compiled files
            os.unlink(os.path.join(PACKAGE, "greeter.py"))
            self.assertEqual(
                subprocess.check_output([sys.executable, os.path.join(PACKAGE, "test.py")]).rstrip(),
                "Hello world!")


def test_main():
    run_unittest(TestMtime, TestCompileall)


if __name__ == "__main__":
    test_main()
