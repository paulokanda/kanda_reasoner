import json
import requests
from pathlib import Path
import sys

# Configuration
API_URL = "http://127.0.0.1:4433/v1/chat/completions"
MODEL = "WizardCoder-Python-13B-GGUF"
API_KEY = "local-anything"  # Dummy key for local-compatible servers

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def ask_llm(json_data):
    prompt = f"""You are an AI assistant that reads diagnostic or profiling JSON data and gives actionable developer advice.

Instructions:
- Read the JSON content below.
- Summarize what it shows.
- Suggest next steps: profiling, bug fixes, improvements, or edge case tests.

JSON Data:
{json.dumps(json_data, indent=2)}
"""

    response = requests.post(API_URL, headers={
        "Authorization": f"Bearer {API_KEY}"
    }, json={
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are an AI software assistant."},
            {"role": "user", "content": prompt}
        ]
    })

    return response.json()["choices"][0]["message"]["content"]

def main():
    if len(sys.argv) != 2:
        print("Usage: python json_adviceout_13.py path/to/input.json")
        return

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"❌ File not found: {path}")
        return

    json_data = load_json(path)
    advice = ask_llm(json_data)
    print("\n💡 LLM Advice:\n")
    print(advice)

if __name__ == "__main__":
    main()
