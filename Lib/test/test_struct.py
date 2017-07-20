from test.test_support import TestFailed, verbose, verify, vereq, is_jython
import struct
import array
import warnings

if is_jython:
    # currently no buffer type, but this will work fine for this testing
    def buffer(s):
        return str(s)


import sys
ISBIGENDIAN = sys.byteorder == "big"
del sys
verify((struct.pack('=i', 1)[0] == chr(0)) == ISBIGENDIAN,
       "bigendian determination appears wrong")

try:
    import _struct
except ImportError:
    PY_STRUCT_RANGE_CHECKING = 0
    PY_STRUCT_OVERFLOW_MASKING = 1
    PY_STRUCT_FLOAT_COERCE = 2
else:
    PY_STRUCT_RANGE_CHECKING = getattr(_struct, '_PY_STRUCT_RANGE_CHECKING', 0)
    PY_STRUCT_OVERFLOW_MASKING = getattr(_struct, '_PY_STRUCT_OVERFLOW_MASKING', 0)
    PY_STRUCT_FLOAT_COERCE = getattr(_struct, '_PY_STRUCT_FLOAT_COERCE', 0)

def string_reverse(s):
    return "".join(reversed(s))

def bigendian_to_native(value):
    if ISBIGENDIAN:
        return value
    else:
        return string_reverse(value)

def simple_err(func, *args):
    try:
        func(*args)
    except struct.error:
        pass
    else:
        raise TestFailed, "%s%s did not raise struct.error" % (
            func.__name__, args)

def any_err(func, *args):
    try:
        func(*args)
    except (struct.error, TypeError):
        pass
    else:
        raise TestFailed, "%s%s did not raise error" % (
            func.__name__, args)

def with_warning_restore(func):
    def _with_warning_restore(*args, **kw):
        # The `warnings` module doesn't have an advertised way to restore
        # its filter list.  Cheat.
        save_warnings_filters = warnings.filters[:]
        # Grrr, we need this function to warn every time.  Without removing
        # the warningregistry, running test_tarfile then test_struct would fail
        # on 64-bit platforms.
        globals = func.func_globals
        if '__warningregistry__' in globals:
            del globals['__warningregistry__']
        warnings.filterwarnings("error", r"""^struct.*""", DeprecationWarning)
        warnings.filterwarnings("error", r""".*format requires.*""",
                                DeprecationWarning)
        try:
            return func(*args, **kw)
        finally:
            warnings.filters[:] = save_warnings_filters[:]
    return _with_warning_restore

def deprecated_err(func, *args):
    try:
        func(*args)
    except (struct.error, TypeError):
        pass
    except DeprecationWarning:
        if not PY_STRUCT_OVERFLOW_MASKING:
            raise TestFailed, "%s%s expected to raise struct.error" % (
                func.__name__, args)
    else:
        raise TestFailed, "%s%s did not raise error" % (
            func.__name__, args)
deprecated_err = with_warning_restore(deprecated_err)


simple_err(struct.calcsize, 'Z')

sz = struct.calcsize('i')
if sz * 3 != struct.calcsize('iii'):
    raise TestFailed, 'inconsistent sizes'

fmt = 'cbxxxxxxhhhhiillffd'
fmt3 = '3c3b18x12h6i6l6f3d'
sz = struct.calcsize(fmt)
sz3 = struct.calcsize(fmt3)
if sz * 3 != sz3:
    raise TestFailed, 'inconsistent sizes (3*%r -> 3*%d = %d, %r -> %d)' % (
        fmt, sz, 3*sz, fmt3, sz3)

simple_err(struct.pack, 'iii', 3)
simple_err(struct.pack, 'i', 3, 3, 3)
simple_err(struct.pack, 'i', 'foo')
if not is_jython:
    simple_err(struct.pack, 'P', 'foo')
simple_err(struct.unpack, 'd', 'flap')
s = struct.pack('ii', 1, 2)
simple_err(struct.unpack, 'iii', s)
simple_err(struct.unpack, 'i', s)

