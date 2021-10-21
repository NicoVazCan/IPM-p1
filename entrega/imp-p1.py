import gi
import requests
import qrcode
from datetime import datetime

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf


#model        PROBLEMA SI LE DAS A HOME PETA LA PAGINA DE RESULTADOS, HABLARLO CON NICO
class Model:
	def CompUser(self,name,surname):

		r = requests.get("http://localhost:8080/api/rest/users",
		headers={"x-hasura-admin-secret":"myadminsecretkey"})
		data = r.json()
		lista=data.get("users")
		i=0

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

		if surname!="":
			while lista[i]["uuid"]!=lista[-1]["uuid"]:
				if lista[i]["surname"].startswith(surname.capitalize()):
					i=i+1
				else:
					lista.remove(lista[i])
					if i!=0:
						i=i-1
			if not lista[i]["surname"].startswith(surname.capitalize()):
				lista.remove(lista[i])

		return(lista)


#view
class PageStack:
	def __init__(self, stack, window):
		self.stack = stack
		self.window = window
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
		self.window.show_all()
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
		sbx.pack_start(gbx, True, False, 0)

		self.pageStack.newPage(sbx, "Search")


	def CUserResult(self, num, data, funBtInfo, funBtCont):
		bxGrid = Gtk.Box()
		gdResult = Gtk.Grid()
		gdResult.set_row_spacing(10)
		gdResult.set_column_spacing(10)
		bxGrid.add(gdResult)

		fmResNum = Gtk.Frame()
		fmResNum.add(Gtk.Label(label=num))
		gdResult.attach(fmResNum, 0,0,1,1)

		fmResNSN = Gtk.Frame()
		fmResNSN.add(Gtk.Label(
			label=data.get("name")+" "+data.get("surname")))
		gdResult.attach(fmResNSN, 1,0,2,1)

		btInfo = Gtk.Button(label="Info")
		btInfo.connect("clicked", funBtInfo, data)
		gdResult.attach(btInfo, 3,0,1,1)
		btCont = Gtk.Button(label="Contactos")
		btCont.connect("clicked", funBtCont, data)
		gdResult.attach(btCont, 3,1,1,1)

		return bxGrid

<<<<<<< HEAD
	def CPageResult(self, name, surname, listData, funBtInfo, funBtCont):
		MAX_USERS = 3
=======
	def CPageResult(self, listData, funBtInfo, funBtCont):
		MAX_USERS = 7
