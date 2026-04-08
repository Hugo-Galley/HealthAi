import pandas as pd
import streamlit as st

from api_client import get_json


def load_flagged_data() -> tuple[pd.DataFrame, str | None]:
    payload = get_json("/admin/flagged-data")
    if not payload.get("success"):
        columns = ["ID", "Type", "Valeur", "Unite", "Raison du flag", "Statut", "Anomalie"]
        return pd.DataFrame(columns=columns), payload.get("error", "API flagged data indisponible")
    data = payload.get("data", [])
    if not isinstance(data, list):
        return pd.DataFrame(), "Format API /admin/flagged-data invalide"

    df = pd.DataFrame(data)
    rename_map = {
        "id": "ID",
        "type": "Type",
        "value": "Valeur",
        "unit": "Unite",
        "flag_reason": "Raison du flag",
        "status": "Statut",
        "is_anomaly": "Anomalie",
        "anomalie": "Anomalie",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
    return df, None


st.title("Administration")
st.markdown("---")
st.subheader("Donnees flaggees")

df, error = load_flagged_data()
if error:
    st.warning("Endpoint `/admin/flagged-data` non disponible dans le backend actuel.")
    st.caption(error)

if df.empty:
    st.info("Aucune donnee retournee par l'API.")
    st.stop()

col_anomalie = "Anomalie" if "Anomalie" in df.columns else "anomalie"
if col_anomalie not in df.columns:
    st.info("Colonne d'anomalie absente de la reponse API.")
    st.dataframe(df, use_container_width=True)
    st.stop()

df_anomalies = df[df[col_anomalie] == True]
if len(df_anomalies) == 0:
    st.success("Aucune donnee avec anomalie detectee.")
else:
    st.dataframe(df_anomalies, use_container_width=True)