c = 'a'
b = 1
h = 255
i = 65535
l = 65536
f = 3.1415
d = 3.1415

for prefix in ('', '@', '<', '>', '=', '!'):
    for format in ('xcbhilfd', 'xcBHILfd'):
        format = prefix + format
        if verbose:
            print "trying:", format
        s = struct.pack(format, c, b, h, i, l, f, d)
        cp, bp, hp, ip, lp, fp, dp = struct.unpack(format, s)
        if (cp != c or bp != b or hp != h or ip != i or lp != l or
            int(100 * fp) != int(100 * f) or int(100 * dp) != int(100 * d)):
            # ^^^ calculate only to two decimal places
            raise TestFailed, "unpack/pack not transitive (%s, %s)" % (
                str(format), str((cp, bp, hp, ip, lp, fp, dp)))

# Test some of the new features in detail

# (format, argument, big-endian result, little-endian result, asymmetric)
tests = [
    ('c', 'a', 'a', 'a', 0),
    ('xc', 'a', '\0a', '\0a', 0),
    ('cx', 'a', 'a\0', 'a\0', 0),
    ('s', 'a', 'a', 'a', 0),
    ('0s', 'helloworld', '', '', 1),
    ('1s', 'helloworld', 'h', 'h', 1),
    ('9s', 'helloworld', 'helloworl', 'helloworl', 1),
    ('10s', 'helloworld', 'helloworld', 'helloworld', 0),
    ('11s', 'helloworld', 'helloworld\0', 'helloworld\0', 1),
    ('20s', 'helloworld', 'helloworld'+10*'\0', 'helloworld'+10*'\0', 1),
    ('b', 7, '\7', '\7', 0),
    ('b', -7, '\371', '\371', 0),
    ('B', 7, '\7', '\7', 0),
    ('B', 249, '\371', '\371', 0),
    ('h', 700, '\002\274', '\274\002', 0),
    ('h', -700, '\375D', 'D\375', 0),
    ('H', 700, '\002\274', '\274\002', 0),
    ('H', 0x10000-700, '\375D', 'D\375', 0),
    ('i', 70000000, '\004,\035\200', '\200\035,\004', 0),
    ('i', -70000000, '\373\323\342\200', '\200\342\323\373', 0),
    ('I', 70000000L, '\004,\035\200', '\200\035,\004', 0),
    ('I', 0x100000000L-70000000, '\373\323\342\200', '\200\342\323\373', 0),
    ('l', 70000000, '\004,\035\200', '\200\035,\004', 0),
    ('l', -70000000, '\373\323\342\200', '\200\342\323\373', 0),
    ('L', 70000000L, '\004,\035\200', '\200\035,\004', 0),
    ('L', 0x100000000L-70000000, '\373\323\342\200', '\200\342\323\373', 0),
    ('f', 2.0, '@\000\000\000', '\000\000\000@', 0),
    ('d', 2.0, '@\000\000\000\000\000\000\000',
               '\000\000\000\000\000\000\000@', 0),
    ('f', -2.0, '\300\000\000\000', '\000\000\000\300', 0),
    ('d', -2.0, '\300\000\000\000\000\000\000\000',
               '\000\000\000\000\000\000\000\300', 0),
]

for fmt, arg, big, lil, asy in tests:
    if verbose:
        print "%r %r %r %r" % (fmt, arg, big, lil)
    for (xfmt, exp) in [('>'+fmt, big), ('!'+fmt, big), ('<'+fmt, lil),
                        ('='+fmt, ISBIGENDIAN and big or lil)]:
        res = struct.pack(xfmt, arg)
        if res != exp:
            raise TestFailed, "pack(%r, %r) -> %r # expected %r" % (
                fmt, arg, res, exp)
        n = struct.calcsize(xfmt)
        if n != len(res):
            raise TestFailed, "calcsize(%r) -> %d # expected %d" % (
                xfmt, n, len(res))
        rev = struct.unpack(xfmt, res)[0]
        if rev != arg and not asy:
            raise TestFailed, "unpack(%r, %r) -> (%r,) # expected (%r,)" % (
                fmt, res, rev, arg)

