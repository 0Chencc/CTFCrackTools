import unittest
import test.test_support

class SubclassInstanceTest(unittest.TestCase):

    def test_subclass_int(self):
        try:
            class foo(12): pass
        except TypeError:
            pass
        else:
            self.fail("expected TypeError for subclassing an int instance")


class TestStableSubclasses(unittest.TestCase):

    def test_subclasses_stable(self):
        class C(object):
            pass

        subclasses = []
        for i in range(1024):
            name = 'S%s' % i
            subclasses.append(type(name, (C,), {}))
        self.assertEqual(subclasses, C.__subclasses__())

    def test_subclasses_stable_with_gc(self):
        class C(object):
            pass

        subclasses = []
        for i in range(1024):
            name = 'S%s' % i
            subclasses.append(type(name, (C,), {}))
        self.assertEqual(subclasses, C.__subclasses__())

        # punch some holes in the previous subclasses, verify
        # continued stability
        for i in range(32):
            del subclasses[i * 32]  # depends on prev deletion of course...
        test.test_support.gc_collect()
        self.assertEqual(subclasses, C.__subclasses__())

        # add some more subclasses
        for i in range(1024, 2048):
            name = 'S%s' % i
            subclasses.append(type(name, (C,), {}))
        self.assertEqual(subclasses, C.__subclasses__())


def test_main():
    test.test_support.run_unittest(
        SubclassInstanceTest, TestStableSubclasses)

if __name__ == "__main__":
    test_main()
