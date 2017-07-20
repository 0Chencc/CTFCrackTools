import copy
import glob
import importlib
import operator
import os
import os.path
import unittest
import shutil
import subprocess
import sys
import tempfile
import re

from collections import deque
from test import test_support

from java.lang import (ClassCastException, ExceptionInInitializerError, String, Runnable, System,
        Runtime, Math, Byte)
from java.math import BigDecimal, BigInteger
from java.net import URI
from java.io import (ByteArrayInputStream, ByteArrayOutputStream, File, FileInputStream,
                     FileNotFoundException, FileOutputStream, FileWriter, ObjectInputStream,
                     ObjectOutputStream, OutputStreamWriter, UnsupportedEncodingException)
from java.util import ArrayList, Date, HashMap, Hashtable, StringTokenizer, Vector
from java.util.concurrent import Executors

from java.awt import Dimension, Color, Component, Container
from java.awt.event import ComponentEvent
from javax.swing.tree import TreePath
from javax.tools import SimpleJavaFileObject, JavaFileObject, ToolProvider

from org.python.core.util import FileUtil
from org.python.compiler import CustomMaker
from org.python.tests import (BeanImplementation, Child, Child2,
                              CustomizableMapHolder, Listenable, ToUnicode)
from org.python.tests.mro import (ConfusedOnGetitemAdd, FirstPredefinedGetitem, GetitemAdder)
from org.python.util import PythonInterpreter

import java
import org.python.core.Options

from javatests import Issue1833
from javatests.ProxyTests import NullToString, Person

from clamp import SerializableProxies



class InstantiationTest(unittest.TestCase):
    def test_cant_instantiate_abstract(self):
        self.assertRaises(TypeError, Component)

    def test_no_public_constructors(self):
        self.assertRaises(TypeError, Math)

    def test_invalid_self_to_java_constructor(self):
        self.assertRaises(TypeError, Color.__init__, 10, 10, 10)

    def test_str_doesnt_coerce_to_int(self):
        self.assertRaises(TypeError, Date, '99-01-01', 1, 1)

    def test_class_in_failed_constructor(self):
        try:
            Dimension(123, 456, 789)
        except TypeError, exc:
            self.failUnless("java.awt.Dimension" in exc.message)


class BeanTest(unittest.TestCase):
    def test_shared_names(self):
        self.failUnless(callable(Vector.size),
                'size method should be preferred to writeonly field')

    def test_multiple_listeners(self):
        '''Check that multiple BEP can be assigned to a single cast listener'''
        m = Listenable()
        called = []
        def f(evt, called=called):
            called.append(0)

        m.componentShown = f
        m.componentHidden = f

        m.fireComponentShown(ComponentEvent(Container(), 0))
        self.assertEquals(1, len(called))
        m.fireComponentHidden(ComponentEvent(Container(), 0))
        self.assertEquals(2, len(called))

    def test_bean_interface(self):
        b = BeanImplementation()
        self.assertEquals("name", b.getName())
        self.assertEquals("name", b.name)
        # Tests for #610576
        class SubBean(BeanImplementation):
            def __init__(bself):
                self.assertEquals("name", bself.getName())
        SubBean()

    def test_inheriting_half_bean(self):
        c = Child()
        self.assertEquals("blah", c.value)
        c.value = "bleh"
        self.assertEquals("bleh", c.value)
        self.assertEquals(7, c.id)
        c.id = 16
        self.assertEquals(16, c.id)

    def test_inheriting_half_bean_issue1333(self):
        # http://bugs.jython.org/issue1333
        c = Child2()
        self.assertEquals("blah", c.value)
        c.value = "bleh"
        self.assertEquals("Child2 bleh", c.value)

    def test_awt_hack(self):
        # We ignore several deprecated methods in java.awt.* in favor of bean properties that were
        # addded in Java 1.1.  This tests that one of those bean properties is visible.
        c = Container()
        c.size = 400, 300
        self.assertEquals(Dimension(400, 300), c.size)

class SysIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.orig_stdout = sys.stdout

    def tearDown(self):
        sys.stdout = self.orig_stdout

    def test_stdout_outputstream(self):
        out = FileOutputStream(test_support.TESTFN)
        sys.stdout = out
        print 'hello',
        out.close()
        f = open(test_support.TESTFN)
        self.assertEquals('hello', f.read())
        f.close()

class IOTest(unittest.TestCase):

    def test_io_errors(self):
        "Check that IOException isn't mangled into an IOError"
        self.assertRaises(UnsupportedEncodingException, OutputStreamWriter, System.out, "garbage")

    def test_fileio_error(self):
        self.assertRaises(FileNotFoundException, FileInputStream, "garbage")

    def fileutil_is_helper(self, mode, expected):
        old_linesep = System.setProperty("line.separator", "\r\n")
        try:
            inputstream = ByteArrayInputStream(bytearray('1\r\n2\r\n3\r\n'))
            inputfile = FileUtil.wrap(inputstream, mode)
            actual = inputfile.readlines()
            inputfile.close()
            self.assertEquals(expected, actual)
        finally:
            System.setProperty("line.separator", old_linesep)

    def test_fileutil_wrap_inputstream(self):
        self.fileutil_is_helper('r', ['1\n', '2\n', '3\n'])

    def test_fileutil_wrap_inputstream_binary(self):
        self.fileutil_is_helper('rb', ['1\r\n', '2\r\n', '3\r\n'])

    def fileutil_os_helper(self, mode, expected):
        old_linesep = System.setProperty("line.separator", "\r\n")
        try:
            outputstream = ByteArrayOutputStream()
            outputfile = FileUtil.wrap(outputstream, mode)
            outputfile.writelines(["1\n", "2\n", "3\n"])
            outputfile.close()
            self.assertEquals(bytearray(outputstream.toByteArray()), expected)
        finally:
            System.setProperty("line.separator", old_linesep)

    def test_fileutil_wrap_outputstream_default_textmode(self):
        self.fileutil_os_helper("w", bytearray("1\r\n2\r\n3\r\n"))

    def test_fileutil_wrap_outputstream_binary(self):
        self.fileutil_os_helper("wb", bytearray("1\n2\n3\n"))

    def test_unsupported_tell(self):
        fp = FileUtil.wrap(System.out)
        self.assertRaises(IOError, fp.tell)


class JavaReservedNamesTest(unittest.TestCase):
    "Access to reserved words"

    def test_system_in(self):
        s = System.in
        self.assert_("method" in str(s.read))

    def test_runtime_exec(self):
        e = Runtime.getRuntime().exec
        self.assert_(re.search("method .*exec", str(e)) is not None)

    def test_byte_class(self):
        b = Byte(10)
        self.assert_("java.lang.Byte" in str(b.class))

class Keywords(object):
    pass

Keywords.in = lambda self: "in"
Keywords.exec = lambda self: "exec"
Keywords.class = lambda self: "class"
Keywords.print = lambda self: "print"
Keywords.and = lambda self: "and"
Keywords.as = lambda self: "as"
Keywords.assert = lambda self: "assert"
Keywords.break = lambda self: "break"
Keywords.continue = lambda self: "continue"
Keywords.def = lambda self: "def"
Keywords.del = lambda self: "del"
Keywords.elif = lambda self: "elif"
Keywords.else = lambda self: "else"
Keywords.except = lambda self: "except"
Keywords.finally = lambda self: "finally"
Keywords.from = lambda self: "from"
Keywords.for = lambda self: "for"
Keywords.global = lambda self: "global"
Keywords.if = lambda self: "if"
Keywords.import = lambda self: "import"
Keywords.is = lambda self: "is"
Keywords.lambda = lambda self: "lambda"
Keywords.pass = lambda self: "pass"
Keywords.print = lambda self: "print"
Keywords.raise = lambda self: "raise"
Keywords.return = lambda self: "return"
Keywords.try = lambda self: "try"
Keywords.while = lambda self: "while"
Keywords.with = lambda self: "with"
Keywords.yield = lambda self: "yield"

