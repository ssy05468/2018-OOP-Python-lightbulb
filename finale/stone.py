import pygame

class Particle_of_Stone:
    def __init__(self,start_x=10,start_y=10,radius=5,mass=1,level=1,screen=None,surface=None):
        self.radius=radius
        self.x=start_x
        self.y=start_y
        self.mass=mass
        self.level=level
        self.color=(0,0,0)
        self.isalive=True
        self.angle=0
        self.vel=0
        self.surface=surface
        
