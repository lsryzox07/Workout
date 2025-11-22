import streamlit as st
import pandas as pd
from io import BytesIO

# Config page
st.set_page_config(
    page_title="Gymverse Mobile Coach",
    page_icon="💪",
    layout="centered"  # Mobile-first
)

# Load data
df_exos = pd.read_csv("base_exercices_musculation.csv")
all_exercises = df_exos["Exercice"].unique().tolist()

# Init session state
if "seances" not in st.session_state:
    st.session_state["seances"] = {j: [] for j in ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]}

# CSS for Notion-style + mobile
st.markdown("""
    <style>
        html, body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #fafafa;
        }
        .block-container {
            padding: 1rem;
        }
        .stRadio > div {
            flex-direction: row !important;
            overflow-x: auto;
            white-space: nowrap;
        }
        .stRadio label {
            padding: 0.2rem 0.8rem;
        }
        .stButton button, .stDownloadButton button {
            width: 100%;
            padding: 0.75rem;
            border-radius: 8px;
            font-weight: 600;
        }
        .stButton button {
            background-color: #4F46E5 !important;
            color: white;
        }
        .stDownloadButton button {
            background-color: #10B981 !important;
            color: white;
        }
        h1, h2, h3 {
            color: #111;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("## 💪 Gymverse Mobile Coach")
st.caption("Optimisé pour ton smartphone • Séances simples et rapides à construire")

# Choose Day
jour = st.radio("📅 Jour :", list(st.session_state["seances"].keys()), horizontal=True, label_visibility="collapsed")

# Display workout
st.markdown(f"### 📋 Séance de {jour}")
df_jour = pd.DataFrame(st.session_state["seances"][jour])
if not df_jour.empty:
    st.dataframe(df_jour, use_container_width=True)
else:
    st.info("Aucun exercice ajouté.")

st.markdown("---")

# Add exercise
st.markdown("### ➕ Ajouter un exercice")

search = st.text_input("🔍 Recherche (nom ou groupe)").strip().lower()
filtered = df_exos[
    df_exos["Exercice"].str.lower().str.contains(search) |
    df_exos["Groupe"].str.lower().str.contains(search)
] if search else df_exos

if not filtered.empty:
    selected = st.selectbox("🏋️ Choisis :", filtered["Exercice"].unique())
    info = filtered[filtered["Exercice"] == selected].iloc[0]

    with st.expander("ℹ️ Détails", expanded=False):
        st.markdown(f"- **Groupe :** {info['Groupe']}")
        st.markdown(f"- **Équipement :** {info['Équipement']}")
        st.markdown(f"- **Type :** {info['Type']}")

    col1, col2 = st.columns(2)
    with col1:
        series = st.number_input("Séries", 1, 10, 3)
    with col2:
        reps = st.number_input("Répétitions", 1, 30, 10)

    charge = st.text_input("Charge", "Poids du corps")

    if st.button("Ajouter à la séance"):
        st.session_state["seances"][jour].append({
            "Groupe": info["Groupe"],
            "Exercice": selected,
            "Séries": series,
            "Répétitions": reps,
            "Charge": charge
        })
        st.success(f"{selected} ajouté à {jour} ✅")
else:
    st.warning("Aucun exercice trouvé.")

st.markdown("---")

# Export Excel
st.markdown("### 📤 Export Excel")

if st.button("📁 Générer"):
    all_data = []
    for j, exos in st.session_state["seances"].items():
        for e in exos:
            all_data.append({"Jour": j, **e})
    if all_data:
        df_export = pd.DataFrame(all_data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df_export.to_excel(writer, index=False, sheet_name="Programme")
        st.download_button("📥 Télécharger", data=output.getvalue(),
                           file_name="programme_hebdo.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.warning("Rien à exporter.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #aaa;'>© 2025 Gymverse Mobile</p>", unsafe_allow_html=True)
