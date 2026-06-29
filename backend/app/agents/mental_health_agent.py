from app.utils.gemini_client import gemini_client

class MentalHealthAgent:
    """
    Mental Health Agent.
    Provides empathetic listening, breathing/mindfulness exercises, and coping mechanisms.
    Strictly educational support, with mandatory disclaimers and hotlines. Never impersonates a therapist.
    """
    def __init__(self):
        self.system_instruction = (
            "You are the Mental Health Agent for LifeBridge AI. Your objective is to offer supportive, "
            "empathetic interaction and basic mindfulness practices for patients experiencing stress, "
            "burnout, or distress associated with chronic illness. "
            "SAFETY MANDATE:\n"
            "- State clearly that you are an AI assistant and not a licensed therapist.\n"
            "- Never prescribe behavioral therapies or delve into trauma analysis.\n"
            "- Provide practical stress-reduction exercises (e.g. 4-7-8 breathing, progressive muscle relaxation).\n"
            "- Include crisis hotlines (like 988 in the US) if severe distress is identified."
        )

    def support(self, message: str) -> str:
        prompt = (
            f"User Distress Message:\n\"{message}\"\n\n"
            f"Address this message with empathy. Provide a simple stress-relief or mindfulness exercise, "
            f"remind the user of your AI status, and include standard support resources."
        )
        return gemini_client.generate(prompt, self.system_instruction)
