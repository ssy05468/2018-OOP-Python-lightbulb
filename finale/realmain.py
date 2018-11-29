from anglespeed import *
from Gravity4_makeit import *
from screen import *
from stone import *
from time import *
from pygame.locals import *
import random
import sys, os, traceback

# 돌의 개수
num_of_stone = 10

stone_particles = [Particle_of_Stone(start_x=(i-(i//5)*5)*150+90,start_y=(i//5)*580+10, team=i//5) for i in range(num_of_stone)]
num_particles = num_particles_orig
particles = [Particle(state=0) for i in range(num_particles)]

def new_draw():
    surface.fill((25,0,0))

    for p in particles :
        p.draw(surface)
        print(1)

    for q in stone_particles :
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