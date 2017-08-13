import java

import unittest
from test import test_support

import errno
import gc
import jarray
import Queue
import platform
import pprint
import select
import socket
import struct
import sys
import time
import thread, threading
from weakref import proxy
from StringIO import StringIO
from _socket import _check_threadpool_for_pending_threads, NIO_GROUP

PORT = 50100
HOST = 'localhost'
MSG = 'Michael Gilfix was here\n'
EIGHT_BIT_MSG = 'Bh\xed Al\xe1in \xd3 Cinn\xe9ide anseo\n'
os_name = platform.java_ver()[3][0]
is_bsd = os_name == 'Mac OS X' or 'BSD' in os_name
is_solaris = os_name == 'SunOS'

if test_support.is_jython:
    import _socket
    _socket._NUM_THREADS = 5

    import java.util.logging
    def _set_java_logging(name, level):
        java.util.logging.Logger.getLogger(name).setLevel(level)


class SocketTCPTest(unittest.TestCase):

    HOST = HOST
    PORT = PORT

    def setUp(self):
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serv.bind((self.HOST, self.PORT))
        self.serv.listen(1)

    def tearDown(self):
        self.serv.close()
        self.serv = None

class SocketUDPTest(unittest.TestCase):

    HOST = HOST
    PORT = PORT

    def setUp(self):
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serv.bind((self.HOST, self.PORT))

    def tearDown(self):
        self.serv.close()
        self.serv = None

class ThreadableTest:
    """Threadable Test class

    The ThreadableTest class makes it easy to create a threaded
    client/server pair from an existing unit test. To create a
    new threaded class from an existing unit test, use multiple
    inheritance:

        class NewClass (OldClass, ThreadableTest):
            pass

    This class defines two new fixture functions with obvious
    purposes for overriding:

        clientSetUp ()
        clientTearDown ()

    Any new test functions within the class must then define
    tests in pairs, where the test name is preceeded with a
    '_' to indicate the client portion of the test. Ex:

        def testFoo(self):
            # Server portion

        def _testFoo(self):
            # Client portion

    Any exceptions raised by the clients during their tests
    are caught and transferred to the main thread to alert
    the testing framework.

    Note, the server setup function cannot call any blocking
    functions that rely on the client thread during setup,
    unless serverExplicitReady() is called just before
    the blocking call (such as in setting up a client/server
    connection and performing the accept() in setUp().
    """

    def __init__(self):
        # Swap the true setup function
        self.__setUp = self.setUp
        self.__tearDown = self.tearDown
        self.setUp = self._setUp
        self.tearDown = self._tearDown

    def serverExplicitReady(self):
        """This method allows the server to explicitly indicate that
        it wants the client thread to proceed. This is useful if the
        server is about to execute a blocking routine that is
        dependent upon the client thread during its setup routine."""

        def be_ready():
            # Because of socket reuse, old server sockets may still be
            # accepting client connections as they get shutdown, but
            # before they accept with the new server socket.
            #
            # Avoid race by ensuring accept is started before clients
            # attempt to connect.
            self.server_ready.set()
        threading.Timer(0.1, be_ready).start()

    def _setUp(self):
        self.server_ready = threading.Event()
        self.client_ready = threading.Event()
        self.done = threading.Event()
        self.queue = Queue.Queue(1)

        # Do some munging to start the client test.
        methodname = self.id()
        i = methodname.rfind('.')
        methodname = methodname[i+1:]
        self.test_method_name = methodname
        test_method = getattr(self, '_' + methodname)
        self.client_thread = thread.start_new_thread(
            self.clientRun, (test_method,))

        self.__setUp()
        if not self.server_ready.isSet():
            self.server_ready.set()
        self.client_ready.wait()

    def _assert_no_pending_threads(self, group, msg):
        # Ensure __del__ finalizers are called on sockets. Two things to note:
        # 1. It takes two collections for finalization to run.
        # 2. gc.collect() is only advisory to the JVM, never mandatory. Still 
        #    it usually seems to happen under light load.

        # Wait up to one second for there not to be pending threads

        for i in xrange(10):
            pending_threads = _check_threadpool_for_pending_threads(group)
            if len(pending_threads) == 0:
                break
            test_support.gc_collect()
            
        if pending_threads:
            print "Pending threads in Netty msg={} pool={}".format(msg, pprint.pformat(pending_threads))
        
    def _tearDown(self):
        self.done.wait()   # wait for the client to exit
        self.__tearDown()

        msg = None
        if not self.queue.empty():
            msg = self.queue.get()
        
        self._assert_no_pending_threads(NIO_GROUP, "Client thread pool")
        if hasattr(self, "srv"):
            self._assert_no_pending_threads(self.srv.group, "Server thread pool")

        if msg:
            print "Got this message=%s %r" % (type(msg), msg)
            self.fail("msg={}".format(msg))

            
    def clientRun(self, test_func):
        self.server_ready.wait()
        self.client_ready.set()
        self.clientSetUp()
        if not callable(test_func):
            raise TypeError, "test_func must be a callable function"
        try:
            test_func()
        except Exception, strerror:
            self.queue.put(strerror)
        self.clientTearDown()

    def clientSetUp(self):
        raise NotImplementedError, "clientSetUp must be implemented."

    def clientTearDown(self):
        self.done.set()

class ThreadedTCPSocketTest(SocketTCPTest, ThreadableTest):

    def __init__(self, methodName='runTest'):
        SocketTCPTest.__init__(self, methodName=methodName)
        ThreadableTest.__init__(self)

    def clientSetUp(self):
        self.cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cli.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def clientTearDown(self):
        self.cli.close()
        self.cli = None
        ThreadableTest.clientTearDown(self)

class ThreadedUDPSocketTest(SocketUDPTest, ThreadableTest):

    def __init__(self, methodName='runTest'):
        SocketUDPTest.__init__(self, methodName=methodName)
        ThreadableTest.__init__(self)

    def clientSetUp(self):
        self.cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.cli.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

class SocketConnectedTest(ThreadedTCPSocketTest):

    def __init__(self, methodName='runTest'):
        ThreadedTCPSocketTest.__init__(self, methodName=methodName)

    def setUp(self):
        ThreadedTCPSocketTest.setUp(self)
        # Indicate explicitly we're ready for the client thread to
        # proceed and then perform the blocking call to accept
        self.serverExplicitReady()
        conn, addr = self.serv.accept()
        self.cli_conn = conn

    def tearDown(self):
        self.cli_conn.close()
        self.cli_conn = None
        ThreadedTCPSocketTest.tearDown(self)

    def clientSetUp(self):
        ThreadedTCPSocketTest.clientSetUp(self)
        self.cli.connect((self.HOST, self.PORT))
        self.serv_conn = self.cli

    def clientTearDown(self):
        self.serv_conn.close()
        self.serv_conn = None
        ThreadedTCPSocketTest.clientTearDown(self)

class SocketPairTest(unittest.TestCase, ThreadableTest):

    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName=methodName)
        ThreadableTest.__init__(self)

    def setUp(self):
        self.serv, self.cli = socket.socketpair()

    def tearDown(self):
        self.serv.close()
        self.serv = None

    def clientSetUp(self):
        pass

    def clientTearDown(self):
        self.cli.close()
        self.cli = None
        ThreadableTest.clientTearDown(self)


#######################################################################
## Begin Tests

class GeneralModuleTests(unittest.TestCase):

    def test_weakref(self):
        if sys.platform[:4] == 'java': return
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        p = proxy(s)
        self.assertEqual(p.fileno(), s.fileno())
        s.close()
        s = None
        try:
            p.fileno()
        except ReferenceError:
            pass
        else:
            self.fail('Socket proxy still exists')

    def testSocketError(self):
        # Testing socket module exceptions
        def raise_error(*args, **kwargs):
            raise socket.error
        def raise_herror(*args, **kwargs):
            raise socket.herror
        def raise_gaierror(*args, **kwargs):
            raise socket.gaierror
        self.failUnlessRaises(socket.error, raise_error,
                              "Error raising socket exception.")
        self.failUnlessRaises(socket.error, raise_herror,
                              "Error raising socket exception.")
        self.failUnlessRaises(socket.error, raise_gaierror,
                              "Error raising socket exception.")

    def testCrucialConstants(self):
        # Testing for mission critical constants
        socket.AF_INET
        socket.SOCK_STREAM
        socket.SOCK_DGRAM
        socket.SOCK_RAW
        socket.SOCK_RDM
        socket.SOCK_SEQPACKET
        socket.SOL_SOCKET
        socket.SO_REUSEADDR

    def testHostnameRes(self):
        # Testing hostname resolution mechanisms
        hostname = socket.gethostname()
        self.assert_(isinstance(hostname, str))
        try:
            ip = socket.gethostbyname(hostname)
            self.assert_(isinstance(ip, str))
        except socket.error:
            # Probably name lookup wasn't set up right; skip this test
            self.fail("Probably name lookup wasn't set up right; skip testHostnameRes.gethostbyname")
            return
        self.assert_(ip.find('.') >= 0, "Error resolving host to ip.")
        try:
            hname, aliases, ipaddrs = socket.gethostbyaddr(ip)
            self.assert_(isinstance(hname, str))
            for hosts in aliases, ipaddrs:
                self.assert_(all(isinstance(host, str) for host in hosts))
        except socket.error:
            # Probably a similar problem as above; skip this test
            self.fail("Probably name lookup wasn't set up right; skip testHostnameRes.gethostbyaddr")
            return
        all_host_names = [hostname, hname] + aliases
        fqhn = socket.getfqdn()
        self.assert_(isinstance(fqhn, str))
        if not fqhn in all_host_names:
            self.fail("Error testing host resolution mechanisms.")

    def testRefCountGetNameInfo(self):
        # Testing reference count for getnameinfo
        import sys
        if hasattr(sys, "getrefcount"):
            try:
                # On some versions, this loses a reference
                orig = sys.getrefcount(__name__)
                socket.getnameinfo(__name__,0)
            except SystemError:
                if sys.getrefcount(__name__) <> orig:
                    self.fail("socket.getnameinfo loses a reference")

    def testInterpreterCrash(self):
        if sys.platform[:4] == 'java': return
        # Making sure getnameinfo doesn't crash the interpreter
        try:
            # On some versions, this crashes the interpreter.
            socket.getnameinfo(('x', 0, 0, 0), 0)
        except socket.error:
            pass

