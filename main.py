import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"


def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Controlli Sezione 3: aggiunta nuovo strumento
    input_tipo = ft.TextField(label="Tipo", width=250)
    input_marca = ft.TextField(label="Marca", width=250)
    input_anno = ft.TextField(label="Anno acquisto", width=250)

    # Contatore per il valore dello strumento
    valore_counter = ft.TextField(value="0", text_align=ft.TextAlign.CENTER, width=60, read_only=True)

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✔" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"
        page.update()

    # Handlers per il contatore del valore
    def decrementa_valore(e):
        valore_attuale = float(valore_counter.value)
        if valore_attuale >= 10:
            valore_counter.value = str(int(valore_attuale - 10))
        else:
            valore_counter.value = "0"
        valore_counter.update()

    def incrementa_valore(e):
        valore_attuale = float(valore_counter.value)
        valore_counter.value = str(int(valore_attuale + 10))
        valore_counter.update()

    # Handler per aggiunta dello strumento
    def aggiungi_strumento_click(e):
        tipo = input_tipo.value.strip()
        marca = input_marca.value.strip()
        anno_str = input_anno.value.strip()

        # Validazione campi numerici
        try:
            anno = int(anno_str)
            valore = float(valore_counter.value)
            if not tipo or not marca:
                alert.show_alert("Errore: compila tutti i campi prima di inserire uno strumento.")
                return
        except ValueError:
            # Messaggio di errore come da specifiche nel README
            alert.show_alert("Errore: inserisci valori numerici validi per anno e posti.")
            return

        # Aggiunta dello strumento al deposito
        deposito.aggiungi_strumento(tipo, marca, anno, valore)

        # Reset dei campi di input
        input_tipo.value = ""
        input_marca.value = ""
        input_anno.value = ""
        valore_counter.value = "0"

        # Aggiornamento dell'interfaccia e della lista
        aggiorna_lista_strumenti()
        page.update()

    # --- EVENTI E PULSANTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    btn_meno = ft.IconButton(icon=ft.Icons.REMOVE, on_click=decrementa_valore, icon_color="red")
    btn_piu = ft.IconButton(icon=ft.Icons.ADD, on_click=incrementa_valore, icon_color="green")
    pulsante_aggiungi = ft.Button("Aggiungi strumento", on_click=aggiungi_strumento_click)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1: Intestazione
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2: Modifica Responsabile
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(
            spacing=30,
            controls=[input_responsabile, pulsante_conferma_responsabile],
            alignment=ft.MainAxisAlignment.CENTER,
        ),

        ft.Divider(),

        # Sezione 3: Aggiunta Nuovo Strumento
        ft.Text("Aggiungi nuovo strumento", size=20),
        ft.Row(
            spacing=15,
            controls=[
                input_tipo,
                input_marca,
                input_anno,
                ft.Row(
                    spacing=5,
                    controls=[btn_meno, valore_counter, btn_piu],
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        ft.Row(
            controls=[pulsante_aggiungi],
            alignment=ft.MainAxisAlignment.CENTER
        ),

        # Sezione 4: Lista Strumenti
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )

    aggiorna_lista_strumenti()


ft.run(main)