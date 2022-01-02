import numpy as np
import utility as util


size = 1000
n = 100
t_max = 50

v_min = 50
v_max = 51
m_min = 100
m_max = 101

particles = util.init_particles(n, size, v_min, v_max, m_min, m_max)

data = open("collisionData.txt", "w")
data.write(str(util.H) + " " + str(n) + " " + str(size) + "\n")

for t in np.arange(0, t_max, util.H):
    util.handle_collisions(particles)
    s = ''
    for p in particles:
        p.update_pos()
        s += p.print()
        s += ' '   
    data.write(s + '\n')
    new_vel_counts = ""
    if int(t / util.H) % 1000 == 0:
        print('Progress:', round(100 * t/t_max, 2), '%')
    util.handle_wall_collision(particles, size/2)
data.close()

import pltfile

