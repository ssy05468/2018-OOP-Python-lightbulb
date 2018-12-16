import pygame

def ending(winner):
    pygame.init()
    font = pygame.font.Font("NanumSquareRoundB.ttf", 80)
    txt="Congratulations! " + winner
    txt=txt.center(38,' ')
    text = font.render(txt, True, (255, 255, 255))
    screen = pygame.display.set_mode((1300, 100))

    while True:
        for event in pygame.event.get():
            if pygame.KEYDOWN == event.type:
                if pygame.K_ESCAPE == event.key:
                    return
            if pygame.QUIT == event.type:
                return

        screen.fill((0, 0, 0))
        screen.blit(text, text.get_rect())
        pygame.display.flip()
