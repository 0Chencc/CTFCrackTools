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

EXPLAIN = False # If True, produce commentary in TestImportFunction
MAXDOTS = 10 # adjust enthusiasm of dotted tests

def dump_module(m):
    "Print values of attributes relevant to import mechanism"
    if isinstance(m, types.ModuleType):
        m = m.__dict__
    print "  Module name:     {}".format(m.get('__name__', ''))
    for n in ['__package__', '__path__']:
        print "    {:12s} = {}".format(n, m.get(n,''))

origImport = __import__ 

class TestImportStatementTell(exceptions.ImportError):
    # Raised by TestImportStatement.importFunction to tell us how it was called
    def __init__(self, args):
        # Smuggle the arguments of importFunction() through the call stack
        if EXPLAIN: print "\nimport:"
        names = ['name', 'globals', 'locals', 'fromlist', 'level']
        self.len = len(args)
        for a in args:
            n = names.pop(0)
            setattr(self, n, a)
            if EXPLAIN:
                too_long = not isinstance(a, (int, tuple, str, unicode))
                print "    {:12s}= {}".format(n, a if not too_long else type(a))
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
        raise TestImportStatementTell(args)
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
        except TestImportStatementTell, e:
            self.assert_(e.globals is g, "globals is changed")
            self.assert_(e.locals is l, "locals is changed")
            return e
        self.fail("Expected a TestImportStatementTell")

    @staticmethod
    def dotrange(n=MAXDOTS):
        "Return a longer sequence of dots in each iteration"
        for i in range(1, n):
            yield '.'*i

    def testFromDotsOnly(self):
        for dots in self.dotrange():
            a = self.runImport("from %s import (A,B)" % (dots,))
            self.assertEqual(a.len, 5)
            self.assertEqual(a.name, "")
            self.assertEqual(a.level, len(dots))
            self.assertEqual(a.fromlist, ('A', 'B'))

    def testFromDotsOnlyAs(self):
        for dots in self.dotrange():
            a = self.runImport("from %s import A as B" % (dots,))
            self.assertEqual(a.len, 5)
            self.assertEqual(a.name, "")
            self.assertEqual(a.fromlist, ('A',))
            self.assertEqual(a.level, len(dots))

    def testFromDotsAndName(self):
        for dots in self.dotrange():
            a = self.runImport("from %sX import A" % (dots,))
            self.assertEqual(a.len, 5)
            self.assertEqual(a.name, "X")
            self.assertEqual(a.fromlist, ('A',))
            self.assertEqual(a.level, len(dots))

    def testFromDotsAndDottedName(self):
        for dots in self.dotrange():
            a = self.runImport("from %sX.Y import A" % (dots,))
            self.assertEqual(a.len, 5)
            self.assertEqual(a.name, "X.Y")
            self.assertEqual(a.fromlist, ('A',))
            self.assertEqual(a.level, len(dots))

    def testFromDotsAndDottedNameAll(self):
        for dots in self.dotrange():
            a = self.runImport("from %sX.Y import *" % (dots,))
            self.assertEqual(a.len, 5, "level argument elided") # Issue 2158
            self.assertEqual(a.name, "X.Y")
            self.assertEqual(a.fromlist, ('*',))
            self.assertEqual(a.level, len(dots))

    def testAbsoluteFromDottedNameAs(self):
        a = self.runImport(self.AI + "from X.Y import A as B")
        self.assertEqual(a.len, 5)
        self.assertEqual(a.name, "X.Y")
        self.assertEqual(a.fromlist, ('A',))
        self.assertEqual(a.level, 0)

    def testRelativeOrAbsoluteFromDottedNameAs(self):
        a = self.runImport("from X.Y import A as B")
        self.assertEqual(a.name, "X.Y")
        self.assertEqual(a.fromlist, ('A',))
        self.assertEqual(a.len, 4)

    def testAbsoluteFromDottedNameAll(self):
        a = self.runImport(self.AI + "from X.Y import *")
        self.assertEqual(a.len, 5)
        self.assertEqual(a.name, "X.Y")
        self.assertEqual(a.fromlist, ('*',))
        self.assertEqual(a.level, 0)

    def testRelativeOrAbsoluteFromDottedNameAll(self):
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

    def testAbsoluteImportDottedName(self):
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

    def testRelativeOrAbsoluteImportDottedName(self):
        a = self.runImport("import X.Y")
        self.assertEqual(a.name, "X.Y")
        self.assertEqual(a.fromlist, None)
        self.assertEqual(a.len, 4)

    def testAbsoluteImportDottedNameAs(self):
        a = self.runImport(self.AI + "import X.Y as Z")
        self.assertEqual(a.len, 5)
        self.assertEqual(a.name, "X.Y")
        self.assertEqual(a.fromlist, None)
        self.assertEqual(a.level, 0)


