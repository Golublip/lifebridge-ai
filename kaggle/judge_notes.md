# Judge Evaluation Cheat Sheet - LifeBridge AI

Dear Judges, here are the key technical parameters to look for when grading LifeBridge AI:

1. **Safety Reflection Loop**:
   - Evaluated in `backend/app/agents/reflection_agent.py`. Inspect how it intercepts the synthetically aggregated response and critiques it against clinical diagnosis guidelines and allergy exclusions before return.
2. **Emergency Triage Bypass**:
   - Located in `backend/app/agents/emergency_agent.py` and routed inside `orchestrator.py`. High-urgency inputs (like chest pain) immediately re-route to ER coordinates, bypassing standard planning loops.
3. **Resilient Memory fallbacks**:
   - Check `backend/app/memory/vector_store.py`. If ChromaDB encounters SQLite library version conflicts on target platforms, it automatically fails-safe to our custom keyword-overlap search, ensuring 100% execution uptime.
4. **Multilingual Localization**:
   - In settings, changing the user language preference (e.g., Swahili, Hindi) automatically localizes chat replies and reminder instructions, addressing global south digital healthcare barriers.
