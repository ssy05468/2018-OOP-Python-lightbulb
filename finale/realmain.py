from anglespeed import *
from Gravity4_makeit import *
from screen import *
from stone import *
from time import *
import pygame
from pygame.locals import *
import random
import sys, os, traceback

pygame.init()

# 돌의 개수
num_of_stone = 10
# 무엇을 선택했나요
now_select = 0

scored=dict()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
fontObj = pygame.font.Font('NanumSquareRoundB.ttf', 16)

stone_particles = [Particle_of_Stone(start_x=(i-(i//5)*5)*70+250,start_y=(i//5)*450+80, team=i//5,surface=surface) for i in range(num_of_stone)] #서피스(게임판)전달
num_particles = num_particles_orig
particles = [Particle(state=0) for i in range(num_particles)] #중력장을 위한 요소

#화면 생성
screen=screen('lightbulb',800,600,(0,0,0)) #게임화면
window=screen.screen
surface=pygame.Surface((500,500)) #게임판
surface.fill((205,154,91)) #바둑판 색
window.blit(surface, (150, 50)) #바둑판 위치
def textprint(printobj, xcord=400, ycord=30):
    textSurfaceObj = fontObj.render(str(printobj), True, WHITE, BLACK)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (xcord, ycord)
    window.blit(textSurfaceObj, textRectObj)

def new_draw(): #돌 클래스에서 게임판을 전달받았으므로 draw에서 surface안써줘도됨
    window.fill((0,0,0))
    window.blit(surface, (150, 50))
    arrow(-stone_particles[now_select].angle)
    for p in particles:
         p.draw(surface)
    for q in stone_particles:
        if q.visible == 1 : q.draw()
    textprint(score())
    textprint("선택한 돌의 방향",720,550)
    pygame.display.flip()

def new_move() :
    for i in range(movement_substeps):
        for p in stone_particles :
            p.move(dt/float(movement_substeps))
            for q in stone_particles :
                if p != q :
                    p.collide(q)

def arrow(angle):
    arrowimg = pygame.transform.scale(pygame.image.load('arrow.png').convert_alpha(), (64, 64))
    rotarrow = pygame.transform.rotate(arrowimg,angle)
    position = rotarrow.get_rect(center = (720,500))
    window.blit(rotarrow, position)

def score():
    global scored
    scored=dict()
    for i in stone_particles:
        scored.setdefault(i.team,0)
        scored[i.team]=scored[i.team]+i.visible

    if scored[0] == 0 : print()
    return 'White : ' + str(scored[0]) + ' vs Gray :' + str(scored[1]) + '\n'+ 'Selection :'+str(now_select+1) + 'angle  :' +str(stone_particles[now_select].angle)

def game_setting():
    global now_select
    setup_particles()
    clock = pygame.time.Clock()
    while True:
        #if not get_input() : break
        vel, now_select = stoneshooting(stone_particles[now_select], now_select)
        if vel == -111 and now_select == -111 : break
        stone_particles[now_select].vel = stone_particles[now_select].vel + vel
        new_move()
        new_draw()
        clock.tick(target_fps)

    pygame.quit()

game_setting()
