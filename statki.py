import streamlit as st
import pandas as pd
import numpy as np
import streamlit_option_menu
from streamlit_option_menu import option_menu
import sqlite3

st.set_page_config(page_title="Statki", page_icon=":ship:", layout="wide")

# conn = sqlite3.connect('statki.db')
# c = conn.cursor()

# # Utworzenie tabeli 'rezerwacje' w bazie danych, jeśli nie istnieje
# c.execute('''CREATE TABLE IF NOT EXISTS rezerwacje
#              (statek TEXT, imie_nazwisko TEXT, nr_tel TEXT, data TEXT, godzina TEXT, rejs TEXT, ilosc_osob INTEGER, zaliczka TEXT, kwota_zaliczki REAL, katering TEXT, notatki TEXT)''')

# # Utworzenie tabeli 'dodaj_rejs' w bazie danych, jeśli nie istnieje
# c.execute('''CREATE TABLE IF NOT EXISTS dodaj_rejs
#              (statek TEXT, imie_nazwisko TEXT, nr_tel TEXT, godzina TEXT, rejs TEXT, ilosc_osob INTEGER, zaliczka TEXT, kwota_zaliczki REAL, bilet_oplacony TEXT, notatki TEXT)''')

# conn.commit()

# # Funkcja do dodawania nowej rezerwacji do bazy danych
# def dodaj_rezerwacje(statek, imie_nazwisko, nr_tel, data, godzina, rejs, ilosc_osob, zaliczka, kwota_zaliczki, katering, notatki):
#     c.execute('''INSERT INTO rezerwacje (statek, imie_nazwisko, nr_tel, data, godzina, rejs, ilosc_osob, zaliczka, kwota_zaliczki, katering, notatki)
#                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (statek, imie_nazwisko, nr_tel, data, godzina, rejs, ilosc_osob, zaliczka, kwota_zaliczki, katering, notatki))
#     conn.commit()

# # Funkcja do dodawania nowego rejsu do bazy danych
# def dodaj_rejs(statek, imie_nazwisko, nr_tel, godzina, rejs, ilosc_osob, zaliczka, kwota_zaliczki, bilet_oplacony, notatki):
#     c.execute('''INSERT INTO dodaj_rejs (statek, imie_nazwisko, nr_tel, godzina, rejs, ilosc_osob, zaliczka, kwota_zaliczki, bilet_oplacony, notatki)
#                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (statek, imie_nazwisko, nr_tel, godzina, rejs, ilosc_osob, zaliczka, kwota_zaliczki, bilet_oplacony, notatki))
#     conn.commit()

# # Funkcja do pobierania wszystkich rezerwacji z bazy danych
# def pobierz_rezerwacje():
#     c.execute("SELECT * FROM rezerwacje")
#     return c.fetchall()

# # Funkcja do pobierania wszystkich rejsów z bazy danych
# def pobierz_rejsy():
#     c.execute("SELECT * FROM dodaj_rejs")
#     return c.fetchall()

with st.sidebar:
    st.image("logo-Port-karamaranow8-2.png")
    selected = option_menu(
        menu_title = "Menu",
        options = ["Strona główna", "Rezerwacje", "Zaloguj"],
        icons = ["house", "book", "box-arrow-in-right"],
        menu_icon = "list-task",
        default_index = 0,
    )

log1 = []
log2 = ""

def logowanie():
    log1.append(log2)
    st.write(log1)


if selected == "Zaloguj":
    st.title("Zaloguj :closed_lock_with_key:")
    with st.container(border=True):
        log2 = st.text_input("Podaj login", key="login")
        pass1 = st.text_input("Podaj hasło", key="password", type="password")
        log_button = st.button("Zaloguj")
        if log_button:
            logowanie()
    st.divider()
    with st.expander("Dodaj nowego użytkownika :male-technologist:"):
        im = st.text_input("Podaj imię i nazwisko")
        lg = st.text_input("Podaj login")
        ps = st.text_input("Podaj hasło", type="password")
        ps2 = st.text_input("Powtórz hasło", type="password")
        add_but = st.button("Dodaj użytkowanika")
        if add_but:
            if (ps == ps2):
                st.info("OK", icon="ℹ️")
            else:
                st.warning("Hasła nie są identyczne", icon="⚠️")

