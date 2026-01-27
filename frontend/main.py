import streamlit as st
from config import configuration

st.set_page_config(
    page_title="HealthAI Coach",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:
    st.title("HealthAI Coach")
    st.markdown("---")
    st.metric("Données à valider", "7", "+2")

st.title("Accueil")
st.markdown("---")

st.markdown(
    """
Application de coaching HealthAI avec :
- un dashboard de synthèse,
- une gestion des utilisateurs,
- une analyse nutritionnelle,
- un suivi de l'activité,
- un module d'administration des données flaggées.
"""
)
