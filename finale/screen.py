import pygame

class screen:
    def __init__(self,name,width=900,height=600,color=[255,255,255]):
        self.width=width
        self.height=height
        self.color=color
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(name)
        self.screen.fill(self.color)