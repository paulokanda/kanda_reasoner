from pathlib import Path
from typing import Optional
import datetime
import os
import re

import requests

# dt_02_adr_writer_ok/ad_writer_02.py

PRIMARY_API_URL = os.getenv(
    "ADR_API_URL", "http://127.0.0.1:5000/v1/chat/completions")
FALLBACK_API_URLS = [
    "http://127.0.0.1:15416/v1/chat/completions",
    "http://127.0.0.1:4433/v1/chat/completions",
]
MODEL = os.getenv("ADR_MODEL", "WizardCoder-Python-13B-GGUF")
API_KEY = os.getenv("ADR_API_KEY", "local-anything")
REQUEST_TIMEOUT = float(os.getenv("ADR_TIMEOUT", "60"))
OUTPUT_DIR = Path("docs/adr")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------
# Step 1 — Collect user input for the ADR title/idea.
# -------------------------------------------------------


def get_user_input() -> str:
    """Get user input for the ADR title/idea."""
    print(
        "Enter a short description of your architectural decision (e.g., 'switch to PySide6'):"
    )
    return input(" ").strip()


# -------------------------------------------------------
# Step 2 — Sanitize the filename based on user input.
# -------------------------------------------------------


def sanitize_filename(title: str) -> str:
    """Sanitize filename for the ADR."""
    return re.sub(r"\W+", "-", title.lower())[:40].strip("-")


# -------------------------------------------------------
# Step 3 — Attempt to post a chat completion request to the primary API URL.
# -------------------------------------------------------
# Depends on PRIMARY_API_URL, MODEL, API_KEY, REQUEST_TIMEOUT.
# -------------------------------------------------------


def _post_chat_completion(api_url: str, prompt: str) -> Optional[str]:
    """
    Attempt a single POST to an OpenAI-compatible /v1/chat/completions endpoint.
    Returns the message content or None on failure.
    """
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a software architect documenting design decisions.",
            },
            {"role": "user", "content": prompt},
        ],
    }
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        resp = requests.post(
            api_url, json=payload, headers=headers, timeout=REQUEST_TIMEOUT
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"  Request to {api_url} failed: {e}")
        try:
            print(" Raw response:", resp.text[:1000])
        except Exception:
            pass
        return None


# -------------------------------------------------------
# Step 4 — Call the LLM to generate the ADR, trying primary URL then fallbacks.
# -------------------------------------------------------
# Depends on _post_chat_completion, PRIMARY_API_URL, FALLBACK_API_URLS.
# -------------------------------------------------------


def call_llm(decision_idea: str) -> str:
    """Call the LLM to generate the ADR, trying primary URL then fallbacks."""
    prompt = f"""
You're a software architect documenting design decisions.
Given this summary:
\"\"\"{decision_idea}\"\"\"
Write a full Architectural Decision Record (ADR) in Markdown format. Use this structure:
Proposed
Explain why this decision is being made now.
Describe the architectural choice being made.
List pros, cons, tradeoffs, or new risks.
Make it concise and professional.
""".strip()
    content = _post_chat_completion(PRIMARY_API_URL, prompt)
    if content:
        return content
    for url in FALLBACK_API_URLS:
        content = _post_chat_completion(url, prompt)
        if content:
            return content
    return "Failed to retrieve ADR from LLM (all endpoints failed)."


# -------------------------------------------------------
# Step 5 — Main function: gathers input, calls the LLM, and writes the ADR file.
# -------------------------------------------------------
# Depends on get_user_input, sanitize_filename, call_llm, OUTPUT_DIR.
# -------------------------------------------------------


def main():
    """Main: gathers input, calls the LLM, and writes the ADR file."""
    decision = get_user_input()
    if not decision:
        print("No input given. Exiting.")
        return
    md_content = call_llm(decision)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    safe_name = sanitize_filename(decision)
    filename = f"ADR-{timestamp}-{safe_name}.md"
    output_path = OUTPUT_DIR / filename
    output_path.write_text(md_content, encoding="utf-8")
    print(f"ADR saved to {output_path.resolve()}")


if __name__ == "__main__":
    main()