>>>>>>> dda59035424458d5fbcc08c74564203b41c99420
		bxCenter = Gtk.Box()
		bxResult = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		bxCenter.pack_start(bxResult, True, False, 0)

		fmBusNSN = Gtk.Frame()
		fmBusNSN.add(Gtk.Label(label=name + " " + surname))
		bxResult.pack_start(fmBusNSN, False, False, 0)

		skResult = Gtk.Stack()
		ssResult = Gtk.StackSwitcher()
		ssResult.set_stack(skResult)
		bxResult.pack_start(skResult, False, False, 10)
		bxResult.pack_end(ssResult, False, False, 10)

		u = 0
		p = 1
		for data in listData:
			if(not(u%MAX_USERS)):
				bxUsers = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
			spacing=10)
				skResult.add_titled(bxUsers, str(p), str(p))
				p+=1
			bxUsers.pack_start(
				self.CUserResult(u, data,
				 funBtInfo, funBtCont), False, False, 0)
			u+=1

		self.pageStack.newPage(bxCenter, "Result")

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
		gdDataUser.attach(
			Gtk.Label(label="Nombre corto:"), 0,1,1,1)
		gdDataUser.attach(
			Gtk.Label(label=dataUser.get("phone")), 1,1,1,1)
		gdDataUser.attach(
			Gtk.Label(label="Telefono:"), 0,2,1,1)
		gdDataUser.attach(
			Gtk.Label(label=dataUser.get("phone")), 1,2,1,1)
		gdDataUser.attach(
			Gtk.Label(label="Email:"), 0,3,1,1)
		gdDataUser.attach(
			Gtk.Label(label=dataUser.get("email")), 1,3,1,1)
		gdDataUser.attach(
			Gtk.Label(label="Vacunado:"), 0,4,1,1)
		gdDataUser.attach(
			Gtk.Label(label=dataUser.get("is_vaccinated")), 1,4,3,3)
		dataUser.get("qr").save("qr.png")
		img = Gtk.Image.new_from_file("qr.png")
		pixelbuf = img.get_pixbuf()
		pixelbuf = pixelbuf.scale_simple(82, 82, GdkPixbuf.InterpType.BILINEAR)
		img.set_from_pixbuf(pixelbuf)
		gdDataUser.attach(img, 2,1,3,3)
		
		fmLogAcc = Gtk.Frame(label="Registro de accesos")
		bxLogAcc = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		fmLogAcc.add(bxLogAcc)

		fbColumnName = Gtk.FlowBox()
		fbColumnName.set_valign(Gtk.Align.START)
		fbColumnName.set_max_children_per_line(4)
		fbColumnName.set_min_children_per_line(4)
		fbColumnName.set_selection_mode(Gtk.SelectionMode.NONE)
		bxLogAcc.pack_start(fbColumnName, False, False, 0)

		fbColumnName.add(Gtk.Label(label="Instalación"))
		fbColumnName.add(Gtk.Label(label="Fecha de entrada"))
		fbColumnName.add(Gtk.Label(label="Fecha de salida"))
		fbColumnName.add(Gtk.Label(label="Temperatura"))

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
			aux = Gtk.Label(label=logAcc.get("facility"))
			aux.set_line_wrap(True)
			fbAcc.add(aux)
			aux = Gtk.Label(label=logAcc.get("timein"))
			aux.set_line_wrap(True)
			fbAcc.add(aux)
			aux = Gtk.Label(label=logAcc.get("timeout"))
			aux.set_line_wrap(True)
			fbAcc.add(aux)
			aux = Gtk.Label(label=logAcc.get("temperature"))
			aux.set_line_wrap(True)
			fbAcc.add(aux)

		bxInfo.pack_start(fmLogAcc, False, False, 10)

		self.pageStack.newPage(bxCenter, "Info")

	def CalendarUpdate(self, widget, bxDest, cdDesde, cdHasta,
		dataUser, listLogContAll, funGetListFiltrada):
		(year, month, day) = cdDesde.get_date()
		dtDesde = datetime(year, month, day)
		(year, month, day) = cdHasta.get_date()
		dtHasta = datetime(year, month, day)

		'''newListLogCont = funGetListFiltrada(listLogContAll, dtDesde, dtHasta)

		swLogCont = Gtk.ScrolledWindow()
		swLogCont.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
		swLogCont.set_propagate_natural_height(True)
		bxLogCont.pack_start(swLogAcc, False, False, 0)

		fbCont = Gtk.FlowBox()
		swLogCont.add(fbAcc)
		fbCont.set_valign(Gtk.Align.START)
		fbCont.set_max_children_per_line(3)
		fbCont.set_min_children_per_line(3)
		fbCont.set_homogeneous(True)
		fbCont.set_selection_mode(Gtk.SelectionMode.NONE)

		for logAcc in listLogAcc:
			aux = Gtk.Label(label=logAcc.get("facility"))
			aux.set_line_wrap(True)
			fbAcc.add(aux)
			aux = Gtk.Label(label=logAcc.get("timein"))
			aux.set_line_wrap(True)
			fbAcc.add(aux)
			aux = Gtk.Label(label=logAcc.get("timeout"))
			aux.set_line_wrap(True)
			fbAcc.add(aux)
			aux = Gtk.Label(label=logAcc.get("temperature"))
			aux.set_line_wrap(True)
			fbAcc.add(aux)'''
		

	def CPageCont(self, dataUser, listLogContAll, funGetListFiltrada):
		bxCenter = Gtk.Box()
		bxCont = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		#bxCenter.pack_start(bxCont, True, False, 0)
		bxFecha = Gtk.Box()
		#bxCont.pack_start(bxFecha, False, False, 0)
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

		bxLogCont = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

		cdDesde.connect("day-selected", self.CalendarUpdate, bxLogCont,
			cdDesde, cdHasta, dataUser, listLogContAll, funGetListFiltrada)
		cdHasta.connect("day-selected", self.CalendarUpdate, bxLogCont,
			cdDesde, cdHasta, dataUser, listLogContAll, funGetListFiltrada)

		

		self.pageStack.newPage(bxCont, "Contactos")


	def __init__(self):
		window = Gtk.Window(title="Sistema de control de accesos Covid-19")
		window.connect("destroy", Gtk.main_quit)
		wbx = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)

		window.connect('delete-event' , Gtk.main_quit)#añadi esto que sino no se cerraba aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

		wbx.add(self.CCabecera())
		skPages = Gtk.Stack()
		wbx.pack_start(skPages, True, True, 0)
		self.pageStack = PageStack(skPages, window)
		window.add(wbx)

