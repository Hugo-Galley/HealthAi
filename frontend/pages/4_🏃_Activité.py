import streamlit as st

st.set_page_config(
    page_title="Activité - HealthAI",
    page_icon="🏃",
    layout="wide"
)

st.title("🏃 Activité")
st.markdown("---")

# Placeholder pour le contenu de la gestion des activités
st.info("Page Activité en cours de développement")

# Filtres pour les activités
col1, col2, col3 = st.columns(3)

with col1:
    # TODO: Charger la liste des types d'activité depuis le backend
    type_activite = st.selectbox("Type d'activité", ["Toutes"])  # À remplacer par la liste depuis le backend
    
with col2:
    date_debut = st.date_input("Date de début", value=None)
    
with col3:
    date_fin = st.date_input("Date de fin", value=None)

st.markdown("---")
st.subheader("Données d'Activité")
st.write("Contenu à venir : graphiques et statistiques des activités physiques")
