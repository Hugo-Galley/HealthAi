# KPI - Health AI Platform

## Données disponibles

### Dataset 1 : `daily_food_nutrition_dataset.csv` (651 aliments)
| Colonne | Description |
|---------|-------------|
| Food_Item | Nom de l'aliment |
| Category | Catégorie (Protein/Dairy, Grain, Fruit, Vegetable, Meal, etc.) |
| Calories (kcal) | Apport calorique |
| Protein (g) | Protéines |
| Carbohydrates (g) | Glucides |
| Fat (g) | Lipides |
| Fiber (g) | Fibres |
| Sugars (g) | Sucres |
| Sodium (mg) | Sodium |
| Cholesterol (mg) | Cholestérol |
| Meal_Type | Type de repas (Breakfast, Lunch, Dinner, Snack) |
| Water_Intake (ml) | Apport en eau |

### Dataset 2 : `diet_recommendations_dataset.csv` (1001 patients)
| Colonne | Description |
|---------|-------------|
| Patient_ID | Identifiant patient |
| Age | Âge |
| Gender | Sexe (Male/Female) |
| Weight_kg | Poids en kg |
| Height_cm | Taille en cm |
| BMI | Indice de Masse Corporelle |
| Disease_Type | Maladie (Diabetes, Obesity, Hypertension, None) |
| Severity | Sévérité (Mild, Moderate, Severe) |
| Physical_Activity_Level | Niveau d'activité (Sedentary, Moderate, Active) |
| Daily_Caloric_Intake | Apport calorique journalier |
| Cholesterol_mg/dL | Taux de cholestérol sanguin |
| Blood_Pressure_mmHg | Tension artérielle |
| Glucose_mg/dL | Glycémie |
| Dietary_Restrictions | Restrictions (None, Low_Sugar, Low_Sodium) |
| Allergies | Allergies (None, Peanuts, Gluten) |
| Preferred_Cuisine | Cuisine préférée (Mexican, Chinese, Italian, Indian) |
| Weekly_Exercise_Hours | Heures d'exercice/semaine |
| Adherence_to_Diet_Plan | Adhérence au régime (%) |
| Dietary_Nutrient_Imbalance_Score | Score de déséquilibre (0-5) |
| Diet_Recommendation | Régime recommandé (Balanced, Low_Carb, Low_Sodium) |

---

## 10 KPI Exploitables via l'API

### KPI 1 : Répartition des patients par type de maladie
**Source :** `diet_recommendations_dataset.csv`  
**Calcul :** `COUNT(Patient_ID) GROUP BY Disease_Type`  
**Exemple de retour :**
```json
{
  "Diabetes": 245,
  "Obesity": 312,
  "Hypertension": 198,
  "None": 246
}
```

---

### KPI 2 : BMI moyen par tranche d'âge
**Source :** `diet_recommendations_dataset.csv`  
**Calcul :** `AVG(BMI) GROUP BY tranche_age` (18-30, 31-50, 51-70, 70+)  
**Exemple de retour :**
```json
{
  "18-30": 26.4,
  "31-50": 28.1,
  "51-70": 27.8,
  "70+": 29.2
}
```

---

### KPI 3 : Taux d'adhérence moyen au régime par type de maladie
**Source :** `diet_recommendations_dataset.csv`  
**Calcul :** `AVG(Adherence_to_Diet_Plan) GROUP BY Disease_Type`  
**Exemple de retour :**
```json
{
  "Diabetes": 68.5,
  "Obesity": 71.2,
  "Hypertension": 74.1,
  "None": 69.8
}
```

---

### KPI 4 : Répartition des régimes recommandés
**Source :** `diet_recommendations_dataset.csv`  
**Calcul :** `COUNT(Patient_ID) GROUP BY Diet_Recommendation`  
**Exemple de retour :**
```json
{
  "Balanced": 520,
  "Low_Carb": 285,
  "Low_Sodium": 196
}
```

---

### KPI 5 : Apport calorique moyen par niveau d'activité physique
**Source :** `diet_recommendations_dataset.csv`  
**Calcul :** `AVG(Daily_Caloric_Intake) GROUP BY Physical_Activity_Level`  
**Exemple de retour :**
```json
{
  "Sedentary": 2350,
  "Moderate": 2580,
  "Active": 2720
}
```

---

### KPI 6 : Score de déséquilibre nutritionnel moyen par sévérité de maladie
**Source :** `diet_recommendations_dataset.csv`  
**Calcul :** `AVG(Dietary_Nutrient_Imbalance_Score) GROUP BY Severity`  
**Exemple de retour :**
```json
{
  "Mild": 2.1,
  "Moderate": 2.8,
  "Severe": 3.4
}
```

---

### KPI 7 : Nombre d'aliments disponibles par catégorie
**Source :** `daily_food_nutrition_dataset.csv`  
**Calcul :** `COUNT(Food_Item) GROUP BY Category`  
**Exemple de retour :**
```json
{
  "Protein/Dairy": 85,
  "Grain": 72,
  "Fruit": 65,
  "Vegetable": 58,
  "Meal/Processed": 120,
  "Beverage": 45
}
```

---

