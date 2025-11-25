from pydantic import BaseModel
from uuid import UUID, uuid4

class NutritionalValuesRequest(BaseModel):
    id: UUID = uuid4()
    food_id: UUID
    calories: float
    protein: float
    carbohydrates: float
    fat: float
    fiber: float
    sugars: float
    sodium: float
    cholesterol: float