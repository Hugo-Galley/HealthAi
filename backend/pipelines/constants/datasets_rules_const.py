class DietRecommendationRulesConst:
    AGE_MIN = 18
    AGE_MAX = 100
    GENDER_CHOICE = ["Male", "Female"]
    WEIGHT_MIN = 40
    WEIGHT_MAX = 130
    HEIGHT_MIN = 130
    HEIGHT_MAX = 202
    BMI_OBESITY = 30
    DISEASES_TYPE_CHOICE = ["None", "Obesity", "Diabetes", "Hypertension"]
    SEVERITY_CHOICE = ["Mild", "Moderate", "Severe"]
    PHYSICAL_ACTIVITY_LEVEL_CHOICE = ["Moderate", "Sedentary", "Active"]
    DAILY_KCAL_INTAKE_MIN = 1500
    DAILY_KCAL_INTAKE_MAX = 3500
    CHOLESTEROL_MIN = 150
    CHOLESTEROL_MAX = 250
    BLOOD_PRESURE_MIN = 110
    BLOOD_PRESURE_MAX = 181
    GLUCOSE_MIN = 70
    GLUCOSE_MAX = 201
    DIETARY_RESTRICTIONS_CHOICE = ["Low_Sodium","Low_Sugar", "None"]
    ALLERGIES_CHOICE = ["Gluten", "Peanuts", "None"]
    PREFERED_CUISINE_CHOICE = ["Mexican", "Chinese", "Italian", "Indian"]
    WEEKLY_EXERCISE_HOURS_MIN = 0
    WEEKLY_EXERCISE_HOURS_MAX = 11
    ADHERENCE_DIET_PLAN_MIN = 0
    ADHERENCE_DIET_PLAN_MAX = 100
    DIETARY_NUTRIENT_IMBALANCE_SCORE_MIN = 0
    DIETARY_NUTRIENT_IMBALANCE_SCORE_MAX = 5
    DIET_RECOMMENDATION_CHOICE = ["Balanced", "Low_Carb", "Low_Sodium"]

    INTERVAL_RULES = {
    "Age": (AGE_MIN, AGE_MAX),
    "Weight_kg": (WEIGHT_MIN, WEIGHT_MAX),
    "Height_cm": (HEIGHT_MIN, HEIGHT_MAX),
    "Daily_Caloric_Intake": (DAILY_KCAL_INTAKE_MIN, DAILY_KCAL_INTAKE_MAX),
    "Cholesterol_mg/dL": (CHOLESTEROL_MIN, CHOLESTEROL_MAX),
    "Blood_Pressure_mmHg": (BLOOD_PRESURE_MIN, BLOOD_PRESURE_MAX),
    "Glucose_mg/dL": (GLUCOSE_MIN, GLUCOSE_MAX),
    "Weekly_Exercise_Hours": (WEEKLY_EXERCISE_HOURS_MIN, WEEKLY_EXERCISE_HOURS_MAX),
    "Adherence_to_Diet_Plan": (ADHERENCE_DIET_PLAN_MIN, ADHERENCE_DIET_PLAN_MAX),
    "Dietary_Nutrient_Imbalance_Score": (DIETARY_NUTRIENT_IMBALANCE_SCORE_MIN, DIETARY_NUTRIENT_IMBALANCE_SCORE_MAX)
}

    CHOICE_RULES = {
        "Gender": GENDER_CHOICE,
        "Severity": SEVERITY_CHOICE,
        "Physical_Activity_Level": PHYSICAL_ACTIVITY_LEVEL_CHOICE,
        "Dietary_Restrictions": DIETARY_RESTRICTIONS_CHOICE,
        "Allergies": ALLERGIES_CHOICE,
        "Preferred_Cuisine": PREFERED_CUISINE_CHOICE,
        "Diet_Recommendation": DIET_RECOMMENDATION_CHOICE,
    }

class FoodNutritionRulesConst:
    CATEGORY_CHOICE = ["Beverage", "Beverage/Dairy", "Beverage/Dairy-Alt", "Beverage/Meal", "Condiment", "Condiment/Dairy", "Condiment/Processed", "Dairy", "Dairy/Dessert", "Dessert", "Fruit", "Grain", "Grain/Dessert", "Grain/Processed", "Legume", "Nut", "Protein", "Vegetable"]
    CALORIES_MIN = 0
    CALORIES_MAX = 700
    PROTEIN_MIN = 0
    PROTEIN_MAX = 201
    CARBOHYDRATES_MIN = 0
    CARBOHYDRATES_MAX = 75
    FAT_MIN = 0
    FAT_MAX = 40
    FIBER_MIN = 0
    FIBER_MAX = 14
    SUGAR_MIN = 0
    SUGAR_MAX = 65
    SODIUM_MIN = 0
    SODIUM_MAX = 1600
    CHOLESTEROL_MIN = 0
    CHOLESTEROL_MAX = 460
    MEAL_TYPE = ["Breakfast", "Dinner", "Lunch", "Snack"]
    WATER_INTAKE_MIN = 0
    WATER_INTAKE_MAX = 510

    INTERVAL_RULES = {
        "Calories (kcal)": (CALORIES_MIN, CALORIES_MAX),
        "Protein (g)": (PROTEIN_MIN, PROTEIN_MAX),
        "Carbohydrates (g)": (CARBOHYDRATES_MIN, CARBOHYDRATES_MAX),
        "Fat (g)": (FAT_MIN, FAT_MAX),
        "Fiber (g)": (FIBER_MIN, FIBER_MAX),
        "Sugars (g)": (SUGAR_MIN, SUGAR_MAX),
        "Sodium (mg)": (SODIUM_MIN, SODIUM_MAX),
        "Cholesterol (mg)": (CHOLESTEROL_MIN, CHOLESTEROL_MAX),
        "Water_Intake (ml)": (WATER_INTAKE_MIN, WATER_INTAKE_MAX)
    }

    CHOICE_RULES = {
        "Meal_Type": MEAL_TYPE,
        "Category": CATEGORY_CHOICE
    }

def interval_rule(min_value, max_value):
        return f"La valeur doit être comprise entre {min_value} et {max_value}"

def choice_rule(choice):
    return f"La valeur doit être parmis les choix suivant: {choice}"
