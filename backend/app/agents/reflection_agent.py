from app.utils.gemini_client import gemini_client
from typing import Dict, Any

class ReflectionAgent:
    """
    Reflection Agent.
    Critiques agent outputs to enforce safety policies, verify medical safety constraints,
    ensure alignment with patient preferences, and correct hallucinations.
    """
    def __init__(self):
        self.system_instruction = (
            "You are the Reflection Agent for LifeBridge AI. Your objective is internal quality control "
            "and patient safety. You analyze proposed assistant answers against clinical safety rules:\n"
            "1. NO DIAGNOSIS: The response must never claim the patient has a specific condition.\n"
            "2. ALLERGY CHECK: Verify that no recommended medications or elements trigger listed patient allergies.\n"
            "3. EMERGENCY TRIAGE: If symptoms suggest acute cardiac/stroke issues, the response MUST feature immediate emergency escalation.\n"
            "4. EMOTIONAL SUPPORT: Ensure mental health queries feature safety disclaimers.\n\n"
            "If the response is fully safe, output: 'STATUS: APPROVED'.\n"
            "If the response fails safety constraints, rewrite the response to correct the issues and output: 'STATUS: REVISED\n[Revised Content]'."
        )

    def critique(self, proposed_response: str, user_profile: Dict[str, Any], user_message: str) -> str:
        prompt = (
            f"User Profile:\n{user_profile}\n\n"
            f"User Query:\n\"{user_message}\"\n\n"
            f"Proposed Assistant Response:\n\"\"\"{proposed_response}\"\"\"\n\n"
            f"Evaluate the proposed response. Check for safety, diagnosis violations, allergy triggers, or "
            f"missing emergency warnings. Output 'STATUS: APPROVED' or supply a safe revised version."
        )
        return gemini_client.generate(prompt, self.system_instruction)
