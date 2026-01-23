import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Nutrition - HealthAI",
    page_icon="🍎",
    layout="wide"
)

st.title("🍎 Nutrition")
st.markdown("---")

# Filtres pour les données nutritionnelles
col1, col2, col3 = st.columns(3)

with col1:
    date_debut = st.date_input("Date de début", value=None)
    
with col2:
    date_fin = st.date_input("Date de fin", value=None)
    
with col3:
    # TODO: Charger la liste des utilisateurs depuis le backend
    utilisateur_filter = st.selectbox("Utilisateur", ["Tous"])  # À remplacer par la liste depuis le backend

st.markdown("---")

# Section pour les graphiques
col1, col2 = st.columns(2)



# Tableau récapitulatif
st.markdown("---")
st.subheader("Données Nutritionnelles Détaillées")
st.write("Tableau des données nutritionnelles filtrées (à connecter avec la base de données)")
