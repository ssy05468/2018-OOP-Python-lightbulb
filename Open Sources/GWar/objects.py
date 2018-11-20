import pygame, os
from math import *
from random import *
from colorsys import *

import gwglob, wepmodules

weapon_packs = []
weapons = {}

def normalabsangle(a):
	if a < 0:
		return (2*pi) - (-a % (2*pi))
	return a % (2*pi)

def in_polygon(point, polygon):
	r = False
	for i in range(len(polygon)):
		if ((polygon[i][1] <= point[1] and point[1] < polygon[i-1][1]) or \
				(polygon[i-1][1] <= point[1] and point[1] < polygon[i][1])) and \
				point[0] < (polygon[i-1][0] - polygon[i][0]) * (point[1] - polygon[i][1]) / (polygon[i-1][1] - polygon[i][1]) + polygon[i][0]:
			r = not r
	return r

def distance(p1,p2):
	return sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def angle_between(point,origion):
	return atan2(point[1]-origion[1],point[0]-origion[0])

def circlerect_overlap(point, r, rect):
	test = list(point)
	if test[0] < rect[0][0]:
		test[0] = rect[0][0]
	if test[0] > rect[0][0]+rect[1][0]:
		test[0] = rect[0][0]+rect[1][0]
	if test[1] < rect[0][1]:
		test[1] = rect[0][1]
	if test[1] > rect[0][1]+rect[1][1]:
		test[1] = rect[0][1]+rect[1][1]
	return (point[0]-test[0])**2+(point[1]-test[1])**2 < r**2

# Closest point on circle to point
def circle_point(point, position, size):
	v = Vector(magnitude=size, angle=angle_between(point,position))
	return v.project(position)

# Closest point on rect to point
def rect_point(point, rectpoint, size):
	if point[0] < rectpoint[0]:
		x = rectpoint[0]
	elif point[0] > rectpoint[0]:
		x = rectpoint[0] + size[0]
	if point[1] < rectpoint[1]:
		y = rectpoint[1]
	elif point[1] > rectpoint[1]:
		y = rectpoint[1] + size[1]
	return [x,y]

def lineline_intersect(x1,y1,x2,y2, x3,y3,x4,y4):
	d = (y4-y3)*(x2-x1)-(x4-x3)*(y2-y1)
	if d:
		ua,ub = ((x4-x3)*(y1-y3)-(y4-y3)*(x1-x3))/d,((x2-x1)*(y1-y3)-(y2-y1)*(x1-x3))/d
		if 0 <= ua <= 1 and 0 <= ub <= 1:
			x,y = x1 + ua * (x2 - x1),y1 + ua * (y2 - y1)
			return ([x,y], sqrt((x4 - x)**2+(y4 - y)**2))

# (x3 - x1)(x2 - x1) + (y3 - y1)(y2 - y1) + (z3 - z1)(z2 - z1)
# ------------------------------------------------------------
# (x2 - x1)(x2 - x1) + (y2 - y1)(y2 - y1) + (z2 - z1)(z2 - z1)
def linecircle_intersect(x1,y1,x2,y2, x3,y3,r):
	a = (x2-x1)**2+(y2-y1)**2
	b = 2*((x2-x1)*(x1-x3)+(y2-y1)*(y1-y3))
	c = x3**2+y3**2+x1**2+y1**2-2*(x3*x1+y3*y1)-r**2
	s = b**2-4*a*c
	if s == 0:
		u = -b/(2*a)
	elif s > 0:
		u1,u2 = (-b+sqrt(s))/(2*a),(-b-sqrt(s))/(2*a)
		if 0 <= u1 <= 1:
			u = u1
		else:
			u = u2
		return [x1+u*(x2-x1),y1+u*(y2-y1)]

