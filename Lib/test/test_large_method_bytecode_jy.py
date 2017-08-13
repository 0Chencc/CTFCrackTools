"""
Tests Jython's capability to handle Python-functions and
methods that are so long that their JVM-bytecode exceeds
JVM method size restrictions.
The case that the main module code exceeds maximal length
is somewhat special, so it is explicitly tested.

Note: As of this writing, a CPython 2.7 bytecode-file (.pyc)
      is required for each module that contains an oversized
      function. The pyc-file is only required at compile-time
      in the sense that if you pre-compile py-files to classes,
      you won't need to distribute the pyc-file; it gets
      embedded into the class-file.
"""

import unittest
from test import test_support

class large_method_tests(unittest.TestCase):
    '''Tests some oversized functions and methods.
    '''

    @classmethod
    def setUpClass(cls):
        import large_methods as _large_methods
        global large_methods
        large_methods = _large_methods

    def test_large_func(self):
        '''Tests a function that slightly exceeds maximal JMV method
        length. It is internally represented as CPython bytecode.
        '''
        self.assertEqual(large_methods.large_function(), 'large 2300')

    def test_large_method(self):
        '''Tests a method that slightly exceeds maximal JMV method
        length. It is internally represented as CPython bytecode.
        '''
        cl = large_methods.OversizedMethodHolder()
        self.assertEqual(cl.large_function(), 'large_method 2300')

    def test_very_large_func(self):
        '''Here we test a function that is so large that its Python bytecode
        exceeds maximal String-literal length. It is automatically split up
        into several literals.
        '''
        self.assertEqual(large_methods.very_large_function(), 'very large 58900')

    def test_small_func(self):
        '''We assert that ordinary-sized, i.e. JVM-bytecode methods still work
        in context of PyBytecode.
        '''
        self.assertEqual(large_methods.small_function(), 'small 10')

class large_module_tests(unittest.TestCase):
    '''Tests a module with oversized main-code.
    So the whole module is represented as a single PyBytecode object.
    Additionally same tests as in large_method_tests are applied.
    '''

    @classmethod
    def setUpClass(cls):
        import large_module as _large_module
        global large_module
        large_module = _large_module

    def test_large_module_main(self):
        '''Tests the module's oversized main-code.
        '''
        self.assertEqual(large_module.count, 2310)

    def test_large_module_method(self):
        cl2 = large_module.OversizedMethodHolder()
        self.assertEqual(cl2.large_function(), 'large_method 2300')

    def test_large_module_large_func(self):
        self.assertEqual(large_module.large_function(), 'large 2300')

    def test_large_module_very_large_func(self):
        self.assertEqual(large_module.very_large_function(), 'very large 58900')

    def test_large_module_small_func(self):
        self.assertEqual(large_module.small_function(), 'small 10')

if __name__ == "__main__":
    unittest.main()

