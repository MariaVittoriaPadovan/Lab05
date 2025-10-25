import flet as ft
from alert import AlertManager
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    # TODO
    #creo 3 campi TextField, non metto value perché devo aggiungere una nuova automobile
    input_marca= ft.TextField(label='Marca')
    input_modello = ft.TextField(label="Modello")
    input_anno= ft.TextField(label="Anno")


    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    # TODO
    #questo è il testo per gestire il counter,slide 18 pwp7
    def handleAdd(e):
        currentVal = int(txtOut.value)
        txtOut.value = currentVal + 1
        txtOut.update()

    def handleRemove(e):
        currentVal = int(txtOut.value)
        txtOut.value = currentVal - 1
        txtOut.update()

    def conferma_automobile(e):
        try:
            marca=input_marca.value
            modello=input_modello.value
            anno=int(input_anno.value)
            posti=int(txtOut.value)

            if not marca or not modello:
                raise ValueError("Inserisci marca e modello validi")

            if anno < 1885 or anno > 2025 or posti==0 or posti>=8: #1885 anno prima macchina
                raise ValueError("Inserisci valori numerici validi per anno e posti")

            autonoleggio.aggiungi_automobile(marca, modello, anno, posti)

            #svuoto i campi
            input_marca.value = ""
            input_modello.value = ""
            input_anno.value = ""

            aggiorna_lista_auto()
            page.update()

        except Exception as e:
            alert.show_alert(f"❌ Errore: {e}")

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto
    # TODO
    #crea i bottoni + e - del counter, slide 19 pwp 7
    btnMinus = ft.IconButton(icon=ft.Icons.REMOVE,
                             icon_color="red",
                             icon_size=24, on_click=handleRemove)
    btnAdd = ft.IconButton(icon=ft.Icons.ADD,
                           icon_color="green",
                           icon_size=24, on_click=handleAdd)
    txtOut = ft.TextField(width=100, disabled=True,
                          value=0, border_color="green",
                          text_align=ft.TextAlign.CENTER)

    pulsante_conferma_automobile = ft.ElevatedButton("Aggiungi Automobile", on_click=conferma_automobile)


    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO
        ft.Text("Aggiungi Nuova Automobile ", size=20),
        ft.Row(spacing=20,
               controls=[input_marca, input_modello, input_anno, btnMinus, txtOut, btnAdd],
               alignment=ft.MainAxisAlignment.CENTER),

        ft.Row(spacing=0,
               controls=[pulsante_conferma_automobile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
