import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

PLIK_BAZY = "karnety.json"
MAX_PIECZATEK = 10

def wczytaj_karnety():
    if os.path.exists(PLIK_BAZY):
        with open(PLIK_BAZY, "r", encoding='utf-8') as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def zapisz_karnety(karnety):
    with open(PLIK_BAZY, "w", encoding='utf-8') as f:
        json.dump(karnety, f, ensure_ascii=False, indent=4)

class AplikacjaKarnetowa:
    def __init__(self, root):
        self.root = root
        self.root.title("Karnety Senso Senso")
        self.root.configure(bg="white")

        self.karnety = wczytaj_karnety()
        self.aktualny_karnet = None
        self.stemple = []

        # Górna sekcja
        self.et_num = tk.Entry(root, font=("Arial", 14))
        self.et_num.grid(row=0, column=0, padx=10, pady=10)
        self.et_num.bind("<Return>", lambda e: self.wczytaj_karnet())

        tk.Button(root, text="Wczytaj karnet", command=self.wczytaj_karnet).grid(row=0, column=1, padx=5)
        tk.Button(root, text="Dodaj nowy karnet", command=self.dodaj_karnet_popup).grid(row=0, column=2, padx=5)
        tk.Button(root, text="Pokaż listę karnetów", command=self.pokaz_liste_karnetow).grid(row=0, column=3, padx=5)

        # Tytuł
        self.tytul = tk.Label(root, text="Przestrzeń rozwoju dziecka,\nciebie i rodziny",
                              font=("Helvetica", 16, "bold"), bg="white")
        self.tytul.grid(row=1, column=0, columnspan=4, pady=10)

        # Dane użytkownika
        self.info_label = tk.Label(root, text="", font=("Arial", 14), bg="white")
        self.info_label.grid(row=2, column=0, columnspan=4)

        # Canvas z pieczątkami
        self.canvas = tk.Canvas(root, width=600, height=200, bg="white", highlightthickness=0)
        self.canvas.grid(row=3, column=0, columnspan=4)

        self.pozycje = self.oblicz_pozycje_stempli()
        for x, y in self.pozycje:
            s = self.canvas.create_oval(x, y, x + 50, y + 50, outline="black", fill="white")
            self.stemple.append(s)

        # Przycisk pieczątki
        self.btn = tk.Button(root, text="Przybij pieczątkę", command=self.przybij_pieczatke)
        self.btn.grid(row=4, column=0, columnspan=4, pady=10)

        # Termin ważności
        self.waznosc_label = tk.Label(root, text="", font=("Arial", 12), bg="white")
        self.waznosc_label.grid(row=5, column=0, columnspan=4, pady=(0, 20))

    def oblicz_pozycje_stempli(self):
        pozycje = []
        start_x = 50
        start_y = 30
        odstep_x = 100
        odstep_y = 80
        for wiersz in range(2):
            for kolumna in range(5):
                x = start_x + kolumna * odstep_x
                y = start_y + wiersz * odstep_y
                pozycje.append((x, y))
        return pozycje

    def wczytaj_karnet(self):
        numer = self.et_num.get().strip()
        if numer in self.karnety:
            self.aktualny_karnet = self.karnety[numer]
            self.aktualny_karnet['numer'] = numer
            self.et_num.delete(0, tk.END)
            self.odswiez_widok()
        else:
            self.info_label.config(text="Nie znaleziono karnetu.")
            self.waznosc_label.config(text="")
            self.resetuj_stemple()

    def odswiez_widok(self):
        dane = self.aktualny_karnet
        self.info_label.config(
            text=f"Karnet: {dane['numer']} - {dane['imie']} {dane['nazwisko']}",
        )
        self.waznosc_label.config(text=f"Termin ważności karnetu: {dane['wazny_do']}")
        for i in range(MAX_PIECZATEK):
            kolor = "#ff69b4" if i < dane['ilosc_pieczatek'] else "white"
            self.canvas.itemconfig(self.stemple[i], fill=kolor)

    def przybij_pieczatke(self):
        if not self.aktualny_karnet:
            return
        if self.aktualny_karnet['ilosc_pieczatek'] < MAX_PIECZATEK:
            self.aktualny_karnet['ilosc_pieczatek'] += 1
            self.karnety[self.aktualny_karnet['numer']] = self.aktualny_karnet
            zapisz_karnety(self.karnety)
            self.odswiez_widok()

    def resetuj_stemple(self):
        for s in self.stemple:
            self.canvas.itemconfig(s, fill="white")

    def dodaj_karnet_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Dodaj nowy karnet")
        popup.geometry("300x320")
        popup.configure(bg="white")

        tk.Label(popup, text="Numer karnetu:", bg="white").pack(pady=5)
        et_numer = tk.Entry(popup)
        et_numer.pack()

        tk.Label(popup, text="Imię:", bg="white").pack(pady=5)
        et_imie = tk.Entry(popup)
        et_imie.pack()

        tk.Label(popup, text="Nazwisko:", bg="white").pack(pady=5)
        et_nazwisko = tk.Entry(popup)
        et_nazwisko.pack()

        tk.Label(popup, text="Ważny do (rrrr-mm-dd):", bg="white").pack(pady=5)
        et_waznosc = tk.Entry(popup)
        et_waznosc.pack()

        def zapisz_nowy():
            numer = et_numer.get().strip()
            imie = et_imie.get().strip()
            nazwisko = et_nazwisko.get().strip()
            waznosc = et_waznosc.get().strip()

            if not (numer and imie and nazwisko and waznosc):
                messagebox.showerror("Błąd", "Wszystkie pola są wymagane.")
                return

            if numer in self.karnety:
                messagebox.showerror("Błąd", "Karnet o tym numerze już istnieje.")
                return

            try:
                datetime.strptime(waznosc, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Błąd", "Zły format daty.")
                return

            self.karnety[numer] = {
                "imie": imie,
                "nazwisko": nazwisko,
                "wazny_do": waznosc,
                "ilosc_pieczatek": 0
            }
            zapisz_karnety(self.karnety)
            popup.destroy()

        tk.Button(popup, text="Zapisz", command=zapisz_nowy).pack(pady=10)

    def pokaz_liste_karnetow(self):
        okno = tk.Toplevel(self.root)
        okno.title("Lista karnetów")
        okno.geometry("600x450")
        okno.configure(bg="white")

        kolumny = ("numer", "imie_nazwisko", "pieczatki", "waznosc")
        tabela = ttk.Treeview(okno, columns=kolumny, show="headings", selectmode="browse")
        tabela.heading("numer", text="Numer karnetu")
        tabela.heading("imie_nazwisko", text="Imię i nazwisko")
        tabela.heading("pieczatki", text="Zużyte pieczątki")
        tabela.heading("waznosc", text="Ważny do")

        tabela.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for numer, dane in self.karnety.items():
            tabela.insert(
                "", "end",
                iid=numer,
                values=(
                    numer,
                    f"{dane['imie']} {dane['nazwisko']}",
                    dane['ilosc_pieczatek'],
                    dane['wazny_do']
                )
            )

        def usun_zaznaczony():
            zaznaczony = tabela.focus()
            if not zaznaczony:
                messagebox.showwarning("Uwaga", "Nie zaznaczono żadnego karnetu.")
                return
            potwierdzenie = messagebox.askyesno("Potwierdź", "Czy na pewno chcesz usunąć ten karnet?")
            if potwierdzenie:
                tabela.delete(zaznaczony)
                if zaznaczony in self.karnety:
                    del self.karnety[zaznaczony]
                    zapisz_karnety(self.karnety)

        tk.Button(okno, text="Usuń zaznaczony karnet", command=usun_zaznaczony).pack(pady=10)

# Uruchomienie aplikacji
root = tk.Tk()
app = AplikacjaKarnetowa(root)
root.mainloop()