### KPI 8 : Valeurs nutritionnelles moyennes par type de repas
**Source :** `daily_food_nutrition_dataset.csv`  
**Calcul :** `AVG(Calories, Protein, Fat, Fiber) GROUP BY Meal_Type`  
**Exemple de retour :**
```json
{
  "Breakfast": {"calories": 180, "protein": 8.5, "fat": 6.2, "fiber": 2.1},
  "Lunch": {"calories": 320, "protein": 18.0, "fat": 12.5, "fiber": 4.5},
  "Dinner": {"calories": 380, "protein": 22.0, "fat": 15.0, "fiber": 3.8},
  "Snack": {"calories": 150, "protein": 5.0, "fat": 7.0, "fiber": 1.5}
}
```

---

### KPI 9 : Répartition des allergies dans la population
**Source :** `diet_recommendations_dataset.csv`  
**Calcul :** `COUNT(Patient_ID) GROUP BY Allergies`  
**Exemple de retour :**
```json
{
  "None": 412,
  "Peanuts": 298,
  "Gluten": 291
}
```

---

### KPI 10 : Patients à risque (biomarqueurs élevés)
**Source :** `diet_recommendations_dataset.csv`  
**Calcul :** 
- Cholestérol élevé : `COUNT WHERE Cholesterol_mg/dL > 200`
- Tension élevée : `COUNT WHERE Blood_Pressure_mmHg > 140`
- Glycémie élevée : `COUNT WHERE Glucose_mg/dL > 126`

**Exemple de retour :**
```json
{
  "cholesterol_eleve": 342,
  "tension_elevee": 285,
  "glycemie_elevee": 198,
  "total_patients": 1001
}
```

---

### KPI 11 : Répartition des maladies par genre
**Source :** `diet_recommendations_dataset.csv`  
**Calcul :** `COUNT(Patient_ID) GROUP BY Gender, Disease_Type`  
**Endpoint :** `GET /kpi/diseases_by_gender`  
**Exemple de retour :**
```json
[
  {"gender": "Male", "disease_type": "Diabetes", "count": 130},
  {"gender": "Male", "disease_type": "Obesity", "count": 155},
  {"gender": "Female", "disease_type": "Diabetes", "count": 115},
  {"gender": "Female", "disease_type": "Hypertension", "count": 102}
]
```

---

### KPI 12 : BMI moyen par genre (avec min/max)
**Source :** `diet_recommendations_dataset.csv`  
**Calcul :** `AVG(BMI), MIN(BMI), MAX(BMI), COUNT(Patient_ID) GROUP BY Gender`  
**Endpoint :** `GET /kpi/avgBmiByGender`  
**Exemple de retour :**
```json
[
  {"gender": "Male", "avg_bmi": 27.5, "min_bmi": 18.2, "max_bmi": 42.1, "count": 510},
  {"gender": "Female", "avg_bmi": 26.8, "min_bmi": 17.9, "max_bmi": 39.5, "count": 491}
]
```

---

### KPI 13 : Top 10 aliments les plus riches en fibres
**Source :** `daily_food_nutrition_dataset.csv`  
**Calcul :** `SELECT Food_Item, Category, Fiber, Calories ORDER BY Fiber DESC LIMIT 10`  
**Endpoint :** `GET /kpi/topFiberFoods`  
**Exemple de retour :**
```json
[
  {"name": "Lentils", "category": "Grain", "fiber_g": 15.6, "calories_kcal": 230},
  {"name": "Artichoke", "category": "Vegetable", "fiber_g": 10.3, "calories_kcal": 47},
  {"name": "Chia Seeds", "category": "Protein/Dairy", "fiber_g": 9.8, "calories_kcal": 138}
]
```

---

### KPI 14 : Aliments à faible sodium (≤ 50 mg) pour patients hypertendus
**Source :** `daily_food_nutrition_dataset.csv`  
**Calcul :** `SELECT Food_Item, Category, Sodium, Calories, Protein WHERE Sodium <= 50 ORDER BY Sodium LIMIT 15`  
**Endpoint :** `GET /kpi/lowSodiumFoods`  
**Exemple de retour :**
```json
[
  {"name": "Apple", "category": "Fruit", "sodium_mg": 1.0, "calories_kcal": 52, "protein_g": 0.3},
  {"name": "Banana", "category": "Fruit", "sodium_mg": 1.0, "calories_kcal": 89, "protein_g": 1.1},
  {"name": "Rice", "category": "Grain", "sodium_mg": 5.0, "calories_kcal": 130, "protein_g": 2.7}
]
```

---

### KPI 15 : Corrélation activité physique / adhérence au régime
**Source :** `diet_recommendations_dataset.csv`  
**Calcul :** `AVG(Adherence_to_Diet_Plan), AVG(Daily_Caloric_Intake), COUNT(Patient_ID) GROUP BY Physical_Activity_Level`  
**Endpoint :** `GET /kpi/adherenceByActivityLevel`  
**Exemple de retour :**
```json
[
  {"physical_activity_level": "Sedentary", "avg_adherence": 62.3, "avg_kcal": 2350, "count": 340},
  {"physical_activity_level": "Moderate", "avg_adherence": 71.5, "avg_kcal": 2580, "count": 345},
  {"physical_activity_level": "Active", "avg_adherence": 78.9, "avg_kcal": 2720, "count": 316}
]
```