#controller
class Controller:
<<<<<<< HEAD
	def showUsers(self, widget, get_name, get_surname):
		nameSearch = get_name().strip()
		surnameSearch = get_surname().strip()
		self.view.CPageResult(
			nameSearch, surnameSearch, 
			self.model.searchUsers(nameSearch, surnameSearch),
=======
	def searchUser(self, widget, get_name, get_surname):#poner get_name() para obtener string, get_name no va

		name=get_name()
		surname=get_surname()

		lista=self.model.CompUser(name,surname)


		self.view.CPageResult(lista,
>>>>>>> dda59035424458d5fbcc08c74564203b41c99420
			self.showInfo, self.showCont)

	def showInfo(self, widget, dataUser):
		listLogAcc = self.model.searchLogAcc(dataUser)

		self.view.CPageInfo(dataUser, listLogAcc)

	def showCont(self, widget, dataUser):
		listLogContAll = self.model.searchCont(dataUser)

		self.view.CPageCont(dataUser, listLogContAll, self.giveCont)

	def giveCont(self, listLogContAll, dateIni, dateFin):


		self.model.filtrarCont(listLogContAll, dateIni, dateFin)
			

	def __init__(self):
		self.model= Model()
		self.view = View()
		self.model = Model()
		self.view.CPageSearch(self.showUsers)

#Model
class Model:
	def __init__(self):
		pass

	def searchUsers(self, name, surname):
		img = qrcode.make("Arturo"+","+"Blanco"+","+"deca9539-3801-4df3-bdcc-d16c629c9f2d")
		exampleBS = [
			{"uuid":"deca9539-3801-4df3-bdcc-d16c629c9f2d","username":"goldenbird345","name":"Arturo","surname":"Blanco","email":"arturo.blanco@example.com","phone":"948-158-045","is_vaccinated":"No", "qr":img},
			{"uuid":"7bd0f511-77a0-4d27-b432-5fdc9439430d","username":"bluesnake674","name":"Xavier","surname":"Suarez","email":"xavier.suarez@example.com","phone":"952-078-384","is_vaccinated":"No", "qr":img},
			{"uuid":"0a9358d1-178a-494e-93de-531514db229e","username":"beautifulostrich652","name":"Patricia","surname":"Sanz","email":"patricia.sanz@example.com","phone":"976-908-484","is_vaccinated":"No", "qr":img},
			{"uuid":"e13927c1-47a0-4779-9ce6-5a37c0193453","username":"purplezebra636","name":"Begoña","surname":"Cabrera","email":"begona.cabrera@example.com","phone":"906-998-337","is_vaccinated":"No", "qr":img},
			{"uuid":"118e7548-1b79-4b66-b825-039943646b44","username":"lazyduck473","name":"Cristobal","surname":"Gonzalez","email":"cristobal.gonzalez@example.com","phone":"992-606-319","is_vaccinated":"Sí", "qr":img},
			{"uuid":"1258b58c-af0d-43be-88f3-e855977f02e1","username":"happyfish853","name":"Ivan","surname":"Herrera","email":"ivan.herrera@example.com","phone":"997-495-548","is_vaccinated":"Sí", "qr":img},
			{"uuid":"505d764e-2884-4a1c-b429-1d7af496f96b","username":"redwolf440","name":"Alejandro","surname":"Hidalgo","email":"alejandro.hidalgo@example.com","phone":"943-200-617","is_vaccinated":"Sí", "qr":img},
			{"uuid":"03438aad-71af-4774-bbca-7ba409bcac20","username":"whitecat392","name":"Pilar","surname":"Campos","email":"pilar.campos@example.com","phone":"989-550-930","is_vaccinated":"No", "qr":img}]
		return exampleBS

	def searchLogAcc(self, data):
		exampleBS = [
			{"temperature":"36.5","timein":"2021-08-17 16:49:38",
				"timeout":"2021-08-17 18:38:50", "facility":"Biblioteca Claudia Alonso"},
			{"temperature":"36.5","timein":"2021-08-17 16:49:38",
				"timeout":"2021-08-17 18:38:50", "facility":"Biblioteca Claudia Alonso"},
			{"temperature":"36.5","timein":"2021-08-17 16:49:38",
				"timeout":"2021-08-17 18:38:50", "facility":"Biblioteca Claudia Alonso"},
			{"temperature":"36.5","timein":"2021-08-17 16:49:38",
				"timeout":"2021-08-17 18:38:50", "facility":"Biblioteca Claudia Alonso"},
			{"temperature":"36.5","timein":"2021-08-17 16:49:38",
				"timeout":"2021-08-17 18:38:50", "facility":"Biblioteca Claudia Alonso"},
			{"temperature":"36.5","timein":"2021-08-17 16:49:38",
				"timeout":"2021-08-17 18:38:50", "facility":"Biblioteca Claudia Alonso"},
			{"temperature":"36.5","timein":"2021-08-17 16:49:38",
				"timeout":"2021-08-17 18:38:50", "facility":"Biblioteca Claudia Alonso"},
			{"temperature":"36.5","timein":"2021-08-17 16:49:38",
				"timeout":"2021-08-17 18:38:50", "facility":"Biblioteca Claudia Alonso"},
			{"temperature":"36.5","timein":"2021-08-17 16:49:38",
				"timeout":"2021-08-17 18:38:50", "facility":"Biblioteca Claudia Alonso"},
			{"temperature":"36.5","timein":"2021-08-17 16:49:38",
				"timeout":"2021-08-17 18:38:50", "facility":"Biblioteca Claudia Alonso"},
			{"temperature":"36.5","timein":"2021-08-17 16:49:38",
				"timeout":"2021-08-17 18:38:50", "facility":"Biblioteca Claudia Alonso"},
			{"temperature":"36.5","timein":"2021-08-17 16:49:38",
				"timeout":"2021-08-17 18:38:50", "facility":"Biblioteca Claudia Alonso"},
			{"temperature":"36.5","timein":"2021-08-17 16:49:38",
				"timeout":"2021-08-17 18:38:50", "facility":"Biblioteca Claudia Alonso"},
			{"temperature":"36.5","timein":"2021-08-17 16:49:38",
				"timeout":"2021-08-17 18:38:50", "facility":"Biblioteca Claudia Alonso"},
			{"temperature":"36.5","timein":"2021-08-17 16:49:38",
				"timeout":"2021-08-17 18:38:50", "facility":"Biblioteca Claudia Alonso"},
			{"temperature":"36.5","timein":"2021-08-17 16:49:38",
				"timeout":"2021-08-17 18:38:50", "facility":"Biblioteca Claudia Alonso"},
			{"temperature":"36.5","timein":"2021-08-17 16:49:38",
				"timeout":"2021-08-17 18:38:50", "facility":"Biblioteca Claudia Alonso"},
			{"temperature":"36.5","timein":"2021-08-17 16:49:38",
				"timeout":"2021-08-17 18:38:50", "facility":"Biblioteca Claudia Alonso"},
			{"temperature":"36.5","timein":"2021-08-17 16:49:38",
				"timeout":"2021-08-17 18:38:50", "facility":"Biblioteca Claudia Alonso"},
			{"temperature":"36.8","timein":"2021-09-09 02:20:47",
				"timeout":"2021-09-09 02:22:47", "facility":"Centro cultural Hector Martin"}]
		return exampleBS

	def searchCont(self, data):
		exampleBS = [
			{"name": "A", "surname": "01", "time": "2021-08-17T16:49:38.277923+00:00",
				"facility":"Centro cultural Hector Martin"},
			{"name": "B", "surname": "02", "time": "2021-07-17T16:49:38.277923+00:00",
				"facility":"Biblioteca Claudia Alonso"}]
		return exampleBS

	def filtrarCont(self, listLogContAllAll, dateIni, dateFin):
		newListLogCont = []

		for logCont in listLogContAll:
			date = logCont.get("time")

			if(date >= dateIni and
				date <= dateFin):
				newListLogCont.append(logCont)

		return newListLogCont



<<<<<<< HEAD
=======



>>>>>>> dda59035424458d5fbcc08c74564203b41c99420
'''
OBTENER TABLA
def accesoBD(nombreTabla, pagina):
	LIMIT = 2
	offset = LIMIT*pagina
	r = requests.get("http://localhost:8080/api/rest/"+nombreTabla+"?offset="+offset+"&limit="+LIMIT,
     headers={"x-hasura-admin-secret":"myadminsecretkey"})
	data = r.json()
	return(data.get(nombreTabla))
'''
Controller()

Gtk.main()
