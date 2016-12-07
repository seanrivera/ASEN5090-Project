import datetime
import math
import sys


def find_gmst(date: datetime.datetime):
    year = date.year
    if year > 2100 or year < 1900:
        sys.exit("Invalid year in find_gmst")
    month = date.month
    day = date.day
    hour = date.hour
    minute = date.minute
    sec = date.second
    JD = 367 * year - int(7 * (year + int((month + 9) / 12)) / 4) + int(
        275 * month / 9) + day + 1721013.5 + (((sec / 60 + minute) / 60) + hour) / 24
    T_UT1 = (JD - 2451545.0) / 36525
    theta_gmst_sec = 67310.54841 + ((876600 * 3600 + 8640184.812866) * T_UT1) + (0.0093104 * T_UT1 ** 2) - (
        6.2 * 10 ** -6 * T_UT1 ** 3)
    theta_gmst_sec = math.fmod(theta_gmst_sec, 86400)
    theta_gmst_deg = theta_gmst_sec / 240
    if theta_gmst_deg < 0:
        theta_gmst_deg += 360
    elif theta_gmst_deg > 360:
        theta_gmst_deg -= 360
    return math.radians(theta_gmst_deg)
