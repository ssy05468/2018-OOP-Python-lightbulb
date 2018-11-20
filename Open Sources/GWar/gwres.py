import pygame, os

import gwglob

CACHE = {}

def load(*path):
	full = os.path.join(gwglob.BASE_DIR, *path)
	if CACHE.get(full):
		return CACHE[full].copy()
	try:
		i = pygame.image.load(full)
		if gwglob.CACHE_IMAGES == True or (gwglob.CACHE_IMAGES and full in gwglob.CACHE_IMAGES):
			CACHE[full] = i
		return i.copy()
	except:
		raise

def roundrect(surface, rect, color, fill=False):
	surf = pygame.Surface(rect[1])
	if color == (0,0,0):
		trans = (255,255,255)
	else:
		trans = (0,0,0)
	surf.set_colorkey(trans)
	if fill:
		surf.fill(color)
	else:
		pygame.draw.rect(surf, color, surf.get_rect(), 1)
	w, h = surf.get_width() - 1, surf.get_height() - 1
	pygame.draw.lines(surf, trans, False, [(0,2),(0,0),(2,0)])
	pygame.draw.lines(surf, trans, False, [(w - 2,0),(w,0),(w,2)])
	pygame.draw.lines(surf, trans, False, [(0,h - 2),(0,h),(2,h)])
	pygame.draw.lines(surf, trans, False, [(w - 2,h),(w,h),(w,h - 2)])
	if not fill:
		pygame.draw.lines(surf, color, False, [(1,2),(1,1),(2,1)])
		pygame.draw.lines(surf, color, False, [(w - 2,1),(w - 1,1),(w - 1,2)])
		pygame.draw.lines(surf, color, False, [(1,h - 2),(1,h - 1),(2,h - 1)])
		pygame.draw.lines(surf, color, False, [(w - 2,h - 1),(w - 1,h - 1),(w - 1,h - 2)])
	surface.blit(surf, rect[0])