class PyReservedNamesTest(unittest.TestCase):
    "Access to reserved words"

    def setUp(self):
        self.kws = Keywords()

    def test_in(self):
        self.assertEquals(self.kws.in(), "in")

    def test_exec(self):
        self.assertEquals(self.kws.exec(), "exec")

    def test_class(self):
        self.assertEquals(self.kws.class(), "class")

    def test_print(self):
        self.assertEquals(self.kws.print(), "print")

    def test_and(self):
        self.assertEquals(self.kws.and(), "and")

    def test_as(self):
        self.assertEquals(self.kws.as(), "as")

    def test_assert(self):
        self.assertEquals(self.kws.assert(), "assert")

    def test_break(self):
        self.assertEquals(self.kws.break(), "break")

    def test_continue(self):
        self.assertEquals(self.kws.continue(), "continue")

    def test_def(self):
        self.assertEquals(self.kws.def(), "def")

    def test_del(self):
        self.assertEquals(self.kws.del(), "del")

    def test_elif(self):
        self.assertEquals(self.kws.elif(), "elif")

    def test_else(self):
        self.assertEquals(self.kws.else(), "else")

    def test_except(self):
        self.assertEquals(self.kws.except(), "except")

    def test_finally(self):
        self.assertEquals(self.kws.finally(), "finally")

    def test_from(self):
        self.assertEquals(self.kws.from(), "from")

    def test_for(self):
        self.assertEquals(self.kws.for(), "for")

    def test_global(self):
        self.assertEquals(self.kws.global(), "global")

    def test_if(self):
        self.assertEquals(self.kws.if(), "if")

    def test_import(self):
        self.assertEquals(self.kws.import(), "import")

    def test_is(self):
        self.assertEquals(self.kws.is(), "is")

    def test_lambda(self):
        self.assertEquals(self.kws.lambda(), "lambda")

    def test_pass(self):
        self.assertEquals(self.kws.pass(), "pass")

    def test_print(self):
        self.assertEquals(self.kws.print(), "print")

    def test_raise(self):
        self.assertEquals(self.kws.raise(), "raise")

    def test_return(self):
        self.assertEquals(self.kws.return(), "return")

    def test_try(self):
        self.assertEquals(self.kws.try(), "try")

    def test_while(self):
        self.assertEquals(self.kws.while(), "while")

    def test_with(self):
        self.assertEquals(self.kws.with(), "with")

    def test_yield(self):
        self.assertEquals(self.kws.yield(), "yield")

class ImportTest(unittest.TestCase):
    def test_bad_input_exception(self):
        self.assertRaises(ValueError, __import__, '')

    def test_broken_static_initializer(self):
        self.assertRaises(ExceptionInInitializerError, __import__, "org.python.tests.BadStaticInitializer")

class ColorTest(unittest.TestCase):
    def test_assigning_over_method(self):
        self.assertRaises(TypeError, setattr, Color.RED, "getRGB", 4)

    def test_static_fields(self):
        self.assertEquals(Color(255, 0, 0), Color.RED)
        # The bean accessor for getRed should be active on instances, but the static field red
        # should be visible on the class
        self.assertEquals(255, Color.red.red)
        self.assertEquals(Color(0, 0, 255), Color.blue)

    def test_is_operator(self):
        red = Color.red
        self.assert_(red is red)
        self.assert_(red is Color.red)

class TreePathTest(unittest.TestCase):
    def test_overloading(self):
        treePath = TreePath([1,2,3])
        self.assertEquals(len(treePath.path), 3, "Object[] not passed correctly")
        self.assertEquals(TreePath(treePath.path).path, treePath.path, "Object[] not passed and returned correctly")

class BigNumberTest(unittest.TestCase):
    def test_coerced_bigdecimal(self):
        from javatests import BigDecimalTest
        x = BigDecimal("123.4321")
        y = BigDecimalTest().asBigDecimal()

        self.assertEqual(type(x), type(y), "BigDecimal coerced")
        self.assertEqual(x, y, "coerced BigDecimal not equal to directly created version")

    def test_biginteger_in_long(self):
        '''Checks for #608628, that long can take a BigInteger in its constructor'''
        ns = '10000000000'
        self.assertEquals(ns, str(long(BigInteger(ns))))

