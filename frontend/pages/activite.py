import pandas as pd
import plotly.express as px
import streamlit as st

from api_client import get_json


def load_kpi(path: str) -> tuple[pd.DataFrame, str | None]:
    payload = get_json(path)
    if not payload.get("success"):
        return pd.DataFrame(), payload.get("error", f"API error on {path}")
    data = payload.get("data")
    if isinstance(data, list):
        return pd.DataFrame(data), None
    if isinstance(data, dict):
        return pd.DataFrame([data]), None
    return pd.DataFrame(), f"Unexpected payload for {path}"


st.title("Activité physique")
st.markdown("---")

df, err = load_kpi("/kpi/adherenceByActivityLevel")

if err:
    st.warning(f"Impossible de charger les données d'activité : {err}")
elif not df.empty:
    df.columns = ["Niveau d'activité", "Adhérence (%)", "Calories moy. (kcal)", "Nb patients"]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Niveaux d'activité", len(df))
    with col2:
        st.metric("Calories moyennes globales", f"{df['Calories moy. (kcal)'].mean():.0f} kcal")
    with col3:
        st.metric("Adhérence moyenne globale", f"{df['Adhérence (%)'].mean():.1f} %")

    st.markdown("---")

    col_a, col_b = st.columns(2)

    with col_a:
        fig = px.bar(
            df.sort_values("Calories moy. (kcal)", ascending=False),
            x="Niveau d'activité",
            y="Calories moy. (kcal)",
            color="Niveau d'activité",
            title="Apport calorique moyen par niveau d'activité physique",
            text_auto=".0f",
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        fig = px.bar(
            df.sort_values("Adhérence (%)", ascending=False),
            x="Niveau d'activité",
            y="Adhérence (%)",
            color="Niveau d'activité",
            title="Adhérence moyenne au régime par niveau d'activité",
            text_auto=".1f",
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Tableau détaillé")
    st.dataframe(df, use_container_width=True)

else:
    st.info("Aucune donnée d'activité disponible — endpoint non exposé par le backend.")
