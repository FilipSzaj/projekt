from tkinter import *
from tkinter import messagebox
import tkintermapview


def get_coordinates(location):
    try:
        import requests
        from bs4 import BeautifulSoup
        address_url = f"https://pl.wikipedia.org/wiki/{location}"
        response = requests.get(address_url, timeout=5)  # dodaj timeout
        if response.status_code != 200:
            return [52.23, 21.0]  # domyślne współrzędne
        response_html = BeautifulSoup(response.text, "html.parser")
        longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
        latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
        return [latitude, longitude]
    except Exception as e:
        print(f"Błąd pobierania współrzędnych: {e}")
        return [52.23, 21.0]  # domyślne współrzędne (Warszawa)


class MilitarySystem:
    def __init__(self):
        self.units_listbox = None
        self.map_widget = None
        self.map_frame = None
        self.menu_frame = None
        self.password_entry = None
        self.login_entry = None
        self.login_frame = None
        self.root = Tk()
        self.root.title("System Zarządzania Jednostkami Wojskowymi")
        self.root.geometry("1024x768")
        
        self.users = {
            "admin": "admin123",  # Login: admin, Hasło: admin123
            "dowodca": "dow123"   # Login: dowodca, Hasło: dow123
        }
        
        self.military_units = []
        self.employees = []
        self.soldiers = []
        self.subunits = []
        
        self.current_user = None
        self.show_login_screen()

    def show_login_screen(self):
        self.login_frame = Frame(self.root)
        self.login_frame.pack(pady=20)
        
        Label(self.login_frame, text="Login:").grid(row=0, column=0, pady=5)
        self.login_entry = Entry(self.login_frame)
        self.login_entry.grid(row=0, column=1, pady=5)
        
        Label(self.login_frame, text="Hasło:").grid(row=1, column=0, pady=5)
        self.password_entry = Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)
        
        Button(self.login_frame, text="Zaloguj", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.login_entry.get()
        password = self.password_entry.get()
        
        if username in self.users and self.users[username] == password:
            self.current_user = username
            self.login_frame.destroy()
            self.show_main_interface()
        else:
            messagebox.showerror("Błąd", "Nieprawidłowy login lub hasło")

    def show_main_interface(self):
        # Główne menu
        self.menu_frame = Frame(self.root)
        self.menu_frame.pack(fill=X, pady=10)
        
        Button(self.menu_frame, text="Jednostki Wojskowe", command=self.show_military_units).pack(side=LEFT, padx=5)
        Button(self.menu_frame, text="Pracownicy", command=self.show_employees).pack(side=LEFT, padx=5)
        Button(self.menu_frame, text="Pododdziały", command=self.show_subunits).pack(side=LEFT, padx=5)
        Button(self.menu_frame, text="Żołnierze", command=self.show_soldiers).pack(side=LEFT, padx=5)
        Button(self.menu_frame, text="Mapy", command=self.show_maps).pack(side=LEFT, padx=5)
        Button(self.menu_frame, text="Wyloguj", command=self.logout).pack(side=RIGHT, padx=5)

        # Ramka mapy
        self.map_frame = Frame(self.root)
        self.map_frame.pack(fill=BOTH, expand=True, pady=10)
        
        self.map_widget = tkintermapview.TkinterMapView(self.map_frame, width=800, height=400)
        self.map_widget.set_position(52.23, 21)  # Warszawa
        self.map_widget.set_zoom(6)
        self.map_widget.pack(fill=BOTH, expand=True)

    def show_military_units(self):
        window = Toplevel(self.root)
        window.title("Zarządzanie Jednostkami Wojskowymi")
        window.geometry("800x600")
        
        # Formularz dodawania
        form_frame = Frame(window)
        form_frame.pack(pady=10)
        
        Label(form_frame, text="Nazwa jednostki:").grid(row=0, column=0)
        unit_name = Entry(form_frame)
        unit_name.grid(row=0, column=1)
        
        Label(form_frame, text="Lokalizacja:").grid(row=1, column=0)
        unit_location = Entry(form_frame)
        unit_location.grid(row=1, column=1)
        
        button_add = Button(form_frame, text="Dodaj jednostkę")
        button_add.grid(row=2, columnspan=2)
        
        # Lista jednostek
        list_frame = Frame(window)
        list_frame.pack(pady=10, fill=BOTH, expand=True)
        
        self.units_listbox = Listbox(list_frame, width=50, height=15)
        self.units_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        
        scrollbar = Scrollbar(list_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.units_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.units_listbox.yview)
        
        # Przyciski akcji
        button_frame = Frame(window)
        button_frame.pack(pady=5)
        
        def add_unit():
            name = unit_name.get().strip()
            location = unit_location.get().strip()
            
            if not name:
                messagebox.showerror("Błąd", "Nazwa jednostki nie może być pusta")
                return
            if not location:
                messagebox.showerror("Błąd", "Lokalizacja nie może być pusta")
                return
            
            self.military_units.append({
                "name": name,
                "location": location,
                "coordinates": get_coordinates(location)
            })
            self.update_unit_list()
            unit_name.delete(0, END)
            unit_location.delete(0, END)
        
        def edit_unit():
            try:
                idx = self.units_listbox.curselection()[0]
                unit = self.military_units[idx]
                unit_name.delete(0, END)
                unit_name.insert(0, unit['name'])
                unit_location.delete(0, END)
                unit_location.insert(0, unit['location'])
                
                def save_edit():
                    name = unit_name.get().strip()
                    location = unit_location.get().strip()
                    
                    if not name or not location:
                        messagebox.showerror("Błąd", "Wszystkie pola muszą być wypełnione")
                        return
                    
                    self.military_units[idx] = {
                        "name": name,
                        "location": location,
                        "coordinates": get_coordinates(location)
                    }
                    self.update_unit_list()
                    button_add.config(text="Dodaj jednostkę", command=add_unit)
                    unit_name.delete(0, END)
                    unit_location.delete(0, END)
                
                button_add.config(text="Zapisz zmiany", command=save_edit)
            except IndexError:
                messagebox.showerror("Błąd", "Wybierz jednostkę do edycji")
        
        def delete_unit():
            try:
                idx = self.units_listbox.curselection()[0]
                if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć tę jednostkę?"):
                    self.military_units.pop(idx)
                    self.update_unit_list()
            except IndexError:
                messagebox.showerror("Błąd", "Wybierz jednostkę do usunięcia")
        
        def show_unit_details():
            try:
                idx = self.units_listbox.curselection()[0]
                unit = self.military_units[idx]
                details = f"Nazwa: {unit['name']}\nLokalizacja: {unit['location']}\n"
                details += f"Współrzędne: {unit['coordinates'][0]}, {unit['coordinates'][1]}"
                messagebox.showinfo("Szczegóły jednostki", details)
            except IndexError:
                messagebox.showerror("Błąd", "Wybierz jednostkę")
        
        button_add.config(command=add_unit)
        Button(button_frame, text="Edytuj", command=edit_unit).pack(side=LEFT, padx=5)
        Button(button_frame, text="Usuń", command=delete_unit).pack(side=LEFT, padx=5)
        Button(button_frame, text="Szczegóły", command=show_unit_details).pack(side=LEFT, padx=5)
        
        self.update_unit_list()

    def show_employees(self):
        # Implementacja zarządzania pracownikami
        window = Toplevel(self.root)
        window.title("Zarządzanie Pracownikami")
        window.geometry("800x600")
        
        # Podobna implementacja jak dla jednostek wojskowych
        pass

    def show_subunits(self):
        # Implementacja zarządzania pododdziałami
        window = Toplevel(self.root)
        window.title("Zarządzanie Pododdziałami")
        window.geometry("800x600")
        
        # Podobna implementacja jak dla jednostek wojskowych
        pass

    def show_soldiers(self):
        # Implementacja zarządzania żołnierzami
        window = Toplevel(self.root)
        window.title("Zarządzanie Żołnierzami")
        window.geometry("800x600")
        
        # Podobna implementacja jak dla jednostek wojskowych
        pass

    def show_maps(self):
        # Implementacja wyświetlania map
        window = Toplevel(self.root)
        window.title("Mapy")
        window.geometry("800x600")
        
        Button(window, text="Mapa jednostek").pack(pady=5)
        Button(window, text="Mapa pracowników").pack(pady=5)
        Button(window, text="Mapa pododdziałów").pack(pady=5)
        Button(window, text="Mapa żołnierzy").pack(pady=5)

    def update_unit_list(self):
        self.units_listbox.delete(0, END)
        for unit in self.military_units:
            self.units_listbox.insert(END, f"{unit['name']} - {unit['location']}")

    def logout(self):
        self.current_user = None
        for widget in self.root.winfo_children():
            widget.destroy()
        self.show_login_screen()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MilitarySystem()
    app.run()