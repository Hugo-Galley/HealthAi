import os
import json
import csv
import logging

class FileUtils():

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
    