class JavaStringTest(unittest.TestCase):
    def test_string_not_iterable(self):
        x = String('test')
        self.assertRaises(TypeError, list, x)

class JavaDelegationTest(unittest.TestCase):
    def test_list_delegation(self):
        for c in ArrayList, Vector:
            a = c()
            self.assertRaises(IndexError, a.__getitem__, 0)
            a.add("blah")
            self.assertTrue("blah" in a)
            self.assertEquals(1, len(a))
            n = 0
            for i in a:
                n += 1
                self.assertEquals("blah", i)
            self.assertEquals(1, n)
            self.assertEquals("blah", a[0])
            a[0] = "bleh"
            del a[0]
            self.assertEquals(0, len(a))

    def test_map_delegation(self):
        m = HashMap()
        m["a"] = "b"
        self.assertTrue("a" in m)
        self.assertEquals("b", m["a"])
        n = 0
        for k in m:
            n += 1
            self.assertEquals("a", k)
        self.assertEquals(1, n)
        del m["a"]
        self.assertEquals(0, len(m))

    def test_enumerable_delegation(self):
        tokenizer = StringTokenizer('foo bar')
        self.assertEquals(list(iter(tokenizer)), ['foo', 'bar'])

    def test_vector_delegation(self):
        class X(Runnable):
            pass
        v = Vector()
        v.addElement(1)
        v.indexOf(X())# Compares the Java object in the vector to a Python subclass
        for i in v:
            pass

    def test_comparable_delegation(self):
        first_file = File("a")
        first_date = Date(100)
        for a, b, c in [(first_file, File("b"), File("c")), (first_date, Date(1000), Date())]:
            self.assertTrue(a.compareTo(b) < 0)
            self.assertEquals(-1, cmp(a, b))
            self.assertTrue(a.compareTo(c) < 0)
            self.assertEquals(-1, cmp(a, c))
            self.assertEquals(0, a.compareTo(a))
            self.assertEquals(0, cmp(a, a))
            self.assertTrue(b.compareTo(a) > 0)
            self.assertEquals(1, cmp(b, a))
            self.assertTrue(c.compareTo(b) > 0)
            self.assertEquals(1, cmp(c, b))
            self.assertTrue(a < b)
            self.assertTrue(a <= a)
            self.assertTrue(b > a)
            self.assertTrue(c >= a)
            self.assertTrue(a != b)
            l = [b, c, a]
            self.assertEquals(a, min(l))
            self.assertEquals(c, max(l))
            l.sort()
            self.assertEquals([a, b, c], l)
        # Check that we fall back to the default comparison(class name) instead of using compareTo
        # on non-Comparable types
        self.assertRaises(ClassCastException, first_file.compareTo, first_date)
        self.assertEquals(-1, cmp(first_file, first_date))
        self.assertTrue(first_file < first_date)
        self.assertTrue(first_file <= first_date)
        self.assertTrue(first_date > first_file)
        self.assertTrue(first_date >= first_file)

    def test_equals(self):
        # Test for bug #1338
        a = range(5)

        x = ArrayList()
        x.addAll(a)

        y = Vector()
        y.addAll(a)

        z = ArrayList()
        z.addAll(range(1, 6))

        self.assertTrue(x.equals(y))
        self.assertEquals(x, y)
        self.assertTrue(not (x != y))

        self.assertTrue(not x.equals(z))
        self.assertNotEquals(x, z)
        self.assertTrue(not (x == z))

class SecurityManagerTest(unittest.TestCase):

    def test_nonexistent_import_with_security(self):
        script = test_support.findfile("import_nonexistent.py")
        home = os.path.realpath(sys.prefix)
        if not os.path.commonprefix((home, os.path.realpath(script))) == home:
            # script must lie within python.home for this test to work
            return
        policy = test_support.findfile("python_home.policy")
        self.assertEquals(subprocess.call([sys.executable,  "-J-Dpython.cachedir.skip=true",
            "-J-Djava.security.manager", "-J-Djava.security.policy=%s" % policy, script]),
            0)

    def test_import_signal_fails_with_import_error_using_security(self):
        policy = test_support.findfile("python_home.policy")
        with self.assertRaises(subprocess.CalledProcessError) as cm:
            subprocess.check_output(
                [sys.executable,
                 "-J-Dpython.cachedir.skip=true",
                 "-J-Djava.security.manager",
                 "-J-Djava.security.policy=%s" % policy,
                 "-c", "import signal"],
                stderr=subprocess.STDOUT)
        self.assertIn(
            'ImportError: signal module requires sun.misc.Signal, which is not allowed by your security profile',
            cm.exception.output)


