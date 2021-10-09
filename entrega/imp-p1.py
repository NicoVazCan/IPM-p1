import gi
import requests

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

#model

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
		page.show()
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

	def CPageSearch(self):
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

	def CPageResult(self, listData):
		MAX_USERS = 3
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
				 None, None), False, False, 0)
			u+=1

		self.pageStack.newPage(bxCenter, "Result")

	def __init__(self):
		window = Gtk.Window(title= "Sistema de control de accesos COVID")
		window.connect('delete-event' , Gtk.main_quit)
		
		wbx = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)
		wbx.add(self.CCabecera())	
		skPages = Gtk.Stack()
		wbx.pack_start(skPages, True, True, 0)
		exampleBS = [
			{"name": "A", "surname": "01"},
			{"name": "B", "surname": "02"},
			{"name": "C", "surname": "03"},
			{"name": "D", "surname": "04"},
			{"name": "E", "surname": "05"},
			{"name": "F", "surname": "06"},
			{"name": "G", "surname": "07"},]

		self.pageStack = PageStack(skPages)
		self.CPageSearch()
		self.CPageResult(exampleBS)
		
		window.add(wbx)
		
		window.show_all()
		

		
#controller
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

View()
Gtk.main()

