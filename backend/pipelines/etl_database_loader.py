import sys
import logging
from pathlib import Path
from uuid import uuid4

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import db
from models import Food, NutritionalValues, Meal, Consumption, Patient, BMI, Disease

logger = logging.getLogger(__name__)


def _to_float(row, col):
    v = row.get(col)
    try:
        return None if pd.isna(v) else float(v)
    except (ValueError, TypeError):
        return None


def _to_int(row, col):
    v = row.get(col)
    try:
        return None if pd.isna(v) else int(float(v))
    except (ValueError, TypeError):
        return None


def _to_str(row, col):
    v = row.get(col)
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    value = str(v).strip()
    return value if value and value != 'None' else None


def _clean_tables(session):
    logger.info("Nettoyage des tables...")
    for model in [Consumption, NutritionalValues, Disease, BMI, Meal, Food, Patient]:
        session.query(model).delete()
    session.commit()
    logger.info("Tables nettoyées.")


def load_food_nutrition(df: pd.DataFrame, session=None):
    session = session or db
    food_cache = {}

    for _, row in df.iterrows():
        food_name = _to_str(row, 'Food_Item')
        meal_type = _to_str(row, 'Meal_Type')
        if not food_name or not meal_type:
            continue

        category = _to_str(row, 'Category')
        key = f"{food_name}_{category}"
        if key not in food_cache:
            food = Food(id=str(uuid4()), name=food_name, category=category)
            session.add(food)
            session.flush()
            food_cache[key] = food
        food = food_cache[key]

        session.add(NutritionalValues(
            id=str(uuid4()), food_id=food.id,
            calories=_to_float(row, 'Calories (kcal)'),
            protein=_to_float(row, 'Protein (g)'),
            carbohydrates=_to_float(row, 'Carbohydrates (g)'),
            fat=_to_float(row, 'Fat (g)'),
            fiber=_to_float(row, 'Fiber (g)'),
            sugars=_to_float(row, 'Sugars (g)'),
            sodium=_to_float(row, 'Sodium (mg)'),
            cholesterol=_to_float(row, 'Cholesterol (mg)'),
        ))

        meal = Meal(id=str(uuid4()), type=meal_type, water_intake=_to_float(row, 'Water_Intake (ml)'))
        session.add(meal)
        session.flush()
        session.add(Consumption(id=str(uuid4()), food_id=food.id, meal_id=meal.id))

    session.commit()
    logger.info(f"Food nutrition chargé : {len(food_cache)} foods, {len(df)} lignes")


def load_diet_recommendations(df: pd.DataFrame, session=None):
    session = session or db
    patient_cache = set()

    for _, row in df.iterrows():
        patient_id = _to_str(row, 'Patient_ID')
        age = _to_int(row, 'Age')
        if not patient_id or age is None:
            continue

        # Patient (dédoublonné par ID)
        if patient_id not in patient_cache:
            session.add(Patient(
                id=patient_id, age=age,
                gender=_to_str(row, 'Gender'),
                daily_caloric_intake=_to_int(row, 'Daily_Caloric_Intake'),
                physical_activity_level=_to_str(row, 'Physical_Activity_Level'),
                allergie=_to_str(row, 'Allergies'),
                dietary_nutrient_imbalance_score=_to_str(row, 'Dietary_Nutrient_Imbalance_Score'),
                adherence_to_diet_plan=_to_str(row, 'Adherence_to_Diet_Plan'),
                cholesterol_mg_dl=_to_float(row, 'Cholesterol_mg/dL'),
                blood_pressure_mmhg=_to_str(row, 'Blood_Pressure_mmHg'),
                glucose_mg_dl=_to_float(row, 'Glucose_mg/dL'),
            ))
            session.flush()
            patient_cache.add(patient_id)

        # BMI
        weight, height = _to_float(row, 'Weight_kg'), _to_float(row, 'Height_cm')
        if weight and height:
            session.add(BMI(
                id=str(uuid4()), patient_id=patient_id,
                weight=weight, height=height, score=_to_float(row, 'BMI'),
            ))

        # Maladie (optionnelle)
        disease_type = _to_str(row, 'Disease_Type')
        if disease_type:
            session.add(Disease(
                id=str(uuid4()), patient_id=patient_id,
                type=disease_type, severity=_to_str(row, 'Severity'),
            ))

    session.commit()
    logger.info(f"Diet recommendations chargé : {len(patient_cache)} patients, {len(df)} lignes")


def run_etl_to_database(food_df=None, diet_df=None, session=None):
    session = session or db
    _clean_tables(session)
    if food_df is not None:
        load_food_nutrition(food_df, session)
    if diet_df is not None:
        load_diet_recommendations(diet_df, session)
    logger.info("ETL terminé.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    data_path = Path(__file__).parent.parent / "data"
    run_etl_to_database(
        food_df=pd.read_csv(data_path / "daily_food_nutrition_dataset.csv", engine="python", on_bad_lines="skip"),
        diet_df=pd.read_csv(data_path / "diet_recommendations_dataset.csv", engine="python", on_bad_lines="skip"),
    )