class JavaWrapperCustomizationTest(unittest.TestCase):
    def tearDown(self):
        CustomizableMapHolder.clearAdditions()

    def test_adding_item_access(self):
        m = CustomizableMapHolder()
        self.assertRaises(TypeError, operator.getitem, m, "initial")
        CustomizableMapHolder.addGetitem()
        self.assertEquals(m.held["initial"], m["initial"])
        # dict would throw a KeyError here, but Map returns null for a missing key
        self.assertEquals(None, m["nonexistent"])
        self.assertRaises(TypeError, operator.setitem, m, "initial")
        CustomizableMapHolder.addSetitem()
        m["initial"] = 12
        self.assertEquals(12, m["initial"])

    def test_adding_attributes(self):
        m = CustomizableMapHolder()
        self.assertRaises(AttributeError, getattr, m, "initial")
        CustomizableMapHolder.addGetattribute()
        self.assertEquals(7, m.held["initial"], "Existing fields should still be accessible")
        self.assertEquals(7, m.initial)
        self.assertEquals(None, m.nonexistent, "Nonexistent fields should be passed on to the Map")

    def test_adding_on_interface(self):
        GetitemAdder.addPredefined()
        class UsesInterfaceMethod(FirstPredefinedGetitem):
            pass
        self.assertEquals("key", UsesInterfaceMethod()["key"])

    def test_add_on_mro_conflict(self):
        """Adding same-named methods to Java classes with MRO conflicts produces TypeError"""
        GetitemAdder.addPredefined()
        self.assertRaises(TypeError, __import__, "org.python.tests.mro.ConfusedOnImport")
        self.assertRaises(TypeError, GetitemAdder.addPostdefined)

    def test_null_tostring(self):
        # http://bugs.jython.org/issue1819
        nts = NullToString()
        self.assertEqual(repr(nts), '')
        self.assertEqual(str(nts), '')
        self.assertEqual(unicode(nts), '')

    def test_diamond_inheritance_of_iterable_and_map(self):
        """Test deeply nested diamond inheritance of Iterable and Map, as see in some Clojure classes"""
        # http://bugs.jython.org/issue1878
        from javatests import DiamondIterableMapMRO  # this will raise a TypeError re MRO conflict without the fix
        # Verify the correct MRO is generated - order is of course *important*;
        # the following used types are implemented as empty interfaces/abstract classes, but match the inheritance graph
        # and naming of Clojure/Storm.
        #
        # Also instead of directly importing, which would cause annoying bloat in javatests by making lots of little files,
        # just match using str - this will still be stable/robust.
        self.assertEqual(
            str(DiamondIterableMapMRO.__mro__),
            "(<type 'javatests.DiamondIterableMapMRO'>, <type 'javatests.ILookup'>, <type 'javatests.IPersistentMap'>, <type 'java.lang.Iterable'>, <type 'javatests.Associative'>, <type 'javatests.IPersistentCollection'>, <type 'javatests.Seqable'>, <type 'javatests.Counted'>, <type 'java.util.Map'>, <type 'javatests.AFn'>, <type 'javatests.IFn'>, <type 'java.util.concurrent.Callable'>, <type 'java.lang.Runnable'>, <type 'java.lang.Object'>, <type 'object'>)")
        # And usable with __iter__ and map functionality
        m = DiamondIterableMapMRO()
        m["abc"] = 42
        m["xyz"] = 47
        self.assertEqual(set(m), set(["abc", "xyz"]))
        self.assertEqual(m["abc"], 42)

