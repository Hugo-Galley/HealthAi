import streamlit as st
import pandas as pd

st.title("Administration")
st.markdown("---")

st.subheader("Données flaggées")

if "donnees_flagees" not in st.session_state:
    st.session_state.donnees_flagees = pd.DataFrame(
        [
            {
                "ID": 1,
                "Type": "Nutrition",
                "Date": "2024-01-20",
                "Valeur": 5200,
                "Unité": "kcal",
                "Raison du flag": "Total calories anormalement élevé",
                "Statut": "En attente",
            },
            {
                "ID": 2,
                "Type": "Activité",
                "Date": "2024-01-19",
                "Valeur": 52,
                "Unité": "km",
                "Raison du flag": "Distance suspecte",
                "Statut": "En attente",
            },
            {
                "ID": 3,
                "Type": "Nutrition",
                "Date": "2024-01-18",
                "Valeur": 120,
                "Unité": "g",
                "Raison du flag": "Apport en lipides inhabituel",
                "Statut": "En attente",
            },
        ]
    )

df = st.session_state.donnees_flagees

if len(df) == 0:
    st.success("Aucune donnée en attente de validation.")
else:
    st.dataframe(df, use_container_width=True)

    st.markdown("---")
    st.subheader("Validation")

    ids = df["ID"].tolist()
    selected_id = st.selectbox("Sélectionner un ID", ids)

    selected = df[df["ID"] == selected_id].iloc[0]

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"Type : {selected['Type']}")
        st.write(f"Date : {selected['Date']}")
        st.write(f"Valeur : {selected['Valeur']} {selected['Unité']}")
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
            st.session_state.donnees_flagees.drop(index=idx, inplace=True)
            st.success(f"Donnée {selected_id} validée.")

        elif action == "Rejeter":
            st.session_state.donnees_flagees.drop(index=idx, inplace=True)
            st.warning(f"Donnée {selected_id} rejetée.")

        else:
            st.session_state.donnees_flagees.at[idx, "Valeur"] = nouvelle_valeur
            st.session_state.donnees_flagees.drop(index=idx, inplace=True)
            st.success(f"Donnée {selected_id} modifiée et validée.")

        st.rerun()

