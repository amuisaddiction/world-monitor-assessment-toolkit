import os
import google.generativeai as genai
import json

def generate_gemini_report(findings: list) -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found")
        
    if not findings:
        return "# World Monitor Security Assessment Report\n\nNo security findings were generated during this assessment."
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    prompt = f"Generate a professional Markdown security report based on these findings:\n{json.dumps(findings)}"
    response = model.generate_content(prompt)
    return response.text
