# LifeBridge AI - Devpost Hackathon Submission Write-Up

## 1. Problem Statement & Impact
In rural, low-income, and marginalized communities worldwide, clinical guidance is extremely scarce. Billions struggle with complex symptom triage, clinic location logistics, and medication adherence. LifeBridge AI fills this gap as a personal, autonomous healthcare navigator that empowers patients to understand their health, organizes record data, and guides them to affordable local care.

## 2. Technical Innovation (How We Built It)
LifeBridge AI is engineered with a modular Python/FastAPI backend and a gorgeous glassmorphic Next.js dashboard UI.
- **Master Orchestrator**: Uses Gemini 2.5 Flash through the Google GenAI SDK to process patient prompts, generate multi-agent plans, and execute reasoning paths.
- **Safety Reflection**: A dedicated clinical safety auditor evaluates synthetically combined responses to strictly block self-diagnoses and filter drug allergy exclusions.
- **Emergency Bypass**: Suspends the standard query-response graphs in high-urgency scenarios, showing immediate first aid and the nearest FQHC clinics.
- **Resilient Memory**: Implements short-term session tables, user profiles, and vector-embedded search utilizing ChromaDB (with automatic local fallbacks).

## 3. Social Good & Equity
By locating clinics using sliding scale programs, translating summaries into Swahili, Spanish, or Hindi, and optimizing diets for low-income budgets, LifeBridge AI is designed from the ground up for global health equity.

---

# LifeBridge AI - Presentation Slides

### Slide 1: LifeBridge AI
- **Title**: LifeBridge AI: Autonomous Healthcare Navigation for Underserved Communities
- **Subtitle**: Bridging the gap in clinical navigation and health literacy.

### Slide 2: The Healthcare Access Crisis
- **Problem**: Extreme doctor shortages in rural areas, language barriers, complex record keeping, and high clinical costs.
- **Opportunity**: Empowering patients with a personal, pocket-sized clinical navigation advocate.

### Slide 3: System Architecture
- **Orchestration Core**: Gemini 2.5 Flash planning and routing.
- **Specialized Agents**: Symptom, Medication, Hospital, Nutrition, Mental Health, Emergency, and Records Agents.
- **Observed Memory**: Session SQL, Profile parameters, and ChromaDB vector store.

### Slide 4: Clinical Safety & Guardrails
- **No Self-Diagnosis**: Educational guidance only.
- **Reflection Loop**: Critique proposed outputs for safety prior to return.
- **Emergency Mode**: Instant bypass and dispatch coordinates.

### Slide 5: The Business Model & Roadmap
- **Future Roadmap**: Smartwatch/wearable integration, rural telemedicine hubs, and government API connections.
- **Business Model**: Open source community license, partnership with rural FQHC clinics, and local health programs.

---

# LifeBridge AI - Demo Video Script (2 Minutes)

- **[0:00 - 0:15] Introduction**: "Meet John. He is a 65-year-old managing type 2 diabetes in rural Ohio. His caregiver uses LifeBridge AI to orchestrate his care."
- **[0:15 - 0:45] Chat & Orchestration**: Show the Caregiver query: *"My father is diabetic and forgets his Metformin, and he is complaining of dizziness today."* Explain how the Orchestrator plans and calls the Symptom, Medication, and Hospital Agents.
- **[0:45 - 1:15] Vitals Dashboard & OCR**: Walk through the vitals trend charts, showing how OCR parsed the HbA1c from the report scan automatically. Log a Metformin dose to show adherence tracking.
- **[1:15 - 1:45] Emergency Bypass**: Input *"My father has severe chest pain"* and demonstrate the immediate Red Emergency Mode transition, showing emergency directions and first-aid instructions.
- **[1:45 - 2:00] Conclusion**: "LifeBridge AI: Advancing health equity, one community at a time. Thank you!"
