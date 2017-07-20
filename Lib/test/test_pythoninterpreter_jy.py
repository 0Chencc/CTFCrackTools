# -*- coding: utf-8 -*-
import java.io
import os
import sys
import traceback
import types
import unittest
import test.test_support
from org.python.core.util import StringUtil
from org.python.core import PyFile
from _codecs import encode
from sun.awt.image import BufImgVolatileSurfaceManager


def exec_code_in_pi(source, inp=None, out=None, err=None, locals=None):
    """Runs code in a separate context: (thread, PySystemState, PythonInterpreter)"""

    def execution_context():
        from org.python.core import Py
        from org.python.util import PythonInterpreter
        from org.python.core import PySystemState

        ps = PySystemState()
        pi = PythonInterpreter({}, ps)
        if locals is not None: pi.setLocals(locals)
        if inp is not None: pi.setIn(inp)
        if out is not None: pi.setOut(out)
        if err is not None: pi.setErr(err)
        try:
            if isinstance(source, types.FunctionType):
                # A function wrapping a compiled code block
                pi.exec(source.func_code)

            elif isinstance(source, java.io.InputStream):
                # A byte-oriented file-like input stream
                pi.execfile(source)

            elif isinstance(source, java.io.Reader):
                # A character-oriented file-like input stream
                code = pi.compile(source)
                pi.exec(code)

            else:
                # A str or unicode (see UnicodeSourceTest)
                pi.exec(source)

        except:
            print
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60


    import threading
    context = threading.Thread(target=execution_context)
    context.start()
    context.join()


class InterpreterTest(unittest.TestCase):

    # in these tests, note the promotion to unicode by java.io.Writer,
    # because these are character-oriented streams. caveat emptor!

    def test_pi_out_unicode(self):
        source_text = [
            u'Some text',
            'Plain text',
            u'\u1000\u2000\u3000\u4000',
            # Some language names from wikipedia
            u'Català · Česky · Dansk · Deutsch · English · Español · Esperanto · Français · Bahasa Indonesia · Italiano · Magyar · Nederlands · 日本語 · Norsk (bokmål) · Polski · Português · Русский · Română · Slovenčina · Suomi · Svenska · Türkçe · Українська · Volapük · 中文',
            ]

        def f():
            global text
            for x in text:
                print x
        out = java.io.StringWriter()
        err = java.io.StringWriter()
        exec_code_in_pi(f, None, out, err, {'text': source_text})
        output_text = out.toString().splitlines()
        for output, source in zip(output_text, source_text):
            self.assertEquals(output, source)

    def test_pi_out(self):
        def f():
            print 42
        out = java.io.StringWriter()
        err = java.io.StringWriter()
        exec_code_in_pi(f, None, out, err)
        self.assertEquals(u"42\n", out.toString())

    def test_more_output(self):
        def f():
            for i in xrange(42):
                print "*" * i
        out = java.io.StringWriter()
        err = java.io.StringWriter()
        exec_code_in_pi(f, None, out, err)
        output = out.toString().splitlines()
        for i, line in enumerate(output):
            self.assertEquals(line, u'*' * i)
        self.assertEquals(42, len(output))


