import unittest
from test import test_support

from decimal import Decimal

from java.lang import Float, Double, Object
from java.math import BigDecimal


class TestJavaDecimal(unittest.TestCase):

    def test_decimal(self):
        x = Decimal("1.1")
        y = x.__tojava__(BigDecimal)
        self.assertTrue(isinstance(y, BigDecimal))

    def test_object(self):
        x = Decimal("1.1")
        y = x.__tojava__(Object)
        self.assertTrue(isinstance(y, BigDecimal))        

    def test_float(self):
        x = Decimal("1.1")
        y = x.__tojava__(Float)
        self.assertTrue(isinstance(y, Float))
    
    def test_double(self):
        x = Decimal("1.1")
        y = x.__tojava__(Double)
        self.assertTrue(isinstance(y, Double))


if __name__ == '__main__':
    unittest.main()
