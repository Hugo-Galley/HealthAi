import requests
import pandas as pd
import plotly.express as px
import streamlit as st

API_BASE = "http://localhost:8000"


def _get(endpoint: str) -> list | None:
    try:
        resp = requests.get(f"{API_BASE}{endpoint}", timeout=5)
        resp.raise_for_status()
        body = resp.json()
        if isinstance(body, dict) and not body.get("success", True):
            st.error(f"Erreur API `{endpoint}` : {body.get('error')}")
            return None
        return body.get("data") if isinstance(body, dict) and "data" in body else body
    except requests.exceptions.ConnectionError:
        st.error(f"Impossible de joindre le backend ({API_BASE}). Vérifiez que le serveur est démarré.")
        return None
    except Exception as ex:
        st.error(f"Erreur lors de l'appel `{endpoint}` : {ex}")
        return None


def _df(endpoint: str) -> pd.DataFrame:
    data = _get(endpoint)
    if not data:
        return pd.DataFrame()
    return pd.DataFrame(data)


st.title("Nutrition")
st.markdown("---")

col1, col2, col3 = st.columns(3)

# Macros moyens par repas
df_meals = _df("/kpi/avgKcalByMeal")
if not df_meals.empty:
    df_meals.columns = ["Type de repas", "Calories moy. (kcal)", "Protéines moy. (g)", "Lipides moy. (g)", "Fibres moy. (g)"]
    with col1:
        st.metric("Calories moyennes", f"{df_meals['Calories moy. (kcal)'].mean():.1f} kcal")
    with col2:
        st.metric("Protéines moyennes", f"{df_meals['Protéines moy. (g)'].mean():.1f} g")
    with col3:
        st.metric("Lipides moyens", f"{df_meals['Lipides moy. (g)'].mean():.1f} g")

st.markdown("---")

left, right = st.columns(2)

with left:
    st.subheader("Répartition des aliments par catégorie")
    df_cat = _df("/kpi/nbrFoodsItemByCategory")
    if not df_cat.empty:
        df_cat.columns = ["Catégorie", "Nombre d'aliments"]
        fig = px.bar(
            df_cat.sort_values("Nombre d'aliments", ascending=False),
            x="Catégorie",
            y="Nombre d'aliments",
            color="Catégorie",
        )
        st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Top aliments riches en fibres")
    df_fiber = _df("/kpi/topFiberFoods")
    if not df_fiber.empty:
        df_fiber.columns = ["Aliment", "Catégorie", "Fibres (g)", "Calories (kcal)"]
        st.dataframe(
            df_fiber.sort_values("Fibres (g)", ascending=False)[["Aliment", "Catégorie", "Fibres (g)"]],
            use_container_width=True,
        )

st.markdown("---")
st.subheader("Aliments à faible sodium")
df_sodium = _df("/kpi/lowSodiumFoods")
if not df_sodium.empty:
    df_sodium.columns = ["Aliment", "Catégorie", "Sodium (mg)", "Calories (kcal)", "Protéines (g)"]
    st.dataframe(
        df_sodium.sort_values("Sodium (mg)")[["Aliment", "Catégorie", "Sodium (mg)"]],
        use_container_width=True,
    )
