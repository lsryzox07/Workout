
import streamlit as st
import pandas as pd

# Chargement de la base d'exercices
df_exos = pd.read_csv("base_exercices_musculation.csv")
all_exercises = df_exos["Exercice"].tolist()

# Initialisation de l'état de session
if "seances" not in st.session_state:
    st.session_state["seances"] = {j: [] for j in ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]}

# Configuration de la page
st.set_page_config(page_title="Mon Coach - Gymverse Style", layout="centered")
st.title("💪 Mon Coach - Planificateur d'entraînement")

st.markdown(
    "Bienvenue dans votre assistant personnel d'entraînement !  
"
    "Ajoutez vos exercices, configurez vos séances et exportez votre programme hebdomadaire."
)

# Sélection du jour
jour = st.selectbox("📅 Sélectionne un jour d'entraînement :", list(st.session_state["seances"].keys()))

# Recherche d'exercices
search = st.text_input("🔍 Rechercher un exercice").lower()
filtered_exos = [exo for exo in all_exercises if search in exo.lower()] if search else all_exercises

# Sélection d'un exercice
if filtered_exos:
    selected_exo = st.selectbox("🏋️ Choisis un exercice :", filtered_exos)
    exo_info = df_exos[df_exos["Exercice"] == selected_exo].iloc[0]

    st.markdown(f"**Groupe musculaire :** {exo_info['Groupe']}  
**Équipement :** {exo_info['Équipement']}  
**Type :** {exo_info['Type']}")

    col1, col2, col3 = st.columns(3)
    with col1:
        series = st.number_input("Séries", min_value=1, max_value=10, value=3)
    with col2:
        reps = st.number_input("Répétitions", min_value=1, max_value=30, value=10)
    with col3:
        charge = st.text_input("Charge (kg ou poids du corps)", "Poids du corps")

    if st.button("➕ Ajouter à la séance"):
        st.session_state["seances"][jour].append({
            "Groupe": exo_info["Groupe"],
            "Exercice": selected_exo,
            "Séries": series,
            "Répétitions": reps,
            "Charge": charge
        })
        st.success(f"✅ {selected_exo} ajouté à la séance du {jour} !")
else:
    st.info("Aucun exercice trouvé.")

# Affichage de la séance du jour
st.subheader(f"📋 Séance du {jour}")
df_jour = pd.DataFrame(st.session_state["seances"][jour])
if not df_jour.empty:
    st.table(df_jour)
else:
    st.warning("Aucun exercice pour ce jour.")

# Export global
if st.button("💾 Exporter le programme hebdomadaire (.xlsx)"):
    all_data = []
    for j, liste in st.session_state["seances"].items():
        for e in liste:
            all_data.append({"Jour": j, **e})
    pd.DataFrame(all_data).to_excel("programme_hebdo.xlsx", index=False)
    st.success("📁 programme_hebdo.xlsx généré avec succès.")
