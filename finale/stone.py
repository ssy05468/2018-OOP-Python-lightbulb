import pygame
from math import *

class Particle_of_Stone: #처음 돌을 놓는 위치와 레벨을 전달받고, 반지름 질량은 기본값을 설정
    def __init__(self,start_x=10,start_y=10,radius=10,mass=1,level=1,surface=None, team=None, visible=1):
        self.radius=radius
        self.x=start_x
        self.y=start_y
        self.mass=mass
        self.level=level
        if team == 0 : self.color=(255,255,255)
        else : self.color=(150,150,200)
        self.isalive=True
        self.angle=0
        self.vel=0
        self.surface=surface
        self.team=team
        self.hidvel = 0
        self.hidang = 0
        self.visible=visible
    def move(self, dt): #전달받은 시간 간격에 속력을 곱해 돌의 위치를 이동시킨다. 속력은 0.95배로 계속 줄어든다.
        self.x += dt*self.vel * cos(radians(self.angle))
        self.y += dt*self.vel * sin(radians(self.angle))
        #print(self.angle, self.vel, self.x, self.y)

        if self.x > 650 :
            self.visible = 0
        if self.y > 550 :
            self.visible = 0
        if self.x < 150 :
            self.visible = 0
        if self.y < 50 :
            self.visible = 0
        self.vel=0.95*self.vel
        if abs(self.vel)<0.1 : self.vel=0


    def draw(self): #스크린에 돌을 그린다.
        pygame.draw.circle(
            self.surface,
            self.color,
            (int(self.x), int(self.y)),
            int(self.radius),
            0
        )