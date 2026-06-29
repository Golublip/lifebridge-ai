from typing import Dict, Any, List
from app.models.database import get_user_profile, update_user_profile

class LongTermMemory:
    """
    Manages user profile records including chronic conditions, allergies, medications, and hospital preferences
    """
    def __init__(self, user_id: str = "default_user"):
        self.user_id = user_id

    def get_profile(self) -> Dict[str, Any]:
        return get_user_profile(self.user_id)

    def update_profile(self, profile_data: Dict[str, Any]):
        update_user_profile(profile_data, self.user_id)

    def get_summary(self) -> str:
        """
        Generates a text summary of the long term profile to feed into agent prompts.
        """
        p = self.get_profile()
        if not p:
            return "No health record profile found."
            
        summary = f"Patient Profile: {p.get('name', 'N/A')}\n"
        summary += f"Age/Gender: {p.get('age', 'N/A')} / {p.get('gender', 'N/A')}\n"
        summary += f"Location: {p.get('location', 'N/A')}\n"
        
        allergies = ", ".join(p.get('allergies', []))
        summary += f"Allergies: {allergies if allergies else 'None declared'}\n"
        
        meds = ", ".join(p.get('medications', []))
        summary += f"Active Medications: {meds if meds else 'None'}\n"
        
        history = ", ".join(p.get('family_history', []))
        summary += f"Family History: {history if history else 'None'}\n"
        
        conditions = ", ".join(p.get('chronic_conditions', []))
        summary += f"Chronic Conditions: {conditions if conditions else 'None'}\n"
        
        prefs = p.get('preferences', {})
        hospitals = ", ".join(prefs.get('favorite_hospitals', []))
        summary += f"Favorite Clinics/Hospitals: {hospitals if hospitals else 'None'}\n"
        summary += f"Language Preference: {prefs.get('language', 'English')}"
        
        return summary
