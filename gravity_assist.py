import math


def gravity_assist_velocity(angle: float, velocity_inf: float, planet_velocity: float):
    vmMax = math.sqrt((planet_velocity + velocity_inf * math.cos(math.pi - angle)) ** 2 + (
        velocity_inf * math.sin(math.pi - angle)) ** 2)
    vmMin = math.sqrt((planet_velocity - velocity_inf * math.cos(math.pi - angle)) ** 2 + (
        velocity_inf * math.sin(math.pi - angle)) ** 2)
    return vmMax, vmMin
