from app.utils.gemini_client import gemini_client
from app.tools.ocr_tool import OCRTool
from typing import Dict, Any
import os

class HealthRecordsAgent:
    """
    Health Records Agent.
    Orchestrates OCR document extraction, summarizes medical reports, and parses clinical vitals/markers
    to update the patient dashboard.
    """
    def __init__(self):
        self.ocr_tool = OCRTool()
        self.system_instruction = (
            "You are the Health Records Agent for LifeBridge AI. Your objective is to parse OCR texts "
            "from scans, invoices, and lab tests. Identify critical parameters (like HbA1c, fasting glucose, "
            "blood pressure), summarize findings in patient-friendly terms, and format a clinical timeline "
            "tracking history."
        )

    def process_record(self, file_path: str) -> Dict[str, Any]:
        ocr_result = self.ocr_tool.parse_document(file_path)
        extracted_text = ocr_result["text"]
        parsed_params = ocr_result["parsed_parameters"]
        
        prompt = (
            f"Extracted Raw Document Text:\n\"\"\"{extracted_text}\"\"\"\n\n"
            f"Please synthesize this document. Explain what the lab values or prescriptions mean "
            f"in plain English. Point out whether any values are out of the normal range (e.g. HbA1c > 6.0% "
            f"is diabetic, Blood Sugar > 100 mg/dL is elevated, BP > 120/80 is prehypertensive). Keep it "
            f"empathetic and easy to understand for elderly or rural patients."
        )
        
        summary = gemini_client.generate(prompt, self.system_instruction)
        
        return {
            "file_name": os.path.basename(file_path),
            "summary": summary,
            "parsed_parameters": parsed_params
        }
