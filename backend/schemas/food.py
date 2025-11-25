from pydantic import BaseModel
from uuid import UUID, uuid4

class FoodRequest(BaseModel):
    id: UUID = uuid4()
    name: str
    category: str