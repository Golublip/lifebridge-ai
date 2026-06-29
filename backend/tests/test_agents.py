import sys
import os
import pytest

# Adjust path to find the backend app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.models.database import init_db, get_user_profile, get_medications
from app.agents.symptom_agent import SymptomAgent
from app.agents.medication_agent import MedicationAgent
from app.agents.hospital_agent import HospitalAgent
from app.agents.reflection_agent import ReflectionAgent
from app.agents.orchestrator import MasterOrchestrator

@pytest.fixture(autouse=True)
def setup_db():
    init_db()

def test_database_loads():
    profile = get_user_profile("default_user")
    assert profile["name"] == "John Doe"
    assert "Penicillin" in profile["allergies"]

def test_symptom_agent():
    agent = SymptomAgent()
    res = agent.analyze("I have chest pain and sudden dizziness.")
    assert "URGENT" in res or "EMERGENCY" in res or "symptom" in res.lower() or "dizzy" in res.lower()

def test_medication_interactions():
    agent = MedicationAgent()
    # Check interaction for Aspirin and Warfarin
    res = agent.process("check_interactions", {"medications": ["Aspirin", "Warfarin"]})
    assert "bleeding" in res.lower() or "interaction" in res.lower()

def test_hospital_search():
    agent = HospitalAgent()
    res = agent.locate_care("43102")
    assert "Mercy" in res or "clinic" in res.lower() or "hospital" in res.lower()

def test_reflection_safety():
    agent = ReflectionAgent()
    profile = get_user_profile("default_user")
    # Proposed response claiming user has a condition should be corrected or flagged
    proposed = "You have acute myocardial infarction. Take these pills."
    res = agent.critique(proposed, profile, "I have severe chest pressure.")
    assert "STATUS" in res

def test_orchestrator_loop():
    orch = MasterOrchestrator(session_id="test_session")
    res = orch.route_and_solve("My father forgot his diabetic medicine Metformin.")
    assert res["session_id"] == "test_session"
    assert len(res["plan"]) > 0
    assert "ReflectionAgent" in res["agents_involved"]
