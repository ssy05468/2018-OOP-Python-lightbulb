from anglespeed import *
from Gravity4_makeit import *
from screen import *
from stone import *
from time import *

# 돌의 개수
num_of_stone = 5

stone_particles = [Particle_of_Stone() for i in range(num_of_stone)]

def new_draw():
    surface.fill((25,0,0))

    for p in particles :
        p.draw(surface)

    for p in stone_particles :
        p.draw(surface)

    pygame.display.flip()

def new_move() :
    '''
    for i in range(movement_substeps):
        for j in range(0, num_particles,1):
            for k in range(0, num_of_stone,1):
                Particle.add_forces
    '''
    for p in stone_particles :
        p.move(dt/float(movement_substeps))
def game_setting():
    setup_particles()
    clock = pygame.time.clock()
    while True:
        if not get_input() : break
        stoneshooting(stone_particles[1])
        move()
        new_draw()
        clock.tick(target_fps)
    pygame.quit()


usemain()

