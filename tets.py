# from cProfile import label
from tkinter import *
import tkintermapview

users = []

class User:
    def __init__(self, nazwa, pracownicy, pododdzial, zolnierze):
        self.nazwa = nazwa
        self.pracownicy = pracownicy
        self.pododdzial = pododdzial
        self.zolnierze = zolnierze
        self.coordinates = self.get_coordinates
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1])

    def get_coordinates(self) -> list:
        try:
            import requests
            from bs4 import BeautifulSoup
            address_url: str = f"https://pl.wikipedia.org/wiki/{self.pododdzial}"
            response = requests.get(address_url).text
            response_html = BeautifulSoup(response, "html.parser")
            longitude: float = float(response_html.select(".longitude")[1].text.replace(",", "."))
            latitude: float = float(response_html.select(".latitude")[1].text.replace(",", "."))
            return [latitude, longitude]
        except:
            return [0, 0]

def add_user():
    nazwa = entry_nazwa.get()
    pracownicy = entry_pracownicy.get()
    pododdzial = entry_pododdzial.get()
    zolnierze = entry_zolnierze.get()

    new_user = User(nazwa=nazwa, pracownicy=pracownicy, pododdzial=pododdzial, zolnierze=zolnierze)
    users.append(new_user)

    entry_nazwa.delete(0, END)
    entry_pracownicy.delete(0, END)
    entry_pododdzial.delete(0, END)
    entry_zolnierze.delete(0, END)
    entry_nazwa.focus()
    show_users()
    update_map()

def show_users():
    listbox_lista_obiektow.delete(0, END)
    for idx, user in enumerate(users):
        listbox_lista_obiektow.insert(idx, f"{idx + 1}. {user.nazwa} {user.pracownicy} {user.pododdzial} {user.zolnierze}")

def delete_user():
    try:
        idx = listbox_lista_obiektow.curselection()[0]
        users.projekt(idx)
        show_users()
        update_map()
    except IndexError:
        pass

def user_details():
    try:
        idx = listbox_lista_obiektow.curselection()[0]
        label_nazwa_szczegoly_obiektu_wartosc.configure(text=users[idx].nazwa)
        label_pracownicy_szczegoly_obiektu_wartosc.configure(text=users[idx].pracownicy)
        label_pododdzial_szczegoly_obiektu_wartosc.configure(text=users[idx].pododdzial)
        label_zolnierze_szczegoly_obiektu_wartosc.configure(text=users[idx].zolnierze)
        map_widget.set_position(users[idx].coordinates[0], users[idx].coordinates[1])
        map_widget.set_zoom(17)
    except IndexError:
        pass

def edit_user():
    try:
        idx = listbox_lista_obiektow.curselection()[0]
        entry_nazwa.delete(0, END)
        entry_nazwa.insert(0, users[idx].nazwa)
        entry_pracownicy.delete(0, END)
        entry_pracownicy.insert(0, users[idx].nazwa)
        entry_pododdzial.delete(0, END)
        entry_pododdzial.insert(0, users[idx].nazwa)
        entry_zolnierze.delete(0, END)
        entry_zolnierze.insert(0, users[idx].nazwa)

        button_dodaj_obiekt.configure(text="Zapisz", command=lambda: update_users(idx))
    except IndexError:
        pass

def update_users(idx):
    nazwa = entry_nazwa.get()
    pracownicy = entry_pracownicy.get()
    pododdzial = entry_pododdzial.get()
    zolnierze = entry_zolnierze.get()

    users[idx].nazwa = nazwa
    users[idx].pracownicy = pracownicy
    users[idx].pododdzial = pododdzial
    users[idx].zolnierze = zolnierze
    users[idx].coordinates = users[idx].get_coordinates()
    users[idx].marker = map_widget.set_marker(users[idx].coordinates[0], users[idx].coordinates[1])

    button_dodaj_obiekt.configure(text="Dodaj", command=add_user)
    entry_nazwa.delete(0, END)
    entry_pracownicy.delete(0, END)
    entry_pododdzial.delete(0, END)
    entry_zolnierze.delete(0, END)
    entry_nazwa.focus()
    show_users()
    update_map()

def update_map():
    map_widget.delete_all_marker()
    for user in users:
        if user.coordinates:
            map_widget.set_position(user.coordinates[0], user.coordinates[1])
            map_widget.set_marker(user.coordinates[0], user.coordinates[1], text=user.nazwa)

root = Tk()
root.title("System zarządzania jednostkami wojskowymi")
root.geometry("1024x768")

