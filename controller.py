import flet as ft

'''
CONTROLLER:
- funziona da intermediario tra MODEL e VIEW
- gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view, model):
        self._autonoleggio=model
        self._view = view
        #se non li passo nel costruttore devo importarli

        #dice al MODEL di caricare i dati e se qualcosa va storto lo mostra tramite la view
        try:
            self._autonoleggio.carica_file_automobili()
        except Exception as e:
            self._view.show_alert(f"{e}") #appare una finestra che mostra l'errore

    def get_nome(self):
        return self._autonoleggio.nome

    def get_responsabile(self):
        return self._autonoleggio.responsabile

    def conferma_responsabile(self, e):
        self._autonoleggio.responsabile = self._view.input_responsabile.value
        self._view.txt_responsabile.value = f"Responsabile: {self._autonoleggio.responsabile}"
        self._view.update()

    def aggiungi_auto(self, e):  # passo l'evento e perché so già che sarà collegato ad un pulsante
        try:
            anno = int(self._view.input_anno.value)
            posti = int(self._view.txt_posti.value)
            self._autonoleggio.aggiungi_automobile(
                self._view.input_marca.value,
                self._view.input_modello.value,
                anno,
                posti
            )

            # setto tutti i singoli elementi a vuoto come richiesto
            self._view.input_marca.value = self._view.input_modello.value = self._view.input_anno.value = self._view.txt_posti.value = ""
            self.aggiorna_lista_auto()

        except ValueError:
            self._view.show_alert("Valore inserito non valido")

    def aggiorna_lista_auto(self):
        self._view.lista_auto.controls.clear()
        for auto in self._autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            self._view.lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        self._view.update()



