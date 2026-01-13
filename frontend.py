import streamlit as st
import requests

# Adresa našeho běžícího API
API_URL = "http://127.0.0.1:8000"

# --- Nastavení stránky ---
st.set_page_config(page_title="ToDo App 2026", page_icon="📝")
st.title("📝 Manažer úkolů 2026")

# --- 1. Sekce: Přidání nového úkolu ---
st.subheader("Nový úkol")
# Vytvoříme textové pole a tlačítko vedle sebe (sloupce)
col1, col2 = st.columns([3, 1])

with col1:
    new_task_title = st.text_input("Co je potřeba udělat?", label_visibility="collapsed")

with col2:
    if st.button("Přidat úkol", type="primary"):
        if new_task_title:
            # Frontend volá API: "Hej, vytvoř úkol!"
            response = requests.post(f"{API_URL}/tasks", json={"title": new_task_title})

            if response.status_code == 200:
                st.success("Přidáno!")
                st.rerun()  # Obnoví stránku, aby byl nový úkol vidět
            else:
                st.error("Chyba při komunikaci se serverem.")
        else:
            st.warning("Napřed něco napiš.")

st.divider()  # Vodorovná čára

# --- 2. Sekce: Výpis úkolů ---
st.subheader("Seznam úkolů")

# Načteme úkoly z API (GET request)
try:
    response = requests.get(f"{API_URL}/tasks")
    if response.status_code == 200:
        tasks = response.json()  # Převedeme JSON odpověď na Python list
    else:
        st.error("Nepodařilo se načíst úkoly.")
        tasks = []
except requests.exceptions.ConnectionError:
    st.error("🚨 API neběží! Nezapomněl jsi spustit uvicorn?")
    tasks = []

if not tasks:
    st.info("Žádné úkoly.")
else:
    # Už nepotřebujeme enumerate(tasks), ID máme přímo v úkolu!
    for task in tasks:
        cols = st.columns([0.1, 0.8, 0.1])

        status_icon = "✅" if task['completed'] else "⬜"
        cols[0].write(status_icon)

        if task['completed']:
            cols[1].markdown(f"~~{task['title']}~~")
        else:
            cols[1].write(task['title'])

        if not task['completed']:
            # Klíč tlačítka musí být unikátní, použijeme task['id']
            if cols[2].button("Hotovo", key=f"btn_{task['id']}"):
                # Posíláme ID úkolu, ne index!
                requests.put(f"{API_URL}/tasks/{task['id']}/complete")
                st.rerun()