# test_import_pep328 - Test various aspects of import 
#
# Copyright (c) 2010 by science+computing ag
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at#
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# Licensed to PSF under a Contributor Agreement.
# See http://www.python.org/2.4/license for licensing details.

'''
Import related tests:

- Test how 'import ...' and 'from ... import ...' invoke the 
  '__import__' function.
- Test the module name resolution of the '__import__'-function.  

The reference is C-python.
'''
import unittest
import exceptions
import imp
import __builtin__
import sys
import types

origImport = __import__ 

class TestImportStatementError(exceptions.ImportError):
    def __init__(self, args):
        names = ['name', 'globals', 'locals', 'fromlist', 'level']
        self.len = len(args)
        for a in args:
            n = names.pop(0)
            setattr(self, n, a)
        for n in names:
            setattr(self, n, None)


class TestImportStatement(unittest.TestCase):
    """Test the 'import' and 'from ... import' statements
    
    This class tests, how the compiler calls the 
    '__import__'-function for various forms of the
    'import' and 'from ... import' statements. 
    """
    
    AI = "from __future__ import absolute_import ;"

    def importFunction(*args):
        if args[0] == '__future__':
            return origImport(*args)
        raise TestImportStatementError(args)
    importFunction = staticmethod(importFunction)

    def setUp(self):
        __builtin__.__import__ = self.importFunction

    def tearDown(self):
        __builtin__.__import__ = origImport

    def runImport(self, statement):
        l = {}
        g = {}
        try:
            exec statement in g, l 
        except TestImportStatementError,e:
            self.assert_(e.globals is g, "globals is changed")
            self.assert_(e.locals is l, "locals is changed")
            return e
        self.fail("Expected a TestImportStatementError")
            
    def testFromDotsOnly(self):
        dots = ''
        for i in range(1,10):
            dots += '.'
            a = self.runImport("from %s import (A,B)" % (dots,))
            self.assertEqual(a.len, 5)
            self.assertEqual(a.name, "")
            self.assertEqual(a.level, i)
            self.assertEqual(a.fromlist, ('A', 'B'))

    def testFromDotsOnlyAs(self):
        dots = ''
        for i in range(1,10):
            dots += '.'
            a = self.runImport("from %s import A as B" % (dots,))
            self.assertEqual(a.len, 5)
            self.assertEqual(a.name, "")
            self.assertEqual(a.fromlist, ('A',))
            self.assertEqual(a.level, i)

    def testFromDotsAndName(self):
        dots = ''
        for i in range(1,10):
            dots += '.'
            a = self.runImport("from %sX import A" % (dots,))
            self.assertEqual(a.len, 5)
            self.assertEqual(a.name, "X")
            self.assertEqual(a.fromlist, ('A',))
            self.assertEqual(a.level, i)

    def testFromDotsAndDotedName(self):
        dots = ''
        for i in range(1,10):
            dots += '.'
            a = self.runImport("from %sX.Y import A" % (dots,))
            self.assertEqual(a.len, 5)
            self.assertEqual(a.name, "X.Y")
            self.assertEqual(a.fromlist, ('A',))
            self.assertEqual(a.level, i)
            
    def testAbsoluteFromDotedNameAs(self):
        a = self.runImport(self.AI + "from X.Y import A as B")
        self.assertEqual(a.len, 5)
        self.assertEqual(a.name, "X.Y")
        self.assertEqual(a.fromlist, ('A',))
        self.assertEqual(a.level, 0)

    def testRelativeOrAbsoluteFromDotedNameAs(self):
        a = self.runImport("from X.Y import A as B")
        self.assertEqual(a.name, "X.Y")
        self.assertEqual(a.fromlist, ('A',))
        self.assertEqual(a.len, 4)

    def testAbsoluteFromDotedNameAll(self):
        a = self.runImport(self.AI + "from X.Y import *")
        self.assertEqual(a.len, 5)
        self.assertEqual(a.name, "X.Y")
        self.assertEqual(a.fromlist, ('*',))
        self.assertEqual(a.level, 0)

    def testRelativeOrAbsoluteFromDotedNameAll(self):
        a = self.runImport("from X.Y import *")
        self.assertEqual(a.name, "X.Y")
        self.assertEqual(a.fromlist, ('*',))
        self.assertEqual(a.len, 4)

    def testAbsoluteImportName(self):
        a = self.runImport(self.AI + "import X")
        self.assertEqual(a.len, 5)
        self.assertEqual(a.name, "X")
        self.assertEqual(a.fromlist, None)
        self.assertEqual(a.level, 0)

    def testAbsoluteImportDotedName(self):
        a = self.runImport(self.AI + "import X.Y")
        self.assertEqual(a.len, 5)
        self.assertEqual(a.name, "X.Y")
        self.assertEqual(a.fromlist, None)
        self.assertEqual(a.level, 0)
        
    def testRelativeOrAbsoluteImportName(self):
        a = self.runImport("import X")
        self.assertEqual(a.name, "X")
        self.assertEqual(a.fromlist, None)
        self.assertEqual(a.len, 4)

    def testRelativeOrAbsoluteImportDotedName(self):
        a = self.runImport("import X.Y")
        self.assertEqual(a.name, "X.Y")
        self.assertEqual(a.fromlist, None)
        self.assertEqual(a.len, 4)

    def testAbsoluteImportDotedNameAs(self):
        a = self.runImport(self.AI + "import X.Y as Z")
        self.assertEqual(a.len, 5)
        self.assertEqual(a.name, "X.Y")
        self.assertEqual(a.fromlist, None)
        self.assertEqual(a.level, 0)