def roundtrip_serialization(obj):
    """Returns a deep copy of an object, via serializing it
 
    see http://weblogs.java.net/blog/emcmanus/archive/2007/04/cloning_java_ob.html
    """
    output = ByteArrayOutputStream()
    serializer = CloneOutput(output)
    serializer.writeObject(obj)
    serializer.close()
    input = ByteArrayInputStream(output.toByteArray())
    unserializer = CloneInput(input, serializer) # to get the list of classes seen, in order
    return unserializer.readObject()

class CloneOutput(ObjectOutputStream):
    def __init__(self, output):
        ObjectOutputStream.__init__(self, output)
        self.classQueue = deque()

    def annotateClass(self, c):
        self.classQueue.append(c)

    def annotateProxyClass(self, c):
        self.classQueue.append(c)

class CloneInput(ObjectInputStream):

    def __init__(self, input, output):
        ObjectInputStream.__init__(self, input)
        self.output = output

    def resolveClass(self, obj_stream_class):
        return self.output.classQueue.popleft()

    def resolveProxyClass(self, interfaceNames):
        return self.output.classQueue.popleft()


def find_jython_jars():
    # Uses the same classpath resolution as bin/jython
    jython_jar_path = os.path.normpath(os.path.join(sys.executable, "../../jython.jar"))
    jython_jar_dev_path = os.path.normpath(os.path.join(sys.executable, "../../jython-dev.jar"))
    if os.path.exists(jython_jar_dev_path):
        jars = [jython_jar_dev_path]
        jars.extend(glob.glob(os.path.normpath(os.path.join(jython_jar_dev_path, "../javalib/*.jar"))))
    elif os.path.exists(jython_jar_path):
        jars = [jython_jar_path]
    else:
        raise Exception("Cannot find jython jar")
    return jars




class JavaSource(SimpleJavaFileObject):

    def __init__(self, name, source):
        self._name = name
        self._source = source
        SimpleJavaFileObject.__init__(
            self, 
            URI.create("string:///" + name.replace(".", "/") + JavaFileObject.Kind.SOURCE.extension),
            JavaFileObject.Kind.SOURCE)

    def getName(self):
        return self._name

    def getCharContent(self, ignore):
        return self._source


def compile_java_source(options, class_name, source):
    """Compiles a single java source "file" contained in the string source
    
    Use options, specifically -d DESTDIR, to control where the class
    file is emitted. Note that we could use forwarding managers to
    avoid tempdirs, but this is overkill here given that we still need
    to run the emitted Java class.
    """
    f = JavaSource(class_name, source)
    compiler = ToolProvider.getSystemJavaCompiler()
    task = compiler.getTask(None, None, None, options, None, [f])
    task.call()


