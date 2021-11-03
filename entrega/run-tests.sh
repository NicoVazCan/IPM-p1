#!/usr/bin/env python3
import gi
gi.require_version('Atspi', '2.0')
from gi.repository import Atspi
import requests
import time
import subprocess
import warnings
warnings.filterwarnings('ignore')

class Model:
	def __init__(self):
		pass

	def CompUser(self, name, surname):

		try:
			r = requests.get("http://localhost:8080/api/rest/users",
			headers={"x-hasura-admin-secret":"myadminsecretkey"})

			data = r.json()
			lista=data.get("users")
			i=0
			if r.status_code!=200:
				return([],r.status_code)
			if name!="":
				while lista[i]["uuid"]!=lista[-1]["uuid"]:
					if lista[i]["name"].startswith(name.capitalize()):
						i=i+1
					else:
						lista.remove(lista[i])
						if i!=0:
							i=i-1
				if not lista[i]["name"].startswith(name.capitalize()):
					lista.remove(lista[i])


			i=0
			if lista and surname!="":
				while lista[i]["uuid"]!=lista[-1]["uuid"]:
					if lista[i]["surname"].startswith(surname.capitalize()):
						i=i+1
					else:
						lista.remove(lista[i])
						if i!=0:
							i=i-1
				if not lista[i]["surname"].startswith(surname.capitalize()):
					lista.remove(lista[i])

			lista.sort(key=(lambda dict: sum(list(map(ord, dict.get("name")+dict.get("surname"))))))

			return(lista,r.status_code)
		except:
			return([], 500)

	def searchLogAcc(self, data):
		try:
			r = requests.get(
			  "http://localhost:8080/api/rest/user_access_log/"+str(data.get("uuid")),
			  headers={"x-hasura-admin-secret":"myadminsecretkey"})
			data = r.json()

			listRows = data.get("access_log")

			listLogAcc = []

			for logIN in listRows:
				if logIN.get("type") == "IN":
					dateIN = datetime.fromisoformat(logIN.get("timestamp"))
					faciIdIN = logIN.get("facility").get("id")
					for logOUT in listRows:
						if logOUT.get("type") == "OUT":
							dateOUT = datetime.fromisoformat(logOUT.get("timestamp"))
							faciIdOUT = logOUT.get("facility").get("id")

							if dateIN < dateOUT and faciIdIN == faciIdOUT:
								listLogAcc.append({"facility": logIN.get("facility"),
									"timein": dateIN, "timeout": dateOUT, "temperature": logIN.get("temperature")})
								break

			listLogAcc.sort(key=(lambda dict: dict.get("timein").timestamp()))

			return(listLogAcc, r.status_code)
		except:
			return([], 500)

	def searchCont(self, data):
		try:
			listLogContAll = []

			(listLogAcc, status) = self.searchLogAcc(data)

			for logAcc in listLogAcc:
				r = requests.get(
					"http://localhost:8080/api/rest/facility_access_log/"+str(logAcc.get("facility").get("id"))+"/daterange",
					headers={"x-hasura-admin-secret":"myadminsecretkey"},
					json={"startdate": str(logAcc.get("timein")), "enddate": str(logAcc.get("timeout"))})
				if r.status_code != 200:
					return([], r.status_code)
				datar = r.json()
				listRows = datar.get("access_log")
				i = 0
				while i < len(listRows):
					if listRows[i].get("user").get("uuid")==data.get("uuid"):
						listRows.pop(i)
						i -= 1
					else:
						listRows[i]["timestamp"] = datetime.fromisoformat(listRows[i].get("timestamp"))
						listRows[i].update({"facility": logAcc.get("facility")})
						typeLog = listRows[i].get("type")
						listRows[i].pop("type")
						if typeLog == "OUT":
							listRows.pop(i)
							i -= 1
					i += 1
				listLogContAll.extend(listRows)

			return(listLogContAll, status)
		except:
			return([], 500)

	def filtrarCont(self, listLogContAll, dateIni, dateFin):
		newListLogCont = []

		for logCont in listLogContAll:
			date = logCont.get("timestamp")

			if(date.timestamp() >= dateIni.timestamp() and
				date.timestamp() <= dateFin.timestamp()):
				newListLogCont.append(logCont)

		newListLogCont.sort(key=(lambda dict: dict.get("timestamp").timestamp()))

		return newListLogCont

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


process, app = run("./imp-p1.py")

if app is None:
	process and process.kill()
	assert False, f"La aplicación imp-p1.py no aparece en el escritorio"

UiBuscarUsuario(app, '', '')
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

'''
MAX_USERS = 10

modelo = Model()
listData, code = modelo.CompUser("","")
lenData = len(listData)'''


'''
time.sleep(1)
for i in range(1, round(lenData/MAX_USERS)+1):
	print('i= '+str(i))
	e2e.dump_app(app.get_name())
	if i == (round(lenData/MAX_USERS)+1):
		maxUsers = lenData-MAX_USERS*(i-1)
	else:
		maxUsers = MAX_USERS

	for j in range(MAX_USERS*(i-1)+1,maxUsers*i+1):
		print('j= '+str(j))
		_, shows = e2e.perform_on(app, role='label', name=str(j))
		assert shows(name=str(j))

	print(list(widget.get_name() for (_,widget) in e2e.tree_walk(app)))
	do, shows = e2e.perform_on(app, role='radio button', name=str(i))
	assert shows(name=str(i))
	do('click')
	time.sleep(2)


for buttons in e2e.find_all_objs(app, role='radio button'):
	found = False
	for i in range(1, round(lenData/MAX_USERS)+1):
		found = found or (buttons.get_name() == str(i))
		if found: break
	assert found

	

	labels = e2e.find_all_objs(app, role='label')
	for j in range(MAX_USERS*(i-1)+1,maxUsers*i+1):
		
		found = False
		for label in labels:
			found = found or label.get_name()==str(j)

			for data in listData:
				found = (found or 
					label.get_name()==(
						data.get('name')+' '+data.get('surname')))
			if found:
				break
		
		if found:
			labels.remove(label)
		assert found

	do, shows = e2e.perform_on(app, role='radio button', name=str(i))
	do('click')
'''

process and process.kill()