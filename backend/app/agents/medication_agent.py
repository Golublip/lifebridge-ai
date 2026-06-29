from app.utils.gemini_client import gemini_client
from app.tools.medicine_checker import MedicineCheckerTool
from app.models.database import get_medications, add_medication, log_medication
from typing import List, Dict, Any

class MedicationAgent:
    """
    Medication Management Agent.
    Schedules reminders, evaluates drug interactions, analyzes adherence metrics, and creates compliance strategies.
    """
    def __init__(self):
        self.checker = MedicineCheckerTool()
        self.system_instruction = (
            "You are the Medication Agent for LifeBridge AI. Your role is to help patients "
            "organize their drug schedules, verify potential interactions, and suggest strategies "
            "to improve medication adherence (like setting alarms or routine mapping)."
        )

    def process(self, action: str, params: Dict[str, Any]) -> str:
        """
        Actions:
        - 'check_interactions': checks a list of medicines
        - 'generate_schedule': returns adherence plan
        - 'compliance_check': returns compliance analysis
        """
        meds = get_medications()
        med_names = [m["name"] for m in meds]
        
        if action == "check_interactions":
            user_meds = params.get("medications", [])
            all_meds = list(set(med_names + user_meds))
            interactions = self.checker.check_interaction(all_meds)
            
            prompt = (
                f"Active Medications: {all_meds}\n"
                f"Found Interactions: {interactions}\n\n"
                f"Explain these interactions to the patient in plain English. State the severity level "
                f"and provide clear, non-alarmist remedies or recommendations."
            )
            return gemini_client.generate(prompt, self.system_instruction)
            
        elif action == "generate_schedule":
            prompt = (
                f"Current Medications List:\n{meds}\n\n"
                f"Create a structured daily medication schedule. Give concrete advice on timing "
                f"(morning, night, with/without food) and propose a reminder strategy to help the patient avoid missed doses."
            )
            return gemini_client.generate(prompt, self.system_instruction)
            
        elif action == "compliance_check":
            prompt = (
                f"Current Medications & Compliance Rates:\n{meds}\n\n"
                f"Analyze this compliance rate. Provide encouragement and recommend behavioral "
                f"techniques (e.g. family text reminders, alarm triggers) to improve adherence."
            )
            return gemini_client.generate(prompt, self.system_instruction)
            
        return "Medication Agent: Action completed."