class Vector:
	def __init__(self, xcomponent=None, ycomponent=None, magnitude=None, angle=None):
		if xcomponent == None or ycomponent == None:
			self.set_vector(magnitude, angle)
		else:
			self.set_components(xcomponent,ycomponent)

	def __getitem__(self, n):
		return (self.xcomponent,self.ycomponent)[n]

	def set_vector(self, magnitude, angle):
		self.magnitude = magnitude
		self.angle = angle
		self.xcomponent = magnitude * cos(angle)
		self.ycomponent = magnitude * sin(angle)

	def set_components(self, xcomponent, ycomponent):
		self.magnitude = (xcomponent**2+ycomponent**2)**0.5
		self.angle = atan2(ycomponent, xcomponent)
		self.xcomponent = xcomponent
		self.ycomponent = ycomponent

	def project(self, point):
		return [point[0]+self.xcomponent,point[1]+self.ycomponent]

	def __add__(self, other):
		self.set_components(self.xcomponent + other[0],self.ycomponent + other[1])

class Gravity:
	def __init__(self, mass, position):
		self.mass = mass
		self.position = position

	def tug(self, object):
		try:
			magnitude = (gwglob.GRAV_CONST * self.mass * object.mass) / ((self.position[0]-object.position[0])**2+(self.position[1]-object.position[1])**2)
		except:
			magnitude = 0
		angle = angle_between(self.position,object.position)
		object += Vector(magnitude=magnitude, angle=angle)

class Map:
	def __init__(self):
		self.size = (1000,800)
		self.planets = [
			# (50,400,[400,400],0),
			# (50,400,[600,400],0),
			(150,300,[200,200],pi/40.0),
			(75,250,[700,200],pi/40.0),
			(25,200,[500,400],pi/40.0),
			(75,250,[300,600],pi/40.0),
			(150,300,[800,600],-pi/40.0)
		]

class Object(Gravity, Vector):
	def __init__(self, screen, mass, position, life, xcomponent=None, ycomponent=None, magnitude=None, angle=None):
		self.screen = screen
		self.life = life
		self.lastposition = None
		if position:
			self.lastposition = list(position)
		Gravity.__init__(self, mass, position)
		Vector.__init__(self, xcomponent, ycomponent, magnitude, angle)

	def collide(self, other):
		return False

	def collision(self, other, position):
		pass

	def draw(self):
		pass

	def update(self):
		if self.life > 0:
			self.life -= 1
		elif self.life == 0:
			return False
		self.lastposition = list(self.position)
		self.position[0] += self.xcomponent
		self.position[1] += self.ycomponent
		return True

bullet_icon = pygame.Surface((16,16))
bullet_icon.fill((0,0,0))

class Bullet(Object):
	icon = bullet_icon
	basedamage = 100
	color = (0,0,255)
	size = 2
	debry = True

	def update(self):
		inside = self.screen.rect.collidepoint(self.position)
		if self.life > 0:
			if inside:
				self.life = -1
		elif self.life == -1 and not inside:
			if self.mass == 0:
				self.life = 0
			else:
				self.life = gwglob.SHOT_OUTSIDE_LIFE
		return Object.update(self)

	def draw(self):
		if circlerect_overlap(self.position, self.size, (self.screen.camera,gwglob.SIZE)):
			if self.size > 1:
				pygame.draw.circle(self.screen.screen, self.color, self.screen.translate(self.position), self.size, 0)
			else:
				self.screen.screen.set_at(self.screen.translate(self.position), self.color)

	# Overwrite for custom
	def damage(self):
		return self.basedamage

	def collision(self, other, position, debry=True):
		if debry and self.debry:
			angle = angle_between(position,other.position)
			for _ in range(gwglob.particles('debry')):
				self.screen.newobjects.append(Debry(self.screen,list(position),(random()*2-1) * (pi/2.0) + angle))
		if isinstance(other, Player):
			other.damage(self.damage())

