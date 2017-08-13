import os
import py_compile
import shutil
import sys
import tempfile
import unittest
import zipfile
from test import test_support
from java.lang import Thread

import pkgutil

class ClasspathImporterTestCase(unittest.TestCase):

    def setUp(self):
        self.orig_context = Thread.currentThread().contextClassLoader

    def tearDown(self):
        Thread.currentThread().contextClassLoader = self.orig_context

    # I don't like the checked in jar file bug1239.jar.  The *one* thing I
    # liked about the tests in bugtests/ is that you could create a java file,
    # compile it, jar it and destroy the jar when done.  Maybe when we move to
    # JDK 6 and can use JSR-199 to do runtime compiling, we can go back to
    # that.  Anyway, see http://bugs.jython.org/issue1239. In short, jars added
    # with sys.path.append where not getting scanned if they start with a top
    # level package we already have, like the "org" in org.python.*
    def test_bug1239(self):
        jar = test_support.findfile("bug1239.jar")
        with test_support.DirsOnSysPath(jar):
            import org.test403javapackage.test403

    # different from test_bug1239 in that only a Java package is imported, not
    # a Java class.  I'd also like to get rid of this checked in test jar.
    def test_bug1126(self):
        jar = test_support.findfile("bug1126.jar", subdir="bug1126")
        with test_support.DirsOnSysPath(jar):
            import org.subpackage


