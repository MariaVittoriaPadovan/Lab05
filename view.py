import flet as ft

from alert import AlertManager

'''
VIEW:
- rappresenta l'interfaccia utente
- riceve i dati dal MODEL e li presenta senza modificarli
'''

class View:
    def __init__(self, page: ft.Page):
        #Page
        self.page = page
        self.page.title= "Lab05"
        self.page.horizontal_alignment="center"
        self.page.theme_mode=ft.ThemeMode.DARK

        #Alert
        self.alert= AlertManager(page)

        #Controller
        self.controller= None

        #Elementi UI
        self.txt_titolo=None
        self.txt_responsabile=None

        #Non obbligatorio mettere già qui tutti gli elementi UI

    def show_alert(self, messaggio):
        self.alert.show_alert(messaggio)

    def show_controller(self, controller):
        ''' Imposta il controller alla pagina'''
        self.controller= controller

    def update(self):
        self.page.update()

    def add_content(self): #aggiunge tutta la parte iniziale
        self.txt_titolo= ft.Text(value=self.controller.get_nome(), size=38, weight=ft.FontWeight.BOLD)
        self.txt_responsabile= ft.Text(
            value=f"Responsabile {self.controller.get_responsabile()}",
            size=16,
            weight=ft.FontWeight.BOLD
        )

        #TextField per responsabile
        self.input_responsabile= ft.Text(
            value=self.controller.get_responsabile(),
            label='Responsabile'
        )

        #ListView per mostrare la lista di auto noleggiate
        self.lista_auto= ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

        #TextField per le info necessarie per aggiungere una nuova automobile(marca, modello, anno, posti)
        self.input_marca = ft.TextField(label='Marca')
        self.input_modello = ft.TextField(label='Modello')
        self.input_anno = ft.TextField(label='Anno')

        #TextField per il Counter impiegato per il numero di posti
        self.txt_posti = ft.TextField(value='0', width=60, disabled=True, text_align=ft.TextAlign.CENTER)

        #---PULSANTI e TOGGLE associati a EVENTI
        self.toggle_cambia_tema=ft.Switch(label="Tema scuro", value=True, on_change=self.cambia_tema)

        pulsante_incrementa_posti = ft.IconButton(icon=ft.Icons.ADD,
                                                  icon_color="red",
                                                  icon_size=24,
                                                  on_click=self.incrementa_posti)

        pulsante_decrementa_posti = ft.IconButton(icon=ft.Icons.REMOVE,
                                                  icon_color="red",
                                                  icon_size=24,
                                                  on_click=self.decrementa_posti)

        pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=self.controller.conferma_responsabile)
        pulsante_aggiungi_auto = ft.ElevatedButton("Aggiungi auto", on_click=self.controller.aggiungi_auto)

        # --- LAYOUT ---
        page.add(
            self.toggle_cambia_tema,

            # Sezione 1
            self.txt_titolo,
            self.txt_responsabile,
            ft.Divider(),

            # Sezione 2
            ft.Text("Modifica Informazioni", size=20),
            ft.Row(spacing=200,
                   controls=[self.input_responsabile, pulsante_conferma_responsabile],
                   alignment=ft.MainAxisAlignment.CENTER),

            # Sezione 3
            # TODO
            ft.Divider(),
            ft.Text("Aggiungi Nuova Automobile ", size=20),
            ft.Row(spacing=30,
                   controls=[self.input_marca, self.input_modello, self.input_anno,
                             ft.Row([pulsante_decrementa_posti, self.txt_posti, pulsante_incrementa_posti])],
                   alignment=ft.MainAxisAlignment.CENTER),
            pulsante_aggiungi_auto,

            # Sezione 4
            ft.Divider(),
            ft.Text("Automobili", size=20),
            self.lista_auto,
        )
        self.controller.aggiorna_lista_auto()
