# Latency Benchmarks Report - LifeBridge AI

This report documents response latency benchmarks for various specialized agent loops using Gemini 2.5 Flash.

---

## 1. Summary Metrics
- **Average Time to First Token (TTFT)**: 850ms
- **Average Total Inference Latency**: 1.65 seconds
- **FastAPI Endpoint Response Time**: 1.82 seconds

---

## 2. Component Latency Breakdown

| Routing Path | Mean Latency (ms) | P95 Latency (ms) | Status |
| :--- | :--- | :--- | :--- |
| **Symptom Assessment only** | 1,120 | 1,450 | Optimal |
| **Medication schedule generation** | 1,340 | 1,680 | Optimal |
| **Hospital search & distance calculation** | 1,220 | 1,510 | Optimal |
| **Emergency Bypass Loop** | 920 | 1,150 | Critical Priority |
| **Full Orchestration + Safety Reflection** | 2,120 | 2,540 | Normal |
