import pygame
from pygame.locals import *

import gwglob,gwres

class WidgetStyles:
	def __init__(self, **styles):
		self.normal = (255,255,255)
		self.highlight = (0,128,255)
		self.selected = (0,128,255)
		self.disabled = (128,128,128)
		self.font = gwglob.FONT
		self.setstyles(**styles)

	def color(self, widget, highlight=0):
		if widget.disabled:
			return self.disabled
		if highlight:
			return self.highlight
		if widget.selected:
			return self.selected
		return self.normal

	def __setitem__(self, style, value):
		if hasattr(self, style):
			setattr(self, style, value)

	def setstyles(self, **styles):
		for style,value in styles.iteritems():
			self[style] = value

STYLE_SMALL_FONT = WidgetStyles()
STYLE_MID_FONT = WidgetStyles(font=gwglob.MID_FONT)
STYLE_BIG_FONT = WidgetStyles(font=gwglob.BIG_FONT)

class Widget(pygame.Rect):
	def __init__(self, screen, style=None, position=(0,0), size=(0,0), selected=False, disabled=False):
		self.screen = screen.screen
		if isinstance(style, WidgetStyles):
			self.style = style
		else:
			self.style = WidgetStyles()
		self.selected = selected
		self.disabled = disabled
		pygame.Rect.__init__(self,position,size)

	def draw(self):
		pass

	def event(self, e):
		pass

class MenuItem(Widget):
	def __init__(self, screen, text, callback, style=None, selected=False, disabled=False):
		self.text = text
		self.callback = callback
		self.selected = selected
		Widget.__init__(self, screen, style, disabled=disabled)
		self.size = self.style.font.size(text)

	def draw(self):
		self.screen.blit(self.style.font.render(self.text, gwglob.ANTI_ALIAS, self.style.color(self)), self.topleft)
		if self.collidepoint(pygame.mouse.get_pos()):
			gwres.roundrect(self.screen, ((self.topleft[0]-5,self.topleft[1]),(self.size[0]+10,self.size[1])), self.style.color(self,1))

class MenuSeperator(Widget):
	def __init__(self, screen, height=gwglob.GUI_SEPERATORHEIGHT):
		self.selected = False
		Widget.__init__(self, screen, None, size=(0,height))

class Menu(Widget):
	def __init__(self, screen, position, centered=False):
		self.items = []
		self.selitem = -1
		self.centered = centered
		Widget.__init__(self, screen, position=position)
		if centered:
			self.midtop = position

	def select(self, item):
		if self.selitem != -1:
			self.items[self.selitem].selected = False
		if isinstance(item, int):
			self.selitem = item
			item = self.items[item]
		else:
			try:
				self.selitem = self.items.index(item)
			except:
				self.selitem = len(self.items)
		item.selected = True

	def add_item(self, item, selected=False):
		if selected or item.selected:
			self.select(item)
		if self.centered:
			if item.width > self.width:
				m = self.midtop
				self.width = item.width
				self.midtop = m
			item.midtop = self.midbottom
		else:
			item.topleft = self.bottomleft
			if item.width > self.width:
				self.width = item.width
		self.items.append(item)
		self.height += item.height

	def remove(self, n):
		if n == self.selitem:
			self.selitem = -1
		elif n < self.selitem:
			self.selitem -= 1
		w,h = self.items[n].size
		del self.items[n]
		while n < len(self.items):
			i = self.items[n]
			i.topleft = (i.topleft[0],i.topleft[1]-h)
			n += 1
		self.height -= h
		if w == self.width:
			w = 0
			for i in self.items:
				if i.width > w:
					w = i.width
			self.width = w

	def draw(self):
		for item in self.items:
			item.draw()

	def event(self, e):
		if e.type == MOUSEBUTTONDOWN and not self.disabled:
			for item in self.items:
				if item.collidepoint(e.pos):
					item.callback(item)
					return

