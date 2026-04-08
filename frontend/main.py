import streamlit as st

from api_client import get_json
from config import configuration


def flagged_count() -> str:
    payload = get_json("/admin/flagged-data")
    if not payload.get("success"):
        return "N/A"
    data = payload.get("data", [])
    if not isinstance(data, list):
        return "N/A"
    return str(len(data))


st.set_page_config(
    page_title="HealthAI Coach",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:
    st.title("HealthAI Coach")
    st.markdown("---")
    st.metric("Donnees a valider", flagged_count())

st.title("Accueil")
st.markdown("---")

st.markdown(
    """
Application de coaching HealthAI avec :
- des visualisations & analyses par catégorie (profil épidémiologique, comportement alimentaire, indicateurs de santé, composition nutritionnelle),
- une gestion des utilisateurs,
- une analyse nutritionnelle,
- un suivi de l'activite,
- un module d'administration des donnees flaggees.
"""
)
