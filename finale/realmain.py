from anglespeed import *
from Gravity4_makeit import *
from screen import *
from stone import *
from time import *

# 돌의 개수
num_of_stone = 5

stone_particles = [Particle_of_Stone() for i in range(num_of_stone)]

def game_setting():
    setup_particles()
    clock = pygame.time.clock()


usemain()

