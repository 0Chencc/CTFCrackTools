from java.io import Serializable
from java.util.concurrent import Callable

class Cat(Callable, Serializable):
    def whoami(self):
        return "Socks"
    def call(self):
        print "meow"  # force use of PySystemState

