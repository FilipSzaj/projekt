from tkinter import *
import tkintermapview

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


root = Tk()
root.title("Zarządzanie jednostkami wojskowymi")
root.geometry("1200x700")

Label(root, text="Jednostki", font=("Arial", 14, "bold")).grid(row=0, column=0)
Label(root, text="Nazwa:").grid(row=1, column=0, sticky=W)
entry_jednostka_nazwa = Entry(root, width=25)
entry_jednostka_nazwa.grid(row=2, column=0)

Label(root, text="Miejscowość:").grid(row=3, column=0, sticky=W)
entry_jednostka_miejscowosc = Entry(root, width=25)
entry_jednostka_miejscowosc.grid(row=4, column=0)

frame_jednostka_buttons = Frame(root)
frame_jednostka_buttons.grid(row=5, column=0)

Button(frame_jednostka_buttons, text="Dodaj", command=dodaj_jednostke, width=10).grid(row=0, column=0)
Button(frame_jednostka_buttons, text="Usuń", command=usun_jednostke, width=10).grid(row=0, column=1)
Button(frame_jednostka_buttons, text="Szczegóły", command=pokaz_szczegoly_jednostki, width=10).grid(row=0, column=2)

listbox_jednostki = Listbox(root, width=30, height=10)
listbox_jednostki.grid(row=8, column=0)

label_szczegoly_jednostki = Label(root, text="Szczegóły jednostki...", justify=LEFT, anchor="w", width=30, height=4, relief=SUNKEN)
label_szczegoly_jednostki.grid(row=9, column=0)

Label(root, text="Pracownicy", font=("Arial", 14, "bold")).grid(row=0, column=1)
Label(root, text="Imię i nazwisko:").grid(row=1, column=1, sticky=W)
entry_pracownik_imie = Entry(root, width=25)
entry_pracownik_imie.grid(row=2, column=1)

Label(root, text="Stanowisko:").grid(row=3, column=1, sticky=W)
entry_pracownik_stanowisko = Entry(root, width=25)
entry_pracownik_stanowisko.grid(row=4, column=1)

frame_pracownik_buttons = Frame(root)
frame_pracownik_buttons.grid(row=5, column=1)

Button(frame_pracownik_buttons, text="Dodaj", command=dodaj_pracownika, width=10).grid(row=0, column=0)
Button(frame_pracownik_buttons, text="Usuń", command=usun_pracownika, width=10).grid(row=0, column=1)
Button(frame_pracownik_buttons, text="Szczegóły", command=pokaz_szczegoly_pracownika, width=10).grid(row=0, column=2)

listbox_pracownicy = Listbox(root, width=30, height=10)
listbox_pracownicy.grid(row=8, column=1)

label_szczegoly_pracownika = Label(root, text="Szczegóły pracownika...", justify=LEFT, anchor="w", width=30, height=4, relief=SUNKEN)
label_szczegoly_pracownika.grid(row=9, column=1)

Label(root, text="Pododdziały", font=("Arial", 14, "bold")).grid(row=0, column=2)
Label(root, text="Nazwa:").grid(row=1, column=2, sticky=W)
entry_pododdzial_nazwa = Entry(root, width=25)
entry_pododdzial_nazwa.grid(row=2, column=2)

frame_pododdzial_buttons = Frame(root)
frame_pododdzial_buttons.grid(row=5, column=2)

Button(frame_pododdzial_buttons, text="Dodaj", command=dodaj_pododdzial, width=10).grid(row=0, column=0)
Button(frame_pododdzial_buttons, text="Usuń", command=usun_pododdzial, width=10).grid(row=0, column=1)
Button(frame_pododdzial_buttons, text="Szczegóły", command=pokaz_szczegoly_pododdzialu, width=10).grid(row=0, column=2)

listbox_pododdzialy = Listbox(root, width=30, height=10)
listbox_pododdzialy.grid(row=8, column=2)

label_szczegoly_pododdzialu = Label(root, text="Szczegóły pododdziału...", justify=LEFT, anchor="w", width=30, height=4, relief=SUNKEN)
label_szczegoly_pododdzialu.grid(row=9, column=2)

Label(root, text="Żołnierze", font=("Arial", 14, "bold")).grid(row=0, column=3)
Label(root, text="Imię i nazwisko:").grid(row=1, column=3, sticky=W)
entry_zolnierz_imie = Entry(root, width=25)
entry_zolnierz_imie.grid(row=2, column=3)

Label(root, text="Stopień:").grid(row=3, column=3, sticky=W)
entry_zolnierz_stopien = Entry(root, width=25)
entry_zolnierz_stopien.grid(row=4, column=3)

frame_zolnierz_buttons = Frame(root)
frame_zolnierz_buttons.grid(row=5, column=3)

Button(frame_zolnierz_buttons, text="Dodaj", command=dodaj_zolnierza, width=10).grid(row=0, column=0)
Button(frame_zolnierz_buttons, text="Usuń", command=usun_zolnierza, width=10).grid(row=0, column=1)
Button(frame_zolnierz_buttons, text="Szczegóły", command=pokaz_szczegoly_zolnierza, width=10).grid(row=0, column=2)

listbox_zolnierze = Listbox(root, width=30, height=10)
listbox_zolnierze.grid(row=8, column=3)

label_szczegoly_zolnierza = Label(root, text="Szczegóły żołnierza...", justify=LEFT, anchor="w", width=30, height=4, relief=SUNKEN)
label_szczegoly_zolnierza.grid(row=9, column=3)

map_widget = tkintermapview.TkinterMapView(root, width=1200, height=250)
map_widget.set_position(52.23, 21)
map_widget.set_zoom(6)
map_widget.grid(row=10, column=0, columnspan=4)

root.mainloop()