class PyclasspathImporterTestCase(unittest.TestCase):

    RESOURCE_DATA = "Always look\non the bright side\r\nof life."

    def setUp(self):
        self.orig_context = Thread.currentThread().contextClassLoader
        self.temp_dir = tempfile.mkdtemp()
        self.modules = sys.modules.keys()

    def tearDown(self):
        Thread.currentThread().contextClassLoader = self.orig_context
        for module in sys.modules.keys():
            if module not in self.modules:
                del sys.modules[module]
        try:
            shutil.rmtree(self.temp_dir)
        except OSError:
            # On Windows at least we cannot delete the open JAR
            pass

    def prepareJar(self, orig_jar):
        # Create a new copy of the checked-in test jar
        orig_jar = test_support.findfile(orig_jar)
        jar = os.path.join(self.temp_dir, os.path.basename(orig_jar))
        shutil.copy(orig_jar, jar)
        return jar

    def compileToJar(self, jar, compile_path=''):
        # Add a compiled version of prefer_compiled.py to the jar
        source = 'prefer_compiled.py'
        code = os.path.join(self.temp_dir, source)
        with open(code, 'w') as fp:
            fp.write('compiled = True')
        # Compile that file
        py_compile.compile(code)
        # Now add the compiled file to the jar
        compiled = source.replace('.py', '$py.class')
        with zipfile.ZipFile(jar, 'a') as zip:
            zip.write(os.path.join(self.temp_dir, compiled),
                      os.path.join(compile_path, 'jar_pkg', compiled))
        return compiled

    def addResourceToJar(self, jar, package='jar_pkg'):
        name = 'testdata.dat'
        with zipfile.ZipFile(jar, 'a') as zip:
            zip.writestr(package + '/' + name, self.RESOURCE_DATA)
        return name

    def checkImports(self, prefix, compiled):
        import flat_in_jar
        self.assertEquals(flat_in_jar.value, 7)
        import jar_pkg
        self.assertEquals(prefix + '/jar_pkg/__init__.py', jar_pkg.__file__)
        from jar_pkg import prefer_compiled
        self.assertEquals(prefix + '/jar_pkg/' + compiled, prefer_compiled.__file__)
        self.assert_(prefer_compiled.compiled)
        self.assertRaises(NameError, __import__, 'flat_bad')
        self.assertRaises(NameError, __import__, 'jar_pkg.bad')

    def test_default_pyclasspath(self):
        jar = self.prepareJar('classimport.jar')
        compiled = self.compileToJar(jar)
        Thread.currentThread().contextClassLoader = test_support.make_jar_classloader(jar)
        self.checkImports('__pyclasspath__', compiled)

    def test_path_in_pyclasspath(self):
        jar = self.prepareJar('classimport_Lib.jar')
        compiled = self.compileToJar(jar, 'Lib')
        Thread.currentThread().contextClassLoader = test_support.make_jar_classloader(jar)
        with test_support.DirsOnSysPath():
            sys.path = ['__pyclasspath__/Lib']
            self.checkImports('__pyclasspath__/Lib', compiled)

    def test_loader_is_package(self):
        jar = self.prepareJar('classimport.jar')
        Thread.currentThread().contextClassLoader = test_support.make_jar_classloader(jar)
        mod_name = 'flat_in_jar'
        loader = pkgutil.get_loader(mod_name)
        self.assertFalse(loader.is_package(mod_name))
        self.assertTrue(loader.is_package('jar_pkg'))
        self.assertFalse(loader.is_package('jar_pkg.prefer_compiled'))

    @unittest.skipIf(test_support.is_jython_posix, "FIXME: failing on Linux issue #2422")
    def test_loader_get_code(self):
        # Execute Python code out of the JAR
        jar = self.prepareJar('classimport.jar')
        Thread.currentThread().contextClassLoader = test_support.make_jar_classloader(jar)
        loader = pkgutil.get_loader('jar_pkg')
        space = { 'value':None, 'compiled':None}

        # flat_in_jar contains the assignment value = 7
        code = loader.get_code('flat_in_jar')
        exec code in space
        self.assertEquals(space['value'], 7)

        # jar_pkg.prefer_compiled contains the assignment compiled = False
        code = loader.get_code('jar_pkg.prefer_compiled')
        exec code in space
        self.assertEquals(space['compiled'], False)

        # Compile a new one containing the assignment compiled = True
        self.compileToJar(jar)
        code = loader.get_code('jar_pkg.prefer_compiled')
        exec code in space
        self.assertEquals(space['compiled'], True)

    def test_pkgutil_get_data(self):
        # Test loader.get_data used via pkgutil
        jar = self.prepareJar('classimport.jar')
        name = self.addResourceToJar(jar)
        Thread.currentThread().contextClassLoader = test_support.make_jar_classloader(jar)
        data = pkgutil.get_data('jar_pkg', name)
        self.assertIsInstance(data, bytes)
        self.assertEqual(data, self.RESOURCE_DATA)

    def test_loader_get_data(self):
        # Test loader.get_data used via pkgutil.get_loader
        jar = self.prepareJar('classimport.jar')
        name = self.addResourceToJar(jar)
        Thread.currentThread().contextClassLoader = test_support.make_jar_classloader(jar)
        loader = pkgutil.get_loader('jar_pkg')
        # path is a resource path (not file system path using os.path.sep)
        path = 'jar_pkg/' + name
        data = loader.get_data(path)
        self.assertIsInstance(data, bytes)
        self.assertEqual(data, self.RESOURCE_DATA)

    def test_importer_get_data(self):
        # Test loader.get_data used via pkgutil.get_importer
        jar = self.prepareJar('classimport.jar')
        name = self.addResourceToJar(jar)
        Thread.currentThread().contextClassLoader = test_support.make_jar_classloader(jar)
        importer = pkgutil.get_importer('__pyclasspath__/')
        # path is a resource path (may be file system path using os.path.sep)
        path = os.path.join('jar_pkg', name)
        data = importer.get_data(path)
        self.assertIsInstance(data, bytes)
        self.assertEqual(data, self.RESOURCE_DATA)
        # Check works a second time (stream use internal to implementation)
        data = importer.get_data(path)
        self.assertEqual(data, self.RESOURCE_DATA)

    def test_importer_get_source(self):
        # Test loader.get_source used via pkgutil.get_importer
        jar = self.prepareJar('classimport.jar')
        Thread.currentThread().contextClassLoader = test_support.make_jar_classloader(jar)
        importer = pkgutil.get_importer('__pyclasspath__/')
        # In package
        mod = 'jar_pkg.prefer_compiled'
        source = importer.get_source(mod)
        self.assertIsInstance(source, bytes)
        self.assertEqual(source, 'compiled = False\n')


def test_main():
    test_support.run_unittest(
                    ClasspathImporterTestCase,
                    PyclasspathImporterTestCase
    )


if __name__ == '__main__':
    test_main()
