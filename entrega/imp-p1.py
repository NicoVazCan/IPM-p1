import gi
import requests

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

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
		if(self.listPages):
			firstName = self.listPages.pop(0)

			while(self.listPages != []):
				auxPage = self.stack.get_child_by_name(
					self.listPages.pop())
				self.stack.remove(auxPage)
				auxPage.destroy()

			self.stack.set_visible_child_name(firstName)




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

		fmResNum = Gtk.Frame(label=num)
		gdResult.attach(fmResNum, 0,0,1,1)

		fmResNSN = Gtk.Frame(
			label=data.get("name")+" "+data.get("surname"))
		gdResult.attach(fmResNSN, 1,0,2,1)

		btInfo = Gtk.Button(label="Info")
		#btInfo.connect("clicked", funBtInfo, data)
		gdResult.attach(btInfo, 3,0,1,1)
		btCont = Gtk.Button(label="Contactos")
		#btInfo.connect("clicked", funBtCont, data)
		gdResult.attach(btCont, 3,1,1,1)

		return bxGrid

	def CPageResult(self, listData, funBtInfo, funBtCont):
		MAX_USERS = 7
		bxCenter = Gtk.Box()
		bxResult = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		bxCenter.pack_start(bxResult, True, False, 0)

		fmBusNSN = Gtk.Frame(label="Juan")
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


	def __init__(self):
		window = Gtk.Window(title="Sistema de control de accesos Covid-19")
		wbx = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)

		window.connect('delete-event' , Gtk.main_quit)#añadi esto que sino no se cerraba aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

		wbx.add(self.CCabecera())
		skPages = Gtk.Stack()
		wbx.pack_start(skPages, True, True, 0)
		self.pageStack = PageStack(skPages, window)
		window.add(wbx)

#controller
class Controller:
	def searchUser(self, widget, get_name, get_surname):#poner get_name() para obtener string, get_name no va

		name=get_name()
		surname=get_surname()

		lista=self.model.CompUser(name,surname)


		self.view.CPageResult(lista,
			self.showInfo, self.showCont)

	def showInfo(self, widget, data):
		pass

	def showCont(self, widget, data):
		pass

	def __init__(self):
		self.model= Model()
		self.view = View()
		self.view.CPageSearch(self.searchUser)




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
