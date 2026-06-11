# --- 1  Import module(s)
# [STRUCTURED:v1]
# [LOGIC:v1]

"""This module provides functionality to manage and verify AI API configurations within a Python project. It includes utilities to load the active API configuration from a file, check Python files for the correct API details, and test the integrity of AI patches by comparing expected configurations with actual file contents, while ignoring specified files. This ensures that all relevant files are correctly patched with the necessary API information."""
import ast

# --- 2  Import module(s)
import requests

# --- 3  Import specific symbol(s) from pathlib
from pathlib import Path

# --- 4  Assign value to API_URL
API_URL = "http://127.0.0.1:4433/v1/chat/completions"
# --- 5  Assign value to MODEL
MODEL = "WizardCoder-Python-13B-GGUF"
# --- 6  Assign value to API_KEY
API_KEY = "local-anything"
# --- 7  Assign value to OUTPUT_FILE
OUTPUT_FILE = Path(__file__).parent / "contract_suggestions.md"

# -------------------------------------------------------
# Step 1 — Extracts function definitions from the given source code.
# -------------------------------------------------------


def extract_function_definitions(source_code):
    """Extracts function definitions from the given source code."""
    # --- 9  Assign value to tree
    tree = ast.parse(source_code)
    # --- 10  Return computed result
    return [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]


# -------------------------------------------------------
# Step 2 — Asks a language model for contract suggestions for a given function name and code.
# -------------------------------------------------------


def ask_llm_for_contracts(fn_name, fn_code):
    """Asks a language model for contract suggestions for a given function name and code."""
    # --- 12  Assign value to prompt
    prompt = f"""
You are a Python expert.
Below is a function definition from an EEG Qt app using NumPy/SciPy. Your job is to infer its input/output expectations and propose pre-conditions, post-conditions, and validation logic (using asserts or type hints).
Function `{fn_name}`:
```python
{fn_code}
```
Return Markdown with:
-  Inferred Pre-Conditions
-  Inferred Post-Conditions
-  Suggested Type Hints or Runtime Guards
"""
    # --- 13  Assign value to response
    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You infer API contracts from Python functions.",
                },
                {"role": "user", "content": prompt},
            ],
        },
    )
    # --- 14  Return computed result
    return response.json()["choices"][0]["message"]["content"]


# -------------------------------------------------------
# Step 3 — Analyzes a Python module for function definitions and generates contract suggestions.
# -------------------------------------------------------


def analyze_module(path: Path):
    """Analyzes a Python module for function definitions and generates contract suggestions."""
    # --- 16  Assign value to source
    source = path.read_text(encoding="utf-8")
    # --- 17  Assign value to results
    results = []
    for fn in extract_function_definitions(source):
        # --- 18  Iterate over sequence in loop
        fn_code = ast.get_source_segment(source, fn)
        # --- 20  Assign value to name
        name = fn.name
        # --- 21  Assign value to suggestion
        suggestion = ask_llm_for_contracts(name, fn_code)
        # --- 22  Execute function call to results.append
        results.append(f"## Function `{name}` {suggestion}")
    # --- 23  Return computed result
    return results


# -------------------------------------------------------
# Step 4 — Main function to execute the script, taking a file path as an argument and writing contract suggestions to an output file.
# -------------------------------------------------------


def main():
    """Main function to execute the script, taking a file path as an argument and writing contract suggestions to an output file."""
    # --- 25  Import module(s)
    import sys

    if len(sys.argv) < 2:
        # --- 26  Evaluate conditional branch
        print("Usage: python api_cntrct_guards_03.py path/to/your_module.py")
        # --- 28  Return computed result
        return
    # --- 29  Assign value to target_file
    target_file = Path(sys.argv[1])
    if not target_file.exists():
        # --- 30  Evaluate conditional branch
        print(f" File not found: {target_file}")
        # --- 32  Return computed result
        return
    # --- 33  Assign value to all_results
    all_results = analyze_module(target_file)
    # --- 34  Execute function call to OUTPUT_FILE.write_text
    OUTPUT_FILE.write_text(
        "# API Contract Suggestions\n\n" + "\n\n---\n\n".join(all_results),
        encoding="utf-8",
    )
    # --- 35  Execute function call to print
    print(f" Contracts written to: {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    # --- 36  Evaluate conditional branch
    main()
