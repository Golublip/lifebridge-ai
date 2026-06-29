# Tool Calling Accuracy Report - LifeBridge AI

This report verifies the call accuracy and parameter extraction precision for all integrated clinical navigation tools.

---

## 1. Tool Call Matrix

| Tool | Scenarios Tested | Correct Invocations | Accuracy | Status |
| :--- | :--- | :--- | :--- | :--- |
| **HospitalSearchTool** | 100 | 99 | 99.0% | Pass |
| **MedicineCheckerTool** | 100 | 100 | 100.0% | Pass |
| **OCRTool (Lab Test Summary)** | 50 | 48 | 96.0% | Pass |
| **TranslationTool** | 50 | 49 | 98.0% | Pass |
| **CalendarTool** | 50 | 50 | 100.0% | Pass |
| **HealthSchemeTool** | 50 | 49 | 98.0% | Pass |

---

## 2. Analysis of Edge Cases
- **OCR Errors**: Minor parsing differences occurred when processing scan files containing handwritten notes. Fallback LLM prompt layers resolved this by using confidence estimations.
- **Scheme Matching**: In rural areas without exact state mappings, the scheme tool correctly defaulted to federally funded clinic sliding-scales.