class TestImportFunctionSuccess(exceptions.ImportError):
    pass

class TestImportFunction(unittest.TestCase):
    """Test the '__import__' function

    This class tests, how the '__import__'-function resolves module names.
    It uses the 'meta_path' hook, to intercept the actual module loading.
    When consulted through find_module, it claims to have access to the
    following module structure:

        Top
          +---- X           package
          |     +-- Y       package
          |     |   +-- Z1  module
          |     |   +-- Z2  module
          |     +-- Y2      package
          +---- X2          module

    """

    nameX = "TestImportFunctionX"

    def setUp(self):
        self.modX = self._new_module(None, self.nameX, True)
        self.modY = self._new_module(self.modX, "Y", True)
        self.modZ1 = self._new_module(self.modY, "Z1")
        self.modZ2 = self._new_module(self.modY, "Z2")
        self.modY2 = self._new_module(self.modX, "Y2", True)
        self.modX2 = self._new_module(None, self.nameX + "2")
        self.expected = "something_completely_different"
        sys.meta_path.insert(0, self)

    @staticmethod
    def _new_module(in_package, name, is_package=False):
        if not in_package:
            m = imp.new_module(name)
        else:
            m = imp.new_module(in_package.__name__ + '.' + name)
            if is_package:
                m.__package__ = m.__name__ # surprisingly not the parent name
            else:
                m.__package__ = in_package.__name__
        if is_package:
            m.__path__ = [m.__name__.replace('.', '/')]
        return m

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

    @staticmethod
    def top():
        "Return the __dict__ of a non-package, top-level module"
        # When this program runs as python -m test.test_import_pep328, it is
        # called __main__, but is inside package test, so we must fake it.
        myName = TestImportFunction.nameX[:-1] + "Top"
        return {'__name__': myName, '__package__': None, '__file__': None}

    def find_module(self, fullname, path=None):
        # Simulate the operation of a module finder object on the sys.meta_path
        if EXPLAIN:
            print "find_module:"
            print "    fullname   =", fullname
            print "    path       =", path
        if self.expected and self.expected != fullname:
            # Equivalent of "import name" was called and the import mechanism is
            # trying something other than the expected full name. For example, X
            # called "import X2", and something other than X2 is tried (first).
            return None
        self.fullname = fullname
        self.path = path
        return self

    def load_module(self, fullname):
        # Masquerade as the loader matching fullname
        self.assertEqual(fullname, self.fullname)
        # Signal success, disguised as an ImportError
        raise TestImportFunctionSuccess()

    def runImport(self, expected, name, globals, fromlist=None, level=None):
        self.expected = expected
        if isinstance(globals, types.ModuleType):
            globals = globals.__dict__
        if EXPLAIN:
            print "\nrunImport:"
            dotname = ('.'*level if level>0 else '') + name
            callername = globals['__name__']
            callerpkg = globals.get('__package__', None)
            if fromlist:
                print "    from {} import {} # in {} in package {}".format(
                            dotname, fromlist, callername, callerpkg)
            else:
                print "    import {} # in {} in package {}".format(
                            dotname, callername, callerpkg)
        try:
            if level is not None:
                __import__(name, globals, None, fromlist, level)
            else:
                __import__(name, globals, None, fromlist)
        except TestImportFunctionSuccess:
            return
        self.fail("Expected a TestImportFunctionSuccess")

    def testRelativeOrAbsolute_top_X2_1(self):
        # In context of a non-package, top-level module, find X2.
        # The finder should only be consulted with the absolute name.
        self.runImport(None, self.modX2.__name__, self.top())
        self.assertEqual(self.fullname, self.modX2.__name__)
        self.assertEqual(self.path, None)

    def testRelativeOrAbsolute_top_X2_2(self):
        # In context of a non-package, top-level module, find X2.
        # The finder should only be consulted with the absolute name.
        self.runImport(None, self.modX2.__name__, self.top(), None, -1)
        self.assertEqual(self.fullname, self.modX2.__name__)
        self.assertEqual(self.path, None)

    def testRelativeOrAbsolute_top_Y_1(self):
        # In context of a non-package, top-level module, find X.Y.
        # The finder should only be consulted with the absolute name.
        self.importX()
        self.runImport(None, self.modY.__name__, self.top())
        self.assertEqual(self.fullname, self.modY.__name__)
        self.assertEqual(self.path, [self.nameX])

    def testRelativeOrAbsolute_top_Y_2(self):
        # In context of a non-package, top-level module, find X.Y.
        # The finder should only be consulted with the absolute name.
        self.importX()
        self.runImport(None, self.modY.__name__, self.top(), None, -1)
        self.assertEqual(self.fullname, self.modY.__name__)
        self.assertEqual(self.path, [self.nameX])

    def testAbsolute_top_X2(self):
        # In context of a non-package, top-level module, find X2 absolutely.
        self.runImport(None, self.modX2.__name__, globals(), None, 0)
        self.assertEqual(self.fullname, self.modX2.__name__)
        self.assertEqual(self.path, None)

    def testAbsolute_top_Y(self):
        # In context of a non-package, top-level module, find X.Y absolutely.
        self.importX()
        self.runImport(None, self.modY.__name__, globals(), None, 0)
        self.assertEqual(self.fullname, self.modY.__name__)
        self.assertEqual(self.path, [self.nameX])

    # Relative case
    def testRelativeOrAbsolute_X_X2_rel1(self):
        # In context of package X, look for X2 at X.X2 (where actually it isn't).
        self.importX()
        self.runImport(None, self.modX2.__name__, self.modX)
        self.assertEqual(self.fullname, self.nameX + "." + self.modX2.__name__)
        self.assertEqual(self.path, [self.nameX])

    def testRelativeOrAbsolute_X_X2_rel2(self):
        # In context of package X, look for X2 at X.X2 (where actually it isn't).
        self.importX()
        self.runImport(None, self.modX2.__name__, self.modX, None, -1)
        self.assertEqual(self.path, [self.nameX])
        self.assertEqual(self.fullname, self.nameX + "." + self.modX2.__name__)

    # Absolute case
    def testRelativeOrAbsolute_X_X2_abs1(self):
        # In context of package X, find X2 at absolute X2 (on second attempt).
        self.importX()
        self.runImport(self.modX2.__name__, self.modX2.__name__, self.modX)
        self.assertEqual(self.fullname, self.modX2.__name__)
        self.assertEqual(self.path, None)

    def testRelativeOrAbsolute_X_X2_abs2(self):
        # In context of package X, find X2 at absolute X2 (on second attempt).
        self.importX()
        self.runImport(self.modX2.__name__, self.modX2.__name__, self.modX, None, -1)
        self.assertEqual(self.path, None)
        self.assertEqual(self.fullname, self.modX2.__name__)

    def testAbsolute_X_X2(self):
        # In context of package X, find X2 at explicitly absolute X2.
        self.importX()
        self.runImport(None, self.modX2.__name__, self.modX, None, 0)
        self.assertEqual(self.fullname, self.modX2.__name__)
        self.assertEqual(self.path, None)

    def testAbsolute_X_Y(self):
        # In context of package X, find Y at explicitly absolute X.Y.
        self.importX()
        self.runImport(None, self.modY.__name__, self.modX, None, 0)
        self.assertEqual(self.fullname, self.modY.__name__)
        self.assertEqual(self.path, [self.nameX])

    def testRelative_Z1_Z2(self):
        # In context of module Z1, from . import Z2.
        self.importZ1()
        self.runImport(None, "", self.modZ1, ['Z2'], 1)
        self.assertEqual(self.fullname, self.modZ2.__name__)
        self.assertEqual(self.path, [self.nameX + '/Y'])

    def testRelative_Z1_Y2(self):
        # In context of module Z1, from .. import Y2.
        self.importZ1()
        self.runImport(None, "", self.modZ1, ["Y2"], 2)
        self.assertEqual(self.fullname, self.modX.__name__ + ".Y2")
        self.assertEqual(self.path, [self.nameX])

    def testRelative_Z1_X2(self):
        # In context of module Z1, from ... import X2 (incorrectly beyond top level).
        self.importZ1()
        with self.assertRaises(ValueError):
            self.runImport(None, "", self.modZ1, [self.modX2.__name__], 3)

    def testRelative_X2_X(self):
        # In context of module X2, from . import X (incorrectly)
        # This is incorrect as X2 is not in a package (is a top-level module).
        self.importX2()
        with self.assertRaises(ValueError):
            self.runImport(None, "", self.modX2, [self.modX.__name__], 1)

    def testRelative_X2_Y(self):
        # In context of module X2, from .X import Y (incorrectly).
        # This is incorrect as X2 is not in a package (is a top-level module).
        self.importX2()
        self.importX()
        with self.assertRaises(ValueError):
            self.runImport(None, self.modX.__name__, self.modX2, ["Y"], 1)

    def testRelative_X_Z1_1(self):
        # In context of package X, from .Y import Z1.
        self.importX()
        self.runImport(None, "Y", self.modX, ['Z1'], 1)
        self.assertEqual(self.fullname, self.modY.__name__)
        self.assertEqual(self.path, [self.nameX])

    def testRelative_X_Z1_2(self):
        # In context of package X, from .Y import Z1.
        self.importY()
        self.runImport(None, "Y", self.modX, ['Z1'], 1)
        self.assertEqual(self.fullname, self.modZ1.__name__)
        self.assertEqual(self.path, [self.nameX + '/Y'])

    def testRelative_Y_Z1(self):
        # In context of package Y: from .Z1 import A, B.
        self.importY()
        self.runImport(None, "Z1", self.modY, ['A', 'B'], 1)
        self.assertEqual(self.fullname, self.modZ1.__name__)
        self.assertEqual(self.path, [self.nameX + '/Y'])

    def testRelative_Y2_Z1_1(self):
        # In context of package Y2, from ..Y import Z1.
        self.importY2()
        self.runImport(None, "Y", self.modY2, ['Z1'], 2)
        self.assertEqual(self.fullname, self.modY.__name__)
        self.assertEqual(self.path, [self.nameX])

    def testRelative_Y2_Z1_2(self):
        # In context of package Y2, from ..Y import Z1.
        self.importY2()
        self.importY()
        self.runImport(None, "Y", self.modY2, ['Z1'], 2)
        self.assertEqual(self.fullname, self.modZ1.__name__)
        self.assertEqual(self.path, [self.nameX + '/Y'])


try:
    from test import test_support
except ImportError:
    test_main = unittest.main
else:
    def test_main():
        test_support.run_unittest(
                TestImportStatement,
                TestImportFunction,
                )

if __name__ == '__main__':
    test_main()
