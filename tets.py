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

class Pracownik:
    def __init__(self, imie_nazwisko, stanowisko, miejscowosc):
        self.imie_nazwisko = imie_nazwisko
        self.stanowisko = stanowisko
        self.miejscowosc = miejscowosc
        self.coordinates = get_coordinates(miejscowosc)
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=self.imie_nazwisko)

class Pododdzial:
    def __init__(self, nazwa, miejscowosc):
        self.nazwa = nazwa
        self.miejscowosc = miejscowosc
        self.coordinates = get_coordinates(miejscowosc)
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=self.nazwa)

class Zolnierz:
    def __init__(self, imie_nazwisko, stopien, miejscowosc):
        self.imie_nazwisko = imie_nazwisko
        self.stopien = stopien
        self.miejscowosc = miejscowosc
        self.coordinates = get_coordinates(miejscowosc)
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=self.imie_nazwisko)

def popup_lista(obiekty, typ):
    popup = Toplevel()
    popup.title(f"Lista: {typ}")
    listbox = Listbox(popup, width=50)
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

        Button(detail_popup, text="Usuń", command=lambda: [obj.marker.delete(), obiekty.pop(index), popup.destroy(), popup_lista(obiekty, typ)]).pack()

    listbox.bind("<<ListboxSelect>>", on_select)

def dodaj_obiekt(typ):
    popup = Toplevel()
    popup.title(f"Dodaj {typ}")

    if typ == "Jednostka":
        Label(popup, text="Nazwa:").grid(row=0, column=0)
        entry1 = Entry(popup)
        entry1.grid(row=0, column=1)
        Label(popup, text="Miejscowość:").grid(row=1, column=0)
        entry2 = Entry(popup)
        entry2.grid(row=1, column=1)

        def save():
            jednostki.append(Jednostka(entry1.get(), entry2.get()))
            popup.destroy()

    elif typ == "Pracownik":
        Label(popup, text="Imię i nazwisko:").grid(row=0, column=0)
        entry1 = Entry(popup)
        entry1.grid(row=0, column=1)
        Label(popup, text="Stanowisko:").grid(row=1, column=0)
        entry2 = Entry(popup)
        entry2.grid(row=1, column=1)
        Label(popup, text="Miejscowość:").grid(row=2, column=0)
        entry3 = Entry(popup)
        entry3.grid(row=2, column=1)

        def save():
            pracownicy.append(Pracownik(entry1.get(), entry2.get(), entry3.get()))
            popup.destroy()

    elif typ == "Pododdział":
        Label(popup, text="Nazwa:").grid(row=0, column=0)
        entry1 = Entry(popup)
        entry1.grid(row=0, column=1)
        Label(popup, text="Miejscowość:").grid(row=1, column=0)
        entry2 = Entry(popup)
        entry2.grid(row=1, column=1)

        def save():
            pododdzialy.append(Pododdzial(entry1.get(), entry2.get()))
            popup.destroy()

    elif typ == "Żołnierz":
        Label(popup, text="Imię i nazwisko:").grid(row=0, column=0)
        entry1 = Entry(popup)
        entry1.grid(row=0, column=1)
        Label(popup, text="Stopień:").grid(row=1, column=0)
        entry2 = Entry(popup)
        entry2.grid(row=1, column=1)
        Label(popup, text="Miejscowość:").grid(row=2, column=0)
        entry3 = Entry(popup)
        entry3.grid(row=2, column=1)

        def save():
            zolnierze.append(Zolnierz(entry1.get(), entry2.get(), entry3.get()))
            popup.destroy()

    Button(popup, text="Zapisz", command=save).grid(row=3, column=0, columnspan=2)

Button(root, text="Dodaj jednostkę", command=lambda: dodaj_obiekt("Jednostka")).grid(row=0, column=0)
Button(root, text="Dodaj pracownika", command=lambda: dodaj_obiekt("Pracownik")).grid(row=0, column=1)
Button(root, text="Dodaj pododdział", command=lambda: dodaj_obiekt("Pododdział")).grid(row=0, column=2)
Button(root, text="Dodaj żołnierza", command=lambda: dodaj_obiekt("Żołnierz")).grid(row=0, column=3)

Button(root, text="Lista jednostek", command=lambda: popup_lista(jednostki, "Jednostka")).grid(row=2, column=0)
Button(root, text="Lista pracowników", command=lambda: popup_lista(pracownicy, "Pracownik")).grid(row=2, column=1)
Button(root, text="Lista pododdziałów", command=lambda: popup_lista(pododdzialy, "Pododdział")).grid(row=2, column=2)
Button(root, text="Lista żołnierzy", command=lambda: popup_lista(zolnierze, "Żołnierz")).grid(row=2, column=3)

root.mainloop()
