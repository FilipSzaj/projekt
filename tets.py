from tkinter import *
import tkintermapview
import requests

jednostki = []
pracownicy = []
pododdzialy = []
zolnierze = []

root = Tk()
root.title("Zarządzanie jednostkami wojskowymi")
root.geometry("1300x800")

# Tutaj dodaję militarny zielony kolor tła:
militarny_zielony = "#4B5320"  # taki odcień militarny
root.configure(bg=militarny_zielony)

# Nagłówki nad kolumnami
Label(root, text="Jednostki", font=("Arial", 16, "bold"), bg=militarny_zielony, fg="white").grid(row=0, column=0)
Label(root, text="Pracownicy", font=("Arial", 16, "bold"), bg=militarny_zielony, fg="white").grid(row=0, column=1)
Label(root, text="Pododdziały", font=("Arial", 16, "bold"), bg=militarny_zielony, fg="white").grid(row=0, column=2)
Label(root, text="Żołnierze", font=("Arial", 16, "bold"), bg=militarny_zielony, fg="white").grid(row=0, column=3)

# Przyciski dodawania w wierszu 1
Button(root, text="Dodaj jednostkę", command=lambda: dodaj_obiekt("Jednostka")).grid(row=1, column=0)
Button(root, text="Dodaj pracownika", command=lambda: dodaj_obiekt("Pracownik")).grid(row=1, column=1)
Button(root, text="Dodaj pododdział", command=lambda: dodaj_obiekt("Pododdział")).grid(row=1, column=2)
Button(root, text="Dodaj żołnierza", command=lambda: dodaj_obiekt("Żołnierz")).grid(row=1, column=3)

# Przyciski list w wierszu 3
Button(root, text="Lista jednostek", command=lambda: popup_lista(jednostki, "Jednostka")).grid(row=3, column=0)
Button(root, text="Lista pracowników", command=lambda: popup_lista(pracownicy, "Pracownik")).grid(row=3, column=1)
Button(root, text="Lista pododdziałów", command=lambda: popup_lista(pododdzialy, "Pododdział")).grid(row=3, column=2)
Button(root, text="Lista żołnierzy", command=lambda: popup_lista(zolnierze, "Żołnierz")).grid(row=3, column=3)

map_widget = tkintermapview.TkinterMapView(root, width=1300, height=500)
map_widget.set_position(52.23, 21.01)  # Warszawa
map_widget.set_zoom(6)
map_widget.grid(row=10, column=0, columnspan=4)

def get_coordinates(miejscowosc):
    try:
        url = f"https://nominatim.openstreetmap.org/search?format=json&q={miejscowosc}"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).json()
        if response:
            latitude = float(response[0]["lat"])
            longitude = float(response[0]["lon"])
            return [latitude, longitude]
        else:
            return [0, 0]
    except:
        return [0, 0]

class Jednostka:
    def __init__(self, nazwa, miejscowosc):
        self.nazwa = nazwa
        self.miejscowosc = miejscowosc
        self.coordinates = get_coordinates(miejscowosc)
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=self.nazwa)
        self.pracownicy = []
        self.pododdzialy = []
        self.zolnierze = []

class Pracownik:
    def __init__(self, imie_nazwisko, stanowisko, miejscowosc, jednostka=None):
        self.imie_nazwisko = imie_nazwisko
        self.stanowisko = stanowisko
        self.miejscowosc = miejscowosc
        self.coordinates = get_coordinates(miejscowosc)
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=self.imie_nazwisko)
        self.jednostka = jednostka
        if jednostka:
            jednostka.pracownicy.append(self)

class Pododdzial:
    def __init__(self, nazwa, miejscowosc, jednostka=None):
        self.nazwa = nazwa
        self.miejscowosc = miejscowosc
        self.coordinates = get_coordinates(miejscowosc)
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=self.nazwa)
        self.jednostka = jednostka
        if jednostka:
            jednostka.pododdzialy.append(self)

class Zolnierz:
    def __init__(self, imie_nazwisko, stopien, miejscowosc, jednostka=None):
        self.imie_nazwisko = imie_nazwisko
        self.stopien = stopien
        self.miejscowosc = miejscowosc
        self.coordinates = get_coordinates(miejscowosc)
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=self.imie_nazwisko)
        self.jednostka = jednostka
        if jednostka:
            jednostka.zolnierze.append(self)

