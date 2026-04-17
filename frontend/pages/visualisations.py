from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# ── Chargement ──────────────────────────────────────────────────────────────

def _load(filename: str) -> pd.DataFrame:
    path = Path(__file__).resolve().parent.parent / "data" / filename
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def _demo_patients() -> pd.DataFrame:
    return pd.DataFrame([
        {"Patient_ID": 1, "Age": 27, "Gender": "Female", "BMI": 25.2, "Disease_Type": "Diabetes",      "Severity": "Moderate", "Physical_Activity_Level": "Moderate",  "Daily_Caloric_Intake": 2400, "Cholesterol_mg/dL": 210, "Blood_Pressure_mmHg": 145, "Glucose_mg/dL": 130, "Allergies": "None",    "Adherence_to_Diet_Plan": 68, "Dietary_Nutrient_Imbalance_Score": 2.7, "Diet_Recommendation": "Low_Carb"},
        {"Patient_ID": 2, "Age": 44, "Gender": "Male",   "BMI": 29.1, "Disease_Type": "Obesity",        "Severity": "Severe",   "Physical_Activity_Level": "Sedentary",  "Daily_Caloric_Intake": 2300, "Cholesterol_mg/dL": 215, "Blood_Pressure_mmHg": 150, "Glucose_mg/dL": 118, "Allergies": "Peanuts", "Adherence_to_Diet_Plan": 71, "Dietary_Nutrient_Imbalance_Score": 3.4, "Diet_Recommendation": "Balanced"},
        {"Patient_ID": 3, "Age": 61, "Gender": "Female", "BMI": 27.8, "Disease_Type": "Hypertension",   "Severity": "Mild",     "Physical_Activity_Level": "Active",     "Daily_Caloric_Intake": 2700, "Cholesterol_mg/dL": 180, "Blood_Pressure_mmHg": 135, "Glucose_mg/dL": 122, "Allergies": "Gluten",  "Adherence_to_Diet_Plan": 74, "Dietary_Nutrient_Imbalance_Score": 2.0, "Diet_Recommendation": "Low_Sodium"},
        {"Patient_ID": 4, "Age": 74, "Gender": "Male",   "BMI": 30.0, "Disease_Type": "None",           "Severity": "Mild",     "Physical_Activity_Level": "Moderate",   "Daily_Caloric_Intake": 2550, "Cholesterol_mg/dL": 199, "Blood_Pressure_mmHg": 141, "Glucose_mg/dL": 127, "Allergies": "None",    "Adherence_to_Diet_Plan": 70, "Dietary_Nutrient_Imbalance_Score": 2.1, "Diet_Recommendation": "Balanced"},
        {"Patient_ID": 5, "Age": 35, "Gender": "Female", "BMI": 22.4, "Disease_Type": "Diabetes",       "Severity": "Mild",     "Physical_Activity_Level": "Active",     "Daily_Caloric_Intake": 1950, "Cholesterol_mg/dL": 175, "Blood_Pressure_mmHg": 120, "Glucose_mg/dL": 110, "Allergies": "None",    "Adherence_to_Diet_Plan": 85, "Dietary_Nutrient_Imbalance_Score": 1.5, "Diet_Recommendation": "Low_Carb"},
        {"Patient_ID": 6, "Age": 52, "Gender": "Male",   "BMI": 31.5, "Disease_Type": "Obesity",        "Severity": "Moderate", "Physical_Activity_Level": "Sedentary",  "Daily_Caloric_Intake": 3100, "Cholesterol_mg/dL": 230, "Blood_Pressure_mmHg": 160, "Glucose_mg/dL": 140, "Allergies": "Lactose", "Adherence_to_Diet_Plan": 55, "Dietary_Nutrient_Imbalance_Score": 4.1, "Diet_Recommendation": "Balanced"},
        {"Patient_ID": 7, "Age": 68, "Gender": "Female", "BMI": 26.3, "Disease_Type": "Hypertension",   "Severity": "Severe",   "Physical_Activity_Level": "Moderate",   "Daily_Caloric_Intake": 2200, "Cholesterol_mg/dL": 195, "Blood_Pressure_mmHg": 170, "Glucose_mg/dL": 115, "Allergies": "None",    "Adherence_to_Diet_Plan": 62, "Dietary_Nutrient_Imbalance_Score": 2.9, "Diet_Recommendation": "Low_Sodium"},
        {"Patient_ID": 8, "Age": 29, "Gender": "Male",   "BMI": 23.0, "Disease_Type": "None",           "Severity": "Mild",     "Physical_Activity_Level": "Active",     "Daily_Caloric_Intake": 2600, "Cholesterol_mg/dL": 165, "Blood_Pressure_mmHg": 118, "Glucose_mg/dL": 95,  "Allergies": "None",    "Adherence_to_Diet_Plan": 90, "Dietary_Nutrient_Imbalance_Score": 1.2, "Diet_Recommendation": "Balanced"},
    ])


