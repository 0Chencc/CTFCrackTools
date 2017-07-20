import os
import subprocess
import sys
import unittest
from test import test_support

WINDOWS = (os._name if test_support.is_jython else os.name) == 'nt'

class TestUsingInitializer(unittest.TestCase):

    def test_syspath_initializer(self):
        fn = test_support.findfile('check_for_initializer_in_syspath.py')
        env = dict(CLASSPATH='tests/data/initializer',
                   PATH=os.environ.get('PATH', ''))

        if WINDOWS:
            # TMP is needed to give property java.io.tmpdir a sensible value
            env['TMP'] = os.environ.get('TMP', '.')
            # SystemRoot is needed to remote debug the subprocess JVM
            env['SystemRoot'] = os.environ.get('SystemRoot', '')

        self.assertEquals(0, subprocess.call([sys.executable, fn], env=env))

def test_main():
    test_support.run_unittest(TestUsingInitializer)

if __name__ == "__main__":
    test_main()
