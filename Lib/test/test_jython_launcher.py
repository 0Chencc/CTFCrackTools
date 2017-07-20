# Cross-platform testing of the Jython launcher (bin/jython or bin/jython.exe) using --print
# Replaces test_bat_jy, with some test cases directly used with minor adaptation from that test

import os
import pprint
import shlex
import subprocess
import sys
import unittest
from collections import OrderedDict
from test import test_support

launcher = None
uname = None
is_windows = False
some_jar = os.path.join(os.sep, "a", "b", "c", "some.jar")


def get_launcher(executable):
    # accounts for continued presence of jython bash script
    # when not installed with the installer or if CPython 2.7
    # is not available
    if os._name == "nt":
        return executable
    exec_path = os.path.dirname(sys.executable)
    jython_py = os.path.join(exec_path, "jython.py")
    if os.path.exists(jython_py):
        return jython_py
    else:
        # presumably jython.py has been renamed to jython, generally
        # by the installer
        return executable


def get_uname():
    _uname = None
    try:
        _uname = subprocess.check_output(["uname"]).strip().lower()
        if _uname.startswith("cygwin"):
            _uname = "cygwin"
    except OSError:
        if os._name == "nt":
            _uname = "windows"
    return _uname


def classpath_delimiter():
    return ";" if (os._name == "nt" or uname == "cygwin") else ":"


