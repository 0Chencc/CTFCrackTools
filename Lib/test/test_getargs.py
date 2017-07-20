"""Test the internal getargs.c implementation

 PyArg_ParseTuple() is defined here.

The test here is not intended to test all of the module, just the
single case that failed between 2.1 and 2.2a2.
"""

# marshal.loads() uses PyArg_ParseTuple(args, "s#:loads")
# The s code will cause a Unicode conversion to occur.  This test
# verify that the error is propagated properly from the C code back to
# Python.

# XXX If the encoding succeeds using the current default encoding,
# this test will fail because it does not test the right part of the
# PyArg_ParseTuple() implementation.
from test_support import is_jython

import marshal

#since this tests getargs.c impl, ignore for jython.
if not is_jython:
    try:
        marshal.loads(u"\222")
    except UnicodeError:
        pass
