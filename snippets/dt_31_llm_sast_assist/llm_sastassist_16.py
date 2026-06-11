import subprocess
import requests
from pathlib import Path

API_URL = "http://127.0.0.1:4433/v1/chat/completions"
MODEL = "WizardCoder-Python-13B-GGUF"
API_KEY = "local-anything"
SAST_REPORT_FILE = Path("llm_sast_assist_16/last_sast_report.md")

def run_bandit_scan():
    result = subprocess.run(
        ["bandit", "-r", "."],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()

def ask_llm_for_fix(raw_report: str):
    prompt = f"""
You are a Python security assistant.

The following is a Bandit security scan result. Your task:
- Summarize real risks vs false positives
- Propose one-liner fixes where relevant
- Group by module or pattern
- Format response in Markdown

Scan report:
{raw_report}
"""

    response = requests.post(API_URL, headers={
        "Authorization": f"Bearer {API_KEY}"
    }, json={
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a Python security assistant."},
            {"role": "user", "content": prompt}
        ]
    })

    try:
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("❌ Failed to parse LLM output:", e)
        print(response.text)
        return "❌ LLM analysis failed."

def main():
    print("🔍 Running Bandit static scan...")
    report = run_bandit_scan()
    print("🤖 Sending to LLM for analysis...")
    advice = ask_llm_for_fix(report)
    SAST_REPORT_FILE.write_text(advice, encoding="utf-8")
    print(f"✅ SAST report saved to {SAST_REPORT_FILE.resolve()}")

if __name__ == "__main__":
    main()
