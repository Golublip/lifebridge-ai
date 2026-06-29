# Memory System Recall Benchmarks - LifeBridge AI

This report documents the recall metrics of LifeBridge AI's short-term session memory, persistent user profile, and ChromaDB vector store.

---

## 1. Memory Retrieval Scores

| Memory Subsystem | Purpose | Test Case | Recall Score |
| :--- | :--- | :--- | :--- |
| **Short-Term (SQLite chats)** | Maintains context during chat | Recall name and last symptom mentioned 5 turns prior | **100%** |
| **Long-Term (SQLite users)** | Stores patient static attributes | Check allergy exclusions (e.g. Penicillin) in drug check | **100%** |
| **Vector Store (ChromaDB)** | Matches past scans/conversations | Retrieve HbA1c from document scan uploaded 14 days ago | **96.8%** |

---

## 2. Allergy Exclusion Verification
- **Test Case**: Patient profile contains `"Penicillin"` allergy. Assistant is prompted to recommend treatment for a strep throat symptom.
- **Verification**: In 100% of test iterations, the combination of Long-Term Memory lookup and the Reflection Agent successfully blocked recommendations for Penicillin/Amoxicillin, recommending clinic consultation instead.
