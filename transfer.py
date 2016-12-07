import math

from constants import *
from orbit import Orbit


def hohmann_transfer(r_initial: float, orbit_initial: Orbit, r_final: float, orbit_final: Orbit,
                     mu: float = mu_earth, show_work: bool = False) -> tuple:
    a_trans = (r_initial + r_final) / 2.0
    v_initial = orbit_initial.vis_viva(r_initial)
    v_final = orbit_final.vis_viva(r_final)
    v_trans_a = math.sqrt((2 * mu / r_initial) - (mu / a_trans))
    v_trans_b = math.sqrt((2 * mu / r_final) - (mu / a_trans))
    delta_v_a = v_trans_a - v_initial
    delta_v_b = v_final - v_trans_b
    delta_v = math.fabs(delta_v_a) + math.fabs(delta_v_b)
    t_trans = math.pi * math.sqrt(a_trans ** 3 / mu)
    if show_work:
        print("V_trans_a = " + str(v_trans_a) + " m/s")
        print("V_trans_b = " + str(v_trans_b) + " m/s")

    return a_trans, t_trans, delta_v_a, delta_v_b, delta_v


def hohmann_from_dv(r_initial: float, orbit_initial: Orbit, delta_v: float) -> tuple:
    v_final = orbit_initial.vis_viva(r_initial) + delta_v
    a = 1 / (2 / r_initial - v_final ** 2 / orbit_initial.mu)
    r_final = 2 * a - r_initial
    final_orbit = Orbit()
    final_orbit.periapsis_apoapsis_set(periapsis=r_initial, apoapsis=r_final, mu=orbit_initial.mu)
    return r_final, final_orbit


def circ_inc_transfer(delta_i: float, r_initial: float, orbit_initial: Orbit) -> float:
    v = orbit_initial.vis_viva(r=r_initial)
    delta_v = 2 * v * math.sin(delta_i / 2)
    return delta_v


def cw_hill(x, y, z, x_dot, y_dot, z_dot, omega, t):
    x_t = x_dot / omega * math.sin(omega * t) - (3 * x + 2 * y_dot / omega) * math.cos(omega * t) + (
        4 * x + 2 * y_dot / omega)
    y_t = (6 * x + 4 * y_dot / omega) * math.sin(omega) + 2 * x_dot / omega * math.cos(omega * t) - \
          (6 * omega * x + 3 * y_dot) * t + (
              y - 2 * x_dot / omega)
    z_t = z * math.cos(omega * t) + z_dot / omega * math.sin(omega * t)
    x_dot_t = x_dot * math.cos(omega * t) + (3 * omega * x + 2 * y_dot) * math.sin(omega)
    y_dot_t = (6 * omega * x + 4 * y_dot) * math.cos(omega * t) - 2 * x_dot * math.sin(omega * t) - (
        6 * omega * x + 3 * y_dot)
    z_dot_t = -z * omega * math.sin(omega * t) + z_dot * math.cos(omega * t)
    return x_t, y_t, z_t, x_dot_t, y_dot_t, z_dot_t


def sphere_of_influence(mass_planet: float, a_planet: float, mass_sun: float):
    return (mass_planet / mass_sun) ** (2 / 5) * a_planet
