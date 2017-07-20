import unittest

from test import test_support

from java import io, awt
import os
import sys


class Foo:
    def bar(self):
        return 'bar'


class JavaSerializationTests(unittest.TestCase):

    def setUp(self):
        self.sername = os.path.join(sys.prefix, "test.ser")

    def tearDown(self):
        os.remove(self.sername)

    def test_serialization(self):
        object1 = 42
        object2 = ['a', 1, 1.0]
        object3 = Foo()
        object3.baz = 99

        object4 = awt.Color(1, 2, 3)

        #writing
        fout = io.ObjectOutputStream(io.FileOutputStream(self.sername))
        #Python int
        fout.writeObject(object1)
        #Python list
        fout.writeObject(object2)
        #Python instance
        fout.writeObject(object3)
        #Java instance
        fout.writeObject(object4)
        fout.close()

        fin = io.ObjectInputStream(io.FileInputStream(self.sername))

        #reading
        iobject1 = fin.readObject()
        iobject2 = fin.readObject()
        iobject3 = fin.readObject()
        iobject4 = fin.readObject()
        fin.close()

        self.assertEquals(iobject1, object1)
        self.assertEquals(iobject2, object2)
        self.assertEquals(iobject3.baz, 99)
        self.assertEquals(iobject3.bar(), 'bar')
        self.assertEquals(iobject3.__class__, Foo)
        self.assertEquals(iobject4, object4)


def test_main():
    test_support.run_unittest(JavaSerializationTests)


if __name__ == "__main__":
    test_main()
