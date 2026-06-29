from app.utils.gemini_client import gemini_client
from app.tools.hospital_search import HospitalSearchTool
from app.tools.health_scheme_tool import HealthSchemeTool
from typing import Dict, Any

class HospitalAgent:
    """
    Hospital Navigation Agent.
    Searches for clinics, compares fees, links visits to health programs, and calculates distances.
    """
    def __init__(self):
        self.search_tool = HospitalSearchTool()
        self.scheme_tool = HealthSchemeTool()
        self.system_instruction = (
            "You are the Hospital Navigation Agent for LifeBridge AI. Your objective is to help patients "
            "locate low-cost or free clinics/hospitals, calculate distances, and recommend government schemes "
            "like Medicaid or local sliding-scale fee assistance programs to cover expenses."
        )

    def locate_care(self, zip_code: str, patient_conditions: list = None, max_cost: float = None) -> str:
        clinics = self.search_tool.search_clinics(zip_code, max_cost=max_cost)
        schemes = self.scheme_tool.check_schemes("US", chronic_conditions=patient_conditions)
        
        prompt = (
            f"Patient Location Zip Code: {zip_code}\n"
            f"Found Nearby Clinics/Hospitals:\n{clinics}\n"
            f"Matching Government Support Schemes:\n{schemes}\n\n"
            f"Summarize these findings for the patient. List the nearest clinics first. Highlight estimated "
            f"consultation costs, phone numbers, and which schemes (like Medicaid or Sliding-Scale fee charts) "
            f"can be utilized to reduce or eliminate payments."
        )
        return gemini_client.generate(prompt, self.system_instruction)
