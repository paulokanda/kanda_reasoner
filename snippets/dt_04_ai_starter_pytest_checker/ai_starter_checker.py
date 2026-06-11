# dt_04_ai_starter_pytest_checker/ai_starter_checker.py

"""This module provides functionality to manage and verify AI API configurations within a Python project. It includes utilities to load the active API configuration from a file, check Python files for the correct API details, and test the integrity of AI patches by comparing expected configurations with actual file contents, while ignoring specified files. This ensures that all relevant files are correctly patched with the necessary API information."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent.parent

AI_STARTER = ROOT / "dev_tools/ai_starter"

ACTIVE_API_FILE = AI_STARTER / "active_api_url.txt"

DEV_TOOLS = ROOT / "dev_tools"

def load_active_api_config():
    """Loads the API_URL, MODEL, and API_KEY from the active_api_url.txt file."""

    if not ACTIVE_API_FILE.exists():
        raise FileNotFoundError("active_api_url.txt not found.")

    content = ACTIVE_API_FILE.read_text(encoding="utf-8")

    url = re.search(r'API_URL\s*=\s*"(.*?)"', content)

    model = re.search(r'MODEL\s*=\s*"(.*?)"', content)

    key = re.search(r'API_KEY\s*=\s*"(.*?)"', content)

    if not (url and model and key):
        raise ValueError("Missing API_URL, MODEL or API_KEY in active_api_url.txt.")

    return url.group(1), model.group(1), key.group(1)

def check_patched_files(expected_url, expected_model, expected_key):
    """Checks if all Python files in the DEV_TOOLS directory have the correct API_URL, MODEL, and API_KEY values."""

    mismatches = []

    for py_file in DEV_TOOLS.rglob("*.py"):
        if "API_URL" in py_file.read_text(encoding="utf-8"):
            content = py_file.read_text(encoding="utf-8")

            if (
                expected_url not in content
                or expected_model not in content
                or expected_key not in content
            ):
                mismatches.append(str(py_file.relative_to(ROOT)))

    return mismatches

def test_ai_patch_integrity():
    """Tests the integrity of AI patches by ensuring all relevant Python files have the correct API configuration."""

    url, model, key = load_active_api_config()

    mismatches = check_patched_files(url, model, key)

    ignore = {
        "dev_tools/ai_starter/start_blue_seek.py",
        "dev_tools/ai_starter_pytest_checker/ai_starter_checker.py",
    }

    mismatches = [m for m in mismatches if m.replace("\\", "/") not in ignore]
    assert not mismatches, f"Unpatched files found: {mismatches}"
