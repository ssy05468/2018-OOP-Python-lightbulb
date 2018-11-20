import pygame,os
from math import *
from random import random
from colorsys import *

__doc__ = """Galaxy War Default Weapon Pack"""

oneshot_icon = pygame.Surface(gwglob.ICON_SIZE)
pygame.draw.circle(oneshot_icon, (0,0,255), (8,8), 2, 0)

class OneShot(objects.Bullet):
	icon = oneshot_icon

	def __init__(self, screen, position, power, angle):
		objects.Bullet.__init__(self, screen, 1, position, -1, magnitude=5 * (power / gwglob.PLAYER_MAXPOWER), angle=angle)

	def collision(self, other, position):
		self.screen.newexplosions.append(objects.Explosion(self.screen, 30, 30, list(position), 1))
		objects.Bullet.collision(self, other, position)

threeshot_icon = pygame.Surface(gwglob.ICON_SIZE)
for p in ((8,7),(4,9),(12,9)):
	pygame.draw.circle(threeshot_icon, (0,0,255), p, 2, 0)

class ThreeShot(OneShot):
	icon = threeshot_icon

	def __init__(self, screen, position, power, angle):
		OneShot.__init__(self, screen, position, power, angle)
		screen.newbullets.append(OneShot(screen, list(position), power, angle+pi/36.0))
		screen.newbullets.append(OneShot(screen, list(position), power, angle-pi/36.0))

jackhammer_icon = pygame.Surface(gwglob.ICON_SIZE)
pygame.draw.circle(jackhammer_icon, (0,0,255), (7,3), 2, 0)
for p in [(7,7),(7,11),(7,15),(9,13),(12,11),(15,9)]:
	jackhammer_icon.set_at(p, (255,255,255))

class Jackhammer(objects.Bullet):
	icon = jackhammer_icon

	def __init__(self, screen, position, power, angle, size=5):
		self.size = size
		self.power = power
		objects.Bullet.__init__(self, screen, 1, position, -1, magnitude=5 * (power / gwglob.PLAYER_MAXPOWER), angle=angle)

	def collision(self, other, position):
		angle = objects.angle_between(position,other.position)
		for _ in range(gwglob.particles('debry')):
			a = (random()*2-1) * (pi/2.0) + angle
			self.screen.newobjects.append(objects.Debry(self.screen,list(position),a))
		self.screen.newexplosions.append(objects.Explosion(self.screen, 10*self.size, 30, list(position), 1))
		if self.size > 2:
			self.screen.newbullets.append(Jackhammer(self.screen, list(position), self.size+300, angle, self.size-1))
		objects.Bullet.collision(self, other, position)

hopper_icon = pygame.Surface(gwglob.ICON_SIZE)
pygame.draw.circle(hopper_icon, (0,0,255), (13,5), 2, 0)
for p in [(0,6),(3,7),(5,10),(7,15),(9,10),(11,7)]:
	hopper_icon.set_at(p, (255,255,255))

class Hopper(objects.Bullet):
	icon = hopper_icon

	def __init__(self, screen, position, power, angle):
		self.power = power
		self.bounces = 10
		objects.Bullet.__init__(self, screen, 1, position, -1, magnitude=5 * (power / gwglob.PLAYER_MAXPOWER), angle=angle)

	def collision(self, other, position):
		if isinstance(other, objects.Planet) and self.bounces:
			if objects.distance(self.lastposition,self.position) <= 1:
				objects.Bullet.collision(self, other, position)
				return
			a1,a2 = self.angle+pi,objects.angle_between(position,other.position)
			d1,d2 = a1-(a2+pi/2.0),a1-(a2-pi/2.0)
			if abs(d1) < abs(d2):
				angle = a2-pi/2.0-d1
			else:
				angle = a2+pi/2.0-d2
			self.set_vector(magnitude=self.magnitude-self.magnitude/5, angle=angle)
			self.position = list(position)
			self.bounces -= 1
			return True
		self.screen.newexplosions.append(objects.Explosion(self.screen, 30, 30, list(position), 1))
		objects.Bullet.collision(self, other, position)

# Not a weapon. Used by Sprinkler.
class WaterDrop(objects.Bullet):
	color = (255,255,255)
	size = 1
	basedamage = 20

	def __init__(self, screen, position, angle):
		v = objects.Vector(magnitude=2,angle=angle)
		objects.Bullet.__init__(self, screen, 1, v.project(position), 100, magnitude=2, angle=angle)

	def collision(self, other, position):
		self.screen.newexplosions.append(objects.Explosion(self.screen, 10, 20, list(position), 1, 5))
		objects.Bullet.collision(self, other, position)

