import unittest
from test import test_support

from datetime import timedelta
from datetime import tzinfo
from datetime import time
from datetime import date, datetime

from java.util import Calendar, GregorianCalendar
from java.sql import Date, Time, Timestamp


class TestCalendar(unittest.TestCase):

    def test_datetime(self):
        self.assertTrue(hasattr(datetime, "__tojava__"))
        x = datetime(2007, 1, 3)
        y = x.__tojava__(Calendar)
        self.assertIsInstance(y, GregorianCalendar)
        self.assertEqual(y.get(Calendar.YEAR), 2007)
        self.assertEqual(y.get(Calendar.MONTH), 0)
        self.assertEqual(y.get(Calendar.DAY_OF_MONTH), 3)
        self.assertEqual(y.get(Calendar.HOUR), 0)
        self.assertEqual(y.get(Calendar.MINUTE), 0)
        self.assertEqual(y.get(Calendar.SECOND), 0)

    def test_date(self):
        self.assertTrue(hasattr(date, "__tojava__"))
        x = date(2007, 1, 3)
        y = x.__tojava__(Calendar)
        self.assertIsInstance(y, GregorianCalendar)
        self.assertEqual(y.get(Calendar.YEAR), 2007)
        self.assertEqual(y.get(Calendar.MONTH), 0)
        self.assertEqual(y.get(Calendar.DAY_OF_MONTH), 3)

    def test_time(self):
        self.assertTrue(hasattr(time, "__tojava__"))
        x = time(1, 3)
        y = x.__tojava__(Calendar)
        self.assertIsInstance(y, GregorianCalendar)
        # Note obvious implementation details from GregorianCalendar
        # and its definition in terms of the epoch
        self.assertEqual(y.get(Calendar.YEAR), 1970)
        self.assertEqual(y.get(Calendar.MONTH), 0)
        self.assertEqual(y.get(Calendar.DAY_OF_MONTH), 1)
        self.assertEqual(y.get(Calendar.HOUR), 1)
        self.assertEqual(y.get(Calendar.MINUTE), 3)
        self.assertEqual(y.get(Calendar.SECOND), 0)


class TestTimezone(unittest.TestCase):

    def test_olson(self):
        class GMT1(tzinfo):
            def utcoffset(self, dt):
                return timedelta(hours=1)
            def dst(self, dt):
                return timedelta(0)
            def tzname(self,dt):
                return "Europe/Prague"

        self.assertTrue(hasattr(datetime, "__tojava__"))
        x = datetime(2007, 1, 3, tzinfo=GMT1())
        y = x.__tojava__(Calendar)
        self.assertIsInstance(y, GregorianCalendar)
        self.assertEqual(y.get(Calendar.YEAR), 2007)
        self.assertEqual(y.get(Calendar.MONTH), 0)
        self.assertEqual(y.get(Calendar.DAY_OF_MONTH), 3)
        self.assertEqual(y.get(Calendar.HOUR), 0)
        self.assertEqual(y.get(Calendar.MINUTE), 0)
        self.assertEqual(y.get(Calendar.SECOND), 0)
        self.assertEqual(y.getTimeZone().getID(), "Europe/Prague")

    def test_offset(self):
        class Offset(tzinfo):
            def utcoffset(self, dt):
                return timedelta(hours=1, minutes=15)
            def dst(self, dt):
                return timedelta(seconds=-900)
            def tzname(self,dt):
                return "Foo/Bar"

        self.assertTrue(hasattr(datetime, "__tojava__"))
        x = datetime(2007, 1, 3, tzinfo=Offset())
        y = x.__tojava__(Calendar)
        self.assertIsInstance(y, GregorianCalendar)
        self.assertEqual(y.get(Calendar.YEAR), 2007)
        self.assertEqual(y.get(Calendar.MONTH), 0)
        self.assertEqual(y.get(Calendar.DAY_OF_MONTH), 3)
        self.assertEqual(y.get(Calendar.HOUR), 0)
        self.assertEqual(y.get(Calendar.MINUTE), 0)
        self.assertEqual(y.get(Calendar.SECOND), 0)
        self.assertEqual(y.getTimeZone().getID(), "UTC")
        self.assertEqual(y.get(Calendar.DST_OFFSET), -900 * 1000)
        self.assertEqual(y.get(Calendar.ZONE_OFFSET), 4500 * 1000)


class TestSQL(unittest.TestCase):

    def test_datetime(self):
        self.assertTrue(hasattr(datetime, "__tojava__"))
        x = datetime(2007, 1, 3)
        y = x.__tojava__(Timestamp)
        self.assertIsInstance(y, Timestamp)
        self.assertEqual(y.getTime(), (x - datetime(1970, 1, 1)).total_seconds() * 1000)

    def test_date(self):
        self.assertTrue(hasattr(date, "__tojava__"))
        x = date(2007, 1, 3)
        y = x.__tojava__(Date)
        self.assertIsInstance(y, Date)
        self.assertEqual(y.getTime(), (x - date(1970, 1, 1)).total_seconds() * 1000)

    def test_time(self):
        self.assertTrue(hasattr(time, "__tojava__"))
        x = time(1, 3)
        y = x.__tojava__(Time)
        self.assertIsInstance(y, Time)
        epoch = y.getTime()/1000.
        self.assertEqual(epoch // 3600, 1)   # 1 hour
        self.assertEqual(epoch % 3600, 180)  # 3 minutes


def test_main():
    test_support.run_unittest(
        TestCalendar,
        TestSQL,
        TestTimezone)


if __name__ == '__main__':
    test_main()
