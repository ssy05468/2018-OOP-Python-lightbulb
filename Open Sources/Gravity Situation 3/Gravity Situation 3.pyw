import pygame
from pygame.locals import *
import random, math, sys

pygame.init()

pygame.display.set_caption("Gravity Simulation 3.0.0 - Earth and Exploding Sun - Ian Mallett")
Surface = pygame.display.set_mode((800,600))
PlanetSurface = pygame.Surface((800,600))
PlanetSurface.fill((0,0,0))
SunSurface = pygame.Surface((800,600))
SunSurface.fill((0,0,0))
SunSurface.set_colorkey((0,0,0))

Particles = []
class Particle:
    def __init__(self,x,y,speedx,speedy,mass,Color=(255,255,255)):
        self.x = x
        self.y = y
        self.speedx = speedx
        self.speedy = speedy
        self.mass = mass
        self.radius = math.sqrt(mass)
        self.color = Color
    def explode(self):
        ParticleNumber = 300
        Theta = 0.0
        ThetaIncrement = 360.0/ParticleNumber
        RadiusLooper = 0
        Radius = [10,15,20,25,30,35,40,35,30,25,20,15]
        for x in xrange(ParticleNumber):
            R = Radius[RadiusLooper]
            Speed = 3.0#random.random()*2.0
            XPos = self.x + R*math.cos(math.radians(Theta))
            YPos = self.y + R*math.sin(math.radians(Theta))
            XSpeed = Speed*math.cos(math.radians(Theta))
            YSpeed = Speed*math.sin(math.radians(Theta))
            Mass = self.mass/float(ParticleNumber)
            Particles.append(Particle(XPos,YPos,XSpeed,YSpeed,Mass))
            Theta += ThetaIncrement
            RadiusLooper += 1
            if RadiusLooper == 12:
                RadiusLooper = 0
        self.mass = 0.0001
        self.radius = 0
##Particles.append(Particle(400,300,0,0,100))
##Particles.append(Particle(400,200,-.35,0,4))
Particles.append(Particle(400,300,0,0,1000))#Sun
Particles.append(Particle(400,240,-1.4,0,4,(100,0,0)))#Mercury
##Particles.append(Particle(400,200,-1.1,0,4,(0,0,255)))#Venus
Particles.append(Particle(400,160,-0.95,0,4,(255,255,0)))#Venus
Particles.append(Particle(400,80,-0.75,0,4,(0,100,255)))#Earth
Particles.append(Particle(400,0,-0.65,0,4,(255,0,0)))#Mars
def Move():
    for P in Particles:
        for P2 in Particles:
            if P != P2:
                XDiff = P.x - P2.x
                YDiff = P.y - P2.y
                Distance = math.sqrt((XDiff**2)+(YDiff**2))
                if Distance < 10: Distance = 10
                #F = (G*M*M)/(R**2)
                Force = 0.125*(P.mass*P2.mass)/(Distance**2)
                #F = M*A  ->  A = F/M
                Acceleration = Force / P.mass
                XComponent = XDiff/Distance
                YComponent = YDiff/Distance
                P.speedx -= Acceleration * XComponent
                P.speedy -= Acceleration * YComponent
    for P in Particles:
        P.x += P.speedx
        P.y += P.speedy
def CollisionDetect():
    for P in Particles:
        if P.color == (255,255,255):
##            if P.x > 800-P.radius:   P.x = 800-P.radius;  P.speedx *= -1
##            if P.x < 0+P.radius:     P.x = 0+P.radius;    P.speedx *= -1
##            if P.y > 600-P.radius:   P.y = 600-P.radius;  P.speedy *= -1
##            if P.y < 0+P.radius:     P.y = 0+P.radius;    P.speedy *= -1
            for P2 in Particles:
                if P != P2:
                    if P2.color == (255,255,255):
                        Distance = math.sqrt(  ((P.x-P2.x)**2)  +  ((P.y-P2.y)**2)  )
                        if Distance < (P.radius+P2.radius):
                            P.speedx = ((P.mass*P.speedx)+(P2.mass*P2.speedx))/(P.mass+P2.mass)
                            P.speedy = ((P.mass*P.speedy)+(P2.mass*P2.speedy))/(P.mass+P2.mass)
                            P.x = ((P.mass*P.x)+(P2.mass*P2.x))/(P.mass+P2.mass)
                            P.y = ((P.mass*P.y)+(P2.mass*P2.y))/(P.mass+P2.mass)
                            P.mass += P2.mass
                            P.radius = math.sqrt(P.mass)
                            Particles.remove(P2)
def Draw():
    SunSurface.fill((0,0,0))
    for P in Particles:
        if P.color == (255,255,255):
            pygame.draw.circle(SunSurface, P.color, (int(P.x),int(600-P.y)), int(round(P.radius)))
        else:
            pygame.draw.circle(PlanetSurface, P.color, (int(P.x),int(600-P.y)), int(round(P.radius)))
##        Surface.set_at((int(P.x),int(600-P.y)),(255,255,255))
    Surface.blit(PlanetSurface,(0,0))
    Surface.blit(SunSurface,(0,0))
    pygame.display.flip()
def GetInput():
    keystate = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT or keystate[K_ESCAPE]:
            pygame.quit(); sys.exit()
    if keystate[K_F1]:
        Particles[0].explode()
        try:  Particles.remove(Particle)
        except:  pass
def main():
    while True:
        GetInput()
        Move()
        CollisionDetect()
        Draw()
if __name__ == '__main__': main()
