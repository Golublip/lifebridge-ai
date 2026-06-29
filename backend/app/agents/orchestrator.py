from app.agents.symptom_agent import SymptomAgent
from app.agents.medication_agent import MedicationAgent
from app.agents.hospital_agent import HospitalAgent
from app.agents.nutrition_agent import NutritionAgent
from app.agents.mental_health_agent import MentalHealthAgent
from app.agents.emergency_agent import EmergencyAgent
from app.agents.health_records_agent import HealthRecordsAgent
from app.agents.reflection_agent import ReflectionAgent

from app.memory.short_term import ShortTermMemory
from app.memory.long_term import LongTermMemory
from app.memory.vector_store import VectorMemory
from app.tools.translation_tool import TranslationTool

from app.utils.gemini_client import gemini_client
from typing import Dict, Any, List
import json

class MasterOrchestrator:
    """
    LifeBridge AI Master Orchestrator.
    Coordinates specialized agents, maintains session memories, executes planning-reflection loops,
    and formats synthesized outputs for the client.
    """
    def __init__(self, session_id: str = "default_session", user_id: str = "default_user"):
        self.session_id = session_id
        self.user_id = user_id
        
        # Initialize specialized agents
        self.symptom_agent = SymptomAgent()
        self.medication_agent = MedicationAgent()
        self.hospital_agent = HospitalAgent()
        self.nutrition_agent = NutritionAgent()
        self.mental_agent = MentalHealthAgent()
        self.emergency_agent = EmergencyAgent()
        self.records_agent = HealthRecordsAgent()
        self.reflection_agent = ReflectionAgent()
        
        # Initialize memory & translation
        self.short_term = ShortTermMemory(session_id)
        self.long_term = LongTermMemory(user_id)
        self.vector_store = VectorMemory()
        self.translator = TranslationTool()

    def route_and_solve(self, message: str, user_location: str = None) -> Dict[str, Any]:
        # 1. Update short term message log
        self.short_term.add_message("user", message)
        
        # 2. Get profile summary for context
        profile_summary = self.long_term.get_summary()
        profile = self.long_term.get_profile()
        
        # Get historical conversations from vector memory
        vector_history = self.vector_store.search(message, limit=2)
        history_text = "\n".join([doc["content"] for doc in vector_history]) if vector_history else "No past records."
        
        # 3. Dynamic Planning & Intent Classification
        planning_instruction = (
            "You are the Planning Core of LifeBridge AI. Categorize the user's message into active intents.\n"
            "Intents available:\n"
            "- emergency: Chest pain, severe shortness of breath, stroke signs, severe bleeding.\n"
            "- symptom: Evaluating mild symptoms, questions, checkups.\n"
            "- medication: Reminder queries, schedules, interaction checking.\n"
            "- hospital: Finding clinics, comparing costs, government schemes.\n"
            "- nutrition: Meal plans, diabetic diets, budget recipes.\n"
            "- mental: Emotional stress, anxiety, mindfulness.\n"
            "- records: OCR summaries, vitals tracking.\n\n"
            "Format your reply as a JSON list of intents in order of execution. Example: ['symptom', 'hospital']"
        )
        
        plan_str = gemini_client.generate(
            prompt=f"User Message: \"{message}\"\nPatient Context Summary:\n{profile_summary}",
            system_instruction=planning_instruction
        )
        
        # Parse plan
        try:
            # Clean possible markdown JSON wrappers
            clean_plan = plan_str.replace("```json", "").replace("```", "").strip()
            plan = json.loads(clean_plan)
            if not isinstance(plan, list):
                plan = ["symptom"]
        except Exception:
            # Heuristic routing if JSON parse fails
            plan = []
            msg_lower = message.lower()
            if any(x in msg_lower for x in ["chest pain", "heart attack", "stroke", "bleeding", "emergency", "911"]):
                plan.append("emergency")
            if any(x in msg_lower for x in ["symptom", "hurt", "pain", "dizzy", "cough", "fever"]):
                plan.append("symptom")
            if any(x in msg_lower for x in ["medication", "pill", "drug", "metformin", "lisinopril", "remind", "dose"]):
                plan.append("medication")
            if any(x in msg_lower for x in ["hospital", "clinic", "doctor", "cost", "cheap", "scheme", "insurance"]):
                plan.append("hospital")
            if any(x in msg_lower for x in ["food", "diet", "nutrition", "meal", "eat"]):
                plan.append("nutrition")
            if any(x in msg_lower for x in ["stress", "anxious", "anxiety", "depressed", "sad", "mental"]):
                plan.append("mental")
            
            # Default fallback
            if not plan:
                plan = ["symptom"]
                
        # 4. Execute agents based on plan
        agent_responses = {}
        agents_involved = []
        is_emergency = "emergency" in plan
        
        # Override plan if severe symptoms are present in the text regardless of classifier output
        msg_lower = message.lower()
        if any(x in msg_lower for x in ["chest pain", "stroke", "heart attack", "unconscious"]) and "emergency" not in plan:
            plan.insert(0, "emergency")
            is_emergency = True
            
        zip_code = user_location or profile.get("location") or "43001"
        
        for intent in plan:
            if intent == "emergency":
                agents_involved.append("EmergencyAgent")
                agent_responses["emergency"] = self.emergency_agent.trigger_emergency(message, zip_code)
            elif intent == "symptom":
                agents_involved.append("SymptomAgent")
                agent_responses["symptom"] = self.symptom_agent.analyze(message, profile_summary)
            elif intent == "medication":
                agents_involved.append("MedicationAgent")
                # Detect action: check interaction if multiple drugs are mentioned
                if len([d for d in ["aspirin", "warfarin", "lisinopril", "potassium", "metformin"] if d in msg_lower]) >= 2:
                    action = "check_interactions"
                else:
                    action = "generate_schedule"
                agent_responses["medication"] = self.medication_agent.process(action, {"message": message})
            elif intent == "hospital":
                agents_involved.append("HospitalAgent")
                conditions = profile.get("chronic_conditions", [])
                agent_responses["hospital"] = self.hospital_agent.locate_care(zip_code, conditions)
            elif intent == "nutrition":
                agents_involved.append("NutritionAgent")
                conditions = profile.get("chronic_conditions", [])
                agent_responses["nutrition"] = self.nutrition_agent.formulate_diet(conditions)
            elif intent == "mental":
                agents_involved.append("MentalHealthAgent")
                agent_responses["mental"] = self.mental_agent.support(message)
                
        # 5. Synthesize Agent Outputs
        synthesis_prompt = (
            f"You are the Synthesis Engine of LifeBridge AI.\n"
            f"User Original Query: \"{message}\"\n"
            f"Specialized Agent Outputs:\n{json.dumps(agent_responses, indent=2)}\n\n"
            f"Combine these outputs into a single, cohesive, highly readable response for the patient. "
            f"Use clear headers, bullet points, and highlight emergency warnings at the top if present. "
            f"Avoid duplicating recommendations. Keep the vocabulary accessible."
        )
        
        proposed_output = gemini_client.generate(synthesis_prompt, "You are a helpful, empathetic clinical navigation assistant.")
        
        # 6. Reflection Loop (Quality Control)
        agents_involved.append("ReflectionAgent")
        reflection_result = self.reflection_agent.critique(proposed_output, profile, message)
        
        final_output = proposed_output
        if "STATUS: REVISED" in reflection_result:
            final_output = reflection_result.replace("STATUS: REVISED", "").strip()
            
        # 7. Localization / Translation
        user_lang = profile.get("preferences", {}).get("language", "English")
        if user_lang.lower() != "english":
            final_output = self.translator.translate(final_output, user_lang)
            
        # 8. Save final response in short term and vector store
        self.short_term.add_message("assistant", final_output)
        self.vector_store.add_document(
            doc_id=f"chat_{self.session_id}_{len(self.short_term.get_chat_history())}",
            content=f"User: {message}\nAssistant: {final_output}",
            metadata={"session_id": self.session_id, "user_id": self.user_id}
        )
        
        return {
            "session_id": self.session_id,
            "response": final_output,
            "plan": plan,
            "agents_involved": agents_involved,
            "emergency_mode": is_emergency,
            "language": user_lang,
            "data": agent_responses
        }
