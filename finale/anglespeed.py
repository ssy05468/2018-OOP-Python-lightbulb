import sys, pygame, math
import easygui
from pygame.locals import *
"""
unpressed=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
"""

plus_vel = 100
plus_ang = 5
def stoneshooting(STONE):
    stone = STONE
    #print(stone.angle)
    angle_data = stone.angle #발사각
    vel_data = stone.vel #발사속도
    #print(angle_data, vel_data)
    #print(pygame.event.get())
    for event in pygame.event.get(): #키보드 입력을 받는다.

        if stone.angle == 360: stone.angle = 0
        if stone.angle == -1: stone.angle = 359
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
            elif event.key == K_SPACE: #스페이스바를 입력받으면 설정한 각도와 속도를 저장한 후 돌의 속도와 각도를 다시 0으로 초기화한다.
                a, b = stone.hidvel, stone.hidang
                stone.hidvel, stone.hidang = 0,0
                return a,b

    return 0,0

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
