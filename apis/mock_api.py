from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import date, timedelta
import uuid

app = FastAPI(title="Mock Healthcare API")

# ---------- Models ----------

class Patient(BaseModel):
    patient_id: str
    name: str

class InsuranceStatus(BaseModel):
    patient_id: str
    eligible: bool

class Slot(BaseModel):
    slot_id: str
    specialty: str
    date: date

class Appointment(BaseModel):
    appointment_id: str
    patient_id: str
    specialty: str
    date: date
    status: str

# ---------- Fake Databases ----------

PATIENT_DB = {
    "Ravi Kumar": "P-1001",
    "Anita Sharma": "P-1002"
}

INSURANCE_DB = {
    "P-1001": True,
    "P-1002": False
}

# ---------- Endpoints ----------

@app.get("/patients/search", response_model=Patient)
def search_patient(name: str):
    if name not in PATIENT_DB:
        raise HTTPException(status_code=404, detail="Patient not found")
    return Patient(patient_id=PATIENT_DB[name], name=name)


@app.get("/insurance/check", response_model=InsuranceStatus)
def check_insurance(patient_id: str):
    if patient_id not in INSURANCE_DB:
        raise HTTPException(status_code=404, detail="Insurance record not found")
    return InsuranceStatus(patient_id=patient_id, eligible=INSURANCE_DB[patient_id])


@app.get("/appointments/slots", response_model=List[Slot])
def find_slots(specialty: str):
    today = date.today()
    return [
        Slot(
            slot_id=str(uuid.uuid4()),
            specialty=specialty,
            date=today + timedelta(days=i)
        )
        for i in range(1, 6)
    ]


@app.post("/appointments/book", response_model=Appointment)
def book_appointment(patient_id: str, specialty: str, date: date):
    return Appointment(
        appointment_id=str(uuid.uuid4()),
        patient_id=patient_id,
        specialty=specialty,
        date=date,
        status="CONFIRMED"
    )
