# try:
    # import psyco
    # psyco.full()
# except:
    # pass
#	Galaxy War is a Scorched Earth style game set in space. Players control a "tank" on one of many planets in a galaxy, and must destroy all other players tanks using various weapons and gravity. The weapons system will be completely pluggable, and come with many pre-built weapons including some classics from other similar games.  

# import sys
# sys.stdout = open('stdeo.txt','w')
# sys.stderr = sys.stdout
import gwglob, screens
import pygame,os

def pprint(obj, depth=0):
	depth += 1
	string = ''
	if isinstance(obj, dict):
		if obj:
			string += '{\n'
			for key in obj:
				string += '%s%s:' % ('\t'*depth, repr(key))
				string += pprint(obj[key], depth)
			string += '%s},\n' % ('\t'*(depth-1))
		else:
			string += '{},\n'
	elif isinstance(obj, list):
		if obj:
			string += '[\n'
			for item in obj:
				string += ('%s' % ('\t'*depth))
				string += pprint(item, depth)
			string += '%s],\n' % ('\t'*(depth-1))
		else:
			string += '[],\n'
	else:
		string += '%s,\n' % (repr(obj),)
	if depth == 1:
		return string[:-2]
	return string

def main():
	pygame.init()

	pygame.display.set_caption("Galaxy War %s - Created by: poiuy_qwert" % gwglob.LONG_VERSION)
	pygame.key.set_repeat(gwglob.REPEAT_DELAY,gwglob.REPEAT_INTERVAL)
	screen = pygame.display.set_mode(gwglob.SIZE, [0,pygame.FULLSCREEN][gwglob.FULLSCREEN])
	s = screens.MainMenu(screen)
	while s:
		s = s.run()
	try:
		f = file(os.path.join(gwglob.BASE_DIR,'settings.txt'),'w')
		f.write(pprint(gwglob.SETTINGS))
		f.close()
	except:
		pass

if __name__ == '__main__':
	main()