# Need to implement binary AND for ints and longs

    def testNtoH(self):
        if sys.platform[:4] == 'java': return # problems with int & long
        # This just checks that htons etc. are their own inverse,
        # when looking at the lower 16 or 32 bits.
        sizes = {socket.htonl: 32, socket.ntohl: 32,
                 socket.htons: 16, socket.ntohs: 16}
        for func, size in sizes.items():
            mask = (1L<<size) - 1
            for i in (0, 1, 0xffff, ~0xffff, 2, 0x01234567, 0x76543210):
                self.assertEqual(i & mask, func(func(i&mask)) & mask)

            swapped = func(mask)
            self.assertEqual(swapped & mask, mask)
            self.assertRaises(OverflowError, func, 1L<<34)

    def testGetServBy(self):
        eq = self.assertEqual
        # Find one service that exists, then check all the related interfaces.
        # I've ordered this by protocols that have both a tcp and udp
        # protocol, at least for modern Linuxes.
        if sys.platform in ('linux2', 'freebsd4', 'freebsd5', 'freebsd6',
                            'darwin') or is_bsd:
            # avoid the 'echo' service on this platform, as there is an
            # assumption breaking non-standard port/protocol entry
            services = ('daytime', 'qotd', 'domain')
        else:
            services = ('echo', 'daytime', 'domain')
        for service in services:
            try:
                port = socket.getservbyname(service, 'tcp')
                break
            except socket.error:
                pass
        else:
            raise socket.error
        # Try same call with optional protocol omitted
        port2 = socket.getservbyname(service)
        eq(port, port2)
        # Try udp, but don't barf it it doesn't exist
        try:
            udpport = socket.getservbyname(service, 'udp')
        except socket.error:
            udpport = None
        else:
            eq(udpport, port)
        # Now make sure the lookup by port returns the same service name
        eq(socket.getservbyport(port2), service)
        eq(socket.getservbyport(port, 'tcp'), service)
        if udpport is not None:
            eq(socket.getservbyport(udpport, 'udp'), service)

    def testGetServByExceptions(self):
        # First getservbyname
        try:
            result = socket.getservbyname("nosuchservice")
        except socket.error:
            pass
        except Exception, x:
            self.fail("getservbyname raised wrong exception for non-existent service: %s" % str(x))
        else:
            self.fail("getservbyname failed to raise exception for non-existent service: %s" % str(result))

        # Now getservbyport
        try:
            result = socket.getservbyport(55555)
        except socket.error:
            pass
        except Exception, x:
            self.fail("getservbyport raised wrong exception for unknown port: %s" % str(x))
        else:
            self.fail("getservbyport failed to raise exception for unknown port: %s" % str(result))

    def testGetProtoByName(self):
        self.failUnlessEqual(socket.IPPROTO_TCP, socket.getprotobyname("tcp"))
        self.failUnlessEqual(socket.IPPROTO_UDP, socket.getprotobyname("udp"))
        try:
            result = socket.getprotobyname("nosuchproto")
        except socket.error:
            pass
        except Exception, x:
            self.fail("getprotobyname raised wrong exception for unknown protocol: %s" % str(x))
        else:
            self.fail("getprotobyname failed to raise exception for unknown protocol: %s" % str(result))

    def testDefaultTimeout(self):
        # Testing default timeout
        # The default timeout should initially be None
        self.assertEqual(socket.getdefaulttimeout(), None)
        s = socket.socket()
        self.assertEqual(s.gettimeout(), None)
        s.close()

        # Set the default timeout to 10, and see if it propagates
        socket.setdefaulttimeout(10)
        self.assertEqual(socket.getdefaulttimeout(), 10)
        s = socket.socket()
        self.assertEqual(s.gettimeout(), 10)
        s.close()

        # Reset the default timeout to None, and see if it propagates
        socket.setdefaulttimeout(None)
        self.assertEqual(socket.getdefaulttimeout(), None)
        s = socket.socket()
        self.assertEqual(s.gettimeout(), None)
        s.close()

        # Check that setting it to an invalid value raises ValueError
        self.assertRaises(ValueError, socket.setdefaulttimeout, -1)

        # Check that setting it to an invalid type raises TypeError
        self.assertRaises(TypeError, socket.setdefaulttimeout, "spam")

    def testIPv4toString(self):
        if not hasattr(socket, 'inet_pton'):
            return # No inet_pton() on this platform
        from socket import inet_aton as f, inet_pton, AF_INET
        g = lambda a: inet_pton(AF_INET, a)

        self.assertEquals('\x00\x00\x00\x00', f('0.0.0.0'))
        self.assertEquals('\xff\x00\xff\x00', f('255.0.255.0'))
        self.assertEquals('\xaa\xaa\xaa\xaa', f('170.170.170.170'))
        self.assertEquals('\x01\x02\x03\x04', f('1.2.3.4'))

        self.assertEquals('\x00\x00\x00\x00', g('0.0.0.0'))
        self.assertEquals('\xff\x00\xff\x00', g('255.0.255.0'))
        self.assertEquals('\xaa\xaa\xaa\xaa', g('170.170.170.170'))

    def testIPv6toString(self):
        if not hasattr(socket, 'inet_pton'):
            return # No inet_pton() on this platform
        try:
            from socket import inet_pton, AF_INET6, has_ipv6
            if not has_ipv6:
                return
        except ImportError:
            return
        f = lambda a: inet_pton(AF_INET6, a)

        self.assertEquals('\x00' * 16, f('::'))
        self.assertEquals('\x00' * 16, f('0::0'))
        self.assertEquals('\x00\x01' + '\x00' * 14, f('1::'))
        self.assertEquals(
            '\x45\xef\x76\xcb\x00\x1a\x56\xef\xaf\xeb\x0b\xac\x19\x24\xae\xae',
            f('45ef:76cb:1a:56ef:afeb:bac:1924:aeae')
        )

    def test_inet_pton_exceptions(self):
        if not hasattr(socket, 'inet_pton'):
            return # No inet_pton() on this platform

        try:
            socket.inet_pton(socket.AF_UNSPEC, "doesntmatter")
        except socket.error, se:
            self.failUnlessEqual(se[0], errno.EAFNOSUPPORT)
        except Exception, x:
            self.fail("inet_pton raised wrong exception for incorrect address family AF_UNSPEC: %s" % str(x))

        try:
            socket.inet_pton(socket.AF_INET, "1.2.3.")
        except socket.error, se:
            pass
        except Exception, x:
            self.fail("inet_pton raised wrong exception for invalid AF_INET address: %s" % str(x))

        try:
            socket.inet_pton(socket.AF_INET6, ":::")
        except socket.error, se:
            pass
        except Exception, x:
            self.fail("inet_pton raised wrong exception for invalid AF_INET6 address: %s" % str(x))

    def testStringToIPv4(self):
        if not hasattr(socket, 'inet_ntop'):
            return # No inet_ntop() on this platform
        from socket import inet_ntoa as f, inet_ntop, AF_INET
        g = lambda a: inet_ntop(AF_INET, a)

        self.assertEquals('1.0.1.0', f('\x01\x00\x01\x00'))
        self.assertEquals('170.85.170.85', f('\xaa\x55\xaa\x55'))
        self.assertEquals('255.255.255.255', f('\xff\xff\xff\xff'))
        self.assertEquals('1.2.3.4', f('\x01\x02\x03\x04'))

        self.assertEquals('1.0.1.0', g('\x01\x00\x01\x00'))
        self.assertEquals('170.85.170.85', g('\xaa\x55\xaa\x55'))
        self.assertEquals('255.255.255.255', g('\xff\xff\xff\xff'))

    def testStringToIPv6(self):
        if not hasattr(socket, 'inet_ntop'):
            return # No inet_ntop() on this platform
        try:
            from socket import inet_ntop, AF_INET6, has_ipv6
            if not has_ipv6:
                return
        except ImportError:
            return
        f = lambda a: inet_ntop(AF_INET6, a)

#        self.assertEquals('::', f('\x00' * 16))
#        self.assertEquals('::1', f('\x00' * 15 + '\x01'))
        # java.net.InetAddress always return the full unabbreviated form
        self.assertEquals('0:0:0:0:0:0:0:0', f('\x00' * 16))
        self.assertEquals('0:0:0:0:0:0:0:1', f('\x00' * 15 + '\x01'))
        self.assertEquals(
            'aef:b01:506:1001:ffff:9997:55:170',
            f('\x0a\xef\x0b\x01\x05\x06\x10\x01\xff\xff\x99\x97\x00\x55\x01\x70')
        )

    def test_inet_ntop_exceptions(self):
        if not hasattr(socket, 'inet_ntop'):
            return # No inet_ntop() on this platform
        valid_address = '\x01\x01\x01\x01'
        invalid_address = '\x01\x01\x01\x01\x01'

        try:
            socket.inet_ntop(socket.AF_UNSPEC, valid_address)
        except ValueError, v:
            pass
        except Exception, x:
            self.fail("inet_ntop raised wrong exception for incorrect address family AF_UNSPEC: %s" % str(x))

        try:
            socket.inet_ntop(socket.AF_INET, invalid_address)
        except ValueError, v:
            pass
        except Exception, x:
            self.fail("inet_ntop raised wrong exception for invalid AF_INET address: %s" % str(x))

        try:
            socket.inet_ntop(socket.AF_INET6, invalid_address)
        except ValueError, v:
            pass
        except Exception, x:
            self.fail("inet_ntop raised wrong exception for invalid AF_INET address: %s" % str(x))

    # XXX The following don't test module-level functionality...

    def testSockName(self):
        # Testing getsockname()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("0.0.0.0", PORT+1))
        name = sock.getsockname()
        self.assertEqual(name, ("0.0.0.0", PORT+1))

    def testSockNameEphemeralV4(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 0))
        sock.listen(1)
        name = sock.getsockname()
        self.assertEqual(len(name), 2)
        self.assertNotEqual(name[1], 0)

    def testSockNameEphemeralV6(self):
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        sock.bind(('', 0, 0, 0))
        sock.listen(1)
        name = sock.getsockname()
        self.assertEqual(len(name), 4)
        self.assertNotEqual(name[1], 0)

    def testSockAttributes(self):
        # Testing required attributes
        for family in [socket.AF_INET, socket.AF_INET6]:
            for sock_type in [socket.SOCK_STREAM, socket.SOCK_DGRAM]:
                s = socket.socket(family, sock_type)
                self.assertEqual(s.family, family)
                self.assertEqual(s.type, sock_type)
                if sock_type == socket.SOCK_STREAM:
                    self.assertEqual(s.proto, socket.IPPROTO_TCP)
                else:
                    self.assertEqual(s.proto, socket.IPPROTO_UDP)

    def testGetSockOpt(self):
        # Testing getsockopt()
        # We know a socket should start without reuse==0
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        reuse = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
        self.failIf(reuse != 0, "initial mode is reuse")

    def testSetSockOpt(self):
        # Testing setsockopt()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        reuse = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
        self.failIf(reuse == 0, "failed to set reuse mode")

    def testSendAfterClose(self):
        # testing send() after close() with timeout
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.close()
        self.assertRaises(socket.error, sock.send, "spam")

    def testSocketTypeAvailable(self):
        self.assertIs(socket.socket, socket.SocketType)

class IPAddressTests(unittest.TestCase):

    def testValidIpV4Addresses(self):
        for a in [
            "0.0.0.1",
            "1.0.0.1",
            "127.0.0.1",
            "255.12.34.56",
            "255.255.255.255",
        ]:
            self.failUnless(socket.is_ipv4_address(a), "is_ipv4_address failed for valid IPV4 address '%s'" % a)
            self.failUnless(socket.is_ip_address(a), "is_ip_address failed for valid IPV4 address '%s'" % a)
            
    def testInvalidIpV4Addresses(self):
        for a in [
            "99.2",
            "99.2.4",
            "-10.1.2.3",
            "256.0.0.0",
            "0.256.0.0",
            "0.0.256.0",
            "0.0.0.256",
            "255.24.x.100",
            "255.24.-1.128",
            "255.24.-1.128.",
            "255.0.0.999",
        ]:
            self.failUnless(not socket.is_ipv4_address(a), "not is_ipv4_address failed for invalid IPV4 address '%s'" % a)
            self.failUnless(not socket.is_ip_address(a), "not is_ip_address failed for invalid IPV4 address '%s'" % a)

    def testValidIpV6Addresses(self):
        for a in [
            "::",
            "::1",
            "fe80::1",
            "::192.168.1.1",
            "0:0:0:0:0:0:0:0",
            "1080::8:800:2C:4A",
            "FEC0:0:0:0:0:0:0:1",
            "::FFFF:192.168.1.1",
            "abcd:ef:111:f123::1",
            "1138:0:0:0:8:80:800:417A",
            "fecc:face::b00c:f001:fedc:fedd",
            "CaFe:BaBe:dEAd:BeeF:12:345:6789:abcd",
        ]:
            self.failUnless(socket.is_ipv6_address(a), "is_ipv6_address failed for valid IPV6 address '%s'" % a)
            self.failUnless(socket.is_ip_address(a), "is_ip_address failed for valid IPV6 address '%s'" % a)
            
    def testInvalidIpV6Addresses(self):
        for a in [
            "2001:db8:::192.0.2.1", # from RFC 5954
            "CaFe:BaBe:dEAd:BeeF:12:345:6789:abcd:",
            "CaFe:BaBe:dEAd:BeeF:12:345:6789:abcd:ef",
            "CaFFe:1a77e:dEAd:BeeF:12:345:6789:abcd",
        ]:
            self.failUnless(not socket.is_ipv6_address(a), "not is_ipv6_address failed for invalid IPV6 address '%s'" % a)
            self.failUnless(not socket.is_ip_address(a), "not is_ip_address failed for invalid IPV6 address '%s'" % a)

    def testRFC5952(self):
        for a in [
            "2001:db8::",
            "2001:db8::1",
            "2001:db8:0::1",
            "2001:db8:0:0::1",
            "2001:db8:0:0:0::1",
            "2001:DB8:0:0:1::1",
            "2001:db8:0:0:1::1",
            "2001:db8::1:0:0:1",
            "2001:0db8::1:0:0:1",
            "2001:db8::0:1:0:0:1",
            "2001:db8:0:0:1:0:0:1",
            "2001:db8:0000:0:1::1",
            "2001:db8::aaaa:0:0:1",
            "2001:db8:0:0:aaaa::1",
            "2001:0db8:0:0:1:0:0:1",
            "2001:db8:aaaa:bbbb:cccc:dddd::1",
            "2001:db8:aaaa:bbbb:cccc:dddd:0:1",
            "2001:db8:aaaa:bbbb:cccc:dddd:eeee:1",
            "2001:db8:aaaa:bbbb:cccc:dddd:eeee:01",
            "2001:db8:aaaa:bbbb:cccc:dddd:eeee:001",
            "2001:db8:aaaa:bbbb:cccc:dddd:eeee:0001",
            "2001:db8:aaaa:bbbb:cccc:dddd:eeee:aaaa",
            "2001:db8:aaaa:bbbb:cccc:dddd:eeee:AAAA",
            "2001:db8:aaaa:bbbb:cccc:dddd:eeee:AaAa",
        ]:
            self.failUnless(socket.is_ipv6_address(a), "is_ipv6_address failed for valid RFC 5952 IPV6 address '%s'" % a)
            self.failUnless(socket.is_ip_address(a), "is_ip_address failed for valid RFC 5952 IPV6 address '%s'" % a)
      
