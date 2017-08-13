import unittest
from test import test_support
import SocketServer

class TestSocketServer(unittest.TestCase):

    def testEphemeralPort(self):
        """ Test that an ephemeral port is set correctly """
        # If we specify 0, system should pick an emphemeral port
        host, port = "localhost", 0
        # Request handler never instantiated
        server = SocketServer.TCPServer( (host, port), None)
        server_host, server_port = server.server_address
        self.failIfEqual(server_port, 0, "System assigned ephemeral port should not be zero")


def test_main():
    test_support.run_unittest(TestSocketServer)


if __name__ == "__main__":
    test_main()
