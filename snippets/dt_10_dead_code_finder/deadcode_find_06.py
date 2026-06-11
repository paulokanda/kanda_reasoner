import ast
from pathlib import Path

def find_dead_code(file_path):
    """
    Analyzes a Python file to find potentially unused functions.

    Args:
        file_path (Path): The path to the Python file to analyze.

    Returns:
        set: A set of function names that are defined but not called within the file.
    """
    # ✅ Step 1.2: Execute block with context manager
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()
    # ✅ Step 1.1: Handle file or configuration
    tree = ast.parse(source, filename=str(file_path))

    defined_funcs = set()
    called_funcs = set()

    class FuncVisitor(ast.NodeVisitor):
        """
        A visitor class to traverse the AST and collect defined and called function names.
        """

        def visit_FunctionDef(self, node):
            """
            Collects the name of each defined function.

            Args:
                node (ast.FunctionDef): The function definition node.
            """
            # ✅ Step 1.1: Perform operation
            defined_funcs.add(node.name)
            self.generic_visit(node)

        def visit_Call(self, node):
            """
            Collects the name of each called function.

            Args:
                node (ast.Call): The function call node.
            """
            # ✅ Step 1.1: Check condition and execute block
            if isinstance(node.func, ast.Name):
                called_funcs.add(node.func.id)
            self.generic_visit(node)

    FuncVisitor().visit(tree)
    dead = defined_funcs - called_funcs
    return dead

def main():
    """
    Main function to prompt the user for a file path, analyze the file for unused functions,
    and print the results.
    """
    print(
        "📂 Enter path to your Python module (relative to EEG_KANDA/, e.g. k00_main/kanda_main.py):"
    )
    # ✅ Step 1.1: Handle file or configuration
    rel_path = input("> ").strip()
    project_root = Path(__file__).resolve().parents[2]
    file_path = project_root / rel_path

    # ✅ Step 1.2: Check condition and execute block
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return

    dead_funcs = find_dead_code(file_path)
    # ✅ Step 1.3: Check condition and execute block
    if dead_funcs:
        print("🧹 Possibly unused functions:")
        # ✅ Step 1.4: Iterate over 'f'
        for f in dead_funcs:
            print(f"  - {f}")
    else:
        print("✅ No unused functions found.")

if __name__ == "__main__":
    main()
