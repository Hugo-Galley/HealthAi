from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


def demo_diet_data() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Patient_ID": 1,
                "Age": 27,
                "Gender": "Female",
                "BMI": 25.2,
                "Disease_Type": "Diabetes",
                "Severity": "Moderate",
                "Physical_Activity_Level": "Moderate",
                "Daily_Caloric_Intake": 2400,
                "Cholesterol_mg/dL": 210,
                "Blood_Pressure_mmHg": 145,
                "Glucose_mg/dL": 130,
                "Allergies": "None",
                "Adherence_to_Diet_Plan": 68,
                "Dietary_Nutrient_Imbalance_Score": 2.7,
                "Diet_Recommendation": "Low_Carb",
            },
            {
                "Patient_ID": 2,
                "Age": 44,
                "Gender": "Male",
                "BMI": 29.1,
                "Disease_Type": "Obesity",
                "Severity": "Severe",
                "Physical_Activity_Level": "Sedentary",
                "Daily_Caloric_Intake": 2300,
                "Cholesterol_mg/dL": 215,
                "Blood_Pressure_mmHg": 150,
                "Glucose_mg/dL": 118,
                "Allergies": "Peanuts",
                "Adherence_to_Diet_Plan": 71,
                "Dietary_Nutrient_Imbalance_Score": 3.4,
                "Diet_Recommendation": "Balanced",
            },
            {
                "Patient_ID": 3,
                "Age": 61,
                "Gender": "Female",
                "BMI": 27.8,
                "Disease_Type": "Hypertension",
                "Severity": "Mild",
                "Physical_Activity_Level": "Active",
                "Daily_Caloric_Intake": 2700,
                "Cholesterol_mg/dL": 180,
                "Blood_Pressure_mmHg": 135,
                "Glucose_mg/dL": 122,
                "Allergies": "Gluten",
                "Adherence_to_Diet_Plan": 74,
                "Dietary_Nutrient_Imbalance_Score": 2.0,
                "Diet_Recommendation": "Low_Sodium",
            },
            {
                "Patient_ID": 4,
                "Age": 74,
                "Gender": "Male",
                "BMI": 30.0,
                "Disease_Type": "None",
                "Severity": "Mild",
                "Physical_Activity_Level": "Moderate",
                "Daily_Caloric_Intake": 2550,
                "Cholesterol_mg/dL": 199,
                "Blood_Pressure_mmHg": 141,
                "Glucose_mg/dL": 127,
                "Allergies": "None",
                "Adherence_to_Diet_Plan": 70,
                "Dietary_Nutrient_Imbalance_Score": 2.1,
                "Diet_Recommendation": "Balanced",
            },
        ]
    )


def demo_food_data() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"Food_Item": "Oatmeal", "Category": "Grain", "Calories (kcal)": 150, "Protein (g)": 5, "Fat (g)": 3, "Fiber (g)": 4, "Meal_Type": "Breakfast", "Sodium (mg)": 6},
            {"Food_Item": "Greek Yogurt", "Category": "Protein/Dairy", "Calories (kcal)": 120, "Protein (g)": 11, "Fat (g)": 4, "Fiber (g)": 0, "Meal_Type": "Breakfast", "Sodium (mg)": 55},
            {"Food_Item": "Chicken Salad", "Category": "Meal/Processed", "Calories (kcal)": 340, "Protein (g)": 26, "Fat (g)": 14, "Fiber (g)": 5, "Meal_Type": "Lunch", "Sodium (mg)": 320},
            {"Food_Item": "Rice Bowl", "Category": "Meal/Processed", "Calories (kcal)": 410, "Protein (g)": 18, "Fat (g)": 12, "Fiber (g)": 6, "Meal_Type": "Dinner", "Sodium (mg)": 410},
            {"Food_Item": "Apple", "Category": "Fruit", "Calories (kcal)": 95, "Protein (g)": 0.5, "Fat (g)": 0.3, "Fiber (g)": 4.4, "Meal_Type": "Snack", "Sodium (mg)": 2},
        ]
    )


def load_dataset(filename: str) -> pd.DataFrame:
    path = Path(__file__).resolve().parent.parent / "data" / filename
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


st.title("Dashboard KPI")
st.markdown("---")

diet_df = load_dataset("diet_recommendations_dataset.csv")
food_df = load_dataset("daily_food_nutrition_dataset.csv")

using_demo = False
if diet_df.empty:
    diet_df = demo_diet_data()
    using_demo = True
if food_df.empty:
    food_df = demo_food_data()
    using_demo = True

if using_demo:
    st.info("Datasets KPI absents dans data/. Affichage en mode demo.")