class TestSocketOptions(unittest.TestCase):

    def setUp(self):
        self.test_udp = self.test_tcp_client = self.test_tcp_server = 0

    def _testSetAndGetOption(self, sock, level, option, values):
        for expected_value in values:
            sock.setsockopt(level, option, expected_value)
            retrieved_value = sock.getsockopt(level, option)
            msg = "TCP Retrieved option(%s, %s) value %s != %s(value set)" % (level, option, retrieved_value, expected_value)
            if option == socket.SO_RCVBUF:
                self.assert_(retrieved_value >= expected_value, msg)
            else:
                self.failUnlessEqual(retrieved_value, expected_value, msg)

    def _testUDPOption(self, level, option, values):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._testSetAndGetOption(sock, level, option, values)
            # now bind the socket i.e. cause the implementation socket to be created
            sock.bind( (HOST, PORT) )
            retrieved_option_value = sock.getsockopt(level, option)
            self.failUnlessEqual(retrieved_option_value, values[-1], \
                 "UDP Option value '(%s, %s)'='%s' did not propagate to implementation socket: got %s" % (level, option, values[-1], retrieved_option_value) )
            self._testSetAndGetOption(sock, level, option, values)
        finally:
            sock.close()

    def _testTCPClientOption(self, level, option, values):
        sock = None
        try:
            # First listen on a server socket, so that the connection won't be refused.
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_sock.bind( (HOST, PORT) )
            server_sock.listen(50)
            # Now do the tests
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._testSetAndGetOption(sock, level, option, values)
            # now connect the socket i.e. cause the implementation socket to be created
            # First bind, so that the SO_REUSEADDR setting propagates
            #sock.bind( (HOST, PORT+1) )
            sock.connect( (HOST, PORT) )
            retrieved_option_value = sock.getsockopt(level, option)
            msg = "TCP client option value '%s'='%s' did not propagate to implementation socket: got %s" % (option, values[-1], retrieved_option_value)
            if option in (socket.SO_RCVBUF, socket.SO_SNDBUF):
                # NOTE: there's no guarantee that bufsize will be the
                # exact setsockopt value, particularly after
                # establishing a connection. seems it will be *at least*
                # the values we test (which are rather small) on
                # BSDs.
                self.assert_(retrieved_option_value >= values[-1], msg)
            else:
                self.failUnlessEqual(retrieved_option_value, values[-1], msg)
            self._testSetAndGetOption(sock, level, option, values)
        finally:
            server_sock.close()
            if sock:
                sock.close()
            pass

    def _testTCPClientInheritedOption(self, level, option, values):
        cli_sock = accepted_sock = None
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._testSetAndGetOption(server_sock, level, option, values)
            # now bind and listen on the socket i.e. cause the implementation socket to be created
            server_sock.bind( (HOST, PORT) )
            server_sock.listen(50)
            # Now create client socket to connect to server
            cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cli_sock.connect( (HOST, PORT) )
            accepted_sock = server_sock.accept()[0]
            retrieved_option_value = accepted_sock.getsockopt(level, option)
            msg = "TCP client inherited option value '(%s,%s)'='%s' did not propagate to accepted socket: got %s" % (level, option, values[-1], retrieved_option_value)
            if option == socket.SO_RCVBUF:
                # NOTE: see similar bsd/solaris workaround above
                self.assert_(retrieved_option_value >= values[-1], msg)
            else:
                self.failUnlessEqual(retrieved_option_value, values[-1], msg)
            self._testSetAndGetOption(accepted_sock, level, option, values)
        finally:
            server_sock.close()
            time.sleep(1)
            if cli_sock:
                cli_sock.close()
            if accepted_sock:
                accepted_sock.close()

    def _testTCPServerOption(self, level, option, values):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._testSetAndGetOption(sock, level, option, values)
            # now bind and listen on the socket i.e. cause the implementation socket to be created
            sock.bind( (HOST, PORT) )
            sock.listen(50)
            retrieved_option_value = sock.getsockopt(level, option)
            msg = "TCP server option value '(%s,%s)'='%s' did not propagate to implementation socket. Got %s" % (level, option, values[-1], retrieved_option_value)
            if option == socket.SO_RCVBUF:
                # NOTE: see similar bsd/solaris workaround above
                self.assert_(retrieved_option_value >= values[-1], msg)
            else:
                self.failUnlessEqual(retrieved_option_value, values[-1], msg)
            self._testSetAndGetOption(sock, level, option, values)
        finally:
            sock.close()

    def _testOption(self, level, option, values):
        for flag, func in [
            (self.test_udp,        self._testUDPOption),
            (self.test_tcp_client, self._testTCPClientOption),
            (self.test_tcp_server, self._testTCPServerOption),
        ]:
            if flag:
                func(level, option, values)
            else:
                try:
                    func(level, option, values)
                except socket.error, se:
                    self.failUnlessEqual(se[0], errno.ENOPROTOOPT, "Wrong errno from unsupported option exception: %d" % se[0])
                except Exception, x:
                    self.fail("Wrong exception raised from unsupported option: %s" % str(x))
                else:
                    self.fail("Setting unsupported option should have raised an exception")

    def _testInheritedOption(self, level, option, values):
        try:
            self._testTCPClientInheritedOption(level, option, values)
        except Exception, x:
            self.fail("Inherited option should not have raised exception: %s" % str(x))

class TestSupportedOptions(TestSocketOptions):

    def testSO_BROADCAST(self):
        self.test_udp = 1
        self._testOption(socket.SOL_SOCKET, socket.SO_BROADCAST, [0, 1])

    def testSO_KEEPALIVE(self):
        self.test_tcp_client = 1
        self.test_tcp_server = 1
        self._testOption(socket.SOL_SOCKET, socket.SO_KEEPALIVE, [0, 1])
        self._testInheritedOption(socket.SOL_SOCKET, socket.SO_KEEPALIVE, [0, 1])

    # def testSO_LINGER(self):
    #     self.test_tcp_client = 1
    #     self.test_tcp_server = 1
    #     off = struct.pack('ii', 0, 0)
    #     on_2_seconds = struct.pack('ii', 1, 2)
    #     self._testOption(socket.SOL_SOCKET, socket.SO_LINGER, [off, on_2_seconds])
    #     self._testInheritedOption(socket.SOL_SOCKET, socket.SO_LINGER, [off, on_2_seconds])

    # # WILL NOT FIX
    # def testSO_OOBINLINE(self):
    #     self.test_tcp_client = 1
    #     self.test_tcp_server = 1
    #     self._testOption(socket.SOL_SOCKET, socket.SO_OOBINLINE, [0, 1])
    #     self._testInheritedOption(socket.SOL_SOCKET, socket.SO_OOBINLINE, [0, 1])

    def testSO_RCVBUF(self):
        self.test_udp        = 1
        self.test_tcp_client = 1
        self.test_tcp_server = 1
        self._testOption(socket.SOL_SOCKET, socket.SO_RCVBUF, [1024, 4096, 16384])
        self._testInheritedOption(socket.SOL_SOCKET, socket.SO_RCVBUF, [1024, 4096, 16384])

    def testSO_REUSEADDR(self):
        self.test_udp        = 1
        self.test_tcp_client = 1
        self.test_tcp_server = 1
        self._testOption(socket.SOL_SOCKET, socket.SO_REUSEADDR, [0, 1])
        self._testInheritedOption(socket.SOL_SOCKET, socket.SO_REUSEADDR, [0, 1])

    def testSO_SNDBUF(self):
        self.test_udp        = 1
        self.test_tcp_client = 1
        self.test_tcp_server = 1
        self._testOption(socket.SOL_SOCKET, socket.SO_SNDBUF, [1024, 4096, 16384])
        self._testInheritedOption(socket.SOL_SOCKET, socket.SO_SNDBUF, [1024, 4096, 16384])

    def testSO_TIMEOUT(self):
        self.test_udp        = 1
        self.test_tcp_client = 1
        self.test_tcp_server = 1
        self._testOption(socket.SOL_SOCKET, socket.SO_TIMEOUT, [0, 1, 1000])
        self._testInheritedOption(socket.SOL_SOCKET, socket.SO_TIMEOUT, [0, 1, 1000])

    def testTCP_NODELAY(self):
        self.test_tcp_client = 1
        self.test_tcp_server = 1
        self._testOption(socket.IPPROTO_TCP, socket.TCP_NODELAY, [0, 1])
        self._testInheritedOption(socket.IPPROTO_TCP, socket.TCP_NODELAY, [0, 1])

class TestPseudoOptions(unittest.TestCase):

    def testSO_ACCEPTCONN(self):
        for socket_type, listen, expected_result in [
            (socket.SOCK_STREAM, 0, 0),
            (socket.SOCK_STREAM, 1, 1),
            (socket.SOCK_DGRAM,   0, Exception),
            ]:
            s = socket.socket(socket.AF_INET, socket_type)
            if listen:
                s.listen(1)
            try:
                result = s.getsockopt(socket.SOL_SOCKET, socket.SO_ACCEPTCONN)
                if expected_result is not Exception:
                    self.failUnlessEqual(result, expected_result)
            except socket.error, se:
                if expected_result is Exception:
                    if se[0] != errno.ENOPROTOOPT:
                        self.fail("getsockopt(SO_ACCEPTCONN) on wrong socket type raised wrong exception: %s" % str(se))
                else:
                    self.fail("getsocket(SO_ACCEPTCONN) on valid socket type should not have raised exception: %s" % (str(se)))

    def testSO_ERROR(self):
        good = bad = None

        try:
            good = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            good.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            good.bind((HOST, PORT))
            good.listen(1)
            bad = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            bad.bind((HOST, PORT))
            bad.listen(1)
            self.fail("Listen operation against same port did not generate an expected error")
        except socket.error, se:
            self.failUnlessEqual(bad.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR), se[0])
            # try again, should now be reset
            self.failUnlessEqual(bad.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR), 0)
        finally:
            if good is not None:
                good.close()
            if bad is not None:
                bad.close()

    def testSO_TYPE(self):
        for socket_type in [socket.SOCK_STREAM, socket.SOCK_DGRAM]:
            s = socket.socket(socket.AF_INET, socket_type)
            self.failUnlessEqual(s.getsockopt(socket.SOL_SOCKET, socket.SO_TYPE), socket_type)

class TestUnsupportedOptions(TestSocketOptions):

    def testSO_DEBUG(self):
        self.failUnless(hasattr(socket, 'SO_DEBUG'))

    def testSO_DONTROUTE(self):
        self.failUnless(hasattr(socket, 'SO_DONTROUTE'))

    def testSO_EXCLUSIVEADDRUSE(self):
        # this is an MS specific option that will not be appearing on java
        # http://bugs.sun.com/bugdatabase/view_bug.do?bug_id=6421091
        # http://bugs.sun.com/bugdatabase/view_bug.do?bug_id=6402335
        # 
        # As of 2.7.1, we no longer support this option - it is also
        # not not necessary since Java implements BSD semantics for
        # address reuse even on Windows. See
        # http://bugs.jython.org/issue2435 and
        # http://sourceforge.net/p/jython/mailman/message/34642295/
        # for discussion
        self.assertFalse(hasattr(socket, 'SO_EXCLUSIVEADDRUSE'))

    def testSO_RCVLOWAT(self):
        self.failUnless(hasattr(socket, 'SO_RCVLOWAT'))

    def testSO_RCVTIMEO(self):
        self.failUnless(hasattr(socket, 'SO_RCVTIMEO'))

    def testSO_REUSEPORT(self):
        # not yet supported on java
        # http://bugs.sun.com/bugdatabase/view_bug.do?bug_id=6432031
        self.failUnless(hasattr(socket, 'SO_REUSEPORT'))

    def testSO_SNDLOWAT(self):
        self.failUnless(hasattr(socket, 'SO_SNDLOWAT'))

    def testSO_SNDTIMEO(self):
        self.failUnless(hasattr(socket, 'SO_SNDTIMEO'))

    def testSO_USELOOPBACK(self):
        self.failUnless(hasattr(socket, 'SO_USELOOPBACK'))