class Button(Widget):
	def __init__(self, screen, position, text, callback, style=None, disabled=False):
		self.text = text
		self.callback = callback
		Widget.__init__(self, screen, style, position, disabled=disabled)
		s = self.style.font.size(text)
		self.size = (s[0]+10,s[1])

	def draw(self):
		if self.collidepoint(pygame.mouse.get_pos()):
			self.selected = True
		self.screen.blit(self.style.font.render(self.text, gwglob.ANTI_ALIAS, self.style.color(self)), (self.topleft[0]+5,self.topleft[1]))
		gwres.roundrect(self.screen, (self.topleft,self.size), self.style.color(self,1))
		self.selected = False

	def event(self, e):
		if e.type == MOUSEBUTTONDOWN and not self.disabled:
			self.callback(self)

class Label(Widget):
	def __init__(self, screen, position, text, style=None, disabled=False):
		self.text = text
		Widget.__init__(self, screen, style, position, disabled=disabled)
		self.size = self.style.font.size(text)

	def draw(self):
		self.screen.blit(self.style.font.render(self.text, gwglob.ANTI_ALIAS, self.style.color(self)), self.topleft)

class Entry(Widget):
	def __init__(self, screen, position, text, letters, style=None, disabled=False):
		self.text = text
		self.letters = letters
		Widget.__init__(self, screen, style, position, disabled=disabled)
		s = self.style.font.size('W'*letters)
		self.size = (s[0]+10,s[1])

	def draw(self):
		if self.text:
			self.screen.blit(self.style.font.render(self.text, gwglob.ANTI_ALIAS, self.style.color(self)), (self.topleft[0]+5,self.topleft[1]))
		gwres.roundrect(self.screen, (self.topleft,self.size), self.style.color(self,1))

	def event(self, e):
		if not self.disabled:
			if e.type == MOUSEBUTTONDOWN:
				self.selected = True
				return self
			elif e.type == KEYDOWN and e.key != K_ESCAPE:
				if e.key == K_BACKSPACE:
					self.text = self.text[:-1]
				elif len(self.text) < self.letters:
					self.text += e.unicode

class ColorDisplay(Widget):
	def __init__(self, screen, position, size, color=(0,0,0)):
		self.color = color
		s = (size[0]+6,size[1]+6)
		Widget.__init__(self, screen, position=position, size=s)

	def draw(self):
		gwres.roundrect(self.screen, ((self.topleft[0]+3,self.topleft[1]+3),(self.size[0]-6,self.size[1]-6)), self.color, 1)
		gwres.roundrect(self.screen, (self.topleft,self.size), self.style.color(self,1))

class ColorBar(Widget):
	def __init__(self, screen, position, size, color=0, value=0, style=None, disabled=False):
		self.color = [0,0,0]
		self.color[color] = 255
		self.value = value
		s = (size[0]+6,size[1]+6)
		Widget.__init__(self, screen, style, position, s, disabled=disabled)

	def draw(self):
		gwres.roundrect(self.screen, ((self.topleft[0]+3,self.topleft[1]+3),(max(1,(self.size[0]-6)/255 * self.value),self.size[1]-6)), self.color, 1)
		gwres.roundrect(self.screen, (self.topleft,self.size), self.style.color(self,1))

	def event(self, e):
		if not self.disabled:
			if e.type == MOUSEBUTTONDOWN:
				self.selected = True
				return self
			elif e.type == KEYDOWN:
				if e.key == K_LEFT and self.value > 0:
					self.value -= 1
				elif e.key == K_RIGHT and self.value < 255:
					self.value += 1
				elif e.key == K_DOWN:
					self.value = max(0,self.value-10)
				elif e.key == K_UP:
					self.value = min(255,self.value+10)
				elif e.key == K_HOME:
					self.value = 0
				elif e.key == K_END:
					self.value = 255

