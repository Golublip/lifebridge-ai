# LifeBridge AI
> "An Autonomous Healthcare Navigation Agent System for Underserved Communities"

LifeBridge AI is a state-of-the-art multi-agent healthcare navigator designed to improve clinical access, safety, and health equity in rural, low-income, and elder care contexts.

---

## Key Features

1. **Master Orchestrator**: Uses Gemini 2.5 Flash to automatically plan execution graphs, dispatch sub-agents, and aggregate clinical summaries.
2. **Clinical Safety Reflection**: An internal Quality Control loop critiques response logs to prevent diagnostic claims and check allergen exclusions.
3. **Emergency Auto-Escalation**: High-urgency symptoms (e.g. chest pressure, stroke) immediately suspend standard loops to show emergency directives and nearest ER coordinates.
4. **OCR Health Records**: Multimodal extraction parses lab sheets or prescriptions to populate patient history and medication tracker metrics.
5. **Government Scheme Recommendations**: Auto-recommends coverage programs (Medicaid, Medicare, Ayushman Bharat, sliding scales) to minimize care costs.
6. **Unified Glassmorphic UI Dashboard**: A futuristic, responsive Dark Mode portal featuring vitals telemetry, compliance charts, and an interactive voice/text AI assistant widget.

---

## Directory Structure

```
lifebridge-ai/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI Routes
│   │   ├── agents/       # Multi-agent System
│   │   ├── memory/       # short-term & vector store
│   │   ├── models/       # schemas & database
│   │   ├── tools/        # search, interactions, OCR
│   │   └── utils/        # gemini unified client
│   └── tests/            # pytest verification suite
├── frontend/
│   └── app/              # Next.js UI views & layouts
└── Dockerfile            # Deployment container configuration
```

---

## Quickstart Guide

### 1. Backend Setup
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate   # On Windows
source .venv/bin/activate # On Unix/macOS

pip install -r requirements.txt
python app/main.py
```
*The FastAPI backend will launch at `http://localhost:8000`. Documentation is available at `/docs`.*

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
*The dashboard will boot at `http://localhost:3000`.*

---

## Verification & Testing
To run the automated agentic evaluation and unit test suite:
```bash
cd backend
.venv\Scripts\pytest tests/
```

---

## Social Impact & Vision
In regions with severe doctor shortages, patients struggle to evaluate when symptoms warrant travel to a distant clinic. By acting as a patient advocate, LifeBridge AI prevents unnecessary travel costs for mild issues, guides proper first aid in crises, and automatically finds low-cost FQHC clinic alternatives, advancing healthcare access globally.
