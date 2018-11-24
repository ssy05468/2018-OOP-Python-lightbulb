import pygame
from pygame.locals import *
import sys, os, traceback
import random
from math import *
if sys.platform in ["win32","win64"]: os.environ["SDL_VIDEO_CENTERED"]="1"
pygame.display.init()
pygame.font.init()

#Set to -1 to choose at runtime
num_particles = 10
#Whether collisions are enabled
collisions = True
#Whether to contrain particles to the edges.  Not affected by the collisions enabled flag.
edge_clamp = False
#The amount to scale the particles' radius by
radius_scale = 30.0
#Particles' maximum (random) speed (pixels/sec)
max_initial_speed = 100.0
#The gravitational constant in this universe in pixels^3 kg^-1 s^-2.  The real one is 6.67384*(10^-11) m^3 kg^-1 s^-2
G = 00000
#Movement substeps at the given timestep
movement_substeps = 1
#Target FPS
target_fps = 120.0
#dt (should be 1.0/target_fps for realtime, but you can change it to speed up or slow down time)
dt = 1.0/target_fps
#flag는 움직임 시작할지에 대한 정보
flag=0
#마찰력
friction_constant = 20
#충돌 탄성 계수
elasticity = 0.75
#현재 지정해주는 임의의 속도
initial_vel = 100
#지정된 돌 바꾸는데 필요한 상수
now_move=0
if num_particles == -1:
    while True:
        try:
            num_particles = int(input("Number of particles: "))
            break
        except:
            print("Could not parse number.")
num_particles_orig = num_particles

width = 900
height = 600
screen_size = [width ,height]
icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
pygame.display.set_caption("Gravity Simulation - Ian Mallett - v.4.0.0 - 2013")
surface = pygame.display.set_mode(screen_size)

def rndint(num): return int(round(num))

