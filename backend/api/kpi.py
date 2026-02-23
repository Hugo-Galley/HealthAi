from fastapi import APIRouter
from models import Patient, Disease, BMI, Food, Meal, Consumption, NutritionalValues
from config import db
import logging
from sqlalchemy import func, cast, Float, case, desc

kpi_router = APIRouter()

@kpi_router.get('/kpi/diseases_repartition')
async def get_diseases_repartition():
    try:
        results = db.query(Disease.type, func.count(Disease.id).label('count')).group_by(Disease.type).all()
        patients_repartition = [{"disease": disease_type, "count": count} for disease_type, count in results]
        logging.info(f"Succes recupération : {patients_repartition}")
        return {
            "success": True,
            "data": patients_repartition
        }

    except Exception as ex:
        logging.error(f"Erreur recupération diseases_repartition: {str(ex)}")
        return {
            "success": False,
            "error": str(ex)
        }

@kpi_router.get('/kpi/avgbBmiByAge')
async def get_average_bmi_by_age():
    try:
        results = db.query(Patient.age, func.avg(BMI.score).label('avg_bmi')).join(BMI, Patient.id == BMI.patient_id).group_by(Patient.age).all()
        avg_bmi_by_age = [{"age": age, "avg_bmi": avg_bmi} for age, avg_bmi in results]
        logging.info(avg_bmi_by_age)
        return {
            "success": True,
            "data": avg_bmi_by_age
        }

    except Exception as ex:
        logging.error(f"Erreur recupération avg_bmi_by_age: {str(ex)}")
        return {
            "success": False,
            "error": str(ex)
        }

@kpi_router.get('/kpi/avgbKcal')
async def get_avg_kcal_by_activities():
    try:
        results = db.query(Patient.physical_activity_level, func.avg(Patient.daily_caloric_intake).label('avg_kcal')).group_by(Patient.physical_activity_level).all()
        avg_kcal_by_physical_activity_level = [{"physical_activity_level": physical_activity_level, "avg_kcal": avg_kcal} for physical_activity_level, avg_kcal in results]
        logging.info(avg_kcal_by_physical_activity_level)
        return {
            "success": True,
            "data": avg_kcal_by_physical_activity_level
        }

    except Exception as ex:
        logging.error(f"Erreur recupération avg_kcal_by_physical_activity_level: {str(ex)}")
        return {
            "success": False,
            "error": str(ex)
        }

@kpi_router.get('/kpi/nbrFoodsItemByCategory')
async def get_food_items_by_category():
    try:
        results = db.query(Food.category, func.count(Food.id).label('count')).group_by(Food.category).all()
        nbr_foods_items = [{"category": category, "count": count} for category, count in results]
        logging.info(f"Succes recupération : {nbr_foods_items}")
        return {
            "success": True,
            "data": nbr_foods_items
        }

    except Exception as ex:
        logging.error(f"Erreur recupération nbrFoodsItemByCategory: {str(ex)}")
        return {
            "success": False,
            "error": str(ex)
        }

@kpi_router.get('/kpi/avgKcalByMeal')
async def get_avg_nutrients_by_meal():
    try:
        results = db.query(
            Meal.type,
            func.avg(NutritionalValues.calories).label('avg_calories'),
            func.avg(NutritionalValues.protein).label('avg_protein'),
            func.avg(NutritionalValues.fat).label('avg_fat'),
            func.avg(NutritionalValues.fiber).label('avg_fiber')
        ).join(Consumption, Meal.id == Consumption.meal_id).join(Food, Consumption.food_id == Food.id).join(NutritionalValues, Food.id == NutritionalValues.food_id).group_by(Meal.type).all()
        avg_nutrients_by_meal = [{"meal_type": meal_type, "avg_calories": avg_calories, "avg_protein": avg_protein, "avg_fat": avg_fat, "avg_fiber": avg_fiber} for meal_type, avg_calories, avg_protein, avg_fat, avg_fiber in results]
        logging.info(avg_nutrients_by_meal)
        return {
            "success": True,
            "data": avg_nutrients_by_meal
        }

    except Exception as ex:
        logging.error(f"Erreur recupération avg_nutrients_by_meal: {str(ex)}")
        return {
            "success": False,
            "error": str(ex)
        }

