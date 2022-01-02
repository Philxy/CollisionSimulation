import pygame
import matplotlib.pyplot as plt
import numpy as np

part_data = open('collisionData.txt', 'r')

s = part_data.readline().split()
H, n, size = float(s[0]), float(s[1]), float(s[2])
frame_size = 1000
scaling = frame_size / size


#  turns string from text file into a float array containing part data
def get_particles(str_data):
    s = str_data.split()
    particles = []
    for c in s:
        lmao = c.split(",")
        p_data = []
        for m in lmao:
            p_data.append(float(m))
        particles.append(p_data)
    return particles


'''
with open("velocities.txt", "r") as a_file:
    xdata = range(0, len(a_file.readline().strip().split(' ')))
    i = 1
    for line in a_file:
        stripped_line = line.strip()
        line_as_array = line.split(' ')
        line_as_array.pop()
        print(i)
        i += 1
        plt.clf()
        plt.plot(xdata, line_as_array)
        ax = plt.gca()
        ax.invert_yaxis()

        plt.pause(0.000001)
'''



pygame.init()
screen1 = pygame.display.set_mode([frame_size, frame_size])

running = True
while running:
    screen1.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    particles = get_particles(part_data.readline())
    for p in particles:
        pygame.draw.circle(screen1, (255, 255, 255),
                           (int(p[0] * scaling + frame_size / 2), int(p[1] * scaling + frame_size / 2)),
                           int(p[5] * scaling))

    pygame.display.flip()
    #pygame.time.wait(1)

pygame.quit()
part_data.close()