import pandas as pd
import plotly.express as px
import streamlit as st

from api_client import get_json


def load_kpi(path: str) -> tuple[pd.DataFrame, str | None]:
    payload = get_json(path)
    if not payload.get("success"):
        return pd.DataFrame(), payload.get("error", f"API error on {path}")
    data = payload.get("data")
    if isinstance(data, list):
        return pd.DataFrame(data), None
    if isinstance(data, dict):
        return pd.DataFrame([data]), None
    return pd.DataFrame(), f"Unexpected payload for {path}"


st.title("Nutrition")
st.markdown("---")

errors: list[str] = []

categories_df, err = load_kpi("/kpi/nbrFoodsItemByCategory")
if err:
    errors.append(err)
top_fiber_df, err = load_kpi("/kpi/topFiberFoods")
if err:
    errors.append(err)
low_sodium_df, err = load_kpi("/kpi/lowSodiumFoods")
if err:
    errors.append(err)
meal_avg_df, err = load_kpi("/kpi/avgKcalByMeal")
if err:
    errors.append(err)

if errors:
    st.warning("Certaines donnees nutrition n'ont pas pu etre chargees depuis l'API.")
    st.caption("\n".join(f"- {error}" for error in sorted(set(errors))))

avg_cal = meal_avg_df["avg_calories"].mean() if "avg_calories" in meal_avg_df.columns else None
avg_protein = meal_avg_df["avg_protein"].mean() if "avg_protein" in meal_avg_df.columns else None
avg_fat = meal_avg_df["avg_fat"].mean() if "avg_fat" in meal_avg_df.columns else None

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Calories moyennes", f"{avg_cal:.1f}" if avg_cal is not None else "N/A")
with col2:
    st.metric("Proteines moyennes", f"{avg_protein:.1f} g" if avg_protein is not None else "N/A")
with col3:
    st.metric("Lipides moyens", f"{avg_fat:.1f} g" if avg_fat is not None else "N/A")

st.markdown("---")

left, right = st.columns(2)

with left:
    st.subheader("Repartition des aliments par categorie")
    if {"category", "count"}.issubset(categories_df.columns):
        fig = px.bar(categories_df, x="category", y="count")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("KPI categories indisponible.")

with right:
    st.subheader("Top aliments riches en fibres")
    expected_top = ["name", "category", "fiber_g", "calories_kcal"]
    if all(col in top_fiber_df.columns for col in expected_top):
        st.dataframe(top_fiber_df[expected_top], use_container_width=True)
    else:
        st.info("KPI fibres indisponible.")

st.markdown("---")
st.subheader("Aliments a faible sodium")
expected_low = ["name", "category", "sodium_mg", "calories_kcal", "protein_g"]
if all(col in low_sodium_df.columns for col in expected_low):
    st.dataframe(low_sodium_df[expected_low], use_container_width=True)
else:
    st.info("KPI sodium indisponible.")
