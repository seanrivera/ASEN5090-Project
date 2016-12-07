import math

import numpy as np


def eci2ecef(pos_eci, theta_gst):
    r3 = np.array(
        [[math.cos(theta_gst), math.sin(theta_gst), 0], [-math.sin(theta_gst), math.cos(theta_gst), 0], [0, 0, 1]])
    pos_ecef = np.matmul(r3, pos_eci)
    return pos_ecef


def ecef2eci(pos_ecef, theta_gst):
    r3 = np.array(
        [[math.cos(theta_gst), math.sin(theta_gst), 0], [-math.sin(theta_gst), math.cos(theta_gst), 0], [0, 0, 1]])
    pos_eci = np.linalg.lstsq(r3, pos_ecef)
    return pos_eci[0]


def ecef2topo(pos_ecef, lat, lon, alt, radius_earth=(6378.1363 * 1000)):
    site_ecef = np.array(lla2ecef(lat=lat, lon=lon, altitude=alt, radius_earth=radius_earth))
    rho_ecef = np.array(pos_ecef) - site_ecef
    # Transformation matrix
    inv_lat = math.radians(90) - lat
    r2 = np.array([[math.cos(inv_lat), 0, -math.sin(inv_lat)], [0, 1, 0], [math.sin(inv_lat), 0, math.cos(inv_lat)]])
    r3 = np.array([[math.cos(lon), math.sin(lon), 0], [-math.sin(lon), math.cos(lon), 0], [0, 0, 1]])
    pos_sez = np.matmul(r2, np.matmul(r3, rho_ecef))
    range_dist = np.linalg.norm(pos_sez)
    projection_xy = math.sqrt(pos_sez[0] ** 2 + pos_sez[1] ** 2)
    az = math.atan2(pos_sez[1] / projection_xy, -pos_sez[0] / projection_xy)
    while az < 0:
        az += math.pi * 2
    el_sin = pos_sez[2] / range_dist
    el_cos = math.sqrt(pos_sez[0] ** 2 + pos_sez[1] ** 2) / range_dist
    el = math.atan2(el_sin, el_cos)

    return el, az, range_dist


def lla2ecef(lat, lon, altitude, radius_earth=6378.1363 * 1000):
    r = radius_earth + altitude
    x = r * math.cos(lat) * math.cos(lon)
    y = r * math.cos(lat) * math.sin(lon)
    z = r * math.sin(lat)
    return [x, y, z]


def ecef2lla(pos_ecef):
    e = 8.1819190842622e-2  # eccentricity
    (lat_a, lon, alt) = ecef2geodediclla(pos_ecef=pos_ecef)
    lat = math.atan2((1 - e ** 2) * math.tan(lat_a), 1)
    return lat, lon, alt


def ecef2geodediclla(pos_ecef):
    # WGS84 constants
    a = 6378137  # radius
    e = 8.1819190842622e-2  # eccentricity
    a_squared = a ** 2
    e_squared = e ** 2

    x = pos_ecef[0]
    y = pos_ecef[1]
    z = pos_ecef[2]

    b = math.sqrt(a_squared * (1 - e_squared))
    b_squared = b ** 2
    ep = math.sqrt((a_squared - b_squared) / b_squared)
    p = math.sqrt((x ** 2) + (y ** 2))
    theta = math.atan2(a * z, b * p)

    lon = math.atan2(y, x)
    lat = math.atan2(z + (ep ** 2) * b * (math.sin(theta) ** 3), p - e_squared * a * (math.cos(theta) ** 3))
    n = a / (math.sqrt(1 - e_squared * (math.sin(lat) ** 2)))
    alt = p / math.cos(lat) - n

    lon = math.fmod(lon, 2 * math.pi)

    return lat, lon, alt