sprinkler_icon = pygame.Surface(gwglob.ICON_SIZE)
pygame.draw.circle(sprinkler_icon, (0,0,255), (13,5), 2, 0)
for p in [(6,3),(9,5),(10,8),(8,11),(5,12),(2,10),(1,7),(3,4)]:
	sprinkler_icon.set_at(p, (255,255,255))

class Sprinkler(objects.Bullet):
	icon = sprinkler_icon

	def __init__(self, screen, position, power, angle):
		self.sprinkle = 75
		objects.Bullet.__init__(self, screen, 1, position, -1, magnitude=5 * (power / gwglob.PLAYER_MAXPOWER), angle=angle)

	def update(self):
		if not self.sprinkle:
			for a in range(8):
				self.screen.newbullets.append(WaterDrop(self.screen, self.position, pi/4.0 * a))
			self.sprinkle = 100
		else:
			self.sprinkle -= 1
		return objects.Bullet.update(self)

	def collision(self, other, position):
		self.screen.newexplosions.append(objects.Explosion(self.screen, 20, 30, list(position), 1))
		objects.Bullet.collision(self, other, position)

chainreaction_icon = pygame.Surface(gwglob.ICON_SIZE)
for p in ((5,4),(6,13),(14,10)):
	chainreaction_icon.set_at(p, (0,0,255))
for p,s in (((8,8),4),((13,3),2),((1,9),3)):
	pygame.draw.circle(chainreaction_icon, (128,0,0), p, s, 0)

class ChainReaction(objects.Bullet):
	icon = chainreaction_icon
	debry = False

	def __init__(self, screen, position, power, angle, piece=3):
		self.piece = piece
		self.die = -1
		if piece < 3:
			self.die = 15
			self.basedamage = 50
		objects.Bullet.__init__(self, screen, 1, position, -1, magnitude=5 * (power / gwglob.PLAYER_MAXPOWER), angle=angle)

	def update(self):
		inside = self.screen.rect.collidepoint(self.position)
		if self.life > 0:
			if inside:
				self.life = -1
		elif self.life == -1 and not inside:
			self.life = gwglob.SHOT_OUTSIDE_LIFE
		if self.life == 0 or self.die == 0:
			if self.die == 0 or self.piece < 3:
				self.collision(self, self.position)
			return False
		if self.die > 0:
			self.die -= 1
		if self.life > 0:
			self.life -= 1
		self.lastposition = list(self.position)
		self.position[0] += self.xcomponent
		self.position[1] += self.ycomponent
		return True

	def collision(self, other, position):
		self.screen.newexplosions.append(objects.Explosion(self.screen, 50 - 10 * (3-self.piece), 30 + 5 * (3-self.piece), list(position), 1, 0))
		if self.piece:
			angle = objects.angle_between(position,other.position)
			v = objects.Vector(magnitude=1,angle=angle)
			for _ in range(self.piece):
				if isinstance(other, ChainReaction):
					a = random() * pi
				else:
					a = (random()*2-1) * (pi/2.0) + angle
				self.screen.newbullets.append(ChainReaction(self.screen, v.project(position), 1000, a, self.piece-1))
		objects.Bullet.collision(self, other, position)

drive_icon = gwres.load('Weapons','drive.bmp')

class Drive(objects.Bullet):
	icon = drive_icon

	def __init__(self, screen, position, power, angle):
		screen.players[screen.turn].gas = 20
		objects.Bullet.__init__(self, screen, 0, (-1,-1), -1, 0, 0)

	def update(self):
		if self.screen.players[self.screen.turn].gas:
			self.screen.stage = 0
			return True

lazer_icon = pygame.Surface(gwglob.ICON_SIZE)
pygame.draw.line(lazer_icon, (255,0,0), (0,5), (15,12), 1)

class Lazer(objects.Bullet):
	icon = lazer_icon

	def __init__(self, screen, position, power, angle):
		self.power = power
		objects.Bullet.__init__(self, screen, 0, position, -1, magnitude=20, angle=angle)

	def draw(self):
		rect = pygame.Rect(self.screen.camera,gwglob.SIZE)
		if rect.collidepoint(self.position) or rect.collidepoint(self.lastposition):
			pygame.draw.line(self.screen.screen, [255*c for c in hls_to_rgb(0, max(0,min(0.5,0.5 * (self.power / gwglob.PLAYER_MAXPOWER) + (random() * 2 - 1) * 0.5)), 1)], self.screen.translate(self.position), self.screen.translate(self.lastposition), 1)

	def update(self):
		if not self.screen.rect.collidepoint(self.position) or objects.distance(self.position,self.lastposition) >= self.power * 2:
			return False
		self.position[0] += self.xcomponent
		self.position[1] += self.ycomponent
		return True

	def collision(self, other, position):
		self.screen.newexplosions.append(objects.Explosion(self.screen, 10, 30, list(position), 2, 0))
		objects.Bullet.collision(self, other, position)