class Particle(object):
    def __init__(self, pos=None,vel=None, mass=None, index=None):
        if pos == None: self.pos = [index*85-50,50]
        else:           self.pos = pos
        if mass == None:
            self.mass = 1.0
            self.hasmass = self.mass
        else:
            self.mass = mass/4
            self.hasmass = self.mass
        if vel == None:
            #angle = random.uniform(0.0,2.0*pi)
            self.angle=900
            r = self.mass # 반지름을 무게에 비례하게 만든다.
            self.vel = [0,0]
        else:
            self.vel = vel
       # self.mass=0
        self.forces = [0.0,0.0]
    def get_radius(self):
        #Assuming these objects are actually spheres, the radius scales with the cube root of
        #the mass.  If you prefer circle, change to the square root.
        self.radius = radius_scale*(self.hasmass**(1.0/3.0)) # 반지름 변수도 추가하였음
        return self.radius
    def set_velocity(particle1):
        angle = particle1.angle
        particle1.vel = [initial_vel*cos(angle), initial_vel*sin(angle)]
    def set_angle(particle1, setting_angle):
        particle1.angle = setting_angle
    @staticmethod
    def add_forces(particle1,particle2): # 만유인력에서의 힘 측정 (사용하지 않음)
        dx = particle2.pos[0] - particle1.pos[0]
        dy = particle2.pos[1] - particle1.pos[1]
        r_squared = dx*dx + dy*dy
        r = r_squared**0.5
        force_magnitude = (G * particle1.mass * particle2.mass) / r_squared #F=G*M1*M2/(r^2)
        dx_normalized_scaled = (dx / r) * force_magnitude
        dy_normalized_scaled = (dy / r) * force_magnitude
        particle1.forces[0] += dx_normalized_scaled
        particle1.forces[1] += dy_normalized_scaled
        particle2.forces[0] -= dx_normalized_scaled
        particle2.forces[1] -= dy_normalized_scaled
    @staticmethod
    def get_collided(particle1,particle2): # 충돌 감지 (현재 사용하고 있음)
        r1 = particle1.get_radius()
        r2 = particle2.get_radius()
        both = r1 + r2
        abs_dx = abs(particle2.pos[0] - particle1.pos[0])
        if abs_dx > both: return False
        abs_dy = abs(particle2.pos[1] - particle1.pos[1])
        if abs_dy > both: return False
        #The above lines are just some optimization.  This is the real test.
        if abs_dx*abs_dx + abs_dy*abs_dy > both*both: return False
        return True
    def move(self, dt):
        self.pos[0] += dt * self.vel[0]
        self.pos[1] += dt * self.vel[1]
        #a_x = dt * self.forces[0] / self.mass #F=MA -> A=F/M
        #a_y = dt * self.forces[1] / self.mass
        #while abs(a_x)>width: a_x/=10.0 #This can happen, especially without collisions
        #while abs(a_y)>height: a_y/=10.0

        # 마찰력 부분입니다....
        # 마찰력 부분입니다....
        a_x=0
        a_y=0

        if self.vel[0]!=0 and self.vel[1]!=0 :
            a_x = -self.vel[0]/abs(self.vel[0])*friction_constant
            a_y = -self.vel[1]/abs(self.vel[1])*friction_constant

        self.vel[0] += dt*a_x
        self.vel[1] += dt*a_y

        if a_x/abs(a_x)<0 and a_y/abs(a_y)<0:
            if self.vel[0] < 0 and self.vel[1] < 0:
                self.vel[0] = 0
                self.vel[1] = 0
        elif a_x/abs(a_x)>0 and a_y/abs(a_y)<0:
            if self.vel[0] > 0 and self.vel[1] < 0:
                self.vel[0] = 0
                self.vel[1] = 0
        elif a_x/abs(a_x)<0 and a_y/abs(a_y)>0:
            if self.vel[0] < 0 and self.vel[1] > 0:
                self.vel[0] = 0
                self.vel[1] = 0
        elif a_x/abs(a_x)>0 and a_y/abs(a_y)>0:
            if self.vel[0] > 0 and self.vel[1] > 0:
                self.vel[0] = 0
                self.vel[1] = 0

    def draw(self, surface):
        pygame.draw.circle(
            surface,
            (255,255,255),
            (rndint(self.pos[0]),rndint(screen_size[1]-self.pos[1])),
            rndint(self.get_radius()),
            0
        )
    # 다른 코드에서 가지고 온 내용
    def bounce(self):
        global elasticity
        if self.x > width - self.radius:
            self.x = 2 * (width - self.radius) - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        if self.y > height - self.size:
            self.y = 2 * (height - self.size) - self.y
            self.angle = pi - self.angle
            self.speed *= elasticity

        elif self.y < self.size:
            self.y = 2 * self.size - self.y
            self.angle = pi - self.angle
            self.speed *= elasticity

def setup_particles():
    global particles # 입자 class를 담고 있는 리스트
    global num_particles
    num_particles = num_particles_orig
    particles = [Particle(mass=i, index=i) for i in range(1, num_particles+1)]

def get_input():
    global flag
    global particles
    global now_move
    keys_pressed = pygame.key.get_pressed()
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_position = pygame.mouse.get_pos()
    mouse_rel = pygame.mouse.get_rel()

    for event in pygame.event.get():
        if   event.type == QUIT: return False
        elif event.type == KEYDOWN:
            if   event.key == K_ESCAPE: return False
            elif event.key == K_r: setup_particles() #reset
            elif event.key == K_m: flag=1 # m키가 눌리면 움직이기 시작한다
            elif event.key == K_s : flag=0
            elif event.key == K_1 :
                Particle.set_velocity(particle1=particles[1])
                now_move=1
            elif event.key == K_2 :
                Particle.set_velocity(particle1=particles[2])
                now_move = 2
            elif event.key == K_3:
                Particle.set_velocity(particle1=particles[3])
                now_move = 3
            elif event.key == K_RIGHT :
                Particle.set_angle(particle1=particles[now_move], setting_angle=0)
            elif event.key == K_LEFT :
                Particle.set_angle(particle1=particles[now_move], setting_angle=pi)
            elif event.key == K_UP :
                Particle.set_angle(particle1=particles[now_move], setting_angle=pi/2)
            elif event.key == K_DOWN:
                Particle.set_angle(particle1=particles[now_move], setting_angle=pi*3/2)
    #if flag==1 : collision_detect()

    return True
