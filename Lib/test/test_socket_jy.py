import errno
import os
import socket
import ssl
import threading
import time
import unittest
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from test import test_support


def data_file(*name):
    return os.path.join(os.path.dirname(__file__), *name)

CERTFILE = data_file("keycert.pem")
ONLYCERT = data_file("ssl_cert.pem")
ONLYKEY = data_file("ssl_key.pem")

def start_server():
    server_address = ('127.0.0.1', 0)

    class DaemonThreadingMixIn(ThreadingMixIn):
        daemon_threads = True

    class ThreadedHTTPServer(DaemonThreadingMixIn, HTTPServer):
        """Handle requests in a separate thread."""

    # not actually going to do anything with this server, so a
    # do-nothing handler is reasonable
    httpd = ThreadedHTTPServer(server_address, BaseHTTPRequestHandler)
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    return httpd, server_thread


class SocketConnectTest(unittest.TestCase):

    def setUp(self):
        self.httpd, self.server_thread = start_server()
        self.address = self.httpd.server_name, self.httpd.server_port

    def tearDown(self):
        self.httpd.shutdown()
        self.server_thread.join()

    def do_nonblocking_connection(self, results, index):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(0)
        connect_errno = 0
        connect_attempt = 0

        while connect_errno != errno.EISCONN and connect_attempt < 10000:
            connect_attempt += 1
            connect_errno = sock.connect_ex(self.address)
            results[index].append(connect_errno)
            time.sleep(0.01)
        sock.close()

    def do_workout(self, num_threads=10):
        connect_results = []
        connect_threads = []
        for i in xrange(num_threads):
            connect_results.append([])
            connect_threads.append(threading.Thread(
                target=self.do_nonblocking_connection,
                name="socket-workout-%s" % i,
                args=(connect_results, i)))
                           
        for thread in connect_threads:
            thread.start()
        for thread in connect_threads:
            thread.join()
        return connect_results

    def test_connect_ex_workout(self):
        """Verify connect_ex states go through EINPROGRESS?, EALREADY*, EISCONN"""
        # Tests fix for http://bugs.jython.org/issue2428; based in part on the
        # code showing failure that was submitted with that bug
        for result in self.do_workout():
            self.assertIn(result[0], {errno.EINPROGRESS, errno.EISCONN})
            self.assertEqual(result[-1], errno.EISCONN)
            for code in result[1:-1]:
                self.assertEqual(code, errno.EALREADY)


class SSLSocketConnectTest(unittest.TestCase):

    def setUp(self):
        self.httpd, self.server_thread = start_server()
        self.httpd.socket = ssl.wrap_socket(
            self.httpd.socket,
            certfile=ONLYCERT,
            server_side=True,
            keyfile=ONLYKEY,
        )
        self.address = self.httpd.server_name, self.httpd.server_port

    def tearDown(self):
        self.httpd.shutdown()
        self.server_thread.join()

    def do_nonblocking_connection(self, results, index):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(0)
        connect_errno = 0
        connect_attempt = 0
        sock = ssl.wrap_socket(sock, certfile=CERTFILE, do_handshake_on_connect=True)

        while connect_errno != errno.EISCONN and connect_attempt < 10000:
            connect_attempt += 1
            connect_errno = sock.connect_ex(self.address)
            results[index].append(connect_errno)
            time.sleep(0.01)
        sock.close()

    def do_workout(self, num_threads=10):
        connect_results = []
        connect_threads = []
        for i in xrange(num_threads):
            connect_results.append([])
            connect_threads.append(threading.Thread(
                target=self.do_nonblocking_connection,
                name="socket-workout-%s" % i,
                args=(connect_results, i)))
                           
        for thread in connect_threads:
            thread.start()
        for thread in connect_threads:
            thread.join()
        return connect_results

    def test_connect_ex_workout(self):
        """Verify connect_ex states go through EINPROGRESS?, EALREADY*, EISCONN"""
        # Tests fix for http://bugs.jython.org/issue2428; based in part on the
        # code showing failure that was submitted with that bug
        for result in self.do_workout():
            self.assertIn(result[0], {errno.EINPROGRESS, errno.EISCONN})
            self.assertEqual(result[-1], errno.EISCONN)
            for code in result[1:-1]:
                self.assertEqual(code, errno.EALREADY)



class SocketOptionsTest(unittest.TestCase):

    def test_socket_options_defined(self):
        # Basic existence test to verify trivial fix for
        # http://bugs.jython.org/issue2436
        self.assertEqual(socket.SOL_TCP, socket.IPPROTO_TCP)


def test_main():
    test_support.run_unittest(SocketConnectTest, SSLSocketConnectTest, SocketOptionsTest)


if __name__ == "__main__":
    test_main()