def _demo_aliments() -> pd.DataFrame:
    return pd.DataFrame([
        {"Food_Item": "Flocons d'avoine",  "Category": "Céréales",         "Calories (kcal)": 150, "Protein (g)": 5.0, "Fat (g)": 3.0,  "Fiber (g)": 4.4, "Sodium (mg)": 6,   "Meal_Type": "Petit-déjeuner"},
        {"Food_Item": "Yaourt grec",       "Category": "Protéines/Laitier","Calories (kcal)": 120, "Protein (g)": 11.0,"Fat (g)": 4.0,  "Fiber (g)": 0.0, "Sodium (mg)": 55,  "Meal_Type": "Petit-déjeuner"},
        {"Food_Item": "Salade de poulet",  "Category": "Plats/Préparés",   "Calories (kcal)": 340, "Protein (g)": 26.0,"Fat (g)": 14.0, "Fiber (g)": 5.0, "Sodium (mg)": 320, "Meal_Type": "Déjeuner"},
        {"Food_Item": "Bol de riz",        "Category": "Céréales",         "Calories (kcal)": 410, "Protein (g)": 18.0,"Fat (g)": 12.0, "Fiber (g)": 6.0, "Sodium (mg)": 410, "Meal_Type": "Dîner"},
        {"Food_Item": "Pomme",             "Category": "Fruits",           "Calories (kcal)": 95,  "Protein (g)": 0.5, "Fat (g)": 0.3,  "Fiber (g)": 4.4, "Sodium (mg)": 2,   "Meal_Type": "Collation"},
        {"Food_Item": "Saumon grillé",     "Category": "Protéines/Laitier","Calories (kcal)": 280, "Protein (g)": 32.0,"Fat (g)": 15.0, "Fiber (g)": 0.0, "Sodium (mg)": 85,  "Meal_Type": "Dîner"},
        {"Food_Item": "Épinards cuits",    "Category": "Légumes",          "Calories (kcal)": 41,  "Protein (g)": 5.0, "Fat (g)": 0.5,  "Fiber (g)": 4.1, "Sodium (mg)": 70,  "Meal_Type": "Déjeuner"},
        {"Food_Item": "Pois chiches",      "Category": "Légumineuses",     "Calories (kcal)": 270, "Protein (g)": 15.0,"Fat (g)": 4.0,  "Fiber (g)": 12.5,"Sodium (mg)": 10,  "Meal_Type": "Dîner"},
        {"Food_Item": "Banane",            "Category": "Fruits",           "Calories (kcal)": 105, "Protein (g)": 1.3, "Fat (g)": 0.4,  "Fiber (g)": 3.1, "Sodium (mg)": 1,   "Meal_Type": "Collation"},
        {"Food_Item": "Pain complet",      "Category": "Céréales",         "Calories (kcal)": 135, "Protein (g)": 5.0, "Fat (g)": 2.0,  "Fiber (g)": 3.8, "Sodium (mg)": 200, "Meal_Type": "Petit-déjeuner"},
        {"Food_Item": "Lentilles rouges",  "Category": "Légumineuses",     "Calories (kcal)": 230, "Protein (g)": 18.0,"Fat (g)": 1.0,  "Fiber (g)": 15.6,"Sodium (mg)": 5,   "Meal_Type": "Dîner"},
        {"Food_Item": "Tomates cerises",   "Category": "Légumes",          "Calories (kcal)": 35,  "Protein (g)": 1.8, "Fat (g)": 0.4,  "Fiber (g)": 1.2, "Sodium (mg)": 8,   "Meal_Type": "Déjeuner"},
    ])


# ── Page config ──────────────────────────────────────────────────────────────

st.title("Visualisations & Analyses")
st.markdown("Exploration des données patients et alimentaires par catégorie thématique.")
st.markdown("---")

