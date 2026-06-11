# crash_triage_05/crashtriage_05.py

import traceback
import sys
import requests
import datetime
from pathlib import Path

# Configuration
API_URL = "http://127.0.0.1:4433/v1/chat/completions"
MODEL = "WizardCoder-Python-13B-GGUF"
API_KEY = "local-anything"
OUTPUT_PATH = Path(__file__).parent / "crash_triage_report.md"

def simulate_crash():
    # Simulated crash: replace this block with real code execution in practice
    raise ValueError("Simulated crash: Invalid signal shape in montage processor.")

def ask_llm_for_triage(tb_text: str) -> str:
    prompt = f"""
You're a debugging assistant for a scientific Python application involving EEG data, PyQt, and NumPy.

The following crash occurred during execution. Analyze the stack trace and suggest:

- Likely root cause
- Broken invariants (e.g., shape assumptions, threading issues)
- A minimal reproduction snippet
- 3-step fix plan

Respond in Markdown format.

Traceback:
{tb_text}
"""

    response = requests.post(API_URL, headers={
        "Authorization": f"Bearer {API_KEY}"
    }, json={
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You're a debugging assistant."},
            {"role": "user", "content": prompt}
        ]
    })

    try:
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("⚠️ Failed to parse LLM response:", e)
        print("Raw response:", response.text)
        return "❌ LLM failed to generate crash triage."

def main():
    try:
        simulate_crash()
    except Exception:
        tb_text = traceback.format_exc()
        report = ask_llm_for_triage(tb_text)
        full_text = f"# Crash Triage Report

Generated: {datetime.datetime.now()}

{report}"
        OUTPUT_PATH.write_text(full_text, encoding="utf-8")
        print(f"✅ Crash triage written to {OUTPUT_PATH.resolve()}")

if __name__ == "__main__":
    main()
