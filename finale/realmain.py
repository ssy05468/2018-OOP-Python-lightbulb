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

stone_particles = [Particle_of_Stone(start_x=(i-(i//5)*5)*70+110,start_y=(i//5)*460+15, team=i//5,surface=surface) for i in range(num_of_stone)] #서피스(게임판)전달
num_particles = num_particles_orig
particles = [Particle(state=0) for i in range(num_particles)] #중력장을 위한 요소

#화면 생성
screen=screen('lightbulb',800,600,(0,0,0)) #게임화면
window=screen.screen
surface=pygame.Surface((500,500)) #게임판
surface.fill((205,154,91)) #바둑판 색
window.blit(surface, (150, 50)) #바둑판 위치


def new_draw(): #돌 클래스에서 게임판을 전달받았으므로 draw에서 surface안써줘도됨
    window.fill((0,0,0))
    window.blit(surface, (150, 50))
    for p in particles:
         p.draw(surface)
         print(1)

    for q in stone_particles:
        q.draw(surface)

    pygame.display.flip()

def new_move() :
    for i in range(movement_substeps):
        for p in stone_particles :
            p.move(dt/float(movement_substeps))

def game_setting():
    setup_particles()
    clock = pygame.time.Clock()
    while True:
        #if not get_input() : break
        vel, angle = stoneshooting(stone_particles[1])
        if vel == -111 and angle == -111 : break
        #print(stone_particles[1].vel, stone_particles[1].angle)
        stone_particles[1].vel,stone_particles[1].angle = stone_particles[1].vel + vel, stone_particles[1].angle + angle
        new_move()
        new_draw()
        clock.tick(target_fps)

    pygame.quit()


game_setting()