class Planet(Object):
	def __init__(self, screen, size, mass, position, rotation, xcomponent=None, ycomponent=None, magnitude=None, angle=None):
		self.size = size
		self.rotation = rotation
		n = 255 * (mass / float(gwglob.MASS_MAX))
		self.color = (n,255-n,0)
		self.players = []
		Object.__init__(self, screen, mass, position, -1, 0, 0)

	def tug(self, object):
		try:
			magnitude = (gwglob.GRAV_CONST * self.mass * object.mass) / ((self.position[0]-object.position[0])**2+(self.position[1]-object.position[1])**2-self.size)
		except:
			magnitude = 0
		angle = angle_between(self.position,object.position)
		object += Vector(magnitude=magnitude, angle=angle)

	def collide(self, other):
		if not isinstance(other, Explosion) and sqrt((self.position[0]-other.position[0])**2+(self.position[1]-other.position[1])**2) - other.size <= self.size:
			return circle_point(other.position, self.position, self.size+other.size)

	def draw(self):
		if circlerect_overlap(self.position, self.size, (self.screen.camera,gwglob.SIZE)):
			p = self.screen.translate(self.position)
			pygame.draw.circle(self.screen.screen, (0,0,0), p, self.size)
			pygame.draw.circle(self.screen.screen, self.color, p, self.size, 1)

	def place_players(self):
		if self.players:
			split = (2*pi) / len(self.players)
			start = 360 * random()
			for n,p in enumerate(self.players):
				angle = start + split * n + 30 * (random()*2-1)
				p.set_positioning(self, angle)

class Explosion(Object):
	def __init__(self, screen, size, speed, position, damage, maxlast=10, color=None):
		self.maxsize = size
		self.size = 0
		self.diff = (size * 2) / float(speed)
		self.damage = damage
		self.maxlast = maxlast
		self.stay = 0
		self.color = color
		Object.__init__(self, screen, 0, position, -1, 0, 0)

	def draw(self):
		if not self.stay:
			self.size += self.diff
			if self.size >= self.maxsize:
				self.diff = -self.diff
				self.stay = self.maxlast
			elif self.size <= 0:
				self.life = 0
		else:
			self.stay -= 1
		if self.color == None:
			color = [255*c for c in hls_to_rgb(gwglob.EXPLOSION_RANGE[0] + random() * (gwglob.EXPLOSION_RANGE[1]-gwglob.EXPLOSION_RANGE[0]), 0.5, 1)]
		else:
			color = self.color
		if self.size > 0 and circlerect_overlap(self.position, self.size, (self.screen.camera,gwglob.SIZE)):
			pygame.draw.circle(self.screen.screen, color, self.screen.translate(self.position), self.size)

	def collision(self, other, position, debry=True):
		if isinstance(other, Player):
			other.damage(self.damage)
		return True

class Debry(Object):
	def __init__(self, screen, position, angle, startcolor=(255,255,255), endcolor=(0,0,0)):
		self.size = 1
		Object.__init__(self, screen, 0, position, gwglob.DEBRY_LIFE, magnitude=3, angle=angle)
		self.colordata = zip(endcolor,((endcolor[0]-startcolor[0])/self.life,(endcolor[1]-startcolor[1])/self.life,(endcolor[2]-startcolor[2])/self.life))

	def draw(self):
		if pygame.Rect(self.screen.camera,gwglob.SIZE).collidepoint(self.position):
			self.screen.screen.set_at(self.screen.translate(self.position), [e - c * self.life for e,c in self.colordata])

