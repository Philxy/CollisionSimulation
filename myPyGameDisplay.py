import util
import pygame
from random import randrange
pygame.init()


frame_size = 500
size = 100
scaling = frame_size/size

objects = []

for i in range(0, 50):
    m = util.Mass(randrange(-10, 10), randrange(-10, 10), 0, 0, 1, 1)
    objects.append(m)


# Set up the drawing window
screen = pygame.display.set_mode([frame_size, frame_size])

# Run until the user asks to quit
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Fill Background
    screen.fill((255, 255, 255))
    # Calculation
    for m in objects:
        m.update()
        pygame.draw.circle(screen, (0, 0, 255), (int(m.x * scaling + frame_size/2), int((m.y * scaling) + frame_size/2)), int(m.radius * scaling))

    #print(len(util.collsion_occurence(objects)))
    pygame.display.flip()
pygame.quit()
