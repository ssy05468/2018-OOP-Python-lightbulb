import pygame
import container
import stone


window=container.screen('alkagit',700,700,(255,255,255))
screen=window.screen
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