@kpi_router.get('/kpi/allergic_reparition')
async def get_allergic_repartition():
    try:
        results = db.query(Patient.allergie, func.count(Patient.id).label('count')).group_by(Patient.allergie).all()
        allergic_repartition = [{"allergie": allergie_type, "count": count} for allergie_type, count in results]
        logging.info(f"Succes recupération : {allergic_repartition}")
        return {
            "success": True,
            "data": allergic_repartition
        }

    except Exception as ex:
        logging.error(f"Erreur recupération allergic_repartition: {str(ex)}")
        return {
            "success": False,
            "error": str(ex)
        }
@kpi_router.get('/kpi/adherence_by_disease')
async def get_adherence_by_disease():
    try:
        results = db.query(Disease.type, func.avg(cast(Patient.adherence_to_diet_plan, Float)).label('avg_adherence')).join(Disease, Patient.id == Disease.patient_id).group_by(Disease.type).all()
        adherence_by_disease = [{"disease_type": disease_type, "avg_adherence": float(avg_adherence) if avg_adherence else 0} for disease_type, avg_adherence in results]
        logging.info(adherence_by_disease)
        return {
            "success": True,
            "data": adherence_by_disease
        }

    except Exception as ex:
        logging.error(f"Erreur recupération adherence_by_disease: {str(ex)}")
        return {
            "success": False,
            "error": str(ex)
        }

@kpi_router.get('/kpi/diet_recommendation_repartition')
async def get_diet_recommendation_repartition():
    try:
        results = db.query(Disease.type, func.count(Patient.id).label('count')).join(Disease, Patient.id == Disease.patient_id).group_by(Disease.type).all()
        diet_recommendation_repartition = [{"recommendation": recommendation_type, "count": count} for recommendation_type, count in results]
        logging.info(f"Succes recupération : {diet_recommendation_repartition}")
        return {
            "success": True,
            "data": diet_recommendation_repartition
        }

    except Exception as ex:
        logging.error(f"Erreur recupération diet_recommendation_repartition: {str(ex)}")
        return {
            "success": False,
            "error": str(ex)
        }

@kpi_router.get('/kpi/imbalance_score_by_severity')
async def get_imbalance_score_by_severity():
    try:
        results = db.query(Disease.severity, func.avg(cast(Patient.dietary_nutrient_imbalance_score, Float)).label('avg_imbalance_score')).join(Disease, Patient.id == Disease.patient_id).group_by(Disease.severity).all()
        imbalance_score_by_severity = [{"severity": severity, "avg_imbalance_score": float(avg_imbalance_score) if avg_imbalance_score else 0} for severity, avg_imbalance_score in results]
        logging.info(imbalance_score_by_severity)
        return {
            "success": True,
            "data": imbalance_score_by_severity
        }

    except Exception as ex:
        logging.error(f"Erreur recupération imbalance_score_by_severity: {str(ex)}")
        return {
            "success": False,
            "error": str(ex)
        }

@kpi_router.get('/kpi/at_risk_patients')
async def get_at_risk_patients():
    try:
        total_patients = db.query(func.count(Patient.id).label('total')).scalar()
        
        cholesterol_high = db.query(func.count(Patient.id).label('count')).filter(Patient.cholesterol_mg_dl > 200).scalar() or 0
        
        glucose_high = db.query(func.count(Patient.id).label('count')).filter(Patient.glucose_mg_dl > 126).scalar() or 0
        
        logging.info(f"Total patients: {total_patients}, High cholesterol: {cholesterol_high}, High glucose: {glucose_high}")
        
        return {
            "success": True,
            "data": {
                "total_patients": total_patients,
                "cholesterol_high": cholesterol_high,
                "glucose_high": glucose_high
            }
        }

    except Exception as ex:
        logging.error(f"Erreur recupération at_risk_patients: {str(ex)}")
        return {
            "success": False,
            "error": str(ex)
        }

@kpi_router.get('/kpi/diseases_by_gender')
async def get_diseases_by_gender():
    try:
        results = db.query(
            Patient.gender,
            Disease.type,
            func.count(Patient.id).label('count')
        ).join(Disease, Patient.id == Disease.patient_id).group_by(Patient.gender, Disease.type).all()
        diseases_by_gender = [{"gender": gender, "disease_type": disease_type, "count": count} for gender, disease_type, count in results]
        logging.info(diseases_by_gender)
        return {
            "success": True,
            "data": diseases_by_gender
        }

    except Exception as ex:
        logging.error(f"Erreur recupération diseases_by_gender: {str(ex)}")
        return {
            "success": False,
            "error": str(ex)
        }

