import numpy as np

H = 0.005
t = 0

# defines a force acting on a particle
def F(x, y, vx, vy, m, t):
    return [0, 0]


# Calculates position and velocity with Runge-Kutta-2nd order
def next_step(x, y, vx, vy, m, F):
    #return [x + vx * H, y + vy * H, vx, vy, t + H]
    k2_x = H * (vx + H / 2 * F(x, y, vx, vy, m, t)[0])
    k1_vx = H * F(x, y, vx, vy, m, t)[0]
    k2_vx = H * F(x, y, vx + k1_vx / 2, vy, m, t + H / 2)[0]
    x_n = x + k2_x
    vx_n = vx + k2_vx
    k2_y = H * (vy + H / 2 * F(x, y, vx, vy, m, t)[1])
    k1_vy = H * F(x, y, vx, vy, m, t)[1]
    k2_vy = H * F(x, y, vx, vy + k1_vy / 2, m, t + H / 2)[1]
    y_n = y + k2_y
    vy_n = vy + k2_vy
    return [x_n, y_n, vx_n, vy_n, t + H]



class Particle:
    def __init__(self, x, y, vx, vy, m, id):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.m = m
        self.r = np.sqrt(m)
        self.id = id

    def __eq__(self, other):
        if (isinstance(other, Particle)):
            return self.id == other.id
        return False

    def fly(self, h):
        self.x += self.vx * h
        self.y += self.vy * h

    def print(self):
        s = ''
        for d in [self.x, self.y, self.vx, self.vy, self.m, self.r]:
            s += str(d) + ','
        s = s[:-1]
        return s
    
    def F_g(self, p):
        dist = (self.x - p.x) ** 2 + (self.y - p.y) ** 2
        if dist == 0:
            return [9999, 9999]
        return  [self.m * p.m * (self.x - p.x) * dist, self.m * p.m * (self.y - p.y) * dist] 
    
    def F_interaction(self, particles):
        Fx, Fy = 0, 0
        for p in particles:
            if p.id != self.id:
                Force = self.F_g(p)
                Fx += Force[0]
                Fy += Force[1]
        return [Fx, Fy]
    
    def update_pos(self):
        calc = next_step(self.x, self.y, self.vx, self.vy, self.m, F)
        self.x, self.y = calc[0], calc[1]
        self.vx, self.vy = calc[2], calc[3]

# updates velocities of two particles ater 2 dim elastic collision. Equations derived from conservation of momentum and energy.
def update_velocities(p1, p2):
    m1, m2 = p1.m, p2.m
    dist = (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2
    if dist == 0:
        return
    temp1 = - (2 * m2 / (m1 + m2) * np.dot([p1.vx - p2.vx, p1.vy - p2.vy], [p1.x - p2.x, p1.y - p2.y])) / dist
    temp2 = - (2 * m2 / (m1 + m2) * np.dot([- p1.vx + p2.vx, - p1.vy + p2.vy], [-p1.x + p2.x, -p1.y + p2.y])) / dist
    v1x_new = p1.vx + temp1 * (p1.x - p2.x)
    v1y_new = p1.vy + temp1 * (p1.y - p2.y)
    v2x_new = p2.vx + temp2 * (p2.x - p1.x)
    v2y_new = p2.vy + temp2 * (p2.y - p1.y)
    p1.vx, p1.vy = v1x_new, v1y_new
    p2.vx, p2.vy = v2x_new, v2y_new


def handle_wall_collision(particles, range):
    for p in particles:
        if np.abs(p.x) > range:
            p.vx = -p.vx
        if np.abs(p.y) > range:
            p.vy = -p.vy


def approaching(p1, p2):
    return np.dot([p1.x - p2.x, p1.y - p2.y], [p1.vx - p2.vx, p1.vy - p2.vy]) < 0 


def colliding(p1, p2):
    return (np.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) < (p1.r + p2.r))

# finds and resolves collisions 
def handle_collisions(particles):
    particles = sorted(particles, key=lambda p: p.x)
    for i in range(len(particles) - 1):
        for j in range(i + 1, len(particles) - 1):
            if colliding(particles[i], particles[j]):
                update_velocities(particles[i], particles[j])
                n = 0
                while colliding(particles[i], particles[j]) and n < 100:
                    particles[i].fly(H)
                    particles[j].fly(H)
                    n+=1
            else:
                break
            





# returns list of randomly generated particles with given velocioty and mass range
def init_particles(number, size, v_min, v_max, m_min, m_max):
    from random import randrange
    particles = []
    X = np.arange(-size / 2 , size / 2 , np.sqrt(m_min))
    Y = np.arange(-size / 2 , size / 2 , np.sqrt(m_min))
    id = 0
    for i in range(number):
        m = randrange(int(m_min), int(m_max))
        vx = (-1) ** (randrange(0, 2)) * randrange(v_min, v_max)
        vy = (-1) ** (randrange(0, 2)) * randrange(v_min, v_max)
        rand_x_index = randrange(0, len(X) - 1)
        rand_y_index = randrange(0, len(Y) - 1)
        x = X[rand_x_index]
        y = Y[rand_y_index]
        particles.append(Particle(x, y, vx, vy, m, id))
        id += 1
    return particles




'''
def init_particles(number, size, v_min, v_max, m_min, m_max):
    from random import randrange
    n = 0
    particles = []
    X = np.arange(-size / 2 + m_max, size / 2 - m_max, 2 * m_max)
    Y = np.arange(-size / 2 + m_max, size / 2 - m_max, 2 * m_max)
    x_index, y_index = [], []
    for i in range(number):
        m = randrange(int(m_min), int(m_max))
        r = m
        vx = (-1) ** (randrange(0, 2)) * randrange(v_min, v_max)
        vy = (-1) ** (randrange(0, 2)) * randrange(v_min, v_max)
        rand_x_index = randrange(0, len(X) - 1)
        rand_y_index = randrange(0, len(Y) - 1)
        x = X[rand_x_index]
        y = Y[rand_y_index]
        particles.append(Particle(x, y, vx, vy, m, n))
        n += 1
    return particles
'''
