import streamlit as st
import pandas as pd

st.title("Activite")
st.markdown("---")

col1 = st.columns(1)[0]

with col1:
    type_activite = st.selectbox("Type d'activite", ["Toutes", "Course", "Marche", "Velo", "Natation"])

st.markdown("---")

df_activites = pd.DataFrame(
    [
        {"Utilisateur": "Alice", "Type": "Course", "Duree (min)": 45, "Distance (km)": 8.2},
        {"Utilisateur": "Bob", "Type": "Marche", "Duree (min)": 30, "Distance (km)": 3.1},
        {"Utilisateur": "Charlie", "Type": "Velo", "Duree (min)": 60, "Distance (km)": 22.4},
        {"Utilisateur": "Diane", "Type": "Course", "Duree (min)": 35, "Distance (km)": 6.5},
    ]
)

df_filtre = df_activites.copy()

if type_activite != "Toutes":
    df_filtre = df_filtre[df_filtre["Type"] == type_activite]

st.subheader("Activites enregistrees")
st.dataframe(df_filtre, use_container_width=True)

