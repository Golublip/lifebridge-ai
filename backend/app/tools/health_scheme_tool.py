from typing import List, Dict, Any

SCHEMES_DATABASE = [
    {
        "name": "Medicaid",
        "region": "US",
        "description": "Public insurance program for low-income families, elderly individuals, and people with disabilities.",
        "benefits": "Covers doctor visits, hospital stays, long-term care, and preventative services with low or zero out-of-pocket costs.",
        "eligibility": "Income below 138% of the Federal Poverty Level (varies by state) or disabled status."
    },
    {
        "name": "Medicare Sliding Scale",
        "region": "US",
        "description": "Federally supported clinics (FQHCs) offer sliding-scale fees based on patients' ability to pay.",
        "benefits": "Deep discounts on consultation, prescription meds, dental care, and mental health counseling.",
        "eligibility": "Open to all, charges scale down based on family size and household income."
    },
    {
        "name": "Ayushman Bharat PM-JAY",
        "region": "IN",
        "description": "National health insurance scheme aimed at providing free access to healthcare for low-income earners in India.",
        "benefits": "Provides hospitalization coverage up to Rs. 5 Lakh per family per year for secondary and tertiary care.",
        "eligibility": "Identified households based on Socio-Economic Caste Census (SECC) database."
    },
    {
        "name": "National Health Insurance Scheme (NHIS)",
        "region": "GH",
        "description": "Public health insurance program in Ghana targeting universal access to healthcare.",
        "benefits": "Covers outpatient consultations, generic medicines, hospital admissions, and maternity care.",
        "eligibility": "All Ghanaian residents (premium exemptions apply for children, pregnant women, and elderly)."
    }
]

class HealthSchemeTool:
    """
    Check for applicable government healthcare schemes and financial assistance depending on patient demographics.
    """
    def check_schemes(self, location: str = "US", chronic_conditions: List[str] = None) -> List[Dict[str, Any]]:
        matching_schemes = []
        loc_normalized = location.upper().strip()
        
        # Simple match by region code or name
        for s in SCHEMES_DATABASE:
            if s["region"] in loc_normalized or loc_normalized in s["region"] or loc_normalized == "RURAL OHIO" or loc_normalized == "OH":
                # Matches US/Ohio region schemes
                if s["region"] == "US":
                    matching_schemes.append(s)
            elif loc_normalized == "INDIA" or loc_normalized == "IN":
                if s["region"] == "IN":
                    matching_schemes.append(s)
            elif loc_normalized == "GHANA" or loc_normalized == "GH":
                if s["region"] == "GH":
                    matching_schemes.append(s)
                    
        # If no region matches, return sliding scale as default fallback
        if not matching_schemes:
            matching_schemes = [SCHEMES_DATABASE[1]] # Slide scale
            
        return matching_schemes
