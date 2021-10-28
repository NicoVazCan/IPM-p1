#!/usr/bin/env python3
from ipm import e2e
import qrcode
import sys
import time
import requests

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

def buscar(name="", surname=""):
	entry = e2e.find_all_objs(app, role='text', name='Buscar')
	assert entry[0] is not None and entry[1] is not None
	entry[1].set_text_contents(name)
	entry[1].set_text_contents(surname)

	do, shows = e2e.perform_on(app, role='push button', name="Buscar")
	do('click')	



process, app = e2e.run("./imp-p1.py")
modelo = Model()

if app is None:
	process and process.kill()
	assert False, f"La aplicación imp-p1.py no aparece en el escritorio"


entry = e2e.find_all_objs(app, role='text', name='Buscar')
assert entry[0] is not None and entry[1] is not None
entry[0].set_text_contents('')
entry[1].set_text_contents('')
do, shows = e2e.perform_on(app, role='push button', name="Buscar")
do('click')	

listData, _ = modelo.CompUser("","")
lenData = len(listData)

MAX_USERS = 10

for buttons in e2e.find_all_objs(app, role='radio button'):
	found = False
	for i in range(1, round(lenData/MAX_USERS)+1):
		found = found or (buttons.get_name() == str(i))
		if found: break
	assert found

	if i == (round(lenData/MAX_USERS)+1):
		maxUsers = lenData-MAX_USERS*(i-1)
	else:
		maxUsers = MAX_USERS

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


process and process.kill()