class Toolbox(Object,pygame.Rect):
	def __init__(self, screen, player):
		self.player = player
		self.topweapon = 0
		self.minimized = False
		Object.__init__(self, screen, 0, player.toolboxposition, -1, 0, 0)
		self.radar = pygame.Rect(gwglob.TOOLBOX_RADAR,gwglob.TOOLBOX_RADARDIM)
		self.listbox = pygame.Rect(gwglob.TOOLBOX_LINE,gwglob.TOOLBOX_LINESDIM)
		self.up = pygame.Rect(gwglob.TOOLBOX_SCROLLUP,gwglob.TOOLBOX_SCROLLBUTTON)
		self.down = pygame.Rect(gwglob.TOOLBOX_SCROLLDOWN,gwglob.TOOLBOX_SCROLLBUTTON)
		self.scroll = pygame.Rect(gwglob.TOOLBOX_SCROLL,gwglob.TOOLBOX_SCROLLDIM)
		self.minimize = pygame.Rect((gwglob.TOOLBOX_MINIMIZE[0]+1,gwglob.TOOLBOX_MINIMIZE[1]+1),gwglob.TOOLBOX_MINIMIZEDIM)
		self.update_static()
		pygame.Rect.__init__(self, list(self.position), gwglob.TOOLBOX_SIZE)

	def resize(self, minimize=None):
		if minimize != None:
			self.minimized = minimize
		else:
			self.minimized = not self.minimized
		self.player.minimized = self.minimized
		if self.minimized:
			self.height = gwglob.TOOLBOX_TITLEHEIGHT+2
		else:
			self.size = gwglob.TOOLBOX_SIZE
			self.move([min(gwglob.SIZE[0]-self.width,self.position[0]),min(gwglob.SIZE[1]-self.height,self.position[1])])

	def click(self, point):
		if self.collidepoint(point):
			if self.radar.collidepoint(point):
				r = float(self.screen.galaxysize[0])/gwglob.TOOLBOX_RADARDIM[0]
				self.screen.camera = [min(self.screen.galaxysize[0]-gwglob.SIZE[0],max(0,(point[0]-self.radar.topleft[0])*r-gwglob.SIZE[0]/2)),min(self.screen.galaxysize[1]-gwglob.SIZE[1],max(0,(point[1]-self.radar.topleft[1])*r-gwglob.SIZE[1]/2))]
				return
			if self.listbox.collidepoint(point):
				self.player.weapon = self.topweapon + (point[1]-self.listbox.topleft[1])/gwglob.TOOLBOX_LINEHEIGHT
				return
			if self.up.collidepoint(point):
				self.topweapon = max(0,self.topweapon-1)
				return
			if self.down.collidepoint(point):
				self.topweapon = min(len(self.player.weapons)-gwglob.TOOLBOX_LINES,self.topweapon+1)
				return
			if self.scroll.collidepoint(point):
				self.topweapon = min(len(self.player.weapons)-gwglob.TOOLBOX_LINES,int(len(self.player.weapons) * ((point[1] - self.scroll.topleft[1]) / float(self.scroll.height))))
				return
			if self.minimize.collidepoint(point):
				self.resize()
				return
			return True

	def move(self, position):
		self.position = position
		self.player.toolboxposition = list(position)
		self.topleft = list(position)
		self.listbox.topleft = (self.position[0]+gwglob.TOOLBOX_LINE[0],self.position[1]+gwglob.TOOLBOX_LINE[1])
		self.up.topleft = (self.position[0]+gwglob.TOOLBOX_SCROLLUP[0],self.position[1]+gwglob.TOOLBOX_SCROLLUP[1])
		self.down.topleft = (self.position[0]+gwglob.TOOLBOX_SCROLLDOWN[0],self.position[1]+gwglob.TOOLBOX_SCROLLDOWN[1])
		self.scroll.topleft = (self.position[0]+gwglob.TOOLBOX_SCROLL[0],self.position[1]+gwglob.TOOLBOX_SCROLL[1])
		self.minimize.topleft = (self.position[0]+gwglob.TOOLBOX_MINIMIZE[0]+1,self.position[1]+gwglob.TOOLBOX_MINIMIZE[1]+1)

	def update_static(self, player=None):
		self.player.topweapon = self.topweapon
		if player:
			self.player = player
		if self.player.toolbox:
			self.static = self.player.toolbox
			self.topweapon = self.player.topweapon
			self.resize(self.player.minimized)
			self.trans = self.player.trans
			self.move(list(self.player.toolboxposition))
		else:
			self.topweapon = 0
			self.static = pygame.Surface(gwglob.TOOLBOX_SIZE)
			self.static.lock()
			self.static.fill(self.player.color)
			pygame.draw.circle(self.static, (0,0,0), gwglob.TOOLBOX_DIAL, 20, 0)
			pygame.draw.rect(self.static, self.player.color, ((gwglob.TOOLBOX_DIAL[0]-gwglob.TOOLBOX_DIALLENGTH,gwglob.TOOLBOX_DIAL[1]),(gwglob.TOOLBOX_DIALLENGTH*2,gwglob.TOOLBOX_DIALLENGTH)), 0)
			pygame.draw.circle(self.static, (0,0,0), (gwglob.TOOLBOX_DIALTEXT[0]+gwglob.TOOLBOX_DIALWIDTH+3,gwglob.TOOLBOX_DIALTEXT[1]+3), 2, 1)
			pygame.draw.rect(self.static, (0,0,0), ((1,1),(gwglob.TOOLBOX_SIZE[0]-2,gwglob.TOOLBOX_SIZE[1]-2)), 1)
			pygame.draw.line(self.static, (0,0,0), (1,gwglob.TOOLBOX_TITLEHEIGHT), (gwglob.TOOLBOX_SIZE[0]-2,gwglob.TOOLBOX_TITLEHEIGHT), 1)
			pygame.draw.rect(self.static, (0,0,0), (gwglob.TOOLBOX_MINIMIZE, (gwglob.TOOLBOX_MINIMIZEDIM[0]+2,gwglob.TOOLBOX_MINIMIZEDIM[1]+2)), 1)
			pygame.draw.rect(self.static, (0,0,0), ((gwglob.TOOLBOX_POWER[0]-1,gwglob.TOOLBOX_POWER[1]-1),(gwglob.TOOLBOX_POWERDIM[0]+2,gwglob.TOOLBOX_POWERDIM[1]+2)), 0)
			pygame.draw.rect(self.static, (0,0,0), (gwglob.TOOLBOX_RADAR,gwglob.TOOLBOX_RADARDIM), 0)
			pygame.draw.rect(self.static, (0,0,0), ((gwglob.TOOLBOX_LINE[0]-1,gwglob.TOOLBOX_LINE[1]-1),(gwglob.TOOLBOX_LINESDIM[0]+2,gwglob.TOOLBOX_LINESDIM[1]+2)), 1)
			pygame.draw.rect(self.static, (0,0,0), ((gwglob.TOOLBOX_SCROLLUP[0]-1,gwglob.TOOLBOX_SCROLLUP[1]-1),(gwglob.TOOLBOX_SCROLLBUTTON[0]+2,gwglob.TOOLBOX_LINESDIM[1]+2)), 0)
			pygame.draw.rect(self.static, self.player.color, (gwglob.TOOLBOX_SCROLLUP,gwglob.TOOLBOX_SCROLLBUTTON), 0)
			pygame.draw.rect(self.static, self.player.color, (gwglob.TOOLBOX_SCROLLDOWN,gwglob.TOOLBOX_SCROLLBUTTON), 0)
			self.static.unlock()
			self.static.blit(gwglob.FONT.render(self.player.name, gwglob.ANTI_ALIAS, (0,0,0), self.player.color), (3,3))
			self.player.toolbox = self.static
			if self.player.color == (1,0,0):
				self.trans = (2,0,0)
			else:
				self.trans = (1,0,0)
			self.player.trans = self.trans
			self.move([gwglob.SIZE[0]-50-gwglob.TOOLBOX_SIZE[0],50])
			self.resize(False)

	def draw(self):
		if self.minimized:
			mini = self.static.copy()
			mini.set_colorkey(self.trans)
			pygame.draw.rect(mini, self.trans, ((0,gwglob.TOOLBOX_TITLEHEIGHT+2),(gwglob.TOOLBOX_SIZE[0],gwglob.TOOLBOX_SIZE[1]-gwglob.TOOLBOX_TITLEHEIGHT+2)), 0)
			mini.set_at((1,gwglob.TOOLBOX_TITLEHEIGHT+1), self.player.color)
			mini.set_at((gwglob.TOOLBOX_SIZE[0]-2,gwglob.TOOLBOX_TITLEHEIGHT+1), self.player.color)
			pygame.draw.rect(mini, (0,0,0), ((gwglob.TOOLBOX_MINIMIZE[0]+2,gwglob.TOOLBOX_MINIMIZE[1]+2),(gwglob.TOOLBOX_MINIMIZEDIM[0]-2,gwglob.TOOLBOX_MINIMIZEDIM[1]-2)), 1)
			pygame.draw.line(mini, (0,0,0), (gwglob.TOOLBOX_MINIMIZE[0]+3,gwglob.TOOLBOX_MINIMIZE[1]+3), (gwglob.TOOLBOX_MINIMIZE[0]+gwglob.TOOLBOX_MINIMIZEDIM[0]-2,gwglob.TOOLBOX_MINIMIZE[1]+3), 1)
			self.screen.screen.blit(mini, self.position)
		else:
			self.screen.screen.blit(self.static, self.position)
			pygame.draw.rect(self.screen.screen, (0,0,0), ((self.position[0]+gwglob.TOOLBOX_MINIMIZE[0]+2,self.position[1]+gwglob.TOOLBOX_MINIMIZE[1]+gwglob.TOOLBOX_MINIMIZEDIM[1]-2),(gwglob.TOOLBOX_MINIMIZEDIM[0]-2,2)))
			v = Vector(magnitude=20, angle=self.player.aiming-pi/2.0)
			dial = (gwglob.TOOLBOX_DIAL[0]+self.position[0],gwglob.TOOLBOX_DIAL[1]+self.position[1])
			pygame.draw.line(self.screen.screen, (255,255,255), dial, v.project(dial))
			self.screen.screen.blit(gwglob.FONT.render('%d' % degrees(self.player.aiming), gwglob.ANTI_ALIAS, (0,0,0), self.player.color), (self.position[0]+gwglob.TOOLBOX_DIALTEXT[0]+gwglob.TOOLBOX_DIALWIDTH-gwglob.FONT.size('%d' % degrees(self.player.aiming))[0],self.position[1]+gwglob.TOOLBOX_DIALTEXT[1]))
			powerbar = (self.position[0]+gwglob.TOOLBOX_POWER[0],self.position[1]+gwglob.TOOLBOX_POWER[1])
			power,maxpower = max(1,int(gwglob.TOOLBOX_POWERDIM[0] * (self.player.power / gwglob.PLAYER_MAXPOWER))),max(1,int(gwglob.TOOLBOX_POWERDIM[0] * (self.player.maxpower / gwglob.PLAYER_MAXPOWER)))
			if power < maxpower:
				pygame.draw.rect(self.screen.screen, self.player.color, (powerbar, (maxpower,gwglob.TOOLBOX_POWERDIM[1])), 1)
			pygame.draw.rect(self.screen.screen, self.player.color, (powerbar, (power,gwglob.TOOLBOX_POWERDIM[1])), 0)
			self.screen.screen.blit(gwglob.FONT.render('%d/%d' % (self.player.power,self.player.maxpower), gwglob.ANTI_ALIAS, (0,0,0), self.player.color), (self.position[0]+gwglob.TOOLBOX_POWERTEXT[0],self.position[1]+gwglob.TOOLBOX_POWERTEXT[1]))
			if len(self.player.weapons) > gwglob.TOOLBOX_LINES:
				n = gwglob.TOOLBOX_SCROLLDIM[1] / float(len(self.player.weapons))
				pygame.draw.rect(self.screen.screen, self.player.color, ((self.position[0]+gwglob.TOOLBOX_SCROLLBAR[0],self.position[1]+gwglob.TOOLBOX_SCROLLBAR[1]+n*self.topweapon),(gwglob.TOOLBOX_SCROLLBUTTON[0],n*gwglob.TOOLBOX_LINES)), 0)
			for n,d in enumerate(zip(self.player.weapons[self.topweapon:self.topweapon+gwglob.TOOLBOX_LINES],self.player.ammo[self.topweapon:self.topweapon+gwglob.TOOLBOX_LINES])):
				w,a = d
				h = gwglob.FONT.size(str(a))[0]
				p = (self.position[0]+gwglob.TOOLBOX_LINE[0],self.position[1]+gwglob.TOOLBOX_LINE[1]+gwglob.TOOLBOX_LINEHEIGHT*n)
				self.screen.screen.blit(weapons[w][0].icon, p)
				self.screen.screen.blit(weapons[w][2], (p[0]+gwglob.ICON_SIZE[0]+1,p[1]), ((0,0),(gwglob.TOOLBOX_LINEWIDTH-2,p[1])))
				self.screen.screen.blit(gwglob.FONT.render(str(a), gwglob.ANTI_ALIAS, (0,0,0)), (p[0]+gwglob.TOOLBOX_LINEWIDTH+gwglob.ICON_SIZE[0]-1,p[1]))
				if self.topweapon + n == self.player.weapon:
					pygame.draw.rect(self.screen.screen, (0,0,0), ((p[0]-1,p[1]-1), (gwglob.TOOLBOX_LINESDIM[0]+2, gwglob.TOOLBOX_LINEHEIGHT+2)), 1)
			if self.screen.galaxysize[0] > self.screen.galaxysize[1]:
				fixx,fixy = 0,(gwglob.TOOLBOX_RADARDIM[0] - (gwglob.TOOLBOX_RADARDIM[0] * (self.screen.galaxysize[1] / float(self.screen.galaxysize[0])))) / 2
				pygame.draw.rect(self.screen.screen, self.player.color, ((self.position[0]+gwglob.TOOLBOX_RADAR[0],self.position[1]+gwglob.TOOLBOX_RADAR[1]),(gwglob.TOOLBOX_RADARDIM[0],fixy)), 0)
				pygame.draw.rect(self.screen.screen, self.player.color, ((self.position[0]+gwglob.TOOLBOX_RADAR[0],self.position[1]+gwglob.TOOLBOX_RADAR[1]+gwglob.TOOLBOX_RADARDIM[1]-fixy),(gwglob.TOOLBOX_RADARDIM[0],fixy)), 0)
			else:
				fixy,fixx = 0,(gwglob.TOOLBOX_RADARDIM[0] - (gwglob.TOOLBOX_RADARDIM[0] * (self.screen.galaxysize[0] / float(self.screen.galaxysize[1])))) / 2
				pygame.draw.rect(self.screen.screen, self.player.color, ((self.position[0]+gwglob.TOOLBOX_RADAR[0],self.position[1]+gwglob.TOOLBOX_RADAR[1]),(fixx,gwglob.TOOLBOX_RADARDIM[1])), 0)
				pygame.draw.rect(self.screen.screen, self.player.color, ((self.position[0]+gwglob.TOOLBOX_RADAR[0]+gwglob.TOOLBOX_RADARDIM[0]-fixx,self.position[1]+gwglob.TOOLBOX_RADAR[1]),(fixx,gwglob.TOOLBOX_RADARDIM[0])), 0)
			r = gwglob.TOOLBOX_RADARDIM[0]/float(self.screen.galaxysize[0])
			v = Vector(0,0)
			self.radar.topleft = (self.position[0]+fixx+gwglob.TOOLBOX_RADAR[0],self.position[1]+fixy+gwglob.TOOLBOX_RADAR[1])
			self.radar.size = (gwglob.TOOLBOX_RADARDIM[0]-fixx*2,gwglob.TOOLBOX_RADARDIM[1]-fixy*2)
			for p in self.screen.planets:
				pos = (self.radar.topleft[0]+p.position[0]*r,self.radar.topleft[1]+p.position[1]*r)
				pygame.draw.circle(self.screen.screen, p.color, pos, int(p.size*r), 1)
				for pl in p.players:
					v.set_vector(int(p.size*r)+1,pl.angle)
					pygame.draw.circle(self.screen.screen, pl.color, v.project(pos), 2, 0)
			pygame.draw.rect(self.screen.screen, (255,255,255), ((self.radar.topleft[0]-1+self.screen.camera[0]*r,self.radar.topleft[1]-1+self.screen.camera[1]*r),(gwglob.SIZE[0]*r+2,gwglob.SIZE[1]*r+2)), 1)

