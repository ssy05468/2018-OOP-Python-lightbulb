ICON_SIZE = (16,16)
TOOLBOX_TITLEHEIGHT = 5+FONT_SIZE[1]
TOOLBOX_LINE = (17+TOOLBOX_RADAR[0],6+TOOLBOX_TITLEHEIGHT)
TOOLBOX_LINES = int((TOOLBOX_RADAR[1]-2) / TOOLBOX_LINEHEIGHT)
TOOLBOX_LINEHEIGHT = max(ICON_SIZE[0],FONT_SIZE[1])
TOOLBOX_LINEWIDTH = FONT.size('W' * 15)[0]
TOOLBOX_AMMOWIDTH = FONT.size('999')[0]
TOOLBOX_LINESDIM = (ICON_SIZE[0]+TOOLBOX_LINEWIDTH[0]+TOOLBOX_AMMOWIDTH[0],TOOLBOX_LINEHEIGHT*TOOLBOX_LINES)
TOOLBOX_RADAR = (100,100)
TOOLBOX_DIALLENGTH = 20
TOOLBOX_DIAL = (8+TOOLBOX_DIALLENGTH,12+TOOLBOX_TITLEHEIGHT+TOOLBOX_RADAR[1]+TOOLBOX_DIALLENGTH)
TOOLBOX_DIALWIDTH = FONT.size('90')[0] + 6
TOOLBOX_POWERDIM = (40,10)
TOOLBOX_POWER = (20+TOOLBOX_DIAL[0]+TOOLBOX_DIALLENGTH+TOOLBOX_DIALWIDTH,12+TOOLBOX_TITLEHEIGHT+TOOLBOX_RADAR[1]+(TOOLBOX_DIALLENGTH/2)-(TOOLBOX_POWERDIM[1]/2))
TOOLBOX_POWERBAR = (12,TOOLBOX_TITLEHEIGHT+TOOLBOX_LINESIZE*3+1)
TOOLBOX_POWERWIDTH = FONT.size('1000/1000')[0]
TOOLBOX_SCROLBUTTON = (10,10)
TOOLBOX_SCROLLUP = (3+TOOLBOX_LINE[0]+ICON_SIZE[0]+TOOLBOX_LINEWIDTH[0]+TOOLBOX_AMMOWIDTH[0],TOOLBOX_LINE[1]+1)
TOOLBOX_SCROLLDOWN = (TOOLBOX_SCROLLUP[0],TOOLBOX_SCROLLUP[1]+TOOLBOX_LINEHEIGHT*TOOLBOX_LINES-TOOLBOX_SCROLLDIM[1])
TOOLBOX_SCROLL = (TOOLBOX_SCROLLUP[0],TOOLBOX_SCROLLUP[1]+TOOLBOX_SCROLLDIM[1])
TOOLBOX_SCROLLDIM = (TOOLBOX_SCROLLDOWN[0],TOOLBOX_SCROLLDOWN[1]-TOOLBOX_SCROLL[1]-1)
TOOLBOX_SIZE = (9+TOOLBOX_SCROLLUP[0]+TOOLBOX_SCROLLDIM[0],8+TOOLBOX_DIAL[1])

