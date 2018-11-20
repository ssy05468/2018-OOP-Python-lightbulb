import os,imp

import gwglob, objects, gwres

WEAPONS_PATH = os.path.join(gwglob.BASE_DIR, 'Weapons')

def load_pyfile(filename):
	s_name = os.extsep.join(os.path.basename(filename).split(os.extsep)[:-1])
	module = imp.new_module(s_name)
	module.__file__ = filename
	module.__module__ = module
	module.gwglob = gwglob
	module.objects = objects
	module.gwres = gwres
	f = file(filename,"U")
	source = f.read()
	f.close()
	exec compile(source, filename, "exec") in module.__dict__
	return module

def load_weapons(path=WEAPONS_PATH):
	for f in os.listdir(path):
		if f.endswith('%spy' % os.extsep) or f.endswith('%spyw' % os.extsep):
			try:
				pack = load_pyfile(os.path.join(path, f))
				register = pack.register
			except:
				raise
				continue
			for n,c in register.iteritems():
				objects.weapons[n] = (c,len(objects.weapon_packs),gwglob.FONT.render(n, gwglob.ANTI_ALIAS, (0,0,0)))
			objects.weapon_packs.append(pack)