class SerializationTest(unittest.TestCase):

    def test_java_serialization(self):
        date_list = [Date(), Date()]
        self.assertEqual(date_list, roundtrip_serialization(date_list))

    def test_java_serialization_pycode(self):

        def universal_answer():
            return 42

        serialized_code = roundtrip_serialization(universal_answer.func_code)
        self.assertEqual(eval(serialized_code), universal_answer())

    def test_builtin_names(self):
        import __builtin__
        names = [x for x in dir(__builtin__)]
        self.assertEqual(names, roundtrip_serialization(names))

    def test_proxy_serialization(self):
        """Proxies can be deserializable in a fresh JVM, including being able to "findPython" to get a PySystemState"""
        tempdir = tempfile.mkdtemp()
        old_proxy_debug_dir = org.python.core.Options.proxyDebugDirectory
        try:
            # Generate a proxy for Cat class;
            org.python.core.Options.proxyDebugDirectory = tempdir
            from pounce import Cat
            cat = Cat()
            self.assertEqual(cat.whoami(), "Socks")

            # Create a jar file containing the Cat proxy; could use Java to do this; do it the easy way for now
            proxies_jar_path = os.path.join(tempdir, "proxies.jar")
            subprocess.check_call(["jar", "cf", proxies_jar_path, "-C", tempdir, "org/"])

            # Serialize our cat
            output = ByteArrayOutputStream()
            serializer = CloneOutput(output)
            serializer.writeObject(cat)
            serializer.close()
            cat_path = os.path.join(tempdir, "serialized-cat")
            with open(cat_path, "wb") as f:
                f.write(output.toByteArray())

            # Then in a completely different JVM running
            # ProxyDeserialization, verify we get "meow" printed to
            # stdout, which in turn ensures that PySystemState (and
            # Jython runtime) is initialized for the proxy
            jars = find_jython_jars()
            jars.append(proxies_jar_path)
            classpath = os.pathsep.join(jars)
            env = dict(os.environ)
            env.update(JYTHONPATH=os.path.normpath(os.path.join(__file__, "..")))
            cmd = [os.path.join(System.getProperty("java.home"), "bin/java"),
                   "-classpath", classpath, "ProxyDeserialization", cat_path]
            self.assertEqual(subprocess.check_output(cmd, env=env, universal_newlines=True),
                             "meow\n")
        finally:
            org.python.core.Options.proxyDebugDirectory = old_proxy_debug_dir
            shutil.rmtree(tempdir)

    def test_custom_proxymaker(self):
        """Verify custom proxymaker supports direct usage of Python code in Java"""
        tempdir = tempfile.mkdtemp()
        try:
            SerializableProxies.serialized_path = tempdir
            import bark
            dog = bark.Dog()
            self.assertEqual(dog.whoami(), "Rover")
            self.assertEqual(dog.serialVersionUID, 1)
            self.assertEqual(dog, roundtrip_serialization(dog))

            # Create a jar file containing the org.python.test.Dog proxy
            proxies_jar_path = os.path.join(tempdir, "proxies.jar")
            subprocess.check_call(["jar", "cf", proxies_jar_path, "-C", tempdir, "org/"])

            # Build a Java class importing Dog
            source = """
import org.python.test.bark.Dog;  // yes, it's that simple

public class BarkTheDog {
    public static void main(String[] args) {
        Dog dog = new Dog();
        try {
            Boolean b = (Boolean)(dog.call());
            if (!b) {
                throw new RuntimeException("Expected site module to be imported");
            }
        }
        catch(Exception e) {
            System.err.println(e);
        }
    }
}
"""
            jars = find_jython_jars()
            jars.append(proxies_jar_path)
            classpath = os.pathsep.join(jars)
            compile_java_source(
                ["-classpath", classpath, "-d", tempdir],
                "BarkTheDog", source)

            # Then in a completely different JVM running our
            # BarkTheDog code, verify we get an appropriate bark
            # message printed to stdout, which in turn ensures that
            # PySystemState (and Jython runtime) is initialized for
            # the proxy
            classpath += os.pathsep + tempdir
            cmd = [os.path.join(System.getProperty("java.home"), "bin/java"),
                   "-classpath", classpath, "BarkTheDog"]
            env = dict(os.environ)
            env.update(JYTHONPATH=os.path.normpath(os.path.join(__file__, "..")))
            self.assertRegexpMatches(
                subprocess.check_output(cmd, env=env, universal_newlines=True,
                                        stderr=subprocess.STDOUT),
                r"^Class defined on CLASSPATH <type 'org.python.test.bark.Dog'>\n"
                                        "Rover barks 42 times$")
        finally:
            pass
            # print "Will not remove", tempdir
            #shutil.rmtree(tempdir)


