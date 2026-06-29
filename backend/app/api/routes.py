from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from app.models.schemas import ChatRequest, ChatResponse, UserProfile, Medication, Appointment
from app.models.database import (
    get_user_profile, update_user_profile, get_medications, add_medication, 
    delete_medication, log_medication, get_appointments, add_appointment,
    get_health_records, add_health_record
)
from app.agents.orchestrator import MasterOrchestrator
from app.agents.health_records_agent import HealthRecordsAgent
from datetime import datetime
import os
import shutil
from typing import List, Dict, Any

router = APIRouter()
records_agent = HealthRecordsAgent()

# Chat Route
@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        orchestrator = MasterOrchestrator(session_id=request.session_id, user_id=request.user_id)
        result = orchestrator.route_and_solve(request.message, request.location)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Orchestration Error: {str(e)}")

# Profile Routes
@router.get("/profile", response_model=UserProfile)
async def get_profile(user_id: str = "default_user"):
    profile = get_user_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return UserProfile(**profile)

@router.put("/profile")
async def update_profile(profile: UserProfile):
    try:
        update_user_profile(profile.model_dump(), profile.user_id)
        return {"status": "success", "message": "Profile updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Medication Routes
@router.get("/medications", response_model=List[Medication])
async def list_meds():
    meds = get_medications()
    return [Medication(**m) for m in meds]

@router.post("/medications", response_model=Dict[str, Any])
async def create_med(med: Medication):
    try:
        new_id = add_medication(med.model_dump())
        return {"status": "success", "id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/medications/{med_id}")
async def remove_med(med_id: int):
    try:
        delete_medication(med_id)
        return {"status": "success", "message": f"Medication {med_id} deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/medications/{med_id}/log")
async def log_med_intake(med_id: int, status: str):
    if status not in ["Taken", "Missed"]:
        raise HTTPException(status_code=400, detail="Invalid status. Must be Taken or Missed")
    try:
        log_medication(med_id, status)
        return {"status": "success", "message": f"Medication {med_id} logged as {status}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Appointment Routes
@router.get("/appointments", response_model=List[Appointment])
async def list_appointments():
    apps = get_appointments()
    return [Appointment(**a) for a in apps]

@router.post("/appointments", response_model=Dict[str, Any])
async def create_appointment(app: Appointment):
    try:
        new_id = add_appointment(app.model_dump())
        return {"status": "success", "id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health Record Upload Route
@router.get("/records")
async def list_records():
    return get_health_records()

@router.post("/records/upload")
async def upload_record(file: UploadFile = File(...)):
    # Set upload directory
    upload_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "uploads"))
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = os.path.join(upload_dir, file.filename)
    
    try:
        # Save file to uploads
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Parse document via health records agent (OCR + LLM)
        analysis = records_agent.process_record(file_path)
        
        # Save to database
        record_db_data = {
            "file_name": file.filename,
            "file_type": file.content_type or "unknown",
            "summary": analysis["summary"],
            "upload_time": datetime.now().isoformat(),
            "parsed_parameters": analysis["parsed_parameters"]
        }
        
        new_id = add_health_record(record_db_data)
        record_db_data["id"] = new_id
        
        return {
            "status": "success",
            "record": record_db_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload processing failed: {str(e)}")

# Emergency Trigger Route
@router.post("/emergency/trigger")
async def trigger_emergency(symptoms: str = Form(...), zip_code: str = Form("43001")):
    try:
        orchestrator = MasterOrchestrator(session_id="emergency_session", user_id="default_user")
        result = orchestrator.route_and_solve(symptoms, zip_code)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