class UnicodeSourceTest(unittest.TestCase):

    # When the core PythonInterpreter is embedded in a Java program
    # it may be supplied as Unicode source as a string or via streams.

    def do_test(self, source, ref_out=u'', ref_var=None, inp=None):
        if ref_var is None:
            ref_var = {}
        out = java.io.StringWriter()
        err = java.io.StringWriter()
        var = {}
        if inp is not None:
            if isinstance(inp, bytes):
                inp = java.io.ByteArrayInputStream(StringUtil.toBytes(inp))
            elif isinstance(inp, unicode):
                inp = java.io.StringReader(inp)

        exec_code_in_pi(source, inp, out, err, var)
        del var['__builtins__']
        self.assertEquals(ref_var, var)
        self.assertEquals(ref_out, out.toString())

    def test_ascii_str(self):
        # Program written in bytes with ascii range only
        self.do_test('a = 42\nprint a', u'42\n', {'a':42})

    def test_latin_str(self):
        # Program written in bytes with codes above 127
        self.do_test('a = "caf\xe9"\nprint a', u'caf\xe9\n', {'a':'caf\xe9'})

    def test_ascii_unicode(self):
        # Program written in Unicode with ascii range only
        self.do_test(u'a = "hello"\nprint a', u'hello\n', {'a':'hello'})

    def test_latin_unicode(self):
        # Program written in Unicode with codes above 127
       self.do_test(u'a = "caf\xe9"\nprint a', u'caf\xe9\n', {'a':'caf\xe9'})

    @unittest.skip("PythonInterpreter.exec(String) does not distinguish str/unicode")
    def test_bmp_unicode(self):
        # Program written in Unicode with codes above 255
        a = u"畫蛇添足 Λόγος"
        prog = u'a = u"{:s}"\nprint repr(a)'.format(a)
        # Submit via exec(unicode)
        self.do_test(prog,
                     u'{}\n'.format(repr(a)),
                     {'a': a})

    def test_bmp_utf8stream(self):
        # Program written in Unicode with codes above 255
        a = u"畫蛇添足 Λόγος"
        prog = u'a = u"{:s}"\nprint repr(a)'.format(a)
        # Program as bytes with declared encoding for execfile(InputStream)
        progbytes = '# coding: utf-8\n' + prog.encode('utf-8')
        stream = java.io.ByteArrayInputStream(StringUtil.toBytes(progbytes))
        self.do_test(stream,
                     u'{}\n'.format(repr(a)),
                     {'a': a})

    def test_bmp_reader(self):
        # Program written in Unicode with codes above 255
        a = u"畫蛇添足 Λόγος"
        prog = u'a = u"{:s}"\nprint repr(a)'.format(a)
        # Program as character stream for exec(compile(Reader))
        self.do_test(java.io.StringReader(prog),
                     u'{}\n'.format(repr(a)),
                     {'a': a})

def unicode_lines():
    input_lines = [
        u'Some text',
        u'un café crème',
        u"Λόγος",
        u"畫蛇添足",
        ]
    input_text = u'\n'.join(input_lines)
    return input_lines, input_text


