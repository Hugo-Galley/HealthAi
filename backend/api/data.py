import logging
from pathlib import Path

import pandas as pd
from fastapi import APIRouter

from config import db
from models import Patient
from backend.pipelines.constants.datasets_rules_const import (
    DietRecommendationRulesConst as CstDiet,
    FoodNutritionRulesConst as CstFood,
)
from backend.pipelines.constants.datasets_verification_const import (
    ITEM_TYPE_DAILY_FOOD_NUTRITION as food_item,
    ITEM_TYPE_DIET_RECOMMENDATIONS as diet_item,
)
from backend.pipelines.datasets_verification import find_inconcienty_field, find_non_parse_type
from backend.utils.data_cleaning import DataCleaning

data_router = APIRouter()

_DATA_PATH = Path(__file__).parent.parent / "data"


@data_router.get("/users")
async def get_users():
    try:
        patients = db.query(Patient).all()
        users = [
            {
                "id": p.id,
                "name": None,
                "email": None,
                "status": p.physical_activity_level,
            }
            for p in patients
        ]
        return {"success": True, "data": users}
    except Exception as ex:
        logging.error(f"Erreur récupération users: {ex}")
        return {"success": False, "error": str(ex)}


@data_router.get("/activities")
async def get_activities():
    try:
        patients = db.query(Patient).all()
        activities = [
            {
                "user": p.id,
                "type": p.physical_activity_level,
                "duration_min": None,
                "distance_km": None,
            }
            for p in patients
            if p.physical_activity_level
        ]
        return {"success": True, "data": activities}
    except Exception as ex:
        logging.error(f"Erreur récupération activities: {ex}")
        return {"success": False, "error": str(ex)}


@data_router.get("/admin/flagged-data")
async def get_flagged_data():
    try:
        food_df = pd.read_csv(_DATA_PATH / "daily_food_nutrition_dataset.csv", engine="python", on_bad_lines="skip")
        diet_df = pd.read_csv(_DATA_PATH / "diet_recommendations_dataset.csv", engine="python", on_bad_lines="skip")

        food_deduped = DataCleaning.remove_duplicates(food_df)
        diet_deduped = DataCleaning.remove_duplicates(diet_df)

        food_non_parse = find_non_parse_type(food_deduped, food_item)["findError"]
        food_inconsistent = find_inconcienty_field(food_deduped, CstFood)
        diet_non_parse = find_non_parse_type(diet_deduped, diet_item)["findError"]
        diet_inconsistent = find_inconcienty_field(diet_deduped, CstDiet)

        flagged = []
        for err in food_non_parse:
            flagged.append({
                "id": err["line"],
                "type": "food",
                "value": str(err["value"]),
                "unit": err["attempt_type"],
                "flag_reason": f"Type non parseable pour {err['field_value']}",
                "status": "flagged",
                "is_anomaly": True,
            })
        for err in food_inconsistent:
            flagged.append({
                "id": err["line"],
                "type": "food",
                "value": str(err["field_value"]),
                "unit": "",
                "flag_reason": err["rule"],
                "status": "flagged",
                "is_anomaly": True,
            })
        for err in diet_non_parse:
            flagged.append({
                "id": err["line"],
                "type": "diet",
                "value": str(err["value"]),
                "unit": err["attempt_type"],
                "flag_reason": f"Type non parseable pour {err['field_value']}",
                "status": "flagged",
                "is_anomaly": True,
            })
        for err in diet_inconsistent:
            flagged.append({
                "id": err["line"],
                "type": "diet",
                "value": str(err["field_value"]),
                "unit": "",
                "flag_reason": err["rule"],
                "status": "flagged",
                "is_anomaly": True,
            })

        return {"success": True, "data": flagged}
    except Exception as ex:
        logging.error(f"Erreur récupération flagged data: {ex}")
        return {"success": False, "error": str(ex)}
