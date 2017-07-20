from test.test_support import run_unittest
import unittest
import sys
import imp
import pkgutil
import os
import os.path
import tempfile
import shutil
import zipfile



class PkgutilTests(unittest.TestCase):

    def setUp(self):
        self.dirname = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dirname)
        sys.path.insert(0, self.dirname)

    def tearDown(self):
        del sys.path[0]

    def test_getdata_filesys(self):
        pkg = 'test_getdata_filesys'

        # Include a LF and a CRLF, to test that binary data is read back
        RESOURCE_DATA = 'Hello, world!\nSecond line\r\nThird line'

        # Make a package with some resources
        package_dir = os.path.join(self.dirname, pkg)
        os.mkdir(package_dir)
        # Empty init.py
        f = open(os.path.join(package_dir, '__init__.py'), "wb")
        f.close()
        # Resource files, res.txt, sub/res.txt
        f = open(os.path.join(package_dir, 'res.txt'), "wb")
        f.write(RESOURCE_DATA)
        f.close()
        os.mkdir(os.path.join(package_dir, 'sub'))
        f = open(os.path.join(package_dir, 'sub', 'res.txt'), "wb")
        f.write(RESOURCE_DATA)
        f.close()

        # Check we can read the resources
        res1 = pkgutil.get_data(pkg, 'res.txt')
        self.assertEqual(res1, RESOURCE_DATA)
        res2 = pkgutil.get_data(pkg, 'sub/res.txt')
        self.assertEqual(res2, RESOURCE_DATA)

        del sys.modules[pkg]

    def test_getdata_zipfile(self):
        zip = 'test_getdata_zipfile.zip'
        pkg = 'test_getdata_zipfile'

        # Include a LF and a CRLF, to test that binary data is read back
        RESOURCE_DATA = 'Hello, world!\nSecond line\r\nThird line'

        # Make a package with some resources
        zip_file = os.path.join(self.dirname, zip)
        z = zipfile.ZipFile(zip_file, 'w')

        # Empty init.py
        z.writestr(pkg + '/__init__.py', "")
        # Resource files, res.txt, sub/res.txt
        z.writestr(pkg + '/res.txt', RESOURCE_DATA)
        z.writestr(pkg + '/sub/res.txt', RESOURCE_DATA)
        z.close()

        # Check we can read the resources
        sys.path.insert(0, zip_file)
        res1 = pkgutil.get_data(pkg, 'res.txt')
        self.assertEqual(res1, RESOURCE_DATA)
        res2 = pkgutil.get_data(pkg, 'sub/res.txt')
        self.assertEqual(res2, RESOURCE_DATA)
        del sys.path[0]

        del sys.modules[pkg]

    def test_unreadable_dir_on_syspath(self):
        # issue7367 - walk_packages failed if unreadable dir on sys.path
        package_name = "unreadable_package"
        d = os.path.join(self.dirname, package_name)
        # this does not appear to create an unreadable dir on Windows
        #   but the test should not fail anyway
        os.mkdir(d, 0)
        self.addCleanup(os.rmdir, d)
        for t in pkgutil.walk_packages(path=[self.dirname]):
            self.fail("unexpected package found")

class PkgutilPEP302Tests(unittest.TestCase):

    class MyTestLoader(object):
        def load_module(self, fullname):
            # Create an empty module
            mod = sys.modules.setdefault(fullname, imp.new_module(fullname))
            mod.__file__ = "<%s>" % self.__class__.__name__
            mod.__loader__ = self
            # Make it a package
            mod.__path__ = []
            # Count how many times the module is reloaded
            mod.__dict__['loads'] = mod.__dict__.get('loads',0) + 1
            return mod

        def get_data(self, path):
            return "Hello, world!"

    class MyTestImporter(object):
        def find_module(self, fullname, path=None):
            return PkgutilPEP302Tests.MyTestLoader()

    def setUp(self):
        sys.meta_path.insert(0, self.MyTestImporter())

    def tearDown(self):
        del sys.meta_path[0]

    def test_getdata_pep302(self):
        # Use a dummy importer/loader
        self.assertEqual(pkgutil.get_data('foo', 'dummy'), "Hello, world!")
        del sys.modules['foo']

    def test_alreadyloaded(self):
        # Ensure that get_data works without reloading - the "loads" module
        # variable in the example loader should count how many times a reload
        # occurs.
        import foo
        self.assertEqual(foo.loads, 1)
        self.assertEqual(pkgutil.get_data('foo', 'dummy'), "Hello, world!")
        self.assertEqual(foo.loads, 1)
        del sys.modules['foo']

def test_main():
    run_unittest(PkgutilTests, PkgutilPEP302Tests)
    # this is necessary if test is run repeated (like when finding leaks)
    import zipimport
    zipimport._zip_directory_cache.clear()

if __name__ == '__main__':
    test_main()
