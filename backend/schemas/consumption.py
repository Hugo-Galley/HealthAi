from pydantic import BaseModel
from uuid import UUID, uuid4

class ConsumptionRequest(BaseModel):
    id: UUID = uuid4()
    food_id: UUID
    meal_id: UUID