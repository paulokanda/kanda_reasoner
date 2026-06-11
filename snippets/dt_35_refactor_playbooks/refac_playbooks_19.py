# refactor_playbooks_19/refac_playbooks_19.py

import sys
import requests
from pathlib import Path

API_URL = "http://127.0.0.1:4433/v1/chat/completions"
MODEL = "WizardCoder-Python-13B-GGUF"
API_KEY = "local-anything"
DEFAULT_PROMPT = "Refactor this code to improve modularity, reduce complexity, and apply good software engineering practices."

def load_code(file_path):
    return Path(file_path).read_text(encoding="utf-8")

def call_llm(prompt):
    response = requests.post(API_URL, headers={
        "Authorization": f"Bearer {API_KEY}"
    }, json={
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a Python refactoring expert."},
            {"role": "user", "content": prompt}
        ]
    })
    return response.json()["choices"][0]["message"]["content"]

def main():
    if len(sys.argv) != 2:
        print("Usage: python refac_playbooks_19.py path/to/your_module.py")
        return

    file_path = sys.argv[1]
    if not Path(file_path).exists():
        print(f"❌ File not found: {file_path}")
        return

    code = load_code(file_path)
    prompt = f"""You are an expert Python refactoring assistant.

Suggest a refactoring playbook for the following code.
Consider design patterns, separation of concerns, readability, and maintainability.

Respond in Markdown with sections:
- 🧩 Code Areas of Concern
- 🔧 Suggested Refactor Plan
- 📦 Potential Module Breakdown
- ✅ Benefits

Code:
{code}
"""

    print("🤖 Sending code to LLM...")
    suggestions = call_llm(prompt)

    output_path = Path("refactor_playbooks_19/refactor_plan.md")
    output_path.write_text(suggestions, encoding="utf-8")
    print(f"✅ Refactor playbook saved to {output_path.resolve()}")

if __name__ == "__main__":
    main()
