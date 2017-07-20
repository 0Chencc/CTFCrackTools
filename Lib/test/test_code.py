#For Jython, removed co_names, co_consts since these are implementation details
# that may never get implemented, and removed flags since there are implementation
# differences that may never line up.  Still failing on one test for varnames
# because I think it is possible that the order of varnames might be useful (in
# order declared) and Jython doesn't quite get that right.
"""This module includes tests of the code object representation.

>>> def f(x):
...     def g(y):
...         return x + y
...     return g
...

>>> dump(f.func_code)
name: f
argcount: 1
varnames: ('x', 'g')
cellvars: ('x',)
freevars: ()
nlocals: 2

>>> dump(f(4).func_code)
name: g
argcount: 1
varnames: ('y',)
cellvars: ()
freevars: ('x',)
nlocals: 1

>>> def h(x, y):
...     a = x + y
...     b = x - y
...     c = a * b
...     return c
...
>>> dump(h.func_code)
name: h
argcount: 2
varnames: ('x', 'y', 'a', 'b', 'c')
cellvars: ()
freevars: ()
nlocals: 5

>>> def attrs(obj):
...     print obj.attr1
...     print obj.attr2
...     print obj.attr3

>>> dump(attrs.func_code)
name: attrs
argcount: 1
varnames: ('obj',)
cellvars: ()
freevars: ()
nlocals: 1

>>> def optimize_away():
...     'doc string'
...     'not a docstring'
...     53
...     53L

>>> dump(optimize_away.func_code)
name: optimize_away
argcount: 0
varnames: ()
cellvars: ()
freevars: ()
nlocals: 0

"""

import unittest
import weakref
from test import test_support
try:
    import _testcapi
except ImportError:
    _testcapi = None

def consts(t):
    """Yield a doctest-safe sequence of object reprs."""
    for elt in t:
        r = repr(elt)
        if r.startswith("<code object"):
            yield "<code object %s>" % elt.co_name
        else:
            yield r

def dump(co):
    """Print out a text representation of a code object."""
    for attr in ["name", "argcount", "varnames", "cellvars",
                 "freevars", "nlocals"]:
        print "%s: %s" % (attr, getattr(co, "co_" + attr))


class CodeTest(unittest.TestCase):

    @unittest.skipIf(_testcapi is None, "No _testcapi present")
    def test_newempty(self):
        co = _testcapi.code_newempty("filename", "funcname", 15)
        self.assertEqual(co.co_filename, "filename")
        self.assertEqual(co.co_name, "funcname")
        self.assertEqual(co.co_firstlineno, 15)


class CodeWeakRefTest(unittest.TestCase):

    @unittest.skipIf(test_support.is_jython,
                     "weakrefs are not deterministic in Jython")
    def test_basic(self):
        # Create a code object in a clean environment so that we know we have
        # the only reference to it left.
        namespace = {}
        exec "def f(): pass" in globals(), namespace
        f = namespace["f"]
        del namespace

        self.called = False
        def callback(code):
            self.called = True

        # f is now the last reference to the function, and through it, the code
        # object.  While we hold it, check that we can create a weakref and
        # deref it.  Then delete it, and check that the callback gets called and
        # the reference dies.
        coderef = weakref.ref(f.__code__, callback)
        self.assertTrue(bool(coderef()))
        del f
        self.assertFalse(bool(coderef()))
        self.assertTrue(self.called)


def test_main(verbose=None):
    from test.test_support import run_doctest, run_unittest
    from test import test_code
    run_doctest(test_code, verbose)
    run_unittest(CodeTest, CodeWeakRefTest)


if __name__ == "__main__":
    test_main()