class TestLauncher(unittest.TestCase):
    
    def get_cmdline(self, cmd, env):

        output = subprocess.check_output(cmd, env=env).rstrip()
        if is_windows:
            return subprocess._cmdline2list(output)
        else:
            return shlex.split(output)

    def get_newenv(self, env=os.environ):
        newenv = env.copy()
        for var in ("CLASSPATH",
                    "JAVA_MEM", "JAVA_HOME", "JAVA_OPTS", "JAVA_STACK",
                    "JYTHON_HOME", "JYTHON_OPTS"):
            try:
                del newenv[var]
            except KeyError:
                pass
        return newenv

    def get_properties(self, args):
        props = OrderedDict()
        for arg in args:
            if arg.startswith("-D"):
                k, v = arg[2:].split("=")
                props[k] = v
        return props
            
    def test_classpath_env(self):
        env = self.get_newenv()
        env["CLASSPATH"] = some_jar
        args = self.get_cmdline([launcher, "--print"], env=env)
        it = iter(args)
        while it:
            arg = next(it)
            if arg == "-classpath":
                self.assertEqual(next(it).split(classpath_delimiter())[-1], some_jar)
                break

    def test_classpath(self):
        env = self.get_newenv()
        args = self.get_cmdline([launcher, "--print", "-J-cp", some_jar], env=env)
        it = iter(args)
        while it:
            arg = next(it)
            if arg == "-classpath":
                self.assertEqual(next(it).split(classpath_delimiter())[-1], some_jar)
                break

    def test_java_home(self):
        env = self.get_newenv()
        my_java = os.path.join(os.sep, "foo", "bar", "my very own (x86) java")
        env["JAVA_HOME"] = my_java
        args = self.get_cmdline([launcher, "--print"], env)
        self.assertEqual(args[0], os.path.join(my_java, "bin", "java"))
        self.assertEqual(args[1], "-Xmx512m")
        self.assertEqual(args[2], "-Xss1024k")
        self.assertEqual(args[-1], "org.python.util.jython")

    def test_java_opts(self):
        env = self.get_newenv()
        env["JAVA_OPTS"] = '-Dfoo=bar -Dbaz="some property" -Xmx2g -classpath %s' % some_jar
        args = self.get_cmdline([launcher, "--print"], env)
        props = self.get_properties(args)
        self.assertEqual(args[0], "java")
        self.assertEqual(args[1], "-Xmx2g")
        self.assertEqual(args[2], "-Xss1024k")
        self.assertEqual(args[3], "-classpath", args)
        self.assertEqual(args[4].split(classpath_delimiter())[-1], some_jar)
        self.assertEqual(args[-1], "org.python.util.jython")
        self.assertEqual(props["foo"], "bar")
        self.assertEqual(props["baz"], "some property")

    def test_default_options(self):
        env = self.get_newenv()
        args = self.get_cmdline([launcher, "--print"], env)
        props = self.get_properties(args)
        self.assertEqual(args[0], "java")
        self.assertEqual(args[1], "-Xmx512m")
        self.assertEqual(args[2], "-Xss1024k")
        self.assertEqual(args[-1], "org.python.util.jython")
        self.assertIn("python.home", props)
        self.assertIn("python.executable", props)
        self.assertIn("python.launcher.uname", props)
        self.assertIn("python.launcher.tty", props)

    def test_mem_env(self):
        env = self.get_newenv()
        env["JAVA_MEM"] = "-Xmx4g"
        env["JAVA_STACK"] = "-Xss2m"
        args = self.get_cmdline([launcher, "--print"], env)
        self.assertEqual(args[0], "java")
        self.assertEqual(args[1], "-Xmx4g")
        self.assertEqual(args[2], "-Xss2m")
        self.assertEqual(args[-1], "org.python.util.jython")

    def test_mem_options(self):
        env = self.get_newenv()
        args = self.get_cmdline([launcher, "-J-Xss2m", "-J-Xmx4g", "--print"], env)
        self.assertEqual(args[0], "java")
        self.assertEqual(args[1], "-Xmx4g", args)
        self.assertEqual(args[2], "-Xss2m", args)
        self.assertEqual(args[-1], "org.python.util.jython")

    def test_jython_opts_env(self):
        env = self.get_newenv()
        env["JYTHON_OPTS"] = '-c "print 47"'
        args = self.get_cmdline([launcher, "--print"], env)
        self.assertEqual(args[0], "java")
        self.assertEqual(args[1], "-Xmx512m")
        self.assertEqual(args[2], "-Xss1024k")
        self.assertEqual(args[-3], "org.python.util.jython")
        self.assertEqual(args[-2], "-c")
        self.assertEqual(args[-1], "print 47")

    def test_options(self):
        env = self.get_newenv()
        args = self.get_cmdline(
            [launcher,
             "-Dquoted=a \"quoted\" option",
             "-Dunder_score=with_underscores",
             "-Dstarred=*/*/more/*/*",
             "--print"], env)
        props = self.get_properties(args)
        self.assertEqual(props["quoted"], 'a "quoted" option')
        self.assertEqual(props["under_score"], "with_underscores")
        self.assertEqual(props["starred"], "*/*/more/*/*")

    def assertHelp(self, output):
        self.assertIn(
            "usage: jython [option] ... [-c cmd | -m mod | file | -] [arg] ...",
            output)

    def test_help(self):
        self.assertHelp(subprocess.check_output([launcher, "--help"], stderr=subprocess.STDOUT))
        self.assertHelp(subprocess.check_output([launcher, "--print", "--help"], stderr=subprocess.STDOUT))
        self.assertHelp(subprocess.check_output([launcher, "--help", "--jdb"], stderr=subprocess.STDOUT))
        with self.assertRaises(subprocess.CalledProcessError) as cm:
            subprocess.check_output([launcher, "--bad-arg"], stderr=subprocess.STDOUT)
        self.assertHelp(cm.exception.output)

    def test_remaining_args(self):
        env = self.get_newenv()
        args = self.get_cmdline([launcher, "--print", "--", "--help"], env)
        self.assertEqual(args[-2], "org.python.util.jython")
        self.assertEqual(args[-1], "--help")

        args = self.get_cmdline([launcher, "--print", "yolk", "--help"], env)
        self.assertEqual(args[-3], "org.python.util.jython")
        self.assertEqual(args[-2], "yolk")
        self.assertEqual(args[-1], "--help")

    def assertCommand(self, command):
        args = self.get_cmdline([launcher, "--print"] + command, self.get_newenv())
        self.assertEqual(args[(len(args) - len(command)):], command)

    def test_file(self):
        self.assertCommand(['test.py'])
    
    def test_dash(self):
        self.assertCommand(['-i'])

    def test_combined(self):
        self.assertCommand(['-W', 'action', 'line'])

    def test_singlequoted(self):
        self.assertCommand(['-c', "'import sys;'"])

    def test_doublequoted(self):
        self.assertCommand(['-c', '"print \'something\'"'])

    def test_nestedquotes(self):
        self.assertCommand(['-c', '"print \'something \"really\" cool\'"'])

    def test_nestedquotes2(self):
        self.assertCommand(['-c', "'print \"something \'really\' cool\"'"])

    def test_starred_args(self):
        self.assertCommand(["my python command.py", "*/*/my ARGS/*.txt"])

    def test_exclamationmark(self):
        self.assertCommand(['-c', 'import sys; print sys.argv[1:]', 'foo!', 'ba!r', '!baz', '!', '!!'])

    def test_percentsign(self):
        self.assertCommand(['-c', 'import sys; print sys.argv[1:]', 'foo%1', 'foo%%1', '%%1bar', '%%1', '%1', '%', '%%'])

    def test_colon(self):
        self.assertCommand(['-c', 'import sys; print sys.argv[1:]', 'foo:', ':bar'])

    def test_semicolon(self):
        self.assertCommand(['-c', ';import sys; print sys.argv[1:]', 'foo;'])


def test_main():
    global is_windows
    global launcher
    global uname

    if sys.executable is None:
        return
    launcher = get_launcher(sys.executable)
    uname = get_uname()
    is_windows = uname in ("cygwin", "windows")
    test_support.run_unittest(
        TestLauncher)


if __name__ == "__main__":
    test_main()
