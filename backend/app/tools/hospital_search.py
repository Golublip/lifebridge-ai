from typing import List, Dict, Any

# Mock hospital data
HOSPITAL_DATABASE = [
    {
        "id": "hosp_1",
        "name": "Mercy Community Health Clinic",
        "type": "Community Clinic",
        "address": "456 Main St, Rural Village, OH 43102",
        "zip": "43102",
        "avg_consultation_cost": 25.0,
        "emergency_services": False,
        "contact": "+1 (555) 123-4567",
        "specialties": ["Primary Care", "Pediatrics", "Diabetes Management"],
        "supported_schemes": ["Medicaid", "Medicare", "Sliding Scale Program"]
    },
    {
        "id": "hosp_2",
        "name": "County General Hospital",
        "type": "General Hospital",
        "address": "789 Medical Plaza, County City, OH 43001",
        "zip": "43001",
        "avg_consultation_cost": 150.0,
        "emergency_services": True,
        "contact": "+1 (555) 987-6543",
        "specialties": ["Emergency Medicine", "Cardiology", "Orthopedics", "Oncology"],
        "supported_schemes": ["Medicare", "Medicaid", "Private Insurance", "Charity Care Plan"]
    },
    {
        "id": "hosp_3",
        "name": "St. Jude Rural Health Center",
        "type": "Federal Qualified Health Center (FQHC)",
        "address": "12 Ridge Road, Appalache, OH 43701",
        "zip": "43701",
        "avg_consultation_cost": 15.0,
        "emergency_services": False,
        "contact": "+1 (555) 234-5678",
        "specialties": ["Family Practice", "Dental", "Mental Health Counselling"],
        "supported_schemes": ["Sliding Scale Program", "Medicaid", "Federal Clinic Fund"]
    },
    {
        "id": "hosp_4",
        "name": "Metro Urgent Care",
        "type": "Urgent Care",
        "address": "100 Highway 20, Suburbia, OH 43081",
        "zip": "43081",
        "avg_consultation_cost": 75.0,
        "emergency_services": True,
        "contact": "+1 (555) 345-6789",
        "specialties": ["Urgent Care", "Minor Injuries", "X-Ray Services"],
        "supported_schemes": ["Medicaid", "Private Insurance"]
    }
]

class HospitalSearchTool:
    """
    Search for affordable nearby clinics and hospitals based on zip code, cost limits, and emergency requirements
    """
    def search_clinics(self, zip_code: str, max_cost: float = None, require_emergency: bool = False) -> List[Dict[str, Any]]:
        results = []
        for h in HOSPITAL_DATABASE:
            # Simple zip comparison (e.g. matching first 2 characters or exact)
            zip_match = (h["zip"] == zip_code) or (h["zip"][:3] == zip_code[:3] if zip_code else True)
            cost_match = (max_cost is None) or (h["avg_consultation_cost"] <= max_cost)
            emerg_match = (not require_emergency) or h["emergency_services"]
            
            if zip_match and cost_match and emerg_match:
                # Add mock travel distance
                dist = 2.5 if h["zip"] == zip_code else 12.4
                item = h.copy()
                item["estimated_distance_miles"] = dist
                results.append(item)
                
        return sorted(results, key=lambda x: x["estimated_distance_miles"])
