import requests
import pandas as pd
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
            st.info("Endpoint non disponible — en attente du backend.")
        else:
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


st.title("Utilisateurs")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    recherche = st.text_input("Recherche par pathologie")
with col2:
    genre = st.selectbox("Filtrer par genre", ["Tous", "Male", "Female"])

st.markdown("---")

df = _df("/kpi/diseases_by_gender")

if not df.empty:
    df.columns = ["Genre", "Pathologie", "Nombre de patients"]

    if genre != "Tous":
        df = df[df["Genre"] == genre]

    if recherche:
        df = df[df["Pathologie"].str.lower().str.contains(recherche.lower())]

    st.subheader("Répartition des patients par genre et pathologie")
    st.dataframe(df, use_container_width=True)

    # Résumé global
    st.markdown("---")
    st.subheader("Données agrégées des patients")

    col_a, col_b = st.columns(2)

    with col_a:
        df_diseases = _df("/kpi/diseases_repartition")
        if not df_diseases.empty:
            df_diseases.columns = ["Pathologie", "Nombre de patients"]
            st.dataframe(df_diseases, use_container_width=True)

    with col_b:
        df_allerg = _df("/kpi/allergic_reparition")
        if not df_allerg.empty:
            df_allerg.columns = ["Allergie", "Nombre de patients"]
            st.dataframe(df_allerg, use_container_width=True)
