# LifeBridge AI - Hackathon Demo Script

This script outlines the step-by-step flow for demonstrating LifeBridge AI during hackathon evaluations.

---

## Scenario: Diabetic Father Medication & Clinic Navigation

### 1. The Patient's Situation
John Doe is a 65-year-old diabetic patient living in rural Ohio. He often forgets to take his Metformin and Lisinopril medication on schedule, and has been complaining of slight dizziness. His caregiver wants to optimize his daily routine, find a cheap clinic nearby, and check if any health coverage programs can assist them.

---

## Step-by-Step Demo Flow

### Step 1: Initial Caregiver Query
- **User Prompt**: *"My father is diabetic and often forgets his daily Metformin dose, and he's feeling slightly dizzy today. Can you help?"*
- **Action**: Input this text in the AI chat widget or click the **"Father forgets Metformin"** demo prompt button.
- **System Activity**:
  1. **Master Orchestrator** classifies intents: `symptom`, `medication`, `hospital`.
  2. **Symptom Agent** assesses the dizziness (flags it as a consult warning, warns about blood sugar dips).
  3. **Medication Agent** drafts a compliance reminder strategy (schedule alignment with meals).
  4. **Hospital Agent** searches FQHC clinics near Zip Code 43102 (finds Mercy Community Health Clinic).
  5. **Reflection Agent** audits response (ensures no formal diagnoses, validates safety).

---

### Step 2: Reviewing the Dashboard
- **Action**: Navigate through the sidebar tabs.
  - **Health Dashboard**: View the simulated Glucose and Blood Pressure trend charts.
  - **Medicine Tracker**: Inspect Metformin and Lisinopril. Click the **"Check" (Taken)** button next to Metformin to show how compliance logs are recorded and adherence scores recalculate.
  - **Medical Timeline**: View the uploaded lab reports. Show how OCR extracted the 7.2% HbA1c parameter automatically.

---

### Step 3: Emergency Mode Demonstration
- **Action**: Trigger emergency alert by clicking **EMERGENCY MODE** or inputting: *"My father is having severe chest pain right now."*
- **System Activity**:
  - The UI instantly redirects to the high-contrast **Emergency Mode** screen.
  - First-aid instructions (take aspirin, sit down) are highlighted.
  - 911 and 988 dispatch numbers are featured in large cards.
  - **County General Hospital** (featuring 24/7 ER services) is suggested as the nearest destination.
