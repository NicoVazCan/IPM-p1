#!/usr/bin/env python3
import gi
gi.require_version('Atspi', '2.0')
from gi.repository import Atspi
import requests
import time
import subprocess
import warnings
warnings.filterwarnings('ignore')


#Nuestra API para pruebas
def run(path, name=None, timeout=5):
	name = name or path.split('/')[-1]
	process = subprocess.Popen([path])
	desktop = Atspi.get_desktop(0)
	start = time.time()
	app = None
	timeout = timeout or 5
	while app is None and (time.time() - start) < timeout:
		gen = filter(lambda child: child and child.get_name() == name,
				 (desktop.get_child_at_index(i) for i in range(desktop.get_child_count())))
		app = next(gen, None)
		if app is None:
			time.sleep(0.6)
	return (process, app)

def get_children(obj):
	return [obj.get_child_at_index(i) for i in range(obj.get_child_count())]

def tree_walk(obj):
	yield obj
	for i in range(obj.get_child_count()):
		yield from tree_walk(obj.get_child_at_index(i))

def find_objs(root, role=None, name=None):
	return list(filter(lambda child: child and
		(not name or child.get_name() == name) and
		(not role or child.get_role_name() == role), tree_walk(root))) 

def get_actions(obj):
	if obj.get_action_iface():
		return [obj.get_action_name(i) for i in range(obj.get_n_actions())]
	else:
		return []

def do(obj, act):
	for idx in range(obj.get_n_actions()):
		if obj.get_action_name(idx) == act:
			obj.do_action(idx)
			return True

	return False

def dump(obj, space=''):

	print(space+
		str({'role': obj.get_role_name(),
			'name': obj.get_name(),
			'actions': get_actions(obj)}))
	for i in range(obj.get_child_count()):
		dump(obj.get_child_at_index(i), space+' ')


#Funciones para navegar en la UI
def UiBack(app):
	buttons = find_objs(app, 'push button', 'Back')
	assert len(buttons) == 1

	do(buttons[0], 'click')

def UiInicio(app):
	buttons = find_objs(app, 'push button', 'Inicio')
	assert len(buttons) == 1

	do(buttons[0], 'click')

def UiBuscarUsuario(app, name="", surname=""):
	entrys = find_objs(app, 'text', 'Buscar')
	buttons = find_objs(app, 'push button', 'Buscar')
	assert len(entrys) == 2 and len(buttons) == 1

	entrys[0].set_text_contents(name)
	entrys[1].set_text_contents(surname)
	do(buttons[0], 'click')

def UiMoveResult(app, idx):
	buttons = find_objs(app, 'radio button', str(idx))
	assert len(buttons) == 1

	do(buttons[0], 'click')

def UiInfoUsuario(app, name, surname):
	tables = find_objs(app, 'table', '')
	assert len(tables) == 1
	items = find_objs(tables[0], 'list item')
	assert items

	for i in range(len(items)):
		labels = find_objs(items[i], 'label')
		buttons = find_objs(items[i+1], 'push button', 'Info')

		if labels and labels[0].get_name() == (name+' '+surname):
			assert len(buttons) == 1
			do(buttons[0], 'click')
			return True

	return False


def UiContUsuario(app, name, surname):
	tables = find_objs(app, 'table', '')
	assert len(tables) == 1
	items = find_objs(tables[0], 'list item')
	assert items

	for i in range(len(items)):
		labels = find_objs(items[i], 'label')
		buttons = find_objs(items[i+1], 'push button', 'Contactos')

		if labels and labels[0].get_name() == (name+' '+surname):
			assert len(buttons) == 1
			do(buttons[0], 'click')
			return True

	return False

def UiContFiltrarDesde(app, day, month, year):
	labels = find_objs(app, 'label', 'Fecha desde:')
	assert len(labels) == 1
	texts = find_objs(labels[0].get_parent(), 'text')
	assert len(texts) == 1
	texts[0].set_text_contents(str(day)+'/'+str(month)+'/'+str(year))
	do(texts[0], 'activate')

def UiContFiltrarHasta(app, day, month, year):
	labels = find_objs(app, 'label', 'Fecha hasta:')
	assert len(labels) == 1
	texts = find_objs(labels[0].get_parent(), 'text')
	assert len(texts) == 1
	texts[0].set_text_contents(str(day)+'/'+str(month)+'/'+str(year))
	do(texts[0], 'activate')

def step_la_interface_sigue_respondiendo(app: Atspi.Object) -> None:
    # ELiminamos el timeout de arrancar la app
    Atspi.set_timeout(800, -1)
    assert app.get_name() != "", "La interface no responde"



#Pruebas
process, app = run("./imp-p1.py")

if app is None:
	process and process.kill()
	assert False, f"La aplicación imp-p1.py no aparece en el escritorio"

UiBuscarUsuario(app)
time.sleep(1)
UiMoveResult(app, 2)
time.sleep(1)
UiInfoUsuario(app, 'Carlos', 'Moya')
time.sleep(1)
UiBack(app)
time.sleep(1)
UiContUsuario(app, 'Carlos', 'Moya')
time.sleep(1)
UiContFiltrarDesde(app,1,9,21)
time.sleep(1)
UiContFiltrarHasta(app,1,10,21)
time.sleep(1)
UiInicio(app)
time.sleep(1)
dump(app)
step_la_interface_sigue_respondiendo(app)