import sys, pygame, math
import easygui
from pygame.locals import *
"""
unpressed=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
"""

plus_vel = 20
plus_ang = 5
def stoneshooting(STONE):
    stone = STONE
    #print(stone.angle)
    angle_data = stone.angle
    vel_data = stone.vel
    #print(angle_data, vel_data)
    #print(pygame.event.get())
    for event in pygame.event.get():

        if stone.angle == 360: stone.angle = 0
        if stone.angle == -1: stone.angle = 359
<<<<<<< HEAD
        SCREEN.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        """
        if math.fabs(stone.vel)>0.6:
            keys=unpressed
        """
        if keys[K_a] or keys[K_LEFT]:
            stone.angle += 1
        elif keys[K_d] or keys[K_RIGHT]:
            stone.angle -= 1
        if keys[K_w] or keys[K_UP]:
            stone.vel += 0.1
            stone.vel = stone.vel % 10
        elif keys[K_s] or keys[K_DOWN]:
            stone.vel -= 0.1
            stone.vel = stone.vel % 10
        if keys[K_SPACE]:
            return [stone.vel, stone.angle]
    rotcar = pygame.transform.rotate(stone.surface, stone.angle)
    position = rotcar.get_rect(center = (stone.x,stone.y))
    SCREEN.blit(rotcar, position)
    pygame.display.update()
    FPS.tick(24)
=======
        if event.type== QUIT : return -111, -111
        if event.type == KEYDOWN :
            if event.key == K_ESCAPE : return -111, -111
            if event.key == K_a or event.key == K_LEFT:
                stone.hidang += plus_ang
            elif event.key == K_d or event.key == K_RIGHT:
                stone.hidang -= plus_ang
            elif event.key == K_w or event.key == K_UP:
                stone.hidvel += plus_vel
                stone.hidvel = stone.hidvel % 100
            elif event.key == K_s or event.key == K_DOWN:
                stone.hidvel -= plus_vel
                stone.hidvel = -stone.hidvel % 100
            elif event.key == K_SPACE:
                a, b = stone.hidvel, stone.hidang
                stone.hidvel, stone.hidang = 0,0
                return a,b

    return 0,0
>>>>>>> 38d52a28a4a692ba903d54f298ebcbac150b5eac

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