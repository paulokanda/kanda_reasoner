# gui_specs_10/gui_specs_10.py

import ast
from pathlib import Path

def extract_gui_sequence(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=str(file_path))

    steps = []

    class Visitor(ast.NodeVisitor):
        def visit_Call(self, node):
            try:
                func_name = getattr(node.func, "attr", None)
                if func_name in ("show", "setVisible", "setText", "setChecked", "setCurrentIndex"):
                    widget = ast.unparse(node.func.value)
                    steps.append(f"{widget}.{func_name}()")
            except Exception:
                pass
            self.generic_visit(node)

    Visitor().visit(tree)
    return steps

def main():
    path = input("📂 Enter Qt/PyQt/PySide6 file path (relative to EEG_KANDA/): ").strip()
    full_path = Path("EEG_KANDA") / path

    if not full_path.exists():
        print(f"❌ File not found: {full_path}")
        return

    steps = extract_gui_sequence(full_path)
    if steps:
        print("🧪 GUI Flow (inferred):")
        for i, step in enumerate(steps, 1):
            print(f"  {i}. {step}")
    else:
        print("✅ No major GUI actions detected.")

if __name__ == "__main__":
    main()
