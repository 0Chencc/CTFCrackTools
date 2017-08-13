"""Misc file tests.

Made for Jython.
"""
import os
import unittest
from test import test_support
from java.lang import System

class FileTestCase(unittest.TestCase):

    def tearDown(self):
        if os.path.exists(test_support.TESTFN):
            os.remove(test_support.TESTFN)

    def test_append(self):
        # http://bugs.jython.org/issue1466
        mode = 'ab'
        fp1 = open(test_support.TESTFN, mode)
        fp1.write('test1\n')
        fp2 = open(test_support.TESTFN, mode)
        fp2.write('test2\n')
        fp1.close()
        fp2.close()
        with open(test_support.TESTFN) as fp:
            self.assertEqual('test1\ntest2\n', fp.read())

    def test_appendplus(self):
        # regression with the test_append fix:
        # http://bugs.jython.org/issue1576
        with open(test_support.TESTFN, 'ab+') as fp:
            fp.write('test1\n')
            fp.seek(0)
            self.assertEqual(fp.read(), 'test1\n')

    def test_issue1825(self):
        testfnu = unicode(test_support.TESTFN)
        try:
            open(testfnu)
        except IOError, e:
            self.assertTrue(isinstance(e.filename, unicode))
            self.assertEqual(e.filename, testfnu)
        else:
            self.assertTrue(False)

    @unittest.skipUnless(hasattr(os, 'chmod'), 'chmod() support required for this test')
    def test_issue2081(self):
        with open(test_support.TESTFN, 'wb'):
            pass
        os.chmod(test_support.TESTFN, 200)      # write-only
        with open(test_support.TESTFN, 'w'):    # should succeed, raised IOError (permission denied) prior to fix
            pass

    # http://bugs.jython.org/issue2358
    def test_read_empty_file(self):
        with open(test_support.TESTFN, 'w'):
            pass
        with open(test_support.TESTFN) as f:
            self.assertEqual(f.read(), '')

    # http://bugs.jython.org/issue2358
    @unittest.skipUnless(System.getProperty('os.name') == u'Linux', 'Linux required')
    def test_can_read_proc_filesystem(self):
        with open('/proc/{}/cmdline'.format(os.getpid())) as f:
            self.assertIn('jython', f.read())


def test_main():
    test_support.run_unittest(FileTestCase)


if __name__ == '__main__':
    test_main()
