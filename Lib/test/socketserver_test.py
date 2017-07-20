# Used by test_threading_jy.py to verify no memory leaks in using a
# relatively large number of threads. This is of course an absolutely
# silly way to write real code on the JVM :), use a thread pool. So
# just for testing.
#
# However, the client here does use a thread pool.
#
# TODO monitor heap consumption too from appropriate MBean. Then we
# could presumably be adaptive or something clever like that.
#
# Test for http://bugs.jython.org/issue1660

import socket
import threading
import SocketServer
import time
from java.lang import Runtime
from java.util.concurrent import Executors, ExecutorCompletionService

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.currentThread()
        response = "%s: %s" % (cur_thread.getName(), data)
        self.request.send(response)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    "mix together"

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    sock.send(message)
    response = sock.recv(1024)
    # print threading.currentThread().getName(), response
    sock.close()

if __name__ == "__main__":
    # ephemeral ports should work on every Java system now
    HOST, PORT = "localhost", 0

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a daemon thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(True)
    server_thread.start()

    # create a client pool to run all client requests
    pool = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors() + 1)
    ecs = ExecutorCompletionService(pool)
    for i in xrange(4000): # empirically, this will exhaust heap when run with 16m heap
        ecs.submit(lambda: client(ip, port, "Hello World %i" % i))
        ecs.take() # wait until we have a thread available in the pool
    pool.shutdown()
        