###########################################################################
# Simple native q/Q tests.

has_native_qQ = 1
try:
    struct.pack("q", 5)
except struct.error:
    has_native_qQ = 0

if verbose:
    print "Platform has native q/Q?", has_native_qQ and "Yes." or "No."

any_err(struct.pack, "Q", -1)   # can't pack -1 as unsigned regardless
simple_err(struct.pack, "q", "a")  # can't pack string as 'q' regardless
simple_err(struct.pack, "Q", "a")  # ditto, but 'Q'

def test_native_qQ():
    bytes = struct.calcsize('q')
    # The expected values here are in big-endian format, primarily because
    # I'm on a little-endian machine and so this is the clearest way (for
    # me) to force the code to get exercised.
    for format, input, expected in (
            ('q', -1, '\xff' * bytes),
            ('q', 0, '\x00' * bytes),
            ('Q', 0, '\x00' * bytes),
            ('q', 1L, '\x00' * (bytes-1) + '\x01'),
            ('Q', (1L << (8*bytes))-1, '\xff' * bytes),
            ('q', (1L << (8*bytes-1))-1, '\x7f' + '\xff' * (bytes - 1))):
        got = struct.pack(format, input)
        native_expected = bigendian_to_native(expected)
        verify(got == native_expected,
               "%r-pack of %r gave %r, not %r" %
                    (format, input, got, native_expected))
        retrieved = struct.unpack(format, got)[0]
        verify(retrieved == input,
               "%r-unpack of %r gave %r, not %r" %
                    (format, got, retrieved, input))

if has_native_qQ:
    test_native_qQ()

###########################################################################
# Standard integer tests (bBhHiIlLqQ).

import binascii

