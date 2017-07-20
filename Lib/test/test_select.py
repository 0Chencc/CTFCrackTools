"""
AMAK: 20050515: This module is the test_select.py from cpython 2.4, ported to jython + unittest
"""
import errno
import os
import select
import socket
import sys
import test_socket
import unittest
from test import test_support

HOST = test_socket.HOST
PORT = test_socket.PORT + 100

class SelectWrapper:

    def __init__(self):
        self.read_fds = []
        self.write_fds = []
        self.oob_fds = []
        self.timeout = None

    def add_read_fd(self, fd):
        self.read_fds.append(fd)

    def add_write_fd(self, fd):
        self.write_fds.append(fd)

    def add_oob_fd(self, fd):
        self.oob_fds.append(fd)

    def set_timeout(self, timeout):
        self.timeout = timeout

class PollWrapper:

    def __init__(self):
        self.timeout = None
        self.poll_object = select.poll()

    def add_read_fd(self, fd):
        self.poll_object.register(fd, select.POLL_IN)

    def add_write_fd(self, fd):
        self.poll_object.register(fd, select.POLL_OUT)

    def add_oob_fd(self, fd):
        self.poll_object.register(fd, select.POLL_PRI)

class TestSelectInvalidParameters(unittest.TestCase):

    def testBadSelectSetTypes(self):
        # Test some known error conditions
        for bad_select_set in [None, 1,]:
            for pos in range(2): # OOB not supported on Java
                args = [[], [], []]
                args[pos] = bad_select_set
                try:
                    timeout = 0 # Can't wait forever
                    rfd, wfd, xfd = select.select(args[0], args[1], args[2], timeout)
                except (select.error, TypeError):
                    pass
                except Exception, x:
                    self.fail("Selecting on '%s' raised wrong exception %s" % (str(bad_select_set), str(x)))
                else:
                    self.fail("Selecting on '%s' should have raised TypeError" % str(bad_select_set))

    def testBadSelectableTypes(self):
        class Nope: pass

        class Almost1:
            def fileno(self):
                return 'fileno'

        class Almost2:
            def fileno(self):
                return 'fileno'

        # Test some known error conditions
        for bad_selectable in [None, 1, object(), Nope(), Almost1(), Almost2()]:
            try:
                timeout = 0 # Can't wait forever
                rfd, wfd, xfd = select.select([bad_selectable], [], [], timeout)
            except (TypeError, select.error), x:
                pass
            else:
                self.fail("Selecting on '%s' should have raised TypeError or select.error" % str(bad_selectable))

    def testInvalidTimeoutTypes(self):
        for invalid_timeout in ['not a number']:
            try:
                rfd, wfd, xfd = select.select([], [], [], invalid_timeout)
            except TypeError:
                pass
            else:
                self.fail("Invalid timeout value '%s' should have raised TypeError" % invalid_timeout)

    def testInvalidTimeoutValues(self):
        for invalid_timeout in [-1]:
            try:
                rfd, wfd, xfd = select.select([], [], [], invalid_timeout)
            except (ValueError, select.error):
                pass
            else:
                self.fail("Invalid timeout value '%s' should have raised ValueError or select.error" % invalid_timeout)

class TestSelectClientSocket(unittest.TestCase):

    def testUnconnectedSocket(self):
        sockets = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for x in range(5)]
        for pos in range(2): # OOB not supported on Java
            args = [[], [], []]
            args[pos] = sockets
            timeout = 0 # Can't wait forever
            rfd, wfd, xfd = select.select(args[0], args[1], args[2], timeout)
            for s in sockets:
                self.failIf(s in rfd)
                self.failIf(s in wfd)

class TestPollClientSocket(unittest.TestCase):

    def testEventConstants(self):
        for event_name in ['IN', 'OUT', 'PRI', 'ERR', 'HUP', 'NVAL', ]:
            self.failUnless(hasattr(select, 'POLL%s' % event_name))

    def testUnregisterRaisesKeyError(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        poll_object = select.poll()
        try:
            poll_object.unregister(s)
        except KeyError:
            pass
        else:
            self.fail("Unregistering socket that is not registered should have raised KeyError")


class ThreadedPollClientSocket(test_socket.SocketConnectedTest):

    def testSocketRegisteredBeforeConnected(self):
        pass

    @test_support.retry(Exception)
    def _testSocketRegisteredBeforeConnected(self):
        timeout = 1000 # milliseconds
        poll_object = select.poll()
        # Register the socket before it is connected
        poll_object.register(self.cli, select.POLLOUT)
        result_list = poll_object.poll(timeout)
        result_sockets = [r[0] for r in result_list]
        self.assertIn(self.cli, result_sockets, "Unconnected client socket should be selectable")
        # Now connect the socket, but DO NOT register it again
        self.cli.setblocking(0)
        self.cli.connect( (self.HOST, self.PORT) )
        # Now poll again, to check that the poll object has recognised that the socket is now connected
        result_list = poll_object.poll(timeout)
        result_sockets = [r[0] for r in result_list]
        self.assertIn(self.cli, result_sockets, "Connected client socket should have been selectable")

    def testSelectOnSocketFileno(self):
        pass

    def _testSelectOnSocketFileno(self):
        self.cli.setblocking(0)
        self.cli.connect( (self.HOST, self.PORT) )
        return
        try:
            rfd, wfd, xfd = select.select([self.cli.fileno()], [], [], 1)
        except Exception, x:
            self.fail("Selecting on socket.fileno() should not have raised exception: %s" % str(x))

class TestJythonSelect(unittest.TestCase):
    # Normally we would have a test_select_jy for such testing, but
    # the reality is that this test module is really that test :)
    
    def test_cpython_compatible_select_exists(self):
        self.assertIs(select.cpython_compatible_select, select.select)


def test_main():

    tests = [TestSelectInvalidParameters,
             TestSelectClientSocket,
             TestPollClientSocket,
             ThreadedPollClientSocket,
             TestJythonSelect]
    suites = [unittest.makeSuite(klass, 'test') for klass in tests]
    test_support._run_suite(unittest.TestSuite(suites))


if __name__ == "__main__":
    test_main()