class TestImportFunctionError(exceptions.ImportError):
    pass

class TestImportFunction(unittest.TestCase):
    """Test the '__import__' function
    
    This class tests, how the '__import__'-function
    resolves module names. It uses the 'meta_path' hook,
    to intercept the actual module loading. 
    
    Module Structure:
    
        Top
          \---- X           package
          |     \-- Y       package
          |     |   \-- Z1  module
          |     |   \-- Z2  module
          |     \-- Y2      package
          \---- X2          module
    
    """

    nameX = "TestImportFunctionX"


    def setUp(self):
        self.modX = imp.new_module(self.nameX)
        self.modX.__path__ = ['X']
        
        self.modX2 = imp.new_module(self.nameX+"2")
        self.modY = imp.new_module(self.nameX+".Y")
        self.modY.__path__ = ['X/Y']
        self.modY2 = imp.new_module(self.nameX+".Y2")
        self.modY2.__path__ = ['X/Y']
        self.modZ1 = imp.new_module(self.nameX+".Y.Z1")
        self.modZ2 = imp.new_module(self.nameX+".Y.Z2")

        self.expected = "something_completely_different"
        sys.meta_path.insert(0, self)
        
    def tearDown(self):
        try:
            sys.meta_path.remove(self)
        except ValueError:
            pass
        for k in sys.modules.keys():
            if k.startswith(self.nameX):
                del sys.modules[k]
                
    def importX(self):
        sys.modules[self.modX.__name__] = self.modX
    def importX2(self):
        sys.modules[self.modX2.__name__] = self.modX2
    def importY(self):
        self.importX()
        sys.modules[self.modY.__name__] = self.modY
        self.modX.Y = self.modY
    def importY2(self):
        self.importX()
        sys.modules[self.modY2.__name__] = self.modY2
        self.modX.Y2 = self.modY2
    def importZ1(self):
        self.importY()
        sys.modules[self.modZ1.__name__] = self.modZ1
        self.modY.Z1 = self.modZ1
    def top(self):
        if sys.modules.has_key("__main__"):
            return sys.modules["__main__"].__dict__
        return globals()


    def find_module(self, fullname, path=None):
        if self.expected and self.expected != fullname:
            return None
        self.fullname = fullname
        self.path = path
        return self
    
    def load_module(self, fullname):
        self.assertEqual(fullname, self.fullname)
        raise TestImportFunctionError()
    
    def runImport(self, expected, name, globals, fromlist=None, level=None):
        self.expected = expected
        if isinstance(globals, types.ModuleType):
            globals = globals.__dict__
        try:
            if level is not None:
                __import__(name, globals, None, fromlist, level)
            else:
                __import__(name, globals, None, fromlist)                
        except TestImportFunctionError:
            return
        self.fail("Expected a TestImportFunctionError")
            
    def testRelativeOrAbsolute_top_X2_1(self):
        self.runImport(None, self.modX2.__name__, self.top())
        self.assertEqual(self.fullname, self.modX2.__name__)
        self.assertEqual(self.path, None)

    def testRelativeOrAbsolute_top_X2_2(self):
        self.runImport(None, self.modX2.__name__, self.top(), None, -1)
        self.assertEqual(self.fullname, self.modX2.__name__)
        self.assertEqual(self.path, None)


    def testRelativeOrAbsolute_top_Y_1(self):
        self.importX()
        self.runImport(None, self.modY.__name__, self.top())
        self.assertEqual(self.fullname, self.modY.__name__)
        self.assertEqual(self.path, ['X'])

    def testRelativeOrAbsolute_top_Y_2(self):
        self.importX()
        self.runImport(None, self.modY.__name__, self.top(), None, -1)
        self.assertEqual(self.fullname, self.modY.__name__)
        self.assertEqual(self.path, ['X'])


    def testAbsolute_top_X2(self):
        self.runImport(None, self.modX2.__name__, globals(), None, 0)
        self.assertEqual(self.fullname, self.modX2.__name__)
        self.assertEqual(self.path, None)

    def testAbsolute_top_Y(self):
        self.importX()
        self.runImport(None, self.modY.__name__, globals(), None, 0)
        self.assertEqual(self.fullname, self.modY.__name__)
        self.assertEqual(self.path, ['X'])

    # Relative case
    def testRelativeOrAbsolute_X_X2_rel1(self):
        self.importX()
        self.runImport(None, self.modX2.__name__, self.modX)
        self.assertEqual(self.fullname, self.nameX + "." + self.modX2.__name__)
        self.assertEqual(self.path, ['X'])

    def testRelativeOrAbsolute_X_X2_rel2(self):
        self.importX()
        self.runImport(None, self.modX2.__name__, self.modX, None, -1)
        self.assertEqual(self.path, ['X'])
        self.assertEqual(self.fullname, self.nameX + "." + self.modX2.__name__)

    # Absolute case
    def testRelativeOrAbsolute_X_X2_abs1(self):
        self.importX()
        self.runImport(self.modX2.__name__, self.modX2.__name__, self.modX)
        self.assertEqual(self.fullname, self.modX2.__name__)
        self.assertEqual(self.path, None)

    def testRelativeOrAbsolute_X_X2_abs2(self):
        self.importX()
        self.runImport(self.modX2.__name__, self.modX2.__name__, self.modX, None, -1)
        self.assertEqual(self.path, None)
        self.assertEqual(self.fullname, self.modX2.__name__)

    def testAbsolute_X_X2(self):
        self.importX()
        self.runImport(None, self.modX2.__name__, self.modX, None, 0)
        self.assertEqual(self.fullname, self.modX2.__name__)
        self.assertEqual(self.path, None)

    def testAbsolute_X_Y(self):
        self.importX()
        self.runImport(None, self.modY.__name__, self.modX, None, 0)
        self.assertEqual(self.fullname, self.modY.__name__)
        self.assertEqual(self.path, ['X'])

    def testRelative_Z1_Z2(self):
        self.importZ1()
        self.runImport(None, "", self.modZ1, ['Z2'], 1)
        self.assertEqual(self.fullname, self.modZ2.__name__)
        self.assertEqual(self.path, ['X/Y'])

    def testRelative_Z1_Y2(self):
        self.importZ1()
        self.runImport(None, "", self.modZ1, ["Y2"], 2)
        self.assertEqual(self.fullname, self.modX.__name__+".Y2")
        self.assertEqual(self.path, ['X'])

    def testRelative_Z1_X2(self):
        # """beyond top level"""
        self.importZ1()
        self.assertRaises(ValueError, self.runImport, None, "", self.modZ1, [self.modX2.__name__], 3)

    def testRelative_X2_X(self):
        # """not a package"""
        self.importX2()
        self.assertRaises(ValueError, self.runImport, None, "", self.modX2, [self.modX.__name__], 1)

    def testRelative_X2_Y(self):
        # """not a package"""
        self.importX2()
        self.importX()
        self.assertRaises(ValueError, self.runImport, None, self.modX.__name__, self.modX2, ["Y"], 1)

    def testRelative_X_Z1_1(self):
        self.importX()
        self.runImport(None, "Y", self.modX, ['Z1'], 1)
        self.assertEqual(self.fullname, self.modY.__name__)
        self.assertEqual(self.path, ['X'])

    def testRelative_X_Z1_2(self):
        self.importY()
        self.runImport(None, "Y", self.modX, ['Z1'], 1)
        self.assertEqual(self.fullname, self.modZ1.__name__)
        self.assertEqual(self.path, ['X/Y'])

    def testRelative_Y_Z1(self):
        self.importY()
        self.runImport(None, "Z1", self.modY, ['A', 'B'], 1)
        self.assertEqual(self.fullname, self.modZ1.__name__)
        self.assertEqual(self.path, ['X/Y'])

    def testRelative_Y2_Z1_1(self):
        self.importY2()
        self.runImport(None, "Y", self.modY2, ['Z1'], 2)
        self.assertEqual(self.fullname, self.modY.__name__)
        self.assertEqual(self.path, ['X'])

    def testRelative_Y2_Z1_2(self):
        self.importY2()
        self.importY()
        self.runImport(None, "Y", self.modY2, ['Z1'], 2)
        self.assertEqual(self.fullname, self.modZ1.__name__)
        self.assertEqual(self.path, ['X/Y'])

try:
    from test import test_support
except ImportError:
    test_main = unittest.main
else:
    def test_main():
        test_support.run_unittest(TestImportStatement,
                              TestImportFunction)

if __name__ == '__main__':
    test_main()
