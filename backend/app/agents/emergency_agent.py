from app.utils.gemini_client import gemini_client
from app.tools.hospital_search import HospitalSearchTool
from typing import Dict, Any

class EmergencyAgent:
    """
    Emergency Response Agent.
    Identifies high-urgency health scenarios (e.g., chest pain, breathing arrest, stroke signs)
    and formats instant, clear first-aid instructions, local dispatch details, and emergency room links.
    """
    def __init__(self):
        self.search_tool = HospitalSearchTool()
        self.system_instruction = (
            "You are the Emergency Agent for LifeBridge AI. Your sole focus is patient stabilization "
            "and immediate emergency action. You write in clear, bold, urgent, and highly structured language. "
            "Your output must start with an emergency header, followed by immediate first-aid instructions, "
            "emergency phone numbers (e.g., 911), and a list of nearby hospitals with 24/7 Emergency Rooms."
        )

    def trigger_emergency(self, symptoms: str, zip_code: str = "43001") -> str:
        hospitals = self.search_tool.search_clinics(zip_code, require_emergency=True)
        # Filter for General Hospital style ERs
        er_rooms = [h for h in hospitals if h["emergency_services"]][:2]
        
        prompt = (
            f"Urgent Symptoms: {symptoms}\n"
            f"Patient Location Zip Code: {zip_code}\n"
            f"Available Emergency Rooms:\n{er_rooms}\n\n"
            f"Generate an immediate emergency response directive. Provide step-by-step first-aid guidance "
            f"(e.g., for suspected heart attack, stroke, or breathing issues). State emergency contacts clearly, "
            f"and list the coordinates/details of the nearest Emergency Rooms."
        )
        return gemini_client.generate(prompt, self.system_instruction)
