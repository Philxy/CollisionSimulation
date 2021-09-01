import numpy as np
H = 0.001
number_of_objects = 0


def F_x(x, v, t):
    return -x


def F_y(y, v, t):
    return -y


# Calculates position and velocity one timestep later by using Runge-Kutta-2nd
def next(r, v, t, F):
    k2_r = H * (v + H/2 * F(r, v, t))
    k1_v = H * F(r, v, t)
    k2_v = H * F(r, v + k1_v/2, t + H/2)
    r_n = r + k2_r
    v_n = v + k2_v
    return [r_n, v_n, t + H]


# Calculates Velocities after collision
def v_new(v1, v2, m1, m2):
    temp = 2 * (m1 * v1 + m2 * v2)/(m1 + m2)
    return [temp - v1, temp - v2]


class Mass:
    def __init__(self, x, y, vx, vy, m, radius):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.m = m
        self.radius = radius
        global number_of_objects
        self.nr = number_of_objects
        number_of_objects += 1

    # update velocity and position
    def update(self):
        calc_x = next(self.x, self.vx, 0, F_x)
        calc_y = next(self.y, self.vy, 0, F_y)
        self.x = calc_x[0]
        self.vx = calc_x[1]
        self.y = calc_y[0]
        self.vy = calc_y[1]


def circlesIntersect(r1, r2, x1, x2, y1, y2):
    return x1 + r1 >= x2 - r2 and y1 + r1 >= y2 - r2


# Given a list of objects this method returns a list of all intersecting objects
def collsion_occurence(masses):
    sorted_by_x = sorted(masses, key=lambda mass: mass.x)
    x_intersection, result = [], []
    for i in range(0, len(sorted_by_x) - 1):
        j = i + 1
        m1, m2 = sorted_by_x[i], sorted_by_x[j]
        while m1.x + m1.radius >= m2.x - m2.radius:
            x_intersection.append([m1, sorted_by_x[j]])
            j += 1
            if j == len(sorted_by_x):
                break
            m2 = sorted_by_x[j]
    for pair in x_intersection:
        m1, m2 = pair[0], pair[1]
        if circlesIntersect(m1.radius, m2.radius, m1.x, m2.x, m1.y, m2.y):
            result.append([m1, m2])
    return result


# Retrns list containint all masses out of bounds
def wall_collision(masses, range):
    result = []
    for m in masses:
        if np.abs(m.x) > range or np.abs(m.y) > range:
            result.append(m)
    return result