def popup_lista(obiekty, typ):
    popup = Toplevel()
    popup.title(f"Lista: {typ}")
    listbox = Listbox(popup, width=70)
    listbox.pack()

    for i, obj in enumerate(obiekty):
        if typ == "Jednostka":
            listbox.insert(END, f"{i+1}. {obj.nazwa} ({obj.miejscowosc})")
        elif typ == "Pracownik":
            listbox.insert(END, f"{i+1}. {obj.imie_nazwisko} - {obj.stanowisko} ({obj.miejscowosc})")
        elif typ == "Pododdział":
            listbox.insert(END, f"{i+1}. {obj.nazwa} ({obj.miejscowosc})")
        elif typ == "Żołnierz":
            listbox.insert(END, f"{i+1}. {obj.stopien} {obj.imie_nazwisko} ({obj.miejscowosc})")

    def on_select(event):
        if not listbox.curselection():
            return
        index = listbox.curselection()[0]
        obj = obiekty[index]

        detail_popup = Toplevel()
        detail_popup.title("Szczegóły")

        if typ == "Jednostka":
            Label(detail_popup, text=f"Nazwa: {obj.nazwa}").pack()
            Label(detail_popup, text=f"Miejscowość: {obj.miejscowosc}").pack()
            Label(detail_popup, text="--- Powiązani ---").pack()
            Label(detail_popup, text=f"Pracownicy: {[p.imie_nazwisko for p in obj.pracownicy]}").pack()
            Label(detail_popup, text=f"Pododdziały: {[p.nazwa for p in obj.pododdzialy]}").pack()
            Label(detail_popup, text=f"Żołnierze: {[z.imie_nazwisko for z in obj.zolnierze]}").pack()
        elif typ == "Pracownik":
            Label(detail_popup, text=f"Imię i nazwisko: {obj.imie_nazwisko}").pack()
            Label(detail_popup, text=f"Stanowisko: {obj.stanowisko}").pack()
            Label(detail_popup, text=f"Miejscowość: {obj.miejscowosc}").pack()
        elif typ == "Pododdział":
            Label(detail_popup, text=f"Nazwa: {obj.nazwa}").pack()
            Label(detail_popup, text=f"Miejscowość: {obj.miejscowosc}").pack()
        elif typ == "Żołnierz":
            Label(detail_popup, text=f"Imię i nazwisko: {obj.imie_nazwisko}").pack()
            Label(detail_popup, text=f"Stopień: {obj.stopien}").pack()
            Label(detail_popup, text=f"Miejscowość: {obj.miejscowosc}").pack()

        def usun():
            obj.marker.delete()
            obiekty.pop(index)
            if typ != "Jednostka" and obj.jednostka:
                if typ == "Pracownik":
                    obj.jednostka.pracownicy.remove(obj)
                elif typ == "Pododdział":
                    obj.jednostka.pododdzialy.remove(obj)
                elif typ == "Żołnierz":
                    obj.jednostka.zolnierze.remove(obj)
            detail_popup.destroy()
            popup.destroy()
            popup_lista(obiekty, typ)

        def edytuj():
            edit_popup = Toplevel()
            edit_popup.title("Edytuj")

            entries = []

            def entry_row(label_text, value, row):
                Label(edit_popup, text=label_text).grid(row=row, column=0)
                e = Entry(edit_popup)
                e.insert(0, value)
                e.grid(row=row, column=1)
                entries.append(e)

            row = 0
            if typ == "Jednostka":
                entry_row("Nazwa", obj.nazwa, row)
                row += 1
                entry_row("Miejscowość", obj.miejscowosc, row)
            elif typ == "Pracownik":
                entry_row("Imię i nazwisko", obj.imie_nazwisko, row)
                row += 1
                entry_row("Stanowisko", obj.stanowisko, row)
                row += 1
                entry_row("Miejscowość", obj.miejscowosc, row)
            elif typ == "Pododdział":
                entry_row("Nazwa", obj.nazwa, row)
                row += 1
                entry_row("Miejscowość", obj.miejscowosc, row)
            elif typ == "Żołnierz":
                entry_row("Imię i nazwisko", obj.imie_nazwisko, row)
                row += 1
                entry_row("Stopień", obj.stopien, row)
                row += 1
                entry_row("Miejscowość", obj.miejscowosc, row)

            def zapisz_zmiany():
                obj.marker.delete()
                if typ == "Jednostka":
                    obj.nazwa = entries[0].get()
                    obj.miejscowosc = entries[1].get()
                elif typ == "Pracownik":
                    obj.imie_nazwisko = entries[0].get()
                    obj.stanowisko = entries[1].get()
                    obj.miejscowosc = entries[2].get()
                elif typ == "Pododdział":
                    obj.nazwa = entries[0].get()
                    obj.miejscowosc = entries[1].get()
                elif typ == "Żołnierz":
                    obj.imie_nazwisko = entries[0].get()
                    obj.stopien = entries[1].get()
                    obj.miejscowosc = entries[2].get()

                obj.coordinates = get_coordinates(obj.miejscowosc)
                label = obj.nazwa if hasattr(obj, "nazwa") else obj.imie_nazwisko
                obj.marker = map_widget.set_marker(obj.coordinates[0], obj.coordinates[1], text=label)

                edit_popup.destroy()
                detail_popup.destroy()
                popup.destroy()
                popup_lista(obiekty, typ)

            Button(edit_popup, text="Zapisz", command=zapisz_zmiany).grid(row=row + 1, column=0, columnspan=2)

        Button(detail_popup, text="Usuń", command=usun).pack()
        Button(detail_popup, text="Edytuj", command=edytuj).pack()

    listbox.bind("<<ListboxSelect>>", on_select)

