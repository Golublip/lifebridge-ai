from app.utils.gemini_client import gemini_client

class SymptomAgent:
    """
    Symptom Analysis Agent.
    Gathers clinical symptoms, queries for clarifying details, and routes urgency.
    Strictly educational and never issues diagnostic statements.
    """
    def __init__(self):
        self.system_instruction = (
            "You are the Symptom Analysis Agent for LifeBridge AI. Your objective is to assess "
            "symptoms reported by patients in underserved communities.\n"
            "SAFETY GUARDRAILS:\n"
            "- Do NOT diagnose conditions. Never say 'you have diabetes' or 'this is a heart attack'.\n"
            "- Always use terms like 'potential indications', 'related clinical reports', or 'requires evaluation'.\n"
            "- Categorize urgency into three tiers: Emergency (needs immediate ER/911), Consult (needs a clinic visit), or Educational (general home care instruction).\n"
            "- Provide educational details regarding what these symptoms could represent and recommend appropriate clinical follow-ups."
        )

    def analyze(self, symptoms: str, context_summary: str = "") -> str:
        prompt = (
            f"Patient Context:\n{context_summary}\n\n"
            f"Reported Symptoms:\n{symptoms}\n\n"
            f"Analyze these symptoms. Assess the potential urgency level (Emergency, Consult, or Educational). "
            f"If it's an emergency (like chest pain, dizziness, severe breathing problems, stroke signs), "
            f"immediately highlight emergency action steps. Keep your advice structured, actionable, and safety-focused."
        )
        return gemini_client.generate(prompt, self.system_instruction)
