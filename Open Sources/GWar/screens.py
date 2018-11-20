import pygame
from pygame.locals import *

import gwglob, gwres, objects, widgets
from math import *
from random import *

class Screen:
	def __init__(self, screen):
		self.screen = screen

	def run(self):
		self.screen.fill((0,0,0))
		while True:
			for e in pygame.event.get():
				if e.type == QUIT or (e.type == KEYUP and e.key == ESCAPE):
					return
			gwglob.CLOCK.tick(gwglob.FPS_MAX)

class MenuScreen(Screen):
	def __init__(self, screen, title):
		self.selected = None
		self.leave = None
		self.static = pygame.Surface(gwglob.SIZE)
		gwres.roundrect(self.static, ((10,10),(gwglob.SIZE[0]-20,gwglob.SIZE[1]-20)), (0,128,255))
		logo = gwres.load('res','logo.png')
		gwres.roundrect(self.static, ((gwglob.SIZE[0]/2-logo.get_width()/2-10,5),(logo.get_width()+20,logo.get_height()+20)), (0,128,255))
		self.static.blit(logo, (gwglob.SIZE[0]/2-logo.get_width()/2,15))
		title = gwglob.BIG_FONT.render(title, gwglob.ANTI_ALIAS, (0,128,255))
		width = max(gwglob.SIZE[0]/2-logo.get_width()/2-5,title.get_width()+20)
		gwres.roundrect(self.static, ((5,logo.get_height()+20),(width,title.get_height()+20)), (0,128,255))
		self.static.blit(title, (5+width/2-title.get_width()/2,logo.get_height()+30))
		self.page = 80+logo.get_height()+title.get_height()
		self.widgets = []
		Screen.__init__(self, screen)

	def pack(self, widget):
		self.widgets.append(widget)

	def processevents(self):
		for e in pygame.event.get():
			if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
				return True
			elif e.type == MOUSEBUTTONDOWN:
				for widget in self.widgets:
					if widget.collidepoint(e.pos):
						w = widget.event(e)
						if w and (w == True or w.selected):
							if w == True:
								self.selected = None
							else:
								if self.selected:
									self.selected.selected = False
								self.selected = w
							break
			elif e.type == KEYDOWN:
				if self.selected:
					self.selected.event(e)

	def draw(self):
		for widget in self.widgets:
			widget.draw()

	def run(self):
		pass

class MainMenu(MenuScreen):
	def __init__(self, screen):
		MenuScreen.__init__(self, screen, 'Main Menu')
		menu = widgets.Menu(self, (gwglob.SIZE[0]/2, self.page), True)
		menu.add_item(widgets.MenuItem(self, 'Hotseat', self.quickplay, widgets.STYLE_MID_FONT))
		menu.add_item(widgets.MenuSeperator(self))
		menu.add_item(widgets.MenuItem(self, 'Exit', self.exit, widgets.STYLE_MID_FONT))
		self.pack(menu)

	def quickplay(self, i):
		self.leave = HotseatMenu(self.screen)

	def exit(self, i):
		self.leave = False

	def run(self):
		while True:
			if self.processevents():
				return False
			if self.leave != None:
				return self.leave
			self.screen.blit(self.static, (0,0))
			self.draw()
			pygame.display.flip()

