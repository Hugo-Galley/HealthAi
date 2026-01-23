import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Administration - HealthAI",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Administration")
st.markdown("---")

# Section pour les données flaggées comme potentiellement non potables
st.subheader("🔍 Données à Valider")
st.markdown("**Panel de validation des données flaggées**")
st.info("Les données ci-dessous ont été marquées comme potentiellement non fiables et nécessitent une validation.")

# TODO: Charger les données flaggées depuis le backend
# Exemple de structure attendue pour df_donnees_flagees:
# df_donnees_flagees = pd.DataFrame({
#     'ID': [ids],
#     'Type': [types],
#     'Date': [dates],
#     'Valeur': [valeurs],
#     'Unité': [unites],
#     'Raison du flag': [raisons],
#     'Statut': [statuts]
# })

# Charger les données depuis le backend (à implémenter)
# donnees_flagees = charger_donnees_flagees()  # Fonction à créer pour appeler l'API backend

# Pour l'instant, on affiche un message
if 'donnees_flagees' not in st.session_state:
    st.session_state.donnees_flagees = pd.DataFrame()

# Affichage des données flaggées
if len(st.session_state.donnees_flagees) > 0:
    st.dataframe(st.session_state.donnees_flagees, use_container_width=True)
else:
    st.info("Aucune donnée flaggée pour le moment. Les données seront chargées depuis le backend.")

st.markdown("---")

# Section pour valider/modifier les données
st.subheader("Validation des Données")

if len(st.session_state.donnees_flagees) > 0:
    selected_id = st.selectbox(
        "Sélectionner une donnée à valider",
        options=st.session_state.donnees_flagees['ID'].tolist()
    )
    
    if selected_id:
        selected_data = st.session_state.donnees_flagees[
            st.session_state.donnees_flagees['ID'] == selected_id
        ].iloc[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Type:** {selected_data['Type']}")
            st.write(f"**Date:** {selected_data['Date']}")
            st.write(f"**Valeur actuelle:** {selected_data['Valeur']} {selected_data['Unité']}")
            st.write(f"**Raison du flag:** {selected_data['Raison du flag']}")
        
        with col2:
            st.write("**Modifier la valeur si nécessaire:**")
            nouvelle_valeur = st.number_input(
                "Nouvelle valeur",
                value=float(selected_data['Valeur']),
                step=0.1
            )
            
            action = st.radio(
                "Action",
                ["Valider", "Rejeter", "Modifier puis Valider"]
            )
            
            if st.button("Appliquer l'action", type="primary"):
                # TODO: Appeler l'API backend pour valider/rejeter/modifier la donnée
                # Exemple:
                # if action == "Valider":
                #     valider_donnee(selected_id)  # Fonction à créer pour appeler l'API
                # elif action == "Rejeter":
                #     rejeter_donnee(selected_id)  # Fonction à créer pour appeler l'API
                # elif action == "Modifier puis Valider":
                #     modifier_et_valider_donnee(selected_id, nouvelle_valeur)  # Fonction à créer
                
                if action == "Valider":
                    st.success(f"✅ Donnée ID {selected_id} validée et ajoutée aux statistiques!")
                    st.info("💡 À connecter avec l'API backend pour persister la validation")
                    # Recharger les données depuis le backend après validation
                    # st.session_state.donnees_flagees = charger_donnees_flagees()
                    st.rerun()
                    
                elif action == "Rejeter":
                    st.warning(f"❌ Donnée ID {selected_id} rejetée!")
                    st.info("💡 À connecter avec l'API backend pour persister le rejet")
                    # Recharger les données depuis le backend après rejet
                    # st.session_state.donnees_flagees = charger_donnees_flagees()
                    st.rerun()
                    
                elif action == "Modifier puis Valider":
                    st.success(f"✅ Donnée ID {selected_id} modifiée ({nouvelle_valeur}) et validée!")
                    st.info("💡 À connecter avec l'API backend pour persister la modification et validation")
                    # Recharger les données depuis le backend après modification
                    # st.session_state.donnees_flagees = charger_donnees_flagees()
                    st.rerun()
else:
    st.success("✅ Aucune donnée en attente de validation!")

st.markdown("---")

# Autres fonctionnalités d'administration
st.subheader("Autres Paramètres d'Administration")
st.write("Contenu à venir : gestion des utilisateurs, paramètres système, etc.")
