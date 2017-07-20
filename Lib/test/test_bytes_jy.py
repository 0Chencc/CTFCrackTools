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


def test_main():
    test.test_support.run_unittest(
            ByteArraySubclassTest,
            SimpleOperationsTest,
        )


if __name__ == "__main__":
    test_main()