class HotseatMenu(MenuScreen):
	def __init__(self, screen):
		MenuScreen.__init__(self, screen, 'Hotseat Setup')
		self.listsize = (gwglob.MID_FONT.size('W'*gwglob.PLAYER_MAXNAME)[0]+20,gwglob.MID_FONT_SIZE[1]*gwglob.PLAYER_MAX+20)
		self.menu = widgets.Menu(self, (100,self.page))
		self.add = widgets.Button(self, (90,self.page+self.listsize[1]+10), 'Add', self.addplayer, widgets.STYLE_MID_FONT)
		self.remove = widgets.Button(self, (90+self.add.width+10, self.page+self.listsize[1]+10), 'Remove', self.removeplayer, widgets.STYLE_MID_FONT, True)
		name = widgets.Label(self, (110+self.listsize[0],self.page-10), 'Name:', widgets.STYLE_MID_FONT)
		color = widgets.Label(self, (110+self.listsize[0],self.page+name.height+5), 'Color:   ', widgets.STYLE_MID_FONT)
		self.name = widgets.Entry(self, (123+self.listsize[0]+color.width,self.page-10), 'Player 1', gwglob.PLAYER_MAXNAME, widgets.STYLE_MID_FONT)
		self.color = widgets.ColorDisplay(self, (110+self.listsize[0]+color.width,self.page+name.height+5), (color.height-6,color.height-6), (255,0,0))
		self.red = widgets.ColorBar(self, (110+self.listsize[0]+color.width,self.page+name.height+color.height+10), (255,10), 0, 255)
		self.green = widgets.ColorBar(self, (110+self.listsize[0]+color.width,self.page+name.height+color.height+30), (255,10), 1)
		self.blue = widgets.ColorBar(self, (110+self.listsize[0]+color.width,self.page+name.height+color.height+50), (255,10), 2)
		start = widgets.Button(self, (0,0), 'Start', self.start, widgets.STYLE_BIG_FONT)
		start.topright = (gwglob.SIZE[0]/2-5,gwglob.SIZE[1]-start.height-100)
		exit = widgets.Button(self, (0,0), 'Exit', self.exit, widgets.STYLE_BIG_FONT)
		exit.topleft = (gwglob.SIZE[0]/2+5,gwglob.SIZE[1]-start.height-100)
		self.profiles = widgets.ButtonDropDown(self, (110+self.listsize[0]+color.width,self.name.topleft[1]+self.name.height/2-6))
		def drawicon(b=None,pos=None):
			if b == None:
				return (5,5)
			c = widgets.STYLE_MID_FONT.color(b)
			pygame.draw.line(b.screen, c, (pos[0]+2,pos[1]), (pos[0]+2,pos[1]+4))
			pygame.draw.line(b.screen, c, (pos[0],pos[1]+2), (pos[0]+4,pos[1]+2))
		add = widgets.IconButton(self, (125+self.listsize[0]+color.width+self.name.width,self.name.topleft[1]+self.name.height/2-6), drawicon, self.addprofile)
		self.pack(self.menu)
		self.pack(self.add)
		self.pack(self.remove)
		self.pack(name)
		self.pack(color)
		self.pack(self.name)
		self.pack(self.color)
		self.pack(self.red)
		self.pack(self.green)
		self.pack(self.blue)
		self.pack(start)
		self.pack(exit)
		self.pack(add)
		self.pack(self.profiles)
		self.addplayer()
		self.addplayer(select=False)
		for text,color in gwglob.SETTINGS.get('profiles',[]):
			self.addprofile(None,text,color)

	def select(self, item):
		self.menu.select(item)
		self.name.text = item.text
		if self.selected:
			self.selected.selected = False
			self.selected = None
		self.red.value,self.green.value,self.blue.value = tuple(item.color)

	def addplayer(self, item=None, select=True):
		p = len(self.menu.items)+1
		while True:
			for item in self.menu.items:
				if item.text == 'Player %d' % p:
					p += 1
					break
			else:
				break
		i = widgets.MenuItem(self, 'Player %d' % p, self.select, widgets.STYLE_MID_FONT)
		i.color = gwglob.PLAYER_COLORS[len(self.menu.items)]
		self.menu.add_item(i)
		if select:
			self.select(i)
		if len(self.menu.items) == gwglob.PLAYER_MAX:
			self.add.disabled = True
		if len(self.menu.items) > 2:
			self.remove.disabled = False

	def removeplayer(self, item=None):
		n = self.menu.selitem
		self.menu.remove(n)
		i = len(self.menu.items)
		if n == i:
			n -= 1
		self.select(self.menu.items[n])
		if i < gwglob.PLAYER_MAX:
			self.add.disabled = False
			if i < 3:
				self.remove.disabled = True

	def profile(self, item):
		i = self.menu.items[self.menu.selitem]
		i.text = item.text
		i.color = item.color
		i.width = i.style.font.size(i.text)[0]
		if i.width > self.menu.width:
			self.menu.width = i.width
		self.name.text = item.text
		self.red.value,self.green.value,self.blue.value = tuple(item.color)

	def addprofile(self, b=None, text=None, color=None):
		if text == None:
			text = self.name.text
			color = self.color.color
			if not 'profiles' in gwglob.SETTINGS:
				gwglob.SETTINGS['profiles'] = []
			gwglob.SETTINGS['profiles'].append((text,color))
		self.profiles.add_item(widgets.ProfileItem(self, text, color, self.profile, self.removeprofile))

	def removeprofile(self, b):
		n = self.profiles.menu.items.index(b)
		self.profiles.menu.remove(n)
		del gwglob.SETTINGS['profiles'][n]

	def start(self, item):
		self.leave = Hotseat(self.screen, [(i.text,i.color) for i in self.menu.items], objects.Map())

	def exit(self, item):
		self.leave = MainMenu(self.screen)

	def run(self):
		while True:
			if self.processevents():
				return MainMenu(self.screen)
			if self.leave != None:
				return self.leave
			self.screen.blit(self.static, (0,0))
			gwres.roundrect(self.screen, ((90,self.page-10),self.listsize), (0,128,255))
			self.color.color = (self.red.value,self.green.value,self.blue.value)
			self.menu.items[self.menu.selitem].color = self.color.color
			self.draw()
			pygame.display.flip()

