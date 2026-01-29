import streamlit as st
import pandas as pd

st.title("Activité")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    type_activite = st.selectbox("Type d'activité", ["Toutes", "Course", "Marche", "Vélo", "Natation"])

with col2:
    date_debut = st.date_input("Date de début")

with col3:
    date_fin = st.date_input("Date de fin")

st.markdown("---")

df_activites = pd.DataFrame(
    [
        {"Date": "2024-01-20", "Utilisateur": "Alice", "Type": "Course", "Durée (min)": 45, "Distance (km)": 8.2},
        {"Date": "2024-01-20", "Utilisateur": "Bob", "Type": "Marche", "Durée (min)": 30, "Distance (km)": 3.1},
        {"Date": "2024-01-19", "Utilisateur": "Charlie", "Type": "Vélo", "Durée (min)": 60, "Distance (km)": 22.4},
        {"Date": "2024-01-19", "Utilisateur": "Diane", "Type": "Course", "Durée (min)": 35, "Distance (km)": 6.5},
    ]
)

df_filtre = df_activites.copy()

if type_activite != "Toutes":
    df_filtre = df_filtre[df_filtre["Type"] == type_activite]

st.subheader("Activités enregistrées")
st.dataframe(df_filtre, use_container_width=True)

