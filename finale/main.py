import sys, pygame, math
from pygame.locals import *
pygame.init()

SCREEN = pygame.display.set_mode((800, 600))
car = pygame.transform.scale(pygame.image.load('Car.png').convert_alpha(), (64, 64))
pygame.display.set_caption('Car Game')
pygame.display.set_icon(car)
FPS = pygame.time.Clock()

carX  = 400
carY  = 100
angle = 90
speed = 0

while True:

    if angle == 360: angle = 0
    if  angle == -1: angle = 359

    SCREEN.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[K_a] or keys[K_LEFT]:
        angle += speed
    elif keys[K_d] or keys[K_RIGHT]:
        angle -= speed
    if keys[K_w] or keys[K_UP]:
        speed += 1
    elif keys[K_s] or keys[K_DOWN]:
        speed -= 0.5

    carX += speed*math.cos(math.radians(angle))
    carY -= speed*math.sin(math.radians(angle))
    speed *= 0.95

    rotcar = pygame.transform.rotate(car, angle)
    position = rotcar.get_rect(center = (carX,carY))
    SCREEN.blit(rotcar, position)

    pygame.display.update()
    FPS.tick(24)