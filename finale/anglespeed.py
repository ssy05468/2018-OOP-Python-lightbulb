import pygame
from pygame.locals import *


plus_vel = 250 # 한번의 클릭으로 더해지는 속도
plus_ang = -10 # 한번의 클릭으로 생겨나는 각도

def stoneshooting(STONE, selectstone, turn):
    now_select = selectstone
    stone = STONE

    for event in pygame.event.get(): #키보드 입력을 받는다.
        if stone.angle == 360: stone.angle = 0
        if stone.angle == -1: stone.angle = 359
        if event.type== QUIT : return -111, -111, turn
        if event.type == KEYDOWN :
            if event.key == K_ESCAPE : return -111, -111, turn
            if event.key == K_1 :
                now_select = 0 + turn * 5
            elif event.key == K_2 :
                now_select = 1 + turn * 5
            elif event.key == K_3 :
                now_select = 2 + turn * 5
            elif event.key == K_4 :
                now_select = 3 + turn * 5
            elif event.key == K_5 :
                now_select = 4 + turn * 5
            elif event.key == K_6 :
                if turn == 1 : now_select = 5
                else : now_select = 0
            elif event.key == K_7 :
                if turn == 1 : now_select = 6
                else : now_select = 1
            elif event.key == K_8 :
                if turn == 1 : now_select = 7
                else : now_select = 2
            elif event.key == K_9 :
                if turn == 1 : now_select = 8
                else : now_select = 3
            elif event.key == K_0 :
                if turn == 1 : now_select = 9
                else : now_select = 4
            if event.key == K_a or event.key == K_LEFT:
                stone.angle+=plus_ang

            elif event.key == K_d or event.key == K_RIGHT:
                stone.angle-=plus_ang

            elif event.key == K_w or event.key == K_UP:
                if stone.hidvel<1000:
                    stone.hidvel += plus_vel

            elif event.key == K_s or event.key == K_DOWN:
                if stone.hidvel>0:
                    stone.hidvel -= plus_vel

            elif event.key == K_SPACE and stone.vel==0: #스페이스바를 입력받았을 때 진행하고 있는 상태라면 설정한 속도를 저장한 후 돌의 속도와 각도를 다시 0으로 초기화한다.
                a = stone.hidvel
                stone.hidvel = 0
                stone.bycon = -1
                turn = 1-turn
                return a,now_select, turn

    return 0,now_select,turn