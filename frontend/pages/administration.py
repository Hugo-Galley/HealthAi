import streamlit as st
import pandas as pd

st.title("Administration")
st.markdown("---")

st.subheader("Donnees flaggees")

if "donnees_flagees" not in st.session_state:
    st.session_state.donnees_flagees = pd.DataFrame(
        [
            {
                "ID": 1,
                "Type": "Nutrition",
                "Valeur": 5200,
                "Unite": "kcal",
                "Raison du flag": "Total calories anormalement élevé",
                "Statut": "En attente",
                "Anomalie": False,
            },
            {
                "ID": 2,
                "Type": "Activite",
                "Valeur": 52,
                "Unite": "km",
                "Raison du flag": "Distance suspecte",
                "Statut": "En attente",
                "Anomalie": True,
            },
            {
                "ID": 3,
                "Type": "Nutrition",
                "Valeur": 120,
                "Unite": "g",
                "Raison du flag": "Apport en lipides inhabituel",
                "Statut": "En attente",
                "Anomalie": True,
            },
        ]
    )

df = st.session_state.donnees_flagees
col_anomalie = "Anomalie" if "Anomalie" in df.columns else "anomalie"
df_anomalies = df[df[col_anomalie] == True] if col_anomalie in df.columns else pd.DataFrame()

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
        nouvelle_valeur = st.number_input(
            "Nouvelle valeur",
            value=float(selected["Valeur"]),
        )
        action = st.radio("Action", ["Valider", "Rejeter", "Modifier puis valider"])

    if st.button("Appliquer"):
        idx = df[df["ID"] == selected_id].index[0]

        if action == "Valider":
            if col_anomalie in st.session_state.donnees_flagees.columns:
                st.session_state.donnees_flagees.at[idx, col_anomalie] = False
            st.success(f"Donnee {selected_id} validee.")

        elif action == "Rejeter":
            st.session_state.donnees_flagees.drop(index=idx, inplace=True)
            st.warning(f"Donnee {selected_id} rejetee.")

        else:
            st.session_state.donnees_flagees.at[idx, "Valeur"] = nouvelle_valeur
            if col_anomalie in st.session_state.donnees_flagees.columns:
                st.session_state.donnees_flagees.at[idx, col_anomalie] = False
            st.success(f"Donnee {selected_id} modifiee et validee.")

        st.rerun()

