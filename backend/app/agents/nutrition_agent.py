from app.utils.gemini_client import gemini_client
from typing import List

class NutritionAgent:
    """
    Nutrition Agent.
    Creates healthy meal plans tailored to specific diseases (like diabetes, hypertension),
    optimized for budget and adjusted for cultural/regional dietary preferences.
    """
    def __init__(self):
        self.system_instruction = (
            "You are the Nutrition Agent for LifeBridge AI. Your objective is to formulate healthy, "
            "cost-effective, and culturally appropriate dietary recommendations for patients. "
            "Focus on disease-specific nutrition parameters, such as low-sodium diets for hypertension "
            "or low-glycemic plans for diabetes, prioritizing affordable ingredients (like dried beans, oats, eggs)."
        )

    def formulate_diet(self, conditions: List[str], budget_level: str = "low", preferences: str = "General") -> str:
        prompt = (
            f"Chronic Conditions: {conditions}\n"
            f"Budget Constraints: {budget_level}\n"
            f"Cultural/Dietary Preferences: {preferences}\n\n"
            f"Design a simple, high-impact daily meal plan (Breakfast, Lunch, Dinner, Snacks). "
            f"Emphasize budget optimization, listing cheap raw ingredients and explaining why "
            f"this plan is safe and healthy for the listed chronic conditions."
        )
        return gemini_client.generate(prompt, self.system_instruction)