class Hotseat(Screen):
	def __init__(self, screen, players, map):
		self.rect = pygame.Rect((0,0),list(map.size))
		self.galaxysize = list(map.size)
		self.camera = (0,0)
		self.backgrounds = []
		for n,l in enumerate(range(gwglob.particles('star fields'))):
			size = (self.galaxysize[0]+(self.galaxysize[0]-gwglob.SIZE[0])*(3-n),self.galaxysize[1]+(self.galaxysize[1]-gwglob.SIZE[1])*(3-n))
			self.backgrounds.append(pygame.Surface(size))
			if n:
				self.backgrounds[-1].set_colorkey((0,0,0))
			self.backgrounds[-1].lock()
			for s in range(gwglob.particles('stars per field') * int(round((size[0]*size[1])/float(gwglob.SIZE[0]*gwglob.SIZE[1])))):
				color = gwglob.STAR_COLORS[int(random() * len(gwglob.STAR_COLORS))]
				pos = (int(random() * size[0]),int(random() * size[1]))
				if n:
					pygame.draw.circle(self.backgrounds[-1], color, pos, 2)
				else:
					self.backgrounds[-1].set_at(pos, color)
			self.backgrounds[-1].unlock()
		self.planets = []
		for p in map.planets:
			self.planets.append(objects.Planet(self, *p))
		self.players = []
		self.turn = 0
		for name,color in players:
			player = objects.Player(self, name, ['One Shot','Hopper','Three Shot','Jackhammer','Sprinkler','Chain Reaction','Drive','Lazer','Roller','Raining Rockets'], [-1]*10, color)
			least = 9999
			planet = None
			planets = list(self.planets)
			while planets:
				n = randint(0,len(planets)-1)
				if planets[n].mass < gwglob.MASS_HABITABLE:
					players = len(planets[n].players)
					if players < least:
						least,planet = players,planets[n]
				del planets[n]
			planet.players.append(player)
			self.players.append(player)
		self.toolbox = objects.Toolbox(self, self.players[0])
		for p in self.planets:
			p.place_players()
		self.centerview()
		self.objects = []
		self.bullets = []
		self.explosions = []
		self.newobjects = []
		self.newbullets = []
		self.newexplosions = []
		self.stage = 0
		self.drag = None
		Screen.__init__(self, screen)

	def centerview(self):
		self.camera = (max(0,min(self.galaxysize[0]-gwglob.SIZE[0],self.players[self.turn].position[0]-400)),max(0,min(self.galaxysize[1]-gwglob.SIZE[1],self.players[self.turn].position[1]-300)))

	def run(self):
		while True:
			if len(self.players) == 1:
				return MainMenu(self.screen)
			player = self.players[self.turn]
			for e in pygame.event.get():
				if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
					return MainMenu(self.screen)
				elif e.type == KEYDOWN:
					if e.key == K_LEFT:
						if player.gas > -1:
							if player.gas > 0:
								player.set_positioning(player.planet, player.angle - 2/float(player.planet.size))
							player.gas -= 1
						else:
							player.aiming = max(-pi/2.0,player.aiming-pi/180.0)
					elif e.key == K_RIGHT:
						if player.gas > -1:
							if player.gas > 0:
								player.set_positioning(player.planet, player.angle + 2/float(player.planet.size))
							player.gas -= 1
						else:
							player.aiming = min(pi/2.0,player.aiming+pi/180.0)
					elif e.key == K_DOWN:
						player.power = max(0,player.power-1)
					elif e.key == K_PAGEDOWN:
						player.power = max(0,player.power-10)
					elif e.key == K_UP:
						player.power = min(player.maxpower,player.power+1)
					elif e.key == K_PAGEUP:
						player.power = min(player.maxpower,player.power+10)
				elif e.type == KEYUP:
					if e.key == K_SPACE and not self.stage:
						self.stage = 1
						angle = player.angle + player.aiming
						v = objects.Vector(magnitude=10, angle=angle)
						weap = objects.weapons[player.weapons[player.weapon]][0](self, v.project(player.turret[0]), player.power, angle)
						if weap:
							self.newbullets.append(weap)
					elif e.key == K_RETURN:
						return Hotseat(self.screen, [('Player 1',(255,0,0)),('Player 2',(0,0,255))], objects.Map())
				elif e.type == MOUSEBUTTONDOWN and self.toolbox.click(e.pos):
					self.drag = [e.pos[0]-self.toolbox.position[0],e.pos[1]-self.toolbox.position[1]]
				elif e.type == MOUSEMOTION and self.drag:
					self.toolbox.move([min(gwglob.SIZE[0]-self.toolbox.width,max(0,e.pos[0]-self.drag[0])),min(gwglob.SIZE[1]-self.toolbox.height,max(0,e.pos[1]-self.drag[1]))])
				elif e.type == MOUSEBUTTONUP and self.drag:
					self.drag = None
			if self.drag == None:
				pos = pygame.mouse.get_pos()
				xmove = 0
				if pos[0] < gwglob.MOVE_SIZE:
					xmove = -int(round((gwglob.MOVE_SIZE-pos[0])/5.0))
				elif pos[0] > gwglob.SIZE[0]-gwglob.MOVE_SIZE:
					xmove = int(round((gwglob.MOVE_SIZE-(gwglob.SIZE[0]-pos[0]))/5.0))
				ymove = 0
				if pos[1] < gwglob.MOVE_SIZE:
					ymove = -int(round((gwglob.MOVE_SIZE-pos[1])/5.0))
				elif pos[1] > gwglob.SIZE[1]-gwglob.MOVE_SIZE:
					ymove = int(round((gwglob.MOVE_SIZE-(gwglob.SIZE[1]-pos[1]))/5.0))
				if xmove+ymove:
					self.camera = (max(0,min(self.galaxysize[0]-gwglob.SIZE[0],self.camera[0]+xmove)),max(0,min(self.galaxysize[1]-gwglob.SIZE[1],self.camera[1]+ymove)))
			kill = []
			last = 0
			for n,o in enumerate(self.objects + self.explosions + self.bullets):
				if o.mass:
					for p in self.planets:
						p.tug(o)
				if o.update():
					for c in self.players + self.planets:
						cp = c.collide(o)
						if cp and not o.collision(c,cp):
							if isinstance(o, objects.Bullet):
								kill.append((2,n-len(self.objects)-len(self.explosions)))
							elif isinstance(o, objects.Explosion):
								kill.append((1,n-len(self.objects)))
							else:
								kill.append((0,n))
							break
					if last != -1 and o.life > last:
						last = o.life
					elif o.life == -1:
						last = -1
				elif isinstance(o, objects.Bullet):
					kill.append((2,n-len(self.objects)-len(self.explosions)))
				elif isinstance(o, objects.Explosion):
					kill.append((1,n-len(self.objects)))
				else:
					kill.append((0,n))
			killed = [0,0,0]
			for t,k in kill:
				del [self.objects,self.explosions,self.bullets][t][k-killed[t]]
				killed[t] += 1
			for n,b in enumerate(self.backgrounds):
				self.screen.blit(b, (0,0), ((self.camera[0]*(3-n),self.camera[1]*(3-n)),gwglob.SIZE))
			self.screen.lock()
			for o in self.objects + self.bullets + self.players + self.explosions + self.planets:
				o.draw()
			self.screen.unlock()
			fps = gwglob.FONT.render("%d" % round(gwglob.CLOCK.get_fps()), gwglob.ANTI_ALIAS, (255,0,0))
			self.screen.blit(fps,(10,10))
			self.toolbox.draw()
			if last > 0:
				l = '%ds' % round(last / gwglob.CLOCK.get_fps())
				s = gwglob.FONT.size(l)
				self.screen.blit(gwglob.FONT.render(l, gwglob.ANTI_ALIAS, (255,0,0)), (gwglob.SIZE[0] / 2 - s[0] / 2,gwglob.SIZE[1] - 20 - s[1]))
			pygame.display.flip()
			if self.stage and not self.bullets and not self.newbullets and not self.explosions and not self.newexplosions:
				self.stage = 0
				self.turn = (self.turn + 1) % len(self.players)
				self.toolbox.update_static(self.players[self.turn])
				player.camera = self.camera
				if self.players[self.turn].camera == None:
					self.centerview()
				else:
					self.camera = list(self.players[self.turn].camera)
				for p in self.players:
					p.rotate()
			if self.newobjects:
				self.objects.extend(self.newobjects)
				self.newobjects = []
			if self.newbullets:
				self.bullets.extend(self.newbullets)
				self.newbullets = []
			if self.newexplosions:
				self.explosions.extend(self.newexplosions)
				self.newexplosions = []
			gwglob.CLOCK.tick(gwglob.FPS_MAX)

	def translate(self, pos):
		return (pos[0] - self.camera[0],pos[1] - self.camera[1])

