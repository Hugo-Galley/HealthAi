from backend.utils.file_utils import FileUtils
from backend.utils.data_cleaning import DataCleaning
from backend.pipelines.datasets_verification import (find_non_parse_type, find_inconcienty_field)
from backend.pipelines.constants.datasets_verification_const import ITEM_TYPE_DAILY_FOOD_NUTRITION as food_item
from backend.pipelines.constants.datasets_verification_const import ITEM_TYPE_DIET_RECOMMENDATIONS as diet_item
from backend.pipelines.constants.datasets_rules_const import DietRecommendationRulesConst as CstDiet
from backend.pipelines.constants.datasets_rules_const import FoodNutritionRulesConst as CstFood
from backend.pipelines.etl_database_loader import run_etl_to_database
from pathlib import Path
import json
import logging
import pandas as pd

logger = logging.getLogger(__name__)


def _get_invalid_lines(non_parse_errors: list, inconsistency_errors: list) -> set:
    """Récupère les indices de lignes invalides (non-parsables ou incohérentes)."""
    invalid = set()
    for err in non_parse_errors:
        invalid.add(err["line"] - 1)  # find_non_parse_type utilise line+1
    for err in inconsistency_errors:
        invalid.add(err["line"])
    return invalid


class EtlService:

    def run(self):
        data_path = Path(__file__).parent.parent / "data"

        output_path = Path(__file__).parent.parent / "output" / "json"
        output_path.mkdir(parents=True, exist_ok=True)

        # Extract
        FileUtils.detect_file_format(data_path / "daily_food_nutrition_dataset.csv")
        food_df = pd.read_csv(
            data_path / "daily_food_nutrition_dataset.csv",
            engine="python",
            on_bad_lines="skip"
        )

        FileUtils.detect_file_format(data_path / "diet_recommendations_dataset.csv")
        diet_df = pd.read_csv(
            data_path / "diet_recommendations_dataset.csv",
            engine="python",
            on_bad_lines="skip"
        )

        # Transform
        food_deduped = DataCleaning.remove_duplicates(food_df)
        food_normalized_basic = find_non_parse_type(food_deduped, food_item)
        food_normalized_final = find_inconcienty_field(food_deduped, CstFood)

        diet_deduped = DataCleaning.remove_duplicates(diet_df)
        diet_normalized_basic = find_non_parse_type(diet_deduped, diet_item)
        diet_normalized_final = find_inconcienty_field(diet_deduped, CstDiet)

        # Sauvegarde des données faussées dans des JSON
        non_parse_food = food_normalized_basic["findError"]
        with open(output_path / "non_parse_food.json", "w", encoding="utf-8") as f:
            json.dump(non_parse_food, f, indent=4, ensure_ascii=False)

        with open(output_path / "inconsistent_food.json", "w", encoding="utf-8") as f:
            json.dump(food_normalized_final, f, indent=4, ensure_ascii=False)

        non_parse_diet = diet_normalized_basic["findError"]
        with open(output_path / "non_parse_diet.json", "w", encoding="utf-8") as f:
            json.dump(non_parse_diet, f, indent=4, ensure_ascii=False)

        with open(output_path / "inconsistent_diet.json", "w", encoding="utf-8") as f:
            json.dump(diet_normalized_final, f, indent=4, ensure_ascii=False)

        # Filtrage des lignes invalides avant insertion en BDD
        food_invalid_lines = _get_invalid_lines(non_parse_food, food_normalized_final)
        diet_invalid_lines = _get_invalid_lines(non_parse_diet, diet_normalized_final)

        food_final_df = food_deduped.drop(index=list(food_invalid_lines), errors='ignore').reset_index(drop=True)
        diet_final_df = diet_deduped.drop(index=list(diet_invalid_lines), errors='ignore').reset_index(drop=True)

        logger.info(f"Food : {len(food_invalid_lines)} lignes invalides retirées, {len(food_final_df)} lignes à insérer")
        logger.info(f"Diet : {len(diet_invalid_lines)} lignes invalides retirées, {len(diet_final_df)} lignes à insérer")

        # ── Load ──
        logger.info("Début du chargement en base de données...")
        results = run_etl_to_database(food_final_df, diet_final_df)
        logger.info(f"Résultats du chargement : {results}")

        return results


if __name__ == "__main__":
    etl = EtlService()
    etl.run()