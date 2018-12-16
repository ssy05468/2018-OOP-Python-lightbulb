from anglespeed import *
from screen import *
from stone import *
import pygame

screen_size = [800,600]

#Movement substeps at the given timestep
movement_substeps = 1
#Target FPS
target_fps = 60.0
#dt (should be 1.0/target_fps for realtime, but you can change it to speed up or slow down time)
dt = 1.0/target_fps

icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
pygame.display.set_caption("OOP_LIGHTBULB")
surface = pygame.display.set_mode(screen_size)


pygame.init()

# 돌의 개수
num_of_stone = 10
now_select = 0
died_num = 0

scored=dict()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SELECTED = (200, 100, 50)
GRAY = (100, 100, 100)
fontObj = pygame.font.Font('NanumSquareRoundB.ttf', 16)

stone_particles = [Particle_of_Stone(start_x=(i-(i//5)*5)*70+250,start_y=(i//5)*450+80,mass=i, team=i//5,surface=surface) for i in range(num_of_stone)] #서피스(게임판)전달

#화면 생성
screen=screen('lightbulb',1000,600,(0,0,0)) #게임화면
window=screen.screen
surface=pygame.Surface((500,500)) #게임판
surface.fill((205,154,91)) #바둑판 색
window.blit(surface, (150, 50)) #바둑판 위치

def textprint(printobj, xcord=400, ycord=30):
    textSurfaceObj = fontObj.render(str(printobj), True, WHITE, BLACK)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (xcord, ycord)
    window.blit(textSurfaceObj, textRectObj)

def new_draw(): #돌 클래스에서 게임판을 전달받았으므로 draw에서 surface안써줘도됨
    window.fill((0,0,0))
    window.blit(surface, (150, 50))
    arrow(-stone_particles[now_select].angle)
    #for p in particles: # 중력장 돌
        # p.draw(surface)
    for q in stone_particles: # 바둑 돌
        if q.visible == 1 : q.draw()
    textprint(score())
    textprint("선택한 돌의 방향",800,530)

    for p in stone_particles :
        if p.mass == 0 :
            textprint("------- WHITE -------", 800, 100)
        if p.mass == 5 :
            textprint("-------  GRAY -------", 800, 230)
        if p.visible == 0:
            textprint("%d 은 죽었습니다."% (p.mass+1), 800, 120+p.mass*20+(p.mass//5)*30)
        else:
            textprint("%d 은 살아있습니다."% (p.mass+1), 800, 120+p.mass*20+(p.mass//5)*30)

    pygame.display.flip()

def new_move() :
    for i in range(movement_substeps):
        for p in stone_particles :
            if p.visible == 1 : p.move(dt/float(movement_substeps)) # 보일 때만 움직임
            for q in stone_particles :
                if p != q:
                    collide(p,q)
                    if q.visible == 0 and p.bycon == q.mass:
                        stone_particles[q.bycon].check_alive(q.mass)
                    if p.visible == 0 and q.bycon == p.mass:
                        stone_particles[p.bycon].check_alive(p.mass)

def arrow(angle):
    arrowimg = pygame.transform.scale(pygame.image.load('arrow.png').convert_alpha(), (64, 64))
    rotarrow = pygame.transform.rotate(arrowimg,angle)
    position = rotarrow.get_rect(center = (800,480))
    window.blit(rotarrow, position)

def score():
    global scored
    scored=dict()
    for i in stone_particles:
        scored.setdefault(i.team,0)
        if i.visible == -1 :
            sum = 0
        else : sum = i.visible
        scored[i.team]=scored[i.team]+sum

    if scored[0]==0 : return 'GRAY WIN'
    elif scored[1]==0 : return 'WHITE WIN'
    else : return 'White : ' + str(scored[0]) + ' vs Gray :' + str(scored[1]) + '\n'+ 'Selection :'+str(now_select+1)

def game_setting():
    global now_select
    clock = pygame.time.Clock()
    while True:
        temp = now_select

        vel, now_select = stoneshooting(stone_particles[now_select], now_select)
        stone_particles[now_select].color=SELECTED
        if now_select != temp :
            if stone_particles[temp].team == 0 : stone_particles[temp].color = WHITE
            else : stone_particles[temp].color = GRAY
        if vel == -111 and now_select == -111 : break
        stone_particles[now_select].vel = stone_particles[now_select].vel + vel
        new_move()
        new_draw()
        clock.tick(target_fps)

    pygame.quit()

try :
    game_setting()
except Exception :
    pass