def move():
    for i in range(movement_substeps):
        for j in range(0,num_particles,1):
            for k in range(j+1,num_particles,1):
                Particle.add_forces(particles[j],particles[k]) #중력의 영향으로 힘을 가해주는 부분
        for p in particles:
            p.move(dt/float(movement_substeps))

def new_move() :
    for i in range(movement_substeps):
        for j in range(0,num_particles,1):
            print(particles[j].angle)
            if particles[j].vel != [0,0] and particles[j].angle != 900:
                particles[j].move(dt/float(movement_substeps))

def collide():
    for i in range(0,num_particles,1):
        for j in range(i+1,num_particles,1):
            p1 = particles[i]
            p2 = particles[j]
            if Particle.get_collided(p1,p2):
                dx = p1.pos[0] - p2.pos[0]
                dy = p1.pos[1] - p2.pos[1]

                tangent = atan2(dy, dx)
                angle = 0.5 * pi + tangent

                angle1 = 2 * tangent - p1.angle
                angle2 = 2 * tangent - p2.angle
                speed1x = p2.vel[0] * elasticity
                speed1y = p2.vel[1] * elasticity
                speed2x = p1.vel[0] * elasticity
                speed2y = p1.vel[1] * elasticity

                (p1.angle) = (angle1)
                (p2.angle) = (angle2)

                p1.vel = [speed1x, speed1y]
                p2.vel = [speed2x, speed2y]
                p1.pos[0] += sin(angle)
                p1.pos[1] -= cos(angle)
                p2.pos[0] -= sin(angle)
                p2.pos[1] += cos(angle)

def collision_detect():
    global particles
    global num_particles
    new_particles = []
    dead_particles = []
    for i in range(0,num_particles,1):
        for j in range(i+1,num_particles,1):
            p1 = particles[i]
            p2 = particles[j]
            if Particle.get_collided(p1,p2):
                #Remove both colliding particles
                dead_particles.append(p1)
                dead_particles.append(p2)
                #Replace with a single particle with their properties
                mv_x = p1.mass*p1.vel[0] + p2.mass*p2.vel[0]
                mv_y = p1.mass*p1.vel[1] + p2.mass*p2.vel[1]
                mass = p1.mass + p2.mass
                new_particles.append(Particle(
                    [(p1.pos[0]*p1.mass+p2.pos[0]*p2.mass)/mass,(p1.pos[1]*p1.mass+p2.pos[1]*p2.mass)/mass], #center of mass
                    [mv_x/mass, mv_y/mass], #momentum is conserved but not kinetic energy
                    mass
                ))
    if len(dead_particles) != 0:
        temp = []
        for p in particles:
            if p in dead_particles: continue
            temp.append(p)
        particles = temp
    particles += new_particles
    num_particles = len(particles)
def clamp_to_edges():
    for p in particles:
        r = p.get_radius()
        if p.pos[0]<=               r: p.vel[0]= abs(p.vel[0])
        if p.pos[1]<=               r: p.vel[1]= abs(p.vel[1])
        if p.pos[0]>=screen_size[0]-r: p.vel[0]=-abs(p.vel[0])
        if p.pos[1]>=screen_size[1]-r: p.vel[1]=-abs(p.vel[1])
def draw():
    surface.fill((25,0,0))
    
    for p in particles:
        p.draw(surface)
        
    pygame.display.flip()

def main():
    global flag
    global particles

    setup_particles()
    clock = pygame.time.Clock()
    while True:
        if not get_input(): break
        #if flag==1 : move()
        if flag==1 : new_move() # 새로운 동작코드
        #if collisions: collision_detect() # 충돌을 감지한다.
        if collisions: collide() # 바꾼 코드인데 충돌 감지해서 튕기기 가능
        if edge_clamp: clamp_to_edges() # 현재는 False 상태
        draw()
        clock.tick(target_fps)
    pygame.quit()
    
if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        pygame.quit()
        input()