import math
import unittest

from numpy import multiply

from orbit import Orbit


class OrbitConvertTestCase(unittest.TestCase):
    def test_xyz_vel_to_kelper(self):
        rvec = multiply([6534.834, 6862.875, 6448.296], 1000)  # [m]
        vvec = multiply([4.901327, 5.533756, -1.976341], 1000)  # [m]
        my_orbit = Orbit()
        my_orbit.xyz_vel_to_kelper(rvec=rvec, vvec=vvec)
        self.assertEqual(round(my_orbit.e, 3), .833)
        self.assertLess(round(my_orbit.a / 1000, 3) - 36127.343, 200)
        self.assertLess(math.fabs(round(math.degrees(my_orbit.i), 2) - 87.87), .1)
        self.assertLess(math.fabs(round(math.degrees(my_orbit.Omega), 2) - 227.898), 1)
        self.assertLess(math.fabs(round(math.degrees(my_orbit.omega), 2) - 53.38), 1)
        self.assertLess(math.fabs(round(math.degrees(my_orbit.nu), 2) - 92.335), 1)

    def test_kelper_to_xyz_vel(self):
        my_orbit = Orbit()
        p = 11067.790 * 1000  # [m]
        e = .83285
        a = p / (1 - e ** 2)
        i = math.radians(87.87)
        raan = math.radians(227.89)
        omega = math.radians(53.38)
        nu = math.radians(92.335)
        my_orbit.e = e
        my_orbit.a = a
        my_orbit.i = i
        my_orbit.Omega = raan
        my_orbit.omega = omega
        my_orbit.nu = nu
        rvec_ijk, vvec_ijk = my_orbit.kelper_to_xvz_vel()
        self.assertAlmostEqual(rvec_ijk[0] / 1000, 6525.34, places=1)
        self.assertAlmostEqual(rvec_ijk[1] / 1000, 6861.5, places=1)
        self.assertAlmostEqual(rvec_ijk[2] / 1000, 6449.1, places=1)

        self.assertAlmostEqual(vvec_ijk[0] / 1000, 4.902, places=3)
        self.assertAlmostEqual(vvec_ijk[1] / 1000, 5.533, places=3)
        self.assertAlmostEqual(vvec_ijk[2] / 1000, -1.9757, places=3)


if __name__ == '__main__':
    unittest.main()