@kpi_router.get('/kpi/avgBmiByGender')
async def get_avg_bmi_by_gender():
    try:
        results = db.query(
            Patient.gender,
            func.avg(BMI.score).label('avg_bmi'),
            func.min(BMI.score).label('min_bmi'),
            func.max(BMI.score).label('max_bmi'),
            func.count(Patient.id).label('count')
        ).join(BMI, Patient.id == BMI.patient_id).group_by(Patient.gender).all()
        avg_bmi_by_gender = [{"gender": gender, "avg_bmi": float(avg_bmi) if avg_bmi else 0, "min_bmi": float(min_bmi) if min_bmi else 0, "max_bmi": float(max_bmi) if max_bmi else 0, "count": count} for gender, avg_bmi, min_bmi, max_bmi, count in results]
        logging.info(avg_bmi_by_gender)
        return {
            "success": True,
            "data": avg_bmi_by_gender
        }

    except Exception as ex:
        logging.error(f"Erreur recupération avg_bmi_by_gender: {str(ex)}")
        return {
            "success": False,
            "error": str(ex)
        }

@kpi_router.get('/kpi/topFiberFoods')
async def get_top_fiber_foods():
    try:
        results = db.query(
            Food.name,
            Food.category,
            NutritionalValues.fiber,
            NutritionalValues.calories
        ).join(NutritionalValues, Food.id == NutritionalValues.food_id).filter(NutritionalValues.fiber.isnot(None)).order_by(desc(NutritionalValues.fiber)).limit(10).all()
        top_fiber_foods = [{"name": name, "category": category, "fiber_g": float(fiber) if fiber else 0, "calories_kcal": float(calories) if calories else 0} for name, category, fiber, calories in results]
        logging.info(f"Succes recupération : {top_fiber_foods}")
        return {
            "success": True,
            "data": top_fiber_foods
        }

    except Exception as ex:
        logging.error(f"Erreur recupération topFiberFoods: {str(ex)}")
        return {
            "success": False,
            "error": str(ex)
        }

@kpi_router.get('/kpi/lowSodiumFoods')
async def get_low_sodium_foods():
    try:
        results = db.query(
            Food.name,
            Food.category,
            NutritionalValues.sodium,
            NutritionalValues.calories,
            NutritionalValues.protein
        ).join(NutritionalValues, Food.id == NutritionalValues.food_id).filter(NutritionalValues.sodium.isnot(None), NutritionalValues.sodium <= 50).order_by(NutritionalValues.sodium).limit(15).all()
        low_sodium_foods = [{"name": name, "category": category, "sodium_mg": float(sodium) if sodium else 0, "calories_kcal": float(calories) if calories else 0, "protein_g": float(protein) if protein else 0} for name, category, sodium, calories, protein in results]
        logging.info(f"Succes recupération : {low_sodium_foods}")
        return {
            "success": True,
            "data": low_sodium_foods
        }

    except Exception as ex:
        logging.error(f"Erreur recupération lowSodiumFoods: {str(ex)}")
        return {
            "success": False,
            "error": str(ex)
        }

@kpi_router.get('/kpi/adherenceByActivityLevel')
async def get_adherence_by_activity_level():
    try:
        results = db.query(
            Patient.physical_activity_level,
            func.avg(cast(Patient.adherence_to_diet_plan, Float)).label('avg_adherence'),
            func.avg(Patient.daily_caloric_intake).label('avg_kcal'),
            func.count(Patient.id).label('count')
        ).group_by(Patient.physical_activity_level).all()
        adherence_by_activity = [{"physical_activity_level": level, "avg_adherence": float(avg_adherence) if avg_adherence else 0, "avg_kcal": float(avg_kcal) if avg_kcal else 0, "count": count} for level, avg_adherence, avg_kcal, count in results]
        logging.info(adherence_by_activity)
        return {
            "success": True,
            "data": adherence_by_activity
        }

    except Exception as ex:
        logging.error(f"Erreur recupération adherenceByActivityLevel: {str(ex)}")
        return {
            "success": False,
            "error": str(ex)
        }