class BasicTCPTest(SocketConnectedTest):

    def __init__(self, methodName='runTest'):
        SocketConnectedTest.__init__(self, methodName=methodName)

    def testRecv(self):
        # Testing large receive over TCP
        msg = self.cli_conn.recv(1024)
        self.assertEqual(msg, MSG)

    def _testRecv(self):
        self.serv_conn.send(MSG)

    def testRecvTimeoutMode(self):
        # Do this test in timeout mode, because the code path is different
        self.cli_conn.settimeout(10)
        msg = self.cli_conn.recv(1024)
        self.assertEqual(msg, MSG)

    def _testRecvTimeoutMode(self):
        self.serv_conn.settimeout(10)
        self.serv_conn.send(MSG)

    def testOverFlowRecv(self):
        # Testing receive in chunks over TCP
        seg1 = self.cli_conn.recv(len(MSG) - 3)
        seg2 = self.cli_conn.recv(1024)
        msg = seg1 + seg2
        self.assertEqual(msg, MSG)

    def _testOverFlowRecv(self):
        self.serv_conn.send(MSG)

    def testRecvFrom(self):
        # Testing large recvfrom() over TCP
        msg, addr = self.cli_conn.recvfrom(1024)
        self.assertEqual(msg, MSG)

    def _testRecvFrom(self):
        self.serv_conn.send(MSG)

    def testOverFlowRecvFrom(self):
        # Testing recvfrom() in chunks over TCP
        seg1, addr = self.cli_conn.recvfrom(len(MSG)-3)
        seg2, addr = self.cli_conn.recvfrom(1024)
        msg = seg1 + seg2
        self.assertEqual(msg, MSG)

    def _testOverFlowRecvFrom(self):
        self.serv_conn.send(MSG)

    def testSendAll(self):
        # Testing sendall() with a 2048 byte string over TCP
        msg = ''
        while 1:
            read = self.cli_conn.recv(1024)
            if not read:
                break
            msg += read
        self.assertEqual(msg, 'f' * 2048)

    def _testSendAll(self):
        big_chunk = 'f' * 2048
        self.serv_conn.sendall(big_chunk)

    def testFromFd(self):
        # Testing fromfd()
        if not hasattr(socket, "fromfd"):
            return # On Windows or Jython, this doesn't exist
        fd = self.cli_conn.fileno()
        sock = socket.fromfd(fd, socket.AF_INET, socket.SOCK_STREAM)
        msg = sock.recv(1024)
        self.assertEqual(msg, MSG)

    def _testFromFd(self):
        self.serv_conn.send(MSG)

    def testShutdown(self):
        # Testing shutdown()
        msg = self.cli_conn.recv(1024)
        self.assertEqual(msg, MSG)

    def _testShutdown(self):
        self.serv_conn.send(MSG)
        self.serv_conn.shutdown(2)

    def testSendAfterRemoteClose(self):
        self.cli_conn.close()

    def _testSendAfterRemoteClose(self):
        for x in range(5):
            try:
                self.serv_conn.send("spam")
            except socket.error, se:
                self.failUnlessEqual(se[0], errno.ECONNRESET)
                return
            except Exception, x:
                self.fail("Sending on remotely closed socket raised wrong exception: %s" % x)
            time.sleep(0.5)
        self.fail("Sending on remotely closed socket should have raised exception")

    def testDup(self):
        msg = self.cli_conn.recv(len(MSG))
        self.assertEqual(msg, MSG)

        dup_conn = self.cli_conn.dup()
        msg = dup_conn.recv(len('and ' + MSG))
        self.assertEqual(msg, 'and ' +  MSG)
        dup_conn.close()  # need to ensure all sockets are closed

    def _testDup(self):
        self.serv_conn.send(MSG)
        self.serv_conn.send('and ' + MSG)

    def testSelect(self):
        # http://bugs.jython.org/issue2242
        self.assertIs(self.cli_conn.gettimeout(), None, "Server socket is not blocking")
        start_time = time.time()
        r, w, x = select.select([self.cli_conn], [], [], 10)
        if (time.time() - start_time) > 1:
            self.fail("Child socket was not immediately available for read when set to blocking")
        self.assertEqual(r[0], self.cli_conn)
        self.assertEqual(self.cli_conn.recv(1024), MSG)

    def _testSelect(self):
        self.serv_conn.send(MSG)


