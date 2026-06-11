import requests
from pathlib import Path
import datetime

API_URL = "http://127.0.0.1:4433/v1/chat/completions"
MODEL = "WizardCoder-Python-13B-GGUF"
API_KEY = "local-anything"
REQUIREMENTS_PATH = Path("requirements.txt")
OUTPUT_PATH = Path(__file__).parent / "dependency_risk_report.md"

def load_requirements():
    """
    Load the content of the requirements.txt file.

    Returns:
        str: The content of the requirements.txt file if it exists, otherwise None.
    """
    # ✅ Step 1.1: Check condition and execute block
    if not REQUIREMENTS_PATH.exists():
        print(f"❌ File not found: {REQUIREMENTS_PATH}")
        return None
    return REQUIREMENTS_PATH.read_text(encoding="utf-8")

def ask_llm(requirements_text):
    """
    Send the requirements.txt content to the language model API for analysis.

    Args:
        requirements_text (str): The content of the requirements.txt file.

    Returns:
        str: The generated dependency risk report in Markdown format.
    """
    prompt = f"""
You are a Python dependency risk analyst.

The following is the content of a requirements.txt file from an EEG processing application using NumPy, PyQt, SciPy, and deep learning backends.

Analyze:
- Possible version conflicts (e.g. Torch+CUDA, Qt bindings)
- Any insecure, unmaintained, or weird packages
- Pin recommendations
- If GPU-related packages match current system specs

Respond in Markdown with these sections:
- 🔍 Version Conflicts or Red Flags
- 🧱 Suggested Stable Pin Set
- 🚫 Deprecated or Problematic Packages
- 💡 Comments on GPU/ML Compatibility
- 📦 Other Insights

Requirements:

{requirements_text}

"""

    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a Python dependency risk analyst.",
                },
                {"role": "user", "content": prompt},
            ],
        },
    )

    # ✅ Step 1.1: Handle possible exceptions
    try:
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("❌ Failed to parse LLM response:", e)
        print("Raw response:", response.text)
        return "❌ Could not generate dependency risk brief."

def main():
    """
    Main function to load requirements, generate the dependency risk report, and save it to a file.
    """
    reqs = load_requirements()
    # ✅ Step 1.1: Check condition and execute block
    if reqs is None:
        return

    report = ask_llm(reqs)
    OUTPUT_PATH.write_text(
        f"# Dependency Risk Brief\n\nGenerated: {datetime.datetime.now()}\n\n{report}",
        encoding="utf-8",
    )
    print(f"✅ Risk brief written to {OUTPUT_PATH.resolve()}")

if __name__ == "__main__":
    main()