class IntTester:

    # XXX Most std integer modes fail to test for out-of-range.
    # The "i" and "l" codes appear to range-check OK on 32-bit boxes, but
    # fail to check correctly on some 64-bit ones (Tru64 Unix + Compaq C
    # reported by Mark Favas).
    BUGGY_RANGE_CHECK = "bBhHiIlL"

    def __init__(self, formatpair, bytesize):
        assert len(formatpair) == 2
        self.formatpair = formatpair
        for direction in "<>!=":
            for code in formatpair:
                format = direction + code
                verify(struct.calcsize(format) == bytesize)
        self.bytesize = bytesize
        self.bitsize = bytesize * 8
        self.signed_code, self.unsigned_code = formatpair
        self.unsigned_min = 0
        self.unsigned_max = 2L**self.bitsize - 1
        self.signed_min = -(2L**(self.bitsize-1))
        self.signed_max = 2L**(self.bitsize-1) - 1

    def test_one(self, x, pack=struct.pack,
                          unpack=struct.unpack,
                          unhexlify=binascii.unhexlify):
        if verbose:
            print "trying std", self.formatpair, "on", x, "==", hex(x)

        # Try signed.
        code = self.signed_code
        if self.signed_min <= x <= self.signed_max:
            # Try big-endian.
            expected = long(x)
            if x < 0:
                expected += 1L << self.bitsize
                assert expected > 0
            expected = hex(expected)[2:-1] # chop "0x" and trailing 'L'
            if len(expected) & 1:
                expected = "0" + expected
            expected = unhexlify(expected)
            expected = "\x00" * (self.bytesize - len(expected)) + expected

            # Pack work?
            format = ">" + code
            got = pack(format, x)
            verify(got == expected,
                   "'%s'-pack of %r gave %r, not %r" %
                    (format, x, got, expected))

            # Unpack work?
            retrieved = unpack(format, got)[0]
            verify(x == retrieved,
                   "'%s'-unpack of %r gave %r, not %r" %
                    (format, got, retrieved, x))

            # Adding any byte should cause a "too big" error.
            any_err(unpack, format, '\x01' + got)

            # Try little-endian.
            format = "<" + code
            expected = string_reverse(expected)

            # Pack work?
            got = pack(format, x)
            verify(got == expected,
                   "'%s'-pack of %r gave %r, not %r" %
                    (format, x, got, expected))

            # Unpack work?
            retrieved = unpack(format, got)[0]
            verify(x == retrieved,
                   "'%s'-unpack of %r gave %r, not %r" %
                    (format, got, retrieved, x))

            # Adding any byte should cause a "too big" error.
            any_err(unpack, format, '\x01' + got)

        else:
            # x is out of range -- verify pack realizes that.
            if not PY_STRUCT_RANGE_CHECKING and code in self.BUGGY_RANGE_CHECK:
                if verbose:
                    print "Skipping buggy range check for code", code
            else:
                deprecated_err(pack, ">" + code, x)
                deprecated_err(pack, "<" + code, x)

        # Much the same for unsigned.
        code = self.unsigned_code
        if self.unsigned_min <= x <= self.unsigned_max:
            # Try big-endian.
            format = ">" + code
            expected = long(x)
            expected = hex(expected)[2:-1] # chop "0x" and trailing 'L'
            if len(expected) & 1:
                expected = "0" + expected
            expected = unhexlify(expected)
            expected = "\x00" * (self.bytesize - len(expected)) + expected

            # Pack work?
            got = pack(format, x)
            verify(got == expected,
                   "'%s'-pack of %r gave %r, not %r" %
                    (format, x, got, expected))

            # Unpack work?
            retrieved = unpack(format, got)[0]
            verify(x == retrieved,
                   "'%s'-unpack of %r gave %r, not %r" %
                    (format, got, retrieved, x))

            # Adding any byte should cause a "too big" error.
            any_err(unpack, format, '\x01' + got)

            # Try little-endian.
            format = "<" + code
            expected = string_reverse(expected)

            # Pack work?
            got = pack(format, x)
            verify(got == expected,
                   "'%s'-pack of %r gave %r, not %r" %
                    (format, x, got, expected))

            # Unpack work?
            retrieved = unpack(format, got)[0]
            verify(x == retrieved,
                   "'%s'-unpack of %r gave %r, not %r" %
                    (format, got, retrieved, x))

            # Adding any byte should cause a "too big" error.
            any_err(unpack, format, '\x01' + got)

        else:
            # x is out of range -- verify pack realizes that.
            if not PY_STRUCT_RANGE_CHECKING and code in self.BUGGY_RANGE_CHECK:
                if verbose:
                    print "Skipping buggy range check for code", code
            else:
                deprecated_err(pack, ">" + code, x)
                deprecated_err(pack, "<" + code, x)

    def run(self):
        from random import randrange

        # Create all interesting powers of 2.
        values = []
        for exp in range(self.bitsize + 3):
            values.append(1L << exp)

        # Add some random values.
        for i in range(self.bitsize):
            val = 0L
            for j in range(self.bytesize):
                val = (val << 8) | randrange(256)
            values.append(val)

        # Try all those, and their negations, and +-1 from them.  Note
        # that this tests all power-of-2 boundaries in range, and a few out
        # of range, plus +-(2**n +- 1).
        for base in values:
            for val in -base, base:
                for incr in -1, 0, 1:
                    x = val + incr
                    try:
                        x = int(x)
                    except OverflowError:
                        pass
                    self.test_one(x)

        # Some error cases.
        for direction in "<>":
            for code in self.formatpair:
                for badobject in "a string", 3+42j, randrange:
                    any_err(struct.pack, direction + code, badobject)

for args in [("bB", 1),
             ("hH", 2),
             ("iI", 4),
             ("lL", 4),
             ("qQ", 8)]:
    t = IntTester(*args)
    t.run()