class UDPBindTest(unittest.TestCase):

    HOST = HOST
    PORT = PORT

    def setUp(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    def testBindSpecific(self):
        self.sock.bind( (self.HOST, self.PORT) ) # Use a specific port
        actual_port = self.sock.getsockname()[1]
        self.failUnless(actual_port == self.PORT,
            "Binding to specific port number should have returned same number: %d != %d" % (actual_port, self.PORT))

    def testBindEphemeral(self):
        self.sock.bind( (self.HOST, 0) ) # let system choose a free port
        self.failUnless(self.sock.getsockname()[1] != 0, "Binding to port zero should have allocated an ephemeral port number")

    def testShutdown(self):
        self.sock.bind( (self.HOST, self.PORT) )
        self.sock.shutdown(socket.SHUT_RDWR)

    def tearDown(self):
        self.sock.close()

class BasicUDPTest(ThreadedUDPSocketTest):

    def __init__(self, methodName='runTest'):
        ThreadedUDPSocketTest.__init__(self, methodName=methodName)

    def testSendtoAndRecv(self):
        # Testing sendto() and recv() over UDP
        msg = self.serv.recv(len(MSG))
        self.assertEqual(msg, MSG)

    def _testSendtoAndRecv(self):
        self.cli.sendto(MSG, 0, (self.HOST, self.PORT))

    def testSendtoAndRecvTimeoutMode(self):
        # Need to test again in timeout mode, which follows
        # a different code path
        self.serv.settimeout(1)
        msg = self.serv.recv(len(MSG))
        self.assertEqual(msg, MSG)

    def _testSendtoAndRecvTimeoutMode(self):
        self.cli.settimeout(10)
        self.cli.sendto(MSG, 0, (self.HOST, self.PORT))

    def testSendAndRecv(self):
        # Testing send() and recv() over connect'ed UDP
        msg = self.serv.recv(len(MSG))
        self.assertEqual(msg, MSG)

    def _testSendAndRecv(self):
        self.cli.connect( (self.HOST, self.PORT) )
        self.cli.send(MSG, 0)

    def testSendAndRecvTimeoutMode(self):
        # Need to test again in timeout mode, which follows
        # a different code path
        self.serv.settimeout(5)
        # Testing send() and recv() over connect'ed UDP
        msg = self.serv.recv(len(MSG))
        self.assertEqual(msg, MSG)

    def _testSendAndRecvTimeoutMode(self):
        self.cli.connect( (self.HOST, self.PORT) )
        self.cli.settimeout(5)
        time.sleep(1)
        self.cli.send(MSG, 0)

    def testRecvFrom(self):
        # Testing recvfrom() over UDP
        msg, addr = self.serv.recvfrom(len(MSG))
        self.assertEqual(msg, MSG)

    def _testRecvFrom(self):
        self.cli.sendto(MSG, 0, (self.HOST, self.PORT))

    def testRecvFromTimeoutMode(self):
        # Need to test again in timeout mode, which follows
        # a different code path
        self.serv.settimeout(1)
        msg, addr = self.serv.recvfrom(len(MSG))
        self.assertEqual(msg, MSG)

    def _testRecvFromTimeoutMode(self):
        self.cli.settimeout(1)
        self.cli.sendto(MSG, 0, (self.HOST, self.PORT))

    def testSendtoEightBitSafe(self):
        # This test is necessary because java only supports signed bytes
        msg = self.serv.recv(len(EIGHT_BIT_MSG))
        self.assertEqual(msg, EIGHT_BIT_MSG)

    def _testSendtoEightBitSafe(self):
        self.cli.sendto(EIGHT_BIT_MSG, 0, (self.HOST, self.PORT))

    def testSendtoEightBitSafeTimeoutMode(self):
        # Need to test again in timeout mode, which follows
        # a different code path
        self.serv.settimeout(10)
        msg = self.serv.recv(len(EIGHT_BIT_MSG))
        self.assertEqual(msg, EIGHT_BIT_MSG)

    def _testSendtoEightBitSafeTimeoutMode(self):
        self.cli.settimeout(10)
        self.cli.sendto(EIGHT_BIT_MSG, 0, (self.HOST, self.PORT))

class UDPBroadcastTest(ThreadedUDPSocketTest):

    def setUp(self):
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def testBroadcast(self):
        self.serv.bind( ("", self.PORT) )
        msg = self.serv.recv(len(EIGHT_BIT_MSG))
        self.assertEqual(msg, EIGHT_BIT_MSG)

    def _testBroadcast(self):
        self.cli.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.cli.sendto(EIGHT_BIT_MSG, ("<broadcast>", self.PORT) )

class BasicSocketPairTest(SocketPairTest):

    def __init__(self, methodName='runTest'):
        SocketPairTest.__init__(self, methodName=methodName)

    def testRecv(self):
        msg = self.serv.recv(1024)
        self.assertEqual(msg, MSG)

    def _testRecv(self):
        self.cli.send(MSG)

    def testSend(self):
        self.serv.send(MSG)

    def _testSend(self):
        msg = self.cli.recv(1024)
        self.assertEqual(msg, MSG)

class NonBlockingTCPServerTests(SocketTCPTest):

    def testSetBlocking(self):
        # Testing whether set blocking works
        self.serv.setblocking(0)
        start = time.time()
        try:
            self.serv.accept()
        except socket.error:
            pass
        end = time.time()
        self.assert_((end - start) < 1.0, "Error setting non-blocking mode.")

    def testAcceptNoConnection(self):
        # Testing non-blocking accept returns immediately when no connection
        self.serv.setblocking(0)
        try:
            conn, addr = self.serv.accept()
        except socket.error:
            pass
        else:
            self.fail("Error trying to do non-blocking accept.")

class NonBlockingTCPTests(ThreadedTCPSocketTest):

    def __init__(self, methodName='runTest'):
        ThreadedTCPSocketTest.__init__(self, methodName=methodName)

    def testAcceptConnection(self):
        # Testing non-blocking accept works when connection present
        self.serv.setblocking(0)

        # this can potentially race with the client, so we need to loop
        while True:
            read, write, err = select.select([self.serv], [], [], 0.1)
            if read or write or err:
                break
        if self.serv in read:
            conn, addr = self.serv.accept()
            conn.close()
        else:
            self.fail("Error trying to do accept after select: server socket was not in 'read'able list")

    def _testAcceptConnection(self):
        # Make a connection to the server
        self.cli.connect((self.HOST, self.PORT))
        time.sleep(1)

    def testBlockingConnect(self):
        # Testing blocking connect
        conn, addr = self.serv.accept()

    def _testBlockingConnect(self):
        # Testing blocking connect
        self.cli.settimeout(10)
        self.cli.connect((self.HOST, self.PORT))

    def testNonBlockingConnect(self):
        # Testing non-blocking connect
        # this can potentially race with the client, so we need to loop
        while True:
            read, write, err = select.select([self.serv], [], [], 0.1)
            if read or write or err:
                break
        if self.serv in read:
            conn, addr = self.serv.accept()
            conn.close()
        else:
            self.fail("Error trying to do accept after select: server socket was not in 'read'able list")

    def _testNonBlockingConnect(self):
        # Testing non-blocking connect
        time.sleep(0.1)
        self.cli.setblocking(0)
        result = self.cli.connect_ex((self.HOST, self.PORT))
        while True:
            rfds, wfds, xfds = select.select([self.cli], [self.cli], [], 0.1)
            if rfds or wfds or xfds:
                break
        try:
            self.cli.send(MSG)
        except socket.error:
            self.fail("Sending on connected socket should not have raised socket.error")

    def testConnectWithLocalBind(self):
        # Test blocking connect
        conn, addr = self.serv.accept()
        conn.close()  # Closing the server socket does not close this client socket

    def _testConnectWithLocalBind(self):
        # Testing blocking connect with local bind
        cli_port = self.PORT - 1
        start = time.time()
        while True:
            # Keep trying until a local port is available
            self.cli.settimeout(1)
            self.cli.bind( (self.HOST, cli_port) )
            try:
                self.cli.connect((self.HOST, self.PORT))
                break
            except socket.error, se:
                # cli_port is in use (maybe in TIME_WAIT state from a
                # previous test run). reset the client socket and try
                # again
                self.failUnlessEqual(se[0], errno.EADDRINUSE)
                print "Got an error in connect, will retry", se
                try:
                    self.cli.close()
                except socket.error:
                    pass
                self.clientSetUp()
                cli_port -= 1
            # Make sure we have no tests currently holding open this socket
            test_support.gc_collect()
            if time.time() - start > 5:
                self.fail("Timed out after 5 seconds")
        bound_host, bound_port = self.cli.getsockname()
        self.failUnlessEqual(bound_port, cli_port)

    def testRecvData(self):
        # Testing non-blocking recv
        conn, addr = self.serv.accept()  # server socket is blocking
        conn.setblocking(0)              # but now the child socket is not

        try:
            # this can potentially race with the client, so we need to loop
            while True:
                rfds, wfds, xfds = select.select([conn], [], [], 0.1)
                if rfds or wfds or xfds:
                    break

            if conn in rfds:
                msg = conn.recv(len(MSG))
                self.assertEqual(msg, MSG)
            else:
                self.fail("Non-blocking socket with data should been in read list.")
        finally:
            conn.close()

    def _testRecvData(self):
        self.cli.connect((self.HOST, self.PORT))
        self.cli.send(MSG)

    def testRecvNoData(self):
        # Testing non-blocking recv
        conn, addr = self.serv.accept()
        conn.setblocking(0)
        try:
            msg = conn.recv(len(MSG))
        except socket.error:
            pass
        else:
            self.fail("Non-blocking recv of no data should have raised socket.error.")
        finally:
            conn.close()

    def _testRecvNoData(self):
        self.cli.connect((self.HOST, self.PORT))
        time.sleep(1)  # Without a sleep, we may not see the connect, because the channel will be closed


class NonBlockingUDPTests(ThreadedUDPSocketTest): pass

#
# TODO: Write some non-blocking UDP tests
#

class TCPFileObjectClassOpenCloseTests(SocketConnectedTest):

    def testCloseFileDoesNotCloseSocket(self):
        # This test is necessary on java/jython
        msg = self.cli_conn.recv(1024)
        self.assertEqual(msg, MSG)

    def _testCloseFileDoesNotCloseSocket(self):
        self.cli_file = self.serv_conn.makefile('wb')
        self.cli_file.close()
        try:
            self.serv_conn.send(MSG)
        except Exception, x:
            self.fail("Closing file wrapper appears to have closed underlying socket: %s" % str(x))

    def testCloseSocketDoesNotCloseFile(self):
        msg = self.cli_conn.recv(1024)
        self.assertEqual(msg, MSG)

    def _testCloseSocketDoesNotCloseFile(self):
        self.cli_file = self.serv_conn.makefile('wb')
        self.serv_conn.close()
        try:
            self.cli_file.write(MSG)
            self.cli_file.flush()
        except Exception, x:
            self.fail("Closing socket appears to have closed file wrapper: %s" % str(x))

class UDPFileObjectClassOpenCloseTests(ThreadedUDPSocketTest):

    def testCloseFileDoesNotCloseSocket(self):
        # This test is necessary on java/jython
        msg = self.serv.recv(1024)
        self.assertEqual(msg, MSG)

    def _testCloseFileDoesNotCloseSocket(self):
        self.cli_file = self.cli.makefile('wb')
        self.cli_file.close()
        try:
            self.cli.sendto(MSG, 0, (self.HOST, self.PORT))
        except Exception, x:
            self.fail("Closing file wrapper appears to have closed underlying socket: %s" % str(x))

    def testCloseSocketDoesNotCloseFile(self):
        self.serv_file = self.serv.makefile('rb')
        self.serv.close()
        msg = self.serv_file.readline()
        self.assertEqual(msg, MSG)

    def _testCloseSocketDoesNotCloseFile(self):
        try:
            self.cli.sendto(MSG, 0, (self.HOST, self.PORT))
        except Exception, x:
            self.fail("Closing file wrapper appears to have closed underlying socket: %s" % str(x))

class FileAndDupOpenCloseTests(SocketConnectedTest):

    def testCloseDoesNotCloseOthers(self):
        msg = self.cli_conn.recv(len(MSG))
        self.assertEqual(msg, MSG)

        msg = self.cli_conn.recv(len('and ' + MSG))
        self.assertEqual(msg, 'and ' + MSG)

    def _testCloseDoesNotCloseOthers(self):
        self.dup_conn1 = self.serv_conn.dup()
        self.dup_conn2 = self.serv_conn.dup()
        self.cli_file = self.serv_conn.makefile('wb')
        self.serv_conn.close()
        self.dup_conn1.close()

        try:
            self.serv_conn.send(MSG)
        except socket.error, se:
            self.failUnlessEqual(se[0], errno.EBADF)
        else:
            self.fail("Original socket did not close")

        try:
            self.dup_conn1.send(MSG)
        except socket.error, se:
            self.failUnlessEqual(se[0], errno.EBADF)
        else:
            self.fail("Duplicate socket 1 did not close")

        self.dup_conn2.send(MSG)
        self.dup_conn2.close()

        try:
            self.cli_file.write('and ' + MSG)
        except Exception, x:
            self.fail("Closing others appears to have closed the socket file: %s" % str(x))
        self.cli_file.close()

class FileObjectClassTestCase(SocketConnectedTest):

    bufsize = -1 # Use default buffer size

    def __init__(self, methodName='runTest'):
        SocketConnectedTest.__init__(self, methodName=methodName)

    def setUp(self):
        SocketConnectedTest.setUp(self)
        self.serv_file = self.cli_conn.makefile('rb', self.bufsize)

    def tearDown(self):
        self.serv_file.close()
        self.assert_(self.serv_file.closed)
        self.serv_file = None
        SocketConnectedTest.tearDown(self)

    def clientSetUp(self):
        SocketConnectedTest.clientSetUp(self)
        self.cli_file = self.serv_conn.makefile('wb')

    def clientTearDown(self):
        self.cli_file.close()
        self.assert_(self.cli_file.closed)
        self.cli_file = None
        SocketConnectedTest.clientTearDown(self)

    def testSmallRead(self):
        # Performing small file read test
        first_seg = self.serv_file.read(len(MSG)-3)
        second_seg = self.serv_file.read(3)
        msg = first_seg + second_seg
        self.assertEqual(msg, MSG)

    def _testSmallRead(self):
        self.cli_file.write(MSG)
        self.cli_file.flush()

    def testFullRead(self):
        # read until EOF
        msg = self.serv_file.read()
        self.assertEqual(msg, MSG)

    def _testFullRead(self):
        self.cli_file.write(MSG)
        self.cli_file.flush()

    def testUnbufferedRead(self):
        # Performing unbuffered file read test
        buf = ''
        while 1:
            char = self.serv_file.read(1)
            if not char:
                break
            buf += char
        self.assertEqual(buf, MSG)

    def _testUnbufferedRead(self):
        self.cli_file.write(MSG)
        self.cli_file.flush()

    def testReadline(self):
        # Performing file readline test
        line = self.serv_file.readline()
        self.assertEqual(line, MSG)

    def _testReadline(self):
        self.cli_file.write(MSG)
        self.cli_file.flush()

    def testClosedAttr(self):
        self.assert_(not self.serv_file.closed)
        
    def _testClosedAttr(self):
        self.assert_(not self.cli_file.closed)

class PrivateFileObjectTestCase(unittest.TestCase):

    """Test usage of socket._fileobject with an arbitrary socket-like
    object.

    E.g. urllib2 wraps an httplib.HTTPResponse object with _fileobject.
    """

    def setUp(self):
        self.socket_like = StringIO()
        self.socket_like.recv = self.socket_like.read
        self.socket_like.sendall = self.socket_like.write

    def testPrivateFileObject(self):
        fileobject = socket._fileobject(self.socket_like, 'rb')
        fileobject.write('hello jython')
        fileobject.flush()
        self.socket_like.seek(0)
        self.assertEqual(fileobject.read(), 'hello jython')

class UnbufferedFileObjectClassTestCase(FileObjectClassTestCase):

    """Repeat the tests from FileObjectClassTestCase with bufsize==0.

    In this case (and in this case only), it should be possible to
    create a file object, read a line from it, create another file
    object, read another line from it, without loss of data in the
    first file object's buffer.  Note that httplib relies on this
    when reading multiple requests from the same socket."""

    bufsize = 0 # Use unbuffered mode

    def testUnbufferedReadline(self):
        # Read a line, create a new file object, read another line with it
        line = self.serv_file.readline() # first line
        self.assertEqual(line, "A. " + MSG) # first line
        self.serv_file = self.cli_conn.makefile('rb', 0)
        line = self.serv_file.readline() # second line
        self.assertEqual(line, "B. " + MSG) # second line

    def _testUnbufferedReadline(self):
        self.cli_file.write("A. " + MSG)
        self.cli_file.write("B. " + MSG)
        self.cli_file.flush()

class LineBufferedFileObjectClassTestCase(FileObjectClassTestCase):

    bufsize = 1 # Default-buffered for reading; line-buffered for writing


class SmallBufferedFileObjectClassTestCase(FileObjectClassTestCase):

    bufsize = 2 # Exercise the buffering code

class TCPServerTimeoutTest(SocketTCPTest):

    def testAcceptTimeout(self):
        def raise_timeout(*args, **kwargs):
            self.serv.settimeout(1.0)
            self.serv.accept()
        self.failUnlessRaises(socket.timeout, raise_timeout,
                              "TCP socket accept failed to generate a timeout exception (TCP)")

    def testTimeoutZero(self):
        ok = False
        try:
            self.serv.settimeout(0.0)
            foo = self.serv.accept()
        except socket.timeout:
            self.fail("caught timeout instead of error (TCP)")
        except socket.error:
            ok = True
        except Exception, x:
            self.fail("caught unexpected exception (TCP): %s" % str(x))
        if not ok:
            self.fail("accept() returned success when we did not expect it")

class TCPClientTimeoutTest(SocketTCPTest):

    def testConnectTimeout(self):
        cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cli.settimeout(0.1)
        host = '192.0.2.42'  # address in TEST-NET-1, guaranteed to not be routeable
        try:
            cli.connect((host, 5000))
        except socket.timeout, st:
            pass
        except Exception, x:
            self.fail("Client socket timeout should have raised socket.timeout, not %s" % str(x))
        else:
            self.fail('''Client socket timeout should have raised
socket.timeout.  This tries to connect to %s in the assumption that it isn't
used, but if it is on your network this failure is bogus.''' % host)

    def testConnectDefaultTimeout(self):
        _saved_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(0.1)
        cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '192.0.2.42'  # address in TEST-NET-1, guaranteed to not be routeable
        try:
            cli.connect((host, 5000))
        except socket.timeout, st:
            pass
        except Exception, x:
            self.fail("Client socket timeout should have raised socket.timeout, not %s" % str(x))
        else:
            self.fail('''Client socket timeout should have raised
socket.timeout.  This tries to connect to %s in the assumption that it isn't
used, but if it is on your network this failure is bogus.''' % host)
        finally:
            socket.setdefaulttimeout(_saved_timeout)

    def testRecvTimeout(self):
        def raise_timeout(*args, **kwargs):
            cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cli_sock.connect( (self.HOST, self.PORT) )
            cli_sock.settimeout(1)
            cli_sock.recv(1024)
        self.failUnlessRaises(socket.timeout, raise_timeout,
                              "TCP socket recv failed to generate a timeout exception (TCP)")

    @unittest.skipIf(test_support.is_jython, "This test takes a very long time")
    def testSendTimeout(self):
        def raise_timeout(*args, **kwargs):
            cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cli_sock.connect( (self.HOST, self.PORT) )
            # First fill the socket
            cli_sock.settimeout(1)
            sent = 0
            while True:
                bytes_sent = cli_sock.send(MSG)
                sent += bytes_sent
        self.failUnlessRaises(socket.timeout, raise_timeout,
                              "TCP socket send failed to generate a timeout exception (TCP)")

    def testSwitchModes(self):
        cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cli_sock.connect( (self.HOST, self.PORT) )
        # set non-blocking mode
        cli_sock.setblocking(0)
        # then set timeout mode
        cli_sock.settimeout(1)
        try:
            cli_sock.send(MSG)
        except Exception, x:
            self.fail("Switching mode from non-blocking to timeout raised exception: %s" % x)
        else:
            pass

class UDPTimeoutTest(SocketUDPTest):

    def testUDPTimeout(self):
        def raise_timeout(*args, **kwargs):
            self.serv.settimeout(1.0)
            self.serv.recv(1024)
        self.failUnlessRaises(socket.timeout, raise_timeout,
                              "Error generating a timeout exception (UDP)")

    def testTimeoutZero(self):
        ok = False
        try:
            self.serv.settimeout(0.0)
            foo = self.serv.recv(1024)
        except socket.timeout:
            self.fail("caught timeout instead of error (UDP)")
        except socket.error:
            ok = True
        except Exception, x:
            self.fail("caught unexpected exception (UDP): %s" % str(x))
        if not ok:
            self.fail("recv() returned success when we did not expect it")

class TestGetAddrInfo(unittest.TestCase):

    def testBadFamily(self):
        try:
            socket.getaddrinfo(HOST, PORT, 9999)
        except socket.gaierror, gaix:
            self.failUnlessEqual(gaix[0], errno.EIO)
        except Exception, x:
            self.fail("getaddrinfo with bad family raised wrong exception: %s" % x)
        else:
            self.fail("getaddrinfo with bad family should have raised exception")

    def testBadSockType(self):
        for socktype in [socket.SOCK_RAW, socket.SOCK_RDM, socket.SOCK_SEQPACKET]:
            try:
                socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socktype)
            except socket.error, se:
                self.failUnlessEqual(se[0], errno.ESOCKTNOSUPPORT)
            except Exception, x:
                self.fail("getaddrinfo with bad socktype raised wrong exception: %s" % x)
            else:
                self.fail("getaddrinfo with bad socktype should have raised exception")

    def testBadSockTypeProtoCombination(self):
        for socktype, proto in [
            (socket.SOCK_STREAM, socket.IPPROTO_UDP),
            (socket.SOCK_STREAM, socket.IPPROTO_ICMP),
            (socket.SOCK_DGRAM,  socket.IPPROTO_TCP),
            (socket.SOCK_DGRAM,  socket.IPPROTO_FRAGMENT),
            ]:
            try:
                results = socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socktype, proto)
                self.failUnless(len(results) == 0, "getaddrinfo with bad socktype/proto combo should not have returned results")
            except Exception, x:
                self.fail("getaddrinfo with bad socktype/proto combo should not have raised exception")

    def testNoSockTypeWithProto(self):
        for expect_results, proto in [
            (True,  socket.IPPROTO_UDP),
            (False, socket.IPPROTO_ICMP),
            (True,  socket.IPPROTO_TCP),
            (False, socket.IPPROTO_FRAGMENT),
            ]:
            try:
                results = socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, 0, proto)
                if expect_results:
                    self.failUnless(len(results) > 0, "getaddrinfo with no socktype and supported proto combo should have returned results")
                else:
                    self.failUnless(len(results) == 0, "getaddrinfo with no socktype and unsupported proto combo should not have returned results")
            except Exception, x:
                self.fail("getaddrinfo with no socktype (un)supported proto combo should not have raised exception")

    def testReturnsAreStrings(self):
        addrinfos = socket.getaddrinfo(HOST, PORT)
        for addrinfo in addrinfos:
            family, socktype, proto, canonname, sockaddr = addrinfo
            self.assert_(isinstance(canonname, str))
            self.assert_(isinstance(sockaddr[0], str))

    def testSockAddrAsTuple(self):
        family, socktype, proto, canonname, sockaddr = socket.getaddrinfo(HOST, PORT, socket.AF_INET, socket.SOCK_STREAM)[0]
        self.assertEqual(len(sockaddr), 2)
        self.assertEqual(sockaddr[-1], PORT)
        self.assertEqual(sockaddr[:2], ('127.0.0.1', PORT))

        family, socktype, proto, canonname, sockaddr = socket.getaddrinfo('::1', PORT, socket.AF_INET6, socket.SOCK_STREAM)[0]
        self.assertEqual(len(sockaddr), 4)
        self.assertEqual(sockaddr[-3], PORT)
        #self.assertEqual(sockaddr[:2], ('::1', PORT))      # FIXME: Got '0:0:...:1' instead!

    def testAI_PASSIVE(self):
        # Disabling this test for now; it's expectations are not portable.
        # Expected results are too dependent on system config to be made portable between systems.
        # And the only way to determine what configuration to test is to use the 
        # java.net.InetAddress.getAllByName() method, which is what is used to 
        # implement the getaddrinfo() function. Therefore, no real point in the test.
        return
        IPV4_LOOPBACK = "127.0.0.1"
        local_hostname = java.net.InetAddress.getLocalHost().getHostName()
        local_ip_address = java.net.InetAddress.getLocalHost().getHostAddress()
        for flags, host_param, expected_canonname, expected_sockaddr in [
            # First passive flag
            (socket.AI_PASSIVE, None, "", socket.INADDR_ANY),
            (socket.AI_PASSIVE, "", "", local_ip_address),
            (socket.AI_PASSIVE, "localhost", "", IPV4_LOOPBACK),
            (socket.AI_PASSIVE, local_hostname, "", local_ip_address),
            # Now passive flag AND canonname flag
            # Commenting out all AI_CANONNAME tests, results too dependent on system config
            #(socket.AI_PASSIVE|socket.AI_CANONNAME, None, "127.0.0.1", "127.0.0.1"),
            #(socket.AI_PASSIVE|socket.AI_CANONNAME, "", local_hostname, local_ip_address),
            # The following gives varying results across platforms and configurations: commenting out for now.
            # Javadoc: http://java.sun.com/j2se/1.5.0/docs/api/java/net/InetAddress.html#getCanonicalHostName()
            #(socket.AI_PASSIVE|socket.AI_CANONNAME, "localhost", local_hostname, IPV4_LOOPBACK),
            #(socket.AI_PASSIVE|socket.AI_CANONNAME, local_hostname, local_hostname, local_ip_address),
        ]:
            addrinfos = socket.getaddrinfo(host_param, 0, socket.AF_INET, socket.SOCK_STREAM, 0, flags)
            for family, socktype, proto, canonname, sockaddr in addrinfos:
                self.failUnlessEqual(expected_canonname, canonname, "For hostname '%s' and flags %d, canonname '%s' != '%s'" % (host_param, flags, expected_canonname, canonname) )
                self.failUnlessEqual(expected_sockaddr, sockaddr[0], "For hostname '%s' and flags %d, sockaddr '%s' != '%s'" % (host_param, flags, expected_sockaddr, sockaddr[0]) )

    def testAddrTupleTypes(self):
        ipv4_address_tuple = socket.getaddrinfo("localhost", 80, socket.AF_INET, socket.SOCK_STREAM, 0, 0)[0][4]
        self.failUnlessEqual(ipv4_address_tuple[0], "127.0.0.1")
        self.failUnlessEqual(ipv4_address_tuple[1], 80)
        self.failUnlessRaises(IndexError, lambda: ipv4_address_tuple[2])
        self.failUnlessEqual(str(ipv4_address_tuple), "('127.0.0.1', 80)")
        self.failUnlessEqual(repr(ipv4_address_tuple), "('127.0.0.1', 80)")

        addrinfo = socket.getaddrinfo("localhost", 80, socket.AF_INET6, socket.SOCK_STREAM, 0, 0)
        if not addrinfo:
            # Maybe no IPv6 configured on the test machine.
            return
        ipv6_address_tuple = addrinfo[0][4]
        self.assertIn(ipv6_address_tuple[0], ["::1", "0:0:0:0:0:0:0:1"])
        self.failUnlessEqual(ipv6_address_tuple[1], 80)
        self.failUnlessEqual(ipv6_address_tuple[2], 0)
        # Can't have an expectation for scope
        try:
            ipv6_address_tuple[3]
        except IndexError:
            self.fail("Failed to retrieve third element of ipv6 4-tuple")
        self.failUnlessRaises(IndexError, lambda: ipv6_address_tuple[4])
        # These str/repr tests may fail on some systems: the scope element of the tuple may be non-zero
        # In this case, we'll have to change the test to use .startswith() or .split() to exclude the scope element
        self.assertIn(str(ipv6_address_tuple), ["('::1', 80, 0, 0)", "('0:0:0:0:0:0:0:1', 80, 0, 0)"])
        self.assertIn(repr(ipv6_address_tuple), ["('::1', 80, 0, 0)", "('0:0:0:0:0:0:0:1', 80, 0, 0)"])

    def testNonIntPort(self):
        hostname = "localhost"

        # Port value of None should map to 0
        addrs = socket.getaddrinfo(hostname, None)
        for a in addrs:
            self.failUnlessEqual(a[4][1], 0, "Port value of None should have returned 0")

        # Port value can be a string rep of the port number
        addrs = socket.getaddrinfo(hostname, "80")
        for a in addrs:
            self.failUnlessEqual(a[4][1], 80, "Port value of '80' should have returned 80")

        # Can also specify a service name
        # This test assumes that service http will always be at port 80
        addrs = socket.getaddrinfo(hostname, "http")
        for a in addrs:
            self.failUnlessEqual(a[4][1], 80, "Port value of 'http' should have returned 80")

        # Check treatment of non-integer numeric port
        try:
            socket.getaddrinfo(hostname, 79.99)
        except socket.error, se:
            self.failUnlessEqual(se[0], "Int or String expected")
        except Exception, x:
            self.fail("getaddrinfo for float port number raised wrong exception: %s" % str(x))
        else:
            self.fail("getaddrinfo for float port number failed to raise exception")

        # Check treatment of non-integer numeric port, as a string
        # The result is that it should fail in the same way as a non-existent service
        try:
            socket.getaddrinfo(hostname, "79.99")
        except socket.gaierror, g:
            self.failUnlessEqual(g[0], socket.EAI_SERVICE)
        except Exception, x:
            self.fail("getaddrinfo for non-integer numeric port, as a string raised wrong exception: %s" % str(x))
        else:
            self.fail("getaddrinfo for non-integer numeric port, as a string failed to raise exception")

        # Check enforcement of AI_NUMERICSERV
        try:
            socket.getaddrinfo(hostname, "http", 0, 0, 0, socket.AI_NUMERICSERV)
        except socket.gaierror, g:
            self.failUnlessEqual(g[0], socket.EAI_NONAME)
        except Exception, x:
            self.fail("getaddrinfo for service name with AI_NUMERICSERV raised wrong exception: %s" % str(x))
        else:
            self.fail("getaddrinfo for service name with AI_NUMERICSERV failed to raise exception")

        # Check treatment of non-existent service
        try:
            socket.getaddrinfo(hostname, "nosuchservice")
        except socket.gaierror, g:
            self.failUnlessEqual(g[0], socket.EAI_SERVICE)
        except Exception, x:
            self.fail("getaddrinfo for unknown service name raised wrong exception: %s" % str(x))
        else:
            self.fail("getaddrinfo for unknown service name failed to raise exception")

    def testHostNames(self):
        # None is only acceptable if AI_NUMERICHOST is not specified
        for flags, expect_exception in [(0, False), (socket.AI_NUMERICHOST, True)]:
            try:
                socket.getaddrinfo(None, 80, 0, 0, 0, flags)
                if expect_exception:
                    self.fail("Non-numeric hostname == None should have raised exception")
            except Exception, x:
                if not expect_exception:
                    self.fail("hostname == None should not have raised exception: %s" % str(x))

        # Check enforcement of AI_NUMERICHOST
        for host in ["", " ", "localhost"]:
            try:
                socket.getaddrinfo(host, 80, 0, 0, 0, socket.AI_NUMERICHOST)
            except socket.gaierror, ge:
                self.failUnlessEqual(ge[0], socket.EAI_NONAME)
            except Exception, x:
                self.fail("Non-numeric host with AI_NUMERICHOST raised wrong exception: %s" % str(x))
            else:
                self.fail("Non-numeric hostname '%s' with AI_NUMERICHOST should have raised exception" % host)

        # Check enforcement of AI_NUMERICHOST with wrong address families
        for host, family in [("127.0.0.1", socket.AF_INET6), ("::1", socket.AF_INET)]:
            try:
                socket.getaddrinfo(host, 80, family, 0, 0, socket.AI_NUMERICHOST)
            except socket.gaierror, ge:
                self.failUnlessEqual(ge[0], socket.EAI_ADDRFAMILY)
            except Exception, x:
                self.fail("Numeric host '%s' in wrong family '%s' with AI_NUMERICHOST raised wrong exception: %s" % 
                    (host, family, str(x)) )
            else:
                self.fail("Numeric host '%s' in wrong family '%s' with AI_NUMERICHOST should have raised exception" % 
                    (host, family) )