patients_df = _load("diet_recommendations_dataset.csv")
aliments_df = _load("daily_food_nutrition_dataset.csv")

using_demo = False
if patients_df.empty:
    patients_df = _demo_patients()
    using_demo = True
if aliments_df.empty:
    aliments_df = _demo_aliments()
    using_demo = True

if using_demo:
    st.info("Données réelles absentes dans data/. Affichage en mode démonstration.")

# Nettoyage numérique
numeric_cols = [
    "Age", "BMI", "Adherence_to_Diet_Plan", "Daily_Caloric_Intake",
    "Dietary_Nutrient_Imbalance_Score", "Cholesterol_mg/dL",
    "Blood_Pressure_mmHg", "Glucose_mg/dL",
]
for col in numeric_cols:
    if col in patients_df.columns:
        patients_df[col] = pd.to_numeric(patients_df[col], errors="coerce")

age_bins   = [0, 30, 50, 70, 200]
age_labels = ["< 30 ans", "30–50 ans", "51–70 ans", "> 70 ans"]
patients_df["Tranche d'âge"] = pd.cut(
    patients_df["Age"], bins=age_bins, labels=age_labels, right=False
)

# ═══════════════════════════════════════════════════════════════════════════
# CATÉGORIE 1 — Profil épidémiologique des patients
# ═══════════════════════════════════════════════════════════════════════════

st.header("Profil épidémiologique des patients")

col_a, col_b = st.columns(2)

