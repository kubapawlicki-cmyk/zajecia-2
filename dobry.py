import streamlit as st
import os

# --- Konfiguracja i Zmienne ---
INVENTORY_FILE = 'inventory_prezenty.txt'  # Zmieniamy nazwę pliku, aby pasowała do Mikołaja
SESSION_KEY = 'inventory_list'

# --- Funkcje Zarządzania Plikiem (Trwałość Danych) ---

def load_inventory_from_file():
    """Wczytuje listę towarów/prezentów z pliku."""
    if not os.path.exists(INVENTORY_FILE):
        return []
    try:
        with open(INVENTORY_FILE, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        st.error(f"Błąd podczas wczytywania pliku: {e}")
        return []

def save_inventory_to_file(inventory_list):
    """Zapisuje listę towarów/prezentów do pliku."""
    try:
        with open(INVENTORY_FILE, 'w', encoding='utf-8') as f:
            for item in inventory_list:
                f.write(item + '\n')
    except Exception as e:
        st.error(f"Błąd podczas zapisywania do pliku: {e}")

# --- Inicjalizacja Stanu Magazynu ---
if SESSION_KEY not in st.session_state:
    st.session_state[SESSION_KEY] = load_inventory_from_file()

# --- Funkcje Akcji ---

def add_item(item_name):
    """Dodaje prezent do sesji i zapisuje do pliku."""
    if item_name and item_name not in st.session_state[SESSION_KEY]:
        st.session_state[SESSION_KEY].append(item_name)
        save_inventory_to_file(st.session_state[SESSION_KEY])
        st.success(f"Włożono do worka: **{item_name}** 🎁")
    elif item_name in st.session_state[SESSION_KEY]:
        st.warning(f"Ten prezent jest już w worku.")

def delete_item(index):
    """Usuwa prezent z sesji i zapisuje do pliku."""
    if 0 <= index < len(st.session_state[SESSION_KEY]):
        deleted_item = st.session_state[SESSION_KEY].pop(index)
        save_inventory_to_file(st.session_state[SESSION_KEY])
        st.success(f"Wyrzucono z worka: **{deleted_item}** 🗑️")

# --- Interfejs Użytkownika Streamlit ---

st.set_page_config(
    page_title="Magazyn Prezentów Mikołaja",
    layout="centered"
)

# --- Tutaj Wstawiamy Obrazek Mikołaja (lub Emotikon) ---
st.title("🎅 Magazyn Prezentów Mikołaja (Brzuch Pełen Dobra)")

# Osadzanie obrazka (możesz wstawić URL do swojego obrazka)
# UWAGA: Jeśli masz plik lokalny (np. 'mikolaj.png'), umieść go w tym samym folderze
# i użyj st.image('mikolaj.png', width=150)
st.image("https://i.imgur.com/gKq9b5L.png", width=150, caption="To jest nasz Magazyn Mikołaja!")
st.markdown("---")

# --- Sekcja Dodawania ---
st.header("🎁 Dodaj Prezent do Worka")
with st.form("add_item_form", clear_on_submit=True):
    new_item = st.text_input("Nazwa Prezentu:").strip()
    submitted = st.form_submit_button("Dodaj do Worka")
    
    if submitted:
        add_item(new_item)

st.markdown("---")

# --- Sekcja Wyświetlania i Usuwania ---
st.header("📋 Zawartość Worka Mikołaja")

current_inventory = st.session_state[SESSION_KEY]

if not current_inventory:
    st.info("Worek jest pusty. Mikołaj musi iść na zakupy! 🛍️")
else:
    for index, item in enumerate(current_inventory):
        col1, col2 = st.columns([0.8, 0.2])
        col1.markdown(f"**{index + 1}.** {item}")
        
        if col2.button("Usuń", key=f"delete_btn_{index}", on_click=delete_item, args=(index,)):
            pass