class TestGetNameInfo(unittest.TestCase):

    def testBadParameters(self):
        for address, flags in [
            ( (0,0),       0),
            ( (0,"http"),  0),
            ( "localhost", 0),
            ( 0,           0),
            ( ("",),       0),
        ]:
            try:
                socket.getnameinfo(address, flags)
            except TypeError:
                pass
            except Exception, x:
                self.fail("Bad getnameinfo parameters (%s, %s) raised wrong exception: %s" % (str(address), flags, str(x)))
            else:
                self.fail("Bad getnameinfo parameters (%s, %s) failed to raise exception" % (str(address), flags))

    def testPort(self):
        for address, flags, expected in [
            ( ("127.0.0.1", 25),  0,                     "smtp" ),
            ( ("127.0.0.1", 25),  socket.NI_NUMERICSERV, 25     ),

            # This portion of the test does not suceed on OS X;
            # the above entries probably suffice
            # ( ("127.0.0.1", 513), socket.NI_DGRAM,       "who"  ),
            # ( ("127.0.0.1", 513), 0,                     "login"),
        ]:
            result = socket.getnameinfo(address, flags)
            self.failUnlessEqual(result[1], expected)


    # This test currently fails due to the recent changes (as of March 2014) at python.org:
    # TBD perhaps there are well-known addresses that guarantee stable resolution

    # def testHost(self):
    #     for address, flags, expected in [
    #         ( ("www.python.org", 80),  0,                     "dinsdale.python.org"),
    #         ( ("www.python.org", 80),  socket.NI_NUMERICHOST, "82.94.164.162"      ),
    #         ( ("www.python.org", 80),  socket.NI_NAMEREQD,    "dinsdale.python.org"),
    #         ( ("82.94.164.162",  80),  socket.NI_NAMEREQD,    "dinsdale.python.org"),
    #     ]:
    #         result = socket.getnameinfo(address, flags)
    #         self.failUnlessEqual(result[0], expected)

    def testNI_NAMEREQD(self):
        # This test may delay for some seconds
        unreversible_address = "198.51.100.1"
        try:
            socket.getnameinfo( (unreversible_address, 80), socket.NI_NAMEREQD)
        except socket.gaierror, ge:
            self.failUnlessEqual(ge[0], socket.EAI_NONAME)
        except Exception, x:
            self.fail("Unreversible address with NI_NAMEREQD (%s) raised wrong exception: %s" % (unreversible_address, str(x)))
        else:
            self.fail("Unreversible address with NI_NAMEREQD (%s) failed to raise exception" % unreversible_address)

    def testHostIdna(self):
        fqdn = u"\u043f\u0440\u0430\u0432\u0438\u0442\u0435\u043b\u044c\u0441\u0442\u0432\u043e.\u0440\u0444"
        idn  = "xn--80aealotwbjpid2k.xn--p1ai"
        ip   = "95.173.135.62"
        try:
            import java.net.IDN
        except ImportError:
            try:
                socket.getnameinfo( (fqdn, 80), 0)
            except UnicodeEncodeError:
                pass
            except Exception, x:
                self.fail("International domain without java.net.IDN raised wrong exception: %s" % str(x))
            else:
                self.fail("International domain without java.net.IDN failed to raise exception")
        else:
            # have to disable this test until I find an IDN that reverses to the punycode name
            return
            for address, flags, expected in [
                ( (fqdn, 80),  0,             idn  ),
                ( (fqdn, 80),  socket.NI_IDN, fqdn ),
            ]:
                result = socket.getnameinfo(address, flags)
                self.failUnlessEqual(result[0], expected)