with col_a:
    # Donut — répartition des pathologies
    maladie_counts = patients_df["Disease_Type"].value_counts().reset_index()
    maladie_counts.columns = ["Pathologie", "Nombre de patients"]
    fig = px.pie(
        maladie_counts,
        names="Pathologie",
        values="Nombre de patients",
        title="Répartition des patients par pathologie",
        hole=0.4,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    # Funnel — sévérité de la maladie
    severity_order = ["Mild", "Moderate", "Severe"]
    severity_counts = (
        patients_df["Severity"]
        .value_counts()
        .reindex(severity_order, fill_value=0)
        .reset_index()
    )
    severity_counts.columns = ["Sévérité", "Nombre de patients"]
    fig = px.funnel(
        severity_counts,
        x="Nombre de patients",
        y="Sévérité",
        title="Entonnoir de gravité des pathologies",
        color="Sévérité",
        color_discrete_sequence=px.colors.sequential.Reds_r,
    )
    st.plotly_chart(fig, use_container_width=True)

col_c, col_d = st.columns(2)

with col_c:
    # Scatter — âge vs IMC, colorié par maladie
    if "Age" in patients_df.columns and "BMI" in patients_df.columns:
        fig = px.scatter(
            patients_df,
            x="Age",
            y="BMI",
            color="Disease_Type",
            size="Daily_Caloric_Intake" if "Daily_Caloric_Intake" in patients_df.columns else None,
            hover_data=["Patient_ID", "Gender", "Severity"] if "Patient_ID" in patients_df.columns else None,
            title="Relation entre l'âge, l'IMC et la pathologie",
            labels={"Age": "Âge", "BMI": "IMC", "Disease_Type": "Pathologie"},
        )
        fig.add_hline(y=25, line_dash="dash", line_color="orange", annotation_text="IMC surpoids (25)")
        fig.add_hline(y=30, line_dash="dash", line_color="red",    annotation_text="IMC obésité (30)")
        st.plotly_chart(fig, use_container_width=True)

with col_d:
    # Histogram — distribution de l'IMC
    if "BMI" in patients_df.columns:
        fig = px.histogram(
            patients_df,
            x="BMI",
            nbins=15,
            color="Gender" if "Gender" in patients_df.columns else None,
            title="Distribution de l'IMC par genre",
            labels={"BMI": "IMC", "count": "Nombre de patients", "Gender": "Genre"},
            barmode="overlay",
            opacity=0.75,
        )
        fig.add_vline(x=25, line_dash="dash", line_color="orange")
        fig.add_vline(x=30, line_dash="dash", line_color="red")
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# CATÉGORIE 2 — Comportement alimentaire et adhérence aux régimes
# ═══════════════════════════════════════════════════════════════════════════

st.header("Comportement alimentaire et adhérence aux régimes")

col_e, col_f = st.columns(2)

with col_e:
    # Bar horizontal — régimes recommandés par fréquence
    regime_counts = patients_df["Diet_Recommendation"].value_counts().reset_index()
    regime_counts.columns = ["Régime recommandé", "Nombre de patients"]
    fig = px.bar(
        regime_counts.sort_values("Nombre de patients"),
        x="Nombre de patients",
        y="Régime recommandé",
        orientation="h",
        title="Régimes diététiques prescrits (par fréquence)",
        color="Nombre de patients",
        color_continuous_scale="Teal",
    )
    st.plotly_chart(fig, use_container_width=True)

with col_f:
    # Box plot — distribution de l'adhérence au régime par pathologie
    if "Adherence_to_Diet_Plan" in patients_df.columns:
        fig = px.box(
            patients_df,
            x="Disease_Type",
            y="Adherence_to_Diet_Plan",
            color="Disease_Type",
            title="Dispersion de l'adhérence au régime selon la pathologie",
            labels={
                "Disease_Type": "Pathologie",
                "Adherence_to_Diet_Plan": "Adhérence au régime (%)",
            },
            points="all",
        )
        st.plotly_chart(fig, use_container_width=True)

col_g, col_h = st.columns(2)

with col_g:
    # Line — IMC moyen par tranche d'âge
    if "BMI" in patients_df.columns:
        imc_age = (
            patients_df.groupby("Tranche d'âge", as_index=False, observed=True)["BMI"]
            .mean()
            .dropna()
        )
        fig = px.line(
            imc_age,
            x="Tranche d'âge",
            y="BMI",
            markers=True,
            title="Évolution de l'IMC moyen par tranche d'âge",
            labels={"BMI": "IMC moyen"},
        )
        fig.update_traces(line_width=3, marker_size=10)
        st.plotly_chart(fig, use_container_width=True)

with col_h:
    # Violin — apport calorique par niveau d'activité
    if "Daily_Caloric_Intake" in patients_df.columns and "Physical_Activity_Level" in patients_df.columns:
        fig = px.violin(
            patients_df,
            x="Physical_Activity_Level",
            y="Daily_Caloric_Intake",
            color="Physical_Activity_Level",
            box=True,
            points="all",
            title="Distribution des apports caloriques selon le niveau d'activité physique",
            labels={
                "Physical_Activity_Level": "Niveau d'activité",
                "Daily_Caloric_Intake": "Apport calorique quotidien (kcal)",
            },
        )
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# CATÉGORIE 3 — Indicateurs de santé critiques
# ═══════════════════════════════════════════════════════════════════════════

st.header("Indicateurs de santé critiques")

col_i, col_j = st.columns(2)

with col_i:
    # Bar — patients dépassant les seuils cliniques
    total = len(patients_df)
    risks = {}
    if "Cholesterol_mg/dL" in patients_df.columns:
        risks["Cholestérol\nélevé (> 200)"]       = int((patients_df["Cholesterol_mg/dL"] > 200).sum())
    if "Blood_Pressure_mmHg" in patients_df.columns:
        risks["Tension artérielle\nélevée (> 140)"] = int((patients_df["Blood_Pressure_mmHg"] > 140).sum())
    if "Glucose_mg/dL" in patients_df.columns:
        risks["Glycémie\nélevée (> 126)"]          = int((patients_df["Glucose_mg/dL"] > 126).sum())

    if risks:
        risk_df = pd.DataFrame({
            "Indicateur": list(risks.keys()),
            "Patients à risque": list(risks.values()),
        })
        risk_df["Pourcentage (%)"] = (risk_df["Patients à risque"] / total * 100).round(1)
        fig = px.bar(
            risk_df,
            x="Indicateur",
            y="Patients à risque",
            text="Pourcentage (%)",
            title="Nombre de patients dépassant les seuils cliniques critiques",
            color="Indicateur",
            color_discrete_sequence=["#E74C3C", "#E67E22", "#F1C40F"],
        )
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
        st.metric("Total patients analysés", total)

with col_j:
    # Scatter — score de déséquilibre nutritionnel vs IMC
    if "Dietary_Nutrient_Imbalance_Score" in patients_df.columns and "BMI" in patients_df.columns:
        fig = px.scatter(
            patients_df,
            x="BMI",
            y="Dietary_Nutrient_Imbalance_Score",
            color="Severity",
            symbol="Disease_Type",
            title="Score de déséquilibre nutritionnel en fonction de l'IMC et de la sévérité",
            labels={
                "BMI": "IMC",
                "Dietary_Nutrient_Imbalance_Score": "Score de déséquilibre nutritionnel",
                "Severity": "Sévérité",
                "Disease_Type": "Pathologie",
            },
        )
        st.plotly_chart(fig, use_container_width=True)

# Histogram des valeurs biologiques
if all(c in patients_df.columns for c in ["Cholesterol_mg/dL", "Blood_Pressure_mmHg", "Glucose_mg/dL"]):
    bio_long = patients_df[["Cholesterol_mg/dL", "Blood_Pressure_mmHg", "Glucose_mg/dL"]].melt(
        var_name="Biomarqueur", value_name="Valeur"
    )
    bio_long["Biomarqueur"] = bio_long["Biomarqueur"].str.replace("_mg/dL", " (mg/dL)").str.replace("_mmHg", " (mmHg)")
    fig = px.histogram(
        bio_long,
        x="Valeur",
        facet_col="Biomarqueur",
        nbins=12,
        title="Distribution des valeurs biologiques mesurées (cholestérol, tension, glycémie)",
        color="Biomarqueur",
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# CATÉGORIE 4 — Composition nutritionnelle des aliments
# ═══════════════════════════════════════════════════════════════════════════

st.header("Composition nutritionnelle des aliments")

col_k, col_l = st.columns(2)

with col_k:
    # Treemap — aliments par catégorie et calories
    if "Category" in aliments_df.columns and "Calories (kcal)" in aliments_df.columns:
        fig = px.treemap(
            aliments_df,
            path=["Category", "Food_Item"],
            values="Calories (kcal)",
            color="Protein (g)" if "Protein (g)" in aliments_df.columns else None,
            color_continuous_scale="Greens",
            title="Répartition calorique des aliments par catégorie (surface = calories, couleur = protéines)",
        )
        st.plotly_chart(fig, use_container_width=True)

with col_l:
    # Bar groupé — macronutriments moyens par repas
    macro_cols = ["Protein (g)", "Fat (g)", "Fiber (g)"]
    available = [c for c in macro_cols if c in aliments_df.columns]
    if "Meal_Type" in aliments_df.columns and available:
        macro_repas = aliments_df.groupby("Meal_Type", as_index=False)[available].mean().round(1)
        macro_long = macro_repas.melt(id_vars="Meal_Type", var_name="Macronutriment", value_name="Quantité (g)")
        fig = px.bar(
            macro_long,
            x="Meal_Type",
            y="Quantité (g)",
            color="Macronutriment",
            barmode="group",
            title="Apports moyens en macronutriments par type de repas",
            labels={"Meal_Type": "Type de repas"},
        )
        st.plotly_chart(fig, use_container_width=True)

# Scatter — fibres vs sodium par catégorie
if "Fiber (g)" in aliments_df.columns and "Sodium (mg)" in aliments_df.columns:
    fig = px.scatter(
        aliments_df,
        x="Fiber (g)",
        y="Sodium (mg)",
        color="Category",
        size="Calories (kcal)" if "Calories (kcal)" in aliments_df.columns else None,
        text="Food_Item",
        title="Teneur en fibres vs teneur en sodium par aliment (taille des bulles = calories)",
        labels={"Category": "Catégorie", "Food_Item": "Aliment"},
    )
    fig.update_traces(textposition="top center")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# CATÉGORIE 5 — Output brut des datasets
# ═══════════════════════════════════════════════════════════════════════════

st.header("Output des datasets")

tab1, tab2 = st.tabs(["Dataset patients & recommandations", "Dataset aliments & nutrition"])

with tab1:
    st.markdown(f"**{len(patients_df)} enregistrements · {len(patients_df.columns)} colonnes**")
    st.dataframe(patients_df, use_container_width=True, height=400)

    csv_patients = patients_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Télécharger le dataset patients (CSV)",
        data=csv_patients,
        file_name="patients_recommandations.csv",
        mime="text/csv",
    )

with tab2:
    st.markdown(f"**{len(aliments_df)} enregistrements · {len(aliments_df.columns)} colonnes**")
    st.dataframe(aliments_df, use_container_width=True, height=400)

    csv_aliments = aliments_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Télécharger le dataset aliments (CSV)",
        data=csv_aliments,
        file_name="aliments_nutrition.csv",
        mime="text/csv",
    )
