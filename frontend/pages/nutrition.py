import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("Nutrition")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    date_debut = st.date_input("Date de début")

with col2:
    date_fin = st.date_input("Date de fin")

with col3:
    utilisateur = st.selectbox("Utilisateur", ["Tous", "Alice", "Bob", "Charlie", "Diane"])

st.markdown("---")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Répartition des macronutriments")

    df_macros = pd.DataFrame(
        {
            "Macronutriment": ["Protéines", "Glucides", "Lipides"],
            "Valeur (g)": [110, 230, 75],
        }
    )

    fig_macros = px.pie(
        df_macros,
        names="Macronutriment",
        values="Valeur (g)",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    st.plotly_chart(fig_macros, use_container_width=True)

with col_right:
    st.subheader("Tendances nutritionnelles")

    dates = pd.date_range(start="2024-01-01", periods=30, freq="D")
    df_tendances = pd.DataFrame(
        {
            "Date": dates,
            "Calories": [1800 + i * 15 for i in range(30)],
            "Protéines": [90 + i * 1.5 for i in range(30)],
            "Glucides": [200 + i * 2 for i in range(30)],
            "Lipides": [60 + i for i in range(30)],
        }
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_tendances["Date"], y=df_tendances["Calories"], mode="lines", name="Calories"))
    fig.add_trace(go.Scatter(x=df_tendances["Date"], y=df_tendances["Protéines"], mode="lines", name="Protéines (g)"))
    fig.add_trace(go.Scatter(x=df_tendances["Date"], y=df_tendances["Glucides"], mode="lines", name="Glucides (g)"))
    fig.add_trace(go.Scatter(x=df_tendances["Date"], y=df_tendances["Lipides"], mode="lines", name="Lipides (g)"))
    fig.update_layout(xaxis_title="Date", yaxis_title="Valeur")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.subheader("Journal nutritionnel (exemple)")

df_journal = pd.DataFrame(
    [
        {"Date": "2024-01-20", "Utilisateur": "Alice", "Repas": "Déjeuner", "Calories": 650},
        {"Date": "2024-01-20", "Utilisateur": "Bob", "Repas": "Dîner", "Calories": 720},
        {"Date": "2024-01-19", "Utilisateur": "Charlie", "Repas": "Petit-déjeuner", "Calories": 420},
        {"Date": "2024-01-19", "Utilisateur": "Diane", "Repas": "Déjeuner", "Calories": 580},
    ]
)

st.dataframe(df_journal, use_container_width=True)

