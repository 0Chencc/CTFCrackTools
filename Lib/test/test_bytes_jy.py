# -*- coding: utf-8 -*-
#
# Tests against problems we have seen in Jython's implementation of
# buffer, bytes, bytearray, and memoryview to prevent possible
# regression as well as integration with Java.

import unittest
import test.test_support


class ByteArraySubclassTest(unittest.TestCase):

    def test_len(self):
        class Sub(bytearray): pass
        s = Sub("abc123")
        self.assertEqual(len(s), 6)


class SimpleOperationsTest(unittest.TestCase):
    # Things the CPython library did not test throughly enough

    def test_irepeat(self) :

        def check_irepeat(a, n) :
            # Check in-place multiplication (repeats)
            b = bytearray(a)
            b *= n
            self.assertEquals(b, bytearray(a*n))

        def irepeat_export(a, n) :
            # In-place multiplication with export mostly raises BufferError
            b = bytearray(a)
            with memoryview(b) as m:
                b *= n
            # If it doesn't raise, it gets the right answer
            self.assertEquals(b, bytearray(a*n))

        for a in [b'', b'a', b'hello'] :
            check_irepeat(a, 7)
            check_irepeat(a, 1)
            check_irepeat(a, 0)
            check_irepeat(a, -1) # -ve treated as 0

        # Resizing with exports should raise an exception
        self.assertRaises(BufferError, irepeat_export, b'a', 5)
        self.assertRaises(BufferError, irepeat_export, b'hello', 3)
        self.assertRaises(BufferError, irepeat_export, b'hello', 0)
        self.assertRaises(BufferError, irepeat_export, b'hello', -1)

        # These don't raise an exception (CPython 2.7.6, 3.4.1)
        irepeat_export(b'a', 1)
        irepeat_export(b'hello', 1)
        for n in range(-1, 3) :
            irepeat_export(b'', n)

    # The following test_is* tests supplement string_tests for non-ascii examples.
    # The principle is to choose some character codes that are letters, digits
    # or spaces in Unicode but not in ASCII and check they are *not* categorised
    # as such in a byte context.

    def checkequal(self, expected, obj, methodname, *args):
        "check that object.method() returns expected result"
        for B in (bytes, bytearray):
            obj = B(obj)
            realresult = getattr(obj, methodname)()
            grumble = "%r.%s() returned %r" % (obj, methodname, realresult)
            self.assertEqual(expected, realresult, grumble)
            # print grumble, 'x' if realresult != expected else '.'

    LOWER = b'\xe0\xe7\xe9\xff' # Uppercase in Latin-1 but not ascii
    UPPER = b'\xc0\xc7\xc9\xdd' # Lowercase in Latin-1 but not ascii
    DIGIT = b'\xb9\xb2\xb3'     # sup 1, 2, 3: numeric in Python (not Java)
    SPACE = b'\x85\xa0'         # NEXT LINE, NBSP: space in Python (not Java)

    def test_isalpha(self):
        for c in self.UPPER + self.LOWER:
            self.checkequal(False, c, 'isalpha')
            self.checkequal(False, b'a' + c + b'Z', 'isalpha')

    def test_isdigit(self):
        for c in self.DIGIT:
            self.checkequal(False, c, 'isdigit')
            self.checkequal(False, b'1' + c + b'3', 'isdigit')

    def test_islower(self):
        for c in self.LOWER:
            self.checkequal(False, c, 'islower')
        for c in self.UPPER:
            self.checkequal(True, b'a' + c + b'z', 'islower')

    def test_isupper(self):
        for c in self.UPPER:
            self.checkequal(False, c, 'isupper')
        for c in self.LOWER:
            self.checkequal(True, b'A' + c + b'Z', 'isupper')

    def test_isspace(self):
        for c in self.SPACE:
            self.checkequal(False, c, 'isspace')
            self.checkequal(False, b'\t' + c + b' ', 'isspace')

    def test_isalnum(self):
        for c in self.UPPER + self.LOWER + self.DIGIT:
            self.checkequal(False, c, 'isalnum')
            self.checkequal(False, b'a' + c + b'3', 'isalnum')

    def test_istitle(self):
        for c in self.UPPER:
            # c should be an un-cased character (effectively a space)
            self.checkequal(False, c, 'istitle')
            self.checkequal(True, b'A' + c + b'Titlecased Line', 'istitle')
            self.checkequal(True, b'A' + c + b' Titlecased Line', 'istitle')
            self.checkequal(True, b'A ' + c + b'Titlecased Line', 'istitle')
        for c in self.LOWER:
            # c should be an un-cased character (effectively a space)
            self.checkequal(True, b'A' + c + b'Titlecased Line', 'istitle')
            self.checkequal(True, b'A ' + c + b' Titlecased Line', 'istitle')

    # The following case-twiddling tests supplement string_tests for
    # non-ascii examples, using characters that are upper/lower-case
    # in latin-1 but uncased in ascii.

    def test_upper(self):
        self.checkequal(b"WAS LOWER:" + self.LOWER,
                        b"was lower:" + self.LOWER, 'upper')

    def test_lower(self):
        self.checkequal(b"was upper:" + self.UPPER,
                        b"WAS UPPER:" + self.UPPER, 'lower')

    def test_capitalize(self):
        for c in self.LOWER:
            self.checkequal(c + b"abcde",
                            c + b"AbCdE", 'capitalize')

    def test_swapcase(self):
        self.checkequal(b"WAS lower:" + self.LOWER,
                        b"was LOWER:" + self.LOWER, 'swapcase')
        self.checkequal(b"was UPPER:" + self.UPPER,
                        b"WAS upper:" + self.UPPER, 'swapcase')

    def test_title(self):
        utitle = u"Le Dîner À Étretat"
        title = utitle.encode('latin-1')
        lower = utitle.lower().encode('latin-1')
        upper = utitle.upper().encode('latin-1')
        # Check we treat an accented character as un-cased (=space)
        self.checkequal(u"Le DîNer à éTretat".encode('latin-1'),
                        lower, 'title')
        self.checkequal(u"Le DÎNer À ÉTretat".encode('latin-1'),
                        upper, 'title')
        self.checkequal(u"Le DîNer À ÉTretat".encode('latin-1'),
                        title, 'title')

    # *strip() tests to supplement string_tests with non-ascii examples,
    # using characters that are spaces in latin-1 but not in ascii.

    def test_strip(self):
        for c in self.SPACE:
            # These should not be stripped at left or right because of c
            sp = b" \t "
            s = c + sp + b"hello" + sp + c
            self.checkequal( s, s, 'strip')
            self.checkequal( s, sp+s+sp, 'strip')
            self.checkequal( sp+s, sp+s, 'rstrip')
            self.checkequal( sp+s, sp+s+sp, 'rstrip')
            self.checkequal( s+sp, s+sp, 'lstrip')
            self.checkequal( s+sp, sp+s+sp, 'lstrip')

    def test_split(self):
        for c in self.SPACE:
            # These should not be split at c
            s = b"AAA" + c + b"BBB"
            self.assertEqual(1, len(s.split()), "split made in " + repr(s))
            self.assertEqual(1, len(s.rsplit()), "rsplit made in " + repr(s))
            s = bytearray(s)
            self.assertEqual(1, len(s.split()), "split made in " + repr(s))
            self.assertEqual(1, len(s.rsplit()), "rsplit made in " + repr(s))


def test_main():
    test.test_support.run_unittest(
            ByteArraySubclassTest,
            SimpleOperationsTest,
        )


if __name__ == "__main__":
    test_main()
