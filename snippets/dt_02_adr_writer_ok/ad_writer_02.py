# dt_02_adr_writer_ok/ad_writer_02.py

"""
ad_writer_02.py
----------------
Generate an Architectural Decision Record (ADR) by calling a local
OpenAI-compatible HTTP API, with simple fallbacks.
"""

from pathlib import Path
from typing import Optional
import datetime
import os
import re

import requests


# --- 1
# Assign value to PRIMARY_API_URL.
# This establishes a key variable or state element used later in computation.
PRIMARY_API_URL = os.getenv("ADR_API_URL", "http://127.0.0.1:5000/v1/chat/completions")
# --- 2
# Assign value to FALLBACK_API_URLS.
# This establishes a key variable or state element used later in computation.
FALLBACK_API_URLS = [
    "http://127.0.0.1:15416/v1/chat/completions",
    "http://127.0.0.1:4433/v1/chat/completions",
]
# --- 3
# Assign value to MODEL.
# This establishes a key variable or state element used later in computation.
MODEL = os.getenv("ADR_MODEL", "WizardCoder-Python-13B-GGUF")
# --- 4
# Assign value to API_KEY.
# This establishes a key variable or state element used later in computation.
API_KEY = os.getenv("ADR_API_KEY", "local-anything")
# --- 5
# Assign value to REQUEST_TIMEOUT.
# This establishes a key variable or state element used later in computation.
REQUEST_TIMEOUT = float(os.getenv("ADR_TIMEOUT", "60"))
# --- 6
# Assign value to OUTPUT_DIR.
# This establishes a key variable or state element used later in computation.
OUTPUT_DIR = Path("docs/adr")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
# -------------------------------------------------------
# Step 2 — Collects user input for the ADR title/idea.
# -------------------------------------------------------
# -------------------------------------------------------


def get_user_input() -> str:
    """Get user input for the ADR title/idea."""

    print(
        "Enter a short description of your architectural decision (e.g., 'switch to PySide6'):"
    )
    # --- 7
    # Return computed result.
    # This value contributes to the output or state transition within the logic flow.
    return input(" ").strip()


# -------------------------------------------------------
# Step 3 — Sanitizes the filename based on user input.
# -------------------------------------------------------
# -------------------------------------------------------


def sanitize_filename(title: str) -> str:
    """Sanitize filename for the ADR."""

    # --- 8
    # Return computed result.
    # This value contributes to the output or state transition within the logic flow.
    return re.sub(r"\W+", "-", title.lower())[:40].strip("-")


# -------------------------------------------------------
# Step 5 — Attempts a single POST request to the API endpoint.
# -------------------------------------------------------
# -------------------------------------------------------


def _post_chat_completion(api_url: str, prompt: str) -> Optional[str]:
    """Attempt a single POST to an OpenAI-compatible /v1/chat/completions endpoint.
    Returns the message content or None on failure.
    """

    # --- 9
    # Assign value to payload.
    # This establishes a key variable or state element used later in computation.
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
    # --- 10
    # Assign value to headers.
    # This establishes a key variable or state element used later in computation.
    headers = {"Authorization": f"Bearer {API_KEY}"}
    # --- 11
    # Enter try/except block.
    # This ensures that potential runtime errors are caught and handled gracefully.
    try:
        # --- 12
        # Assign value to response.
        # This establishes a key variable or state element used later in computation.
        response = requests.post(
            api_url, json=payload, headers=headers, timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        # --- 13
        # Return computed result.
        # This value contributes to the output or state transition within the logic flow.
        return response.json().get("choices", [{}])[0].get("message", {}).get("content")
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        # --- 14
        # Return computed result.
        # This value contributes to the output or state transition within the logic flow.
        return None


# -------------------------------------------------------
# Step 4 — Calls the LLM to generate the ADR content.
# -------------------------------------------------------
# -------------------------------------------------------


def call_llm(decision_idea: str) -> str:
    """Call the LLM to generate the ADR, trying primary URL then fallbacks."""

    # --- 15
    # Assign value to prompt.
    # This establishes a key variable or state element used later in computation.
    prompt = (
        "You're a software architect documenting design decisions.\n"
        "Given this summary:\n"
        f'"""{decision_idea}"""\n'
        "Write a full Architectural Decision Record (ADR) in Markdown format. Use this structure:\n"
        "Proposed\n"
        "Explain why this decision is being made now.\n"
        "Describe the architectural choice being made.\n"
        "List pros, cons, tradeoffs, or new risks.\n"
        "Make it concise and professional."
    )
    # --- 16
    # Assign value to content.
    # This establishes a key variable or state element used later in computation.
    content = _post_chat_completion(PRIMARY_API_URL, prompt)
    # --- 17
    # Evaluate conditional branch.
    # This controls logic flow and ensures that only valid conditions trigger downstream logic.
    if content:
        # --- 18
        # Return computed result.
        # This value contributes to the output or state transition within the logic flow.
        return content
    # --- 19
    # Iterate over a sequence in a controlled loop.
    # Each iteration processes an element relevant to the current computation scope.
    for url in FALLBACK_API_URLS:
        # --- 20
        # Assign value to content.
        # This establishes a key variable or state element used later in computation.
        content = _post_chat_completion(url, prompt)
        # --- 21
        # Evaluate conditional branch.
        # This controls logic flow and ensures that only valid conditions trigger downstream logic.
        if content:
            # --- 22
            # Return computed result.
            # This value contributes to the output or state transition within the logic flow.
            return content
    # --- 23
    # Return computed result.
    # This value contributes to the output or state transition within the logic flow.
    return "Failed to retrieve ADR from LLM (all endpoints failed)."


# -------------------------------------------------------
# Step 6 — Writes the generated ADR content to a file.
# -------------------------------------------------------
# -------------------------------------------------------


def main() -> None:
    """Main: gathers input, calls the LLM, and writes the ADR file."""

    # --- 24
    # Assign value to decision.
    # This establishes a key variable or state element used later in computation.
    decision = get_user_input()
    # --- 25
    # Evaluate conditional branch.
    # This controls logic flow and ensures that only valid conditions trigger downstream logic.
    if not decision:
        print("No input given. Exiting.")
        # --- 26
        # Return computed result.
        # This value contributes to the output or state transition within the logic flow.
        return
    # --- 27
    # Assign value to md_content.
    # This establishes a key variable or state element used later in computation.
    md_content = call_llm(decision)
    # --- 28
    # Assign value to timestamp.
    # This establishes a key variable or state element used later in computation.
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    # --- 29
    # Assign value to safe_name.
    # This establishes a key variable or state element used later in computation.
    safe_name = sanitize_filename(decision)
    # --- 30
    # Assign value to filename.
    # This establishes a key variable or state element used later in computation.
    filename = f"ADR-{timestamp}-{safe_name}.md"
    # --- 31
    # Assign value to output_path.
    # This establishes a key variable or state element used later in computation.
    output_path = OUTPUT_DIR / filename
    output_path.write_text(md_content, encoding="utf-8")
    print(f"ADR saved to {output_path.resolve()}")


# --- 32
# Evaluate conditional branch.
# This controls logic flow and ensures that only valid conditions trigger downstream logic.
if __name__ == "__main__":
    main()
