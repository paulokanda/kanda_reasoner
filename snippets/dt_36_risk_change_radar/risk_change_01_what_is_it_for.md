📌 risk_change_01.py – What Is It For?

This script is an AI-assisted code reviewer designed specifically for EEG projects using PyQt and NumPy/SciPy.

Its goal is to analyze staged Git diffs and generate a Markdown report that highlights:

⚠️ Risks Detected: timeline bugs, GUI sync issues, NumPy broadcasting traps, etc.

✅ Safe Changes: low-risk or clearly beneficial changes.

🧪 Suggested Tests: edge cases and tests to add for robustness.

🛠️ Suggested Fixes: refactor or logic corrections.

🔧 How It Works (Under the Hood)

Reads your staged changes (via git diff --cached) — this means changes you’ve run git add on.

Builds a prompt for the local LLM:

Assumes context: EEG + GUI + signal processing.

Requests structured Markdown output.

Sends it to your local OpenAI-compatible endpoint, e.g.:

http://127.0.0.1:5000/v1/chat/completions

Writes a Markdown file with the AI’s code review:
▶️ How to Use It
✅ Step-by-step

Stage some changes using Git:

git add path/to/your_file.py


Run the script:

python dev_tools/risk_change_radar_01/risk_change_01.py

Check the Markdown report:

dev_tools/risk_change_radar_01/risk_analysis.md

🧠 Why It's Useful

Replaces manual diffs and low-value code reviews with LLM-generated insight.

Spots tricky EEG edge cases: timing, threading, shape mismatches, etc.

Suggests relevant tests and assertions automatically.

Fits right into your PyCharm or terminal Git workflow.

⚙️ Requirements

Your local model server must expose an OpenAI-compatible API (e.g. oobabooga with OpenAI extension enabled).

MODEL, API_URL, and API_KEY are configured inside the script:

API_URL = "http://127.0.0.1:5000/v1/chat/completions"
MODEL = "WizardCoder-Python-13B-GGUF"
API_KEY = "local-anything"

You can adjust these to match your setup.