# TODO: consider re-enabling this set of tests, but for now
# this set reliably does *not* work on Ubuntu (but does on
# OSX). However the underlying internal method _get_jsockaddr
# is exercised by nearly every socket usage, along with the
# corresponding tests.

@unittest.skipIf(test_support.is_jython, "Skip internal tests for address lookup due to underlying OS issues")
class TestJython_get_jsockaddr(unittest.TestCase):
    "These tests are specific to jython: they test a key internal routine"

    def testIPV4AddressesFromGetAddrInfo(self):
        local_addr = socket.getaddrinfo("localhost", 80, socket.AF_INET, socket.SOCK_STREAM, 0, 0)[0][4]
        sockaddr = socket._get_jsockaddr(local_addr, socket.AF_INET, None, 0, 0)
        self.failUnless(isinstance(sockaddr, java.net.InetSocketAddress), "_get_jsockaddr returned wrong type: '%s'" % str(type(sockaddr)))
        self.failUnlessEqual(sockaddr.address.hostAddress, "127.0.0.1")
        self.failUnlessEqual(sockaddr.port, 80)

    def testIPV6AddressesFromGetAddrInfo(self):
        addrinfo = socket.getaddrinfo("localhost", 80, socket.AF_INET6, socket.SOCK_STREAM, 0, 0)
        if not addrinfo and is_bsd:
            # older FreeBSDs may have spotty IPV6 Java support
            return
        local_addr = addrinfo[0][4]
        sockaddr = socket._get_jsockaddr(local_addr, socket.AF_INET6, None, 0, 0)
        self.failUnless(isinstance(sockaddr, java.net.InetSocketAddress), "_get_jsockaddr returned wrong type: '%s'" % str(type(sockaddr)))
        self.failUnless(sockaddr.address.hostAddress in ["::1", "0:0:0:0:0:0:0:1"])
        self.failUnlessEqual(sockaddr.port, 80)

    def testAddressesFrom2Tuple(self):
        for family, addr_tuple, jaddress_type, expected in [
            (socket.AF_INET,  ("localhost", 80), java.net.Inet4Address, ["127.0.0.1"]),
            (socket.AF_INET6, ("localhost", 80), java.net.Inet6Address, ["::1", "0:0:0:0:0:0:0:1"]),
            ]:
            sockaddr = socket._get_jsockaddr(addr_tuple, family, 0, 0, 0)
            self.failUnless(isinstance(sockaddr, java.net.InetSocketAddress), "_get_jsockaddr returned wrong type: '%s'" % str(type(sockaddr)))
            self.failUnless(isinstance(sockaddr.address, jaddress_type), "_get_jsockaddr returned wrong address type: '%s'(family=%d)" % (str(type(sockaddr.address)), family))
            self.failUnless(sockaddr.address.hostAddress in expected)
            self.failUnlessEqual(sockaddr.port, 80)

    def testAddressesFrom4Tuple(self):
        for addr_tuple in [
            ("localhost", 80),
            ("localhost", 80, 0, 0),
            ]:
            sockaddr = socket._get_jsockaddr(addr_tuple, socket.AF_INET6, 0, 0, 0)
            self.failUnless(isinstance(sockaddr, java.net.InetSocketAddress), "_get_jsockaddr returned wrong type: '%s'" % str(type(sockaddr)))
            self.failUnless(isinstance(sockaddr.address, java.net.Inet6Address), "_get_jsockaddr returned wrong address type: '%s'" % str(type(sockaddr.address)))
            self.failUnless(sockaddr.address.hostAddress in ["::1", "0:0:0:0:0:0:0:1"])
            self.failUnlessEqual(sockaddr.address.scopeId, 0)
            self.failUnlessEqual(sockaddr.port, 80)

    def testSpecialHostnames(self):
        for family, sock_type, flags, addr_tuple, expected in [
            ( socket.AF_INET,  0,                 0,                 ("", 80),            ["localhost"]),
            ( socket.AF_INET,  0,                 socket.AI_PASSIVE, ("", 80),            [socket.INADDR_ANY]),
            ( socket.AF_INET6, 0,                 0,                 ("", 80),            ["localhost"]),
            ( socket.AF_INET6, 0,                 socket.AI_PASSIVE, ("", 80),            [socket.IN6ADDR_ANY_INIT, "0:0:0:0:0:0:0:0"]),
            ( socket.AF_INET,  socket.SOCK_DGRAM, 0,                 ("<broadcast>", 80), ["broadcasthost"]),
            ]:
            sockaddr = socket._get_jsockaddr(addr_tuple, family, sock_type, 0, flags)
            self.failUnless(sockaddr.hostName in expected, "_get_jsockaddr returned wrong hostname '%s' for special hostname '%s'(family=%d)" % (sockaddr.hostName, addr_tuple[0], family))

    def testNoneTo_get_jsockaddr(self):
        for family, flags, expected in [
            ( socket.AF_INET,  0,                 ["localhost"]),
            ( socket.AF_INET,  socket.AI_PASSIVE, [socket.INADDR_ANY]),
            ( socket.AF_INET6, 0,                 ["localhost"]),
            ( socket.AF_INET6, socket.AI_PASSIVE, [socket.IN6ADDR_ANY_INIT, "0:0:0:0:0:0:0:0"]),
            ]:
            sockaddr = socket._get_jsockaddr(None, family, 0, 0, flags)
            self.failUnless(sockaddr.hostName in expected, "_get_jsockaddr returned wrong hostname '%s' for sock tuple == None (family=%d)" % (sockaddr.hostName, family))

    def testBadAddressTuples(self):
        for family, address_tuple in [
            ( socket.AF_INET,  ()                      ),
            ( socket.AF_INET,  ("")                    ),
            ( socket.AF_INET,  (80)                    ),
            ( socket.AF_INET,  ("localhost", 80, 0)    ),
            ( socket.AF_INET,  ("localhost", 80, 0, 0) ),
            ( socket.AF_INET6,  ()                      ),
            ( socket.AF_INET6,  ("")                    ),
            ( socket.AF_INET6,  (80)                    ),
            ( socket.AF_INET6,  ("localhost", 80, 0)    ),
            ]:
            try:
                sockaddr = socket._get_jsockaddr(address_tuple, family, None, 0, 0)
            except TypeError:
                pass
            else:
                self.fail("Bad tuple %s (family=%d) should have raised TypeError" % (str(address_tuple), family))

class TestExceptions(unittest.TestCase):

    def testExceptionTree(self):
        self.assert_(issubclass(socket.error, IOError))
        self.assert_(issubclass(socket.herror, socket.error))
        self.assert_(issubclass(socket.gaierror, socket.error))
        self.assert_(issubclass(socket.timeout, socket.error))

    def testExceptionAtributes(self):
        for exc_class_name in ['error', 'herror', 'gaierror', 'timeout']:
            exc_class = getattr(socket, exc_class_name)
            exc = exc_class(12345, "Expected message")
            self.failUnlessEqual(getattr(exc, 'errno'), 12345, "Socket module exceptions must have an 'errno' attribute")
            self.failUnlessEqual(getattr(exc, 'strerror'), "Expected message", "Socket module exceptions must have an 'strerror' attribute")

class TestJythonExceptionsShared:

    def tearDown(self):
        self.s.close()
        self.s = None

    def testHostNotFound(self):
        try:
            socket.gethostbyname("doesnotexist")
        except socket.gaierror, gaix:
            self.failUnlessEqual(gaix[0], errno.EGETADDRINFOFAILED)
        except Exception, x:
            self.fail("Get host name for non-existent host raised wrong exception: %s" % x)

    def testUnresolvedAddress(self):
        try:
            self.s.connect( ('non.existent.server', PORT) )
        except socket.gaierror, gaix:
            self.failUnlessEqual(gaix[0], errno.ENOEXEC)
        except Exception, x:
            self.fail("Get host name for non-existent host raised wrong exception: %s" % x)
        else:
            self.fail("Get host name for non-existent host should have raised exception")

    def testSocketNotConnected(self):
        try:
            self.s.send(MSG)
        except socket.error, se:
            self.failUnlessEqual(se[0], errno.ENOTCONN)
        except Exception, x:
            self.fail("Send on unconnected socket raised wrong exception: %s" % x)
        else:
            self.fail("Send on unconnected socket raised exception")

    def testClosedSocket(self):
        self.s.close()
        try:
            self.s.send(MSG)
        except socket.error, se:
            self.failUnlessEqual(se[0], errno.EBADF)

        dup = self.s.dup()
        try:
            dup.send(MSG)
        except socket.error, se:
            self.failUnlessEqual(se[0], errno.EBADF)

        fp = self.s.makefile()
        try:
            fp.write(MSG)
            fp.flush()
        except socket.error, se:
            self.failUnlessEqual(se[0], errno.EBADF)

