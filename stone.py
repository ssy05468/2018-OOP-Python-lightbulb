import pygame

class stone:

    def __init__(self,start_x,start_y,radius,mass,level,screen,surface):
        self.radius=radius
        self.x=start_x
        self.y=start_y
        self.mass=mass
        self.level=level
        self.color=(0,0,0)
        self.isalive=True
        self.angle=0
        self.velocity=0
        self.surface=surface
        
