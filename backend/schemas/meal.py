from pydantic import BaseModel
from uuid import UUID, uuid4

class MealRequest(BaseModel):
    id: UUID = uuid4()
    type: str
    water_intake: float