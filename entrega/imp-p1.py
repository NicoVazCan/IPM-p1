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

	def __init__(self):
		window = Gtk.Window(title= "Sistema de control de accesos COVID")
		window.connect('delete-event' , Gtk.main_quit)
		
		wbx = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)
		
		wbx.add(self.CCabecera())
		
		skPages = Gtk.Stack()
		wbx.pack_start(skPages, True, True, 0)

		sbx = Gtk.Box()
		gbx = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		gdSearch = Gtk.Grid()
		gdSearch.set_row_spacing(40)
		gdSearch.set_column_spacing(40)

		lbName = Gtk.Label(label="Introduzca un nombre")
		seName = Gtk.SearchEntry()
		lbSubname = Gtk.Label(label="Introduzca un apellido")
		seSubname = Gtk.SearchEntry()
		btSearch = Gtk.Button(label="Buscar")

		gdSearch.attach(lbName,0,0,1,1)
		gdSearch.attach(seName,1,0,1,1)
		gdSearch.attach(lbSubname,4,0,1,1)
		gdSearch.attach(seSubname,5,0,1,1)
		gdSearch.attach(btSearch,2,1,2,1)


		gbx.pack_start(gdSearch, True, False, 100)
		sbx.pack_start(gbx, True, False, 0)
		

		bxResult = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		
		gdResult = Gtk.Grid()


		etBusNSN = Gtk.Entry()

		etResNum1 = Gtk.Entry()
		etResNum1.set_text("1")
		etResNum2 = Gtk.Entry()
		etResNum2.set_text("2")
		etResNum3 = Gtk.Entry()
		etResNum3.set_text("3")

		etResNSN1 = Gtk.Entry()
		etResNSN2 = Gtk.Entry()
		etResNSN3 = Gtk.Entry()

		btInfo1 = Gtk.Button(label="Info")
		btCont1 = Gtk.Button(label="Contactos")
		btInfo2 = Gtk.Button(label="Info")
		btCont2 = Gtk.Button(label="Contactos")
		btInfo3 = Gtk.Button(label="Info")
		btCont3 = Gtk.Button(label="Contactos")


		bxResult.pack_start(etBusNSN, False, True, 10)

		self.pageStack = PageStack(skPages)
		
		self.pageStack.newPage(sbx, "Search")
		self.pageStack.newPage(bxResult, "Result")
		self.pageStack.newPage(Gtk.Label(label="Lol"), "Label")
		
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

