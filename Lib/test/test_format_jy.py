"""String formatting tests

Made for Jython.
"""
from test import test_support
import unittest

class FormatSubclass(unittest.TestCase):
    # Custom __int__ and __float__ should be respected by %-formatting

    def test_int_conversion_support(self):
        class Foo(object):
            def __init__(self, x): self.x = x
            def __int__(self): return self. x
        self.assertEqual('1', '%d' % Foo(1))
        self.assertEqual('1', '%d' % Foo(1L)) # __int__ can return a long, but
                                              # it should be accepted too

    def test_float_conversion_support(self):
        class Foo(object):
            def __init__(self, x): self.x = x
            def __float__(self): return self. x
        self.assertEqual('1.0', '%.1f' % Foo(1.0))

class FormatUnicodeBase(unittest.TestCase):

    # Test padding non-BMP result
    def test_pad_string(self):
        self.padcheck(u"architect")
        self.padcheck(u'a\U00010001cde')

class FormatUnicodeClassic(FormatUnicodeBase):
    # Check using %-formatting

    def padcheck(self, s):
        self.assertEqual(10, len('%10.4s' % s))
        self.assertEqual(u' '*6 + s[0:4], '%10.4s' % s)
        self.assertEqual(u' '*6 + s[0:4], '% 10.4s' % s)
        self.assertEqual(u' '*6 + s[0:4], '%010.4s' % s)
        self.assertEqual(s[0:3] + u' '*5, '%-8.3s' % s)

class FormatUnicodeModern(FormatUnicodeBase):
    # Check using __format__

    def padcheck(self, s):
        self.assertEqual(10, len(format(s, '10.4s')))
        self.assertEqual(s[0:3] + u' '*7, format(s, '10.3s'))
        self.assertEqual(s[0:3] + u'~'*7, format(s, '~<10.3s'))
        self.assertEqual(s[0:3] + u'~'*7, format(s, '~<10.3'))
        self.assertEqual(u' '*6 + s[0:4], format(s, '>10.4s'))
        self.assertEqual(u'*'*6 + s[0:4], format(s, '*>10.4s'))
        self.assertEqual(u'*'*6 + s[0:4], format(s, '*>10.4'))


