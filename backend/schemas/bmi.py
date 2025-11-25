from pydantic import BaseModel
from uuid import UUID, uuid4

class BmiResquest(BaseModel):
    id: UUID = uuid4()
    patient_id: str
    height: float
    weight: float
    score: float