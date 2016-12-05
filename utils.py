import math
from datetime import datetime

default_day = datetime(year=1957, month=1, day=1)


def days_in_month(m, y):  # m is 1 indexed: 1-12
    if m == 2:
        return 29 if (y % 4 == 0 and y % 100) or y % 400 == 0 else 28
    elif m in [9, 4, 6, 11]:
        return 30
    else:
        return 31


def is_valid_date(d, m, y):
    return 0 < m <= 12 and 0 < d <= days_in_month(m, y) and 1957 <= y < 2100


def plot_solar_system(current_date):
    mercury_nu = math.radians(333.3721)
    venus_nu = math.radians(88.7083)
    earth_nu = math.radians(358.3110)
    mars_nu = math.radians(79.7596)
    jupiter_nu = math.radians(157.2837)
    saturn_nu = math.radians(152.4320)
    uranus_nu = math.radians(316.3032)
    neptune_nu = math.radians(129.1372)
    pluto_nu = math.radians(287.1723)
