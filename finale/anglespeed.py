import sys, pygame, math
import easygui
from pygame.locals import *
"""
unpressed=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
"""
def stoneshooting(STONE):
    stone = STONE
    #print(stone.angle)
    angle_data = stone.angle
    vel_data = stone.vel
    #print(pygame.event.get())
    for event in pygame.event.get():
        print(event.type==K_UP)
        if event.type == K_ESCAPE : pass
        if stone.angle == 360: stone.angle = 0
        if stone.angle == -1: stone.angle = 359

        if event.type == KEYDOWN :
            if event.key == K_a or event.key == K_LEFT:
                stone.angle += 1
            elif event.key == K_d or event.key == K_RIGHT:
                stone.angle -= 1
                print(1)
            if event.key == K_w or event.key == K_UP:
                stone.vel += 1
                stone.vel = stone.vel % 100
            elif event.key == K_s or event.key == K_DOWN:
                stone.vel -= 1
                stone.vel = -stone.vel % 100
            if event.key == K_SPACE:
                return [stone.vel, stone.angle]

    return [vel_data,angle_data]

"""
    stone.x += stone.vel*math.cos(math.radians(stone.angle))
    stone.y -= stone.vel*math.sin(math.radians(stone.angle))
    stone.vel *= 0.95

    rotcar = pygame.transform.rotate(stone.surface, stone.angle)
    position = rotcar.get_rect(center = (stone.x,stone.y))
    SCREEN.blit(rotcar, position)
    pygame.display.update()
    FPS.tick(24)
"""