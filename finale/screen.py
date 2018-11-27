import pygame

class screen:
    def __init__(self,name,width,height,color):
        self.width=width
        self.height=height
        self.color=color
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(name)
        self.screen.fill(self.color)
