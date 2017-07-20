from __future__ import print_function

import sys
from java.io import Serializable
from java.util.concurrent import Callable

from clamp import PackageProxy


class Dog(Callable, Serializable):
    # FIXME in a future branch, support the ability to call __init__
    # via __initProxy__ To support this functionality, the test
    # version of the clamp module in this directory needs to add a
    # Java constructor with an Object... arg list; possibly introspect
    # the arg list of __init__; or get some additional metadata from
    # the initialization of PackageProxy.
    __proxymaker__ = PackageProxy("org.python.test")
                
    def __init__(self):
        self.name = "Rover"
        self.number = 42
        
    def whoami(self):
        return self.name

    def call(self):
        # Using print forces use of PySystemState and shows it's initialized
        print("%s barks %s times" % (self.name, self.number))
        # Verify that site has been imported and therefore
        # site-packages and distutils/setuptools goodness is available
        return "site" in sys.modules

    def __eq__(self, other):
        return self.name == other.name and self.number == other.number