###########################################################################
# The p ("Pascal string") code.

def test_p_code():
    for code, input, expected, expectedback in [
            ('p','abc', '\x00', ''),
            ('1p', 'abc', '\x00', ''),
            ('2p', 'abc', '\x01a', 'a'),
            ('3p', 'abc', '\x02ab', 'ab'),
            ('4p', 'abc', '\x03abc', 'abc'),
            ('5p', 'abc', '\x03abc\x00', 'abc'),
            ('6p', 'abc', '\x03abc\x00\x00', 'abc'),
            ('1000p', 'x'*1000, '\xff' + 'x'*999, 'x'*255)]:
        got = struct.pack(code, input)
        if got != expected:
            raise TestFailed("pack(%r, %r) == %r but expected %r" %
                             (code, input, got, expected))
        (got,) = struct.unpack(code, got)
        if got != expectedback:
            raise TestFailed("unpack(%r, %r) == %r but expected %r" %
                             (code, input, got, expectedback))

test_p_code()


###########################################################################
# SF bug 705836.  "<f" and ">f" had a severe rounding bug, where a carry
# from the low-order discarded bits could propagate into the exponent
# field, causing the result to be wrong by a factor of 2.

def test_705836():
    import math

    for base in range(1, 33):
        # smaller <- largest representable float less than base.
        delta = 0.5
        while base - delta / 2.0 != base:
            delta /= 2.0
        smaller = base - delta
        # Packing this rounds away a solid string of trailing 1 bits.
        packed = struct.pack("<f", smaller)
        unpacked = struct.unpack("<f", packed)[0]
        # This failed at base = 2, 4, and 32, with unpacked = 1, 2, and
        # 16, respectively.
        verify(base == unpacked)
        bigpacked = struct.pack(">f", smaller)
        verify(bigpacked == string_reverse(packed),
               ">f pack should be byte-reversal of <f pack")
        unpacked = struct.unpack(">f", bigpacked)[0]
        verify(base == unpacked)

    # Largest finite IEEE single.
    big = (1 << 24) - 1
    big = math.ldexp(big, 127 - 23)
    packed = struct.pack(">f", big)
    unpacked = struct.unpack(">f", packed)[0]
    verify(big == unpacked)

    # The same, but tack on a 1 bit so it rounds up to infinity.
    big = (1 << 25) - 1
    big = math.ldexp(big, 127 - 24)
    try:
        packed = struct.pack(">f", big)
    except OverflowError:
        pass
    else:
        TestFailed("expected OverflowError")

test_705836()

###########################################################################
# SF bug 1229380. No struct.pack exception for some out of range integers

def test_1229380():
    import sys
    for endian in ('', '>', '<'):
        for cls in (int, long):
            for fmt in ('B', 'H', 'I', 'L'):
                deprecated_err(struct.pack, endian + fmt, cls(-1))

            deprecated_err(struct.pack, endian + 'B', cls(300))
            deprecated_err(struct.pack, endian + 'H', cls(70000))

        deprecated_err(struct.pack, endian + 'I', sys.maxint * 4L)
        deprecated_err(struct.pack, endian + 'L', sys.maxint * 4L)

if PY_STRUCT_RANGE_CHECKING:
    test_1229380()

###########################################################################
# SF bug 1530559. struct.pack raises TypeError where it used to convert.

def check_float_coerce(format, number):
    if PY_STRUCT_FLOAT_COERCE == 2:
        # Test for pre-2.5 struct module
        packed = struct.pack(format, number)
        floored = struct.unpack(format, packed)[0]
        if floored != int(number):
            raise TestFailed("did not correcly coerce float to int")
        return
    try:
        func(*args)
    except (struct.error, TypeError):
        if PY_STRUCT_FLOAT_COERCE:
            raise TestFailed("expected DeprecationWarning for float coerce")
    except DeprecationWarning:
        if not PY_STRUCT_FLOAT_COERCE:
            raise TestFailed("expected to raise struct.error for float coerce")
    else:
        raise TestFailed("did not raise error for float coerce")

