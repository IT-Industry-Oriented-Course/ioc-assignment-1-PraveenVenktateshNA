from pydantic import BaseModel
from datetime import date

class PatientSearchInput(BaseModel):
    name: str

class InsuranceCheckInput(BaseModel):
    patient_id: str

class SlotSearchInput(BaseModel):
    specialty: str

class BookAppointmentInput(BaseModel):
    patient_id: str
    specialty: str
    date: date
