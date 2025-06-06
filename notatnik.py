from tkinter import *
import tkintermapview

# Listy i klasy takie jak wcześniej - dla przejrzystości pomijam ich definicję
jednostki = []
pracownicy = []
pododdzialy = []
zolnierze = []

class Jednostka:
    def __init__(self, nazwa, miejscowosc):
        self.nazwa = nazwa
        self.miejscowosc = miejscowosc
        self.coordinates = (0, 0)

class Pracownik:
    def __init__(self, imie_nazwisko, stanowisko):
        self.imie_nazwisko = imie_nazwisko
        self.stanowisko = stanowisko

class Pododdzial:
    def __init__(self, nazwa):
        self.nazwa = nazwa

class Zolnierz:
    def __init__(self, imie_nazwisko, stopien):
        self.imie_nazwisko = imie_nazwisko
        self.stopien = stopien

def dodaj_jednostke():
    nazwa = entry_jednostka_nazwa.get()
    miejscowosc = entry_jednostka_miejscowosc.get()
    if nazwa and miejscowosc:
        jednostki.append(Jednostka(nazwa, miejscowosc))
        entry_jednostka_nazwa.delete(0, END)
        entry_jednostka_miejscowosc.delete(0, END)
        pokaz_jednostki()

def usun_jednostke():
    try:
        idx = listbox_jednostki.curselection()[0]
        del jednostki[idx]
        pokaz_jednostki()
    except IndexError:
        pass

def pokaz_jednostki():
    listbox_jednostki.delete(0, END)
    for i, j in enumerate(jednostki):
        listbox_jednostki.insert(END, f"{i+1}. {j.nazwa} ({j.miejscowosc})")

def pokaz_szczegoly_jednostki():
    try:
        idx = listbox_jednostki.curselection()[0]
        j = jednostki[idx]
        label_szczegoly_jednostki.config(text=f"Nazwa: {j.nazwa}\nMiejscowość: {j.miejscowosc}")
    except IndexError:
        pass

def dodaj_pracownika():
    imie = entry_pracownik_imie.get()
    stanowisko = entry_pracownik_stanowisko.get()
    if imie and stanowisko:
        pracownicy.append(Pracownik(imie, stanowisko))
        entry_pracownik_imie.delete(0, END)
        entry_pracownik_stanowisko.delete(0, END)
        pokaz_pracownikow()

def usun_pracownika():
    try:
        idx = listbox_pracownicy.curselection()[0]
        del pracownicy[idx]
        pokaz_pracownikow()
    except IndexError:
        pass

def pokaz_pracownikow():
    listbox_pracownicy.delete(0, END)
    for i, p in enumerate(pracownicy):
        listbox_pracownicy.insert(END, f"{i+1}. {p.imie_nazwisko} - {p.stanowisko}")

def pokaz_szczegoly_pracownika():
    try:
        idx = listbox_pracownicy.curselection()[0]
        p = pracownicy[idx]
        label_szczegoly_pracownika.config(text=f"Imię i nazwisko: {p.imie_nazwisko}\nStanowisko: {p.stanowisko}")
    except IndexError:
        pass

def dodaj_pododdzial():
    nazwa = entry_pododdzial_nazwa.get()
    if nazwa:
        pododdzialy.append(Pododdzial(nazwa))
        entry_pododdzial_nazwa.delete(0, END)
        pokaz_pododdzialy()

def usun_pododdzial():
    try:
        idx = listbox_pododdzialy.curselection()[0]
        del pododdzialy[idx]
        pokaz_pododdzialy()
    except IndexError:
        pass

def pokaz_pododdzialy():
    listbox_pododdzialy.delete(0, END)
    for i, p in enumerate(pododdzialy):
        listbox_pododdzialy.insert(END, f"{i+1}. {p.nazwa}")

def pokaz_szczegoly_pododdzialu():
    try:
        idx = listbox_pododdzialy.curselection()[0]
        p = pododdzialy[idx]
        label_szczegoly_pododdzialu.config(text=f"Nazwa: {p.nazwa}")
    except IndexError:
        pass

def dodaj_zolnierza():
    imie = entry_zolnierz_imie.get()
    stopien = entry_zolnierz_stopien.get()
    if imie and stopien:
        zolnierze.append(Zolnierz(imie, stopien))
        entry_zolnierz_imie.delete(0, END)
        entry_zolnierz_stopien.delete(0, END)
        pokaz_zolnierzy()

def usun_zolnierza():
    try:
        idx = listbox_zolnierze.curselection()[0]
        del zolnierze[idx]
        pokaz_zolnierzy()
    except IndexError:
        pass

def pokaz_zolnierzy():
    listbox_zolnierze.delete(0, END)
    for i, z in enumerate(zolnierze):
        listbox_zolnierze.insert(END, f"{i+1}. {z.imie_nazwisko} - {z.stopien}")

def pokaz_szczegoly_zolnierza():
    try:
        idx = listbox_zolnierze.curselection()[0]
        z = zolnierze[idx]
        label_szczegoly_zolnierza.config(text=f"Imię i nazwisko: {z.imie_nazwisko}\nStopień: {z.stopien}")
    except IndexError:
        pass