import numpy as np


# noinspection PyUnusedLocal
def two_body_model(t, x, mu):
    r = np.linalg.norm(x[0:3])
    x_dot = np.array([x[3], x[4], x[5], -mu * x[0] / r ** 3, -mu * x[1] / r ** 3, -mu * x[2] / r ** 3])
    return x_dot