if (selected == "Strona główna"):
    # Funkcja get_data_tab pobiera dane z sesji, lub zwraca pusty słownik, jeśli nie ma jeszcze danych w sesji
    def get_data_tab_2():
        return st.session_state.setdefault('dane_tab_2', {
            "Albatros": [],
            "Biała Mewa": [],
            "Kormoran": [],
            "CKT VIP": []
        })

    # Funkcja save_data_tab zapisuje dane do sesji
    def save_data_tab(dane_tab_2):
        st.session_state['dane_tab_2'] = dane_tab_2
    st.title("Dodaj rejs :anchor:")
    with st.expander("Dodaj nowy rejs"):
        c1_2, c2_2 = st.columns((1, 1))
        with c1_2:
            name2 = st.text_input("Podaj imię i nazwisko")
            hr2 = st.time_input("Podaj godzinę")
            stat2 = st.selectbox("Wybierz statek", ["Albatros", "Biała Mewa", "Kormoran", "CKT VIP"])
            zal2 = st.selectbox("Zaliczka", ["Tak", "Nie"])
            ob = st.selectbox("Bilet opłacony", ["Tak", "Nie"])
            
        with c2_2:
            nb2 = st.text_input("Podaj numer telefonu")
            ilos2 = st.number_input("Ilość osób", step=1, max_value=60, min_value=0)
            rejs2 = st.selectbox("Wybierz rejs: ", ["Po rzekach i jeziorach - 1h", "Fotel Papieski - 1h", "Kanał Augustowski - 1h", "Dolina Rospudy - 1,5h", "Szlakiem Papieskim - 3h", "Staw Swoboda - 4h", "Gorczyca - „Pełen Szlak Papieski” – 6h", "Paniewo"])
            if zal2 == "Tak":
                kwt2 = st.number_input("Kwotwa zaliczki")
        
        note2 = st.text_area("Notatki")
        button2 = st.button("Dodaj rejs")

        # Pobranie danych z sesji
        dane_tab_2 = get_data_tab_2()

        if button2:
            new_entry = {
                "Imię i nazwisko": name2,
                "Nr tel.": nb2,
                "Godzina": hr2.strftime("%H:%M"),
                "Rejs": rejs2,
                "Ilość pasażerów": ilos2,
                "Zaliczka": zal2,
                "Kwota zaliczki": kwt2 if zal2 == "Tak" else None,
                "Bilet opłacony": ob,
                "Notatki": note2 if note2 != "" else "Brak",
            }
            
            if stat2 in dane_tab_2:
                dane_tab_2[stat2].append(new_entry)
            else:
                dane_tab_2[stat2] = [new_entry]
                
            # Zapisanie danych do sesji
            save_data_tab(dane_tab_2)
                
            st.write("Dane dodane pomyślnie.")

    tab1_2, tab2_2, tab3_2, tab4_2 = st.tabs(["Albatros", "Biała Mewa", "Kormoran", "CKT VIP"])
    
    for stat, entries in dane_tab_2.items():
        global key2, value2
        if stat == "Albatros":
            with tab1_2:
                st.markdown(f"<h2 style='text-align: center; background-color: #333333; padding: 10px; color: white; border-radius: 5px;'>Albatros</h2>", unsafe_allow_html=True)
                st.divider()
                for entry2 in entries:
                    with st.container(border=True):
                        for key2, value2 in entry2.items():
                            if key2 == "Kwota zaliczki":
                                value2 = value2 if value2 is not None else "Brak"
                            st.write(f"{key2}: {value2}")
                    st.divider()
        elif stat == "Biała Mewa":
            with tab2_2:
                st.markdown(f"<h2 style='text-align: center; background-color: #333333; padding: 10px; color: white; border-radius: 5px;'>Biała Mewa</h2>", unsafe_allow_html=True)
                st.divider()
                for entry2 in entries:
                    with st.container(border=True):
                        for key2, value2 in entry2.items():
                            if key2 == "Kwota zaliczki":
                                value2 = value2 if value2 is not None else "Brak"
                            st.write(f"{key2}: {value2}")
                    st.divider()
        elif stat == "Kormoran":
            with tab3_2:
                st.markdown(f"<h2 style='text-align: center; background-color: #333333; padding: 10px; color: white; border-radius: 5px;'>Kormoran</h2>", unsafe_allow_html=True)
                st.divider()
                for entry2 in entries:
                    with st.container(border=True):
                        for key2, value2 in entry2.items():
                            if key2 == "Kwota zaliczki":
                                value2 = value2 if value2 is not None else "Brak"
                            st.write(f"{key2}: {value2}")
                    st.divider()
        elif stat == "CKT VIP":
            with tab4_2:
                st.markdown(f"<h2 style='text-align: center; background-color: #333333; padding: 10px; color: white; border-radius: 5px;'>CKT VIP</h2>", unsafe_allow_html=True)
                st.divider()
                for entry2 in entries:
                    with st.container(border=True):
                        for key2, value2 in entry2.items():
                            if key2 == "Kwota zaliczki":
                                value2 = value2 if value2 is not None else "Brak"
                            st.write(f"{key2}: {value2}")
                    st.divider()

