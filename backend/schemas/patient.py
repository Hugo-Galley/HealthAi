from pydantic import BaseModel

class PatientRequest(BaseModel):
    id: str
    age: int
    gender: str
    daily_caloric_intake: int
    physical_activity_level: str