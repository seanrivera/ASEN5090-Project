import math

import matplotlib.pyplot as plt
from numpy import cross, dot, divide, arccos, arcsin, array, matmul, isnan, concatenate, transpose
from numpy.linalg import norm
from scipy.integrate import ode

from constants import *
from coordinate_system import eci2ecef, ecef2lla
from models import two_body_model


class Orbit:
    DIFF = 1e-8  # Diff for eccentric
    MAX_ITER = 100

    # noinspection PyPep8Naming
    def __init__(self, a=float('nan'), e=float('nan'), i=float('nan'), Omega=float('nan'), omega=float('nan'),
                 mo=float('nan'), tp=float('nan'), mu=mu_earth, name=''):
        self.mu = mu
        self.a = a  # Semi-major Axis
        if not math.isnan(a) and not math.isnan(mu):
            self.period = 2 * math.pi * math.sqrt((a ** 3) / mu)
            self.n = 2 * math.pi / self.period
        else:
            self.period = float('nan')
            self.n = float('nan')
        self.periapsis = float('nan')
        self.apoapsis = float('nan')
        self.E = float('nan')  # Specific Energy
        self.phi = float('nan')  # flight path angle
        self.h_hat = [float('nan'), float('nan'), float('nan')]  # Angular momentum
        self.tp = tp  # time since periapsis
        self.e = e  # Eccentricity
        self.i = i  # Inclination
        self.Omega = Omega  # Longitude of the ascending node
        self.omega = omega  # Argument of periapsis
        self.nu = float('nan')  # True anomaly -Radians
        self.ecc_anomaly = float('nan')  # Eccentric anomaly -Radians
        if math.isnan(mo):
            self.find_mean_anomaly()
        else:
            self.mo = mo  # Mean anomaly at epoch -Radians
        self.find_eccentric_anomaly()
        self.find_true_anomaly()
        self.find_time_periapsis()
        self.find_periapsis_apoapsis()
        self.name = name

    def xyz_vel_to_kelper(self, rvec, vvec, mu=mu_earth):
        self.mu = mu
        r = norm(rvec)  # Radius
        v = norm(vvec)  # Velocity
        self.h_hat = cross(rvec, vvec)  # Specific angular momentum
        h = norm(self.h_hat)

        self.phi = arcsin(dot(rvec, vvec) / (r * v))  # flight path angle
        n_hat = cross([0, 0, 1], self.h_hat)

        period = norm(n_hat)  # orbital period

        e_hat = divide(cross(vvec, self.h_hat), mu) - divide(rvec, r)
        self.E = (v ** 2 / 2) - (mu / r)
        self.e = norm(e_hat)
        self.i = arccos(divide(dot([0, 0, 1], self.h_hat), h))
        self.Omega = arccos(n_hat[0] / period)
        if n_hat[1] < 0:
            self.Omega = 2 * math.pi - self.Omega
        self.omega = arccos(dot(n_hat, e_hat) / (period * self.e))
        if e_hat[2] < 0:
            self.omega = 2 * math.pi - self.omega
        self.nu = arccos(dot(e_hat, rvec) / (self.e * r))
        if dot(rvec, vvec) < 0:
            self.nu = 2 * math.pi - self.nu
        self.a = -mu / (2 * self.E)
        self.period = 2 * math.pi * math.sqrt((self.a ** 3) / mu)
        self.n = 2 * math.pi / self.period
        self.find_eccentric_anomaly()
        self.find_mean_anomaly()

    def kelper_to_xvz_vel(self):
        p = self.a * (1 - self.e ** 2)  # semiparameter
        rvec_pqw = [p * math.cos(self.nu) / (1 + self.e * math.cos(self.nu)),
                    p * math.sin(self.nu) / (1 + self.e * math.cos(self.nu)),
                    0]  # R in the pqw frame
        vvec_pqw = [-math.sqrt(self.mu / p) * math.sin(self.nu), math.sqrt(self.mu / p) * (self.e + math.cos(self.nu)),
                    0]  # V vector in the pqw frame
        transformation__matrix = array([
            [math.cos(self.Omega) *
             math.cos(self.omega) - math.sin(self.Omega) * math.sin(self.omega) *
             math.cos(self.i), -math.cos(self.Omega) * math.sin(self.omega) -
             math.sin(self.Omega) * math.cos(self.omega) * math.cos(self.i),
             math.sin(self.Omega) * math.sin(self.i)],
            [math.sin(self.Omega) *
             math.cos(self.omega) + math.cos(self.Omega) * math.sin(self.omega) *
             math.cos(self.i),
             -math.sin(self.Omega) * math.sin(
                 self.omega) +
             math.cos(self.Omega) * math.cos(
                 self.omega) * math.cos(self.i),
             -math.cos(self.Omega) * math.sin(
                 self.i)],
            [math.sin(self.omega) *
             math.sin(self.i),
             math.cos(
                 self.omega) * math.sin(
                 self.i),
             math.cos(self.i)]])

        rvec_ijk = matmul(transformation__matrix, rvec_pqw)
        vvec_ijk = matmul(transformation__matrix, vvec_pqw)

        return rvec_ijk, vvec_ijk

    def periapsis_apoapsis_set(self, periapsis, apoapsis, mu=mu_earth):
        self.a = (apoapsis + periapsis) / 2
        self.e = (apoapsis - periapsis) / (apoapsis + periapsis)
        self.mu = mu
        if not math.isnan(self.a) and not math.isnan(mu):
            self.period = 2 * math.pi * math.sqrt((self.a ** 3) / mu)
            self.n = 2 * math.pi / self.period
        else:
            self.period = float('nan')
            self.n = float('nan')

    def find_periapsis_apoapsis(self):
        if not math.isnan(self.a) and not math.isnan(self.e):
            self.periapsis = self.a * (1 - self.e)
            self.apoapsis = self.a * (1 + self.e)
        else:
            self.periapsis = float('nan')
            self.apoapsis = float('nan')

    def find_eccentric_anomaly(self):
        if math.isnan(self.e):
            self.ecc_anomaly = float('nan')
            return
        if not math.isnan(self.mo):
            cur_diff = float('inf')
            guess_ecc = self.mo
            cur_iter = 0
            while cur_diff > self.DIFF and cur_iter < self.MAX_ITER:
                self.ecc_anomaly = guess_ecc - (
                    (guess_ecc - self.e * math.sin(guess_ecc) - self.mo) / (1 - self.e * math.cos(guess_ecc)))
                cur_diff = math.fabs(guess_ecc - self.ecc_anomaly)
                guess_ecc = self.ecc_anomaly
                cur_iter += 1
        elif not math.isnan(self.nu) and not math.isnan(self.a):
            cos_e = (self.e + math.cos(self.nu)) / (1 + self.e * math.cos(self.nu))
            sin_e = (math.sqrt(1 - self.e ** 2) * math.sin(self.nu)) / (1 + self.e * math.cos(self.nu))
            self.ecc_anomaly = math.atan2(sin_e, cos_e)
        else:
            self.ecc_anomaly = float('nan')

    def find_true_anomaly(self):
        if math.isnan(self.ecc_anomaly) or math.isnan(self.e):
            self.nu = float('nan')
        else:
            self.nu = 2 * math.atan2(math.tan(self.ecc_anomaly / 2),
                                     math.sqrt((1 - self.e) / (1 + self.e)))

    def find_mean_anomaly(self):
        if not math.isnan(self.ecc_anomaly) and not math.isnan(self.e):  # Try the eccentric anomaly
            self.mo = self.ecc_anomaly - self.e * math.sin(self.ecc_anomaly)
        elif not math.isnan(self.tp) and not math.isnan(self.n):  # Try the time since periapsis
            self.mo = self.n * self.tp
        else:
            self.mo = float('nan')
        if self.mo < 0:
            self.mo += 2 * math.pi

    def find_time_periapsis(self):
        if math.isnan(self.mo) or math.isnan(self.n):
            self.tp = float('nan')
        else:
            self.tp = self.mo / self.n

    def vis_viva(self, r):
        v = math.sqrt(self.mu * ((2 / r) - (1 / self.a)))
        return v

    def plot_ground_track(self, filename: str, duration: float, time_step: float, theta_gst: float,
                          rot: float = 7.2921158553 * 10 ** -5, out_name: str = "ground_track.png"):
        plt.figure()
        with open(filename, 'r') as f:
            lat_lon_str = f.read()
        lat = []
        lon = []
        sat_lat = []
        sat_lon = []
        for pos in lat_lon_str.split('\n'):
            lls = pos.split()
            if lls:
                lon.append(float(lls[0]))
                lat.append(float(lls[1]))
        plt.plot(lon, lat)
        time = 0
        while time < duration:
            (pos_eci, _) = self.kelper_to_xvz_vel()
            pos_ecef = eci2ecef(pos_eci=pos_eci, theta_gst=theta_gst)
            (tmp_lat, tmp_lon, _) = ecef2lla(pos_ecef=pos_ecef)
            sat_lat.append(math.degrees(tmp_lat))
            sat_lon.append(math.degrees(tmp_lon))
            self.propagate(time_step=time_step)
            time += time_step
            theta_gst += rot * time_step
        plt.plot(sat_lon, sat_lat, 'gd')
        plt.xlabel("Latitude (deg)")
        plt.ylabel("Longitude (deg)")
        plt.title("Ground track plot")
        plt.xlim([-180, 180])
        plt.ylim([-90, 90])
        plt.savefig(out_name)

    def propagate(self, time_step: float):
        if not isnan(self.mo):
            self.mo += self.n * time_step
            if self.mo > 2 * math.pi:
                self.mo -= 2 * math.pi
            if self.mo < - 2 * math.pi:
                self.mo += 2 * math.pi
            self.find_eccentric_anomaly()
            self.find_true_anomaly()
        if not isnan(self.tp):
            self.tp += time_step
            if self.tp > self.period:
                self.tp -= self.period

    def ode_propagate(self, time_step: float, end_time: float, tol: float):
        t = 0
        dt = time_step
        (X, V) = self.kelper_to_xvz_vel()
        y0 = array(concatenate((X, transpose(V))))
        r = ode(two_body_model).set_integrator('dopri5', atol=tol, rtol=tol)
        r.set_initial_value(y=y0, t=t).set_f_params(self.mu)
        while r.successful() and r.t < end_time:
            r.integrate(r.t + dt)
        pos_eci = r.y[0:3]
        vel_eci = r.y[3:6]
        self.xyz_vel_to_kelper(rvec=pos_eci, vvec=vel_eci, mu=self.mu)

    def j2_nodal_regression(self, radius: float = rad_earth, j2: float = j2_earth):
        p = self.a * (1 - self.e ** 2)
        Omega_dot = -3 * self.n * radius ** 2 * j2 / (2 * p ** 2) * math.cos(self.i)
        return Omega_dot

    def polar_plot(self, time_step: float, fig=None, label: str = ""):
        if not fig:
            fig = plt.figure().add_subplot(111, 'polar')
        self.find_eccentric_anomaly()
        self.find_true_anomaly()
        r = []
        theta = []
        r_init = (self.a * (1 - self.e * math.cos(self.ecc_anomaly))) / 1000
        theta_init = self.nu
        fig.plot(theta_init, r_init, '*')
        counter = 0
        while counter < self.period:
            self.propagate(time_step=time_step)
            r.append(self.a * (1 - self.e * math.cos(self.ecc_anomaly)) / 1000)
            theta.append(self.nu)
            counter += time_step

        fig.plot(theta, r, label=label)