class Player(Object):
	def __init__(self, screen, name, weapons, ammo, color):
		self.body = None
		self.turret = None
		self.planet = None
		self.toolbox = None
		self.toolboxposition = None
		self.topweapon = 0
		self.name = name
		self.color = color
		self.aiming = 0
		self.maxpower = gwglob.PLAYER_MAXPOWER
		self.power = gwglob.PLAYER_MAXPOWER
		self.weapons = weapons
		self.ammo = ammo
		self.weapon = 0
		self.gas = 0
		self.camera = None
		self.minimized = False
		self.trans = (1,0,0)
		Object.__init__(self, screen, 0, [0,0], -1, 0, 0)

	def set_positioning(self, planet, angle):
		self.planet = planet
		v = Vector(magnitude=planet.size,angle=angle)
		self.position = v.project(planet.position)
		self.set_vector(0, angle)
		self.body = []
		vect = Vector(0,0)
		last = len(gwglob.PLAYER)-1
		for n,v in enumerate(gwglob.PLAYER):
			vect.set_components(*v)
			vect.set_vector(vect.magnitude,vect.angle + self.angle)
			p = vect.project(self.position)
			if not n or n == last:
				p = circle_point(p, self.planet.position, self.planet.size)
			self.body.append(p)
		vect.set_components(*gwglob.PLAYER_TURRET_BASE)
		vect.set_vector(vect.magnitude,vect.angle + self.angle)
		self.turret = [vect.project(self.position)]
		vect.set_vector(1,vect.angle + pi/2.0)
		self.turret.append(vect.project(self.turret[0]))
		vect.set_vector(-vect.magnitude,vect.angle)
		self.turret.append(vect.project(self.turret[0]))

	def rotate(self):
		self.set_positioning(self.planet, self.angle+self.planet.rotation)

	def damage(self, dmg):
		self.maxpower -= dmg
		self.power = min(self.power,self.maxpower)
		if self.maxpower < 1:
			self.screen.newexplosions.append(Explosion(self.screen, 50, 30, list(self.position), 1, 20))
			self.screen.players.remove(self)
			self.planet.players.remove(self)

	def collide(self, other):
		closest = 9999
		point = None
		a = other.angle or angle_between(other.position,self.position)
		v = Vector(magnitude=other.size,angle=a)
		x3,y3 = v.project(other.position)
		v.set_vector(-v.magnitude,v.angle)
		x4,y4 = v.project(other.lastposition)
		for n in range(len(self.body)):
			x1,y1 = self.body[n]
			x2,y2 = self.body[n-1]
			d = (y4-y3)*(x2-x1)-(x4-x3)*(y2-y1)
			if d:
				ua,ub = ((x4-x3)*(y1-y3)-(y4-y3)*(x1-x3))/d,((x2-x1)*(y1-y3)-(y2-y1)*(x1-x3))/d
				if 0 <= ua <= 1 and 0 <= ub <= 1:
					x,y = x1 + ua * (x2 - x1),y1 + ua * (y2 - y1)
					distance = sqrt((x4 - x)**2+(y4 - y)**2)
					if distance < closest:
						closest = distance
						point = [x,y]
		if point:
			v.set_vector(magnitude=-1, angle=a)
			point = v.project(point)
		return point

	def draw(self):
		if self.planet:
			draw = self.body[:len(gwglob.PLAYER)/2]
			draw.append(self.turret[1])
			v = Vector(magnitude=8, angle=self.angle + self.aiming)
			turretend = v.project(self.turret[0])
			v.set_vector(1, v.angle + pi/2.0)
			draw.append(v.project(turretend))
			v.set_vector(-1, v.angle)
			draw.append(v.project(turretend))
			draw.append(self.turret[2])
			draw.extend(self.body[len(gwglob.PLAYER)/2:])
			d = []
			lastpoint = None
			for rp in draw:
				p = self.screen.translate(rp)
				d.append(p)
				if lastpoint:
					pygame.draw.line(self.screen.screen, self.color, lastpoint, p, 1)
				lastpoint = p
			pygame.draw.polygon(self.screen.screen, self.color, d, 0)

wepmodules.load_weapons()