"""Misc subprocess tests"""
import unittest
import os
import sys
import signal
import time
import errno
from test import test_support
from subprocess import PIPE, Popen, _cmdline2list


class TerminationAndSignalTest(unittest.TestCase):

    def setUp(self):
        program = '''
import signal, sys

def print_signal(signum, frame):
    print signum

def exit_signal(signum, frame):
    sys.exit(signum)

signal.signal(signal.SIGTERM, print_signal)
signal.signal(signal.SIGINT, exit_signal)

print 'Started'
sys.stdout.flush()

while True:
    pass
'''
        self.proc = Popen(['python', '-c', program], stdout=PIPE, stderr=PIPE)
        assert self.proc.stdout.readline().strip() == 'Started'

    def tearDown(self):
        if self.proc.poll() is None:
            self.proc.kill()

    def test_kill(self):
        self.proc.kill()
        self.assertNotEqual(self.proc.wait(), 0)

    if os._name != 'nt':

        def test_terminate_can_be_ignored_on_posix(self):
            self.proc.terminate()
            self.assertIsNone(self.proc.poll())

        def test_send_signals_on_posix(self):
            self.proc.send_signal(signal.SIGTERM)
            time.sleep(0.01)  # Make sure SIGTERM is handled first
            self.proc.send_signal(signal.SIGINT)
            self.assertEqual(self.proc.wait(), 2)
            self.assertEqual(self.proc.stdout.read(), '15\n')

    else:

        def test_terminate_cannot_be_ignored_on_windows(self):
            self.proc.terminate()
            self.assertNotEqual(self.proc.wait(), 0)

        def test_sending_sigterm_signal_terminates_on_windows(self):
            self.proc.send_signal(signal.SIGTERM)
            self.assertNotEqual(self.proc.wait(), 0)


class PidTest(unittest.TestCase):

    def testPid(self):
        # Cannot use sys.executable here because it's a script and has different
        # pid than the actual started Java process.
        p = Popen(['python', '-c', 'import os; print os.getpid()'],
                  stdout=PIPE)
        p.wait()
        self.assertEquals(int(p.stdout.read()), p.pid)

    def testNonExistingField(self):
        # Test we don't crash if Process class doesn't have field we need.
        p = Popen(['echo foo'], shell=True, stdout=PIPE)
        self.assertIsNone(p._get_pid('nonex'))


class EnvironmentInheritanceTest(unittest.TestCase):

    def testDefaultEnvIsInherited(self):
        # Test for issue #1104
        os.environ['foo'] = 'something'
        p1 = Popen([sys.executable, "-c",
                    'import os, sys; sys.stdout.write(os.environ["foo"])'],
                   stdout=PIPE)
        self.assertEquals('something', p1.stdout.read())


class JythonOptsTest(unittest.TestCase):

    """ Tests for (some parts of) issue #1187: JYTHON_OPTS should not be
    enriched by arguments
    """

    def testNoJythonOpts(self):
        os.environ['JYTHON_OPTS'] = ''
        p1 = Popen([sys.executable, "-c",
                    'import os, sys; sys.stdout.write(os.environ["JYTHON_OPTS"])'],
                   stdout=PIPE)
        self.assertEquals('', p1.stdout.read())

    def testExistingJythonOpts(self):
        options = '-Qold -Qwarn'
        os.environ['JYTHON_OPTS'] = options
        p1 = Popen([sys.executable, "-c",
                    'import os, sys; sys.stdout.write(os.environ["JYTHON_OPTS"])'],
                   stdout=PIPE)
        self.assertEquals(options, p1.stdout.read())


class Cmdline2ListTestCase(unittest.TestCase):

    cmdlines = {
        # From "Parsing C Command-Line Arguments"
        # http://msdn.microsoft.com/en-us/library/a1y7w461(VS.80).aspx
        '"a b c" d e': ['a b c', 'd', 'e'],
        r'"ab\"c" "\\" d': ['ab"c', '\\', 'd'],
        r'a\\\b d"e f"g h': [r'a\\\b', 'de fg', 'h'],
        r'a\\\"b c d': [r'a\"b', 'c', 'd'],
        r'a\\\\"b c" d e': [r'a\\b c', 'd', 'e'],

        r'C:\\foo\bar\baz jy thon': [r'C:\\foo\bar\baz', 'jy', 'thon'],
        r'C:\\Program Files\Foo\Bar qu \\ ux':
            [r'C:\\Program', 'Files\Foo\Bar', 'qu', '\\\\', 'ux'],
        r'"C:\\Program Files\Foo\Bar" qu \\ ux':
            [r'C:\\Program Files\Foo\Bar', 'qu', '\\\\', 'ux'],
        r'dir "C:\\Program Files\Foo\\" bar':
            ['dir', 'C:\\\\Program Files\\Foo\\', 'bar'],

        r'echo "\"I hate Windows!\""': ['echo', '"I hate Windows!"'],
        r'print "jython" "': ['print', 'jython', ''],
        r'print \"jython\" \"': ['print', '"jython"', '"'],
        r'print \"jython\" \\"': ['print', '"jython"', '\\']
    }

    def test_cmdline2list(self):
        for cmdline, argv in self.cmdlines.iteritems():
            self.assertEqual(_cmdline2list(cmdline), argv)


class ExceptionsTestCase(unittest.TestCase):

    def test_oserror_raised_with_errno_no_such_file_or_directory(self):
        try:
            Popen('a-file-that-should-never-exist-subprocess-test')
        except OSError as err:
            self.assertEquals(err.errno, errno.ENOENT)


def test_main():
    test_support.run_unittest(
        TerminationAndSignalTest,
        PidTest,
        EnvironmentInheritanceTest,
        JythonOptsTest,
        Cmdline2ListTestCase,
        ExceptionsTestCase,
    )


if __name__ == '__main__':
    test_main()
