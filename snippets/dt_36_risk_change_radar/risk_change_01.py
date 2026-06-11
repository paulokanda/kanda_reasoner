# risk_change_radar/risk_change_01.py

import subprocess
import requests
from pathlib import Path
import datetime


# Configuration
API_URL = "http://127.0.0.1:4433/v1/chat/completions"
MODEL = "WizardCoder-Python-13B-GGUF"
API_KEY = "local-anything"  # Required by some clients, even if dummy
OUTPUT_PATH = Path(__file__).parent / "risk_analysis.md"

def get_staged_diff():
    result = subprocess.run(
        ["git", "diff", "--cached"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",     # ✅ Fix 1
        errors="replace",     # ✅ Fix 1
    )
    if result.returncode != 0:
        raise RuntimeError(f"Git error: {result.stderr}")
    if not result.stdout:
        raise RuntimeError("Empty Git diff. Check staged files.")  # ✅ Fix 2
    return result.stdout

def ask_llm_for_risks(diff_text: str) -> str:
    prompt = """
You are a senior Python code reviewer.

The user is working on an EEG analysis/visualization tool in PyQt and NumPy/SciPy. Below is a staged diff from their Git repo.

Analyze the risks in these changes. Consider:
- Timeline sync, GUI event handling
- NumPy array shape assumptions
- Signal processing logic errors
- Code clarity and maintainability
- Suggested tests or assertions

Respond in Markdown, with sections:
- ⚠️ Risks Detected
- ✅ Safe Changes
- 🧪 Suggested Tests
- 🛠️ Suggested Fixes

Diff:
"""

    response = requests.post(API_URL, headers={
        "Authorization": f"Bearer {API_KEY}"
    }, json={
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a senior Python code reviewer."},
            {"role": "user", "content": prompt}
        ]
    })

    try:
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("⚠️ LLM response parsing failed:", e)
        print("🧪 Raw response from LLM:\n", response.text)
        return "❌ Failed to retrieve analysis from LLM."

def main():
    try:
        diff = get_staged_diff()
        if not diff.strip():
            print("⚠️ No staged changes found. Use `git add` first.")
            return
        report = ask_llm_for_risks(diff)
        OUTPUT_PATH.write_text(f"# Risk Change Analysis\n\nGenerated: {datetime.datetime.now()}\n\n{report}", encoding="utf-8")
        print(f"✅ Report written to {OUTPUT_PATH.resolve()}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
