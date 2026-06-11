# release_notes_generator_20/release_notes_genrtr_20.py

import subprocess
import requests
from pathlib import Path
import datetime

OUTPUT_PATH = Path("release_notes_generator_20/release_notes.md")
API_URL = "http://127.0.0.1:4433/v1/chat/completions"
MODEL = "WizardCoder-Python-13B-GGUF"
API_KEY = "local-anything"

def get_git_log():
    result = subprocess.run(
        ["git", "log", "--pretty=format:%h - %s (%an, %ad)", "--date=short"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"Git log error: {result.stderr}")
    return result.stdout

def ask_llm(log_text: str) -> str:
    prompt = f"""
You are a documentation assistant.

Given the following git log, generate:
- 📦 Release Highlights
- ⚠️ Breaking Changes
- 🛠️ Migration Notes (if needed)

Format in clean Markdown.

Git Log:
{log_text}
"""

    response = requests.post(API_URL, headers={
        "Authorization": f"Bearer {API_KEY}"
    }, json={
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a documentation assistant."},
            {"role": "user", "content": prompt}
        ]
    })

    try:
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("❌ LLM response parse failed:", e)
        print("Raw response:", response.text)
        return "❌ Failed to generate release notes."

def main():
    try:
        log = get_git_log()
        if not log.strip():
            print("⚠️ No git history found.")
            return
        notes = ask_llm(log)
        OUTPUT_PATH.write_text(f"# 📝 Release Notes

Generated: {datetime.datetime.now()}

{notes}", encoding="utf-8")
        print(f"✅ Release notes saved to: {OUTPUT_PATH.resolve()}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
