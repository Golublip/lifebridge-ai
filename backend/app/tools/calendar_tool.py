from typing import List, Dict, Any
from app.models.database import get_appointments, add_appointment

class CalendarTool:
    """
    Schedules appointments, tracks reminders, and integrates with the backend database.
    """
    def schedule_appointment(self, doctor_name: str, hospital_name: str, date_time: str, purpose: str) -> Dict[str, Any]:
        app_data = {
            "doctor_name": doctor_name,
            "hospital_name": hospital_name,
            "date_time": date_time,
            "purpose": purpose,
            "status": "Scheduled"
        }
        new_id = add_appointment(app_data)
        app_data["id"] = new_id
        return app_data

    def get_upcoming_reminders(self) -> List[Dict[str, Any]]:
        return get_appointments()