class TestJythonTCPExceptions(TestJythonExceptionsShared, unittest.TestCase):

    def setUp(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def testConnectionRefused(self):
        try:
            # This port should not be open at this time
            self.s.connect( (HOST, PORT) )
        except socket.error, se:
            self.failUnlessEqual(se[0], errno.ECONNREFUSED)
        except Exception, x:
            self.fail("Connection to non-existent host/port raised wrong exception: %s" % x)
        else:
            self.fail("Socket (%s,%s) should not have been listening at this time" % (HOST, PORT))

    def testBindException(self):
        # First bind to the target port
        self.s.bind( (HOST, PORT) )
        self.s.listen(50)
        try:
            # And then try to bind again
            t = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            t.bind( (HOST, PORT) )
            t.listen(50)
        except socket.error, se:
            self.failUnlessEqual(se[0], errno.EADDRINUSE)
        except Exception, x:
            self.fail("Binding to already bound host/port raised wrong exception: %s" % x)
        else:
            self.fail("Binding to already bound host/port should have raised exception")

    def testSocketNotBound(self):
        try:
            result = self.s.recv(1024)
        except socket.error, se:
            self.failUnlessEqual(se[0], errno.ENOTCONN)
        except Exception, x:
            self.fail("Receive on unbound socket raised wrong exception: %s" % x)
        else:
            self.fail("Receive on unbound socket raised exception")


class TestJythonUDPExceptions(TestJythonExceptionsShared, unittest.TestCase):

    def setUp(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def testBindException(self):
        # First bind to the target port
        self.s.bind( (HOST, PORT) )
        try:
            # And then try to bind again
            t = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            t.bind( (HOST, PORT) )
        except socket.error, se:
            self.failUnlessEqual(se[0], errno.EADDRINUSE)
        except Exception, x:
            self.fail("Binding to already bound host/port raised wrong exception: %s" % x)
        else:
            self.fail("Binding to already bound host/port should have raised exception")

class TestAddressParameters:

    def testBindNonTupleEndpointRaisesTypeError(self):
        try:
            self.socket.bind(HOST, PORT)
        except TypeError:
            pass
        else:
            self.fail("Illegal non-tuple bind address did not raise TypeError")

    def testConnectNonTupleEndpointRaisesTypeError(self):
        try:
            self.socket.connect(HOST, PORT)
        except TypeError:
            pass
        else:
            self.fail("Illegal non-tuple connect address did not raise TypeError")

    def testConnectExNonTupleEndpointRaisesTypeError(self):
        try:
            self.socket.connect_ex(HOST, PORT)
        except TypeError:
            pass
        else:
            self.fail("Illegal non-tuple connect address did not raise TypeError")

class TestTCPAddressParameters(unittest.TestCase, TestAddressParameters):

    def setUp(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class TestUDPAddressParameters(unittest.TestCase, TestAddressParameters):

    def setUp(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class UnicodeTest(ThreadedTCPSocketTest):

    def testUnicodeHostname(self):
        pass

    def _testUnicodeHostname(self):
        self.cli.connect((unicode(self.HOST), self.PORT))

class IDNATest(unittest.TestCase):

    def testGetAddrInfoIDNAHostname(self):
        idna_domain = u"al\u00e1n.com"
        if socket.supports('idna'):
            try:
                addresses = socket.getaddrinfo(idna_domain, 80)
                self.failUnless(len(addresses) > 0, "No addresses returned for test IDNA domain '%s'" % repr(idna_domain))
            except Exception, x:
                self.fail("Unexpected exception raised for socket.getaddrinfo(%s)" % repr(idna_domain))
        else:
            try:
                socket.getaddrinfo(idna_domain, 80)
            except UnicodeEncodeError:
                pass
            except Exception, x:
                self.fail("Non ascii domain '%s' should have raised UnicodeEncodeError, not %s" % (repr(idna_domain), str(x)))
            else:
                self.fail("Non ascii domain '%s' should have raised UnicodeEncodeError: no exception raised" % repr(idna_domain))

    def testAddrTupleIDNAHostname(self):
        idna_domain = u"al\u00e1n.com"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if socket.supports('idna'):
            try:
                s.bind( (idna_domain, 80) )
            except socket.error:
                # We're not worried about socket errors, i.e. bind problems, etc.
                pass
            except Exception, x:
                self.fail("Unexpected exception raised for socket.bind(%s)" % repr(idna_domain))
        else:
            try:
                s.bind( (idna_domain, 80) )
            except UnicodeEncodeError:
                pass
            except Exception, x:
                self.fail("Non ascii domain '%s' should have raised UnicodeEncodeError, not %s" % (repr(idna_domain), str(x)))
            else:
                self.fail("Non ascii domain '%s' should have raised UnicodeEncodeError: no exception raised" % repr(idna_domain))

class TestInvalidUsage(unittest.TestCase):

    def setUp(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def testShutdownIOOnListener(self):
        self.socket.listen(50) # socket is now a server socket
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except Exception, x:
            self.fail("Shutdown on listening socket should not have raised socket exception, not %s" % str(x))
        else:
            pass

    def testShutdownOnUnconnectedSocket(self):
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except socket.error, se:
            self.failUnlessEqual(se[0], errno.ENOTCONN, "Shutdown on unconnected socket should have raised errno.ENOTCONN, not %s" % str(se[0]))
        except Exception, x:
            self.fail("Shutdown on unconnected socket should have raised socket exception, not %s" % str(x))
        else:
            self.fail("Shutdown on unconnected socket should have raised socket exception")

class TestGetSockAndPeerName:

    def testGetpeernameNoImpl(self):
        try:
            self.s.getpeername()
        except socket.error, se:
            if se[0] == errno.ENOTCONN:
                return
        self.fail("getpeername() on unconnected socket should have raised socket.error")

    def testGetsocknameUnboundNoImpl(self):
        try:
            self.s.getsockname()
        except socket.error, se:
            if se[0] == errno.ENOTCONN:
                return
        self.fail("getsockname() on unconnected socket should have raised socket.error")

    def testGetsocknameBoundNoImpl(self):
        self.s.bind( ("localhost", 0) )
        try:
            self.s.getsockname()
        except socket.error, se:
            self.fail("getsockname() on bound socket should have not raised socket.error")

    def testGetsocknameImplCreated(self):
        self._create_impl_socket()
        try:
            self.s.getsockname()
        except socket.error, se:
            self.fail("getsockname() on active socket should not have raised socket.error")

    def tearDown(self):
        self.s.close()

class TestGetSockAndPeerNameTCPClient(unittest.TestCase, TestGetSockAndPeerName):

    def setUp(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # This server is not needed for all tests, but create it anyway
        # It uses an ephemeral port, so there should be no port clashes or
        # problems with reuse.
        self.server_peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_peer.bind( ("localhost", 0) )
        self.server_peer.listen(5)

    def _create_impl_socket(self):
        self.s.connect(self.server_peer.getsockname())

    def testGetpeernameImplCreated(self):
        self._create_impl_socket()
        try:
            self.s.getpeername()
        except socket.error, se:
            self.fail("getpeername() on active socket should not have raised socket.error")
        self.failUnlessEqual(self.s.getpeername(), self.server_peer.getsockname())

    def tearDown(self):
        self.server_peer.close()

class TestGetSockAndPeerNameTCPServer(unittest.TestCase, TestGetSockAndPeerName):

    def setUp(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _create_impl_socket(self):
        self.s.bind(("localhost", 0))
        self.s.listen(5)

    def testGetpeernameImplCreated(self):
        self._create_impl_socket()
        try:
            self.s.getpeername()
        except socket.error, se:
            if se[0] == errno.ENOTCONN:
                return
        self.fail("getpeername() on listening socket should have raised socket.error")

class TestGetSockAndPeerNameUDP(unittest.TestCase, TestGetSockAndPeerName):

    def setUp(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def _create_impl_socket(self):
        # Binding is enough to cause socket impl creation
        self.s.bind(("localhost", 0))

    def testGetpeernameImplCreatedNotConnected(self):
        self._create_impl_socket()
        try:
            self.s.getpeername()
        except socket.error, se:
            if se[0] == errno.ENOTCONN:
                return
        self.fail("getpeername() on unconnected UDP socket should have raised socket.error")

    def testGetpeernameImplCreatedAndConnected(self):
        # This test also tests that an UDP socket can be bound and connected at the same time
        self._create_impl_socket()
        # Need to connect to an UDP port
        self._udp_peer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._udp_peer.bind( ("localhost", 0) )
        self.s.connect(self._udp_peer.getsockname())
        try:
            try:
                self.s.getpeername()
            except socket.error, se:
                # FIXME Apparently Netty doesn't set remoteAddress,
                # even if connected, for datagram channels so we may
                # have to shadow
                self.fail("getpeername() on connected UDP socket should not have raised socket.error")
            self.failUnlessEqual(self.s.getpeername(), self._udp_peer.getsockname())
        finally:
            self._udp_peer.close()

class ConfigurableClientSocketTest(SocketTCPTest, ThreadableTest):

    # Too bad we are not using cooperative multiple inheritance -
    # **super is super**, after all!  So this means we currently have
    # a bit of code duplication with respect to other unit tests. May
    # want to refactor these unit tests accordingly at some point.

    def config_client(self):
        raise NotImplementedError("subclassing unit tests must define")

    def __init__(self, methodName='runTest'):
        SocketTCPTest.__init__(self, methodName=methodName)
        ThreadableTest.__init__(self)

    def setUp(self):
        SocketTCPTest.setUp(self)
        # Indicate explicitly we're ready for the client thread to
        # proceed and then perform the blocking call to accept
        self.serverExplicitReady()
        self.cli_conn, _ = self.serv.accept()

    def clientSetUp(self):
        self.cli = self.config_client()
        self.cli.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.cli.connect((self.HOST, self.PORT))
        self.serv_conn = self.cli

    def clientTearDown(self):
        self.cli.close()
        self.cli = None
        ThreadableTest.clientTearDown(self)

    def testRecv(self):
        # Testing large receive over TCP
        msg = self.cli_conn.recv(1024)
        self.assertEqual(msg, MSG)

    def _testRecv(self):
        self.serv_conn.send(MSG)

class ProtocolCanBeZeroTest(ConfigurableClientSocketTest):

    def config_client(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

class SocketClassCanBeSubclassed(ConfigurableClientSocketTest):

    def config_client(self):
        class MySocket(socket.socket):
            pass
        return MySocket()


def test_main():

    if test_support.is_jython:
        # Netty logs stack dumps when we destroy sockets after their parent
        # group, see http://bugs.jython.org/issue2517 . Is this a real bug?
        # For now, treat as inconvenient artifact of test.
        _set_java_logging("io.netty.channel.ChannelInitializer",
                          java.util.logging.Level.SEVERE)
        _set_java_logging("io.netty.util.concurrent.DefaultPromise",
                          java.util.logging.Level.OFF)

    tests = [
        GeneralModuleTests,
        IPAddressTests,
        TestSupportedOptions,
        TestPseudoOptions,
        TestUnsupportedOptions,
        BasicTCPTest,
        TCPServerTimeoutTest,
        TCPClientTimeoutTest,
        TestExceptions,
        TestInvalidUsage,
        TestGetAddrInfo,
        TestGetNameInfo,
        TestTCPAddressParameters,
        TestUDPAddressParameters,
        UDPBindTest,
        BasicUDPTest,
        UDPTimeoutTest,
        NonBlockingTCPTests,
        NonBlockingUDPTests,
        TCPFileObjectClassOpenCloseTests,
        UDPFileObjectClassOpenCloseTests,
        FileAndDupOpenCloseTests,
        FileObjectClassTestCase,
        PrivateFileObjectTestCase,
        UnbufferedFileObjectClassTestCase,
        LineBufferedFileObjectClassTestCase,
        SmallBufferedFileObjectClassTestCase,
        UnicodeTest,
        IDNATest,
        TestGetSockAndPeerNameTCPClient, 
        TestGetSockAndPeerNameTCPServer, 
        TestGetSockAndPeerNameUDP,
        ProtocolCanBeZeroTest,
        SocketClassCanBeSubclassed
    ]

    if hasattr(socket, "socketpair"):
        tests.append(BasicSocketPairTest)

    if sys.platform[:4] == 'java':
        tests.append(TestJythonTCPExceptions)
        tests.append(TestJythonUDPExceptions)
        tests.append(TestJython_get_jsockaddr)

    # TODO: Broadcast requires permission, and is blocked by some firewalls
    # Need some way to discover the network setup on the test machine
    if False:
        tests.append(UDPBroadcastTest)
    suites = [unittest.makeSuite(klass, 'test') for klass in tests]
    test_support._run_suite(unittest.TestSuite(suites))


if __name__ == "__main__":
    test_main()
