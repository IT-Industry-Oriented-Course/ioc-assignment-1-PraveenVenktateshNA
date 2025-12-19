import requests
from agent.schemas import (
    PatientSearchInput,
    InsuranceCheckInput,
    SlotSearchInput,
    BookAppointmentInput
)

BASE_URL = "http://127.0.0.1:8000"

def search_patient(data: PatientSearchInput):
    r = requests.get(f"{BASE_URL}/patients/search", params=data)
    r.raise_for_status()
    return r.json()

def check_insurance_eligibility(data: InsuranceCheckInput):
    r = requests.get(f"{BASE_URL}/insurance/check", params=data)
    r.raise_for_status()
    return r.json()

def find_available_slots(data: SlotSearchInput):
    r = requests.get(f"{BASE_URL}/appointments/slots", params=data)
    r.raise_for_status()
    return r.json()

def book_appointment(data: BookAppointmentInput):
    r = requests.post(f"{BASE_URL}/appointments/book", params=data)
    r.raise_for_status()
    return r.json()
