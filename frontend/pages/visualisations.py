import requests
import pandas as pd
import plotly.express as px
import streamlit as st

API_BASE = "http://localhost:8000"


def _get(endpoint: str) -> list | dict | None:
    try:
        resp = requests.get(f"{API_BASE}{endpoint}", timeout=5)
        resp.raise_for_status()
        body = resp.json()
        if isinstance(body, dict) and not body.get("success", True):
            st.error(f"Erreur API `{endpoint}` : {body.get('error')}")
            return None
        return body.get("data") if isinstance(body, dict) and "data" in body else body
    except requests.exceptions.ConnectionError:
        st.error(f"Impossible de joindre le backend ({API_BASE}). Vérifiez que le serveur est démarré.")
        return None
    except Exception as ex:
        st.error(f"Erreur lors de l'appel `{endpoint}` : {ex}")
        return None


def _df(endpoint: str) -> pd.DataFrame:
    data = _get(endpoint)
    if not data:
        return pd.DataFrame()
    return pd.DataFrame(data)


# ── Page ─────────────────────────────────────────────────────────────────────

st.title("Visualisations & Analyses")
st.markdown("Exploration des données patients et alimentaires par catégorie thématique.")
st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# CATÉGORIE 1 — Profil épidémiologique des patients
# ═══════════════════════════════════════════════════════════════════════════

st.header("Profil épidémiologique des patients")

col_a, col_b = st.columns(2)

with col_a:
    # Donut — répartition des pathologies
    df = _df("/kpi/diseases_repartition")
    if not df.empty:
        df.columns = ["Pathologie", "Nombre de patients"]
        fig = px.pie(
            df,
            names="Pathologie",
            values="Nombre de patients",
            title="Répartition des patients par pathologie",
            hole=0.4,
        )
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

with col_b:
    # Bar empilé — maladies par genre
    df = _df("/kpi/diseases_by_gender")
    if not df.empty:
        df.columns = ["Genre", "Pathologie", "Nombre de patients"]
        fig = px.bar(
            df,
            x="Pathologie",
            y="Nombre de patients",
            color="Genre",
            barmode="stack",
            title="Répartition des pathologies par genre",
        )
        st.plotly_chart(fig, use_container_width=True)

col_c, col_d = st.columns(2)

with col_c:
    # Bar groupé — IMC moyen/min/max par genre
    df = _df("/kpi/avgBmiByGender")
    if not df.empty:
        df.columns = ["Genre", "IMC moyen", "IMC min", "IMC max", "Nombre de patients"]
        df_long = df.melt(
            id_vars="Genre",
            value_vars=["IMC moyen", "IMC min", "IMC max"],
            var_name="Indicateur",
            value_name="IMC",
        )
        fig = px.bar(
            df_long,
            x="Genre",
            y="IMC",
            color="Indicateur",
            barmode="group",
            title="Distribution de l'IMC (moyen, min, max) par genre",
        )
        fig.add_hline(y=25, line_dash="dash", line_color="orange", annotation_text="Surpoids (25)")
        fig.add_hline(y=30, line_dash="dash", line_color="red", annotation_text="Obésité (30)")
        st.plotly_chart(fig, use_container_width=True)

with col_d:
    # Scatter — IMC moyen par âge
    df = _df("/kpi/avgbBmiByAge")
    if not df.empty:
        df.columns = ["Âge", "IMC moyen"]
        fig = px.line(
            df.sort_values("Âge"),
            x="Âge",
            y="IMC moyen",
            markers=True,
            title="Évolution de l'IMC moyen selon l'âge",
        )
        fig.add_hline(y=25, line_dash="dash", line_color="orange", annotation_text="Surpoids (25)")
        fig.add_hline(y=30, line_dash="dash", line_color="red", annotation_text="Obésité (30)")
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# CATÉGORIE 2 — Comportement alimentaire et adhérence aux régimes
# ═══════════════════════════════════════════════════════════════════════════

st.header("Comportement alimentaire et adhérence aux régimes")

col_e, col_f = st.columns(2)

with col_e:
    # Bar horizontal — régimes recommandés par fréquence
    df = _df("/kpi/diet_recommendation_repartition")
    if not df.empty:
        df.columns = ["Régime recommandé", "Nombre de patients"]
        fig = px.bar(
            df.sort_values("Nombre de patients"),
            x="Nombre de patients",
            y="Régime recommandé",
            orientation="h",
            title="Régimes diététiques prescrits (par fréquence)",
            color="Nombre de patients",
            color_continuous_scale="Teal",
        )
        st.plotly_chart(fig, use_container_width=True)

