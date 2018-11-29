import pygame
from math import *

class Particle_of_Stone:
    def __init__(self,start_x=10,start_y=10,radius=10,mass=1,level=1,screen=None,surface=None, team=None):
        self.radius=radius
        self.x=start_x
        self.y=start_y
        self.mass=mass
        self.level=level
        self.color=(255,255,255)
        self.isalive=True
        self.angle=0
        self.vel=0
        self.surface=surface
        self.team=team
        self.hidvel = 0
        self.hidang = 0
    def move(self, dt):
        self.x += dt*self.vel * cos(radians(self.angle))
        self.y += dt*self.vel * sin(radians(self.angle))
        #print(self.angle, self.vel, self.x, self.y)
        self.vel=0.95*self.vel
        if abs(self.vel)<0.1 : self.vel=0

    def draw(self, surface):
        pygame.draw.circle(
            surface,
            self.color,
            (int(self.x), int(self.y)),
            int(self.radius),
            0
        )