class Toolbox(Object,pygame.Rect):
	def __init__(self, screen, player):
		self.player = player
		self.topweapon = 0
		Object.__init__(self, screen, 0, player.toolboxposition, -1, 0, 0)
		self.listbox = pygame.Rect(gwglob.TOOLBOX_LINE,gwglob.TOOLBOX_LINESDIM)
		self.up = pygame.Rect(gwglob.TOOLBOX_SCROLLUP,gwglob.TOOLBOX_SCROLLBUTTON)
		self.down = pygame.Rect(gwglob.TOOLBOX_SCROLLDOWN,gwglob.TOOLBOX_SCROLLBUTTON)
		self.scroll = pygame.Rect(gwglob.TOOLBOX_SCROLL,gwglob.TOOLBOX_SCROLLDIM)
		self.update_static()
		pygame.Rect.__init__(self, list(self.position), gwglob.TOOLBOX_SIZE)

	def click(self, point):
		if self.collidepoint(point):
			if self.listbox.collidepoint(point):
				self.player.weapon = self.topweapon + (point[1]-self.listbox.topleft[1])/gwglob.TOOLBOX_LINEHEIGHT
				return
			if self.up.collidepoint(point):
				self.topweapon = max(0,self.topweapon-1)
				return
			if self.down.collidepoint(point):
				self.topweapon = min(len(self.player.weapons)-3,self.topweapon+1)
				return
			if self.scroll.collidepoint(point):
				self.topweapon = min(len(self.player.weapons)-3,int(len(self.player.weapons) * ((point[1] - self.scroll.topleft[1]) / float(self.scroll.height))))
				return
			return True

	def move(self, position):
		self.position = position
		self.player.toolboxposition = list(position)
		self.topleft = list(position)
		self.listbox.topleft = (self.position[0]+gwglob.TOOLBOX_LINE[0],self.position[1]+gwglob.TOOLBOX_LINE[1])
		self.up.topleft = (self.position[0]+gwglob.TOOLBOX_SCROLLUP[0],self.position[1]+ggwglob.TOOLBOX_SCROLLUP[1])
		self.down.topleft = (self.position[0]+gwglob.TOOLBOX_SCROLLDOWN[0],self.position[1]+gwglob.TOOLBOX_SCROLLDOWN[1])
		self.scroll.topleft = (self.position[0]+gwglob.TOOLBOX_SCROLL[0],self.position[1]+gwglob.TOOLBOX_SCROLL[1])

	def update_static(self, player=None):
		self.player.topweapon = self.topweapon
		if player:
			self.player = player
		if self.player.toolbox:
			self.static = self.player.toolbox
			self.topweapon = self.player.topweapon
			self.move(list(self.player.toolboxposition))
		else:
			self.topweapon = 0
			self.static = pygame.Surface(gwglob.TOOLBOX_SIZE)
			self.static.lock()
			self.static.fill(self.player.color)
			pygame.draw.circle(self.static, (0,0,0), gwglob.TOOLBOX_DIAL, 20, 0)
			pygame.draw.rect(self.static, self.player.color, ((gwglob.TOOLBOX_DIAL[0]-gwglob.TOOLBOX_DIALLENGTH,gwglob.TOOLBOX_DIAL[1]),(gwglob.TOOLBOX_DIALLENGTH*2,gwglob.TOOLBOX_DIALLENGTH)), 0)
			pygame.draw.rect(self.static, (0,0,0), ((1,1),(gwglob.TOOLBOX_SIZE[0]-2,gwglob.TOOLBOX_SIZE[1]-2)), 1)
			pygame.draw.line(self.static, (0,0,0), (1,gwglob.TOOLBOX_TITLEHEIGHT), (gwglob.TOOLBOX_SIZE[0]-2,gwglob.TOOLBOX_TITLEHEIGHT), 1)
			pygame.draw.rect(self.static, (0,0,0), ((gwglob.TOOLBOX_POWERBAR[0]-1,gwglob.TOOLBOX_POWERBAR[1]-1),(gwglob.TOOLBOX_POWERDIM[0]+2,gwglob.TOOLBOX_POWERDIM[1]+2)), 0)
			pygame.draw.rect(self.static, (0,0,0), ((gwglob.TOOLBOX_LINE[0]-1,gwglob.TOOLBOX_LINE[1]-1),(gwglob.TOOLBOX_LINESDIM[0]+gwglob.TOOLBOX_SCROLLBUTTON[0]+2,gwglob.TOOLBOX_LINESDIM[0]+2)), 1)
			# pygame.draw.rect(self.static, (0,0,0), ((gwglob.TOOLBOX_SIZE[0]-24,gwglob.TOOLBOX_TITLEHEIGHT+11),(12,gwglob.TOOLBOX_LINESIZE*3+2)), 1)
			# pygame.draw.rect(self.static, (0,0,0), ((gwglob.TOOLBOX_SIZE[0]-24,gwglob.TOOLBOX_TITLEHEIGHT+22),(12,gwglob.TOOLBOX_LINESIZE*3-20)), 0)
			self.static.unlock()
			self.static.blit(gwglob.FONT.render(self.player.name, gwglob.ANTI_ALIAS, (0,0,0), self.player.color), (3,3))
			self.player.toolbox = self.static
			self.move([gwglob.SIZE[0]-50-gwglob.TOOLBOX_SIZE[0],50])

	def draw(self):
		self.screen.screen.blit(self.static, self.position)
		# v = Vector(magnitude=20, angle=self.player.aiming-pi/2.0)
		# dial = (gwglob.TOOLBOX_DIAL[0]+self.position[0],gwglob.TOOLBOX_DIAL[1]+self.position[1])
		# pygame.draw.line(self.screen.screen, (255,255,255), dial, v.project(dial))
		# size = gwglob.FONT.size('%d' % degrees(self.player.aiming))
		# degree = (dial[0]+25,dial[1]-10-gwglob.FONT_SIZE[1]/2)
		# self.screen.screen.blit(gwglob.FONT.render('%d' % degrees(self.player.aiming), gwglob.ANTI_ALIAS, (0,0,0), self.player.color), degree)
		# pygame.draw.circle(self.screen.screen, (0,0,0), (degree[0]+size[0]+3,degree[1]+3), 2, 1)
		# powerbar = (gwglob.TOOLBOX_POWERBAR[0]+1+self.position[0],gwglob.TOOLBOX_POWERBAR[1]+1+self.position[1])
		# power,maxpower = int(38 * (self.player.power / gwglob.PLAYER_MAXPOWER)),int(38 * (self.player.maxpower / gwglob.PLAYER_MAXPOWER))
		# if power < maxpower:
			# pygame.draw.rect(self.screen.screen, self.player.color, (powerbar, (maxpower,8)), 1)
		# pygame.draw.rect(self.screen.screen, self.player.color, (powerbar, (power,8)), 0)
		# self.screen.screen.blit(gwglob.FONT.render('%d/%d' % (self.player.power,self.player.maxpower), gwglob.ANTI_ALIAS, (0,0,0), self.player.color), (powerbar[0]+45,powerbar[1]+4-gwglob.FONT_SIZE[1]/2))
		# if len(self.player.weapons) > 3:
			# n = gwglob.TOOLBOX_SCROLLHEIGHT / float(len(self.player.weapons))
			# pygame.draw.rect(self.screen.screen, self.player.color, ((self.position[0]+gwglob.TOOLBOX_SIZE[0]-23,self.position[1]+gwglob.TOOLBOX_TITLEHEIGHT+23+n*self.topweapon),(10,n*3)), 0)
		# for n,d in enumerate(zip(self.player.weapons[self.topweapon:self.topweapon+3],self.player.ammo[self.topweapon:self.topweapon+3])):
			# w,a = d
			# h = gwglob.FONT.size(str(a))[0]
			# p = (gwglob.TOOLBOX_WEAPONS[0]+self.position[0]+1,gwglob.TOOLBOX_WEAPONS[1]+self.position[1]+1+gwglob.TOOLBOX_LINESIZE*n)
			# self.screen.screen.blit(weapons[w][0].icon, p)
			# self.screen.screen.blit(weapons[w][2], (p[0]+17,p[1]), ((0,0),(gwglob.TOOLBOX_WEAPONS_WIDTH-3-h,p[1])))
			# self.screen.screen.blit(gwglob.FONT.render(str(a), gwglob.ANTI_ALIAS, (0,0,0)), (p[0]+gwglob.TOOLBOX_WEAPONS_WIDTH-3-h,p[1]))
			# if self.topweapon + n == self.player.weapon:
				# pygame.draw.rect(self.screen.screen, (0,0,0), ((p[0]-1,p[1]-1), (gwglob.TOOLBOX_WEAPONS_WIDTH, gwglob.TOOLBOX_LINESIZE+2)), 1)
