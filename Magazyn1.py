import streamlit as st
import os

# Nazwa pliku do przechowywania danych
INVENTORY_FILE = 'inventory.txt'

# --- Funkcje Zarządzania Plikiem ---

def load_inventory():
    """Wczytuje listę towarów z pliku."""
    if not os.path.exists(INVENTORY_FILE):
        return []
    with open(INVENTORY_FILE, 'r', encoding='utf-8') as f:
        # Odczyt linii i usunięcie białych znaków (np. znaku nowej linii)
        return [line.strip() for line in f if line.strip()]

def save_inventory(inventory_list):
    """Zapisuje listę towarów do pliku."""
    with open(INVENTORY_FILE, 'w', encoding='utf-8') as f:
        for item in inventory_list:
            f.write(item + '\n')

# --- Logika Aplikacji Streamlit ---

st.set_page_config(
    page_title="Magazyn Bez Sesji (Plik)",
    layout="centered"
)

st.title("💾 Prosty 'Magazyn' z Zapisem do Pliku")
st.markdown("---")

# Wczytanie obecnego stanu magazynu
current_inventory = load_inventory()

# --- Dodawanie Towaru ---
st.header("➕ Dodaj nowy towar")
# Używamy formularza (st.form) do grupowania interakcji,
# co zapobiega wielokrotnemu uruchamianiu skryptu przy wprowadzaniu tekstu.
with st.form("add_item_form", clear_on_submit=True):
    new_item = st.text_input("Nazwa towaru:")
    submitted = st.form_submit_button("Dodaj do Magazynu")
    
    if submitted and new_item:
        current_inventory.append(new_item)
        save_inventory(current_inventory)
        st.success(f"Dodano i zapisano: **{new_item}**")
        st.experimental_rerun() # Ponowne uruchomienie po zmianie danych

st.markdown("---")

# --- Wyświetlanie i Usuwanie Towarów ---
st.header("📋 Stan Magazynu")

if not current_inventory:
    st.info("Magazyn jest pusty.")
else:
    # Wyświetlanie listy i przycisków usuwania
    for index, item in enumerate(current_inventory):
        col1, col2 = st.columns([0.8, 0.2])
        col1.markdown(f"**{index + 1}.** {item}")
        
        # Przycisk usuwania
        if col2.button("Usuń", key=f"delete_btn_{index}"):
            # Usuń element z listy
            del current_inventory[index]
            # Zapisz zmienioną listę do pliku
            save_inventory(current_inventory)
            st.success(f"Usunięto: **{item}**")
            st.experimental_rerun() # Ponowne uruchomienie po zmianie danych