def dodaj_obiekt(typ):
    popup = Toplevel()
    popup.title(f"Dodaj {typ}")

    jednostka_var = StringVar(popup)
    jednostka_var.set("Brak")

    row = 0

    if typ != "Jednostka":
        Label(popup, text="Przypisz do jednostki:").grid(row=row, column=0)
        jednostka_menu = OptionMenu(popup, jednostka_var, "Brak", *[j.nazwa for j in jednostki])
        jednostka_menu.grid(row=row, column=1)
        row += 1

    if typ == "Jednostka":
        Label(popup, text="Nazwa:").grid(row=row, column=0)
        entry1 = Entry(popup)
        entry1.grid(row=row, column=1)
        row += 1
        Label(popup, text="Miejscowość:").grid(row=row, column=0)
        entry2 = Entry(popup)
        entry2.grid(row=row, column=1)

        def save():
            jednostki.append(Jednostka(entry1.get(), entry2.get()))
            popup.destroy()

    elif typ == "Pracownik":
        Label(popup, text="Imię i nazwisko:").grid(row=row, column=0)
        entry1 = Entry(popup)
        entry1.grid(row=row, column=1)
        row += 1
        Label(popup, text="Stanowisko:").grid(row=row, column=0)
        entry2 = Entry(popup)
        entry2.grid(row=row, column=1)
        row += 1
        Label(popup, text="Miejscowość:").grid(row=row, column=0)
        entry3 = Entry(popup)
        entry3.grid(row=row, column=1)

        def save():
            jednostka = next((j for j in jednostki if j.nazwa == jednostka_var.get()), None)
            pracownicy.append(Pracownik(entry1.get(), entry2.get(), entry3.get(), jednostka))
            popup.destroy()

    elif typ == "Pododdział":
        Label(popup, text="Nazwa:").grid(row=row, column=0)
        entry1 = Entry(popup)
        entry1.grid(row=row, column=1)
        row += 1
        Label(popup, text="Miejscowość:").grid(row=row, column=0)
        entry2 = Entry(popup)
        entry2.grid(row=row, column=1)

        def save():
            jednostka = next((j for j in jednostki if j.nazwa == jednostka_var.get()), None)
            pododdzialy.append(Pododdzial(entry1.get(), entry2.get(), jednostka))
            popup.destroy()

    elif typ == "Żołnierz":
        Label(popup, text="Imię i nazwisko:").grid(row=row, column=0)
        entry1 = Entry(popup)
        entry1.grid(row=row, column=1)
        row += 1
        Label(popup, text="Stopień:").grid(row=row, column=0)
        entry2 = Entry(popup)
        entry2.grid(row=row, column=1)
        row += 1
        Label(popup, text="Miejscowość:").grid(row=row, column=0)
        entry3 = Entry(popup)
        entry3.grid(row=row, column=1)

        def save():
            jednostka = next((j for j in jednostki if j.nazwa == jednostka_var.get()), None)
            zolnierze.append(Zolnierz(entry1.get(), entry2.get(), entry3.get(), jednostka))
            popup.destroy()

    Button(popup, text="Zapisz", command=save).grid(row=row + 1, column=0, columnspan=2)

root.mainloop()
