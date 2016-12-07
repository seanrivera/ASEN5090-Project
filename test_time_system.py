import datetime
import math
import unittest

import pytz

from time_system import find_gmst


class TimeConvertTestCase(unittest.TestCase):
    def test_find_gmst(self):
        UTC = pytz.timezone('UTC')
        date = datetime.datetime(year=1992, month=8, day=20, hour=12, minute=14, second=0, tzinfo=UTC)
        gmst_rad = find_gmst(date=date)
        self.assertAlmostEqual(math.degrees(gmst_rad), 152.578787810, places=5)


if __name__ == '__main__':
    unittest.main()
