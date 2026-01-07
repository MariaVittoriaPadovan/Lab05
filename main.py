import flet as ft
from view import View
from controller import Controller
from model import Autonoleggio


def main(page: ft.Page):
    #setup del MODEL, della VIEW, del CONTROLLER in base al pattern MVC
    view = View(page)#inizializza la pagina
    model=Autonoleggio("Polito Rent", "Alessandro Visconti")
    controller = Controller(view, model) #controller prende le informazioni dal model e le passa alla view
    view.set_controller(controller)
    view.add_content()
    ft.add_content()

ft.app(target=main)
