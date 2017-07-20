# XXX Earlier version of this test also tested put, get, eval on the
# engine, however this introduced action at a distance where aspects
# of the sys state changed (notably sys.stdin.newlines), which then
# impacted test_univnewlines later in the regrtest.
#
# For now, there may be limits in how much we can test Jython from
# itself, no matter how attractive from an ouroboros perspective that
# may be :). Certainly worth revisiting in 2.6.

import unittest
import sys
from test import test_support
from javax.script import ScriptEngine, ScriptEngineManager


class JSR223TestCase(unittest.TestCase):

    def test_factory(self):
        engine = ScriptEngineManager().getEngineByName("python")
        f = engine.factory
        language_version = ".".join(str(comp) for comp in sys.version_info[0:2]) # such as "2.5"
        impl_version =  ".".join(str(comp) for comp in sys.version_info[0:3]) # such as "2.5.2"

        self.assertNotEqual(f.scriptEngine, engine) # we don't pool engines

        self.assertEqual(f.engineName, "jython")
        self.assertEqual(f.engineVersion, impl_version)
        self.assertEqual(set(f.extensions), set(['py']))
        self.assertEqual(f.languageName, "python")
        self.assertEqual(f.languageVersion, language_version)
        self.assertEqual(set(f.names), set(["python", "jython"]))
        self.assertEqual(set(f.mimeTypes), set(["text/python", "application/python", "text/x-python", "application/x-python"]))

        # variants
        self.assertEqual(f.getParameter(ScriptEngine.ENGINE), "jython")
        self.assertEqual(f.getParameter(ScriptEngine.ENGINE_VERSION), impl_version)
        self.assertEqual(f.getParameter(ScriptEngine.NAME), "jython")
        self.assertEqual(f.getParameter(ScriptEngine.LANGUAGE), "python")
        self.assertEqual(f.getParameter(ScriptEngine.LANGUAGE_VERSION), language_version)

        self.assertEqual(f.getOutputStatement("abc"), "print u'abc'")
        self.assertEqual(f.getProgram("x = 42", "y = 'abc'"), "x = 42\ny = 'abc'\n")


def test_main():
    test_support.run_unittest(
        JSR223TestCase)


if __name__ == "__main__":
    test_main()
