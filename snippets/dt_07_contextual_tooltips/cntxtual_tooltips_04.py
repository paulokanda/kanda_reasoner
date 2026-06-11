# contextual_tooltips_04/cntxtual_tooltips_04.py

import ast
from pathlib import Path

def extract_tooltip_candidates(file_path):
    """
    Extracts potential tooltip candidates from a given Python file.

    Args:
        file_path (Path): The path to the Python file to be analyzed.

    Returns:
        list of tuples: Each tuple contains the variable name, widget type, line number, and comment.
    """
    # ✅ Step 1.1: Execute block with context manager
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=str(file_path))

    tooltips = []

    # ✅ Step 1.2: Iterate over 'node'
    for node in ast.walk(tree):
        # ✅ Step 1.3: Check condition and execute block
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            func_name = getattr(node.value.func, "id", "") or getattr(
                getattr(node.value.func, "attr", ""), "id", ""
            )
            # ✅ Step 1.4: Check condition and execute block
            if func_name in [
                "QPushButton",
                "QCheckBox",
                "QComboBox",
                "QSlider",
                "QLabel",
            ]:
                var_name = (
                    node.targets[0].id
                    if isinstance(node.targets[0], ast.Name)
                    else "unknown"
                )
                # ✅ Step 1.5: Perform operation
                lineno = node.lineno
                comment = ast.get_docstring(node, clean=True) or "No comment"
                tooltips.append((var_name, func_name, lineno, comment))

    return tooltips

def main():
    """
    Main function to execute the script.
    Prompts the user for a file path, analyzes the file, and prints tooltip suggestions.
    """
    print(
        "📂 Enter path to your Qt/PyQt/PySide6 Python file (relative to EEG_KANDA/, e.g. k00_main/kanda_main.py):"
    )
    # ✅ Step 1.1: Handle file or configuration
    rel_input = input("> ").strip()

    # Detect EEG_KANDA root based on this script's location
    script_path = Path(__file__).resolve()
    eeg_kanda_root = script_path.parents[2]  # EEG_KANDA/

    file_path = eeg_kanda_root / rel_input

    # ✅ Step 1.2: Check condition and execute block
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return

    candidates = extract_tooltip_candidates(file_path)

    # ✅ Step 1.3: Check condition and execute block
    if not candidates:
        print("✅ No tooltip candidates found.")
    else:
        print("🧠 Tooltip Suggestions:")
        # ✅ Step 1.4: Iterate over 'items'
        for name, widget, line, comment in candidates:
            print(f"  - Line {line}: `{name}` ({widget}) → Tooltip: {comment}")

if __name__ == "__main__":
    main()
