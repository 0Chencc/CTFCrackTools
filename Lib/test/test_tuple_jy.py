import unittest
from test import test_support


class TupleTestCase(unittest.TestCase):
    def test_big_tuple(self):
        """Verify that fairly large collection literals of primitives can be constructed."""
        # use \n to separate to avoid parser problems
        s = eval("(" + ",\n".join((str(x) for x in xrange(64000))) +")")
        self.assertEqual(len(s), 64000)
        self.assertEqual(sum(s), 2047968000)

    def test_subclass_iter_does_not_call_other_special_methods(self):
        # Verify fix for http://bugs.jython.org/issue2442

        class C(tuple):
            def __init__(self, *args):
                self.called = False
                return super(C, type(self)).__init__(self, *args)

            def __len__(self):
                self.called = True
                return super(C, type(self)).__len__(self)

            def __getitem__(self, index):
                self.called = True
                return super(C, type(self)).__getitem__(self, index)

        c = C(range(10))
        self.assertEqual(list(iter(c)), range(10))
        self.assertFalse(c.called)


def test_main():
    test_support.run_unittest(TupleTestCase)


if __name__ == '__main__':
    test_main()
