import ast
import sys
from pathlib import Path
import requests

API_URL = "http://127.0.0.1:4433/v1/chat/completions"
MODEL = "WizardCoder-Python-13B-GGUF"
API_KEY = "local-anything"

def extract_functions_for_testing(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=str(file_path))

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            args = [arg.arg for arg in node.args.args]
            functions.append((node.name, args, ast.get_docstring(node)))
    return functions

def ask_llm_for_property_tests(functions):
    prompt = "Generate Hypothesis property-based tests for the following EEG-related functions:

"
    for name, args, doc in functions:
        prompt += f"### Function: {name}({', '.join(args)})
"
        if doc:
            prompt += f"Docstring: {doc}
"
    prompt += "\nRespond with test functions in Python."

    response = requests.post(API_URL, headers={
        "Authorization": f"Bearer {API_KEY}"
    }, json={
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a Python test generation assistant."},
            {"role": "user", "content": prompt}
        ]
    })

    try:
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Failed to parse response: {e}\nRaw: {response.text}"

def main():
    path = input("📂 Enter Python file to analyze (relative to EEG_KANDA/): ").strip()
    file_path = Path("EEG_KANDA") / path
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return

    funcs = extract_functions_for_testing(file_path)
    if not funcs:
        print("✅ No functions found.")
        return

    print("🤖 Asking LLM to generate property-based tests...")
    result = ask_llm_for_property_tests(funcs)
    print("🧪 Generated Tests:\n")
    print(result)

if __name__ == "__main__":
    main()
