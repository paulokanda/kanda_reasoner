# preset_curator_17/pr_curator_17.py

import json
from pathlib import Path
from datetime import datetime
import requests

# Configuration
HISTORY_FILE = Path("preset_curator_17/last_actions.json")
OUTPUT_FILE = Path("preset_curator_17/preset_suggestions.md")
API_URL = "http://127.0.0.1:4433/v1/chat/completions"
MODEL = "WizardCoder-Python-13B-GGUF"
API_KEY = "local-anything"  # Dummy key for local API

def load_last_actions():
    if not HISTORY_FILE.exists():
        raise FileNotFoundError(f"History file not found: {HISTORY_FILE}")
    return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))

def ask_llm_for_presets(action_data: dict) -> str:
    prompt = f"""
You are a UX assistant for an EEG visualization tool.

The user has performed the following recent actions in the GUI (e.g., selected filters, colormap, FFT settings, gain, etc). Based on this, suggest reusable **presets** they could save.

Respond in markdown format with:

- 🎛️ Preset Name
- 📋 Description
- 🧪 When to use it

Actions:
{json.dumps(action_data, indent=2)}
"""

    response = requests.post(API_URL, headers={
        "Authorization": f"Bearer {API_KEY}"
    }, json={
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a UX assistant for an EEG visualization tool."},
            {"role": "user", "content": prompt}
        ]
    })

    try:
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("❌ Failed to parse LLM output:", e)
        print(response.text)
        return "❌ Failed to get preset suggestions from LLM."

def main():
    try:
        actions = load_last_actions()
        markdown = ask_llm_for_presets(actions)
        OUTPUT_FILE.write_text(f"# Suggested Presets\n\nGenerated: {datetime.now()}\n\n{markdown}", encoding="utf-8")
        print(f"✅ Preset suggestions written to {OUTPUT_FILE.resolve()}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
