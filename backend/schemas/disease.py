from pydantic import BaseModel
from uuid import UUID, uuid4

class DiseaseRequest(BaseModel):
    id: UUID = uuid4()
    patient_id: str
    type: str
    severity: str