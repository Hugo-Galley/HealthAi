import os
import json
import csv

class FileUtils():

    @staticmethod
    def detect_file_format(filepath: str) -> str:
        # Vérification de l'extension
        extension = os.path.splitext(filepath)[1].lower()
        
        if extension == ".json":
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    json.load(f)
                return print("json - OK")
            except json.JSONDecodeError:
                return print("json invalide")
        
        elif extension == ".csv":
            try:
                with open(filepath, newline="", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    # lecture d'une ligne pour tester
                    next(reader)
                return print("csv - OK")
            except Exception:
                return print("csv invalide")
        
        else:
            return print("Format invalide")
    