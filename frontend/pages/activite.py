import requests
import pandas as pd
import plotly.express as px
import streamlit as st

API_BASE = "http://localhost:8000"


def _get(endpoint: str) -> list | dict | None:
    try:
        resp = requests.get(f"{API_BASE}{endpoint}", timeout=5)
        resp.raise_for_status()
        body = resp.json()
        if isinstance(body, dict) and not body.get("success", True):
            return None
        return body.get("data") if isinstance(body, dict) and "data" in body else body
    except requests.exceptions.ConnectionError:
        st.error(f"Impossible de joindre le backend ({API_BASE}). Vérifiez que le serveur est démarré.")
        return None
    except requests.exceptions.HTTPError as ex:
        if ex.response.status_code == 404:
            return None
        st.error(f"Erreur API `{endpoint}` : {ex}")
        return None
    except Exception as ex:
        st.error(f"Erreur lors de l'appel `{endpoint}` : {ex}")
        return None


def _df(endpoint: str) -> pd.DataFrame:
    data = _get(endpoint)
    if not data:
        return pd.DataFrame()
    return pd.DataFrame(data)


st.title("Activité physique")
st.markdown("---")

# Données disponibles via le back : calories et adhérence par niveau d'activité
df = _df("/kpi/adherenceByActivityLevel")

if not df.empty:
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
