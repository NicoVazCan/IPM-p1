import gi
import requests

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

#model

#view


		
		
class View:

	def CCabecera(self):
		whd = Gtk.HeaderBar()
		btBack = Gtk.Button.new_from_icon_name("go-previous", Gtk.IconSize.MENU)
		btHome = Gtk.Button.new_from_icon_name("go-home", Gtk.IconSize.MENU)
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
		
		self.skPages = Gtk.Stack()
		wbx.pack_start(self.skPages, True, True, 0)

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
		self.skPages.add_named(sbx, "Search")
		
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

