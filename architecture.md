# LifeBridge AI - Architecture Design Document

This document outlines the detailed system architecture, agent graphs, memory layers, and safety loops.

---

## 1. Multi-Agent Orchestration Flow

LifeBridge AI follows a **Plan-Execute-Reflect-Replan** workflow:

1. **Intent Classifier & Plan Core**: Analyzes user text input to output a prioritized list of specialized clinical intents (e.g. `['symptom', 'hospital']`).
2. **Clinical Dispatch**: Executes specialized agents in parallel or sequentially.
3. **Synthesis Engine**: Merges specialized agent outputs into a unified response.
4. **Reflection Agent (Quality Control)**: Evaluates the synthesized summary against compliance rules. If rules are violated, it automatically triggers a rewrite of the response before return.

---

## 2. Memory Subsystems

```
                     ┌──────────────────┐
                     │   User Request   │
                     └────────┬─────────┘
                              ▼
                     ┌──────────────────┐
                     │MasterOrchestrator│
                     └────────┬─────────┘
                              ▼
     ┌────────────────────────┼────────────────────────┐
     ▼                        ▼                        ▼
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│  Short-Term  │         │  Long-Term   │         │    Vector    │
│  Session DB  │         │  Patient DB  │         │   ChromaDB   │
└──────────────┘         └──────────────┘         └──────────────┘
- Active Tasks           - Allergies              - Lab Reports
- Current Chat           - Chronic Illness        - Conversation
- Tool Outputs           - Clinic Favorites       - Prescriptions
```

1. **Short-Term Memory**: Stores session state (chat bubbles) in an SQLite table `chats` for prompt history.
2. **Long-Term Memory**: Stores static profiles (name, location, allergies, conditions, preferences) in table `users`.
3. **Vector Memory**: Uses ChromaDB to embed files and past conversations, enabling semantic query search for historical trends. If ChromaDB dependencies fail on-disk, a keyword-overlap fallback memory is active to guarantee execution.

---

## 3. Specialized Tools Integration

- **Hospital Search**: Queries clinic records matching the patient's ZIP code, filtering for low-cost FQHC/sliding-scale programs.
- **Medicine Interaction Checker**: Evaluates co-prescribed drugs for harmful clinical side effects and generates advice.
- **OCR Engine**: Scans uploaded health documents, extracting critical parameters (HbA1c, glucose, BP).
- **Translation Tool**: Formats final text outputs in Spanish, Hindi, or Swahili to remove language barriers.
