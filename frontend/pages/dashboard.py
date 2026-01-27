import streamlit as st
import pandas as pd

st.title("Dashboard")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Utilisateurs actifs", "128", "+5")

with col2:
    st.metric("Sessions aujourd'hui", "342", "+18")

with col3:
    st.metric("Plans nutrition", "76", "+3")

with col4:
    st.metric("Données à valider", "7", "+2")

st.markdown("### Activité récente (exemple)")

data = pd.DataFrame(
    {
        "Utilisateur": ["Alice", "Bob", "Charlie", "Diane"],
        "Dernière action": [
            "Mise à jour profil",
            "Nouveau plan nutrition",
            "Ajout d'activité",
            "Validation de données",
        ],
        "Date": ["2024-01-20", "2024-01-20", "2024-01-19", "2024-01-19"],
    }
)

st.table(data)

