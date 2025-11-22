
import streamlit as st
import pandas as pd

try:
    from streamlit_extras.badges import badge
    from streamlit_extras.metric_cards import style_metric_cards
except ImportError:
    st.warning("Installez streamlit-extras avec : pip install streamlit-extras")

# Chargement des exercices
df_exos = pd.read_csv("base_exercices_musculation.csv")
all_exercises = df_exos["Exercice"].tolist()

if "seances" not in st.session_state:
    st.session_state["seances"] = {
        j: [] for j in ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    }

st.set_page_config(page_title="Gymverse Pro", layout="centered")
st.title("🏋️ Gymverse Coach")
st.caption("Crée ta semaine d'entraînement avec style")

# Style du haut
colA, colB = st.columns([2, 1])
with colA:
    st.subheader("Planifie ta séance journalière")
with colB:
    badge(type="github", name="Voir le dépôt", url="https://github.com", label="Projet")

# Sélection du jour
jour = st.selectbox("📆 Choisis ton jour :", list(st.session_state["seances"].keys()))

# Barre de recherche
search = st.text_input("🔍 Recherche un exercice").lower()
filtered = [e for e in all_exercises if search in e.lower()] if search else all_exercises

if filtered:
    selected = st.selectbox("🏋️ Exercice :", filtered)
    info = df_exos[df_exos["Exercice"] == selected].iloc[0]

    st.info(f"Groupe : {info['Groupe']} | Équipement : {info['Équipement']} | Type : {info['Type']}")

    col1, col2, col3 = st.columns(3)
    with col1:
        series = st.number_input("Séries", 1, 10, 3)
    with col2:
        reps = st.number_input("Répétitions", 1, 30, 10)
    with col3:
        charge = st.text_input("Charge", "Poids du corps")

    if st.button("➕ Ajouter"):
        st.session_state["seances"][jour].append({
            "Groupe": info["Groupe"],
            "Exercice": selected,
            "Séries": series,
            "Répétitions": reps,
            "Charge": charge
        })
        st.success(f"{selected} ajouté au {jour}")
else:
    st.warning("Aucun exercice trouvé.")

# Affichage dynamique
st.subheader(f"🗓️ Séance du {jour}")
df_jour = pd.DataFrame(st.session_state["seances"][jour])
if not df_jour.empty:
    st.data_editor(df_jour, num_rows="dynamic")
else:
    st.write("Aucun exercice pour ce jour.")

# Export Excel
if st.button("💾 Export hebdo (.xlsx)"):
    all_data = []
    for j, exos in st.session_state["seances"].items():
        for e in exos:
            all_data.append({"Jour": j, **e})
    pd.DataFrame(all_data).to_excel("programme_hebdo.xlsx", index=False)
    st.success("Fichier programme_hebdo.xlsx exporté !")