with col_f:
    # Bar — adhérence moyenne au régime par pathologie
    df = _df("/kpi/adherence_by_disease")
    if not df.empty:
        df.columns = ["Pathologie", "Adhérence moyenne (%)"]
        fig = px.bar(
            df.sort_values("Adhérence moyenne (%)"),
            x="Pathologie",
            y="Adhérence moyenne (%)",
            color="Pathologie",
            title="Adhérence moyenne au régime selon la pathologie",
            text_auto=".1f",
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

col_g, col_h = st.columns(2)

with col_g:
    # Bar — allergies les plus fréquentes
    df = _df("/kpi/allergic_reparition")
    if not df.empty:
        df.columns = ["Allergie", "Nombre de patients"]
        fig = px.bar(
            df.sort_values("Nombre de patients", ascending=False),
            x="Allergie",
            y="Nombre de patients",
            color="Allergie",
            title="Répartition des allergies alimentaires chez les patients",
        )
        st.plotly_chart(fig, use_container_width=True)

with col_h:
    # Line + scatter — caloric intake et adhérence par niveau d'activité
    df = _df("/kpi/adherenceByActivityLevel")
    if not df.empty:
        df.columns = ["Niveau d'activité", "Adhérence (%)", "Calories moy. (kcal)", "Nb patients"]
        fig = px.scatter(
            df,
            x="Calories moy. (kcal)",
            y="Adhérence (%)",
            size="Nb patients",
            color="Niveau d'activité",
            text="Niveau d'activité",
            title="Apport calorique et adhérence au régime selon le niveau d'activité physique",
        )
        fig.update_traces(textposition="top center")
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# CATÉGORIE 3 — Indicateurs de santé critiques
# ═══════════════════════════════════════════════════════════════════════════

st.header("Indicateurs de santé critiques")

col_i, col_j = st.columns(2)

with col_i:
    # Bar — patients dépassant les seuils cliniques
    data = _get("/kpi/at_risk_patients")
    if data:
        total = data.get("total_patients", 0)
        risk_df = pd.DataFrame({
            "Indicateur": ["Cholestérol élevé\n(> 200 mg/dL)", "Glycémie élevée\n(> 126 mg/dL)"],
            "Patients à risque": [data.get("cholesterol_high", 0), data.get("glucose_high", 0)],
        })
        risk_df["Pourcentage (%)"] = (risk_df["Patients à risque"] / total * 100).round(1) if total else 0
        fig = px.bar(
            risk_df,
            x="Indicateur",
            y="Patients à risque",
            text="Pourcentage (%)",
            title="Patients dépassant les seuils cliniques critiques",
            color="Indicateur",
            color_discrete_sequence=["#E74C3C", "#F39C12"],
        )
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
        st.metric("Total patients analysés", total)

with col_j:
    # Bar — score de déséquilibre nutritionnel par sévérité
    df = _df("/kpi/imbalance_score_by_severity")
    if not df.empty:
        df.columns = ["Sévérité", "Score de déséquilibre moyen"]
        severity_order = {"Mild": 1, "Moderate": 2, "Severe": 3}
        df["_order"] = df["Sévérité"].map(severity_order)
        df = df.sort_values("_order").drop(columns="_order")
        fig = px.bar(
            df,
            x="Sévérité",
            y="Score de déséquilibre moyen",
            color="Sévérité",
            color_discrete_map={"Mild": "#2ECC71", "Moderate": "#F39C12", "Severe": "#E74C3C"},
            title="Score de déséquilibre nutritionnel moyen par sévérité de pathologie",
            text_auto=".2f",
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

# Calories moyennes par niveau d'activité
df = _df("/kpi/avgbKcal")
if not df.empty:
    df.columns = ["Niveau d'activité", "Calories moyennes (kcal)"]
    fig = px.bar(
        df.sort_values("Calories moyennes (kcal)", ascending=False),
        x="Niveau d'activité",
        y="Calories moyennes (kcal)",
        color="Calories moyennes (kcal)",
        color_continuous_scale="Oranges",
        title="Apport calorique quotidien moyen selon le niveau d'activité physique",
        text_auto=".0f",
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# CATÉGORIE 4 — Composition nutritionnelle des aliments
# ═══════════════════════════════════════════════════════════════════════════

st.header("Composition nutritionnelle des aliments")

col_k, col_l = st.columns(2)

with col_k:
    # Bar horizontal — nombre d'aliments par catégorie
    df = _df("/kpi/nbrFoodsItemByCategory")
    if not df.empty:
        df.columns = ["Catégorie", "Nombre d'aliments"]
        fig = px.bar(
            df.sort_values("Nombre d'aliments"),
            x="Nombre d'aliments",
            y="Catégorie",
            orientation="h",
            color="Nombre d'aliments",
            color_continuous_scale="Greens",
            title="Nombre d'aliments référencés par catégorie alimentaire",
        )
        st.plotly_chart(fig, use_container_width=True)

with col_l:
    # Bar groupé — macronutriments moyens par repas
    df = _df("/kpi/avgKcalByMeal")
    if not df.empty:
        df.columns = ["Type de repas", "Calories moy. (kcal)", "Protéines moy. (g)", "Lipides moy. (g)", "Fibres moy. (g)"]
        macro_long = df.melt(
            id_vars="Type de repas",
            value_vars=["Protéines moy. (g)", "Lipides moy. (g)", "Fibres moy. (g)"],
            var_name="Macronutriment",
            value_name="Quantité (g)",
        )
        fig = px.bar(
            macro_long,
            x="Type de repas",
            y="Quantité (g)",
            color="Macronutriment",
            barmode="group",
            title="Apports moyens en macronutriments par type de repas",
        )
        st.plotly_chart(fig, use_container_width=True)

col_m, col_n = st.columns(2)

with col_m:
    # Bar horizontal — top aliments riches en fibres
    df = _df("/kpi/topFiberFoods")
    if not df.empty:
        df.columns = ["Aliment", "Catégorie", "Fibres (g)", "Calories (kcal)"]
        fig = px.bar(
            df.sort_values("Fibres (g)"),
            x="Fibres (g)",
            y="Aliment",
            orientation="h",
            color="Catégorie",
            title="Top 10 aliments les plus riches en fibres",
        )
        st.plotly_chart(fig, use_container_width=True)

with col_n:
    # Scatter — fibres vs calories pour les aliments riches en fibres
    df_fiber = _df("/kpi/topFiberFoods")
    df_sodium = _df("/kpi/lowSodiumFoods")
    if not df_sodium.empty:
        df_sodium.columns = ["Aliment", "Catégorie", "Sodium (mg)", "Calories (kcal)", "Protéines (g)"]
        fig = px.scatter(
            df_sodium,
            x="Sodium (mg)",
            y="Protéines (g)",
            size="Calories (kcal)",
            color="Catégorie",
            text="Aliment",
            title="Aliments à faible sodium : teneur en protéines vs sodium (taille = calories)",
        )
        fig.update_traces(textposition="top center")
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════
# CATÉGORIE 5 — Output des datasets
# ═══════════════════════════════════════════════════════════════════════════

st.header("Output des datasets")

tab1, tab2, tab3, tab4 = st.tabs([
    "Patients & pathologies",
    "Régimes & adhérence",
    "Aliments (fibres)",
    "Aliments (faible sodium)",
])

with tab1:
    df_diseases = _df("/kpi/diseases_repartition")
    df_gender   = _df("/kpi/diseases_by_gender")
    if not df_diseases.empty:
        df_diseases.columns = ["Pathologie", "Nombre de patients"]
        st.markdown(f"**{len(df_diseases)} pathologies · données en temps réel**")
        st.dataframe(df_diseases, use_container_width=True)
    if not df_gender.empty:
        df_gender.columns = ["Genre", "Pathologie", "Nombre de patients"]
        st.dataframe(df_gender, use_container_width=True)

with tab2:
    df_adh = _df("/kpi/adherence_by_disease")
    df_act = _df("/kpi/adherenceByActivityLevel")
    if not df_adh.empty:
        df_adh.columns = ["Pathologie", "Adhérence moyenne (%)"]
        st.dataframe(df_adh, use_container_width=True)
    if not df_act.empty:
        df_act.columns = ["Niveau d'activité", "Adhérence (%)", "Calories moy. (kcal)", "Nb patients"]
        st.dataframe(df_act, use_container_width=True)

with tab3:
    df_fiber = _df("/kpi/topFiberFoods")
    if not df_fiber.empty:
        df_fiber.columns = ["Aliment", "Catégorie", "Fibres (g)", "Calories (kcal)"]
        st.markdown(f"**{len(df_fiber)} aliments**")
        st.dataframe(df_fiber, use_container_width=True)

with tab4:
    df_sodium = _df("/kpi/lowSodiumFoods")
    if not df_sodium.empty:
        df_sodium.columns = ["Aliment", "Catégorie", "Sodium (mg)", "Calories (kcal)", "Protéines (g)"]
        st.markdown(f"**{len(df_sodium)} aliments**")
        st.dataframe(df_sodium, use_container_width=True)