roller_icon = pygame.Surface(gwglob.ICON_SIZE)
pygame.draw.circle(roller_icon, (128,128,128), (8,8), 2, 0)
for p in [(8,5),(5,9),(9,9)]:
	roller_icon.set_at(p, (255,255,255))

class Roller(objects.Bullet):
	icon = roller_icon
	color = (128,128,128)

	def __init__(self, screen, position, power, angle):
		self.planet = None
		self.planetangle = 0
		self.direction = 1
		self.drawangle = 0
		objects.Bullet.__init__(self, screen, 1, position, -1, magnitude=5 * (power / gwglob.PLAYER_MAXPOWER), angle=angle)

	def damage(self):
		if self.planet:
			return self.basedamage/2
		return self.basedamage

	def update(self):
		if not self.planet:
			inside = self.screen.rect.collidepoint(self.position)
			if self.life > 0:
				if inside:
					self.life = -1
			elif self.life == -1 and not inside:
				self.life = gwglob.SHOT_OUTSIDE_LIFE
		if self.life > 0:
			self.life -= 1
		elif self.life == 0:
			if self.planet:
				self.screen.newexplosions.append(objects.Explosion(self.screen, 30, 30, list(self.position), 1))
			return False
		self.lastposition = list(self.position)
		if self.planet:
			self.planetangle += self.direction
			v = objects.Vector(magnitude=self.planet.size+2,angle=self.planetangle)
			self.position = v.project(self.planet.position)
		else:
			self.position[0] += self.xcomponent
			self.position[1] += self.ycomponent
		return True

	def draw(self):
		if objects.circlerect_overlap(self.position, self.size+1, (self.screen.camera,gwglob.SIZE)):
			pygame.draw.circle(self.screen.screen, self.color, self.screen.translate(self.position), self.size, 0)
			v = objects.Vector(magnitude=3,angle=self.drawangle)
			for n in range(3):
				self.screen.screen.set_at(self.screen.translate(v.project(self.position)), (255,255,255))
				v.set_vector(magnitude=3,angle=v.angle+(2*pi)/3.0)
			if self.direction > 0:
				self.drawangle += pi/20.0
			else:
				self.drawangle -= pi/20.0

	def collision(self, other, position):
		if isinstance(other, objects.Planet):
			if not self.planet:
				self.planetangle = objects.angle_between(position, other.position)
				self.direction = 2/float(other.size)
				if objects.normalabsangle(self.angle-self.planetangle) > pi:
					self.direction = -self.direction
				self.planet = other
				self.life = 60
			return True
		else:
			self.screen.newexplosions.append(objects.Explosion(self.screen, 30, 30, list(position), 1))
			objects.Bullet.collision(self, other, position)

rainingrockets_icon = pygame.Surface(gwglob.ICON_SIZE)
pygame.draw.circle(rainingrockets_icon, (0,0,128), (7,3), 2, 0)
for p in [(1,6),(3,9),(6,11),(9,11),(12,9),(14,6)]:
	rainingrockets_icon.set_at(p, (255,255,255))

# Not a weapon. Used by Raining Rockets.
class RainingRocket(OneShot):
	color = (255,255,255)
	size = 1
	basedamage = 50

	def __init__(self, screen, position, angle):
		objects.Bullet.__init__(self, screen, 1, position, -1, magnitude=5, angle=angle)

class RainingRockets(objects.Bullet):
	icon = rainingrockets_icon

	def __init__(self, screen, position, power, angle):
		self.ascend = -1
		self.planet = None
		objects.Bullet.__init__(self, screen, 1, position, -1, magnitude=5 * (power / gwglob.PLAYER_MAXPOWER), angle=angle)

	def update(self):
		if self.ascend > 0:
			self.ascend -= 1
		elif not self.ascend:
			self.life = 0
			for n in range(6):
				self.screen.newbullets.append(RainingRocket(self.screen, list(self.position), self.angle+pi/180.0*130+(pi/9.0)*n))
		return objects.Bullet.update(self)

	def collision(self, other, position):
		if isinstance(other, objects.Player) or isinstance(other, objects.Planet):
			if isinstance(other, objects.Player):
				self.planet = other.planet
			else:
				self.planet = other
			self.position = position
			if self.ascend > 0:
				self.ascend = 0
			else:
				self.ascend = 10
				self.mass = 0
				self.set_vector(magnitude=5, angle=objects.angle_between(position, self.planet.position))
			return True
		else:
			objects.Bullet.collison(self, other, position)

register = {
	'One Shot':OneShot,
	'Three Shot':ThreeShot,
	'Jackhammer':Jackhammer,
	'Hopper':Hopper,
	'Sprinkler':Sprinkler,
	'Chain Reaction':ChainReaction,
	'Drive':Drive,
	'Lazer':Lazer,
	'Roller':Roller,
	'Raining Rockets':RainingRockets,
}