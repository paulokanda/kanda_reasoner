# dt_03_ai_starter/start_blue_seek.py

"""
This module automates the process of identifying a running Blueseek API, updating scripts with the new API URL, MODEL, and API_KEY, and storing the URL in a file. It is designed to streamline the configuration of a Python project to interact with a dynamically located Blueseek API.
"""
import subprocess
import re
from pathlib import Path

# --- 1
# Assign value to ROOT.
# This establishes a key variable or state element used later in computation.
ROOT = Path(__file__).resolve().parent.parent.parent
# --- 2
# Assign value to OUTPUT_PATH.
# This establishes a key variable or state element used later in computation.
OUTPUT_PATH = ROOT / "ai_starter/active_api_url.txt"
# --- 3
# Assign value to MODEL.
# This establishes a key variable or state element used later in computation.
MODEL = "WizardCoder-Python-13B-GGUF"
# --- 4
# Assign value to API_KEY.
# This establishes a key variable or state element used later in computation.
API_KEY = "local-anything"

# -------------------------------------------------------
# Step 2 — Scans running processes to identify the Blueseek API URL. Critical for detecting the active API server.
# -------------------------------------------------------


def find_running_api_url():
    """Scans running processes for a Blueseek API port and returns the URL if the API is responding."""

    print("Scanning running processes for Blueseek API port...")
    # --- 5
    # Assign value to process.
    # This establishes a key variable or state element used later in computation.
    process = subprocess.Popen(
        ["netstat", "-ano"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    # --- 6
    # Assign value to ports.
    # This establishes a key variable or state element used later in computation.
    ports = set()
    # --- 7
    # Iterate over a sequence in a controlled loop.
    # Each iteration processes an element relevant to the current computation scope.
    for line in process.stdout:
        # --- 8
        # Assign value to match.
        # This establishes a key variable or state element used later in computation.
        match = re.search(r"127\.0\.0\.1:(\d+).*LISTENING", line)
        # --- 9
        # Evaluate conditional branch.
        # This controls logic flow and ensures that only valid conditions trigger downstream logic.
        if match:
            ports.add(match.group(1))
    # --- 10
    # Iterate over a sequence in a controlled loop.
    # Each iteration processes an element relevant to the current computation scope.
    for port in sorted(ports):
        # --- 11
        # Assign value to test_url.
        # This establishes a key variable or state element used later in computation.
        test_url = f"http://127.0.0.1:{port}/v1/chat/completions"
        # --- 12
        # Enter try/except block.
        # This ensures that potential runtime errors are caught and handled gracefully.
        try:
            import requests

            # --- 13
            # Assign value to r.
            # This establishes a key variable or state element used later in computation.
            r = requests.post(
                test_url,
                json={
                    "model": MODEL,
                    "messages": [{"role": "user", "content": "ping"}],
                },
                timeout=2,
            )
            # --- 14
            # Evaluate conditional branch.
            # This controls logic flow and ensures that only valid conditions trigger downstream logic.
            if r.status_code == 200:
                # --- 15
                # Return computed result.
                # This value contributes to the output or state transition within the logic flow.
                return test_url
        except Exception:
            continue
    # --- 16
    # Return computed result.
    # This value contributes to the output or state transition within the logic flow.
    return None


# -------------------------------------------------------
# Step 3 — Updates Python scripts with the new API URL, MODEL, and API_KEY. Essential for configuration consistency.
# -------------------------------------------------------


def patch_scripts(api_url):
    """Patches Python scripts in the project with the new API URL, MODEL, and API_KEY."""

    print("Patching dev_tools with new API_URL...")
    # --- 17
    # Iterate over a sequence in a controlled loop.
    # Each iteration processes an element relevant to the current computation scope.
    for path in ROOT.glob("**/*.py"):
        # --- 18
        # Evaluate conditional branch.
        # This controls logic flow and ensures that only valid conditions trigger downstream logic.
        if path.name == "start_blue_seek.py":
            continue
        # --- 19
        # Assign value to text.
        # This establishes a key variable or state element used later in computation.
        text = path.read_text(encoding="utf-8")
        # --- 20
        # Evaluate conditional branch.
        # This controls logic flow and ensures that only valid conditions trigger downstream logic.
        if "API_URL" in text and "/v1/chat/completions" in text:
            # --- 21
            # Assign value to backup_path.
            # This establishes a key variable or state element used later in computation.
            backup_path = path.with_suffix(".py.bak")
            backup_path.write_text(text, encoding="utf-8")
            # --- 22
            # Assign value to new_text.
            # This establishes a key variable or state element used later in computation.
            new_text = re.sub(r'API_URL\s*=\s*".*?"', f'API_URL = "{api_url}"', text)
            # --- 23
            # Assign value to new_text.
            # This establishes a key variable or state element used later in computation.
            new_text = re.sub(r'MODEL\s*=\s*".*?"', f'MODEL = "{MODEL}"', new_text)
            # --- 24
            # Assign value to new_text.
            # This establishes a key variable or state element used later in computation.
            new_text = re.sub(
                r'API_KEY\s*=\s*".*?"', f'API_KEY = "{API_KEY}"', new_text
            )
            path.write_text(new_text, encoding="utf-8")
            print(f"Patched: {path.relative_to(ROOT)}")


# -------------------------------------------------------
# Step 1 — Orchestrates the entire process by invoking the API URL detection and script patching.
# -------------------------------------------------------


def main():
    """Finds the running API URL, writes it to a file, and patches relevant scripts with the new API URL."""

    # --- 25
    # Assign value to api_url.
    # This establishes a key variable or state element used later in computation.
    api_url = find_running_api_url()
    # --- 26
    # Evaluate conditional branch.
    # This controls logic flow and ensures that only valid conditions trigger downstream logic.
    if api_url:
        OUTPUT_PATH.write_text(
            f'API_URL = "{api_url}"\nMODEL = "{MODEL}"\nAPI_KEY = "{API_KEY}"\n',
            encoding="utf-8",
        )
        print(f"API connected: {api_url}")
        print(f"Written to: {OUTPUT_PATH.resolve()}")
        patch_scripts(api_url)
    else:
        print("Could not detect a running local AI server.")


# --- 27
# Evaluate conditional branch.
# This controls logic flow and ensures that only valid conditions trigger downstream logic.
if __name__ == "__main__":
    main()
