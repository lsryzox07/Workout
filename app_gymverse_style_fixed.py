
import streamlit as st
import pandas as pd

# Chargement de la base d'exercices
df_exos = pd.read_csv("base_exercices_musculation.csv")
all_exercises = df_exos["Exercice"].tolist()

# Initialisation de la session
if "seances" not in st.session_state:
    st.session_state["seances"] = {
        j: [] for j in ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    }

# Config de la page
st.set_page_config(page_title="Gymverse Coach", layout="centered")
st.title("💪 Mon Coach - Gymverse Style")
st.write("Bienvenue dans votre assistant personnel d'entraînement !")
st.write("Ajoutez vos exercices, configurez vos séances et exportez votre programme hebdomadaire.")

# Choix du jour
jour = st.selectbox("📅 Choisis un jour :", list(st.session_state["seances"].keys()))

# Recherche
search = st.text_input("🔍 Rechercher un exercice").lower()
filtered = [e for e in all_exercises if search in e.lower()] if search else all_exercises

if filtered:
    selected = st.selectbox("🏋️ Sélectionne un exercice :", filtered)
    info = df_exos[df_exos["Exercice"] == selected].iloc[0]

    st.markdown("**Groupe musculaire :** " + info["Groupe"])
    st.markdown("**Équipement :** " + info["Équipement"])
    st.markdown("**Type :** " + info["Type"])

    col1, col2, col3 = st.columns(3)
    with col1:
        series = st.number_input("Séries", 1, 10, 3)
    with col2:
        reps = st.number_input("Répétitions", 1, 30, 10)
    with col3:
        charge = st.text_input("Charge", "Poids du corps")

    if st.button("Ajouter à la séance"):
        st.session_state["seances"][jour].append({
            "Groupe": info["Groupe"],
            "Exercice": selected,
            "Séries": series,
            "Répétitions": reps,
            "Charge": charge
        })
        st.success(selected + " ajouté au " + jour)
else:
    st.info("Aucun exercice trouvé.")

# Affichage
st.subheader("📋 Séance du " + jour)
df_jour = pd.DataFrame(st.session_state["seances"][jour])
if not df_jour.empty:
    st.table(df_jour)
else:
    st.warning("Aucun exercice ajouté.")

# Export Excel
if st.button("📁 Exporter programme complet (.xlsx)"):
    all_data = []
    for j, exos in st.session_state["seances"].items():
        for e in exos:
            row = {"Jour": j}
            row.update(e)
            all_data.append(row)
    pd.DataFrame(all_data).to_excel("programme_hebdo.xlsx", index=False)
    st.success("Exporté dans programme_hebdo.xlsx")
