import streamlit as st

st.set_page_config(
    page_title="Dashboard - HealthAI",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard")
st.markdown("---")

# Placeholder pour le contenu du dashboard
st.info("Dashboard en cours de développement")

# TODO: Charger les métriques depuis le backend
# Exemple:
# nb_utilisateurs = charger_nombre_utilisateurs()
# nb_nutrition = charger_nombre_donnees_nutrition()
# nb_activites = charger_nombre_activites()
# nb_a_valider = charger_nombre_donnees_a_valider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Utilisateurs actifs", "0", "0")

with col2:
    st.metric("Données nutritionnelles", "0", "0")

with col3:
    st.metric("Activités enregistrées", "0", "0")

with col4:
    st.metric("Données à valider", "0", "0")