# class Test(Screen):
	# def run(self):
		# self.screen.fill((0,0,0))
		# self.screen.set_at([167.96599221034, 356.6151537155115], (0,0,255))
		# self.screen.set_at([167.07539983066539, 347.36678969051832], (255,0,0))
		# pygame.draw.line(self.screen, (255,255,255), (170.841608599,386.477016189), (170.841608599,386.477016189), 1)
		# v = objects.Vector(magnitude=100, angle=radians(195.892635657))
		# pygame.draw.line(self.screen, (255,0,0), (400,300), v.project((400,300)), 1)
		# v.set_vector(100, radians(180+146.646214765))
		# pygame.draw.line(self.screen, (0,255,0), (400,300), v.project((400,300)), 1)
		# v.set_vector(100, angle=v.angle+pi/2.0)
		# a = v.angle
		# pygame.draw.line(self.screen, (100,255,100), (400,300), v.project((400,300)), 1)
		# v.set_vector(100, angle=v.angle-pi)
		# b = v.angle
		# pygame.draw.line(self.screen, (100,255,100), (400,300), v.project((400,300)), 1)
		# d1,d2 = radians(195.892635657)-a,radians(195.892635657)-b
		# print degrees(d1)
		# print degrees(d2)
		# if abs(d1) < abs(d2):
			# angle = b-d1
		# else:
			# angle = a-d2
		# print degrees(angle)
		# v.set_vector(100, angle=angle)
		# pygame.draw.line(self.screen, (0,0,255), (400,300), v.project((400,300)), 1)
		# pygame.display.flip()
		# while True:
			# for e in pygame.event.get():
				# if e.type == QUIT or (e.type == KEYUP and e.key == ESCAPE):
					# return
			# gwglob.CLOCK.tick(gwglob.FPS_MAX)