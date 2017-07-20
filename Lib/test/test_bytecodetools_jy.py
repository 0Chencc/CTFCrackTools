from test import test_support
from jythonlib import bytecodetools as tools 
from java.util.concurrent import Callable
from org.python.core import Options

import glob
import os.path
import sys
import tempfile
import unittest


class BytecodeCallbackTest(unittest.TestCase):

    def setUp(self):
        self.count=0
        tools.clear()

    def assert_callback(self, name, byte, klass):
        self.count+=1
        self.assertEqual(name, klass.name)

    def test_register(self):
        tools.register(self.assert_callback)
        eval("42+1")

    def test_unregister(self):
        self.count=0
        tools.register(self.assert_callback)
        eval("42+1")
        self.assertEqual(self.count, 1)

        tools.unregister(self.assert_callback)
        eval("42+1")
        self.assertEqual(self.count, 1)

    def faulty_callback(self, name, byte, klass):
        raise Exception("test exception")
    def faulty_callback2(self, name, byte, klass, bogus):
        return 

    def test_faulty_callback(self):
        import java.lang.System as Sys
        import java.io.PrintStream as PrintStream
        import java.io.OutputStream as OutputStream

        class NullOutputStream(OutputStream):
            def write(self, b): pass
            def write(self, buf, offset, len): pass

        syserr = Sys.err
        Sys.setErr(PrintStream(NullOutputStream()))

        tools.register(self.faulty_callback)
        tools.register(self.assert_callback)
        tools.register(self.faulty_callback2)
        self.count=0
        try:
            eval("42+1")
        finally:
            self.assertTrue(tools.unregister(self.faulty_callback))
            self.assertTrue(tools.unregister(self.faulty_callback2))
            self.assertTrue(tools.unregister(self.assert_callback))
            Sys.setErr(syserr)
        self.assertEqual(self.count, 1)


class ProxyDebugDirectoryTest(unittest.TestCase):
    """ProxyDebugDirectory used to be the only way to save proxied classes"""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        test_support.rmtree(self.tmpdir)

    def test_set_debug_directory(self):
        """Verify that proxy debug directory can be set at runtime"""
        self.assertIs(Options.proxyDebugDirectory, None)
        Options.proxyDebugDirectory = self.tmpdir

        class C(Callable):
            def call(self):
                return 47
        
        self.assertEqual(C().call(), 47)
        proxy_dir = os.path.join(self.tmpdir, "org", "python", "proxies")
        # If test script is run outside of regrtest, the first path is used;
        # otherwise the second
        proxy_classes = glob.glob(os.path.join(proxy_dir, "*.class")) + \
                        glob.glob(os.path.join(proxy_dir, "test", "*.class"))
        self.assertEqual(len(proxy_classes), 1, "Only one proxy class is generated")
        self.assertRegexpMatches(
            proxy_classes[0],
            r'\$C\$\d+.class$')
        

def test_main():
    test_support.run_unittest(
        BytecodeCallbackTest,
        ProxyDebugDirectoryTest
    )


if __name__ == '__main__':
    test_main()

