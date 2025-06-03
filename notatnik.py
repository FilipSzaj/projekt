#from cProfile import label
from tkinter import *
import tkintermapview

from proj import listbox_lista_obiektow, update_map, label_name_szczegoly_obiektu_wartosc, map_widget, \
    buttton_dodaj_obiekt, label_lista_obiektow, button_pokaz_szczegoly, button_edytuj_obiekt, button_usun_obiekt

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

    new_user = User(nazwa=Nazwa jednostki, pracownicy=Pracownicy, pododdzial=Pododdział w jednostce, zolnierze=Żołnierze)
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
        label_name_szczegoly_obiektu_wartosc.configure(text=users[idx].nazwa)
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

        buttton_dodaj_obiekt.configure(text="Zapisz", command=lambda: update_users(idx))
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

    buttton_dodaj_obiekt.configure(text="Dodaj", command=add_user)
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
root.title("GÓWNO")
root.geometry("1024x768")

ramka_lista_obiektow = Frame(root)
ramka_formularz = Frame(root)
ramka_szczegol_obiektow = Frame(root)
ramka_mapa = Frame(root)

ramka_lista_obiektow.grid(row=0, column=0)
ramka_formularz.grid(row=0, column=1)
ramka_szczegol_obiektow.grid(row=1, column=0)
ramka_mapa.grid(row=2, column=0, columnspan=2)

label_jednostek = Label(ramka_jednostki, text="Lista jednostek wojskowych:")
label_jednostek.grid(row=0, column=0, columnspan=3)
listbox_lista_obiektow = Listbox(ramka_jednostek)
listbox_lista_obiektow.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly = Button(ramka_jednostki, text="Pokaż Szczegóły", command=user_details)
button_pokaz_szczegoly.grid(row=2, column=0)
button_edytuj_obiekt = Button(ramka_jednostki, text="Edytuj obiekt", command=edit_user)
button_edytuj_obiekt.grid(row=2, column=1)
button_usun_obiekt = Button(ramka_jednostki, text="Usuń obiekt", command=delete_user)
button_usun_obiekt.grid(row=2, column=2)
button_usun_obiekt.grid(row=2, column=2)

label_formularz = Label(ramka_formularz, text="Formularz: ")
label_formularz.grid(row=0, column=0, columnspan=2, )
label_nazwa = Label(ramka_formularz, text="Nazwa jednostki: ")
label_nazwa.grid(row=1, column=0, sticky=W)
