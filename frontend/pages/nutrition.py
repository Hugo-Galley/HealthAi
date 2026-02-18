from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


def load_food_data() -> pd.DataFrame:
    data_dir = Path(__file__).resolve().parent.parent / "data"
    full_dataset = data_dir / "daily_food_nutrition_dataset.csv"
    fallback_dataset = data_dir / "base_alimentaire.csv"

    if full_dataset.exists():
        return pd.read_csv(full_dataset)

    if fallback_dataset.exists():
        df = pd.read_csv(fallback_dataset)
        return df.rename(
            columns={
                "Aliment": "Food_Item",
                "Categorie": "Category",
                "Calories": "Calories (kcal)",
                "Proteines": "Protein (g)",
                "Glucides": "Carbohydrates (g)",
                "Lipides": "Fat (g)",
            }
        )

    return pd.DataFrame()


st.title("Nutrition")
st.markdown("---")

df_food = load_food_data()

if df_food.empty:
    st.warning("Aucune donnee alimentaire disponible.")
    st.stop()

if "Category" in df_food.columns:
    categories = ["Toutes"] + sorted(df_food["Category"].dropna().astype(str).unique().tolist())
    category = st.selectbox("Categorie", categories)
    if category != "Toutes":
        df_food = df_food[df_food["Category"] == category]

cal_col = "Calories (kcal)"
protein_col = "Protein (g)"
fat_col = "Fat (g)"
fiber_col = "Fiber (g)"
sodium_col = "Sodium (mg)"

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Calories moyennes", f"{df_food[cal_col].mean():.1f}" if cal_col in df_food.columns else "N/A")
with col2:
    st.metric("Proteines moyennes", f"{df_food[protein_col].mean():.1f} g" if protein_col in df_food.columns else "N/A")
with col3:
    st.metric("Lipides moyens", f"{df_food[fat_col].mean():.1f} g" if fat_col in df_food.columns else "N/A")

st.markdown("---")

left, right = st.columns(2)

with left:
    st.subheader("Repartition des aliments par categorie")
    if "Category" in df_food.columns:
        category_counts = df_food["Category"].value_counts().reset_index()
        category_counts.columns = ["Category", "Count"]
        fig = px.bar(category_counts, x="Category", y="Count")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Colonne Category absente.")

with right:
    st.subheader("Top aliments riches en fibres")
    if fiber_col in df_food.columns and "Food_Item" in df_food.columns:
        st.dataframe(
            df_food.sort_values(by=fiber_col, ascending=False)[["Food_Item", "Category", fiber_col]].head(10),
            use_container_width=True,
        )
    else:
        st.info("Colonnes Fiber (g) / Food_Item absentes.")

st.markdown("---")
st.subheader("Aliments a faible sodium")
if sodium_col in df_food.columns and "Food_Item" in df_food.columns:
    st.dataframe(
        df_food.sort_values(by=sodium_col, ascending=True)[["Food_Item", "Category", sodium_col]].head(10),
        use_container_width=True,
    )
else:
    st.info("Colonnes Sodium (mg) / Food_Item absentes.")
