#!/usr/bin/env python
#
# test_codecencodings_tw.py
#   Codec encoding tests for ROC encodings.
#

from test import test_support
from test import test_multibytecodec_support
import unittest
import sys

# Codecs re-synchronise faster after illegal byte in Java 8+ than in Java 7 to
# update 60 (and in CPython 3.3+ faster than in CPython 2.7-3.2). Either is
# correct, but we need to know which one to expect.
RESYNC_FASTER = False # True for CPython 3.3 and later

if sys.platform.startswith('java'):
    if test_support.get_java_version() > (1, 7, 0, 60):
        RESYNC_FASTER = True


class Test_Big5(test_multibytecodec_support.TestBase, unittest.TestCase):
    encoding = 'big5'
    tstring = test_multibytecodec_support.load_teststring('big5')
    if RESYNC_FASTER:
        # Version from CPython 3.6 where \0x80\0x80 is two invalid sequences.
        # Java 8 agrees with this interpretation.
        codectests = (
            # invalid bytes
            (b"abc\x80\x80\xc1\xc4", "strict",  None),
            (b"abc\xc8", "strict",  None),
            (b"abc\x80\x80\xc1\xc4", "replace", u"abc\ufffd\ufffd\u8b10"),
            (b"abc\x80\x80\xc1\xc4\xc8", "replace", u"abc\ufffd\ufffd\u8b10\ufffd"),
            (b"abc\x80\x80\xc1\xc4", "ignore",  u"abc\u8b10"),
        )
    else:
        # Standard version of test from CPython 2.7
        codectests = (
            # invalid bytes
            ("abc\x80\x80\xc1\xc4", "strict",  None),
            ("abc\xc8", "strict",  None),
            ("abc\x80\x80\xc1\xc4", "replace", u"abc\ufffd\u8b10"),
            ("abc\x80\x80\xc1\xc4\xc8", "replace", u"abc\ufffd\u8b10\ufffd"),
            ("abc\x80\x80\xc1\xc4", "ignore",  u"abc\u8b10"),
        )

def test_main():
    test_support.run_unittest(__name__)

if __name__ == "__main__":
    test_main()
