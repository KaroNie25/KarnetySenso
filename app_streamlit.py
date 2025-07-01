import streamlit as st
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

def pokaz_pieczatki(ilosc):
    kolumny = st.columns(5)
    for i in range(MAX_PIECZATEK):
        kolumna = kolumny[i % 5]
        with kolumna:
            kolor = "#ff69b4" if i < ilosc else "#ffffff"
            st.markdown(
                f"<div style='width:50px;height:50px;border-radius:25px;border:2px solid black;background-color:{kolor};margin:10px auto;'></div>",
                unsafe_allow_html=True
            )

def dodaj_karnet(karnety):
    with st.form("nowy_karnet"):
        st.subheader("➕ Dodaj nowy karnet")
        numer = st.text_input("Numer karnetu")
        imie = st.text_input("Imię")
        nazwisko = st.text_input("Nazwisko")
        wazny_do = st.date_input("Ważny do", format="YYYY-MM-DD")

        submitted = st.form_submit_button("Zapisz")
        if submitted:
            if numer in karnety:
                st.error("❌ Karnet o tym numerze już istnieje.")
            else:
                karnety[numer] = {
                    "imie": imie,
                    "nazwisko": nazwisko,
                    "wazny_do": str(wazny_do),
                    "ilosc_pieczatek": 0
                }
                zapisz_karnety(karnety)
                st.success("✅ Dodano nowy karnet!")
                st.rerun()

def main():
    st.set_page_config(page_title="Karnety Senso Senso", layout="centered")
    st.title("🎟 Karnety Senso Senso")

    karnety = wczytaj_karnety()

    st.header("🔍 Wczytaj karnet")
    numer = st.text_input("Podaj numer karnetu")

    if numer and numer in karnety:
        dane = karnety[numer]
        st.write(f"**{dane['imie']} {dane['nazwisko']}**")
        st.write(f"📅 Ważny do: {dane['wazny_do']}")
        pokaz_pieczatki(dane["ilosc_pieczatek"])

        if dane["ilosc_pieczatek"] < MAX_PIECZATEK:
            if st.button("Przybij pieczątkę"):
                dane["ilosc_pieczatek"] += 1
                zapisz_karnety(karnety)
                st.rerun()
        else:
            st.info("ℹ️ Karnet jest już pełny.")

    elif numer:
        st.error("❌ Nie znaleziono karnetu.")

    st.divider()
    dodaj_karnet(karnety)

    st.divider()
    with st.expander("📋 Pokaż listę karnetów i zarządzaj nimi", expanded=True):
        if karnety:
            st.write("### Lista wszystkich karnetów")
            tabela = []
            for num, dane in karnety.items():
                tabela.append({
                    "Numer": num,
                    "Imię i nazwisko": f"{dane['imie']} {dane['nazwisko']}",
                    "Pieczątki": dane["ilosc_pieczatek"],
                    "Ważny do": dane["wazny_do"]
                })
            st.dataframe(tabela, use_container_width=True)

            st.write("### 🗑 Usuń karnet")
            do_usuniecia = st.selectbox("Wybierz numer karnetu do usunięcia:", options=list(karnety.keys()), key="usun_select")
            if st.button("Usuń wybrany karnet", key="usun_btn"):
                if do_usuniecia in karnety:
                    del karnety[do_usuniecia]
                    zapisz_karnety(karnety)
                    st.success(f"Karnet {do_usuniecia} został usunięty.")
                    st.rerun()
        else:
            st.info("Brak karnetów w bazie.")

if __name__ == "__main__":
    main()
