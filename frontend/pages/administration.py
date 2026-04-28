import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

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

if "donnees_flagees" not in st.session_state:
    df_api, error = load_flagged_data()
    if error:
        st.warning("Endpoint `/admin/flagged-data` non disponible dans le backend actuel.")
        st.caption(error)
    st.session_state.donnees_flagees = df_api

df = st.session_state.donnees_flagees

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

    st.markdown("---")
    st.subheader("Validation")

    ids = df_anomalies["ID"].tolist()
    selected_id = st.selectbox("Selectionner un ID", ids)

    selected = df[df["ID"] == selected_id].iloc[0]

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"Type : {selected['Type']}")
        st.write(f"Valeur : {selected['Valeur']} {selected['Unite']}")
        st.write(f"Raison du flag : {selected['Raison du flag']}")

    with col2:
        try:
            valeur_num = float(selected["Valeur"])
        except (ValueError, TypeError):
            valeur_num = 0.0
        nouvelle_valeur = st.number_input("Nouvelle valeur", value=valeur_num)
        action = st.radio("Action", ["Valider", "Rejeter", "Modifier puis valider"])

    if st.button("Appliquer"):
        idx = df[df["ID"] == selected_id].index[0]

        if action == "Valider":
            st.session_state.donnees_flagees.at[idx, col_anomalie] = False
            st.success(f"Donnee {selected_id} validee.")

        elif action == "Rejeter":
            st.session_state.donnees_flagees.drop(index=idx, inplace=True)
            st.warning(f"Donnee {selected_id} rejetee.")

        else:
            st.session_state.donnees_flagees.at[idx, "Valeur"] = nouvelle_valeur
            st.session_state.donnees_flagees.at[idx, col_anomalie] = False
            st.success(f"Donnee {selected_id} modifiee et validee.")

        st.rerun()
