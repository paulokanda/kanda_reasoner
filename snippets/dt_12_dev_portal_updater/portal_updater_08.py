# dev_portal_updater_08/portal_updater_08.py

import subprocess
import requests
from pathlib import Path
import datetime

# Configuration
BASE_PATH = Path("EEG_KANDA")
OUTPUT_MD = Path(__file__).parent / "dev_portal_report.md"
FORMAT_PYS_PATH = Path(__file__).resolve().parents[2] / "dev_tools" / "format_py_tool" / "format_my_pys.py"
API_URL = "http://127.0.0.1:4433/v1/chat/completions"
MODEL = "WizardCoder-Python-13B-GGUF"
API_KEY = "local-anything"  # Dummy key for compatibility

def run_format_my_pys():
    result = subprocess.run(
        ["python", str(FORMAT_PYS_PATH), "--dry-run"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",  # 👈 Force UTF-8
        errors="replace"   # 👈 Replace unknown characters to avoid crash
    )
    if result.returncode != 0:
        raise RuntimeError(f"format_my_pys failed: {result.stderr}")
    return result.stdout

def ask_llm(summary_text: str) -> str:
    prompt = f'''
You are an AI documentation assistant.

The following is a structural summary of a Python project. Turn this into a Markdown dev portal entry that includes:

- 🗂️ Module Overview (what exists and why)
- ⚠️ Known Sharp Edges (complex areas)
- 👨‍🔧 Main Owners or Responsibilities
- ✅ Suggestions for refactors or cleanup

Summary:
{summary_text}
'''

    response = requests.post(API_URL, headers={
        "Authorization": f"Bearer {API_KEY}"
    }, json={
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are an AI documentation assistant."},
            {"role": "user", "content": prompt}
        ]
    })

    try:
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("❌ Failed to parse LLM output:", e)
        print(response.text)
        return "❌ Failed to get dev portal summary."

def main():
    try:
        print("[RUN] Running format_my_pys dry run...")
        summary = run_format_my_pys()
        print("[LLM] Asking model to draft portal entry...")
        doc = ask_llm(summary)

        # ✅ Ensure folder exists
        OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)

        OUTPUT_MD.write_text(f"# Dev Portal Overview\n\nGenerated: {datetime.datetime.now()}\n\n{doc}",
                             encoding="utf-8")
        print(f"[OK] Portal report saved to {OUTPUT_MD.resolve()}")

    except Exception as e:
        print(f"[ERR] Error: {e}")

if __name__ == "__main__":
    main()
