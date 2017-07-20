# -*- coding: koi8-r -*-

import unittest
from test import test_support

class PEP263Test(unittest.TestCase):

    def test_pep263(self):
        self.assertEqual(
            u"�����".encode("utf-8"),
            '\xd0\x9f\xd0\xb8\xd1\x82\xd0\xbe\xd0\xbd'
        )
        self.assertEqual(
            u"\�".encode("utf-8"),
            '\\\xd0\x9f'
        )

    def test_compilestring(self):
        # see #1882
        c = compile("\n# coding: utf-8\nu = u'\xc3\xb3'\n", "dummy", "exec")
        d = {}
        exec c in d
        self.assertEqual(d['u'], u'\xf3')


    def test_issue3297(self):
        c = compile("a, b = '\U0001010F', '\\U0001010F'", "dummy", "exec")
        d = {}
        exec(c, d)
        self.assertEqual(d['a'], d['b'])
        self.assertEqual(len(d['a']), len(d['b']))

    def test_issue7820(self):
        # Ensure that check_bom() restores all bytes in the right order if
        # check_bom() fails in pydebug mode: a buffer starts with the first
        # byte of a valid BOM, but next bytes are different

        # one byte in common with the UTF-16-LE BOM
        self.assertRaises(SyntaxError, eval, '\xff\x20')

        # two bytes in common with the UTF-8 BOM
        self.assertRaises(SyntaxError, eval, '\xef\xbb\x20')

def test_main():
    test_support.run_unittest(PEP263Test)

if __name__=="__main__":
    test_main()
