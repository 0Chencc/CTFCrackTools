from test import test_support
import unittest

import xdrlib

class XDRTest(unittest.TestCase):

    def test_xdr(self):
        p = xdrlib.Packer()

        s = 'hello world'
        a = ['what', 'is', 'hapnin', 'doctor']

        p.pack_int(42)
        p.pack_int(-17)
        p.pack_uint(9)
        p.pack_bool(True)
        p.pack_bool(False)
        p.pack_uhyper(45L)
        p.pack_float(1.9)
        p.pack_double(1.9)
        p.pack_string(s)
        p.pack_list(range(5), p.pack_uint)
        p.pack_array(a, p.pack_string)

        # now verify
        data = p.get_buffer()
        up = xdrlib.Unpacker(data)

        self.assertEqual(up.get_position(), 0)

        self.assertEqual(up.unpack_int(), 42)
        self.assertEqual(up.unpack_int(), -17)
        self.assertEqual(up.unpack_uint(), 9)
        self.assertTrue(up.unpack_bool() is True)

        # remember position
        pos = up.get_position()
        self.assertTrue(up.unpack_bool() is False)

        # rewind and unpack again
        up.set_position(pos)
        self.assertTrue(up.unpack_bool() is False)

        self.assertEqual(up.unpack_uhyper(), 45L)
        self.assertAlmostEqual(up.unpack_float(), 1.9)
        self.assertAlmostEqual(up.unpack_double(), 1.9)
        self.assertEqual(up.unpack_string(), s)
        self.assertEqual(up.unpack_list(up.unpack_uint), range(5))
        self.assertEqual(up.unpack_array(up.unpack_string), a)
        up.done()
        self.assertRaises(EOFError, up.unpack_uint)

def test_main():
    test_support.run_unittest(XDRTest)

if __name__ == "__main__":
    test_main()
