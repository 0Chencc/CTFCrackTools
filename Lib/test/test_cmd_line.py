import os
import test.test_support, unittest
import sys
import popen2
import subprocess

class CmdLineTest(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        if test.test_support.is_jython:
            # GC is not immediate, so if Popen.__del__ may be delayed.
            # Try to force any Popen.__del__ errors within scope of test.
            from test_weakref import extra_collect
            extra_collect()

    def start_python(self, cmd_line):
        outfp, infp = popen2.popen4('"%s" %s' % (sys.executable, cmd_line))
        infp.close()
        data = outfp.read()
        outfp.close()
        # try to cleanup the child so we don't appear to leak when running
        # with regrtest -R.  This should be a no-op on Windows.
        popen2._cleanup()
        return data

    def exit_code(self, *args):
        cmd_line = [sys.executable]
        cmd_line.extend(args)
        devnull = open(os.devnull, 'w')
        result = subprocess.call(cmd_line, stdout=devnull,
                                 stderr=subprocess.STDOUT)
        devnull.close()
        return result

    def test_directories(self):
        self.assertNotEqual(self.exit_code('.'), 0)
        self.assertNotEqual(self.exit_code('< .'), 0)

    def verify_valid_flag(self, cmd_line):
        data = self.start_python(cmd_line)
        self.assertTrue(data == '' or data.endswith('\n'))
        self.assertTrue('Traceback' not in data)

    def test_environment(self):
        self.verify_valid_flag('-E')

    def test_optimize(self):
        self.verify_valid_flag('-O')
        self.verify_valid_flag('-OO')

    def test_q(self):
        self.verify_valid_flag('-Qold')
        self.verify_valid_flag('-Qnew')
        self.verify_valid_flag('-Qwarn')
        self.verify_valid_flag('-Qwarnall')

    def test_site_flag(self):
        self.verify_valid_flag('-S')

    def test_usage(self):
        self.assertTrue('usage' in self.start_python('-h'))

    def test_version(self):
        prefix = 'J' if test.test_support.is_jython else 'P'
        version = prefix + 'ython %d.%d' % sys.version_info[:2]
        start = self.start_python('-V')
        self.assertTrue(start.startswith(version),
            "%s does not start with %s" % (start, version))

    def test_run_module(self):
        # Test expected operation of the '-m' switch
        # Switch needs an argument
        self.assertNotEqual(self.exit_code('-m'), 0)
        # Check we get an error for a nonexistent module
        self.assertNotEqual(
            self.exit_code('-m', 'fnord43520xyz'),
            0)
        # Check the runpy module also gives an error for
        # a nonexistent module
        self.assertNotEqual(
            self.exit_code('-m', 'runpy', 'fnord43520xyz'),
            0)
        # All good if module is located and run successfully
        self.assertEqual(
            self.exit_code('-m', 'timeit', '-n', '1'),
            0)

    def test_run_code(self):
        # Test expected operation of the '-c' switch
        # Switch needs an argument
        self.assertNotEqual(self.exit_code('-c'), 0)
        # Check we get an error for an uncaught exception
        self.assertNotEqual(
            self.exit_code('-c', 'raise Exception'),
            0)
        # All good if execution is successful
        self.assertEqual(
            self.exit_code('-c', 'pass'),
            0)


def test_main():
    test.test_support.run_unittest(CmdLineTest)
    test.test_support.reap_children()

if __name__ == "__main__":
    test_main()
