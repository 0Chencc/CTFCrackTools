import unittest
from test import test_support

import io
import _io

from os import pipe


class NameTest(unittest.TestCase):

    def test_names_available_in__io_module(self):
        # verifies fix for http://bugs.jython.org/issue2368
        self.assertGreaterEqual(
            set(dir(_io)),
            { 'BlockingIOError', 'BufferedRWPair', 'BufferedRandom',
              'BufferedReader', 'BufferedWriter', 'BytesIO',
              'DEFAULT_BUFFER_SIZE', 'FileIO', 'IncrementalNewlineDecoder',
              'TextIOWrapper', 'UnsupportedOperation',
              '_BufferedIOBase', '_IOBase', '_RawIOBase', '_TextIOBase'
            })


class PipeTestCase(unittest.TestCase):

    def test_pipe_seekable_bool(self):
        r, _ = pipe()

        self.assertFalse(io.open(r).seekable())


def test_main():
    test_support.run_unittest(NameTest, PipeTestCase)


if __name__ == "__main__":
    test_main()
