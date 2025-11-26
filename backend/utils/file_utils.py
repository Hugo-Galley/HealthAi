import os
import json
import csv
import logging
import pandas as pd

class FileUtils:

    @staticmethod
    def detect_file_format(filepath: str) -> str:
        # Vérification de l'extension
        extension = os.path.splitext(filepath)[1].lower()
        
        if extension == ".json":
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    json.load(f)
                logging.info("json valide")
                return "json"
            except json.JSONDecodeError:
                raise ValueError("json invalide")
        
        elif extension == ".csv":
            try:
                with open(filepath, newline="", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    # lecture d'une ligne pour tester
                    next(reader)
                logging.info("csv valide")
                return "csv"
            except Exception:
                raise ValueError("csv invalide")
        
        else:
            return print("Format invalide")

    @staticmethod
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
            
    @staticmethod
    def find_non_parse_type(df: pd.DataFrame):
        non_parse = []
        item_type = {
            "Food_Item": "str",
            "Category": "str",
            "Calories (kcal)": "int",
            "Protein (g)": "float",
            "Carbohydrates (g)": "float",
            "Fat (g)": "float",
            "Fiber (g)": "float",
            "Sugars (g)": "float",
            "Sodium (mg)": "float",
            "Cholesterol (mg)": "float",
            "Meal_Type": "str",
            "Water_Intake (ml)": "int"
        }
        for line in range(df.shape[0]):
            for item, intended_type in item_type.items():
                value = df.loc[line, item]
                if value == "" or pd.isna(value):
                    continue
                elif not FileUtils.try_parse_value(value, intended_type):
                    non_parse.append(
                        {"line": line + 1, "field_value": item, "attempt_type": intended_type, "value": value})
        return {"findError": non_parse}


    