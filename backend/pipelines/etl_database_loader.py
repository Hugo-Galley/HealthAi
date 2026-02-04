import sys
from pathlib import Path
from uuid import uuid4

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import db
from models import Food, NutritionalValues, Meal, Consumption, Patient, BMI, Disease


def _safe_float(value):
    try:
        return None if pd.isna(value) else float(value)
    except (ValueError, TypeError):
        return None


def _safe_int(value):
    try:
        return None if pd.isna(value) else int(float(value))
    except (ValueError, TypeError):
        return None


def load_food_nutrition(df: pd.DataFrame, session=None) -> dict:
    session = session or db
    stats = {"foods": 0, "meals": 0, "errors": []}
    food_cache = {}

    for idx, row in df.iterrows():
        try:
            key = f"{row.get('Food_Item')}_{row.get('Category')}"
            if key not in food_cache:
                food = Food(id=str(uuid4()), name=row.get('Food_Item', ''), category=row.get('Category', ''))
                session.add(food)
                session.flush()
                food_cache[key] = food
                stats["foods"] += 1
            else:
                food = food_cache[key]

            session.add(NutritionalValues(
                id=str(uuid4()), food_id=food.id,
                calories=_safe_float(row.get('Calories (kcal)')),
                protein=_safe_float(row.get('Protein (g)')),
                carbohydrates=_safe_float(row.get('Carbohydrates (g)')),
                fat=_safe_float(row.get('Fat (g)')),
                fiber=_safe_float(row.get('Fiber (g)')),
                sugars=_safe_float(row.get('Sugars (g)')),
                sodium=_safe_float(row.get('Sodium (mg)')),
                cholesterol=_safe_float(row.get('Cholesterol (mg)'))
            ))

            meal = Meal(id=str(uuid4()), type=row.get('Meal_Type', ''), 
                        water_intake=_safe_float(row.get('Water_Intake (ml)')))
            session.add(meal)
            session.flush()
            session.add(Consumption(id=str(uuid4()), food_id=food.id, meal_id=meal.id))
            stats["meals"] += 1

        except Exception as e:
            stats["errors"].append(f"Ligne {idx}: {e}")

    session.commit()
    return stats


def load_diet_recommendations(df: pd.DataFrame, session=None) -> dict:
    session = session or db
    stats = {"patients": 0, "diseases": 0, "errors": []}
    patient_cache = {}

    for idx, row in df.iterrows():
        try:
            patient_id = row.get('Patient_ID', '')
            
            if patient_id not in patient_cache:
                patient = Patient(
                    id=patient_id, age=_safe_int(row.get('Age')) or 0,
                    gender=row.get('Gender', ''),
                    daily_caloric_intake=_safe_int(row.get('Daily_Caloric_Intake')),
                    physical_activity_level=row.get('Physical_Activity_Level', '')
                )
                session.add(patient)
                session.flush()
                patient_cache[patient_id] = patient
                stats["patients"] += 1

            session.add(BMI(
                id=str(uuid4()), patient_id=patient_id,
                weight=_safe_float(row.get('Weight_kg')) or 0.0,
                height=_safe_float(row.get('Height_cm')) or 0.0,
                score=_safe_float(row.get('BMI'))
            ))

            disease_type = row.get('Disease_Type', '')
            severity = row.get('Severity', '')
            
            if pd.notna(disease_type) and disease_type and disease_type != 'None':
                disease_type = str(disease_type)
                severity = str(severity) if pd.notna(severity) else None
                session.add(Disease(
                    id=str(uuid4()), patient_id=patient_id,
                    type=disease_type, severity=severity
                ))
                stats["diseases"] += 1

        except Exception as e:
            stats["errors"].append(f"Ligne {idx}: {e}")
            session.rollback()

    session.commit()
    return stats


def run_etl_to_database(food_df: pd.DataFrame = None, diet_df: pd.DataFrame = None, session=None) -> dict:
    """Exécute le chargement ETL complet vers la BDD."""
    return {
        "food_nutrition": load_food_nutrition(food_df, session) if food_df is not None else None,
        "diet_recommendations": load_diet_recommendations(diet_df, session) if diet_df is not None else None
    }


if __name__ == "__main__":
    data_path = Path(__file__).parent.parent / "data"
    results = run_etl_to_database(
        food_df=pd.read_csv(data_path / "daily_food_nutrition_dataset.csv"),
        diet_df=pd.read_csv(data_path / "diet_recommendations_dataset.csv")
    )
    print(f"Résultats: {results}")