for col in ["Age", "BMI", "Adherence_to_Diet_Plan", "Daily_Caloric_Intake", "Dietary_Nutrient_Imbalance_Score", "Cholesterol_mg/dL", "Blood_Pressure_mmHg", "Glucose_mg/dL"]:
    if col in diet_df.columns:
        diet_df[col] = pd.to_numeric(diet_df[col], errors="coerce")

st.subheader("KPI 1, 4, 9")
col1, col2, col3 = st.columns(3)

with col1:
    kpi1 = diet_df["Disease_Type"].value_counts().reset_index()
    kpi1.columns = ["Disease_Type", "Patients"]
    st.plotly_chart(px.pie(kpi1, names="Disease_Type", values="Patients", title="Patients par maladie"), use_container_width=True)

with col2:
    kpi4 = diet_df["Diet_Recommendation"].value_counts().reset_index()
    kpi4.columns = ["Diet_Recommendation", "Patients"]
    st.plotly_chart(px.bar(kpi4, x="Diet_Recommendation", y="Patients", title="Regimes recommandes"), use_container_width=True)

with col3:
    kpi9 = diet_df["Allergies"].value_counts().reset_index()
    kpi9.columns = ["Allergies", "Patients"]
    st.plotly_chart(px.bar(kpi9, x="Allergies", y="Patients", title="Repartition des allergies"), use_container_width=True)

st.subheader("KPI 2, 3, 5, 6")
age_bins = [18, 31, 51, 71, 200]
age_labels = ["18-30", "31-50", "51-70", "70+"]
diet_df["Age_Group"] = pd.cut(diet_df["Age"], bins=age_bins, labels=age_labels, right=False)

col4, col5 = st.columns(2)
with col4:
    kpi2 = diet_df.groupby("Age_Group", as_index=False)["BMI"].mean().dropna()
    st.plotly_chart(px.line(kpi2, x="Age_Group", y="BMI", markers=True, title="BMI moyen par tranche d'age"), use_container_width=True)

    kpi3 = diet_df.groupby("Disease_Type", as_index=False)["Adherence_to_Diet_Plan"].mean().dropna()
    st.plotly_chart(px.bar(kpi3, x="Disease_Type", y="Adherence_to_Diet_Plan", title="Adherence moyenne par maladie"), use_container_width=True)

with col5:
    kpi5 = diet_df.groupby("Physical_Activity_Level", as_index=False)["Daily_Caloric_Intake"].mean().dropna()
    st.plotly_chart(px.bar(kpi5, x="Physical_Activity_Level", y="Daily_Caloric_Intake", title="Calories moyennes par activite"), use_container_width=True)

    kpi6 = diet_df.groupby("Severity", as_index=False)["Dietary_Nutrient_Imbalance_Score"].mean().dropna()
    st.plotly_chart(px.bar(kpi6, x="Severity", y="Dietary_Nutrient_Imbalance_Score", title="Score desequilibre par severite"), use_container_width=True)

st.subheader("KPI 7, 8, 10")
col6, col7 = st.columns(2)

with col6:
    kpi7 = food_df["Category"].value_counts().reset_index()
    kpi7.columns = ["Category", "Foods"]
    st.plotly_chart(px.bar(kpi7, x="Category", y="Foods", title="Aliments par categorie"), use_container_width=True)

    nutrition_cols = ["Calories (kcal)", "Protein (g)", "Fat (g)", "Fiber (g)"]
    available_cols = [c for c in nutrition_cols if c in food_df.columns]
    if "Meal_Type" in food_df.columns and available_cols:
        kpi8 = food_df.groupby("Meal_Type", as_index=False)[available_cols].mean()
        st.dataframe(kpi8, use_container_width=True)

with col7:
    total_patients = int(diet_df["Patient_ID"].count()) if "Patient_ID" in diet_df.columns else int(len(diet_df))
    high_cholesterol = int((diet_df["Cholesterol_mg/dL"] > 200).sum()) if "Cholesterol_mg/dL" in diet_df.columns else 0
    high_bp = int((diet_df["Blood_Pressure_mmHg"] > 140).sum()) if "Blood_Pressure_mmHg" in diet_df.columns else 0
    high_glucose = int((diet_df["Glucose_mg/dL"] > 126).sum()) if "Glucose_mg/dL" in diet_df.columns else 0

    risk_df = pd.DataFrame(
        {
            "Indicateur": ["Cholesterol eleve", "Tension elevee", "Glycemie elevee"],
            "Patients": [high_cholesterol, high_bp, high_glucose],
        }
    )
    st.plotly_chart(px.bar(risk_df, x="Indicateur", y="Patients", title="Patients a risque"), use_container_width=True)
    st.metric("Total patients", total_patients)
