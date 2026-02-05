from fastapi import APIRouter
from models import Patient, Disease, BMI, Food, Meal, Consumption, NutritionalValues
from config import db
import logging
from sqlalchemy import func

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