class ProfileItem(MenuItem):
	def __init__(self, screen, text, color, callback, removecb, style=None, selected=False, disabled=False):
		self.color = color
		self.removecb = removecb
		MenuItem.__init__(self, screen, text, callback, style, selected, disabled)
		s = self.style.font.size(text)
		self.size = (s[0]+s[1]*2+17,s[1])
		self.remove = IconButton(screen, (0,0), self.drawicon, self.remove)

	def drawicon(self, b=None,pos=None):
		if b == None:
			return (self.size[1]-6,self.size[1]-6)
		c = self.style.color(b)
		pygame.draw.line(b.screen, c, (pos[0],pos[1]+(self.size[1]-6)/2), (pos[0]+(self.size[1]-6),pos[1]+(self.size[1]-6)/2))

	def remove(self, b):
		self.removecb(self)

	def draw(self):
		gwres.roundrect(self.screen, ((self.topleft[0]+2,self.topleft[1]+2),(self.size[1]-4,self.size[1]-4)), self.color, 1)
		self.screen.blit(self.style.font.render(self.text, gwglob.ANTI_ALIAS, self.style.color(self)), (self.topleft[0]+self.size[1]+5,self.topleft[1]))
		if self.collidepoint(pygame.mouse.get_pos()):
			gwres.roundrect(self.screen, ((self.topleft[0]-5,self.topleft[1]),(self.size[0]-self.size[1],self.size[1])), self.style.color(self,1))
			self.remove.topleft = (self.topright[0]-self.size[1],self.topright[1])
			self.remove.draw()

class ButtonDropDown(Widget):
	def __init__(self, screen, position, style=None):
		self.menu = Menu(screen, (position[0]+10,position[1]+19))
		Widget.__init__(self, screen, style, position, (12,12), disabled=True)

	def draw(self):
		gwres.roundrect(self.screen, (self.topleft,(12,12)), self.style.color(self,1))
		c = self.style.color(self)
		pygame.draw.line(self.screen, c, (self.topleft[0]+2,self.topleft[1]+4), (self.topleft[0]+5,self.topleft[1]+7))
		pygame.draw.line(self.screen, c, (self.topleft[0]+6,self.topleft[1]+7), (self.topleft[0]+9,self.topleft[1]+4))
		if self.selected:
			dd = ((self.menu.topleft[0]-10,self.menu.topleft[1]-5),(self.menu.width+15,self.menu.height+10))
			gwres.roundrect(self.screen, dd, (0,0,0), 1)
			gwres.roundrect(self.screen, dd, self.style.color(self,1))
			self.menu.draw()

	def add_item(self, item):
		self.menu.add_item(item)
		self.disabled = False

	def event(self, e):
		if not self.disabled:
			if e.type == MOUSEBUTTONDOWN:
				if self.selected:
					if self.menu.collidepoint(e.pos):
						for item in self.menu.items:
							if item.collidepoint(e.pos):
								if isinstance(item, ProfileItem) and item.remove.collidepoint(e.pos):
									item.removecb(item)
								else:
									item.callback(item)
								self.selected = False
								self.size = (12,12)
								return True
					elif self.collidepoint(e.pos):
						self.selected = False
						self.size = (12,12)
						return True
				elif not self.selected:
					self.selected = True
					self.size = (self.menu.width+20, self.height+self.menu.height+22)
					return self

class IconButton(Widget):
	def __init__(self, screen, position, icon, callback, style=None, disabled=False):
		self.icon = icon
		self.callback = callback
		if isinstance(self.icon, pygame.Surface):
			s = self.icon.size
		else:
			s = self.icon()
		Widget.__init__(self, screen, style, position, (s[0]+6,s[1]+6), disabled=disabled)

	def draw(self):
		if self.collidepoint(pygame.mouse.get_pos()):
			self.selected = True
		if isinstance(self.icon, pygame.Surface):
			self.screen.blit(self.icon, (self.topleft[0]+3,self.topleft[1]+3))
		else:
			icon = self.icon(self, (self.topleft[0]+3,self.topleft[1]+3))
		gwres.roundrect(self.screen, (self.topleft,self.size), self.style.color(self,1))
		self.selected = False

	def event(self, e):
		if e.type == MOUSEBUTTONDOWN and not self.disabled:
			self.callback(self)