class CopyTest(unittest.TestCase):

    def test_copy(self):
        fruits = ArrayList(["apple", "banana"])
        fruits_copy = copy.copy(fruits)
        self.assertEqual(fruits, fruits_copy)
        self.assertNotEqual(id(fruits), id(fruits_copy))

    def test_deepcopy(self):
        items = ArrayList([ArrayList(["apple", "banana"]),
                           ArrayList(["trs80", "vic20"])])
        items_copy = copy.deepcopy(items)
        self.assertEqual(items, items_copy)
        self.assertNotEqual(id(items), id(items_copy))
        self.assertNotEqual(id(items[0]), id(items_copy[0]))
        self.assertNotEqual(id(items[1]), id(items_copy[1]))

    def test_copy_when_not_cloneable(self):
        bdfl = Person("Guido", "von Rossum")
        self.assertRaises(TypeError, copy.copy, bdfl)

        # monkeypatching in a __copy__ should now work
        Person.__copy__ = lambda p: Person(p.firstName, p.lastName)
        copy_bdfl = copy.copy(bdfl)
        self.assertEqual(str(bdfl), str(copy_bdfl))

    def test_copy_when_not_serializable(self):
        bdfl = Person("Guido", "von Rossum")
        self.assertRaises(TypeError, copy.deepcopy, bdfl)

        # monkeypatching in a __deepcopy__ should now work
        Person.__deepcopy__ = lambda p, memo: Person(p.firstName, p.lastName)
        copy_bdfl = copy.deepcopy(bdfl)
        self.assertEqual(str(bdfl), str(copy_bdfl))

    def test_immutable(self):
        abc = String("abc")
        abc_copy = copy.copy(abc)
        self.assertEqual(id(abc), id(abc_copy))
        
        fruits = ArrayList([String("apple"), String("banana")])
        fruits_copy = copy.copy(fruits)
        self.assertEqual(fruits, fruits_copy)
        self.assertNotEqual(id(fruits), id(fruits_copy))


class UnicodeTest(unittest.TestCase):

    def test_unicode_conversion(self):
        test = unicode(ToUnicode())
        self.assertEqual(type(test), unicode)
        self.assertEqual(test, u"Circle is 360\u00B0")


class BeanPropertyTest(unittest.TestCase):

    def test_issue1833(self):
        class TargetClass(object):
            def _getattribute(self):
                return self.__attribute
            def _setattribute(self, value):
                self.__attribute = value
            attribute = property(_getattribute, _setattribute)

        target = TargetClass()
        test = Issue1833(target=target)
        value = ('bleh', 'blah')
        test.value = value
        self.assertEqual(target.attribute, value)


class WrappedUp(object):
    def __init__(self):
        self.data = list()
    def doit(self):
        self.data.append(42)


class CallableObject(object):
    def __init__(self):
        self.data = list()
    def __call__(self):
        self.data.append(42)


class SingleMethodInterfaceTest(unittest.TestCase):

    def setUp(self):
        self.executor = Executors.newSingleThreadExecutor()

    def tearDown(self):
        self.executor.shutdown()

    def test_function(self):
        x = list()
        def f():
            x.append(42)
        future = self.executor.submit(f)
        future.get()
        self.assertEqual(x, [42])

    @unittest.skip("FIXME: not working")
    def test_callable_object(self):
        callable_obj = CallableObject()
        future = self.executor.submit(callable_obj)
        future.get()
        self.assertEqual(callable_obj.data, [42])

    def test_bound_method(self):
        obj = WrappedUp()
        future = self.executor.submit(obj.doit)
        future.get()
        self.assertEqual(obj.data, [42])

    def test_unbound_method(self):
        with self.assertRaises(TypeError) as exc:
            future = self.executor.submit(WrappedUp.doit)  # not a bound method
        self.assertIsInstance(
            exc.exception, TypeError,
            "submit(): 1st arg can't be coerced to java.util.concurrent.Callable, java.lang.Runnable")

    def test_some_noncallable_object(self):
        obj = WrappedUp()
        with self.assertRaises(TypeError) as exc:
            future = self.executor.submit(obj)
        self.assertIsInstance(
            exc.exception, TypeError,
            "submit(): 1st arg can't be coerced to java.util.concurrent.Callable, java.lang.Runnable")


def test_main():
    test_support.run_unittest(
        BeanPropertyTest,
        BeanTest,
        BigNumberTest,
        ColorTest,
        CopyTest,
        IOTest,
        ImportTest,
        InstantiationTest,
        JavaDelegationTest,
        JavaReservedNamesTest,
        JavaStringTest,
        JavaWrapperCustomizationTest,
        PyReservedNamesTest,
        SecurityManagerTest,
        SerializationTest,
        SysIntegrationTest,
        TreePathTest,
        UnicodeTest,
        SingleMethodInterfaceTest)

if __name__ == "__main__":
    test_main()