class FormatMisc(unittest.TestCase):
    # Odd tests Jython used to fail

    def test_str_format_unicode(self):
        # Check unicode is down-converted to str silently if possible
        self.assertEqual("full half hour", "full {:s} hour".format(u"half"))
        self.assertEqual("full \xbd hour", "full {:s} hour".format("\xbd"))
        self.assertRaises(UnicodeEncodeError, "full {:s} hour".format, u"\xbd")
        self.assertEqual(u"full \xbd hour", u"full {:s} hour".format(u"\xbd"))

    def test_mixtures(self) :
        # Check formatting to a common buffer in PyString
        result = 'The cube of 0.5 -0.866j is -1 to 0.01%.'
        self.assertEqual(result, 'The %s of %.3g -%.3fj is -%d to %.2f%%.' %
                          ('cube', 0.5, 0.866, 1, 0.01))
        self.assertEqual(result, 'The %s of %.3g %.3fj is %d to %.2f%%.' %
                          ('cube', 0.5, -0.866, -1, 0.01))
        self.assertEqual(result, 'The%5s of%4.3g%7.3fj is%3d to%5.2f%%.' %
                          ('cube', 0.5, -0.866, -1, 0.01))
        self.assertEqual(result, 'The %-5.4sof %-4.3g%.3fj is %-3dto %.4g%%.' %
                          ('cubensis', 0.5, -0.866, -1, 0.01))

    def test_percent_padded(self) :
        self.assertEqual('%hello', '%%%s' % 'hello')
        self.assertEqual(u'     %hello', '%6%%s' % u'hello')
        self.assertEqual(u'%     hello', u'%-6%%s' % 'hello')

        self.assertEqual('     %', '%6%' % ())
        self.assertEqual('     %', '%06%' % ())
        self.assertEqual('   %', '%*%' % 4)
        self.assertEqual('%     ', '%-6%' % ())
        self.assertEqual('%     ', '%-06%' % ())
        self.assertEqual('%   ', '%*%' % -4)

    def test_formatter_parser(self):

        def check_parse(fmt, expected):
            fmt_list = list(fmt._formatter_parser())
            #print repr(fmt_list)
            self.assertListEqual(fmt_list, expected)
            # Tuples elements are strings with type matching fmt or are None
            t = (type(fmt), type(None))
            for tup in fmt_list :
                for s in tup :
                    self.assertIsInstance(s, t)

        # Verify str._formatter_parser()
        check_parse('{a:8.2f}', [('', 'a', '8.2f', None)])
        check_parse('{a!r}', [('', 'a', '', 'r')])
        check_parse('{a.b[2]!r}', [('', 'a.b[2]', '', 'r')])
        check_parse('A={a:#12x}', [('A=', 'a', '#12x', None)])
        check_parse('Hello {2!r:9s} world!',
                    [('Hello ', '2', '9s', 'r'), (' world!', None, None, None)])

        # Verify unicode._formatter_parser()
        check_parse(u'{a:8.2f}', [(u'', u'a', u'8.2f', None)])
        check_parse(u'{a!r}', [(u'', u'a', u'', u'r')])
        check_parse(u'{a.b[2]!r}', [(u'', u'a.b[2]', u'', u'r')])
        check_parse(u'A={a:#12x}', [(u'A=', u'a', u'#12x', None)])
        check_parse(u'Hello {2!r:9s} world!',
                    [(u'Hello ', u'2', u'9s', u'r'), (u' world!', None, None, None)])

        # Differs from CPython: Jython str._formatter_parser generates the
        # automatic argument number, while CPython leaves it to the client.
        check_parse('hello {:{}d} and {:{}.{}f}',
                    [('hello ', '0', '{}d', None), (' and ', '1', '{}.{}f', None)] )
        check_parse('hello {[2]:{}d} and {.xx:{}.{}f}',
                    [('hello ', '0[2]', '{}d', None), (' and ', '1.xx', '{}.{}f', None)] )
        # The result is the same, however, of:
        self.assertEqual('hello {:{}d} and {:{}.{}f}'.format(20, 16, 12, 8, 4),
                      'hello               20 and  12.0000' )

    def test_formatter_field_name_split(self):

        def check_split(name, xfirst, xrest):
            first, r = name._formatter_field_name_split()
            rest = list(r)
            #print repr(first), repr(rest)
            self.assertEqual(first, xfirst)
            self.assertListEqual(rest, xrest)
            # Types ought to match the original if not numeric
            self.assertIsInstance(first, (type(name), int, long))
            for is_attr, i in rest :
                if is_attr :
                    self.assertIsInstance(i, type(name))
                else :
                    self.assertIsInstance(i, (int, long))

        # Verify str._formatter_field_name_split()
        check_split('a', 'a', [])
        check_split('2', 2, [])
        check_split('.b', '', [(True, 'b')])
        check_split('a.b[2]', 'a', [(True, 'b'), (False, 2)])
        check_split('a.b[2].c[7]', 'a', [(True, 'b'), (False, 2), (True, 'c'), (False, 7)])
        check_split('.b[2].c[7]', '', [(True, 'b'), (False, 2), (True, 'c'), (False, 7)])
        check_split('[3].b[2].c[7]', '',
                    [(False, 3), (True, 'b'), (False, 2), (True, 'c'), (False, 7)])

        # Verify unicode._formatter_field_name_split()
        check_split(u'a', 'a', [])
        check_split(u'2', 2, [])
        check_split(u'.b', '', [(True, 'b')])
        check_split(u'a.b[2]', 'a', [(True, 'b'), (False, 2)])
        check_split(u'a.b[2].c[7]', 'a', [(True, 'b'), (False, 2), (True, 'c'), (False, 7)])
        check_split(u'.b[2].c[7]', '', [(True, 'b'), (False, 2), (True, 'c'), (False, 7)])
        check_split(u'[3].b[2].c[7]', '',
                    [(False, 3), (True, 'b'), (False, 2), (True, 'c'), (False, 7)])


def test_main():
    test_support.run_unittest(
            FormatSubclass,
            FormatUnicodeClassic,
            FormatUnicodeModern,
            FormatMisc,
    )

if __name__ == '__main__':
    test_main()
