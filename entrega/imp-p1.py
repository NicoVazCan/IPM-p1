#!/usr/bin/env python3
import gi
import requests
import qrcode
from datetime import datetime
import tempfile

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf


#view
class PageStack:
	def __init__(self, stack):
		self.stack = stack
		self.listPages = []

	def getStack(self):
		return self.stack

	def setStack(self, stack):
		self.stack = stack

	def newPage(self, page, pageName):
		actName = self.stack.get_visible_child_name()
		if(actName != None):
			self.listPages.append(actName)
		self.stack.add_named(page, pageName)
		self.stack.set_visible_child_name(pageName)

	def prevPage(self):
		act = self.stack.get_visible_child()

		if(act != None and self.listPages):
			prevName = self.listPages.pop()

			self.stack.set_visible_child(
				self.stack.get_child_by_name(prevName))
			self.stack.remove(act)

	def firstPage(self):
		while(self.listPages):
			self.prevPage()

class View:
	def clicked_btBack(self, widget):
		self.pageStack.prevPage()

	def clicked_btHome(self, widget):
		self.pageStack.firstPage()

	def CCabecera(self):
		whd = Gtk.HeaderBar()
		btBack = Gtk.Button.new_from_icon_name("go-previous", Gtk.IconSize.MENU)
		btBack.connect("clicked", self.clicked_btBack)
		btHome = Gtk.Button.new_from_icon_name("go-home", Gtk.IconSize.MENU)
		btHome.connect("clicked", self.clicked_btHome)
		bxNaveg = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

		whd.pack_start(btBack)
		whd.pack_end(btHome)
		bxNaveg.add(whd)
		return bxNaveg

	def CPageSearch(self, funBtSearch):
		sbx = Gtk.Box()
		gbx = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		gdSearch = Gtk.Grid()
		gdSearch.set_row_spacing(10)
		gdSearch.set_column_spacing(10)

		lbName = Gtk.Label(label="Introduzca un nombre")
		seName = Gtk.SearchEntry()
		lbSurname = Gtk.Label(label="Introduzca un apellido")
		seSurname = Gtk.SearchEntry()
		btSearch = Gtk.Button(label="Buscar")
		btSearch.connect("clicked", funBtSearch,
			seName.get_text, seSurname.get_text)

		gdSearch.attach(lbName,0,0,1,1)
		gdSearch.attach(seName,0,1,1,1)
		gdSearch.attach(lbSurname,4,0,1,1)
		gdSearch.attach(seSurname,4,1,1,1)
		gdSearch.attach(btSearch,2,2,2,1)


		gbx.pack_start(gdSearch, True, False, 100)
		sbx.pack_start(gbx, True, False, 20)

		sbx.show_all()
		self.pageStack.newPage(sbx, "Search")


	def CPageResult(self, name, surname, listData, funBtInfo, funBtCont):
		MAX_USERS = 10
		bxCenter = Gtk.Box()
		bxResult = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		bxCenter.pack_start(bxResult, True, False, 0)

		fmBusNSN = Gtk.Frame()
		fmBusNSN.add(Gtk.Label(label=name + " " + surname))
		bxResult.pack_start(fmBusNSN, False, False, 0)

		if listData:
			swUsers = Gtk.ScrolledWindow()
			swUsers.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
			swUsers.set_propagate_natural_height(True)
			skResult = Gtk.Stack()
			skResult.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
			swUsers.add(skResult)
			ssResult = Gtk.StackSwitcher()
			ssResult.set_stack(skResult)
			ssResult.set_halign(Gtk.Align.CENTER)
			bxResult.pack_start(swUsers, False, False, 20)
			bxResult.pack_end(ssResult, False, True, 20)

			u = 0
			p = 1
			for data in listData:
				if(not(u%MAX_USERS)):
					fbUsers = Gtk.FlowBox()
					skResult.add_titled(fbUsers, str(p), str(p))
					fbUsers.set_valign(Gtk.Align.START)
					fbUsers.set_max_children_per_line(3)
					fbUsers.set_min_children_per_line(3)
					fbUsers.set_row_spacing(20)
					fbUsers.set_homogeneous(True)
					fbUsers.set_selection_mode(Gtk.SelectionMode.NONE)
					p+=1

				fmResNum = Gtk.Frame()
				fmResNum.add(Gtk.Label(label=str(u)))
				fbUsers.add(fmResNum)

				fmResNSN = Gtk.Frame()
				aux = Gtk.Label(
					label=data.get("name")+" "+
					data.get("surname"))
				aux.set_line_wrap(True)
				fmResNSN.add(aux)
				fbUsers.add(fmResNSN)

				gdButtons = Gtk.Grid()
				btInfo = Gtk.Button(label="Info")
				btInfo.connect("clicked", funBtInfo, data)
				gdButtons.attach(btInfo, 0,0,1,1)
				btCont = Gtk.Button(label="Contactos")
				btCont.connect("clicked", funBtCont, data)
				gdButtons.attach(btCont, 0,1,1,1)
				fbUsers.add(gdButtons)

				u+=1
		else:
			bxResult.pack_start(
				Gtk.Label(label="No se encontro ninguna coincidencia."),
				False, False, 20)

		bxCenter.show_all()
		self.pageStack.newPage(bxCenter, "Result")

	def date2str(self, date):
		return date.strftime("%d/%m/%y %H:%M:%S")

	def QrWidget(self, dataUser):
		tmp = tempfile.NamedTemporaryFile(suffix=".png")
		qrcode.make(dataUser.get("name")+","+
			dataUser.get("surname")+","+
			dataUser.get("uuid")).save(tmp)
		img = Gtk.Image.new_from_file(tmp.name)
		pixelbuf = img.get_pixbuf()
		pixelbuf = pixelbuf.scale_simple(82, 82, GdkPixbuf.InterpType.BILINEAR)
		img.set_from_pixbuf(pixelbuf)
		return img

	def CPageInfo(self, dataUser, listLogAcc):
		bxCenter = Gtk.Box()
		bxInfo = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		bxCenter.pack_start(bxInfo, True, False, 0)
		gdDataUser = Gtk.Grid()
		gdDataUser.set_row_spacing(10)
		gdDataUser.set_column_spacing(10)
		bxInfo.pack_start(gdDataUser, False, False, 0)
		gdDataUser.attach(
			Gtk.Label(label="Informacion de "+dataUser.get("name")+" "+dataUser.get("surname")),
			0,0,3,1)
		aux = Gtk.Label(label="Nombre corto:")
		aux.set_halign(Gtk.Align.START)
		gdDataUser.attach(aux, 0,1,1,1)
		aux = Gtk.Label(label=dataUser.get("username"))
		aux.set_halign(Gtk.Align.START)
		gdDataUser.attach(aux, 1,1,1,1)
		aux = Gtk.Label(label="Telefono:")
		aux.set_halign(Gtk.Align.START)
		gdDataUser.attach(aux, 0,2,1,1)
		aux = Gtk.Label(label=dataUser.get("phone"))
		aux.set_halign(Gtk.Align.START)
		gdDataUser.attach(aux, 1,2,1,1)
		aux = Gtk.Label(label="Email:")
		aux.set_halign(Gtk.Align.START)
		gdDataUser.attach(aux, 0,3,1,1)
		aux = Gtk.Label(label=dataUser.get("email"))
		aux.set_halign(Gtk.Align.START)
		gdDataUser.attach(aux, 1,3,1,1)
		aux = Gtk.Label(label="Vacunado:")
		aux.set_halign(Gtk.Align.START)
		gdDataUser.attach(aux, 0,4,1,1)
		aux = Gtk.Label(label=dataUser.get("is_vaccinated"))
		aux.set_halign(Gtk.Align.START)
		gdDataUser.attach(aux, 1,4,1,1)
		gdDataUser.attach(self.QrWidget(dataUser), 2,1,3,3)

		fmLogAcc = Gtk.Frame(label="Registro de accesos")
		bxLogAcc = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		fmLogAcc.add(bxLogAcc)

		fbColumnName = Gtk.FlowBox()
		fbColumnName.set_valign(Gtk.Align.START)
		fbColumnName.set_max_children_per_line(4)
		fbColumnName.set_min_children_per_line(4)
		fbColumnName.set_homogeneous(True)
		#fbColumnName.set_column_spacing(20)
		fbColumnName.set_selection_mode(Gtk.SelectionMode.NONE)
		bxLogAcc.pack_start(fbColumnName, False, False, 0)

		aux = Gtk.Label(label="Instalación")
		aux.set_halign(Gtk.Align.START)
		fbColumnName.add(aux)
		aux = Gtk.Label(label="Fecha de entrada")
		aux.set_halign(Gtk.Align.START)
		fbColumnName.add(aux)
		aux = Gtk.Label(label="Fecha de salida")
		aux.set_halign(Gtk.Align.START)
		fbColumnName.add(aux)
		aux = Gtk.Label(label="Temperatura")
		aux.set_halign(Gtk.Align.START)
		fbColumnName.add(aux)

		swLogAcc = Gtk.ScrolledWindow()
		swLogAcc.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		swLogAcc.set_propagate_natural_height(True)
		bxLogAcc.pack_start(swLogAcc, False, False, 0)

		fbAcc = Gtk.FlowBox()
		swLogAcc.add(fbAcc)
		fbAcc.set_valign(Gtk.Align.START)
		fbAcc.set_max_children_per_line(4)
		fbAcc.set_min_children_per_line(4)
		fbAcc.set_homogeneous(True)
		fbAcc.set_selection_mode(Gtk.SelectionMode.NONE)

		for logAcc in listLogAcc:
			aux = Gtk.Label(label=logAcc.get("facility").get("name"))
			aux.set_line_wrap(True)
			fbAcc.add(aux)
			aux = Gtk.Label(label=self.date2str(logAcc.get("timein")))
			aux.set_line_wrap(True)
			fbAcc.add(aux)
			aux = Gtk.Label(label=self.date2str(logAcc.get("timeout")))
			aux.set_line_wrap(True)
			fbAcc.add(aux)
			aux = Gtk.Label(label=logAcc.get("temperature"))
			aux.set_line_wrap(True)
			fbAcc.add(aux)

		bxInfo.pack_start(fmLogAcc, False, False, 10)

		bxCenter.show_all()
		self.pageStack.newPage(bxCenter, "Info")

	def CalendarUpdate(self, widget, skDest, cdDesde, cdHasta,
		dataUser, listLogContAll, funGetListFiltrada):
		(year, month, day) = cdDesde.get_date()
		month += 1
		dtDesde = datetime(year, month, day)
		(year, month, day) = cdHasta.get_date()
		month += 1
		dtHasta = datetime(year, month, day)

		prevChild = skDest.get_visible_child()
		bxDest = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		skDest.add(bxDest)
		skDest.set_visible_child(bxDest)
		if prevChild != None: skDest.remove(prevChild)


		newListLogCont = funGetListFiltrada(listLogContAll, dtDesde, dtHasta)

		if(newListLogCont == []):
			lbMsg = Gtk.Label()
			if(dtHasta < dtDesde):
				lbMsg.set_label("Debe poner una fecha desde donde quiere buscar anterior a la de hasta.")
			else:
				lbMsg.set_label("No se encontró nada entre esas fechas.")

			bxDest.pack_start(lbMsg, False, False, 20)
			bxDest.show_all()
			return

		swLogCont = Gtk.ScrolledWindow()
		swLogCont.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		swLogCont.set_propagate_natural_height(True)
		fbColumnName = Gtk.FlowBox()
		fbColumnName.set_valign(Gtk.Align.START)
		fbColumnName.set_max_children_per_line(3)
		fbColumnName.set_min_children_per_line(3)
		fbColumnName.set_selection_mode(Gtk.SelectionMode.NONE)
		bxDest.pack_start(fbColumnName, False, False, 0)

		aux = Gtk.Label(label="Persona")
		aux.set_halign(Gtk.Align.START)
		fbColumnName.add(aux)
		aux = Gtk.Label(label="Instalación")
		aux.set_halign(Gtk.Align.START)
		fbColumnName.add(aux)
		aux = Gtk.Label(label="Fecha de contacto")
		aux.set_halign(Gtk.Align.START)
		fbColumnName.add(aux)

		bxDest.pack_start(swLogCont, False, False, 0)

		fbCont = Gtk.FlowBox()
		swLogCont.add(fbCont)
		fbCont.set_valign(Gtk.Align.START)
		fbCont.set_max_children_per_line(3)
		fbCont.set_min_children_per_line(3)
		fbCont.set_homogeneous(True)
		fbCont.set_selection_mode(Gtk.SelectionMode.NONE)


		for logCont in newListLogCont:
			aux = Gtk.Label(label=logCont.get("user").get("name")+" "+logCont.get("user").get("surname"))
			aux.set_line_wrap(True)
			aux.set_halign(Gtk.Align.START)
			fbCont.add(aux)
			aux = Gtk.Label(label=logCont.get("facility").get("name"))
			aux.set_line_wrap(True)
			aux.set_halign(Gtk.Align.START)
			fbCont.add(aux)
			aux = Gtk.Label(label=self.date2str(logCont.get("timestamp")))
			aux.set_line_wrap(True)
			aux.set_halign(Gtk.Align.START)
			fbCont.add(aux)
		bxDest.show_all()


	def CPageCont(self, dataUser, listLogContAll, funGetListFiltrada):
		bxCenter = Gtk.Box()
		bxCont = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		bxFecha = Gtk.Box()
		dtToday = datetime.today()

		bxCont.add(Gtk.Label(
			label="Contactos de "+
				dataUser.get("name")+" "+
				dataUser.get("surname")))

		edDesde = Gtk.Expander(label="Ver desde:")
		cdDesde = Gtk.Calendar()
		edDesde.add(cdDesde)
		cdDesde.select_day(dtToday.day)
		cdDesde.select_month((dtToday.month-2)%12, dtToday.year)
		bxFecha.pack_start(edDesde, False, False, 60)

		edHasta = Gtk.Expander(label="Ver hasta:")
		cdHasta = Gtk.Calendar()
		edHasta.add(cdHasta)
		cdHasta.select_day(dtToday.day)
		cdHasta.select_month((dtToday.month-1)%12, dtToday.year)
		bxFecha.pack_end(edHasta, False, False, 60)
		bxCont.add(bxFecha)

		fmLogCont = Gtk.Frame(label="Registro de contactos")
		skLogCont = Gtk.Stack()
		fmLogCont.add(skLogCont)
		bxCont.pack_start(fmLogCont, False, False, 20)

		cdDesde.connect("day-selected", self.CalendarUpdate, skLogCont,
			cdDesde, cdHasta, dataUser, listLogContAll, funGetListFiltrada)
		cdHasta.connect("day-selected", self.CalendarUpdate, skLogCont,
			cdDesde, cdHasta, dataUser, listLogContAll, funGetListFiltrada)

		self.CalendarUpdate(None, skLogCont, cdDesde, cdHasta,
			dataUser, listLogContAll, funGetListFiltrada)

		bxCont.show_all()
		self.pageStack.newPage(bxCont, "Contactos")

	def CPageError(self, status):
		bxError = Gtk.Box()
		bxError = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		error = Gtk.Label()

		if status==400:
			error.set_label("Error "+ str(status) + "\n Bad Request")
		elif status==401:
			error.set_label("Error "+ str(status) + "\n Unauthorized")
		elif status==404:
			error.set_label("Error "+ str(status) + "\n Not Found")
		elif status==408:
			error.set_label("Error "+ str(status) + "\n Request Timeout")
		elif status==500:
			error.set_label("Error "+ str(status) + "\n Internal Server Error")
		elif status==502:
			error.set_label("Error "+ str(status) + "\n Bad Gateaway")
		elif status==504:
			error.set_label("Error "+ str(status) + "\n Gateaway Timeout")
		else:
			error.set_label("Error "+ str(status))

		bxError.add(error)
		bxError.show_all()
		self.pageStack.newPage(bxError, "Error")


	def __init__(self):
		window = Gtk.Window(title="Sistema de control de accesos Covid-19")
		window.connect("destroy", Gtk.main_quit)
		wbx = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)
		wbx.add(self.CCabecera())
		skPages = Gtk.Stack()
		wbx.pack_start(skPages, True, True, 0)
		self.pageStack = PageStack(skPages)
		window.add(wbx)
		window.show_all()



#controller
class Controller:
	def showUsers(self, widget, get_name, get_surname):
		nameSearch = get_name().strip()
		surnameSearch = get_surname().strip()
		(lista,status)=self.model.CompUser(nameSearch, surnameSearch)

		if status!=200:
			self.view.CPageError(status)
		else:
			self.view.CPageResult(nameSearch, surnameSearch,
				lista,
				self.showInfo, self.showCont)

	def showInfo(self, widget, dataUser):
		(lista,status) = self.model.searchLogAcc(dataUser)

		if status!=200:
			self.view.CPageError(status)
		else:
			self.view.CPageInfo(dataUser, lista)

	def showCont(self, widget, dataUser):
		(lista,status) = self.model.searchCont(dataUser)

		if status!=200:
			self.view.CPageError(status)
		else:
			self.view.CPageCont(dataUser, lista, self.giveCont)

	def giveCont(self, listLogContAll, dateIni, dateFin):


		return self.model.filtrarCont(listLogContAll, dateIni, dateFin)


	def __init__(self):
		self.view = View()
		self.model = Model()
		self.view.CPageSearch(self.showUsers)



#Model
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



Controller()
Gtk.main()