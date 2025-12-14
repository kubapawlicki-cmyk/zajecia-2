import streamlit as st
import os

# --- Konfiguracja i Zmienne ---
INVENTORY_FILE = 'inventory.txt'
SESSION_KEY = 'inventory_list'

# --- Funkcje Zarządzania Plikiem (Trwałość Danych) ---

def load_inventory_from_file():
    """Wczytuje listę towarów z pliku."""
    if not os.path.exists(INVENTORY_FILE):
        return []
    try:
        with open(INVENTORY_FILE, 'r', encoding='utf-8') as f:
            # Filtruj puste linie
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        st.error(f"Błąd podczas wczytywania pliku: {e}")
        return []

def save_inventory_to_file(inventory_list):
    """Zapisuje listę towarów do pliku."""
    try:
        with open(INVENTORY_FILE, 'w', encoding='utf-8') as f:
            for item in inventory_list:
                f.write(item + '\n')
    except Exception as e:
        st.error(f"Błąd podczas zapisywania do pliku: {e}")

# --- Inicjalizacja Stanu Magazynu (tylko raz!) ---

# Użyj st.session_state, ale załaduj go z pliku przy pierwszym uruchomieniu
if SESSION_KEY not in st.session_state:
    st.session_state[SESSION_KEY] = load_inventory_from_file()

# --- Funkcje Akcji ---

def add_item(item_name):
    """Dodaje towar do sesji i zapisuje do pliku."""
    if item_name and item_name not in st.session_state[SESSION_KEY]:
        st.session_state[SESSION_KEY].append(item_name)
        save_inventory_to_file(st.session_state[SESSION_KEY])
        st.success(f"Dodano i zapisano: **{item_name}**")
    elif item_name in st.session_state[SESSION_KEY]:
        st.warning(f"Towar '{item_name}' jest już w magazynie.")

def delete_item(index):
    """Usuwa towar z sesji i zapisuje do pliku."""
    if 0 <= index < len(st.session_state[SESSION_KEY]):
        deleted_item = st.session_state[SESSION_KEY].pop(index)
        save_inventory_to_file(st.session_state[SESSION_KEY])
        st.success(f"Usunięto i zapisano: **{deleted_item}**")

# --- Interfejs Użytkownika Streamlit ---

st.set_page_config(
    page_title="Stabilny Magazyn Streamlit",
    layout="centered"
)

st.title("📦 Stabilny 'Magazyn' Streamlit")
st.markdown("---")

# --- Sekcja Dodawania ---
st.header("➕ Dodaj nowy towar")
with st.form("add_item_form", clear_on_submit=True):
    new_item = st.text_input("Nazwa towaru:").strip()
    submitted = st.form_submit_button("Dodaj do Magazynu")
    
    if submitted:
        add_item(new_item)
        # UWAGA: W tej wersji nie potrzebujemy st.rerun() po dodaniu,
        # ponieważ Streamlit sam się odświeży po interakcji w formularzu.

st.markdown("---")

# --- Sekcja Wyświetlania i Usuwania ---
st.header("📋 Stan Magazynu")

current_inventory = st.session_state[SESSION_KEY]

if not current_inventory:
    st.info("Magazyn jest pusty.")
else:
    # Używamy iteracji po kopii listy dla bezpieczeństwa
    for index, item in enumerate(current_inventory):
        col1, col2 = st.columns([0.8, 0.2])
        col1.markdown(f"**{index + 1}.** {item}")
        
        # Przycisk usuwania z unikalnym kluczem
        if col2.button("Usuń", key=f"delete_btn_{index}", on_click=delete_item, args=(index,)):
            # Po kliknięciu przycisk wywołuje funkcję delete_item, która usuwa
            # element z sesji i pliku. Streamlit odświeży się automatycznie.
            pass