check_float_coerce = with_warning_restore(deprecated_err)

def test_1530559():
    for endian in ('', '>', '<'):
        for fmt in ('B', 'H', 'I', 'L', 'b', 'h', 'i', 'l'):
            check_float_coerce(endian + fmt, 1.0)
            check_float_coerce(endian + fmt, 1.5)

test_1530559()

###########################################################################
# Packing and unpacking to/from buffers.

# Copied and modified from unittest.
def assertRaises(excClass, callableObj, *args, **kwargs):
    try:
        callableObj(*args, **kwargs)
    except excClass:
        return
    else:
        raise TestFailed("%s not raised." % excClass)

def test_unpack_from():
    test_string = 'abcd01234'
    fmt = '4s'
    s = struct.Struct(fmt)
    for cls in (str, buffer):
        data = cls(test_string)
        vereq(s.unpack_from(data), ('abcd',))
        vereq(s.unpack_from(data, 2), ('cd01',))
        vereq(s.unpack_from(data, 4), ('0123',))
        for i in xrange(6):
            vereq(s.unpack_from(data, i), (data[i:i+4],))
        for i in xrange(6, len(test_string) + 1):
            simple_err(s.unpack_from, data, i)
    for cls in (str, buffer):
        data = cls(test_string)
        vereq(struct.unpack_from(fmt, data), ('abcd',))
        vereq(struct.unpack_from(fmt, data, 2), ('cd01',))
        vereq(struct.unpack_from(fmt, data, 4), ('0123',))
        for i in xrange(6):
            vereq(struct.unpack_from(fmt, data, i), (data[i:i+4],))
        for i in xrange(6, len(test_string) + 1):
            simple_err(struct.unpack_from, fmt, data, i)

def test_pack_into():
    test_string = 'Reykjavik rocks, eow!'
    writable_buf = array.array('c', ' '*100)
    fmt = '21s'
    s = struct.Struct(fmt)

    # Test without offset
    s.pack_into(writable_buf, 0, test_string)
    from_buf = writable_buf.tostring()[:len(test_string)]
    vereq(from_buf, test_string)

    # Test with offset.
    s.pack_into(writable_buf, 10, test_string)
    from_buf = writable_buf.tostring()[:len(test_string)+10]
    vereq(from_buf, test_string[:10] + test_string)

    # Go beyond boundaries.
    small_buf = array.array('c', ' '*10)
    assertRaises(struct.error, s.pack_into, small_buf, 0, test_string)
    assertRaises(struct.error, s.pack_into, small_buf, 2, test_string)

def test_pack_into_fn():
    test_string = 'Reykjavik rocks, eow!'
    writable_buf = array.array('c', ' '*100)
    fmt = '21s'
    pack_into = lambda *args: struct.pack_into(fmt, *args)

    # Test without offset.
    pack_into(writable_buf, 0, test_string)
    from_buf = writable_buf.tostring()[:len(test_string)]
    vereq(from_buf, test_string)

    # Test with offset.
    pack_into(writable_buf, 10, test_string)
    from_buf = writable_buf.tostring()[:len(test_string)+10]
    vereq(from_buf, test_string[:10] + test_string)

    # Go beyond boundaries.
    small_buf = array.array('c', ' '*10)
    assertRaises(struct.error, pack_into, small_buf, 0, test_string)
    assertRaises(struct.error, pack_into, small_buf, 2, test_string)

def test_unpack_with_buffer():
    # SF bug 1563759: struct.unpack doens't support buffer protocol objects
    data = array.array('B', '\x12\x34\x56\x78')
    value, = struct.unpack('>I', data)
    vereq(value, 0x12345678)

# Test methods to pack and unpack from buffers rather than strings.
test_unpack_from()
test_pack_into()
test_pack_into_fn()
test_unpack_with_buffer()
