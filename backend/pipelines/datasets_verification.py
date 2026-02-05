import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pandas as pd

from constants.datasets_rules_const import DietRecommendationRulesConst as CstDiet
from constants.datasets_rules_const import FoodNutritionRulesConst as CstFood
from datasets_rules import apply_recommendations_rules
from etl_database_loader import load_food_nutrition, load_diet_recommendations

def try_parse_value(value, intended_type):
        match intended_type:
            case "int":
                try:
                    int(float(value))
                    return True
                except (ValueError, TypeError):
                    return False
            case "float":
                try:
                    float(value)
                    return True
                except (ValueError, TypeError):
                    return False
            case "str":
                return isinstance(value, str)
            case _:
                return False
            
def find_non_parse_type(df: pd.DataFrame, item_type):
    non_parse = []
    for line in range(df.shape[0]):
        for item, intended_type in item_type.items():
            value = df.loc[line, item]
            if value == "" or pd.isna(value):
                continue
            elif not try_parse_value(value, intended_type):
                non_parse.append(
                    {"line": line + 1, "field_value": item, "attempt_type": intended_type, "value": value})
    return {"findError": non_parse}


def find_inconcienty_field(df: pd.DataFrame):
    inconcienty_field = []
    constants = [CstDiet, CstFood]
    for line in range(df.shape[0]):
        for column in range(df.shape[1]):
            value = df.iloc[line, column]
            if pd.isna(value):
                continue
            if hasattr(value, 'item'):
                value = value.item()
            for constant in constants:
                response = apply_recommendations_rules(df, line, column, constant)
                if isinstance(response, str):
                    inconcienty_field.append(
                        {"line": line, "column": column, "field_value": value, "rule": response}
                    )
                    break
    return inconcienty_field


def save_to_database(df: pd.DataFrame, dataset_type: str, session=None) -> dict:
    if dataset_type == "food_nutrition":
        return load_food_nutrition(df, session)
    elif dataset_type == "diet_recommendations":
        return load_diet_recommendations(df, session)
    raise ValueError(f"Type de dataset inconnu: {dataset_type}")


def run_etl_pipeline(session=None) -> dict:
    data_path = Path(__file__).parent.parent / "data"
    
    food_df = pd.read_csv(data_path / "daily_food_nutrition_dataset.csv")
    diet_df = pd.read_csv(data_path / "diet_recommendations_dataset.csv")
    
    return {
        "food_nutrition": load_food_nutrition(food_df, session),
        "diet_recommendations": load_diet_recommendations(diet_df, session)
    }
