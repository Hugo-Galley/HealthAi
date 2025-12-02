import pandas as pd

from constants.datasets_rules_const import DietRecommendationRulesConst as Cst

def validate_interval(value, min_val, max_val):
    if value < min_val or value > max_val:
        return Cst.interval_rule(min_val, max_val)
    return True

def validate_choice(value, choices):
    if value not in choices:
        return Cst.choice_rule(choices)
    return True

def validate_bmi(value, weight, height):
    height_m = height / 100
    expected_bmi = weight / (height_m ** 2)
    if round(value, 1) != round(expected_bmi, 1):
        return f"L'IMC doit respecter la formule poid/(taille**2): ici taille: {height}, poid: {weight}"
    return True

def validate_disease_type(value, bmi_value):
    if value == "Obesity" and bmi_value < Cst.BMI_OBESITY:
        return f"L'obésité est considérée à partir de 30 d'IMC (IMC actuel: {bmi_value})"
    if value not in Cst.DISEASES_TYPE_CHOICE:
        return Cst.choice_rule(Cst.DISEASES_TYPE_CHOICE)
    return True


def apply_diet_recommendations_rules(df: pd.DataFrame, line, column):
    column_name = df.columns[column]
    value = df.iloc[line, column]

    if pd.isna(value):
        return True

    weight = df.loc[line, "Weight_kg"]
    height = df.loc[line, "Height_cm"]

    if pd.isna(weight) or pd.isna(height):
        return True

    if column_name in Cst.INTERVAL_RULES:
        min_val, max_val = Cst.INTERVAL_RULES[column_name]
        return validate_interval(value, min_val, max_val)

    if column_name in Cst.CHOICE_RULES:
        return validate_choice(value, Cst.CHOICE_RULES[column_name])

    if column_name == "BMI":
        return validate_bmi(value, weight, height)

    if column_name == "Disease_Type":
        bmi_value = df.loc[line, "BMI"]
        return validate_disease_type(value, bmi_value)

    return True

