import streamlit as st
import pandas as pd

st.title("Utilisateurs")
st.markdown("---")

st.subheader("Liste des utilisateurs")

df = pd.DataFrame(
    [
        {"ID": 1, "Nom": "Alice Martin", "Email": "alice@example.com", "Statut": "Actif", "Dernière activité": "2024-01-20"},
        {"ID": 2, "Nom": "Bob Dupont", "Email": "bob@example.com", "Statut": "Actif", "Dernière activité": "2024-01-19"},
        {"ID": 3, "Nom": "Charlie Durand", "Email": "charlie@example.com", "Statut": "Inactif", "Dernière activité": "2023-12-05"},
        {"ID": 4, "Nom": "Diane Leroy", "Email": "diane@example.com", "Statut": "Actif", "Dernière activité": "2024-01-18"},
    ]
)

col1, col2 = st.columns(2)

with col1:
    statut = st.selectbox("Filtrer par statut", ["Tous", "Actif", "Inactif"])

with col2:
    recherche = st.text_input("Recherche par nom ou email")

df_filtre = df.copy()

if statut != "Tous":
    df_filtre = df_filtre[df_filtre["Statut"] == statut]

if recherche:
    recherche_lower = recherche.lower()
    df_filtre = df_filtre[
        df_filtre["Nom"].str.lower().str.contains(recherche_lower)
        | df_filtre["Email"].str.lower().str.contains(recherche_lower)
    ]

st.dataframe(df_filtre, use_container_width=True)

