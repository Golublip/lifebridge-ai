from typing import List, Dict, Any

INTERACTION_RULES = [
    {
        "drugs": ["Metformin", "Contrast Dye"],
        "severity": "High",
        "mechanism": "Increases risk of lactic acidosis. Metformin should be temporarily suspended prior to or at the time of contrast media injection.",
        "remedy": "Hold Metformin for 48 hours following contrast injection and restart only after renal function is confirmed normal."
    },
    {
        "drugs": ["Aspirin", "Warfarin"],
        "severity": "Critical",
        "mechanism": "Both medications inhibit clotting. Combining them increases the risk of major gastrointestinal and systemic bleeding.",
        "remedy": "Avoid combination unless strictly directed by a cardiologist. Monitor for dark stools, easy bruising, or gum bleeding."
    },
    {
        "drugs": ["Lisinopril", "Potassium"],
        "severity": "High",
        "mechanism": "Lisinopril (an ACE inhibitor) spares potassium in kidneys. Adding potassium supplements leads to severe hyperkalemia (high blood potassium).",
        "remedy": "Discontinue over-the-counter potassium supplements. Monitor blood electrolyte levels regularly."
    },
    {
        "drugs": ["Sildenafil", "Nitroglycerin"],
        "severity": "Critical",
        "mechanism": "Nitrates combined with Sildenafil cause severe, life-threatening drops in blood pressure (hypotension).",
        "remedy": "Do NOT take Sildenafil if using Nitroglycerin or other nitrates. Seek immediate emergency care if chest pain occurs after taking Sildenafil."
    },
    {
        "drugs": ["Ibuprofen", "Aspirin"],
        "severity": "Moderate",
        "mechanism": "Both are NSAIDs. Combined use decreases aspirin's cardioprotective effect and increases gastric ulceration risk.",
        "remedy": "Take Ibuprofen at least 2 hours after or 8 hours before Aspirin if both are required, or switch to Acetaminophen."
    }
]

class MedicineCheckerTool:
    """
    Check for harmful drug-drug interactions and provide mitigation guidelines.
    """
    def check_interaction(self, drug_list: List[str]) -> List[Dict[str, Any]]:
        found_interactions = []
        normalized_list = [d.strip().lower() for d in drug_list]
        
        for rule in INTERACTION_RULES:
            match_count = 0
            for rule_drug in rule["drugs"]:
                if any(rule_drug.lower() in user_drug for user_drug in normalized_list):
                    match_count += 1
            if match_count >= len(rule["drugs"]):
                found_interactions.append(rule)
                
        return found_interactions
