import json
import os
from ai_triage.gemini_client import generate_gemini_report
from ai_triage.fallback import generate_local_fallback_report

def run_report_generation(findings: list, output_path: str):
    try:
        report_content = generate_gemini_report(findings)
    except Exception as e:
        print(f"Gemini generation failed or missing key, using fallback: {e}")
        report_content = generate_local_fallback_report(findings)
        
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
