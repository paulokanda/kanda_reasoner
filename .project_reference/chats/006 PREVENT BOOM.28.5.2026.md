Python Path Provenance Audit Plan

We need to create a snippet of code to insert in the main initial prompt that forbids the use of BOM (Byte Order Mark) in Python modules. The user wants to enforce that no BOM characters are present in Python files, likely as a pre-commit hook, validation check, or as part of the project's initialization or CI process.

The instruction: "create a snippet of code to insert in main initial prompt forbidden use of BOM in modules of python files". Could be interpreted as: add code at the beginning of the main script that checks for BOM in Python modules and prevents execution or raises an error if found.

Alternatively, could be a prompt to include in the project setup to inform contributors not to use BOM. But likely the user wants a Python code snippet that scans all Python files in the project and forbids/errors if any BOM is found.

I'll provide a robust snippet that can be placed at the start of the main script (e.g., just after imports) to recursively check all .py files in the project directory (or a specified directory) for BOM (UTF-8 BOM \xef\xbb\xbf or other encodings) and exit with an error if any are found. Include an option to skip certain directories like __pycache__, .git, venv, etc.

Also mention how to use it in a pre-commit hook or CI.

Will produce the code with comments explaining what it does.

Below is a ready‑to‑insert code snippet that you can place at the very beginning of your main Python script (after imports) to forbid any Python module from containing a BOM (Byte Order Mark). If a BOM is found in any .py file within your project, the script will print an error and exit with code 1 (preventing further execution).

This is useful for enforcing UTF‑8 without BOM across your entire codebase, especially in team environments or CI pipelines.
Snippet – BOM Checker (place early in main() or at module level)
python

import sys
from pathlib import Path

def forbid_bom_in_python_modules(root_dir: str = ".") -> None:
    """
    Recursively scan all .py files under root_dir.
    If any file starts with a UTF-8 BOM (EF BB BF), print error and exit.
    Skips common non-source directories: __pycache__, .git, venv, env, .venv, dist, build, etc.
    """
    root = Path(root_dir).resolve()
    # Directories to ignore (common for virtual envs, cache, version control)
    ignore_dirs = {
        "__pycache__", ".git", ".hg", ".svn", 
        "venv", "env", ".venv", ".env", 
        "dist", "build", ".mypy_cache", ".pytest_cache", 
        ".tox", ".eggs", "node_modules"
    }
    
    bom_found = False
    for py_file in root.rglob("*.py"):
        # Skip ignored directories
        if any(part in ignore_dirs for part in py_file.parts):
            continue
        # Check first 3 bytes for UTF-8 BOM
        with open(py_file, "rb") as f:
            first_bytes = f.read(3)
            if first_bytes == b'\xef\xbb\xbf':
                print(f"❌ BOM forbidden: {py_file}")
                bom_found = True
    
    if bom_found:
        print("\nERROR: One or more Python files contain a UTF-8 Byte Order Mark (BOM).")
        print("Please save all .py files as UTF-8 WITHOUT BOM. (Use 'utf-8' encoding, not 'utf-8-sig')")
        sys.exit(1)

# -------------------------
# Insert this call at the start of your main execution
# (after imports, before any real logic)
if __name__ == "__main__":
    forbid_bom_in_python_modules(".")   # scan current directory and subdirs
    # ... rest of your main code

How to integrate into an existing main script

Place the function definition at the top (or in a utils module), then call it immediately after argument parsing or at the very beginning of your main():
python

def main():
    # Enforce no-BOM rule before anything else
    forbid_bom_in_python_modules(".")
    
    # Your real application code here ...

If you want it to run unconditionally even when the script is imported, you can move the call outside the if __name__ == "__main__": block (but that would fire on every import – not recommended for libraries).
Bonus: Pre‑commit hook version (for .pre-commit-config.yaml)

Add this to your repository’s pre‑commit configuration (no need to insert into main script):
yaml

- repo: local
  hooks:
    - id: forbid-bom
      name: Forbid UTF-8 BOM in Python files
      entry: python -c "import sys; from pathlib import Path; sys.exit(any(p.read_bytes().startswith(b'\xef\xbb\xbf') for p in Path('.').rglob('*.py') if not any(d in p.parts for d in ['__pycache__','.git','venv'])))"
      language: system
      files: \.py$

Why this snippet is effective

    Stops execution early – prevents corrupted BOM‑containing modules from being imported or causing SyntaxError later.

    Ignores virtual environments – avoids scanning venv, .env, etc., where third‑party modules might legitimately have BOMs (rare but possible).

    Explicit error message – tells the developer exactly which file(s) are wrong and how to fix them.

    Zero dependencies – uses only pathlib and standard library.

Insert this snippet once at the start of your main entry point, and your project will be automatically protected against accidental BOM insertion.
create a prompt asking creation of file without bom ,  canonical = no BOM

We need to create a prompt that asks for creation of a file without BOM, specifying "canonical = no BOM". The user wants a prompt to be given to an AI (like me) or to a code generator to ensure that when a file is created, it is saved without a UTF-8 BOM. The prompt should be clear and include the requirement "canonical = no BOM". I'll write a concise instruction prompt.

Here's a clear, instruction‑style prompt you can use to request creation of a file without a BOM, explicitly referencing the canonical standard:
Prompt: "Create a file without BOM (canonical = no BOM)"
text

Create the following file with UTF-8 encoding, but DO NOT include a Byte Order Mark (BOM). 
Use the canonical UTF-8 format: no BOM at the beginning of the file.

File path: [INSERT PATH]
File content: [INSERT CONTENT OR DESCRIPTION]

Requirements:
- Encoding: UTF-8 without BOM (canonical = no BOM)
- No U+FEFF character at the start
- Ensure any writing operation uses 'utf-8' (not 'utf-8-sig')
- If you generate code that writes this file, the code must use open(file, 'w', encoding='utf-8')
- Verify that the first three bytes are NOT EF BB BF

Example usage

If you are asking an AI (like me) to generate the file or the code to write it:

    Prompt to AI:
    *"Create a Python script that writes a configuration file called 'config.json' with the content {"version": 1}. Use UTF-8 encoding without BOM (canonical = no BOM). Ensure no Byte Order Mark is written."*

The AI should produce code like:
python

with open('config.json', 'w', encoding='utf-8') as f:
    f.write('{"version": 1}')

For batch file creation (e.g., via a script)

If you need to instruct a tool or a team member:

    *"All source files in this project MUST be saved as UTF-8 without BOM.
    Canonical UTF-8 = no BOM. Use encoding='utf-8' when writing files, never utf-8-sig.
    Existing BOMs must be removed (strip \xef\xbb\xbf bytes)."*

This prompt clearly communicates the requirement and leaves no ambiguity about the canonical form.
