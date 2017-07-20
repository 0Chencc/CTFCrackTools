import os
import subprocess
import sys
import unittest
from test import test_support


class ImportSiteTestCase(unittest.TestCase):
    
    def test_empty_python_home(self):
        # http://bugs.jython.org/issue2283
        with test_support.temp_cwd() as temp_cwd:
            # using a new directory ensures no Lib/ directory is available
            self.assertEqual(
                subprocess.check_output(
                    [sys.executable, "-Dpython.home=", "-c",
                     "import os; os.system('echo 42'); os.system('echo 47')"])\
                .replace("\r", ""),  # in case of running on Windows
                "42\n47\n")

    def test_bad_python_home(self):
        # http://bugs.jython.org/issue2283
        with test_support.temp_cwd() as temp_cwd:
            os.makedirs(os.path.join(temp_cwd, "Lib"))
            with self.assertRaises(subprocess.CalledProcessError) as cm:
                subprocess.check_output(
                    [sys.executable, "-Dpython.home=%s" % temp_cwd, "-c",
                     "print 42"],
                    stderr=subprocess.STDOUT)
            self.assertIn(
                'Exception in thread "main" ImportError: Cannot import site module and its dependencies: No module named site',
                cm.exception.output)

    def test_property_no_site_import(self):
        # only the minimal set of modules are imported
        with test_support.temp_cwd() as temp_cwd:
            self.assertEqual(
                subprocess.check_output(
                    [sys.executable, "-Dpython.import.site=false", "-c",
                     "import sys; print sorted(sys.modules.keys())"]).strip(),
                "['__builtin__', '__main__', 'exceptions', 'sys']")

    def test_options_no_site_import(self):
        with test_support.temp_cwd() as temp_cwd:
            self.assertEqual(
                subprocess.check_output(
                    [sys.executable, "-S", "-c",
                     "import sys; print sorted(sys.modules.keys())"]).strip(),
                "['__builtin__', '__main__', 'exceptions', 'sys']")


def test_main():
    test_support.run_unittest(
        ImportSiteTestCase,
    )

if __name__ == '__main__':
    test_main()