class InterpreterSetInTest(unittest.TestCase):

    # When the core PythonInterpreter is embedded in a Java program it
    # may be connected through SetIn to a Unicode or byte stream.
    # However, the Unicode Reader interface narrows the data to bytes
    # in a way that mangles anything beyond Latin-1. These tests
    # illustrate that preparatory to a possible solution, in which the
    # encoding is specified to the PythonInterpreter and appears as
    # sys.stdin.encoding etc. for use by the application (and libraries).

    @staticmethod
    def do_read():
        import sys
        buf = bytearray()
        while True:
            c = sys.stdin.read(1)
            if not c: break
            buf.append(c)
        # A defined encoding ought to be advertised in sys.stdin.encoding
        enc = getattr(sys.stdin, 'encoding', None)
        # In the test, allow an override via local variables
        enc = locals().get('encoding', enc)
        if enc:
            result = buf.decode(enc) # unicode
        else:
            result = bytes(buf)

    def test_pi_bytes_read(self):
        # Test read() with pi.setIn(PyFile(InputStream))
        input_lines, input_text = unicode_lines()
        input_bytes = input_text.encode('utf-8')
        inp = java.io.ByteArrayInputStream(input_bytes)
        var = dict()
        exec_code_in_pi(InterpreterSetInTest.do_read, inp, locals=var)
        result = var['result']
        self.assertEquals(result, input_bytes)
        self.assertEquals(type(result), type(input_bytes))

    @unittest.skip("Jython treats characters from a Reader as bytes.")
    # Has no unicode encoding and fails to build PyString for codes > 255
    def test_pi_unicode_read(self):
        # Test read() with pi.setIn(Reader)
        input_lines, input_text = unicode_lines()
        inp = java.io.StringReader(input_text)
        var = dict()
        exec_code_in_pi(InterpreterSetInTest.do_read, inp, locals=var)
        result = var['result']
        self.assertEquals(result, input_text)
        self.assertEquals(type(result), type(input_text))

    def test_pi_encoding_read(self):
        # Test read() with pi.setIn(PyFile(InputStream)) and defined encoding
        input_lines, input_text = unicode_lines()
        input_bytes = input_text.encode('utf-8')
        inp = java.io.ByteArrayInputStream(input_bytes)
        var = {'encoding': 'utf-8'}
        exec_code_in_pi(InterpreterSetInTest.do_read, inp, locals=var)
        result = var['result']
        self.assertEquals(result, input_text)
        self.assertEquals(type(result), type(input_text))

    @staticmethod
    def do_readline():
        import sys
        # A defined encoding ought to be advertised in sys.stdin.encoding
        enc = getattr(sys.stdin, 'encoding', None)
        # In the test, allow an override via local variables
        enc = locals().get('encoding', enc)
        result = list()
        while True:
            line = sys.stdin.readline()
            if not line: break
            if enc: line = line.decode(enc) # unicode
            result.append(line.rstrip('\n'))

    def test_pi_bytes_readline(self):
        # Test readline() with pi.setIn(PyFile(InputStream))
        input_lines, input_text = unicode_lines()
        input_bytes = input_text.encode('utf-8')
        inp = java.io.ByteArrayInputStream(input_bytes)
        var = dict()
        exec_code_in_pi(InterpreterSetInTest.do_readline, inp, locals=var)
        for output, source in zip(var['result'], input_lines):
            source = source.encode('utf-8')
            self.assertEquals(output, source)
            self.assertEquals(type(output), type(source))

    @unittest.skip("Jython treats characters from a Reader as bytes.")
    # Has no unicode encoding and fails to build PyString for codes > 255
    def test_pi_unicode_readline(self):
        # Test readline() with pi.setIn(Reader)
        input_lines, input_text = unicode_lines()
        inp = java.io.StringReader(input_text)
        var = dict()
        exec_code_in_pi(InterpreterSetInTest.do_readline, inp, locals=var)
        for output, source in zip(var['result'], input_lines):
            self.assertEquals(output, source)
            self.assertEquals(type(output), type(source))

    def test_pi_encoding_readline(self):
        # Test readline() pi.setIn(PyFile(InputStream)) and defined encoding
        input_lines, input_text = unicode_lines()
        input_bytes = input_text.encode('utf-8')
        inp = java.io.ByteArrayInputStream(input_bytes)
        var = {'encoding': 'utf-8'}
        exec_code_in_pi(InterpreterSetInTest.do_readline, inp, locals=var)
        for output, source in zip(var['result'], input_lines):
            self.assertEquals(output, source)
            self.assertEquals(type(output), type(source))

    @staticmethod
    def do_readinto():
        import sys
        buf = bytearray(1024)
        n = sys.stdin.readinto(buf)
        result = buf[:n]

    def test_pi_bytes_readinto(self):
        # Test readinto() with pi.setIn(PyFile(InputStream))
        input_lines, input_text = unicode_lines()
        input_bytes = input_text.encode('utf-8')
        inp = java.io.ByteArrayInputStream(input_bytes)
        var = dict()
        exec_code_in_pi(InterpreterSetInTest.do_readinto, inp, locals=var)
        self.assertEquals(var['result'], input_bytes)

    # There is no readinto() with pi.setIn(Reader)


class StdoutWrapperTest(unittest.TestCase):

    def test_choose_str(self):

        def f():
            class Example:
                def __str__(self):
                    return "str"
                def __repr__(self):
                    return "repr"
            print Example()

        out = java.io.StringWriter()
        err = java.io.StringWriter()
        exec_code_in_pi(f, None, out, err)
        self.assertEqual(out.toString(), "str\n")


def test_main():
    test.test_support.run_unittest(
            InterpreterTest,
            UnicodeSourceTest,
            InterpreterSetInTest,
            StdoutWrapperTest
    )

if __name__ == "__main__":
    test_main()