if (selected == "Rezerwacje"):
    # Funkcja get_data_tab pobiera dane z sesji, lub zwraca pusty słownik, jeśli nie ma jeszcze danych w sesji
    def get_data_tab():
        return st.session_state.setdefault('dane_tab', {
            "Albatros": [],
            "Biała Mewa": [],
            "Kormoran": [],
            "CKT VIP": []
        })

    # Funkcja save_data_tab zapisuje dane do sesji
    def save_data_tab(dane_tab):
        st.session_state['dane_tab'] = dane_tab
    
    st.title("Dodaj rezerwację :anchor:")
    with st.expander("Dodaj nową rezerwację"):
        c1, c2 = st.columns((1,1))
        with c1:
            name = st.text_input("Podaj imię i nazwisko")
            date = st.date_input("Podaj dzień", value="today", format="DD.MM.YYYY", label_visibility="visible")
            stat = st.selectbox("Wybierz statek", ["Albatros", "Biała Mewa", "Kormoran", "CKT VIP"])
            zal = st.selectbox("Zaliczka", ["Tak", "Nie"])
            ilos = st.number_input("Ilość osób", step=1, max_value=60, min_value=0)
        
        with c2:
            nb = st.text_input("Podaj numer telefonu")
            hr = st.time_input("Podaj godzinę")
            rejs = st.selectbox("Wybierz rejs", ["Po rzekach i jeziorach - 1h", "Fotel Papieski - 1h", "Kanał Augustowski - 1h", "Dolina Rospudy - 1,5h", "Szlakiem Papieskim - 3h", "Staw Swoboda - 4h", "Gorczyca - „Pełen Szlak Papieski” – 6h", "Paniewo"])
            if zal == "Tak":
                kwt = st.number_input("Kwotwa zaliczki")
            kat = st.selectbox("Katering", ["Tak", "Nie"])
            
        note = st.text_area("Notatki")
        button1 = st.button("Dodaj rezerwację")

        # Pobranie danych z sesji
        dane_tab = get_data_tab()

        if button1:
            new_entry = {
                "Imię i nazwisko": name,
                "Nr tel.": nb,
                "Data": date.strftime("%d.%m.%y"),
                "Godzina": hr.strftime("%H:%M"),
                "Rejs": rejs,
                "Ilość pasażerów": ilos,
                "Zaliczka": zal,
                "Kwota zaliczki": kwt if zal == "Tak" else None,
                "Katering": kat,
                "Notatki": note if note != "" else "Brak",
            }
            
            if stat in dane_tab:
                dane_tab[stat].append(new_entry)
            else:
                dane_tab[stat] = [new_entry]
            
            # Zapisanie danych do sesji
            save_data_tab(dane_tab)

            st.write("Dane dodane pomyślnie.")

    tab1, tab2, tab3, tab4 = st.tabs(["Albatros", "Biała Mewa", "Kormoran", "CKT VIP"])

    for stat, entries in dane_tab.items():
        global key, value
        if stat == "Albatros":
            with tab1:
                st.markdown(f"<h2 style='text-align: center; background-color: #333333; padding: 10px; color: white; border-radius: 5px;'>Albatros</h2>", unsafe_allow_html=True)
                st.divider()
                for entry in entries:
                    with st.container(border=True):
                        for key, value in entry.items():
                            if key == "Kwota zaliczki":
                                value = value if value is not None else "Brak"
                            st.write(f"{key}: {value}")
                    st.divider()
        elif stat == "Biała Mewa":
            with tab2:
                st.markdown(f"<h2 style='text-align: center; background-color: #333333; padding: 10px; color: white; border-radius: 5px;'>Biała Mewa</h2>", unsafe_allow_html=True)
                st.divider()
                for entry in entries:
                    with st.container(border=True):
                        for key, value in entry.items():
                            if key == "Kwota zaliczki":
                                value = value if value is not None else "Brak"
                            st.write(f"{key}: {value}")
                    st.divider()
        elif stat == "Kormoran":
            with tab3:
                st.markdown(f"<h2 style='text-align: center; background-color: #333333; padding: 10px; color: white; border-radius: 5px;'>Kormoran</h2>", unsafe_allow_html=True)
                st.divider()
                for entry in entries:
                    with st.container(border=True):
                        for key, value in entry.items():
                            if key == "Kwota zaliczki":
                                value = value if value is not None else "Brak"
                            st.write(f"{key}: {value}")
                    st.divider()
        elif stat == "CKT VIP":
            with tab4:
                st.markdown(f"<h2 style='text-align: center; background-color: #333333; padding: 10px; color: white; border-radius: 5px;'>CKT VIP</h2>", unsafe_allow_html=True)
                st.divider()
                for entry in entries:
                    with st.container(border=True):
                        for key, value in entry.items():
                            if key == "Kwota zaliczki":
                                value = value if value is not None else "Brak"
                            st.write(f"{key}: {value}")
                    st.divider()
