from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class UserPreferences(BaseModel):
    language: str = "English"
    favorite_hospitals: List[str] = []

class UserProfile(BaseModel):
    user_id: str = "default_user"
    name: str = "Guest User"
    age: Optional[int] = None
    gender: Optional[str] = None
    location: Optional[str] = None
    allergies: List[str] = []
    medications: List[str] = []
    family_history: List[str] = []
    chronic_conditions: List[str] = []
    preferences: UserPreferences = Field(default_factory=UserPreferences)

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session"
    user_id: str = "default_user"
    location: Optional[str] = None

class ChatResponse(BaseModel):
    session_id: str
    response: str
    plan: List[str] = []
    agents_involved: List[str] = []
    emergency_mode: bool = False
    language: str = "English"
    data: Dict[str, Any] = {}

class Medication(BaseModel):
    id: Optional[int] = None
    name: str
    dosage: str
    frequency: str
    reminders: List[str]  # e.g., ["08:00", "20:00"]
    compliance: Optional[float] = 100.0  # Percentage of doses taken

class MedicationLog(BaseModel):
    medication_id: int
    taken_at: datetime
    status: str  # Taken, Missed

class Appointment(BaseModel):
    id: Optional[int] = None
    doctor_name: str
    hospital_name: str
    date_time: str  # e.g., "2026-07-05 10:00:00"
    purpose: str
    status: str = "Scheduled"

class HealthRecord(BaseModel):
    id: Optional[int] = None
    file_name: str
    file_type: str
    summary: str
    upload_time: str
    parsed_parameters: Dict[str, Any] = {}
