# dt_05_api_contract_guards/api_cntrct_guards_03.py

import ast
import requests
from pathlib import Path
API_URL = "http://127.0.0.1:4433/v1/chat/completions"
MODEL = "WizardCoder-Python-13B-GGUF"
API_KEY = "local-anything"
OUTPUT_FILE = Path(__file__).parent / "contract_suggestions.md"
def extract_function_definitions(source_code):
    """Extracts function definitions from the given source code."""
    tree = ast.parse(source_code)
    return [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
def ask_llm_for_contracts(fn_name, fn_code):
    """Asks a language model for contract suggestions for a given function name and code."""
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
    response = requests.post(API_URL, headers={
        "Authorization": f"Bearer {API_KEY}"
    }, json={
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You infer API contracts from Python functions."},
            {"role": "user", "content": prompt}
        ]
    })
    return response.json()["choices"][0]["message"]["content"]
def analyze_module(path: Path):
    """Analyzes a Python module for function definitions and generates contract suggestions."""
    source = path.read_text(encoding="utf-8")
    results = []
    for fn in extract_function_definitions(source):
        fn_code = ast.get_source_segment(source, fn)
        name = fn.name
        suggestion = ask_llm_for_contracts(name, fn_code)
        results.append(f"## Function `{name}` {suggestion}")
    return results
def main():
    """Main function to execute the script, taking a file path as an argument and writing contract suggestions to an output file."""
    import sys
    if len(sys.argv) < 2:
        print("Usage: python api_cntrct_guards_03.py path/to/your_module.py")
        return
    target_file = Path(sys.argv[1])
    if not target_file.exists():
        print(f" File not found: {target_file}")
        return
    all_results = analyze_module(target_file)
    OUTPUT_FILE.write_text("# API Contract Suggestions\n\n" + "\n\n---\n\n".join(all_results), encoding="utf-8")
    print(f" Contracts written to: {OUTPUT_FILE.resolve()}")
if __name__ == "__main__":
    main()
