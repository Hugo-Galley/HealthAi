import streamlit as st
from config import configuration

# Configuration de la page principale
st.set_page_config(
    page_title="HealthAI Coach",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar pour la navigation
with st.sidebar:
    st.image("https://via.placeholder.com/200x100?text=HealthAI", use_container_width=True)
    st.title("🏥 HealthAI Coach")
    st.markdown("---")
    
    st.markdown("### Navigation")
    
    # Les pages sont automatiquement détectées par Streamlit dans le dossier pages/
    # On peut aussi ajouter des liens personnalisés ici si nécessaire
    
    st.markdown("---")
    
    st.markdown("### Informations")
    st.info("""
    **Version:** 1.0.0
    
    **Statut:** En développement
    
    Naviguez entre les différentes sections via le menu ci-dessus.
    """)
    
    st.markdown("---")
    
    # TODO: Charger le nombre de données à valider depuis le backend
    # nombre_a_valider = charger_nombre_donnees_a_valider()  # Fonction à créer
    st.metric("Données à valider", "0", "⚠️")

# Contenu principal de la page d'accueil
st.title("🏥 Bienvenue sur HealthAI Coach")
st.markdown("---")

st.markdown("""
### 📋 Vue d'ensemble

Cette application vous permet de :
- **📊 Dashboard** : Visualiser les statistiques globales
- **👥 Utilisateurs** : Gérer les utilisateurs de l'application
- **🍎 Nutrition** : Analyser les données nutritionnelles avec graphiques et tendances
- **🏃 Activité** : Suivre les activités physiques
- **⚙️ Administration** : Valider les données flaggées comme potentiellement non fiables

### 🚀 Navigation

Utilisez le menu de navigation dans la barre latérale pour accéder aux différentes sections.
""")

# Métriques principales
st.markdown("### 📈 Métriques Rapides")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Utilisateurs", "0", "0")

with col2:
    st.metric("Données nutritionnelles", "0", "0")

with col3:
    st.metric("Activités", "0", "0")

with col4:
    # TODO: Charger le nombre depuis le backend
    st.metric("⚠️ À valider", "0", "0")

st.markdown("---")

# Alertes ou notifications
with st.expander("🔔 Notifications"):
    # TODO: Charger les notifications depuis le backend
    st.info("ℹ️ Les données seront chargées depuis le backend")
