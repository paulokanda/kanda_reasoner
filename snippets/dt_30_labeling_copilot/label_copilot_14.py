# labeling_copilot_14/label_copilot_14.py

import json
import requests
from pathlib import Path

API_URL = "http://127.0.0.1:4433/v1/chat/completions"
MODEL = "WizardCoder-Python-13B-GGUF"
API_KEY = "local-anything"
OUTPUT_FILE = Path(__file__).parent / "labeling_suggestions.md"

def load_features_from_json(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def ask_llm(features):
    prompt = f"""
You are a labeling assistant for EEG data.

You will receive extracted features per EEG window (like band power, kurtosis, line noise). Generate:
- Weak label suggestions (e.g. artifact, eyes closed, seizure)
- Explanations (why this label fits)
- Suggestions for heuristics

Respond in Markdown per window.

Features:
{json.dumps(features, indent=2)}
"""

    response = requests.post(API_URL, headers={
        "Authorization": f"Bearer {API_KEY}"
    }, json={
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are an EEG labeling assistant."},
            {"role": "user", "content": prompt}
        ]
    })

    try:
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("❌ Failed to parse LLM output:", e)
        print(response.text)
        return "❌ LLM error."

def main():
    json_path = input("📂 Path to features JSON (relative to EEG_KANDA): ").strip()
    json_file = Path("EEG_KANDA") / json_path

    if not json_file.exists():
        print(f"❌ File not found: {json_file}")
        return

    features = load_features_from_json(json_file)
    result = ask_llm(features)
    OUTPUT_FILE.write_text(result, encoding="utf-8")
    print(f"✅ Labeling advice saved to: {OUTPUT_FILE.resolve()}")

if __name__ == "__main__":
    main()