ramka_lista_obiektow = Frame(root)
ramka_formularz = Frame(root)
ramka_szczegol_obiektow = Frame(root)
ramka_mapa = Frame(root)

ramka_lista_obiektow.grid(row=0, column=0)
ramka_formularz.grid(row=0, column=1)
ramka_szczegol_obiektow.grid(row=1, column=0)
ramka_mapa.grid(row=2, column=0, columnspan=2)

label_jednostek = Label(ramka_szczegol_obiektow, text="Lista jednostek wojskowych:")
label_jednostek.grid(row=0, column=0, columnspan=3)
listbox_lista_obiektow = Listbox()
listbox_lista_obiektow.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly = Button(ramka_szczegol_obiektow, text="Pokaż Szczegóły", command=user_details)
button_pokaz_szczegoly.grid(row=2, column=0)
button_edytuj_obiekt = Button(ramka_szczegol_obiektow, text="Edytuj obiekt", command=edit_user)
button_edytuj_obiekt.grid(row=2, column=1)
button_usun_obiekt = Button(ramka_szczegol_obiektow, text="Usuń obiekt", command=delete_user)
button_usun_obiekt.grid(row=2, column=2)
button_usun_obiekt.grid(row=2, column=2)

label_formularz = Label(ramka_formularz, text="Formularz: ")
label_formularz.grid(row=0, column=0, columnspan=2, )
label_nazwa = Label(ramka_formularz, text="Nazwa jednostki: ")
label_nazwa.grid(row=1, column=0, sticky=W)
label_pracownicy = Label(ramka_formularz, text="Pracownicy: ")
label_pracownicy.grid(row=2, column=0, sticky=W)
label_pododdzial = Label(ramka_formularz, text="Nazwa pododdziału: ")
label_pododdzial.grid(row=3, column=0, sticky=W)
label_zolnierze = Label(ramka_formularz, text="Żołnierze: ")
label_zolnierze.grid(row=4, column=0, sticky=W)

entry_nazwa = Entry(ramka_formularz)
entry_nazwa.grid(row=1, column=1, sticky=W)
entry_pracownicy = Entry(ramka_formularz)
entry_pracownicy.grid(row=2, column=1, sticky=W)
entry_pododdzial = Entry(ramka_formularz)
entry_pododdzial.grid(row=3, column=1, sticky=W)
entry_zolnierze = Entry(ramka_formularz)
entry_zolnierze.grid(row=4, column=1, sticky=W)

button_dodaj_obiekt = Button(ramka_formularz, text="Dodaj", command=add_user)
button_dodaj_obiekt.grid(row=5, column=1, columnspan=2)

label_szczegoly_obiektu = Label(ramka_szczegol_obiektow, text="Szczegóły: ")
label_szczegoly_obiektu.grid(row=0, column=0, sticky=W)

label_nazwa_szczegoly_obiektu = Label(ramka_szczegol_obiektow, text="Nazwa jednostki: ")
label_nazwa_szczegoly_obiektu.grid(row=1, column=0, )
label_nazwa_szczegoly_obiektu_wartosc = Label(ramka_szczegol_obiektow, text="....")
label_nazwa_szczegoly_obiektu_wartosc.grid(row=1, column=1, )

label_pracownicy_szczegoly_obiektu = Label(ramka_szczegol_obiektow, text="Pracownicy: ")
label_pracownicy_szczegoly_obiektu.grid(row=2, column=0, )
label_pracownicy_szczegoly_obiektu_wartosc = Label(ramka_szczegol_obiektow, text="....")
label_pracownicy_szczegoly_obiektu_wartosc.grid(row=2, column=1, )

label_pododdzial_szczegoly_obiektu = Label(ramka_szczegol_obiektow, text="Pododdziały: ")
label_pododdzial_szczegoly_obiektu.grid(row=3, column=0, )
label_pododdzial_szczegoly_obiektu_wartosc = Label(ramka_szczegol_obiektow, text="....")
label_pododdzial_szczegoly_obiektu_wartosc.grid(row=3, column=1, )

label_zolnierze_szczegoly_obiektu = Label(ramka_szczegol_obiektow, text="Żołnierze: ")
label_zolnierze_szczegoly_obiektu.grid(row=4, column=0, )
label_zolnierze_szczegoly_obiektu_wartosc = Label(ramka_szczegol_obiektow, text="....")
label_zolnierze_szczegoly_obiektu_wartosc.grid(row=4, column=1, )

map_widget = tkintermapview.TkinterMapView(width=1024, height=400)
map_widget.set_position(52.23, 21)
map_widget.set_zoom(5)
map_widget.grid(row=0, column=0, columnspan=8)

root.mainloop()