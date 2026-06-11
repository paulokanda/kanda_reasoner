#!/usr/bin/env python3
"""
GUI tool to generate/update __init__.py with module map for a Python project.
Extracts public symbols (functions, classes, top-level variables) from .py files.
Merges with existing __init__.py content.
Optionally generates a top-level README.md and/or ARCHITECTURE.md.
"""

import ast
import sys
import traceback
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QFileDialog, QMessageBox, QCheckBox, QProgressBar
)
from PySide6.QtCore import QThread, Signal, QObject


# ---------- Helper functions for parsing ----------

def find_public_symbols(filepath):
    """Extract public functions, classes, and top-level variable names not starting with '_'."""
    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read(), filename=filepath)
        except SyntaxError:
            return set()

    symbols = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            if not node.name.startswith('_'):
                symbols.add(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and not target.id.startswith('_'):
                    symbols.add(target.id)
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and not node.target.id.startswith('_'):
                symbols.add(node.target.id)
    return symbols


def parse_existing_init(filepath):
    """
    Read an existing __init__.py and extract:
    - docstring (string or None)
    - list of import statements (as they appear in the source)
    - existing __all__ (as a set of strings)
    - existing __module_map__ (as a dict)
    - other lines (strings) that are not part of the above
    """
    if not filepath.exists():
        return None, [], set(), {}, []

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    try:
        tree = ast.parse(content, filename=filepath)
    except SyntaxError:
        return None, [], set(), {}, content.splitlines(keepends=True)

    docstring = ast.get_docstring(tree)

    # Extract import statements (as original text) using line numbers
    lines = content.splitlines(keepends=True)
    import_lines = []
    other_lines = []
    import_ranges = set()

    def add_lines(node):
        if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
            for i in range(node.lineno - 1, node.end_lineno):
                import_ranges.add(i)

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            add_lines(node)

    all_assign = None
    map_assign = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    if target.id == '__all__':
                        all_assign = node
                        add_lines(node)
                    elif target.id == '__module_map__':
                        map_assign = node
                        add_lines(node)

    for i, line in enumerate(lines):
        if i in import_ranges:
            import_lines.append(line)
        else:
            other_lines.append(line)

    existing_all = set()
    if all_assign is not None:
        try:
            val = ast.literal_eval(all_assign.value)
            if isinstance(val, list):
                existing_all = set(val)
        except (ValueError, SyntaxError):
            pass

    existing_module_map = {}
    if map_assign is not None:
        try:
            val = ast.literal_eval(map_assign.value)
            if isinstance(val, dict):
                existing_module_map = val
        except (ValueError, SyntaxError):
            pass

    return docstring, import_lines, existing_all, existing_module_map, other_lines


def generate_init_content(folder, symbols_by_file, existing_docstring,
                          existing_imports, existing_all, existing_module_map, other_lines):
    """Generate the full content for __init__.py."""
    auto_imports = []
    new_module_map = {}
    new_all = set()

    for rel_path, symbols in symbols_by_file.items():
        if not symbols:
            continue
        import_path = f'.{rel_path}'
        auto_imports.append(f'from {import_path} import {", ".join(symbols)}')
        for sym in symbols:
            new_module_map[sym] = str(rel_path)
        new_all.update(symbols)

    final_all = existing_all.union(new_all)
    final_module_map = {**existing_module_map, **new_module_map}

    existing_imports_set = set(existing_imports)
    final_imports = auto_imports + [imp for imp in existing_imports if imp not in auto_imports]

    lines = []
    if existing_docstring:
        lines.append(f'"""{existing_docstring}"""')
    else:
        lines.append('"""Auto-generated __init__.py - maps public symbols to source files."""')
    lines.append('')

    if final_imports:
        lines.extend(final_imports)
        lines.append('')

    lines.append(f'__all__ = {sorted(final_all)}')
    lines.append('')

    lines.append(f'__module_map__ = {final_module_map}')
    lines.append('')

    if other_lines:
        lines.append('# --- Preserved custom code ---')
        lines.extend(other_lines)

    return '\n'.join(lines)


# ---------- Data structures ----------
class PackageInfo:
    """Summary info for a package (used in README)."""
    def __init__(self, rel_path, init_docstring, public_symbols):
        self.rel_path = rel_path
        self.init_docstring = init_docstring
        self.public_symbols = public_symbols


class ModuleInfo:
    """Detailed info for a module (file) within a package (used in ARCHITECTURE)."""
    def __init__(self, rel_path, symbols):
        self.rel_path = rel_path        # relative to package folder
        self.symbols = symbols


class PackageDetail:
    """Detailed info for a package (used in ARCHITECTURE)."""
    def __init__(self, rel_path, init_docstring, modules):
        self.rel_path = rel_path
        self.init_docstring = init_docstring
        self.modules = modules           # list of ModuleInfo


# ---------- Worker class ----------
class Worker(QObject):
    finished = Signal()
    log = Signal(str)
    progress = Signal(int)

    def __init__(self, root_path, dry_run, generate_readme, generate_architecture):
        super().__init__()
        self.root_path = root_path
        self.dry_run = dry_run
        self.readme_flag = generate_readme        # renamed to avoid conflict
        self.arch_flag = generate_architecture    # renamed
        self.packages = []          # PackageInfo for README
        self.package_details = []   # PackageDetail for ARCHITECTURE

    def process_folder(self, folder):
        """Generate or update __init__.py for a single folder."""
        init_path = folder / '__init__.py'
        py_files = [f for f in folder.glob('*.py')
                    if f.name != '__init__.py' and not f.name.startswith('_')]

        if not py_files:
            return

        symbols_by_file = {}
        for py_file in py_files:
            symbols = find_public_symbols(py_file)
            if symbols:
                rel_path = py_file.relative_to(folder).with_suffix('')
                symbols_by_file[rel_path] = symbols

        if not symbols_by_file:
            return

        # Parse existing __init__.py
        existing_docstring, existing_imports, existing_all, existing_module_map, other_lines = \
            parse_existing_init(init_path)

        # Generate new content
        new_content = generate_init_content(
            folder, symbols_by_file,
            existing_docstring, existing_imports, existing_all, existing_module_map, other_lines
        )

        if self.dry_run:
            self.log.emit(f"[DRY RUN] Would update {init_path}")
            preview = '\n'.join(new_content.splitlines()[:10])
            if len(new_content.splitlines()) > 10:
                preview += '\n...'
            self.log.emit(f"Preview:\n{preview}\n")
        else:
            try:
                with open(init_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                self.log.emit(f"Updated: {init_path}")
            except Exception as e:
                self.log.emit(f"ERROR writing {init_path}: {e}")

        # Collect data for README and ARCHITECTURE
        try:
            rel_path = folder.relative_to(self.root_path)
            final_all = existing_all.union({sym for syms in symbols_by_file.values() for sym in syms})
            self.packages.append(PackageInfo(str(rel_path), existing_docstring, sorted(final_all)))

            # Build detailed module list for this package
            modules = []
            for rel_mod_path, syms in symbols_by_file.items():
                modules.append(ModuleInfo(str(rel_mod_path), sorted(syms)))
            self.package_details.append(PackageDetail(str(rel_path), existing_docstring, modules))
        except Exception as e:
            self.log.emit(f"ERROR collecting package info for {folder}: {e}")

    def generate_readme(self):
        """Generate README.md at the project root."""
        root = Path(self.root_path)
        readme_path = root / 'README.md'

        lines = []
        lines.append(f"# {root.name}\n")
        lines.append("This project was structured using the **__module_map__** pattern to help AI assistants and developers locate code quickly.\n")
        lines.append("## Package Structure\n")
        lines.append("Each subfolder that contains Python files has an `__init__.py` that re‑exports all public symbols and provides a `__module_map__` dictionary mapping each symbol to its source file.\n")

        if self.packages:
            lines.append("| Package | Public Symbols | Description |")
            lines.append("|---------|----------------|-------------|")
            for pkg in self.packages:
                symbols = ', '.join(pkg.public_symbols) if pkg.public_symbols else '*none*'
                desc = pkg.init_docstring or ''
                desc = desc.replace('|', '\\|')
                lines.append(f"| `{pkg.rel_path}` | {symbols} | {desc} |")
        else:
            lines.append("No packages with public symbols found.\n")

        lines.append("\n## How AI Can Use This Structure\n")
        lines.append("- Each `__init__.py` re‑exports all public symbols from its folder.\n")
        lines.append("- The `__module_map__` dictionary maps every public symbol directly to the file where it is defined.\n")
        lines.append("- AI assistants can inspect `__init__.py` to locate any symbol without guessing.\n")
        lines.append("- This structure is self‑documenting and follows Python best practices.\n")

        lines.append("\n## Generated by the __init__.py Generator Tool\n")
        lines.append("This `README.md` was automatically generated. You can re‑run the tool to update it after changes.\n")

        content = '\n'.join(lines)

        if self.dry_run:
            self.log.emit("[DRY RUN] Would generate README.md")
            preview = '\n'.join(content.splitlines()[:20])
            if len(content.splitlines()) > 20:
                preview += '\n...'
            self.log.emit(f"Preview:\n{preview}\n")
        else:
            try:
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.log.emit(f"Generated: {readme_path}")
            except Exception as e:
                self.log.emit(f"ERROR writing README.md: {e}")

    def generate_architecture(self):
        """Generate ARCHITECTURE.md at the project root."""
        root = Path(self.root_path)
        arch_path = root / 'ARCHITECTURE.md'

        lines = []
        lines.append(f"# Architecture of {root.name}\n")
        lines.append("This document provides a structural overview of the project. It lists every package, its modules, and the public symbols each module exports. Use this to understand where responsibilities live and which file owns what.\n")
        lines.append("## Packages and Modules\n")

        if self.package_details:
            for pkg in self.package_details:
                # Package heading
                if pkg.rel_path == '.':
                    pkg_name = f"{root.name} (root package)"
                else:
                    pkg_name = pkg.rel_path
                lines.append(f"### `{pkg_name}`")
                if pkg.init_docstring:
                    lines.append(f"*{pkg.init_docstring}*")
                lines.append("")

                # List modules
                if pkg.modules:
                    lines.append("| Module File | Public Symbols |")
                    lines.append("|-------------|----------------|")
                    for mod in sorted(pkg.modules, key=lambda m: m.rel_path):
                        symbols = ', '.join(mod.symbols)
                        lines.append(f"| `{mod.rel_path}.py` | {symbols} |")
                else:
                    lines.append("*No public modules in this package.*")
                lines.append("")
        else:
            lines.append("No packages with public symbols found.\n")

        lines.append("## How to Use This Index\n")
        lines.append("- Each `__init__.py` re‑exports all public symbols and includes a `__module_map__` dictionary that maps each symbol to its source file.\n")
        lines.append("- You can quickly locate any symbol by searching the `__module_map__` in the relevant package.\n")
        lines.append("- This document is automatically updated whenever the project structure changes.\n")

        content = '\n'.join(lines)

        if self.dry_run:
            self.log.emit("[DRY RUN] Would generate ARCHITECTURE.md")
            preview = '\n'.join(content.splitlines()[:20])
            if len(content.splitlines()) > 20:
                preview += '\n...'
            self.log.emit(f"Preview:\n{preview}\n")
        else:
            try:
                with open(arch_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.log.emit(f"Generated: {arch_path}")
            except Exception as e:
                self.log.emit(f"ERROR writing ARCHITECTURE.md: {e}")

    def run(self):
        """Main processing routine."""
        try:
            root = Path(self.root_path)
            if not root.is_dir():
                self.log.emit("Invalid folder path.")
                return

            # Gather all subfolders (including root)
            folders = [root] + [d for d in root.rglob('*') if d.is_dir()]
            total = len(folders)
            self.log.emit(f"Found {total} folders to process.")

            for idx, folder in enumerate(folders):
                self.progress.emit(int(100 * idx / total))
                self.log.emit(f"Processing {folder.relative_to(root)} ...")
                try:
                    self.process_folder(folder)
                except Exception as e:
                    self.log.emit(f"ERROR in folder {folder}: {e}")
                    self.log.emit(traceback.format_exc())

            if self.readme_flag:
                self.generate_readme()
            if self.arch_flag:
                self.generate_architecture()

            self.progress.emit(100)
            self.log.emit("\nProcessing complete.")
        except Exception as e:
            self.log.emit(f"UNEXPECTED ERROR: {e}")
            self.log.emit(traceback.format_exc())
        finally:
            self.finished.emit()


# ---------- GUI Main Window ----------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("__init__.py Generator with Module Map & README/ARCHITECTURE")
        self.setMinimumSize(700, 500)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Folder selection
        folder_layout = QHBoxLayout()
        self.folder_path_edit = QTextEdit()
        self.folder_path_edit.setPlaceholderText("No folder selected")
        self.folder_path_edit.setMaximumHeight(50)
        self.folder_path_edit.setReadOnly(True)
        self.select_button = QPushButton("Select Project Folder")
        self.select_button.clicked.connect(self.select_folder)
        folder_layout.addWidget(self.folder_path_edit)
        folder_layout.addWidget(self.select_button)
        layout.addLayout(folder_layout)

        # Options
        options_layout = QHBoxLayout()
        self.dry_run_check = QCheckBox("Dry run (only preview, no files written)")
        self.generate_readme_check = QCheckBox("Generate README.md (project overview)")
        self.generate_readme_check.setChecked(True)
        self.generate_arch_check = QCheckBox("Generate ARCHITECTURE.md (structural index)")
        self.generate_arch_check.setChecked(True)
        options_layout.addWidget(self.dry_run_check)
        options_layout.addWidget(self.generate_readme_check)
        options_layout.addWidget(self.generate_arch_check)
        layout.addLayout(options_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Log area
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        # Start button
        self.start_button = QPushButton("Generate/Update __init__.py files")
        self.start_button.clicked.connect(self.start_processing)
        self.start_button.setEnabled(False)
        layout.addWidget(self.start_button)

        self.worker = None
        self.thread = None

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Project Folder")
        if folder:
            self.folder_path_edit.setPlainText(folder)
            self.start_button.setEnabled(True)

    def start_processing(self):
        folder = self.folder_path_edit.toPlainText().strip()
        if not folder:
            QMessageBox.warning(self, "No Folder", "Please select a project folder first.")
            return

        dry_run = self.dry_run_check.isChecked()
        generate_readme = self.generate_readme_check.isChecked()
        generate_architecture = self.generate_arch_check.isChecked()

        self.start_button.setEnabled(False)
        self.select_button.setEnabled(False)
        self.progress_bar.setValue(0)
        self.log_text.clear()

        self.thread = QThread()
        self.worker = Worker(folder, dry_run, generate_readme, generate_architecture)
        self.worker.moveToThread(self.thread)

        self.worker.log.connect(self.log_text.append)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self.on_processing_finished)
        self.thread.started.connect(self.worker.run)

        self.thread.start()

    def on_processing_finished(self):
        self.thread.quit()
        self.thread.wait()
        self.worker.deleteLater()
        self.thread.deleteLater()

        self.start_button.setEnabled(True)
        self.select_button.setEnabled(True)
        QMessageBox.information(self, "Done", "Processing finished.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())