I know parts of it well, but not the whole repository exhaustively.

From this session, I now have a solid working picture of the startup/UI path around:
EEGVisualizerCore
EEGMainWindowBuilder
eeg_display_launcher
SignalManager
MemoryManager
snapshot reset/capture flow
splash creation and path resolution
navbar SVG controls
filter lane / middle toolbar wiring
EEG Traces tab loading/unloading
timeline attachment and both timeline manager layers
tooltip hover infrastructure
some HDF5 folder/file creation pieces
some montage/table/statistics imports that were involved in the startup crash tracing

So I understand the structure well enough to keep debugging and refactoring this startup/UI slice with continuity.

But I do not yet know the entire project architecture end-to-end in the sense of:
every package
every plugin
all data pipelines
all storage flows
all rendering modes
all tab modules
all deprecated/current overlaps
all cross-module dependencies

What I know is a partial but meaningful map, not a full repo-wide map.

A fair summary is:
I know the current boot chain and several connected subsystems well.
I do not yet know the entire repository comprehensively.

If you want, the next productive step is to build a precise repo map module-by-module from the current codebase, so we stop working only reactively and start with a stable architectural overview.

eeg_dayly_reporter_daily_refactor_report_bundle.json
File
eeg_kernel_migration.json
File
does json gives you  a full understanding of app?
Thought for 10s

Não por si só.

Esses JSONs ajudam muito, mas não dão entendimento completo do app.

O eeg_dayly_reporter_daily_refactor_report_bundle.json parece ser um bundle de estado/refatoração incremental, com snapshot arquitetural, histórico de mudanças, hotspots, dependências tocadas e projeções de próximos riscos. Ele próprio mostra que vários blocos derivados estão ausentes, como dependency_graph, project_snapshot, stability_analysis, symbol_churn e symbol_index, marcados como missing.

Já o eeg_kernel_migration.json parece muito mais um índice estrutural e histórico de chamadas cruzadas de módulos/funções do processo de migração e ferramentas associadas, não uma descrição semântica completa do comportamento real da aplicação em execução. Além disso, o conteúdo visível está truncado, então ele claramente não é uma visão autoexplicativa e total do sistema inteiro.

Então, na prática:

Ele dá um mapa parcial forte.
Ele ajuda a entender arquitetura, churn, migração e pontos de integração.
Ele não substitui leitura do código-fonte real.
Ele não garante entendimento completo de fluxo em runtime, ordem de inicialização, estado Qt, sinais, side effects e diferenças entre código atual e legado.

Para este projeto, eu diria assim:
os JSONs me dão uma boa visão macro e de refatoração;
o entendimento completo só vem combinando JSON + leitura dos módulos reais + testes de execução.

lets interact in english .
to answer me questions as 1. which code is creating superior tab , or which module starts the app, show me which code is implementing topomap . What data should I collect from project and how to do it with a python script ?
Thought for 8s

Yes. For questions like:

which code creates the top tab
which module starts the app
which code implements the topomap

the most useful thing to collect is not just file names, but a searchable structural index of the project.

You should collect these 8 categories:

Entry points
Files that contain:
if __name__ == "__main__"
QApplication(...)
app.exec()
main launcher functions
window creation functions

Definitions
All classes, functions, methods, and their file paths and line numbers.

Imports
Who imports whom. This helps identify startup chains and cross-module dependencies.

Calls
Function and method calls inside each function.
This helps answer:
which code calls display_pyside6_eeg_visualizer
which code creates TopInTabBarInNotebook
which code calls topomap functions

Qt/UI construction
Widget creation, addWidget, addTab, setCentralWidget, signal connections, toolbar creation, tab creation.

Domain anchors
Keywords like:
topomap
amplitude_map
Timeline
EEGTab
MainWindow
Splash
Notebook
addTab
showMaximized
FigureCanvas
mne.viz.plot_topomap

String literals
Useful because many UI elements are only visible through labels like:
"EEG Traces"
"Spectrogram"
"Connectivity"
"Heat Map Test"

File-to-symbol index
A reverse index:
symbol -> file(s)
file -> symbols
keyword -> files

With that, I can answer questions much more reliably.

For your project, the best practical approach is:
build one JSON index from the whole repo using Python AST.

Use this script.

"""
Project structural indexer for Python repositories.

What it collects:
- Python files
- imports
- classes
- functions and methods
- calls inside functions
- string literals
- simple entry-point markers
- keyword hits for UI / EEG-related terms

Output:
- project_structure_index.json

Designed for Windows + standard CPython.
"""

from __future__ import annotations

import ast
import json
import os
from dataclasses import dataclass, asdict
from typing import Any


KEYWORDS = [
    "topomap",
    "amplitude_map",
    "timeline",
    "eeg traces",
    "spectrogram",
    "connectivity",
    "heat map",
    "notebook",
    "main window",
    "addtab",
    "setcentralwidget",
    "qapplication",
    "app.exec",
    "showmaximized",
    "figurecanvas",
    "plot_topomap",
    "mne.viz",
    "splash",
]


@dataclass
class ImportRecord:
    module: str
    name: str
    alias: str | None
    lineno: int


@dataclass
class CallRecord:
    call_name: str
    lineno: int


@dataclass
class FunctionRecord:
    name: str
    qualname: str
    lineno: int
    end_lineno: int | None
    calls: list[CallRecord]


@dataclass
class ClassRecord:
    name: str
    lineno: int
    end_lineno: int | None
    methods: list[FunctionRecord]


@dataclass
class FileRecord:
    path: str
    imports: list[ImportRecord]
    functions: list[FunctionRecord]
    classes: list[ClassRecord]
    strings: list[str]
    keyword_hits: list[str]
    entry_markers: list[str]


class FunctionVisitor(ast.NodeVisitor):
    def __init__(self, source_text: str) -> None:
        self.source_text = source_text
        self.imports: list[ImportRecord] = []
        self.functions: list[FunctionRecord] = []
        self.classes: list[ClassRecord] = []
        self.strings: list[str] = []
        self.entry_markers: list[str] = []

    def visit_Import(self, node: ast.Import) -> Any:
        for alias in node.names:
            self.imports.append(
                ImportRecord(
                    module=alias.name,
                    name="",
                    alias=alias.asname,
                    lineno=node.lineno,
                )
            )
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        module = node.module or ""
        for alias in node.names:
            self.imports.append(
                ImportRecord(
                    module=module,
                    name=alias.name,
                    alias=alias.asname,
                    lineno=node.lineno,
                )
            )
        self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant) -> Any:
        if isinstance(node.value, str):
            value = node.value.strip()
            if value:
                self.strings.append(value)
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> Any:
        try:
            text = ast.unparse(node.test)
        except Exception:
            text = ""
        if "__name__" in text and "__main__" in text:
            self.entry_markers.append("if __name__ == '__main__'")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> Any:
        name = get_call_name(node.func)
        if name in ("QApplication", "QApplication.instance", "app.exec", "exec", "sys.exit"):
            self.entry_markers.append(name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.functions.append(build_function_record(node, parent_name=None))
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> Any:
        self.functions.append(build_function_record(node, parent_name=None))
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        methods: list[FunctionRecord] = []
        for child in node.body:
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                methods.append(build_function_record(child, parent_name=node.name))
        self.classes.append(
            ClassRecord(
                name=node.name,
                lineno=node.lineno,
                end_lineno=getattr(node, "end_lineno", None),
                methods=methods,
            )
        )
        self.generic_visit(node)


def get_call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parts = []
        current = node
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            parts.append(current.id)
        parts.reverse()
        return ".".join(parts)
    return ""


def build_function_record(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    parent_name: str | None,
) -> FunctionRecord:
    calls: list[CallRecord] = []
    for subnode in ast.walk(node):
        if isinstance(subnode, ast.Call):
            call_name = get_call_name(subnode.func)
            if call_name:
                calls.append(CallRecord(call_name=call_name, lineno=subnode.lineno))

    qualname = node.name if parent_name is None else parent_name + "." + node.name

    return FunctionRecord(
        name=node.name,
        qualname=qualname,
        lineno=node.lineno,
        end_lineno=getattr(node, "end_lineno", None),
        calls=calls,
    )


def file_contains_keywords(strings: list[str], source_text: str) -> list[str]:
    found = set()
    source_lower = source_text.lower()
    for item in strings:
        item_lower = item.lower()
        for keyword in KEYWORDS:
            if keyword in item_lower:
                found.add(keyword)
    for keyword in KEYWORDS:
        if keyword in source_lower:
            found.add(keyword)
    return sorted(found)


def is_python_file(path: str) -> bool:
    return path.lower().endswith(".py")


def read_text_file(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return handle.read()


def build_index(project_root: str) -> dict[str, Any]:
    files: list[FileRecord] = []
    symbol_index: dict[str, list[str]] = {}
    keyword_index: dict[str, list[str]] = {}
    entry_files: list[str] = []

    for root, _dirs, filenames in os.walk(project_root):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            if not is_python_file(full_path):
                continue

            rel_path = os.path.relpath(full_path, project_root)

            try:
                source_text = read_text_file(full_path)
                tree = ast.parse(source_text, filename=rel_path)
            except Exception as exc:
                files.append(
                    FileRecord(
                        path=rel_path,
                        imports=[],
                        functions=[],
                        classes=[],
                        strings=[],
                        keyword_hits=["parse_error"],
                        entry_markers=[str(exc)],
                    )
                )
                continue

            visitor = FunctionVisitor(source_text)
            visitor.visit(tree)

            keyword_hits = file_contains_keywords(visitor.strings, source_text)

            file_record = FileRecord(
                path=rel_path,
                imports=visitor.imports,
                functions=visitor.functions,
                classes=visitor.classes,
                strings=sorted(set(visitor.strings))[:300],
                keyword_hits=keyword_hits,
                entry_markers=sorted(set(visitor.entry_markers)),
            )
            files.append(file_record)

            if file_record.entry_markers:
                entry_files.append(rel_path)

            for func in file_record.functions:
                symbol_index.setdefault(func.qualname, []).append(rel_path)

            for cls in file_record.classes:
                symbol_index.setdefault(cls.name, []).append(rel_path)
                for method in cls.methods:
                    symbol_index.setdefault(method.qualname, []).append(rel_path)

            for keyword in keyword_hits:
                keyword_index.setdefault(keyword, []).append(rel_path)

    output = {
        "project_root": os.path.abspath(project_root),
        "file_count": len(files),
        "entry_files": sorted(set(entry_files)),
        "files": [serialize_file_record(item) for item in sorted(files, key=lambda x: x.path)],
        "symbol_index": {k: sorted(set(v)) for k, v in sorted(symbol_index.items())},
        "keyword_index": {k: sorted(set(v)) for k, v in sorted(keyword_index.items())},
    }
    return output


def serialize_file_record(record: FileRecord) -> dict[str, Any]:
    return {
        "path": record.path,
        "imports": [asdict(item) for item in record.imports],
        "functions": [
            {
                "name": item.name,
                "qualname": item.qualname,
                "lineno": item.lineno,
                "end_lineno": item.end_lineno,
                "calls": [asdict(call) for call in item.calls],
            }
            for item in record.functions
        ],
        "classes": [
            {
                "name": item.name,
                "lineno": item.lineno,
                "end_lineno": item.end_lineno,
                "methods": [
                    {
                        "name": method.name,
                        "qualname": method.qualname,
                        "lineno": method.lineno,
                        "end_lineno": method.end_lineno,
                        "calls": [asdict(call) for call in method.calls],
                    }
                    for method in item.methods
                ],
            }
            for item in record.classes
        ],
        "strings": record.strings,
        "keyword_hits": record.keyword_hits,
        "entry_markers": record.entry_markers,
    }


def save_json(data: dict[str, Any], output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=True)


def main() -> None:
    project_root = r"E:\eeg_kernel_ai_neural_data_analysis"
    output_path = r"E:\eeg_kernel_ai_neural_data_analysis\project_structure_index.json"

    data = build_index(project_root)
    save_json(data, output_path)

    print("Index created successfully.")
    print("Project root:", data["project_root"])
    print("Python files indexed:", data["file_count"])
    print("Entry files found:", len(data["entry_files"]))
    print("Output:", output_path)


if __name__ == "__main__":
    main()

After you generate this JSON, I can answer questions like these much better:

Which module starts the app?
Look at entry_files, then inspect files containing QApplication, app.exec, create_main_window, display_pyside6_eeg_visualizer.

Which code creates the superior tab?
Search for:
TopInTabBarInNotebook
addTab
EEGTab
NotebookBuilder
TopInTabBar
and inspect constructor calls in the indexed calls.

Which code implements topomap?
Search for:
topomap
amplitude_map
plot_topomap
mne.viz
and inspect matching files in keyword_index.

What else would improve understanding even more:
a second JSON for runtime state flow
a third JSON for Qt signal connections
a fourth JSON for widget tree construction

If you want, next I can give you a second script specifically for:
startup chain + Qt tabs + topomap tracing.

improve this code to an app pyside6 gui  that:
1. ask for name of file 
2. ask to place to insert file 
3. select folder to inspect python files recursivelly  as deepest as necessary 
4. create json using  name in 1 and localized in 2

also get all semantic information about the project 
Thought for 8s

Below is a single-file PySide6 app that does what you asked.

It lets the user:

enter the JSON file name

choose where to save it

choose the project folder to inspect recursively

generate the JSON using the chosen name and location

It also collects much richer semantic information than the earlier script:
project metadata
entry points
imports
classes
inheritance
functions and methods
calls
docstrings
string literals
comments
keyword hits
Qt/UI hints
EEG/domain hints
symbol index
import graph
simple call edges
file summaries

Code:

"""
PySide6 GUI app to recursively inspect a Python project and export a rich JSON
structure/semantic index.

Features
--------
1. User enters output JSON file name.
2. User chooses output folder.
3. User chooses a project folder to inspect recursively.
4. App generates JSON at the selected location.
5. Collects structural and semantic project information:
   - imports
   - classes
   - inheritance
   - functions and methods
   - call sites
   - docstrings
   - comments
   - string literals
   - keyword hits
   - simple entry points
   - UI hints
   - EEG/domain hints
   - symbol index
   - import graph
   - simple call edges
"""

from __future__ import annotations

import ast
import io
import json
import keyword
import os
import re
import sys
import tokenize
from dataclasses import dataclass, asdict
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QProgressBar,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


ENTRY_MARKERS = [
    "QApplication",
    "app.exec",
    "sys.exit",
    "display_pyside6_eeg_visualizer",
    "create_main_window",
    "if __name__ == '__main__'",
]

UI_KEYWORDS = [
    "QApplication",
    "QMainWindow",
    "QWidget",
    "QDialog",
    "QTabWidget",
    "QToolBar",
    "QVBoxLayout",
    "QHBoxLayout",
    "QGridLayout",
    "QSplitter",
    "QStackedWidget",
    "addWidget",
    "addTab",
    "setCentralWidget",
    "show",
    "showMaximized",
    "connect",
    "Signal",
    "Slot",
]

EEG_KEYWORDS = [
    "eeg",
    "topomap",
    "amplitude_map",
    "timeline",
    "spectrogram",
    "connectivity",
    "heat map",
    "mne",
    "plot_topomap",
    "raw",
    "epoch",
    "montage",
    "notch",
    "high-pass",
    "low-pass",
    "brain",
    "neuro",
]

SEMANTIC_HINT_KEYWORDS = [
    "load",
    "save",
    "render",
    "plot",
    "update",
    "reset",
    "build",
    "create",
    "attach",
    "connect",
    "signal",
    "timeline",
    "topomap",
    "amplitude",
    "filter",
    "toolbar",
    "tab",
    "window",
    "splash",
    "diagnostic",
    "snapshot",
    "memory",
]


@dataclass
class ImportRecord:
    module: str
    name: str
    alias: str | None
    lineno: int


@dataclass
class CallRecord:
    call_name: str
    lineno: int


@dataclass
class FunctionRecord:
    name: str
    qualname: str
    lineno: int
    end_lineno: int | None
    docstring: str
    decorators: list[str]
    calls: list[CallRecord]
    parameters: list[str]
    returns_annotation: str


@dataclass
class ClassRecord:
    name: str
    lineno: int
    end_lineno: int | None
    docstring: str
    bases: list[str]
    methods: list[FunctionRecord]


@dataclass
class FileRecord:
    path: str
    module_name: str
    imports: list[ImportRecord]
    functions: list[FunctionRecord]
    classes: list[ClassRecord]
    strings: list[str]
    comments: list[str]
    docstring: str
    entry_markers: list[str]
    ui_keyword_hits: list[str]
    eeg_keyword_hits: list[str]
    semantic_hints: list[str]
    parse_error: str


def safe_read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return handle.read()


def is_python_file(path: str) -> bool:
    return path.lower().endswith(".py")


def normalize_module_name(rel_path: str) -> str:
    module_name = rel_path.replace("\\", ".").replace("/", ".")
    if module_name.lower().endswith(".py"):
        module_name = module_name[:-3]
    if module_name.endswith(".__init__"):
        module_name = module_name[:-9]
    return module_name.strip(".")


def get_call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        parts: list[str] = []
        current: ast.AST = node
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            parts.append(current.id)
        parts.reverse()
        return ".".join(parts)

    if isinstance(node, ast.Call):
        return get_call_name(node.func)

    return ""


def get_annotation_text(node: ast.AST | None) -> str:
    if node is None:
        return ""
    try:
        return ast.unparse(node)
    except Exception:
        return ""


def get_decorators(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    decorators: list[str] = []
    for item in node.decorator_list:
        try:
            decorators.append(ast.unparse(item))
        except Exception:
            decorators.append("")
    return [x for x in decorators if x]


def get_parameters(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    params: list[str] = []

    args = node.args

    for arg in args.posonlyargs:
        params.append(arg.arg)
    for arg in args.args:
        params.append(arg.arg)
    if args.vararg:
        params.append("*" + args.vararg.arg)
    for arg in args.kwonlyargs:
        params.append(arg.arg)
    if args.kwarg:
        params.append("**" + args.kwarg.arg)

    return params


def get_comments_from_source(source_text: str) -> list[str]:
    comments: list[str] = []

    try:
        tokens = tokenize.generate_tokens(io.StringIO(source_text).readline)
        for token_info in tokens:
            if token_info.type == tokenize.COMMENT:
                text = token_info.string.strip()
                if text:
                    comments.append(text)
    except Exception:
        pass

    return sorted(set(comments))[:500]


def unique_trimmed_strings(values: list[str], max_items: int = 300) -> list[str]:
    seen = set()
    result: list[str] = []

    for value in values:
        cleaned = value.strip()
        if not cleaned:
            continue
        if cleaned in seen:
            continue
        seen.add(cleaned)
        result.append(cleaned)
        if len(result) >= max_items:
            break

    return result


def detect_keyword_hits(source_text: str, keywords: list[str]) -> list[str]:
    source_lower = source_text.lower()
    found = []
    for item in keywords:
        if item.lower() in source_lower:
            found.append(item)
    return sorted(set(found))


def detect_entry_markers(source_text: str) -> list[str]:
    markers: list[str] = []
    lowered = source_text.lower()

    if "__name__" in source_text and "__main__" in source_text:
        markers.append("if __name__ == '__main__'")

    if "QApplication" in source_text:
        markers.append("QApplication")

    if "app.exec(" in source_text or "app.exec()" in source_text:
        markers.append("app.exec")

    if "sys.exit(" in source_text:
        markers.append("sys.exit")

    if "create_main_window" in source_text:
        markers.append("create_main_window")

    if "display_pyside6_eeg_visualizer" in source_text:
        markers.append("display_pyside6_eeg_visualizer")

    if "main(" in lowered:
        markers.append("main")

    return sorted(set(markers))


class ProjectAstVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.imports: list[ImportRecord] = []
        self.functions: list[FunctionRecord] = []
        self.classes: list[ClassRecord] = []
        self.strings: list[str] = []

    def visit_Import(self, node: ast.Import) -> Any:
        for alias in node.names:
            self.imports.append(
                ImportRecord(
                    module=alias.name,
                    name="",
                    alias=alias.asname,
                    lineno=node.lineno,
                )
            )
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        module = node.module or ""
        for alias in node.names:
            self.imports.append(
                ImportRecord(
                    module=module,
                    name=alias.name,
                    alias=alias.asname,
                    lineno=node.lineno,
                )
            )
        self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant) -> Any:
        if isinstance(node.value, str):
            self.strings.append(node.value)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.functions.append(build_function_record(node, None))
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> Any:
        self.functions.append(build_function_record(node, None))
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        methods: list[FunctionRecord] = []
        for child in node.body:
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                methods.append(build_function_record(child, node.name))

        bases: list[str] = []
        for base in node.bases:
            try:
                bases.append(ast.unparse(base))
            except Exception:
                bases.append("")

        self.classes.append(
            ClassRecord(
                name=node.name,
                lineno=node.lineno,
                end_lineno=getattr(node, "end_lineno", None),
                docstring=ast.get_docstring(node) or "",
                bases=[x for x in bases if x],
                methods=methods,
            )
        )

        self.generic_visit(node)


def build_function_record(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    parent_name: str | None,
) -> FunctionRecord:
    qualname = node.name if parent_name is None else parent_name + "." + node.name

    calls: list[CallRecord] = []
    for subnode in ast.walk(node):
        if isinstance(subnode, ast.Call):
            call_name = get_call_name(subnode.func)
            if call_name:
                calls.append(CallRecord(call_name=call_name, lineno=subnode.lineno))

    return FunctionRecord(
        name=node.name,
        qualname=qualname,
        lineno=node.lineno,
        end_lineno=getattr(node, "end_lineno", None),
        docstring=ast.get_docstring(node) or "",
        decorators=get_decorators(node),
        calls=calls,
        parameters=get_parameters(node),
        returns_annotation=get_annotation_text(node.returns),
    )


def summarize_file_semantics(record: FileRecord) -> dict[str, Any]:
    roles: list[str] = []

    full_text_parts = []
    full_text_parts.extend(record.ui_keyword_hits)
    full_text_parts.extend(record.eeg_keyword_hits)
    full_text_parts.extend(record.semantic_hints)
    full_text_parts.extend([f.name for f in record.functions])
    full_text_parts.extend([c.name for c in record.classes])

    lowered = " ".join(full_text_parts).lower()

    if "qapplication" in lowered or "app.exec" in lowered:
        roles.append("startup")
    if "mainwindow" in lowered or "setcentralwidget" in lowered or "window" in lowered:
        roles.append("main_window")
    if "addtab" in lowered or "tab" in lowered or "notebook" in lowered:
        roles.append("tabs")
    if "toolbar" in lowered:
        roles.append("toolbar")
    if "timeline" in lowered:
        roles.append("timeline")
    if "topomap" in lowered or "amplitude_map" in lowered or "plot_topomap" in lowered:
        roles.append("topomap")
    if "spectrogram" in lowered:
        roles.append("spectrogram")
    if "connectivity" in lowered:
        roles.append("connectivity")
    if "splash" in lowered:
        roles.append("splash")
    if "filter" in lowered:
        roles.append("filters")
    if "snapshot" in lowered or "reset" in lowered:
        roles.append("state_reset")
    if "memory" in lowered:
        roles.append("memory_monitoring")
    if "diagnostic" in lowered:
        roles.append("diagnostics")

    return {
        "roles": sorted(set(roles)),
        "has_ui": bool(record.ui_keyword_hits),
        "has_eeg_domain": bool(record.eeg_keyword_hits),
        "entry_like": bool(record.entry_markers),
    }


def analyze_python_file(project_root: str, full_path: str) -> FileRecord:
    rel_path = os.path.relpath(full_path, project_root)
    module_name = normalize_module_name(rel_path)

    try:
        source_text = safe_read_text(full_path)
    except Exception as exc:
        return FileRecord(
            path=rel_path,
            module_name=module_name,
            imports=[],
            functions=[],
            classes=[],
            strings=[],
            comments=[],
            docstring="",
            entry_markers=[],
            ui_keyword_hits=[],
            eeg_keyword_hits=[],
            semantic_hints=[],
            parse_error=str(exc),
        )

    try:
        tree = ast.parse(source_text, filename=rel_path)
        visitor = ProjectAstVisitor()
        visitor.visit(tree)
        file_docstring = ast.get_docstring(tree) or ""
        parse_error = ""
    except Exception as exc:
        visitor = ProjectAstVisitor()
        file_docstring = ""
        parse_error = str(exc)

    comments = get_comments_from_source(source_text)
    entry_markers = detect_entry_markers(source_text)
    ui_hits = detect_keyword_hits(source_text, UI_KEYWORDS)
    eeg_hits = detect_keyword_hits(source_text, EEG_KEYWORDS)
    semantic_hits = detect_keyword_hits(source_text, SEMANTIC_HINT_KEYWORDS)

    return FileRecord(
        path=rel_path,
        module_name=module_name,
        imports=visitor.imports,
        functions=visitor.functions,
        classes=visitor.classes,
        strings=unique_trimmed_strings(visitor.strings, 300),
        comments=comments,
        docstring=file_docstring,
        entry_markers=entry_markers,
        ui_keyword_hits=ui_hits,
        eeg_keyword_hits=eeg_hits,
        semantic_hints=semantic_hits,
        parse_error=parse_error,
    )


def build_project_index(project_root: str, log_callback=None) -> dict[str, Any]:
    file_records: list[FileRecord] = []
    python_files: list[str] = []

    for root, _dirs, filenames in os.walk(project_root):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            if is_python_file(full_path):
                python_files.append(full_path)

    python_files.sort()

    symbol_index: dict[str, list[str]] = {}
    import_graph: dict[str, list[str]] = {}
    call_edges: list[dict[str, str]] = []
    entry_files: list[str] = []
    semantic_roles: dict[str, dict[str, Any]] = {}

    total = len(python_files)

    for index, full_path in enumerate(python_files, start=1):
        if log_callback is not None:
            log_callback("Analyzing: " + full_path, index, total)

        record = analyze_python_file(project_root, full_path)
        file_records.append(record)

        if record.entry_markers:
            entry_files.append(record.path)

        semantic_roles[record.path] = summarize_file_semantics(record)

        import_graph.setdefault(record.module_name, [])

        for imp in record.imports:
            target = imp.module
            if imp.name and imp.module:
                target = imp.module + "." + imp.name
            elif imp.name and not imp.module:
                target = imp.name
            if target:
                import_graph[record.module_name].append(target)

        for function_record in record.functions:
            symbol_index.setdefault(function_record.qualname, []).append(record.path)
            for call in function_record.calls:
                call_edges.append(
                    {
                        "from_file": record.path,
                        "from_symbol": function_record.qualname,
                        "to_call": call.call_name,
                    }
                )

        for class_record in record.classes:
            symbol_index.setdefault(class_record.name, []).append(record.path)
            for method_record in class_record.methods:
                symbol_index.setdefault(method_record.qualname, []).append(record.path)
                for call in method_record.calls:
                    call_edges.append(
                        {
                            "from_file": record.path,
                            "from_symbol": method_record.qualname,
                            "to_call": call.call_name,
                        }
                    )

    keyword_index = {
        "ui": sorted(
            [r.path for r in file_records if r.ui_keyword_hits]
        ),
        "eeg": sorted(
            [r.path for r in file_records if r.eeg_keyword_hits]
        ),
        "semantic": sorted(
            [r.path for r in file_records if r.semantic_hints]
        ),
    }

    project_summary = {
        "project_root": os.path.abspath(project_root),
        "python_file_count": len(file_records),
        "entry_file_count": len(set(entry_files)),
        "class_count": sum(len(r.classes) for r in file_records),
        "top_level_function_count": sum(len(r.functions) for r in file_records),
        "method_count": sum(len(c.methods) for r in file_records for c in r.classes),
        "files_with_parse_errors": sorted([r.path for r in file_records if r.parse_error]),
        "files_with_ui": keyword_index["ui"],
        "files_with_eeg": keyword_index["eeg"],
        "files_with_semantic_hints": keyword_index["semantic"],
    }

    return {
        "project_summary": project_summary,
        "entry_files": sorted(set(entry_files)),
        "files": [serialize_file_record(record) for record in file_records],
        "symbol_index": {k: sorted(set(v)) for k, v in sorted(symbol_index.items())},
        "import_graph": {k: sorted(set(v)) for k, v in sorted(import_graph.items())},
        "call_edges": call_edges,
        "semantic_roles": semantic_roles,
        "keyword_index": keyword_index,
    }


def serialize_file_record(record: FileRecord) -> dict[str, Any]:
    return {
        "path": record.path,
        "module_name": record.module_name,
        "docstring": record.docstring,
        "imports": [asdict(item) for item in record.imports],
        "functions": [
            {
                "name": item.name,
                "qualname": item.qualname,
                "lineno": item.lineno,
                "end_lineno": item.end_lineno,
                "docstring": item.docstring,
                "decorators": item.decorators,
                "parameters": item.parameters,
                "returns_annotation": item.returns_annotation,
                "calls": [asdict(call) for call in item.calls],
            }
            for item in record.functions
        ],
        "classes": [
            {
                "name": item.name,
                "lineno": item.lineno,
                "end_lineno": item.end_lineno,
                "docstring": item.docstring,
                "bases": item.bases,
                "methods": [
                    {
                        "name": method.name,
                        "qualname": method.qualname,
                        "lineno": method.lineno,
                        "end_lineno": method.end_lineno,
                        "docstring": method.docstring,
                        "decorators": method.decorators,
                        "parameters": method.parameters,
                        "returns_annotation": method.returns_annotation,
                        "calls": [asdict(call) for call in method.calls],
                    }
                    for method in item.methods
                ],
            }
            for item in record.classes
        ],
        "strings": record.strings,
        "comments": record.comments,
        "entry_markers": record.entry_markers,
        "ui_keyword_hits": record.ui_keyword_hits,
        "eeg_keyword_hits": record.eeg_keyword_hits,
        "semantic_hints": record.semantic_hints,
        "parse_error": record.parse_error,
    }


def save_json_file(data: dict[str, Any], output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=True)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Python Project Semantic JSON Indexer")
        self.resize(980, 700)

        self.project_folder_edit = QLineEdit()
        self.output_folder_edit = QLineEdit()
        self.output_file_name_edit = QLineEdit("project_structure_index.json")

        self.log_box = QPlainTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setLineWrapMode(QPlainTextEdit.NoWrap)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

        self.inspect_button = QPushButton("Generate JSON")
        self.browse_project_button = QPushButton("Browse Project Folder")
        self.browse_output_button = QPushButton("Browse Output Folder")

        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

        input_group = QGroupBox("Project Inspection Settings")
        input_layout = QGridLayout(input_group)

        input_layout.addWidget(QLabel("Project folder to inspect recursively:"), 0, 0)
        input_layout.addWidget(self.project_folder_edit, 0, 1)
        input_layout.addWidget(self.browse_project_button, 0, 2)

        input_layout.addWidget(QLabel("Output folder:"), 1, 0)
        input_layout.addWidget(self.output_folder_edit, 1, 1)
        input_layout.addWidget(self.browse_output_button, 1, 2)

        input_layout.addWidget(QLabel("Output JSON file name:"), 2, 0)
        input_layout.addWidget(self.output_file_name_edit, 2, 1, 1, 2)

        action_layout = QHBoxLayout()
        action_layout.addWidget(self.inspect_button)
        action_layout.addStretch()

        log_group = QGroupBox("Execution Log")
        log_layout = QVBoxLayout(log_group)
        log_layout.addWidget(self.log_box)

        main_layout.addWidget(input_group)
        main_layout.addLayout(action_layout)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(log_group)

    def _connect_signals(self) -> None:
        self.browse_project_button.clicked.connect(self.select_project_folder)
        self.browse_output_button.clicked.connect(self.select_output_folder)
        self.inspect_button.clicked.connect(self.generate_json)

    def append_log(self, text: str) -> None:
        self.log_box.appendPlainText(text)
        self.log_box.verticalScrollBar().setValue(
            self.log_box.verticalScrollBar().maximum()
        )
        QApplication.processEvents()

    def update_progress(self, current: int, total: int) -> None:
        if total <= 0:
            self.progress_bar.setValue(0)
            return
        percent = int((current / total) * 100)
        self.progress_bar.setValue(percent)
        QApplication.processEvents()

    def select_project_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Project Folder",
            self.project_folder_edit.text().strip() or os.getcwd(),
        )
        if folder:
            self.project_folder_edit.setText(folder)

    def select_output_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Output Folder",
            self.output_folder_edit.text().strip() or os.getcwd(),
        )
        if folder:
            self.output_folder_edit.setText(folder)

    def validate_inputs(self) -> tuple[bool, str]:
        project_folder = self.project_folder_edit.text().strip()
        output_folder = self.output_folder_edit.text().strip()
        output_file_name = self.output_file_name_edit.text().strip()

        if not project_folder:
            return False, "Please choose a project folder."
        if not os.path.isdir(project_folder):
            return False, "The selected project folder does not exist."
        if not output_folder:
            return False, "Please choose an output folder."
        if not os.path.isdir(output_folder):
            return False, "The selected output folder does not exist."
        if not output_file_name:
            return False, "Please provide a JSON file name."

        if not output_file_name.lower().endswith(".json"):
            return False, "The output file name must end with .json"

        bad_chars = set('<>:"/\\|?*')
        if any(ch in bad_chars for ch in output_file_name):
            return False, "The output file name contains invalid Windows filename characters."

        return True, ""

    def generate_json(self) -> None:
        is_valid, message = self.validate_inputs()
        if not is_valid:
            QMessageBox.warning(self, "Invalid Input", message)
            return

        project_folder = self.project_folder_edit.text().strip()
        output_folder = self.output_folder_edit.text().strip()
        output_file_name = self.output_file_name_edit.text().strip()
        output_path = os.path.join(output_folder, output_file_name)

        self.log_box.clear()
        self.progress_bar.setValue(0)
        self.inspect_button.setEnabled(False)

        try:
            self.append_log("Project folder: " + project_folder)
            self.append_log("Output path: " + output_path)
            self.append_log("Starting recursive analysis...")

            def progress_logger(text: str, current: int, total: int) -> None:
                self.append_log(text)
                self.update_progress(current, total)

            data = build_project_index(project_folder, progress_logger)
            save_json_file(data, output_path)

            self.progress_bar.setValue(100)
            self.append_log("JSON created successfully.")
            self.append_log("Indexed files: " + str(data["project_summary"]["python_file_count"]))
            self.append_log("Entry files found: " + str(data["project_summary"]["entry_file_count"]))
            self.append_log("Output saved to: " + output_path)

            QMessageBox.information(
                self,
                "Success",
                "JSON created successfully:\n" + output_path,
            )

        except Exception as exc:
            self.append_log("ERROR: " + str(exc))
            QMessageBox.critical(
                self,
                "Error",
                "Failed to create JSON:\n" + str(exc),
            )
        finally:
            self.inspect_button.setEnabled(True)


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

What this app gives you semantically:
It does not truly "understand" the project like a human architect, but it extracts the best static semantic metadata you can reliably get from source code without running the whole app:
module roles
entry points
UI-related files
EEG-related files
docstrings
comments
imports
symbols
calls
inheritance
string-based semantic hints

That is usually enough to answer questions like:
which module starts the app
which code creates the top tab
which file implements topomap
where timeline is wired
which file owns splash creation
which code performs reset/snapshot logic

If you want, the next step is a second companion app that loads the generated JSON and lets you ask interactive questions like:
"show startup chain"
"find topomap implementation"
"find tab creation code"
"show all callers of display_pyside6_eeg_visualizer"

do it
Thought for 6s

Below is a companion PySide6 app that loads the generated JSON and lets you ask practical architecture questions.

It supports:
loading the JSON index
asking natural project questions
showing matching files, symbols, calls, entry files, and semantic roles
quick buttons for common queries:
startup chain
top tab creation
topomap implementation
timeline wiring
splash creation
reset and snapshot flow

It is heuristic, but very useful in practice.

"""
PySide6 companion app for exploring a project_structure_index.json file.

What it does
------------
1. Loads the JSON generated by the project semantic indexer.
2. Lets the user ask practical architecture questions.
3. Searches entry files, symbols, imports, call edges, semantic roles, and
   file content summaries already stored in the JSON.
4. Displays ranked results in a readable way.

Examples of supported questions
-------------------------------
- which module starts the app
- which code creates superior tab
- show me which code is implementing topomap
- where is timeline wired
- where is splash created
- where is reset to initial eeg state implemented
"""

from __future__ import annotations

import json
import os
import re
import sys
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QSizePolicy,
    QSplitter,
    QVBoxLayout,
    QWidget,
)


def safe_lower(value: Any) -> str:
    return str(value).lower() if value is not None else ""


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def tokenize_query(text: str) -> list[str]:
    tokens = re.findall(r"[a-zA-Z0-9_\.]+", text.lower())
    stop_words = {
        "the",
        "is",
        "are",
        "a",
        "an",
        "of",
        "to",
        "me",
        "show",
        "which",
        "what",
        "where",
        "who",
        "does",
        "do",
        "in",
        "on",
        "for",
        "and",
        "or",
        "with",
        "code",
        "module",
        "file",
        "implementing",
        "implements",
        "created",
        "creates",
        "create",
    }
    return [token for token in tokens if token not in stop_words]


def get_nested(data: dict[str, Any], key: str, default: Any) -> Any:
    return data[key] if key in data else default


class JsonProjectExplorer(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Project JSON Explorer")
        self.resize(1300, 800)

        self.index_data: dict[str, Any] | None = None

        self.json_path_edit = QLineEdit()
        self.question_edit = QLineEdit()

        self.load_button = QPushButton("Load JSON")
        self.ask_button = QPushButton("Ask")
        self.clear_button = QPushButton("Clear")
        self.quick_startup_button = QPushButton("Startup Chain")
        self.quick_tabs_button = QPushButton("Top Tab Creation")
        self.quick_topomap_button = QPushButton("Topomap")
        self.quick_timeline_button = QPushButton("Timeline")
        self.quick_splash_button = QPushButton("Splash")
        self.quick_reset_button = QPushButton("Reset / Snapshot")

        self.result_list = QListWidget()
        self.result_details = QPlainTextEdit()
        self.result_details.setReadOnly(True)
        self.log_box = QPlainTextEdit()
        self.log_box.setReadOnly(True)

        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

        load_group = QGroupBox("Load Semantic JSON Index")
        load_layout = QGridLayout(load_group)
        load_layout.addWidget(QLabel("JSON file:"), 0, 0)
        load_layout.addWidget(self.json_path_edit, 0, 1)
        load_layout.addWidget(self.load_button, 0, 2)

        ask_group = QGroupBox("Ask a Project Question")
        ask_layout = QGridLayout(ask_group)
        ask_layout.addWidget(QLabel("Question:"), 0, 0)
        ask_layout.addWidget(self.question_edit, 0, 1)
        ask_layout.addWidget(self.ask_button, 0, 2)
        ask_layout.addWidget(self.clear_button, 0, 3)

        quick_layout = QHBoxLayout()
        quick_layout.addWidget(self.quick_startup_button)
        quick_layout.addWidget(self.quick_tabs_button)
        quick_layout.addWidget(self.quick_topomap_button)
        quick_layout.addWidget(self.quick_timeline_button)
        quick_layout.addWidget(self.quick_splash_button)
        quick_layout.addWidget(self.quick_reset_button)
        quick_layout.addStretch()

        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout(results_group)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.result_list)
        splitter.addWidget(self.result_details)
        splitter.setSizes([450, 800])

        results_layout.addWidget(splitter)

        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout(log_group)
        log_layout.addWidget(self.log_box)

        main_layout.addWidget(load_group)
        main_layout.addWidget(ask_group)
        main_layout.addLayout(quick_layout)
        main_layout.addWidget(results_group, stretch=1)
        main_layout.addWidget(log_group, stretch=0)

    def _connect_signals(self) -> None:
        self.load_button.clicked.connect(self.load_json)
        self.ask_button.clicked.connect(self.ask_question)
        self.clear_button.clicked.connect(self.clear_results)
        self.question_edit.returnPressed.connect(self.ask_question)

        self.quick_startup_button.clicked.connect(
            lambda: self.run_quick_query("which module starts the app")
        )
        self.quick_tabs_button.clicked.connect(
            lambda: self.run_quick_query("which code creates superior tab")
        )
        self.quick_topomap_button.clicked.connect(
            lambda: self.run_quick_query("show me which code is implementing topomap")
        )
        self.quick_timeline_button.clicked.connect(
            lambda: self.run_quick_query("where is timeline wired")
        )
        self.quick_splash_button.clicked.connect(
            lambda: self.run_quick_query("where is splash created")
        )
        self.quick_reset_button.clicked.connect(
            lambda: self.run_quick_query("where is reset and snapshot flow")
        )

        self.result_list.currentItemChanged.connect(self.display_result_details)

    def append_log(self, text: str) -> None:
        self.log_box.appendPlainText(text)

    def load_json(self) -> None:
        current_path = self.json_path_edit.text().strip()
        start_dir = os.path.dirname(current_path) if current_path else os.getcwd()

        file_path, _filter = QFileDialog.getOpenFileName(
            self,
            "Select project_structure_index.json",
            start_dir,
            "JSON Files (*.json)",
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as handle:
                self.index_data = json.load(handle)

            self.json_path_edit.setText(file_path)
            self.append_log("Loaded JSON: " + file_path)

            summary = get_nested(self.index_data, "project_summary", {})
            self.append_log(
                "Python files indexed: "
                + str(summary.get("python_file_count", "unknown"))
            )
            self.append_log(
                "Entry files found: "
                + str(summary.get("entry_file_count", "unknown"))
            )

            QMessageBox.information(self, "Loaded", "JSON loaded successfully.")
        except Exception as exc:
            QMessageBox.critical(self, "Error", "Failed to load JSON:\n" + str(exc))
            self.append_log("ERROR loading JSON: " + str(exc))

    def clear_results(self) -> None:
        self.result_list.clear()
        self.result_details.clear()

    def run_quick_query(self, question: str) -> None:
        self.question_edit.setText(question)
        self.ask_question()

    def ask_question(self) -> None:
        if not self.index_data:
            QMessageBox.warning(self, "No JSON Loaded", "Please load a JSON index first.")
            return

        question = self.question_edit.text().strip()
        if not question:
            QMessageBox.warning(self, "No Question", "Please type a question.")
            return

        self.clear_results()
        self.append_log("Question: " + question)

        results = self.search_question(question)

        if not results:
            self.append_log("No matches found.")
            self.result_details.setPlainText("No matches found.")
            return

        for result in results:
            item = QListWidgetItem(result["title"])
            item.setData(Qt.UserRole, result)
            self.result_list.addItem(item)

        self.result_list.setCurrentRow(0)
        self.append_log("Matches found: " + str(len(results)))

    def search_question(self, question: str) -> list[dict[str, Any]]:
        q = normalize_text(question)
        tokens = tokenize_query(q)

        files = get_nested(self.index_data, "files", [])
        entry_files = set(get_nested(self.index_data, "entry_files", []))
        symbol_index = get_nested(self.index_data, "symbol_index", {})
        import_graph = get_nested(self.index_data, "import_graph", {})
        call_edges = get_nested(self.index_data, "call_edges", [])
        semantic_roles = get_nested(self.index_data, "semantic_roles", {})

        scored_results: list[dict[str, Any]] = []

        for file_record in files:
            path = file_record.get("path", "")
            module_name = file_record.get("module_name", "")
            docstring = file_record.get("docstring", "")
            strings = file_record.get("strings", [])
            comments = file_record.get("comments", [])
            entry_markers = file_record.get("entry_markers", [])
            ui_hits = file_record.get("ui_keyword_hits", [])
            eeg_hits = file_record.get("eeg_keyword_hits", [])
            semantic_hints = file_record.get("semantic_hints", [])
            functions = file_record.get("functions", [])
            classes = file_record.get("classes", [])

            haystack_parts = [
                path,
                module_name,
                docstring,
                " ".join(strings),
                " ".join(comments),
                " ".join(entry_markers),
                " ".join(ui_hits),
                " ".join(eeg_hits),
                " ".join(semantic_hints),
            ]

            function_names = []
            method_names = []
            call_names = []

            for fn in functions:
                function_names.append(fn.get("name", ""))
                function_names.append(fn.get("qualname", ""))
                for call in fn.get("calls", []):
                    call_names.append(call.get("call_name", ""))

            for cls in classes:
                function_names.append(cls.get("name", ""))
                for method in cls.get("methods", []):
                    method_names.append(method.get("name", ""))
                    method_names.append(method.get("qualname", ""))
                    for call in method.get("calls", []):
                        call_names.append(call.get("call_name", ""))

            haystack_parts.extend(function_names)
            haystack_parts.extend(method_names)
            haystack_parts.extend(call_names)

            haystack = " ".join([safe_lower(x) for x in haystack_parts])

            score = 0
            reasons: list[str] = []

            for token in tokens:
                if token in haystack:
                    score += 3
                    reasons.append("token match: " + token)

            if path in entry_files:
                if "start" in q or "entry" in q or "app" in q or "main" in q:
                    score += 12
                    reasons.append("entry file")

            roles = get_nested(semantic_roles, path, {}).get("roles", [])

            if "topomap" in q:
                if "topomap" in haystack or "amplitude_map" in haystack:
                    score += 15
                    reasons.append("topomap role/keyword")
                if "topomap" in roles:
                    score += 10
                    reasons.append("semantic role topomap")

            if "timeline" in q:
                if "timeline" in haystack:
                    score += 15
                    reasons.append("timeline keyword")
                if "timeline" in roles:
                    score += 10
                    reasons.append("semantic role timeline")

            if "splash" in q:
                if "splash" in haystack:
                    score += 15
                    reasons.append("splash keyword")
                if "splash" in roles:
                    score += 10
                    reasons.append("semantic role splash")

            if "tab" in q:
                if "addtab" in haystack or "tab" in haystack or "notebook" in haystack:
                    score += 12
                    reasons.append("tab creation keyword")
                if "tabs" in roles:
                    score += 10
                    reasons.append("semantic role tabs")

            if "reset" in q or "snapshot" in q:
                if "reset" in haystack or "snapshot" in haystack:
                    score += 14
                    reasons.append("reset/snapshot keyword")
                if "state_reset" in roles:
                    score += 10
                    reasons.append("semantic role state_reset")

            if "superior tab" in q or "top tab" in q:
                if "topintabbar" in haystack or "top bar" in haystack or "notebook" in haystack:
                    score += 16
                    reasons.append("top tab match")

            if "starts the app" in q or "start app" in q or "module starts the app" in q:
                if path in entry_files:
                    score += 20
                    reasons.append("startup entry match")
                if "startup" in roles:
                    score += 10
                    reasons.append("semantic role startup")

            if score > 0:
                detail = self.build_result_detail(
                    file_record=file_record,
                    reasons=reasons,
                    roles=roles,
                    entry_files=entry_files,
                    import_graph=import_graph,
                    call_edges=call_edges,
                    symbol_index=symbol_index,
                )
                scored_results.append(
                    {
                        "score": score,
                        "title": self.build_result_title(path, module_name, score),
                        "detail": detail,
                        "path": path,
                    }
                )

        scored_results.sort(key=lambda item: (-item["score"], item["path"]))
        return scored_results[:40]

    def build_result_title(self, path: str, module_name: str, score: int) -> str:
        return "[" + str(score) + "] " + path + "  |  " + module_name

    def build_result_detail(
        self,
        file_record: dict[str, Any],
        reasons: list[str],
        roles: list[str],
        entry_files: set[str],
        import_graph: dict[str, list[str]],
        call_edges: list[dict[str, str]],
        symbol_index: dict[str, list[str]],
    ) -> str:
        path = file_record.get("path", "")
        module_name = file_record.get("module_name", "")
        docstring = file_record.get("docstring", "")
        entry_markers = file_record.get("entry_markers", [])
        ui_hits = file_record.get("ui_keyword_hits", [])
        eeg_hits = file_record.get("eeg_keyword_hits", [])
        semantic_hints = file_record.get("semantic_hints", [])
        functions = file_record.get("functions", [])
        classes = file_record.get("classes", [])

        lines: list[str] = []

        lines.append("FILE")
        lines.append(path)
        lines.append("")
        lines.append("MODULE")
        lines.append(module_name)
        lines.append("")
        lines.append("WHY THIS MATCHED")
        for reason in sorted(set(reasons)):
            lines.append("- " + reason)

        lines.append("")
        lines.append("SEMANTIC ROLES")
        if roles:
            for role in roles:
                lines.append("- " + role)
        else:
            lines.append("- none")

        lines.append("")
        lines.append("ENTRY FILE")
        lines.append("yes" if path in entry_files else "no")

        if entry_markers:
            lines.append("")
            lines.append("ENTRY MARKERS")
            for marker in entry_markers:
                lines.append("- " + marker)

        if docstring:
            lines.append("")
            lines.append("FILE DOCSTRING")
            lines.append(docstring)

        if ui_hits:
            lines.append("")
            lines.append("UI KEYWORD HITS")
            for item in ui_hits:
                lines.append("- " + item)

        if eeg_hits:
            lines.append("")
            lines.append("EEG KEYWORD HITS")
            for item in eeg_hits:
                lines.append("- " + item)

        if semantic_hints:
            lines.append("")
            lines.append("SEMANTIC HINTS")
            for item in semantic_hints:
                lines.append("- " + item)

        if import_graph.get(module_name):
            lines.append("")
            lines.append("IMPORTS OUT")
            for item in import_graph[module_name][:50]:
                lines.append("- " + item)

        file_call_edges = [edge for edge in call_edges if edge.get("from_file") == path]
        if file_call_edges:
            lines.append("")
            lines.append("CALLS OUT")
            for edge in file_call_edges[:80]:
                lines.append("- " + edge.get("from_symbol", "") + " -> " + edge.get("to_call", ""))

        if functions:
            lines.append("")
            lines.append("TOP-LEVEL FUNCTIONS")
            for fn in functions[:50]:
                lines.append("- " + fn.get("qualname", "") + "  (line " + str(fn.get("lineno", "")) + ")")

        if classes:
            lines.append("")
            lines.append("CLASSES")
            for cls in classes[:50]:
                class_line = "- " + cls.get("name", "") + "  (line " + str(cls.get("lineno", "")) + ")"
                bases = cls.get("bases", [])
                if bases:
                    class_line += "  bases: " + ", ".join(bases)
                lines.append(class_line)

                methods = cls.get("methods", [])
                for method in methods[:20]:
                    lines.append("    * " + method.get("qualname", ""))

        lines.append("")
        lines.append("RELATED SYMBOL INDEX HINTS")
        symbol_hits = []

        for fn in functions[:20]:
            symbol_name = fn.get("qualname", "")
            if symbol_name in symbol_index:
                symbol_hits.append(symbol_name)

        for cls in classes[:20]:
            cls_name = cls.get("name", "")
            if cls_name in symbol_index:
                symbol_hits.append(cls_name)
            for method in cls.get("methods", [])[:10]:
                method_name = method.get("qualname", "")
                if method_name in symbol_index:
                    symbol_hits.append(method_name)

        if symbol_hits:
            for symbol_name in sorted(set(symbol_hits))[:30]:
                lines.append("- " + symbol_name + " -> " + ", ".join(symbol_index.get(symbol_name, [])))
        else:
            lines.append("- none")

        return "\n".join(lines)

    def display_result_details(self, current: QListWidgetItem, previous: QListWidgetItem) -> None:
        _ = previous
        if not current:
            self.result_details.clear()
            return

        result = current.data(Qt.UserRole)
        if not result:
            self.result_details.clear()
            return

        self.result_details.setPlainText(result.get("detail", ""))


def main() -> None:
    app = QApplication(sys.argv)
    window = JsonProjectExplorer()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

How to use it:
generate your project_structure_index.json
run this GUI
load the JSON
ask questions like:
which module starts the app
which code creates superior tab
show me which code is implementing topomap
where is timeline wired
where is splash created
where is reset and snapshot flow

Good next improvement:
I can build version 2 with a dedicated graph view for:
startup chain
tab creation chain
topomap chain
timeline chain

go
Thought for 6s

Here is version 2.

It adds:
a dedicated graph explorer
startup chain view
tab creation view
topomap chain view
timeline chain view
splash chain view
reset/snapshot chain view
interactive file detail panel
ranked matches plus graph neighbors

This app loads the JSON produced by the first indexer app and builds navigable relationship views from:
entry files
imports
call edges
semantic roles
keyword hits

"""
PySide6 Project JSON Explorer v2

Loads a project_structure_index.json and provides:
- natural-language question search
- graph-oriented views for startup, tabs, topomap, timeline, splash, reset
- file detail panel
- relation panel with imports and calls

Compatible with standard CPython and Windows.
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections import defaultdict, deque
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QSplitter,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


def norm_text(value: Any) -> str:
    return str(value).strip().lower() if value is not None else ""


def tokenize_query(text: str) -> list[str]:
    tokens = re.findall(r"[a-zA-Z0-9_\.]+", text.lower())
    stop_words = {
        "the", "is", "are", "a", "an", "of", "to", "me", "show", "which", "what",
        "where", "who", "does", "do", "in", "on", "for", "and", "or", "with",
        "code", "module", "file", "implementing", "implements", "created",
        "creates", "create", "that", "this", "app",
    }
    return [token for token in tokens if token not in stop_words]


class ProjectJsonExplorerV2(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Project JSON Explorer v2")
        self.resize(1500, 900)

        self.index_data: dict[str, Any] | None = None
        self.files_by_path: dict[str, dict[str, Any]] = {}
        self.files_by_module: dict[str, dict[str, Any]] = {}
        self.call_graph_out: dict[str, set[str]] = defaultdict(set)
        self.call_graph_in: dict[str, set[str]] = defaultdict(set)
        self.import_graph_out: dict[str, set[str]] = defaultdict(set)
        self.import_graph_in: dict[str, set[str]] = defaultdict(set)

        self.json_path_edit = QLineEdit()
        self.question_edit = QLineEdit()

        self.load_button = QPushButton("Load JSON")
        self.ask_button = QPushButton("Ask")
        self.clear_button = QPushButton("Clear")

        self.quick_startup_button = QPushButton("Startup")
        self.quick_tabs_button = QPushButton("Tabs")
        self.quick_topomap_button = QPushButton("Topomap")
        self.quick_timeline_button = QPushButton("Timeline")
        self.quick_splash_button = QPushButton("Splash")
        self.quick_reset_button = QPushButton("Reset")

        self.result_list = QListWidget()
        self.detail_text = QPlainTextEdit()
        self.detail_text.setReadOnly(True)

        self.graph_list = QListWidget()
        self.graph_text = QPlainTextEdit()
        self.graph_text.setReadOnly(True)

        self.log_box = QPlainTextEdit()
        self.log_box.setReadOnly(True)

        self.tabs = QTabWidget()

        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

        top_row = QHBoxLayout()
        top_row.addWidget(QLabel("JSON:"))
        top_row.addWidget(self.json_path_edit)
        top_row.addWidget(self.load_button)

        query_row = QHBoxLayout()
        query_row.addWidget(QLabel("Question:"))
        query_row.addWidget(self.question_edit)
        query_row.addWidget(self.ask_button)
        query_row.addWidget(self.clear_button)

        quick_row = QHBoxLayout()
        quick_row.addWidget(self.quick_startup_button)
        quick_row.addWidget(self.quick_tabs_button)
        quick_row.addWidget(self.quick_topomap_button)
        quick_row.addWidget(self.quick_timeline_button)
        quick_row.addWidget(self.quick_splash_button)
        quick_row.addWidget(self.quick_reset_button)
        quick_row.addStretch()

        search_page = QWidget()
        search_layout = QVBoxLayout(search_page)
        search_splitter = QSplitter(Qt.Horizontal)
        search_splitter.addWidget(self.result_list)
        search_splitter.addWidget(self.detail_text)
        search_splitter.setSizes([500, 900])
        search_layout.addWidget(search_splitter)

        graph_page = QWidget()
        graph_layout = QVBoxLayout(graph_page)
        graph_splitter = QSplitter(Qt.Horizontal)
        graph_splitter.addWidget(self.graph_list)
        graph_splitter.addWidget(self.graph_text)
        graph_splitter.setSizes([500, 900])
        graph_layout.addWidget(graph_splitter)

        self.tabs.addTab(search_page, "Search")
        self.tabs.addTab(graph_page, "Graph Views")

        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout(log_group)
        log_layout.addWidget(self.log_box)

        main_layout.addLayout(top_row)
        main_layout.addLayout(query_row)
        main_layout.addLayout(quick_row)
        main_layout.addWidget(self.tabs, stretch=1)
        main_layout.addWidget(log_group, stretch=0)

    def _connect_signals(self) -> None:
        self.load_button.clicked.connect(self.load_json)
        self.ask_button.clicked.connect(self.ask_question)
        self.clear_button.clicked.connect(self.clear_all)
        self.question_edit.returnPressed.connect(self.ask_question)

        self.quick_startup_button.clicked.connect(lambda: self.run_graph_view("startup"))
        self.quick_tabs_button.clicked.connect(lambda: self.run_graph_view("tabs"))
        self.quick_topomap_button.clicked.connect(lambda: self.run_graph_view("topomap"))
        self.quick_timeline_button.clicked.connect(lambda: self.run_graph_view("timeline"))
        self.quick_splash_button.clicked.connect(lambda: self.run_graph_view("splash"))
        self.quick_reset_button.clicked.connect(lambda: self.run_graph_view("reset"))

        self.result_list.currentItemChanged.connect(self._show_result_detail)
        self.graph_list.currentItemChanged.connect(self._show_graph_detail)

    def append_log(self, text: str) -> None:
        self.log_box.appendPlainText(text)

    def clear_all(self) -> None:
        self.result_list.clear()
        self.detail_text.clear()
        self.graph_list.clear()
        self.graph_text.clear()
        self.log_box.clear()

    def load_json(self) -> None:
        current = self.json_path_edit.text().strip()
        start_dir = os.path.dirname(current) if current else os.getcwd()

        file_path, _filter = QFileDialog.getOpenFileName(
            self,
            "Load project_structure_index.json",
            start_dir,
            "JSON Files (*.json)",
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as handle:
                self.index_data = json.load(handle)

            self.json_path_edit.setText(file_path)
            self._rebuild_indexes()
            self.append_log("Loaded: " + file_path)

            summary = self.index_data.get("project_summary", {})
            self.append_log("Python files: " + str(summary.get("python_file_count", "unknown")))
            self.append_log("Entry files: " + str(summary.get("entry_file_count", "unknown")))

            QMessageBox.information(self, "Loaded", "JSON loaded successfully.")
        except Exception as exc:
            QMessageBox.critical(self, "Error", "Failed to load JSON:\n" + str(exc))
            self.append_log("ERROR: " + str(exc))

    def _rebuild_indexes(self) -> None:
        self.files_by_path.clear()
        self.files_by_module.clear()
        self.call_graph_out.clear()
        self.call_graph_in.clear()
        self.import_graph_out.clear()
        self.import_graph_in.clear()

        if not self.index_data:
            return

        for file_record in self.index_data.get("files", []):
            path = file_record.get("path", "")
            module_name = file_record.get("module_name", "")
            self.files_by_path[path] = file_record
            if module_name:
                self.files_by_module[module_name] = file_record

        for src_module, targets in self.index_data.get("import_graph", {}).items():
            src_path = self._resolve_module_to_path(src_module) or src_module
            for target in targets:
                self.import_graph_out[src_path].add(target)
                self.import_graph_in[target].add(src_path)

        for edge in self.index_data.get("call_edges", []):
            from_file = edge.get("from_file", "")
            to_call = edge.get("to_call", "")
            if from_file and to_call:
                self.call_graph_out[from_file].add(to_call)
                self.call_graph_in[to_call].add(from_file)

    def _resolve_module_to_path(self, module_name: str) -> str | None:
        record = self.files_by_module.get(module_name)
        if record:
            return record.get("path")
        return None

    def ask_question(self) -> None:
        if not self.index_data:
            QMessageBox.warning(self, "No JSON", "Please load a JSON file first.")
            return

        question = self.question_edit.text().strip()
        if not question:
            QMessageBox.warning(self, "No Question", "Please type a question.")
            return

        self.result_list.clear()
        self.detail_text.clear()
        self.tabs.setCurrentIndex(0)

        results = self._search(question)
        self.append_log("Question: " + question)
        self.append_log("Results: " + str(len(results)))

        for result in results:
            item = QListWidgetItem(result["title"])
            item.setData(Qt.UserRole, result)
            self.result_list.addItem(item)

        if results:
            self.result_list.setCurrentRow(0)

    def _search(self, question: str) -> list[dict[str, Any]]:
        q = norm_text(question)
        tokens = tokenize_query(q)
        entry_files = set(self.index_data.get("entry_files", []))
        semantic_roles = self.index_data.get("semantic_roles", {})

        scored: list[dict[str, Any]] = []

        for path, file_record in self.files_by_path.items():
            module_name = file_record.get("module_name", "")
            docstring = file_record.get("docstring", "")
            strings = " ".join(file_record.get("strings", []))
            comments = " ".join(file_record.get("comments", []))
            ui_hits = " ".join(file_record.get("ui_keyword_hits", []))
            eeg_hits = " ".join(file_record.get("eeg_keyword_hits", []))
            semantic_hints = " ".join(file_record.get("semantic_hints", []))
            entry_markers = " ".join(file_record.get("entry_markers", []))

            function_names = []
            call_names = []
            class_names = []

            for fn in file_record.get("functions", []):
                function_names.append(fn.get("name", ""))
                function_names.append(fn.get("qualname", ""))
                for call in fn.get("calls", []):
                    call_names.append(call.get("call_name", ""))

            for cls in file_record.get("classes", []):
                class_names.append(cls.get("name", ""))
                for method in cls.get("methods", []):
                    function_names.append(method.get("name", ""))
                    function_names.append(method.get("qualname", ""))
                    for call in method.get("calls", []):
                        call_names.append(call.get("call_name", ""))

            haystack = " ".join([
                norm_text(path),
                norm_text(module_name),
                norm_text(docstring),
                norm_text(strings),
                norm_text(comments),
                norm_text(ui_hits),
                norm_text(eeg_hits),
                norm_text(semantic_hints),
                norm_text(entry_markers),
                norm_text(" ".join(function_names)),
                norm_text(" ".join(call_names)),
                norm_text(" ".join(class_names)),
            ])

            roles = semantic_roles.get(path, {}).get("roles", [])
            score = 0
            reasons = []

            for token in tokens:
                if token in haystack:
                    score += 3
                    reasons.append("token match: " + token)

            if path in entry_files and ("start" in q or "main" in q or "entry" in q or "launch" in q):
                score += 20
                reasons.append("entry file")

            if "topomap" in q and ("topomap" in haystack or "amplitude_map" in haystack or "topomap" in roles):
                score += 18
                reasons.append("topomap match")

            if "tab" in q and ("addtab" in haystack or "notebook" in haystack or "tabs" in roles):
                score += 15
                reasons.append("tab match")

            if "timeline" in q and ("timeline" in haystack or "timeline" in roles):
                score += 15
                reasons.append("timeline match")

            if "splash" in q and ("splash" in haystack or "splash" in roles):
                score += 15
                reasons.append("splash match")

            if ("reset" in q or "snapshot" in q) and (
                "reset" in haystack or "snapshot" in haystack or "state_reset" in roles
            ):
                score += 15
                reasons.append("reset or snapshot match")

            if score > 0:
                scored.append(
                    {
                        "score": score,
                        "title": "[" + str(score) + "] " + path + " | " + module_name,
                        "detail": self._build_file_detail(path, reasons),
                        "path": path,
                    }
                )

        scored.sort(key=lambda item: (-item["score"], item["path"]))
        return scored[:50]

    def _build_file_detail(self, path: str, reasons: list[str]) -> str:
        file_record = self.files_by_path[path]
        semantic_roles = self.index_data.get("semantic_roles", {})
        roles = semantic_roles.get(path, {}).get("roles", [])

        lines = []
        lines.append("FILE")
        lines.append(path)
        lines.append("")
        lines.append("MODULE")
        lines.append(file_record.get("module_name", ""))
        lines.append("")
        lines.append("WHY THIS MATCHED")
        for reason in sorted(set(reasons)):
            lines.append("- " + reason)

        lines.append("")
        lines.append("ROLES")
        if roles:
            for role in roles:
                lines.append("- " + role)
        else:
            lines.append("- none")

        if file_record.get("entry_markers"):
            lines.append("")
            lines.append("ENTRY MARKERS")
            for marker in file_record["entry_markers"]:
                lines.append("- " + marker)

        if file_record.get("docstring"):
            lines.append("")
            lines.append("DOCSTRING")
            lines.append(file_record["docstring"])

        if file_record.get("functions"):
            lines.append("")
            lines.append("FUNCTIONS")
            for fn in file_record["functions"][:40]:
                lines.append("- " + fn.get("qualname", "") + " (line " + str(fn.get("lineno", "")) + ")")

        if file_record.get("classes"):
            lines.append("")
            lines.append("CLASSES")
            for cls in file_record["classes"][:30]:
                line = "- " + cls.get("name", "") + " (line " + str(cls.get("lineno", "")) + ")"
                bases = cls.get("bases", [])
                if bases:
                    line += " bases: " + ", ".join(bases)
                lines.append(line)
                for method in cls.get("methods", [])[:15]:
                    lines.append("    * " + method.get("qualname", ""))

        imports_out = sorted(self.import_graph_out.get(path, []))
        if imports_out:
            lines.append("")
            lines.append("IMPORTS OUT")
            for item in imports_out[:50]:
                lines.append("- " + item)

        calls_out = sorted(self.call_graph_out.get(path, []))
        if calls_out:
            lines.append("")
            lines.append("CALLS OUT")
            for item in calls_out[:80]:
                lines.append("- " + item)

        return "\n".join(lines)

    def _show_result_detail(self, current: QListWidgetItem, previous: QListWidgetItem) -> None:
        _ = previous
        if not current:
            self.detail_text.clear()
            return
        payload = current.data(Qt.UserRole)
        self.detail_text.setPlainText(payload.get("detail", ""))

    def run_graph_view(self, mode: str) -> None:
        if not self.index_data:
            QMessageBox.warning(self, "No JSON", "Please load a JSON file first.")
            return

        self.graph_list.clear()
        self.graph_text.clear()
        self.tabs.setCurrentIndex(1)

        nodes = self._collect_graph_nodes(mode)
        self.append_log("Graph view: " + mode)
        self.append_log("Nodes found: " + str(len(nodes)))

        for node in nodes:
            item = QListWidgetItem(node["title"])
            item.setData(Qt.UserRole, node)
            self.graph_list.addItem(item)

        if nodes:
            self.graph_list.setCurrentRow(0)

    def _collect_graph_nodes(self, mode: str) -> list[dict[str, Any]]:
        semantic_roles = self.index_data.get("semantic_roles", {})
        entry_files = set(self.index_data.get("entry_files", []))
        nodes = []

        for path, file_record in self.files_by_path.items():
            roles = semantic_roles.get(path, {}).get("roles", [])
            title = path + " | " + file_record.get("module_name", "")

            matched = False
            reasons = []

            if mode == "startup":
                if path in entry_files or "startup" in roles or "main_window" in roles:
                    matched = True
                    reasons.append("startup related")
            elif mode == "tabs":
                if "tabs" in roles or "notebook" in title.lower() or "addtab" in self._all_text(path):
                    matched = True
                    reasons.append("tab related")
            elif mode == "topomap":
                if "topomap" in roles or "topomap" in self._all_text(path) or "amplitude_map" in self._all_text(path):
                    matched = True
                    reasons.append("topomap related")
            elif mode == "timeline":
                if "timeline" in roles or "timeline" in self._all_text(path):
                    matched = True
                    reasons.append("timeline related")
            elif mode == "splash":
                if "splash" in roles or "splash" in self._all_text(path):
                    matched = True
                    reasons.append("splash related")
            elif mode == "reset":
                text = self._all_text(path)
                if "state_reset" in roles or "reset" in text or "snapshot" in text:
                    matched = True
                    reasons.append("reset or snapshot related")

            if matched:
                nodes.append(
                    {
                        "title": title,
                        "detail": self._build_graph_detail(path, reasons),
                        "path": path,
                    }
                )

        nodes.sort(key=lambda item: item["path"])
        return nodes[:80]

    def _all_text(self, path: str) -> str:
        file_record = self.files_by_path[path]
        parts = [
            path,
            file_record.get("module_name", ""),
            file_record.get("docstring", ""),
            " ".join(file_record.get("strings", [])),
            " ".join(file_record.get("comments", [])),
            " ".join(file_record.get("entry_markers", [])),
            " ".join(file_record.get("ui_keyword_hits", [])),
            " ".join(file_record.get("eeg_keyword_hits", [])),
            " ".join(file_record.get("semantic_hints", [])),
        ]

        for fn in file_record.get("functions", []):
            parts.append(fn.get("qualname", ""))
            for call in fn.get("calls", []):
                parts.append(call.get("call_name", ""))

        for cls in file_record.get("classes", []):
            parts.append(cls.get("name", ""))
            for method in cls.get("methods", []):
                parts.append(method.get("qualname", ""))
                for call in method.get("calls", []):
                    parts.append(call.get("call_name", ""))

        return norm_text(" ".join(parts))

    def _build_graph_detail(self, path: str, reasons: list[str]) -> str:
        file_record = self.files_by_path[path]
        semantic_roles = self.index_data.get("semantic_roles", {})
        roles = semantic_roles.get(path, {}).get("roles", [])

        lines = []
        lines.append("NODE")
        lines.append(path)
        lines.append("")
        lines.append("WHY INCLUDED")
        for reason in reasons:
            lines.append("- " + reason)

        lines.append("")
        lines.append("ROLES")
        if roles:
            for role in roles:
                lines.append("- " + role)
        else:
            lines.append("- none")

        lines.append("")
        lines.append("OUTGOING IMPORTS")
        imports_out = sorted(self.import_graph_out.get(path, []))
        if imports_out:
            for item in imports_out[:50]:
                lines.append("- " + item)
        else:
            lines.append("- none")

        lines.append("")
        lines.append("OUTGOING CALLS")
        calls_out = sorted(self.call_graph_out.get(path, []))
        if calls_out:
            for item in calls_out[:80]:
                lines.append("- " + item)
        else:
            lines.append("- none")

        lines.append("")
        lines.append("NEIGHBOR FILE HINTS")
        neighbor_paths = self._infer_neighbor_files(path)
        if neighbor_paths:
            for item in neighbor_paths[:40]:
                lines.append("- " + item)
        else:
            lines.append("- none")

        lines.append("")
        lines.append("FILE SUMMARY")
        lines.append(self._build_file_detail(path, reasons))

        return "\n".join(lines)

    def _infer_neighbor_files(self, path: str) -> list[str]:
        neighbors = set()

        for module_target in self.import_graph_out.get(path, set()):
            resolved = self._resolve_module_to_path(module_target)
            if resolved:
                neighbors.add(resolved)

        for call_name in self.call_graph_out.get(path, set()):
            for file_path, file_record in self.files_by_path.items():
                if self._file_contains_symbol(file_record, call_name):
                    neighbors.add(file_path)

        return sorted(neighbors)

    def _file_contains_symbol(self, file_record: dict[str, Any], symbol_name: str) -> bool:
        for fn in file_record.get("functions", []):
            if fn.get("name") == symbol_name or fn.get("qualname") == symbol_name:
                return True
        for cls in file_record.get("classes", []):
            if cls.get("name") == symbol_name:
                return True
            for method in cls.get("methods", []):
                if method.get("name") == symbol_name or method.get("qualname") == symbol_name:
                    return True
        return False

    def _show_graph_detail(self, current: QListWidgetItem, previous: QListWidgetItem) -> None:
        _ = previous
        if not current:
            self.graph_text.clear()
            return
        payload = current.data(Qt.UserRole)
        self.graph_text.setPlainText(payload.get("detail", ""))


def main() -> None:
    app = QApplication(sys.argv)
    window = ProjectJsonExplorerV2()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

How to use it:
run your first GUI indexer and generate project_structure_index.json
run this second GUI
load the JSON
either ask questions manually or use the quick graph buttons

Best workflow:
first generate the JSON after each major refactor
then use this explorer to answer:
which module starts the app
which code creates the superior tab
which module implements topomap
where timeline is wired
where splash is created
where reset and snapshot are handled

Next step that would make this much stronger:
I can build version 3 that opens the original .py file directly from a selected result and jumps to the approximate line number for the matched symbol.

go
Thought for 4s

Here is version 3.

It adds the practical missing piece:
you can load the JSON, ask questions, inspect graph views, and also open the original .py file from a selected result and jump to an approximate line.

It includes:
JSON loader
natural-language search
graph views
file detail panel
source preview panel
open source file from result
jump to best matched line
line-aware display for functions, methods, classes, and entry points

"""
PySide6 Project JSON Explorer v3

Features
--------
1. Load a project_structure_index.json file.
2. Ask architecture questions.
3. Browse graph-oriented views:
   - startup
   - tabs
   - topomap
   - timeline
   - splash
   - reset
4. Preview source code for a selected result.
5. Open the original Python file and jump to an approximate line.
6. Works best with JSON generated by the earlier semantic indexer.

Notes
-----
- This app assumes the JSON contains "project_summary.project_root" and "files".
- Source preview is read directly from disk using the project root + file path from JSON.
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections import defaultdict
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QSplitter,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


def norm_text(value: Any) -> str:
    return str(value).strip().lower() if value is not None else ""


def tokenize_query(text: str) -> list[str]:
    tokens = re.findall(r"[a-zA-Z0-9_\.]+", text.lower())
    stop_words = {
        "the",
        "is",
        "are",
        "a",
        "an",
        "of",
        "to",
        "me",
        "show",
        "which",
        "what",
        "where",
        "who",
        "does",
        "do",
        "in",
        "on",
        "for",
        "and",
        "or",
        "with",
        "code",
        "module",
        "file",
        "implementing",
        "implements",
        "created",
        "creates",
        "create",
        "that",
        "this",
        "app",
    }
    return [token for token in tokens if token not in stop_words]


def safe_read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return handle.read()


class ProjectJsonExplorerV3(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Project JSON Explorer v3")
        self.resize(1700, 980)

        self.index_data: dict[str, Any] | None = None
        self.project_root: str = ""
        self.files_by_path: dict[str, dict[str, Any]] = {}
        self.files_by_module: dict[str, dict[str, Any]] = {}
        self.call_graph_out: dict[str, set[str]] = defaultdict(set)
        self.import_graph_out: dict[str, set[str]] = defaultdict(set)

        self.json_path_edit = QLineEdit()
        self.question_edit = QLineEdit()

        self.load_button = QPushButton("Load JSON")
        self.ask_button = QPushButton("Ask")
        self.clear_button = QPushButton("Clear")
        self.open_source_button = QPushButton("Open Source File")
        self.refresh_source_button = QPushButton("Refresh Source Preview")

        self.quick_startup_button = QPushButton("Startup")
        self.quick_tabs_button = QPushButton("Tabs")
        self.quick_topomap_button = QPushButton("Topomap")
        self.quick_timeline_button = QPushButton("Timeline")
        self.quick_splash_button = QPushButton("Splash")
        self.quick_reset_button = QPushButton("Reset")

        self.result_list = QListWidget()
        self.detail_text = QPlainTextEdit()
        self.detail_text.setReadOnly(True)

        self.graph_list = QListWidget()
        self.graph_text = QPlainTextEdit()
        self.graph_text.setReadOnly(True)

        self.source_preview = QPlainTextEdit()
        self.source_preview.setReadOnly(True)
        self.source_path_label = QLabel("Source: -")

        self.log_box = QPlainTextEdit()
        self.log_box.setReadOnly(True)

        self.tabs = QTabWidget()

        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

        load_row = QHBoxLayout()
        load_row.addWidget(QLabel("JSON:"))
        load_row.addWidget(self.json_path_edit)
        load_row.addWidget(self.load_button)

        query_row = QHBoxLayout()
        query_row.addWidget(QLabel("Question:"))
        query_row.addWidget(self.question_edit)
        query_row.addWidget(self.ask_button)
        query_row.addWidget(self.clear_button)

        quick_row = QHBoxLayout()
        quick_row.addWidget(self.quick_startup_button)
        quick_row.addWidget(self.quick_tabs_button)
        quick_row.addWidget(self.quick_topomap_button)
        quick_row.addWidget(self.quick_timeline_button)
        quick_row.addWidget(self.quick_splash_button)
        quick_row.addWidget(self.quick_reset_button)
        quick_row.addStretch()
        quick_row.addWidget(self.refresh_source_button)
        quick_row.addWidget(self.open_source_button)

        search_page = QWidget()
        search_layout = QVBoxLayout(search_page)

        search_splitter = QSplitter(Qt.Horizontal)
        search_splitter.addWidget(self.result_list)
        search_splitter.addWidget(self.detail_text)
        search_splitter.addWidget(self.source_preview)
        search_splitter.setSizes([420, 620, 760])

        search_layout.addWidget(self.source_path_label)
        search_layout.addWidget(search_splitter)

        graph_page = QWidget()
        graph_layout = QVBoxLayout(graph_page)

        graph_splitter = QSplitter(Qt.Horizontal)
        graph_splitter.addWidget(self.graph_list)
        graph_splitter.addWidget(self.graph_text)
        graph_splitter.addWidget(self.source_preview)
        graph_splitter.setSizes([420, 620, 760])

        graph_layout.addWidget(self.source_path_label)
        graph_layout.addWidget(graph_splitter)

        self.tabs.addTab(search_page, "Search")
        self.tabs.addTab(graph_page, "Graph Views")

        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout(log_group)
        log_layout.addWidget(self.log_box)

        main_layout.addLayout(load_row)
        main_layout.addLayout(query_row)
        main_layout.addLayout(quick_row)
        main_layout.addWidget(self.tabs, stretch=1)
        main_layout.addWidget(log_group, stretch=0)

    def _connect_signals(self) -> None:
        self.load_button.clicked.connect(self.load_json)
        self.ask_button.clicked.connect(self.ask_question)
        self.clear_button.clicked.connect(self.clear_all)
        self.question_edit.returnPressed.connect(self.ask_question)

        self.quick_startup_button.clicked.connect(lambda: self.run_graph_view("startup"))
        self.quick_tabs_button.clicked.connect(lambda: self.run_graph_view("tabs"))
        self.quick_topomap_button.clicked.connect(lambda: self.run_graph_view("topomap"))
        self.quick_timeline_button.clicked.connect(lambda: self.run_graph_view("timeline"))
        self.quick_splash_button.clicked.connect(lambda: self.run_graph_view("splash"))
        self.quick_reset_button.clicked.connect(lambda: self.run_graph_view("reset"))

        self.result_list.currentItemChanged.connect(self._show_result_detail)
        self.graph_list.currentItemChanged.connect(self._show_graph_detail)

        self.refresh_source_button.clicked.connect(self.refresh_source_preview)
        self.open_source_button.clicked.connect(self.open_selected_source_file)

    def append_log(self, text: str) -> None:
        self.log_box.appendPlainText(text)

    def clear_all(self) -> None:
        self.result_list.clear()
        self.graph_list.clear()
        self.detail_text.clear()
        self.graph_text.clear()
        self.source_preview.clear()
        self.source_path_label.setText("Source: -")
        self.log_box.clear()

    def load_json(self) -> None:
        current = self.json_path_edit.text().strip()
        start_dir = os.path.dirname(current) if current else os.getcwd()

        file_path, _filter = QFileDialog.getOpenFileName(
            self,
            "Load project_structure_index.json",
            start_dir,
            "JSON Files (*.json)",
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as handle:
                self.index_data = json.load(handle)

            self.json_path_edit.setText(file_path)
            self.project_root = (
                self.index_data.get("project_summary", {}).get("project_root", "") or ""
            )
            self._rebuild_indexes()

            self.append_log("Loaded JSON: " + file_path)
            self.append_log("Project root: " + self.project_root)

            summary = self.index_data.get("project_summary", {})
            self.append_log("Python files: " + str(summary.get("python_file_count", "unknown")))
            self.append_log("Entry files: " + str(summary.get("entry_file_count", "unknown")))

            QMessageBox.information(self, "Loaded", "JSON loaded successfully.")
        except Exception as exc:
            QMessageBox.critical(self, "Error", "Failed to load JSON:\n" + str(exc))
            self.append_log("ERROR loading JSON: " + str(exc))

    def _rebuild_indexes(self) -> None:
        self.files_by_path.clear()
        self.files_by_module.clear()
        self.call_graph_out.clear()
        self.import_graph_out.clear()

        if not self.index_data:
            return

        for file_record in self.index_data.get("files", []):
            path = file_record.get("path", "")
            module_name = file_record.get("module_name", "")
            if path:
                self.files_by_path[path] = file_record
            if module_name:
                self.files_by_module[module_name] = file_record

        for src_module, targets in self.index_data.get("import_graph", {}).items():
            src_path = self._resolve_module_to_path(src_module) or src_module
            for target in targets:
                self.import_graph_out[src_path].add(target)

        for edge in self.index_data.get("call_edges", []):
            from_file = edge.get("from_file", "")
            to_call = edge.get("to_call", "")
            if from_file and to_call:
                self.call_graph_out[from_file].add(to_call)

    def _resolve_module_to_path(self, module_name: str) -> str | None:
        record = self.files_by_module.get(module_name)
        if record:
            return record.get("path")
        return None

    def ask_question(self) -> None:
        if not self.index_data:
            QMessageBox.warning(self, "No JSON", "Please load a JSON file first.")
            return

        question = self.question_edit.text().strip()
        if not question:
            QMessageBox.warning(self, "No Question", "Please type a question.")
            return

        self.result_list.clear()
        self.detail_text.clear()
        self.tabs.setCurrentIndex(0)

        results = self._search(question)

        self.append_log("Question: " + question)
        self.append_log("Search results: " + str(len(results)))

        for result in results:
            item = QListWidgetItem(result["title"])
            item.setData(Qt.UserRole, result)
            self.result_list.addItem(item)

        if results:
            self.result_list.setCurrentRow(0)

    def _search(self, question: str) -> list[dict[str, Any]]:
        q = norm_text(question)
        tokens = tokenize_query(q)
        entry_files = set(self.index_data.get("entry_files", []))
        semantic_roles = self.index_data.get("semantic_roles", {})

        scored: list[dict[str, Any]] = []

        for path, file_record in self.files_by_path.items():
            module_name = file_record.get("module_name", "")
            docstring = file_record.get("docstring", "")
            strings = " ".join(file_record.get("strings", []))
            comments = " ".join(file_record.get("comments", []))
            ui_hits = " ".join(file_record.get("ui_keyword_hits", []))
            eeg_hits = " ".join(file_record.get("eeg_keyword_hits", []))
            semantic_hints = " ".join(file_record.get("semantic_hints", []))
            entry_markers = " ".join(file_record.get("entry_markers", []))

            function_names = []
            call_names = []
            class_names = []

            for fn in file_record.get("functions", []):
                function_names.append(fn.get("name", ""))
                function_names.append(fn.get("qualname", ""))
                for call in fn.get("calls", []):
                    call_names.append(call.get("call_name", ""))

            for cls in file_record.get("classes", []):
                class_names.append(cls.get("name", ""))
                for method in cls.get("methods", []):
                    function_names.append(method.get("name", ""))
                    function_names.append(method.get("qualname", ""))
                    for call in method.get("calls", []):
                        call_names.append(call.get("call_name", ""))

            haystack = " ".join([
                norm_text(path),
                norm_text(module_name),
                norm_text(docstring),
                norm_text(strings),
                norm_text(comments),
                norm_text(ui_hits),
                norm_text(eeg_hits),
                norm_text(semantic_hints),
                norm_text(entry_markers),
                norm_text(" ".join(function_names)),
                norm_text(" ".join(call_names)),
                norm_text(" ".join(class_names)),
            ])

            roles = semantic_roles.get(path, {}).get("roles", [])
            score = 0
            reasons = []

            for token in tokens:
                if token in haystack:
                    score += 3
                    reasons.append("token match: " + token)

            if path in entry_files and ("start" in q or "main" in q or "entry" in q or "launch" in q):
                score += 20
                reasons.append("entry file")

            if "topomap" in q and ("topomap" in haystack or "amplitude_map" in haystack or "topomap" in roles):
                score += 18
                reasons.append("topomap match")

            if "tab" in q and ("addtab" in haystack or "notebook" in haystack or "tabs" in roles):
                score += 15
                reasons.append("tab match")

            if "timeline" in q and ("timeline" in haystack or "timeline" in roles):
                score += 15
                reasons.append("timeline match")

            if "splash" in q and ("splash" in haystack or "splash" in roles):
                score += 15
                reasons.append("splash match")

            if ("reset" in q or "snapshot" in q) and (
                "reset" in haystack or "snapshot" in haystack or "state_reset" in roles
            ):
                score += 15
                reasons.append("reset or snapshot match")

            if score > 0:
                best_line = self._best_line_for_file(file_record, q)
                scored.append(
                    {
                        "score": score,
                        "title": "[" + str(score) + "] " + path + " | " + module_name,
                        "detail": self._build_file_detail(path, reasons),
                        "path": path,
                        "line": best_line,
                    }
                )

        scored.sort(key=lambda item: (-item["score"], item["path"]))
        return scored[:50]

    def _best_line_for_file(self, file_record: dict[str, Any], question: str) -> int:
        q = norm_text(question)

        for fn in file_record.get("functions", []):
            if norm_text(fn.get("qualname", "")) in q or norm_text(fn.get("name", "")) in q:
                return int(fn.get("lineno", 1))

        for cls in file_record.get("classes", []):
            if norm_text(cls.get("name", "")) in q:
                return int(cls.get("lineno", 1))
            for method in cls.get("methods", []):
                if norm_text(method.get("qualname", "")) in q or norm_text(method.get("name", "")) in q:
                    return int(method.get("lineno", 1))

        entry_markers = file_record.get("entry_markers", [])
        if entry_markers:
            return 1

        if file_record.get("functions"):
            return int(file_record["functions"][0].get("lineno", 1))

        if file_record.get("classes"):
            return int(file_record["classes"][0].get("lineno", 1))

        return 1

    def _build_file_detail(self, path: str, reasons: list[str]) -> str:
        file_record = self.files_by_path[path]
        semantic_roles = self.index_data.get("semantic_roles", {})
        roles = semantic_roles.get(path, {}).get("roles", [])

        lines = []
        lines.append("FILE")
        lines.append(path)
        lines.append("")
        lines.append("MODULE")
        lines.append(file_record.get("module_name", ""))
        lines.append("")
        lines.append("WHY THIS MATCHED")
        for reason in sorted(set(reasons)):
            lines.append("- " + reason)

        lines.append("")
        lines.append("ROLES")
        if roles:
            for role in roles:
                lines.append("- " + role)
        else:
            lines.append("- none")

        if file_record.get("entry_markers"):
            lines.append("")
            lines.append("ENTRY MARKERS")
            for marker in file_record["entry_markers"]:
                lines.append("- " + marker)

        if file_record.get("docstring"):
            lines.append("")
            lines.append("DOCSTRING")
            lines.append(file_record["docstring"])

        if file_record.get("functions"):
            lines.append("")
            lines.append("FUNCTIONS")
            for fn in file_record["functions"][:40]:
                lines.append("- " + fn.get("qualname", "") + " (line " + str(fn.get("lineno", "")) + ")")

        if file_record.get("classes"):
            lines.append("")
            lines.append("CLASSES")
            for cls in file_record["classes"][:30]:
                line = "- " + cls.get("name", "") + " (line " + str(cls.get("lineno", "")) + ")"
                bases = cls.get("bases", [])
                if bases:
                    line += " bases: " + ", ".join(bases)
                lines.append(line)
                for method in cls.get("methods", [])[:15]:
                    lines.append("    * " + method.get("qualname", "") + " (line " + str(method.get("lineno", "")) + ")")

        imports_out = sorted(self.import_graph_out.get(path, []))
        if imports_out:
            lines.append("")
            lines.append("IMPORTS OUT")
            for item in imports_out[:50]:
                lines.append("- " + item)

        calls_out = sorted(self.call_graph_out.get(path, []))
        if calls_out:
            lines.append("")
            lines.append("CALLS OUT")
            for item in calls_out[:80]:
                lines.append("- " + item)

        return "\n".join(lines)

    def _show_result_detail(self, current: QListWidgetItem, previous: QListWidgetItem) -> None:
        _ = previous
        if not current:
            self.detail_text.clear()
            return

        payload = current.data(Qt.UserRole)
        if not payload:
            return

        self.detail_text.setPlainText(payload.get("detail", ""))
        self._load_source_preview(payload.get("path", ""), int(payload.get("line", 1)))

    def run_graph_view(self, mode: str) -> None:
        if not self.index_data:
            QMessageBox.warning(self, "No JSON", "Please load a JSON file first.")
            return

        self.graph_list.clear()
        self.graph_text.clear()
        self.tabs.setCurrentIndex(1)

        nodes = self._collect_graph_nodes(mode)

        self.append_log("Graph view: " + mode)
        self.append_log("Graph nodes: " + str(len(nodes)))

        for node in nodes:
            item = QListWidgetItem(node["title"])
            item.setData(Qt.UserRole, node)
            self.graph_list.addItem(item)

        if nodes:
            self.graph_list.setCurrentRow(0)

    def _collect_graph_nodes(self, mode: str) -> list[dict[str, Any]]:
        semantic_roles = self.index_data.get("semantic_roles", {})
        entry_files = set(self.index_data.get("entry_files", []))
        nodes = []

        for path, file_record in self.files_by_path.items():
            roles = semantic_roles.get(path, {}).get("roles", [])
            title = path + " | " + file_record.get("module_name", "")

            matched = False
            reasons = []

            text = self._all_text(path)

            if mode == "startup":
                if path in entry_files or "startup" in roles or "main_window" in roles:
                    matched = True
                    reasons.append("startup related")
            elif mode == "tabs":
                if "tabs" in roles or "notebook" in text or "addtab" in text:
                    matched = True
                    reasons.append("tab related")
            elif mode == "topomap":
                if "topomap" in roles or "topomap" in text or "amplitude_map" in text:
                    matched = True
                    reasons.append("topomap related")
            elif mode == "timeline":
                if "timeline" in roles or "timeline" in text:
                    matched = True
                    reasons.append("timeline related")
            elif mode == "splash":
                if "splash" in roles or "splash" in text:
                    matched = True
                    reasons.append("splash related")
            elif mode == "reset":
                if "state_reset" in roles or "reset" in text or "snapshot" in text:
                    matched = True
                    reasons.append("reset or snapshot related")

            if matched:
                best_line = self._best_line_for_graph_mode(file_record, mode)
                nodes.append(
                    {
                        "title": title,
                        "detail": self._build_graph_detail(path, reasons),
                        "path": path,
                        "line": best_line,
                    }
                )

        nodes.sort(key=lambda item: item["path"])
        return nodes[:80]

    def _best_line_for_graph_mode(self, file_record: dict[str, Any], mode: str) -> int:
        keywords_by_mode = {
            "startup": ["QApplication", "app.exec", "create_main_window", "display_pyside6_eeg_visualizer"],
            "tabs": ["addTab", "Notebook", "Tab", "TopInTabBar"],
            "topomap": ["topomap", "amplitude_map", "plot_topomap"],
            "timeline": ["timeline", "TimelineManager", "TimelineWidget"],
            "splash": ["splash", "SplashManager", "KandaSplashImageText"],
            "reset": ["reset", "snapshot", "reset_to_initial_eeg_state", "capture_initial_eeg_state"],
        }

        wanted = [norm_text(x) for x in keywords_by_mode.get(mode, [])]

        for fn in file_record.get("functions", []):
            name_blob = norm_text(fn.get("qualname", "") + " " + fn.get("name", ""))
            for wanted_item in wanted:
                if wanted_item in name_blob:
                    return int(fn.get("lineno", 1))

        for cls in file_record.get("classes", []):
            class_blob = norm_text(cls.get("name", ""))
            for wanted_item in wanted:
                if wanted_item in class_blob:
                    return int(cls.get("lineno", 1))
            for method in cls.get("methods", []):
                method_blob = norm_text(method.get("qualname", "") + " " + method.get("name", ""))
                for wanted_item in wanted:
                    if wanted_item in method_blob:
                        return int(method.get("lineno", 1))

        return 1

    def _all_text(self, path: str) -> str:
        file_record = self.files_by_path[path]
        parts = [
            path,
            file_record.get("module_name", ""),
            file_record.get("docstring", ""),
            " ".join(file_record.get("strings", [])),
            " ".join(file_record.get("comments", [])),
            " ".join(file_record.get("entry_markers", [])),
            " ".join(file_record.get("ui_keyword_hits", [])),
            " ".join(file_record.get("eeg_keyword_hits", [])),
            " ".join(file_record.get("semantic_hints", [])),
        ]

        for fn in file_record.get("functions", []):
            parts.append(fn.get("qualname", ""))
            for call in fn.get("calls", []):
                parts.append(call.get("call_name", ""))

        for cls in file_record.get("classes", []):
            parts.append(cls.get("name", ""))
            for method in cls.get("methods", []):
                parts.append(method.get("qualname", ""))
                for call in method.get("calls", []):
                    parts.append(call.get("call_name", ""))

        return norm_text(" ".join(parts))

    def _build_graph_detail(self, path: str, reasons: list[str]) -> str:
        file_record = self.files_by_path[path]
        semantic_roles = self.index_data.get("semantic_roles", {})
        roles = semantic_roles.get(path, {}).get("roles", [])

        lines = []
        lines.append("NODE")
        lines.append(path)
        lines.append("")
        lines.append("WHY INCLUDED")
        for reason in reasons:
            lines.append("- " + reason)

        lines.append("")
        lines.append("ROLES")
        if roles:
            for role in roles:
                lines.append("- " + role)
        else:
            lines.append("- none")

        lines.append("")
        lines.append("OUTGOING IMPORTS")
        imports_out = sorted(self.import_graph_out.get(path, []))
        if imports_out:
            for item in imports_out[:50]:
                lines.append("- " + item)
        else:
            lines.append("- none")

        lines.append("")
        lines.append("OUTGOING CALLS")
        calls_out = sorted(self.call_graph_out.get(path, []))
        if calls_out:
            for item in calls_out[:80]:
                lines.append("- " + item)
        else:
            lines.append("- none")

        lines.append("")
        lines.append("NEIGHBOR FILE HINTS")
        neighbors = self._infer_neighbor_files(path)
        if neighbors:
            for item in neighbors[:40]:
                lines.append("- " + item)
        else:
            lines.append("- none")

        lines.append("")
        lines.append("FILE SUMMARY")
        lines.append(self._build_file_detail(path, reasons))

        return "\n".join(lines)

    def _infer_neighbor_files(self, path: str) -> list[str]:
        neighbors = set()

        for module_target in self.import_graph_out.get(path, set()):
            resolved = self._resolve_module_to_path(module_target)
            if resolved:
                neighbors.add(resolved)

        for call_name in self.call_graph_out.get(path, set()):
            for file_path, file_record in self.files_by_path.items():
                if self._file_contains_symbol(file_record, call_name):
                    neighbors.add(file_path)

        return sorted(neighbors)

    def _file_contains_symbol(self, file_record: dict[str, Any], symbol_name: str) -> bool:
        for fn in file_record.get("functions", []):
            if fn.get("name") == symbol_name or fn.get("qualname") == symbol_name:
                return True
        for cls in file_record.get("classes", []):
            if cls.get("name") == symbol_name:
                return True
            for method in cls.get("methods", []):
                if method.get("name") == symbol_name or method.get("qualname") == symbol_name:
                    return True
        return False

    def _show_graph_detail(self, current: QListWidgetItem, previous: QListWidgetItem) -> None:
        _ = previous
        if not current:
            self.graph_text.clear()
            return

        payload = current.data(Qt.UserRole)
        if not payload:
            return

        self.graph_text.setPlainText(payload.get("detail", ""))
        self._load_source_preview(payload.get("path", ""), int(payload.get("line", 1)))

    def _absolute_source_path(self, relative_path: str) -> str:
        if not self.project_root:
            return ""
        return os.path.normpath(os.path.join(self.project_root, relative_path))

    def _load_source_preview(self, relative_path: str, line_number: int) -> None:
        abs_path = self._absolute_source_path(relative_path)
        self.source_path_label.setText("Source: " + abs_path if abs_path else "Source: -")

        if not abs_path or not os.path.exists(abs_path):
            self.source_preview.setPlainText("Source file not found:\n" + abs_path)
            return

        try:
            source = safe_read_text(abs_path)
        except Exception as exc:
            self.source_preview.setPlainText("Failed to read source:\n" + str(exc))
            return

        numbered = []
        for idx, line in enumerate(source.splitlines(), start=1):
            numbered.append(str(idx).rjust(5) + " | " + line)

        self.source_preview.setPlainText("\n".join(numbered))
        self._scroll_preview_to_line(line_number)
        self.append_log("Preview loaded: " + relative_path + " @ line " + str(line_number))

    def _scroll_preview_to_line(self, line_number: int) -> None:
        if line_number < 1:
            line_number = 1

        block = self.source_preview.document().findBlockByLineNumber(line_number - 1)
        if not block.isValid():
            return

        cursor = QTextCursor(block)
        self.source_preview.setTextCursor(cursor)
        self.source_preview.centerCursor()

    def refresh_source_preview(self) -> None:
        payload = self._current_payload()
        if not payload:
            QMessageBox.information(self, "No Selection", "Select a result first.")
            return
        self._load_source_preview(payload.get("path", ""), int(payload.get("line", 1)))

    def open_selected_source_file(self) -> None:
        payload = self._current_payload()
        if not payload:
            QMessageBox.information(self, "No Selection", "Select a result first.")
            return

        relative_path = payload.get("path", "")
        line_number = int(payload.get("line", 1))
        abs_path = self._absolute_source_path(relative_path)

        if not abs_path or not os.path.exists(abs_path):
            QMessageBox.warning(self, "File Not Found", "Source file not found:\n" + abs_path)
            return

        self._load_source_preview(relative_path, line_number)

        QMessageBox.information(
            self,
            "Source Opened In Preview",
            "Loaded source preview for:\n"
            + abs_path
            + "\n\nApproximate line: "
            + str(line_number),
        )

    def _current_payload(self) -> dict[str, Any] | None:
        current_tab = self.tabs.currentIndex()

        if current_tab == 0:
            item = self.result_list.currentItem()
        else:
            item = self.graph_list.currentItem()

        if not item:
            return None

        payload = item.data(Qt.UserRole)
        if not isinstance(payload, dict):
            return None

        return payload


def main() -> None:
    app = QApplication(sys.argv)
    window = ProjectJsonExplorerV3()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

What version 3 adds over version 2:
it uses project_summary.project_root to locate the original files
it previews the real source code
it jumps to an approximate line for the selected result
it works for both search results and graph results

What it still does not do:
true OS-level editor integration
exact AST symbol highlighting
full call-chain graph rendering as nodes and edges on canvas

The best next upgrade would be version 4:
a real dependency/call graph canvas with clickable nodes and expandable chains like:
startup chain
tab creation chain
topomap chain
timeline chain

go
Thought for 7s

Here is version 4.

This one adds a real interactive graph canvas using QGraphicsView and QGraphicsScene.
It still loads the JSON from the indexer, but now it can build clickable graph views for:

startup chain
tab creation chain
topomap chain
timeline chain
splash chain
reset/snapshot chain

What it does:
load JSON
search questions
show file details
preview source
draw graph nodes on a canvas
click a node to inspect it
show neighbor expansion based on imports and call hints

This is still heuristic, but much closer to an architecture explorer.

"""
PySide6 Project JSON Explorer v4

Adds:
- interactive graph canvas with QGraphicsView
- clickable nodes
- graph generation for startup/tabs/topomap/timeline/splash/reset
- source preview
- file detail panel

Designed for Windows + standard CPython + PySide6.
"""

from __future__ import annotations

import json
import math
import os
import re
import sys
from collections import defaultdict
from typing import Any

from PySide6.QtCore import QRectF, Qt, Signal
from PySide6.QtGui import QBrush, QColor, QFont, QPainter, QPen, QTextCursor
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGraphicsEllipseItem,
    QGraphicsItem,
    QGraphicsLineItem,
    QGraphicsScene,
    QGraphicsSimpleTextItem,
    QGraphicsView,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QSplitter,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


def norm_text(value: Any) -> str:
    return str(value).strip().lower() if value is not None else ""


def tokenize_query(text: str) -> list[str]:
    tokens = re.findall(r"[a-zA-Z0-9_\.]+", text.lower())
    stop_words = {
        "the",
        "is",
        "are",
        "a",
        "an",
        "of",
        "to",
        "me",
        "show",
        "which",
        "what",
        "where",
        "who",
        "does",
        "do",
        "in",
        "on",
        "for",
        "and",
        "or",
        "with",
        "code",
        "module",
        "file",
        "implementing",
        "implements",
        "created",
        "creates",
        "create",
        "that",
        "this",
        "app",
    }
    return [token for token in tokens if token not in stop_words]


def safe_read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return handle.read()


class GraphNodeItem(QGraphicsEllipseItem):
    """
    Clickable graph node for a file/module.
    """

    def __init__(
        self,
        node_id: str,
        label: str,
        role_text: str,
        rect: QRectF,
        fill_color: QColor,
        border_color: QColor,
    ) -> None:
        super().__init__(rect)
        self.node_id = node_id
        self.label = label
        self.role_text = role_text
        self.setBrush(QBrush(fill_color))
        self.setPen(QPen(border_color, 2))
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setAcceptHoverEvents(True)

        self.text_item = QGraphicsSimpleTextItem(label, self)
        font = QFont("Segoe UI", 9)
        self.text_item.setFont(font)

        text_rect = self.text_item.boundingRect()
        x = rect.center().x() - (text_rect.width() / 2.0)
        y = rect.center().y() - (text_rect.height() / 2.0)
        self.text_item.setPos(x, y)

    def hoverEnterEvent(self, event) -> None:
        self.setPen(QPen(QColor("#ff8800"), 3))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event) -> None:
        self.setPen(QPen(QColor("#333333"), 2))
        super().hoverLeaveEvent(event)


class GraphCanvas(QGraphicsView):
    """
    QGraphicsView-based graph canvas with clickable nodes.
    """

    node_selected = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self._node_items: dict[str, GraphNodeItem] = {}

    def clear_graph(self) -> None:
        self._scene.clear()
        self._node_items.clear()

    def wheelEvent(self, event) -> None:
        if event.modifiers() & Qt.ControlModifier:
            factor = 1.15 if event.angleDelta().y() > 0 else 1.0 / 1.15
            self.scale(factor, factor)
            event.accept()
            return
        super().wheelEvent(event)

    def build_graph(
        self,
        nodes: list[dict[str, Any]],
        edges: list[tuple[str, str]],
    ) -> None:
        self.clear_graph()

        if not nodes:
            return

        radius_x = 260
        radius_y = 190
        center_x = 0
        center_y = 0
        node_width = 180
        node_height = 64

        count = len(nodes)
        positions: dict[str, tuple[float, float]] = {}

        for index, node in enumerate(nodes):
            angle = (2.0 * math.pi * index) / max(count, 1)
            x = center_x + radius_x * math.cos(angle)
            y = center_y + radius_y * math.sin(angle)
            positions[node["id"]] = (x, y)

        for source_id, target_id in edges:
            if source_id not in positions or target_id not in positions:
                continue
            x1, y1 = positions[source_id]
            x2, y2 = positions[target_id]
            line = QGraphicsLineItem(x1, y1, x2, y2)
            line.setPen(QPen(QColor("#888888"), 1.5))
            self._scene.addItem(line)

        for node in nodes:
            node_id = node["id"]
            x, y = positions[node_id]

            role_text = ", ".join(node.get("roles", []))
            fill_color = role_to_color(node.get("roles", []))

            item = GraphNodeItem(
                node_id=node_id,
                label=node["label"],
                role_text=role_text,
                rect=QRectF(x - node_width / 2.0, y - node_height / 2.0, node_width, node_height),
                fill_color=fill_color,
                border_color=QColor("#333333"),
            )
            self._scene.addItem(item)
            self._node_items[node_id] = item

        scene_rect = self._scene.itemsBoundingRect().adjusted(-100, -100, 100, 100)
        self.setSceneRect(scene_rect)
        self.fitInView(scene_rect, Qt.KeepAspectRatio)

    def mousePressEvent(self, event) -> None:
        item = self.itemAt(event.pos())
        if isinstance(item, QGraphicsSimpleTextItem):
            parent_item = item.parentItem()
            if isinstance(parent_item, GraphNodeItem):
                self.node_selected.emit(parent_item.node_id)
        elif isinstance(item, GraphNodeItem):
            self.node_selected.emit(item.node_id)

        super().mousePressEvent(event)


def role_to_color(roles: list[str]) -> QColor:
    if "startup" in roles:
        return QColor("#d6ecff")
    if "tabs" in roles:
        return QColor("#e9ddff")
    if "topomap" in roles:
        return QColor("#d8ffd8")
    if "timeline" in roles:
        return QColor("#fff0c9")
    if "splash" in roles:
        return QColor("#ffdce5")
    if "state_reset" in roles:
        return QColor("#ffe0c7")
    if "main_window" in roles:
        return QColor("#d9f5f0")
    return QColor("#f0f0f0")


class ProjectJsonExplorerV4(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Project JSON Explorer v4")
        self.resize(1780, 1020)

        self.index_data: dict[str, Any] | None = None
        self.project_root: str = ""
        self.files_by_path: dict[str, dict[str, Any]] = {}
        self.files_by_module: dict[str, dict[str, Any]] = {}
        self.call_graph_out: dict[str, set[str]] = defaultdict(set)
        self.import_graph_out: dict[str, set[str]] = defaultdict(set)
        self.semantic_roles: dict[str, dict[str, Any]] = {}

        self.json_path_edit = QLineEdit()
        self.question_edit = QLineEdit()

        self.load_button = QPushButton("Load JSON")
        self.ask_button = QPushButton("Ask")
        self.clear_button = QPushButton("Clear")
        self.open_source_button = QPushButton("Open Source File")
        self.refresh_source_button = QPushButton("Refresh Source Preview")
        self.expand_neighbors_button = QPushButton("Expand Neighbors")

        self.quick_startup_button = QPushButton("Startup")
        self.quick_tabs_button = QPushButton("Tabs")
        self.quick_topomap_button = QPushButton("Topomap")
        self.quick_timeline_button = QPushButton("Timeline")
        self.quick_splash_button = QPushButton("Splash")
        self.quick_reset_button = QPushButton("Reset")

        self.result_list = QListWidget()
        self.detail_text = QPlainTextEdit()
        self.detail_text.setReadOnly(True)

        self.graph_list = QListWidget()
        self.graph_text = QPlainTextEdit()
        self.graph_text.setReadOnly(True)

        self.source_preview = QPlainTextEdit()
        self.source_preview.setReadOnly(True)
        self.source_path_label = QLabel("Source: -")

        self.graph_canvas = GraphCanvas()
        self.graph_canvas.node_selected.connect(self._graph_node_selected)

        self.log_box = QPlainTextEdit()
        self.log_box.setReadOnly(True)

        self.tabs = QTabWidget()

        self._current_graph_mode = ""
        self._current_graph_nodes: list[dict[str, Any]] = []
        self._current_graph_edges: list[tuple[str, str]] = []

        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

        load_row = QHBoxLayout()
        load_row.addWidget(QLabel("JSON:"))
        load_row.addWidget(self.json_path_edit)
        load_row.addWidget(self.load_button)

        query_row = QHBoxLayout()
        query_row.addWidget(QLabel("Question:"))
        query_row.addWidget(self.question_edit)
        query_row.addWidget(self.ask_button)
        query_row.addWidget(self.clear_button)

        quick_row = QHBoxLayout()
        quick_row.addWidget(self.quick_startup_button)
        quick_row.addWidget(self.quick_tabs_button)
        quick_row.addWidget(self.quick_topomap_button)
        quick_row.addWidget(self.quick_timeline_button)
        quick_row.addWidget(self.quick_splash_button)
        quick_row.addWidget(self.quick_reset_button)
        quick_row.addStretch()
        quick_row.addWidget(self.expand_neighbors_button)
        quick_row.addWidget(self.refresh_source_button)
        quick_row.addWidget(self.open_source_button)

        search_page = QWidget()
        search_layout = QVBoxLayout(search_page)
        search_splitter = QSplitter(Qt.Horizontal)
        search_splitter.addWidget(self.result_list)
        search_splitter.addWidget(self.detail_text)
        search_splitter.addWidget(self.source_preview)
        search_splitter.setSizes([380, 560, 840])
        search_layout.addWidget(self.source_path_label)
        search_layout.addWidget(search_splitter)

        graph_page = QWidget()
        graph_layout = QVBoxLayout(graph_page)

        graph_upper_splitter = QSplitter(Qt.Horizontal)
        graph_upper_splitter.addWidget(self.graph_list)
        graph_upper_splitter.addWidget(self.graph_canvas)
        graph_upper_splitter.setSizes([360, 980])

        graph_lower_splitter = QSplitter(Qt.Horizontal)
        graph_lower_splitter.addWidget(self.graph_text)
        graph_lower_splitter.addWidget(self.source_preview)
        graph_lower_splitter.setSizes([560, 840])

        graph_layout.addWidget(self.source_path_label)
        graph_layout.addWidget(graph_upper_splitter, stretch=2)
        graph_layout.addWidget(graph_lower_splitter, stretch=1)

        self.tabs.addTab(search_page, "Search")
        self.tabs.addTab(graph_page, "Graph Views")

        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout(log_group)
        log_layout.addWidget(self.log_box)

        main_layout.addLayout(load_row)
        main_layout.addLayout(query_row)
        main_layout.addLayout(quick_row)
        main_layout.addWidget(self.tabs, stretch=1)
        main_layout.addWidget(log_group, stretch=0)

    def _connect_signals(self) -> None:
        self.load_button.clicked.connect(self.load_json)
        self.ask_button.clicked.connect(self.ask_question)
        self.clear_button.clicked.connect(self.clear_all)
        self.question_edit.returnPressed.connect(self.ask_question)

        self.quick_startup_button.clicked.connect(lambda: self.run_graph_view("startup"))
        self.quick_tabs_button.clicked.connect(lambda: self.run_graph_view("tabs"))
        self.quick_topomap_button.clicked.connect(lambda: self.run_graph_view("topomap"))
        self.quick_timeline_button.clicked.connect(lambda: self.run_graph_view("timeline"))
        self.quick_splash_button.clicked.connect(lambda: self.run_graph_view("splash"))
        self.quick_reset_button.clicked.connect(lambda: self.run_graph_view("reset"))

        self.result_list.currentItemChanged.connect(self._show_result_detail)
        self.graph_list.currentItemChanged.connect(self._show_graph_detail)

        self.refresh_source_button.clicked.connect(self.refresh_source_preview)
        self.open_source_button.clicked.connect(self.open_selected_source_file)
        self.expand_neighbors_button.clicked.connect(self.expand_current_graph_neighbors)

    def append_log(self, text: str) -> None:
        self.log_box.appendPlainText(text)

    def clear_all(self) -> None:
        self.result_list.clear()
        self.graph_list.clear()
        self.detail_text.clear()
        self.graph_text.clear()
        self.source_preview.clear()
        self.graph_canvas.clear_graph()
        self.source_path_label.setText("Source: -")
        self.log_box.clear()
        self._current_graph_mode = ""
        self._current_graph_nodes = []
        self._current_graph_edges = []

    def load_json(self) -> None:
        current = self.json_path_edit.text().strip()
        start_dir = os.path.dirname(current) if current else os.getcwd()

        file_path, _filter = QFileDialog.getOpenFileName(
            self,
            "Load project_structure_index.json",
            start_dir,
            "JSON Files (*.json)",
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as handle:
                self.index_data = json.load(handle)

            self.json_path_edit.setText(file_path)
            self.project_root = (
                self.index_data.get("project_summary", {}).get("project_root", "") or ""
            )
            self.semantic_roles = self.index_data.get("semantic_roles", {})
            self._rebuild_indexes()

            self.append_log("Loaded JSON: " + file_path)
            self.append_log("Project root: " + self.project_root)

            summary = self.index_data.get("project_summary", {})
            self.append_log("Python files: " + str(summary.get("python_file_count", "unknown")))
            self.append_log("Entry files: " + str(summary.get("entry_file_count", "unknown")))

            QMessageBox.information(self, "Loaded", "JSON loaded successfully.")
        except Exception as exc:
            QMessageBox.critical(self, "Error", "Failed to load JSON:\n" + str(exc))
            self.append_log("ERROR loading JSON: " + str(exc))

    def _rebuild_indexes(self) -> None:
        self.files_by_path.clear()
        self.files_by_module.clear()
        self.call_graph_out.clear()
        self.import_graph_out.clear()

        if not self.index_data:
            return

        for file_record in self.index_data.get("files", []):
            path = file_record.get("path", "")
            module_name = file_record.get("module_name", "")
            if path:
                self.files_by_path[path] = file_record
            if module_name:
                self.files_by_module[module_name] = file_record

        for src_module, targets in self.index_data.get("import_graph", {}).items():
            src_path = self._resolve_module_to_path(src_module) or src_module
            for target in targets:
                self.import_graph_out[src_path].add(target)

        for edge in self.index_data.get("call_edges", []):
            from_file = edge.get("from_file", "")
            to_call = edge.get("to_call", "")
            if from_file and to_call:
                self.call_graph_out[from_file].add(to_call)

    def _resolve_module_to_path(self, module_name: str) -> str | None:
        record = self.files_by_module.get(module_name)
        if record:
            return record.get("path")
        return None

    def ask_question(self) -> None:
        if not self.index_data:
            QMessageBox.warning(self, "No JSON", "Please load a JSON file first.")
            return

        question = self.question_edit.text().strip()
        if not question:
            QMessageBox.warning(self, "No Question", "Please type a question.")
            return

        self.result_list.clear()
        self.detail_text.clear()
        self.tabs.setCurrentIndex(0)

        results = self._search(question)

        self.append_log("Question: " + question)
        self.append_log("Search results: " + str(len(results)))

        for result in results:
            item = QListWidgetItem(result["title"])
            item.setData(Qt.UserRole, result)
            self.result_list.addItem(item)

        if results:
            self.result_list.setCurrentRow(0)

    def _search(self, question: str) -> list[dict[str, Any]]:
        q = norm_text(question)
        tokens = tokenize_query(q)
        entry_files = set(self.index_data.get("entry_files", []))

        scored: list[dict[str, Any]] = []

        for path, file_record in self.files_by_path.items():
            module_name = file_record.get("module_name", "")
            docstring = file_record.get("docstring", "")
            strings = " ".join(file_record.get("strings", []))
            comments = " ".join(file_record.get("comments", []))
            ui_hits = " ".join(file_record.get("ui_keyword_hits", []))
            eeg_hits = " ".join(file_record.get("eeg_keyword_hits", []))
            semantic_hints = " ".join(file_record.get("semantic_hints", []))
            entry_markers = " ".join(file_record.get("entry_markers", []))

            function_names = []
            call_names = []
            class_names = []

            for fn in file_record.get("functions", []):
                function_names.append(fn.get("name", ""))
                function_names.append(fn.get("qualname", ""))
                for call in fn.get("calls", []):
                    call_names.append(call.get("call_name", ""))

            for cls in file_record.get("classes", []):
                class_names.append(cls.get("name", ""))
                for method in cls.get("methods", []):
                    function_names.append(method.get("name", ""))
                    function_names.append(method.get("qualname", ""))
                    for call in method.get("calls", []):
                        call_names.append(call.get("call_name", ""))

            haystack = " ".join([
                norm_text(path),
                norm_text(module_name),
                norm_text(docstring),
                norm_text(strings),
                norm_text(comments),
                norm_text(ui_hits),
                norm_text(eeg_hits),
                norm_text(semantic_hints),
                norm_text(entry_markers),
                norm_text(" ".join(function_names)),
                norm_text(" ".join(call_names)),
                norm_text(" ".join(class_names)),
            ])

            roles = self.semantic_roles.get(path, {}).get("roles", [])
            score = 0
            reasons = []

            for token in tokens:
                if token in haystack:
                    score += 3
                    reasons.append("token match: " + token)

            if path in entry_files and ("start" in q or "main" in q or "entry" in q or "launch" in q):
                score += 20
                reasons.append("entry file")

            if "topomap" in q and ("topomap" in haystack or "amplitude_map" in haystack or "topomap" in roles):
                score += 18
                reasons.append("topomap match")

            if "tab" in q and ("addtab" in haystack or "notebook" in haystack or "tabs" in roles):
                score += 15
                reasons.append("tab match")

            if "timeline" in q and ("timeline" in haystack or "timeline" in roles):
                score += 15
                reasons.append("timeline match")

            if "splash" in q and ("splash" in haystack or "splash" in roles):
                score += 15
                reasons.append("splash match")

            if ("reset" in q or "snapshot" in q) and (
                "reset" in haystack or "snapshot" in haystack or "state_reset" in roles
            ):
                score += 15
                reasons.append("reset or snapshot match")

            if score > 0:
                best_line = self._best_line_for_file(file_record, q)
                scored.append(
                    {
                        "score": score,
                        "title": "[" + str(score) + "] " + path + " | " + module_name,
                        "detail": self._build_file_detail(path, reasons),
                        "path": path,
                        "line": best_line,
                    }
                )

        scored.sort(key=lambda item: (-item["score"], item["path"]))
        return scored[:50]

    def _best_line_for_file(self, file_record: dict[str, Any], question: str) -> int:
        q = norm_text(question)

        for fn in file_record.get("functions", []):
            if norm_text(fn.get("qualname", "")) in q or norm_text(fn.get("name", "")) in q:
                return int(fn.get("lineno", 1))

        for cls in file_record.get("classes", []):
            if norm_text(cls.get("name", "")) in q:
                return int(cls.get("lineno", 1))
            for method in cls.get("methods", []):
                if norm_text(method.get("qualname", "")) in q or norm_text(method.get("name", "")) in q:
                    return int(method.get("lineno", 1))

        if file_record.get("functions"):
            return int(file_record["functions"][0].get("lineno", 1))
        if file_record.get("classes"):
            return int(file_record["classes"][0].get("lineno", 1))
        return 1

    def _build_file_detail(self, path: str, reasons: list[str]) -> str:
        file_record = self.files_by_path[path]
        roles = self.semantic_roles.get(path, {}).get("roles", [])

        lines = []
        lines.append("FILE")
        lines.append(path)
        lines.append("")
        lines.append("MODULE")
        lines.append(file_record.get("module_name", ""))
        lines.append("")
        lines.append("WHY THIS MATCHED")
        for reason in sorted(set(reasons)):
            lines.append("- " + reason)

        lines.append("")
        lines.append("ROLES")
        if roles:
            for role in roles:
                lines.append("- " + role)
        else:
            lines.append("- none")

        if file_record.get("entry_markers"):
            lines.append("")
            lines.append("ENTRY MARKERS")
            for marker in file_record["entry_markers"]:
                lines.append("- " + marker)

        if file_record.get("docstring"):
            lines.append("")
            lines.append("DOCSTRING")
            lines.append(file_record["docstring"])

        if file_record.get("functions"):
            lines.append("")
            lines.append("FUNCTIONS")
            for fn in file_record["functions"][:40]:
                lines.append("- " + fn.get("qualname", "") + " (line " + str(fn.get("lineno", "")) + ")")

        if file_record.get("classes"):
            lines.append("")
            lines.append("CLASSES")
            for cls in file_record["classes"][:30]:
                line = "- " + cls.get("name", "") + " (line " + str(cls.get("lineno", "")) + ")"
                bases = cls.get("bases", [])
                if bases:
                    line += " bases: " + ", ".join(bases)
                lines.append(line)
                for method in cls.get("methods", [])[:15]:
                    lines.append("    * " + method.get("qualname", "") + " (line " + str(method.get("lineno", "")) + ")")

        imports_out = sorted(self.import_graph_out.get(path, []))
        if imports_out:
            lines.append("")
            lines.append("IMPORTS OUT")
            for item in imports_out[:50]:
                lines.append("- " + item)

        calls_out = sorted(self.call_graph_out.get(path, []))
        if calls_out:
            lines.append("")
            lines.append("CALLS OUT")
            for item in calls_out[:80]:
                lines.append("- " + item)

        return "\n".join(lines)

    def _show_result_detail(self, current: QListWidgetItem, previous: QListWidgetItem) -> None:
        _ = previous
        if not current:
            self.detail_text.clear()
            return

        payload = current.data(Qt.UserRole)
        if not payload:
            return

        self.detail_text.setPlainText(payload.get("detail", ""))
        self._load_source_preview(payload.get("path", ""), int(payload.get("line", 1)))

    def run_graph_view(self, mode: str) -> None:
        if not self.index_data:
            QMessageBox.warning(self, "No JSON", "Please load a JSON file first.")
            return

        self.graph_list.clear()
        self.graph_text.clear()
        self.graph_canvas.clear_graph()
        self.tabs.setCurrentIndex(1)
        self._current_graph_mode = mode

        nodes, edges = self._collect_graph_nodes_and_edges(mode)
        self._current_graph_nodes = nodes
        self._current_graph_edges = edges

        self.append_log("Graph view: " + mode)
        self.append_log("Graph nodes: " + str(len(nodes)))
        self.append_log("Graph edges: " + str(len(edges)))

        for node in nodes:
            item = QListWidgetItem(node["title"])
            item.setData(Qt.UserRole, node)
            self.graph_list.addItem(item)

        self.graph_canvas.build_graph(nodes, edges)

        if nodes:
            self.graph_list.setCurrentRow(0)

    def _collect_graph_nodes_and_edges(self, mode: str) -> tuple[list[dict[str, Any]], list[tuple[str, str]]]:
        entry_files = set(self.index_data.get("entry_files", []))
        nodes = []
        edges: list[tuple[str, str]] = []

        selected_paths = []

        for path, file_record in self.files_by_path.items():
            roles = self.semantic_roles.get(path, {}).get("roles", [])
            title = path + " | " + file_record.get("module_name", "")
            text = self._all_text(path)

            matched = False
            reasons = []

            if mode == "startup":
                if path in entry_files or "startup" in roles or "main_window" in roles:
                    matched = True
                    reasons.append("startup related")
            elif mode == "tabs":
                if "tabs" in roles or "notebook" in text or "addtab" in text:
                    matched = True
                    reasons.append("tab related")
            elif mode == "topomap":
                if "topomap" in roles or "topomap" in text or "amplitude_map" in text:
                    matched = True
                    reasons.append("topomap related")
            elif mode == "timeline":
                if "timeline" in roles or "timeline" in text:
                    matched = True
                    reasons.append("timeline related")
            elif mode == "splash":
                if "splash" in roles or "splash" in text:
                    matched = True
                    reasons.append("splash related")
            elif mode == "reset":
                if "state_reset" in roles or "reset" in text or "snapshot" in text:
                    matched = True
                    reasons.append("reset or snapshot related")

            if matched:
                best_line = self._best_line_for_graph_mode(file_record, mode)
                selected_paths.append(path)
                nodes.append(
                    {
                        "id": path,
                        "title": title,
                        "label": shorten_path(path),
                        "detail": self._build_graph_detail(path, reasons),
                        "path": path,
                        "line": best_line,
                        "roles": roles,
                    }
                )

        selected_path_set = set(selected_paths)

        for path in selected_paths:
            for imported in self.import_graph_out.get(path, set()):
                resolved = self._resolve_module_to_path(imported)
                if resolved and resolved in selected_path_set:
                    edges.append((path, resolved))

            for call_name in self.call_graph_out.get(path, set()):
                for candidate_path, candidate_record in self.files_by_path.items():
                    if candidate_path == path:
                        continue
                    if candidate_path not in selected_path_set:
                        continue
                    if self._file_contains_symbol(candidate_record, call_name):
                        edges.append((path, candidate_path))

        edges = sorted(set(edges))
        nodes.sort(key=lambda item: item["path"])
        return nodes[:90], edges[:240]

    def _best_line_for_graph_mode(self, file_record: dict[str, Any], mode: str) -> int:
        keywords_by_mode = {
            "startup": ["QApplication", "app.exec", "create_main_window", "display_pyside6_eeg_visualizer"],
            "tabs": ["addTab", "Notebook", "Tab", "TopInTabBar"],
            "topomap": ["topomap", "amplitude_map", "plot_topomap"],
            "timeline": ["timeline", "TimelineManager", "TimelineWidget"],
            "splash": ["splash", "SplashManager", "KandaSplashImageText"],
            "reset": ["reset", "snapshot", "reset_to_initial_eeg_state", "capture_initial_eeg_state"],
        }

        wanted = [norm_text(x) for x in keywords_by_mode.get(mode, [])]

        for fn in file_record.get("functions", []):
            blob = norm_text(fn.get("qualname", "") + " " + fn.get("name", ""))
            for item in wanted:
                if item in blob:
                    return int(fn.get("lineno", 1))

        for cls in file_record.get("classes", []):
            blob = norm_text(cls.get("name", ""))
            for item in wanted:
                if item in blob:
                    return int(cls.get("lineno", 1))
            for method in cls.get("methods", []):
                blob2 = norm_text(method.get("qualname", "") + " " + method.get("name", ""))
                for item in wanted:
                    if item in blob2:
                        return int(method.get("lineno", 1))

        return 1

    def _all_text(self, path: str) -> str:
        file_record = self.files_by_path[path]
        parts = [
            path,
            file_record.get("module_name", ""),
            file_record.get("docstring", ""),
            " ".join(file_record.get("strings", [])),
            " ".join(file_record.get("comments", [])),
            " ".join(file_record.get("entry_markers", [])),
            " ".join(file_record.get("ui_keyword_hits", [])),
            " ".join(file_record.get("eeg_keyword_hits", [])),
            " ".join(file_record.get("semantic_hints", [])),
        ]

        for fn in file_record.get("functions", []):
            parts.append(fn.get("qualname", ""))
            for call in fn.get("calls", []):
                parts.append(call.get("call_name", ""))

        for cls in file_record.get("classes", []):
            parts.append(cls.get("name", ""))
            for method in cls.get("methods", []):
                parts.append(method.get("qualname", ""))
                for call in method.get("calls", []):
                    parts.append(call.get("call_name", ""))

        return norm_text(" ".join(parts))

    def _build_graph_detail(self, path: str, reasons: list[str]) -> str:
        file_record = self.files_by_path[path]
        roles = self.semantic_roles.get(path, {}).get("roles", [])

        lines = []
        lines.append("NODE")
        lines.append(path)
        lines.append("")
        lines.append("WHY INCLUDED")
        for reason in reasons:
            lines.append("- " + reason)

        lines.append("")
        lines.append("ROLES")
        if roles:
            for role in roles:
                lines.append("- " + role)
        else:
            lines.append("- none")

        lines.append("")
        lines.append("OUTGOING IMPORTS")
        imports_out = sorted(self.import_graph_out.get(path, []))
        if imports_out:
            for item in imports_out[:50]:
                lines.append("- " + item)
        else:
            lines.append("- none")

        lines.append("")
        lines.append("OUTGOING CALLS")
        calls_out = sorted(self.call_graph_out.get(path, []))
        if calls_out:
            for item in calls_out[:80]:
                lines.append("- " + item)
        else:
            lines.append("- none")

        lines.append("")
        lines.append("NEIGHBOR FILE HINTS")
        neighbors = self._infer_neighbor_files(path)
        if neighbors:
            for item in neighbors[:40]:
                lines.append("- " + item)
        else:
            lines.append("- none")

        lines.append("")
        lines.append("FILE SUMMARY")
        lines.append(self._build_file_detail(path, reasons))

        return "\n".join(lines)

    def _infer_neighbor_files(self, path: str) -> list[str]:
        neighbors = set()

        for module_target in self.import_graph_out.get(path, set()):
            resolved = self._resolve_module_to_path(module_target)
            if resolved:
                neighbors.add(resolved)

        for call_name in self.call_graph_out.get(path, set()):
            for file_path, file_record in self.files_by_path.items():
                if self._file_contains_symbol(file_record, call_name):
                    neighbors.add(file_path)

        return sorted(neighbors)

    def _file_contains_symbol(self, file_record: dict[str, Any], symbol_name: str) -> bool:
        for fn in file_record.get("functions", []):
            if fn.get("name") == symbol_name or fn.get("qualname") == symbol_name:
                return True
        for cls in file_record.get("classes", []):
            if cls.get("name") == symbol_name:
                return True
            for method in cls.get("methods", []):
                if method.get("name") == symbol_name or method.get("qualname") == symbol_name:
                    return True
        return False

    def _show_graph_detail(self, current: QListWidgetItem, previous: QListWidgetItem) -> None:
        _ = previous
        if not current:
            self.graph_text.clear()
            return

        payload = current.data(Qt.UserRole)
        if not payload:
            return

        self.graph_text.setPlainText(payload.get("detail", ""))
        self._load_source_preview(payload.get("path", ""), int(payload.get("line", 1)))

    def _graph_node_selected(self, node_id: str) -> None:
        for row in range(self.graph_list.count()):
            item = self.graph_list.item(row)
            payload = item.data(Qt.UserRole)
            if payload and payload.get("path") == node_id:
                self.graph_list.setCurrentRow(row)
                self.graph_text.setPlainText(payload.get("detail", ""))
                self._load_source_preview(payload.get("path", ""), int(payload.get("line", 1)))
                break

    def expand_current_graph_neighbors(self) -> None:
        if not self._current_graph_nodes:
            QMessageBox.information(self, "No Graph", "Build a graph view first.")
            return

        current_item = self.graph_list.currentItem()
        if not current_item:
            QMessageBox.information(self, "No Selection", "Select a graph node first.")
            return

        payload = current_item.data(Qt.UserRole)
        if not payload:
            return

        base_path = payload.get("path", "")
        if not base_path:
            return

        neighbor_paths = self._infer_neighbor_files(base_path)
        existing = {node["id"] for node in self._current_graph_nodes}
        new_nodes = list(self._current_graph_nodes)
        new_edges = list(self._current_graph_edges)

        for neighbor_path in neighbor_paths[:20]:
            if neighbor_path not in self.files_by_path:
                continue
            if neighbor_path not in existing:
                roles = self.semantic_roles.get(neighbor_path, {}).get("roles", [])
                rec = self.files_by_path[neighbor_path]
                new_nodes.append(
                    {
                        "id": neighbor_path,
                        "title": neighbor_path + " | " + rec.get("module_name", ""),
                        "label": shorten_path(neighbor_path),
                        "detail": self._build_graph_detail(neighbor_path, ["expanded neighbor"]),
                        "path": neighbor_path,
                        "line": 1,
                        "roles": roles,
                    }
                )
                existing.add(neighbor_path)

            new_edges.append((base_path, neighbor_path))

        self._current_graph_nodes = new_nodes
        self._current_graph_edges = sorted(set(new_edges))

        self.graph_canvas.build_graph(self._current_graph_nodes, self._current_graph_edges)

        self.graph_list.clear()
        for node in self._current_graph_nodes:
            item = QListWidgetItem(node["title"])
            item.setData(Qt.UserRole, node)
            self.graph_list.addItem(item)

        self.append_log("Expanded neighbors for: " + base_path)

    def _absolute_source_path(self, relative_path: str) -> str:
        if not self.project_root:
            return ""
        return os.path.normpath(os.path.join(self.project_root, relative_path))

    def _load_source_preview(self, relative_path: str, line_number: int) -> None:
        abs_path = self._absolute_source_path(relative_path)
        self.source_path_label.setText("Source: " + abs_path if abs_path else "Source: -")

        if not abs_path or not os.path.exists(abs_path):
            self.source_preview.setPlainText("Source file not found:\n" + abs_path)
            return

        try:
            source = safe_read_text(abs_path)
        except Exception as exc:
            self.source_preview.setPlainText("Failed to read source:\n" + str(exc))
            return

        numbered = []
        for idx, line in enumerate(source.splitlines(), start=1):
            numbered.append(str(idx).rjust(5) + " | " + line)

        self.source_preview.setPlainText("\n".join(numbered))
        self._scroll_preview_to_line(line_number)
        self.append_log("Preview loaded: " + relative_path + " @ line " + str(line_number))

    def _scroll_preview_to_line(self, line_number: int) -> None:
        if line_number < 1:
            line_number = 1

        block = self.source_preview.document().findBlockByLineNumber(line_number - 1)
        if not block.isValid():
            return

        cursor = QTextCursor(block)
        self.source_preview.setTextCursor(cursor)
        self.source_preview.centerCursor()

    def refresh_source_preview(self) -> None:
        payload = self._current_payload()
        if not payload:
            QMessageBox.information(self, "No Selection", "Select a result first.")
            return
        self._load_source_preview(payload.get("path", ""), int(payload.get("line", 1)))

    def open_selected_source_file(self) -> None:
        payload = self._current_payload()
        if not payload:
            QMessageBox.information(self, "No Selection", "Select a result first.")
            return

        relative_path = payload.get("path", "")
        line_number = int(payload.get("line", 1))
        abs_path = self._absolute_source_path(relative_path)

        if not abs_path or not os.path.exists(abs_path):
            QMessageBox.warning(self, "File Not Found", "Source file not found:\n" + abs_path)
            return

        self._load_source_preview(relative_path, line_number)

        QMessageBox.information(
            self,
            "Source Opened In Preview",
            "Loaded source preview for:\n"
            + abs_path
            + "\n\nApproximate line: "
            + str(line_number),
        )

    def _current_payload(self) -> dict[str, Any] | None:
        current_tab = self.tabs.currentIndex()

        if current_tab == 0:
            item = self.result_list.currentItem()
        else:
            item = self.graph_list.currentItem()

        if not item:
            return None

        payload = item.data(Qt.UserRole)
        if not isinstance(payload, dict):
            return None

        return payload


def shorten_path(path: str, max_len: int = 26) -> str:
    if len(path) <= max_len:
        return path
    parts = path.replace("\\", "/").split("/")
    if len(parts) >= 2:
        short = parts[-2] + "/" + parts[-1]
        if len(short) <= max_len:
            return short
    return "..." + path[-(max_len - 3):]


def main() -> None:
    app = QApplication(sys.argv)
    window = ProjectJsonExplorerV4()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

What version 4 adds over version 3:
real graph canvas
clickable nodes
node layout
expand neighbors
list + graph synchronized
better architecture navigation for startup, tabs, topomap, timeline, splash, reset

What version 5 could add:
true left-to-right dependency layout instead of circular layout
separate import edges and call edges with different colors
symbol-level graph, not only file-level graph
search inside source preview
export graph as PNG
double-click result to isolate a local subgraph

If you want, next I will build version 5 with:
edge coloring
legend
PNG export
search inside source
double-click isolate-subgraph mode.

go
Thought for a few seconds

Here is version 5.

It adds:
edge coloring for imports vs calls
legend
PNG export
search inside source preview
double-click isolate-subgraph mode
clear isolation / rebuild graph
better left-to-right layered layout instead of circular layout

from __future__ import annotations

import json
import os
import re
import sys
from collections import defaultdict, deque
from typing import Any

from PySide6.QtCore import QRectF, Qt, Signal
from PySide6.QtGui import QBrush, QColor, QFont, QImage, QPainter, QPen, QTextCursor
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGraphicsEllipseItem,
    QGraphicsItem,
    QGraphicsLineItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsSimpleTextItem,
    QGraphicsView,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QSplitter,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


IMPORT_EDGE_COLOR = QColor("#4C78A8")
CALL_EDGE_COLOR = QColor("#E45756")
DEFAULT_BORDER_COLOR = QColor("#333333")
HOVER_BORDER_COLOR = QColor("#FF8800")


def norm_text(value: Any) -> str:
    return str(value).strip().lower() if value is not None else ""


def tokenize_query(text: str) -> list[str]:
    tokens = re.findall(r"[a-zA-Z0-9_\.]+", text.lower())
    stop_words = {
        "the",
        "is",
        "are",
        "a",
        "an",
        "of",
        "to",
        "me",
        "show",
        "which",
        "what",
        "where",
        "who",
        "does",
        "do",
        "in",
        "on",
        "for",
        "and",
        "or",
        "with",
        "code",
        "module",
        "file",
        "implementing",
        "implements",
        "created",
        "creates",
        "create",
        "that",
        "this",
        "app",
    }
    return [token for token in tokens if token not in stop_words]


def safe_read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return handle.read()


def shorten_path(path: str, max_len: int = 28) -> str:
    if len(path) <= max_len:
        return path
    parts = path.replace("\\", "/").split("/")
    if len(parts) >= 2:
        short = parts[-2] + "/" + parts[-1]
        if len(short) <= max_len:
            return short
    return "..." + path[-(max_len - 3):]


def role_to_color(roles: list[str]) -> QColor:
    if "startup" in roles:
        return QColor("#D6ECFF")
    if "tabs" in roles:
        return QColor("#E9DDFF")
    if "topomap" in roles:
        return QColor("#D8FFD8")
    if "timeline" in roles:
        return QColor("#FFF0C9")
    if "splash" in roles:
        return QColor("#FFDCE5")
    if "state_reset" in roles:
        return QColor("#FFE0C7")
    if "main_window" in roles:
        return QColor("#D9F5F0")
    return QColor("#F0F0F0")


class GraphNodeItem(QGraphicsEllipseItem):
    node_clicked = Signal(str)
    node_double_clicked = Signal(str)

    def __init__(
        self,
        node_id: str,
        label: str,
        role_text: str,
        rect: QRectF,
        fill_color: QColor,
        border_color: QColor,
    ) -> None:
        super().__init__(rect)
        self.node_id = node_id
        self.label = label
        self.role_text = role_text
        self.setBrush(QBrush(fill_color))
        self.setPen(QPen(border_color, 2))
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setAcceptHoverEvents(True)

        self.text_item = QGraphicsSimpleTextItem(label, self)
        font = QFont("Segoe UI", 9)
        self.text_item.setFont(font)

        text_rect = self.text_item.boundingRect()
        x_pos = rect.center().x() - (text_rect.width() / 2.0)
        y_pos = rect.center().y() - (text_rect.height() / 2.0)
        self.text_item.setPos(x_pos, y_pos)

    def hoverEnterEvent(self, event) -> None:
        self.setPen(QPen(HOVER_BORDER_COLOR, 3))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event) -> None:
        self.setPen(QPen(DEFAULT_BORDER_COLOR, 2))
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event) -> None:
        self.node_clicked.emit(self.node_id)
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event) -> None:
        self.node_double_clicked.emit(self.node_id)
        super().mouseDoubleClickEvent(event)


class GraphCanvas(QGraphicsView):
    node_selected = Signal(str)
    node_double_selected = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self._node_items: dict[str, GraphNodeItem] = {}
        self._legend_items: list[QGraphicsItem] = []

    def clear_graph(self) -> None:
        self._scene.clear()
        self._node_items.clear()
        self._legend_items.clear()

    def wheelEvent(self, event) -> None:
        if event.modifiers() & Qt.ControlModifier:
            factor = 1.15 if event.angleDelta().y() > 0 else (1.0 / 1.15)
            self.scale(factor, factor)
            event.accept()
            return
        super().wheelEvent(event)

    def build_graph(
        self,
        nodes: list[dict[str, Any]],
        edges: list[dict[str, Any]],
    ) -> None:
        self.clear_graph()

        if not nodes:
            return

        positions = compute_layered_positions(nodes, edges)

        for edge in edges:
            source_id = edge["source"]
            target_id = edge["target"]
            edge_type = edge["type"]

            if source_id not in positions or target_id not in positions:
                continue

            x1, y1 = positions[source_id]
            x2, y2 = positions[target_id]

            line = QGraphicsLineItem(x1, y1, x2, y2)
            if edge_type == "import":
                line.setPen(QPen(IMPORT_EDGE_COLOR, 2))
            else:
                line.setPen(QPen(CALL_EDGE_COLOR, 2))
            self._scene.addItem(line)

        node_width = 190.0
        node_height = 70.0

        for node in nodes:
            node_id = node["id"]
            x_pos, y_pos = positions[node_id]
            roles = node.get("roles", [])
            fill_color = role_to_color(roles)

            item = GraphNodeItem(
                node_id=node_id,
                label=node["label"],
                role_text=", ".join(roles),
                rect=QRectF(
                    x_pos - node_width / 2.0,
                    y_pos - node_height / 2.0,
                    node_width,
                    node_height,
                ),
                fill_color=fill_color,
                border_color=DEFAULT_BORDER_COLOR,
            )
            item.node_clicked.connect(self.node_selected.emit)
            item.node_double_clicked.connect(self.node_double_selected.emit)
            self._scene.addItem(item)
            self._node_items[node_id] = item

        self._build_legend()

        scene_rect = self._scene.itemsBoundingRect().adjusted(-80, -80, 80, 80)
        self.setSceneRect(scene_rect)
        self.fitInView(scene_rect, Qt.KeepAspectRatio)

    def _build_legend(self) -> None:
        x0 = -40
        y0 = -40

        bg = QGraphicsRectItem(x0, y0, 250, 70)
        bg.setBrush(QBrush(QColor("#FFFFFF")))
        bg.setPen(QPen(QColor("#BBBBBB"), 1))
        self._scene.addItem(bg)
        self._legend_items.append(bg)

        title = QGraphicsSimpleTextItem("Legend")
        title.setPos(x0 + 8, y0 + 4)
        title.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self._scene.addItem(title)
        self._legend_items.append(title)

        import_line = QGraphicsLineItem(x0 + 10, y0 + 28, x0 + 60, y0 + 28)
        import_line.setPen(QPen(IMPORT_EDGE_COLOR, 2))
        self._scene.addItem(import_line)
        self._legend_items.append(import_line)

        import_text = QGraphicsSimpleTextItem("Import edge")
        import_text.setPos(x0 + 70, y0 + 18)
        self._scene.addItem(import_text)
        self._legend_items.append(import_text)

        call_line = QGraphicsLineItem(x0 + 10, y0 + 50, x0 + 60, y0 + 50)
        call_line.setPen(QPen(CALL_EDGE_COLOR, 2))
        self._scene.addItem(call_line)
        self._legend_items.append(call_line)

        call_text = QGraphicsSimpleTextItem("Call edge")
        call_text.setPos(x0 + 70, y0 + 40)
        self._scene.addItem(call_text)
        self._legend_items.append(call_text)

    def export_png(self, output_path: str) -> None:
        rect = self._scene.itemsBoundingRect().adjusted(-40, -40, 40, 40)
        image = QImage(int(rect.width()), int(rect.height()), QImage.Format_ARGB32)
        image.fill(QColor("#FFFFFF"))

        painter = QPainter(image)
        self._scene.render(painter, QRectF(image.rect()), rect)
        painter.end()

        image.save(output_path)


def compute_layered_positions(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> dict[str, tuple[float, float]]:
    node_ids = [node["id"] for node in nodes]
    indegree: dict[str, int] = {node_id: 0 for node_id in node_ids}
    outgoing: dict[str, list[str]] = {node_id: [] for node_id in node_ids}

    for edge in edges:
        source_id = edge["source"]
        target_id = edge["target"]
        if source_id in outgoing and target_id in indegree:
            outgoing[source_id].append(target_id)
            indegree[target_id] += 1

    roots = [node_id for node_id in node_ids if indegree[node_id] == 0]
    if not roots:
        roots = node_ids[:1]

    levels: dict[str, int] = {}
    queue = deque()

    for root in roots:
        levels[root] = 0
        queue.append(root)

    while queue:
        current = queue.popleft()
        current_level = levels[current]
        for neighbor in outgoing.get(current, []):
            next_level = current_level + 1
            if neighbor not in levels or next_level > levels[neighbor]:
                levels[neighbor] = next_level
                queue.append(neighbor)

    for node_id in node_ids:
        levels.setdefault(node_id, 0)

    layers: dict[int, list[str]] = defaultdict(list)
    for node_id, level in levels.items():
        layers[level].append(node_id)

    x_spacing = 320.0
    y_spacing = 150.0
    positions: dict[str, tuple[float, float]] = {}

    for level in sorted(layers.keys()):
        layer_nodes = sorted(layers[level])
        total_height = (len(layer_nodes) - 1) * y_spacing
        start_y = -total_height / 2.0

        for index, node_id in enumerate(layer_nodes):
            x_pos = level * x_spacing
            y_pos = start_y + (index * y_spacing)
            positions[node_id] = (x_pos, y_pos)

    return positions


class ProjectJsonExplorerV5(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Project JSON Explorer v5")
        self.resize(1800, 1040)

        self.index_data: dict[str, Any] | None = None
        self.project_root: str = ""
        self.files_by_path: dict[str, dict[str, Any]] = {}
        self.files_by_module: dict[str, dict[str, Any]] = {}
        self.call_graph_out: dict[str, set[str]] = defaultdict(set)
        self.import_graph_out: dict[str, set[str]] = defaultdict(set)
        self.semantic_roles: dict[str, dict[str, Any]] = {}

        self.json_path_edit = QLineEdit()
        self.question_edit = QLineEdit()
        self.source_search_edit = QLineEdit()

        self.load_button = QPushButton("Load JSON")
        self.ask_button = QPushButton("Ask")
        self.clear_button = QPushButton("Clear")
        self.open_source_button = QPushButton("Open Source File")
        self.refresh_source_button = QPushButton("Refresh Source Preview")
        self.expand_neighbors_button = QPushButton("Expand Neighbors")
        self.rebuild_graph_button = QPushButton("Rebuild Graph")
        self.export_png_button = QPushButton("Export Graph PNG")
        self.find_in_source_button = QPushButton("Find In Source")

        self.quick_startup_button = QPushButton("Startup")
        self.quick_tabs_button = QPushButton("Tabs")
        self.quick_topomap_button = QPushButton("Topomap")
        self.quick_timeline_button = QPushButton("Timeline")
        self.quick_splash_button = QPushButton("Splash")
        self.quick_reset_button = QPushButton("Reset")

        self.result_list = QListWidget()
        self.detail_text = QPlainTextEdit()
        self.detail_text.setReadOnly(True)

        self.graph_list = QListWidget()
        self.graph_text = QPlainTextEdit()
        self.graph_text.setReadOnly(True)

        self.source_preview = QPlainTextEdit()
        self.source_preview.setReadOnly(True)
        self.source_path_label = QLabel("Source: -")

        self.graph_canvas = GraphCanvas()
        self.graph_canvas.node_selected.connect(self._graph_node_selected)
        self.graph_canvas.node_double_selected.connect(self._graph_node_double_selected)

        self.log_box = QPlainTextEdit()
        self.log_box.setReadOnly(True)

        self.tabs = QTabWidget()

        self._current_graph_mode = ""
        self._base_graph_mode = ""
        self._current_graph_nodes: list[dict[str, Any]] = []
        self._current_graph_edges: list[dict[str, Any]] = []
        self._isolated_node_id = ""

        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

        load_row = QHBoxLayout()
        load_row.addWidget(QLabel("JSON:"))
        load_row.addWidget(self.json_path_edit)
        load_row.addWidget(self.load_button)

        query_row = QHBoxLayout()
        query_row.addWidget(QLabel("Question:"))
        query_row.addWidget(self.question_edit)
        query_row.addWidget(self.ask_button)
        query_row.addWidget(self.clear_button)

        quick_row = QHBoxLayout()
        quick_row.addWidget(self.quick_startup_button)
        quick_row.addWidget(self.quick_tabs_button)
        quick_row.addWidget(self.quick_topomap_button)
        quick_row.addWidget(self.quick_timeline_button)
        quick_row.addWidget(self.quick_splash_button)
        quick_row.addWidget(self.quick_reset_button)
        quick_row.addStretch()
        quick_row.addWidget(self.expand_neighbors_button)
        quick_row.addWidget(self.rebuild_graph_button)
        quick_row.addWidget(self.export_png_button)

        source_tools_row = QHBoxLayout()
        source_tools_row.addWidget(QLabel("Find in source:"))
        source_tools_row.addWidget(self.source_search_edit)
        source_tools_row.addWidget(self.find_in_source_button)
        source_tools_row.addStretch()
        source_tools_row.addWidget(self.refresh_source_button)
        source_tools_row.addWidget(self.open_source_button)

        search_page = QWidget()
        search_layout = QVBoxLayout(search_page)
        search_splitter = QSplitter(Qt.Horizontal)
        search_splitter.addWidget(self.result_list)
        search_splitter.addWidget(self.detail_text)
        search_splitter.addWidget(self.source_preview)
        search_splitter.setSizes([360, 560, 860])
        search_layout.addWidget(self.source_path_label)
        search_layout.addLayout(source_tools_row)
        search_layout.addWidget(search_splitter)

        graph_page = QWidget()
        graph_layout = QVBoxLayout(graph_page)

        graph_upper_splitter = QSplitter(Qt.Horizontal)
        graph_upper_splitter.addWidget(self.graph_list)
        graph_upper_splitter.addWidget(self.graph_canvas)
        graph_upper_splitter.setSizes([360, 1020])

        graph_lower_splitter = QSplitter(Qt.Horizontal)
        graph_lower_splitter.addWidget(self.graph_text)
        graph_lower_splitter.addWidget(self.source_preview)
        graph_lower_splitter.setSizes([560, 860])

        graph_layout.addWidget(self.source_path_label)
        graph_layout.addLayout(source_tools_row)
        graph_layout.addWidget(graph_upper_splitter, stretch=2)
        graph_layout.addWidget(graph_lower_splitter, stretch=1)

        self.tabs.addTab(search_page, "Search")
        self.tabs.addTab(graph_page, "Graph Views")

        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout(log_group)
        log_layout.addWidget(self.log_box)

        main_layout.addLayout(load_row)
        main_layout.addLayout(query_row)
        main_layout.addLayout(quick_row)
        main_layout.addWidget(self.tabs, stretch=1)
        main_layout.addWidget(log_group, stretch=0)

    def _connect_signals(self) -> None:
        self.load_button.clicked.connect(self.load_json)
        self.ask_button.clicked.connect(self.ask_question)
        self.clear_button.clicked.connect(self.clear_all)
        self.question_edit.returnPressed.connect(self.ask_question)

        self.quick_startup_button.clicked.connect(lambda: self.run_graph_view("startup"))
        self.quick_tabs_button.clicked.connect(lambda: self.run_graph_view("tabs"))
        self.quick_topomap_button.clicked.connect(lambda: self.run_graph_view("topomap"))
        self.quick_timeline_button.clicked.connect(lambda: self.run_graph_view("timeline"))
        self.quick_splash_button.clicked.connect(lambda: self.run_graph_view("splash"))
        self.quick_reset_button.clicked.connect(lambda: self.run_graph_view("reset"))

        self.result_list.currentItemChanged.connect(self._show_result_detail)
        self.graph_list.currentItemChanged.connect(self._show_graph_detail)

        self.refresh_source_button.clicked.connect(self.refresh_source_preview)
        self.open_source_button.clicked.connect(self.open_selected_source_file)
        self.expand_neighbors_button.clicked.connect(self.expand_current_graph_neighbors)
        self.rebuild_graph_button.clicked.connect(self.rebuild_current_graph)
        self.export_png_button.clicked.connect(self.export_current_graph_png)
        self.find_in_source_button.clicked.connect(self.find_in_source)
        self.source_search_edit.returnPressed.connect(self.find_in_source)

    def append_log(self, text: str) -> None:
        self.log_box.appendPlainText(text)

    def clear_all(self) -> None:
        self.result_list.clear()
        self.graph_list.clear()
        self.detail_text.clear()
        self.graph_text.clear()
        self.source_preview.clear()
        self.graph_canvas.clear_graph()
        self.source_path_label.setText("Source: -")
        self.log_box.clear()
        self._current_graph_mode = ""
        self._base_graph_mode = ""
        self._current_graph_nodes = []
        self._current_graph_edges = []
        self._isolated_node_id = ""

    def load_json(self) -> None:
        current = self.json_path_edit.text().strip()
        start_dir = os.path.dirname(current) if current else os.getcwd()

        file_path, _filter = QFileDialog.getOpenFileName(
            self,
            "Load project_structure_index.json",
            start_dir,
            "JSON Files (*.json)",
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as handle:
                self.index_data = json.load(handle)

            self.json_path_edit.setText(file_path)
            self.project_root = (
                self.index_data.get("project_summary", {}).get("project_root", "") or ""
            )
            self.semantic_roles = self.index_data.get("semantic_roles", {})
            self._rebuild_indexes()

            self.append_log("Loaded JSON: " + file_path)
            self.append_log("Project root: " + self.project_root)

            summary = self.index_data.get("project_summary", {})
            self.append_log("Python files: " + str(summary.get("python_file_count", "unknown")))
            self.append_log("Entry files: " + str(summary.get("entry_file_count", "unknown")))

            QMessageBox.information(self, "Loaded", "JSON loaded successfully.")
        except Exception as exc:
            QMessageBox.critical(self, "Error", "Failed to load JSON:\n" + str(exc))
            self.append_log("ERROR loading JSON: " + str(exc))

    def _rebuild_indexes(self) -> None:
        self.files_by_path.clear()
        self.files_by_module.clear()
        self.call_graph_out.clear()
        self.import_graph_out.clear()

        if not self.index_data:
            return

        for file_record in self.index_data.get("files", []):
            path = file_record.get("path", "")
            module_name = file_record.get("module_name", "")
            if path:
                self.files_by_path[path] = file_record
            if module_name:
                self.files_by_module[module_name] = file_record

        for src_module, targets in self.index_data.get("import_graph", {}).items():
            src_path = self._resolve_module_to_path(src_module) or src_module
            for target in targets:
                self.import_graph_out[src_path].add(target)

        for edge in self.index_data.get("call_edges", []):
            from_file = edge.get("from_file", "")
            to_call = edge.get("to_call", "")
            if from_file and to_call:
                self.call_graph_out[from_file].add(to_call)

    def _resolve_module_to_path(self, module_name: str) -> str | None:
        record = self.files_by_module.get(module_name)
        if record:
            return record.get("path")
        return None

    def ask_question(self) -> None:
        if not self.index_data:
            QMessageBox.warning(self, "No JSON", "Please load a JSON file first.")
            return

        question = self.question_edit.text().strip()
        if not question:
            QMessageBox.warning(self, "No Question", "Please type a question.")
            return

        self.result_list.clear()
        self.detail_text.clear()
        self.tabs.setCurrentIndex(0)

        results = self._search(question)

        self.append_log("Question: " + question)
        self.append_log("Search results: " + str(len(results)))

        for result in results:
            item = QListWidgetItem(result["title"])
            item.setData(Qt.UserRole, result)
            self.result_list.addItem(item)

        if results:
            self.result_list.setCurrentRow(0)

    def _search(self, question: str) -> list[dict[str, Any]]:
        q = norm_text(question)
        tokens = tokenize_query(q)
        entry_files = set(self.index_data.get("entry_files", []))

        scored: list[dict[str, Any]] = []

        for path, file_record in self.files_by_path.items():
            module_name = file_record.get("module_name", "")
            docstring = file_record.get("docstring", "")
            strings = " ".join(file_record.get("strings", []))
            comments = " ".join(file_record.get("comments", []))
            ui_hits = " ".join(file_record.get("ui_keyword_hits", []))
            eeg_hits = " ".join(file_record.get("eeg_keyword_hits", []))
            semantic_hints = " ".join(file_record.get("semantic_hints", []))
            entry_markers = " ".join(file_record.get("entry_markers", []))

            function_names = []
            call_names = []
            class_names = []

            for fn in file_record.get("functions", []):
                function_names.append(fn.get("name", ""))
                function_names.append(fn.get("qualname", ""))
                for call in fn.get("calls", []):
                    call_names.append(call.get("call_name", ""))

            for cls in file_record.get("classes", []):
                class_names.append(cls.get("name", ""))
                for method in cls.get("methods", []):
                    function_names.append(method.get("name", ""))
                    function_names.append(method.get("qualname", ""))
                    for call in method.get("calls", []):
                        call_names.append(call.get("call_name", ""))

            haystack = " ".join([
                norm_text(path),
                norm_text(module_name),
                norm_text(docstring),
                norm_text(strings),
                norm_text(comments),
                norm_text(ui_hits),
                norm_text(eeg_hits),
                norm_text(semantic_hints),
                norm_text(entry_markers),
                norm_text(" ".join(function_names)),
                norm_text(" ".join(call_names)),
                norm_text(" ".join(class_names)),
            ])

            roles = self.semantic_roles.get(path, {}).get("roles", [])
            score = 0
            reasons = []

            for token in tokens:
                if token in haystack:
                    score += 3
                    reasons.append("token match: " + token)

            if path in entry_files and ("start" in q or "main" in q or "entry" in q or "launch" in q):
                score += 20
                reasons.append("entry file")

            if "topomap" in q and ("topomap" in haystack or "amplitude_map" in haystack or "topomap" in roles):
                score += 18
                reasons.append("topomap match")

            if "tab" in q and ("addtab" in haystack or "notebook" in haystack or "tabs" in roles):
                score += 15
                reasons.append("tab match")

            if "timeline" in q and ("timeline" in haystack or "timeline" in roles):
                score += 15
                reasons.append("timeline match")

            if "splash" in q and ("splash" in haystack or "splash" in roles):
                score += 15
                reasons.append("splash match")

            if ("reset" in q or "snapshot" in q) and (
                "reset" in haystack or "snapshot" in haystack or "state_reset" in roles
            ):
                score += 15
                reasons.append("reset or snapshot match")

            if score > 0:
                best_line = self._best_line_for_file(file_record, q)
                scored.append(
                    {
                        "score": score,
                        "title": "[" + str(score) + "] " + path + " | " + module_name,
                        "detail": self._build_file_detail(path, reasons),
                        "path": path,
                        "line": best_line,
                    }
                )

        scored.sort(key=lambda item: (-item["score"], item["path"]))
        return scored[:50]

    def _best_line_for_file(self, file_record: dict[str, Any], question: str) -> int:
        q = norm_text(question)

        for fn in file_record.get("functions", []):
            if norm_text(fn.get("qualname", "")) in q or norm_text(fn.get("name", "")) in q:
                return int(fn.get("lineno", 1))

        for cls in file_record.get("classes", []):
            if norm_text(cls.get("name", "")) in q:
                return int(cls.get("lineno", 1))
            for method in cls.get("methods", []):
                if norm_text(method.get("qualname", "")) in q or norm_text(method.get("name", "")) in q:
                    return int(method.get("lineno", 1))

        if file_record.get("functions"):
            return int(file_record["functions"][0].get("lineno", 1))
        if file_record.get("classes"):
            return int(file_record["classes"][0].get("lineno", 1))
        return 1

    def _build_file_detail(self, path: str, reasons: list[str]) -> str:
        file_record = self.files_by_path[path]
        roles = self.semantic_roles.get(path, {}).get("roles", [])

        lines = []
        lines.append("FILE")
        lines.append(path)
        lines.append("")
        lines.append("MODULE")
        lines.append(file_record.get("module_name", ""))
        lines.append("")
        lines.append("WHY THIS MATCHED")
        for reason in sorted(set(reasons)):
            lines.append("- " + reason)

        lines.append("")
        lines.append("ROLES")
        if roles:
            for role in roles:
                lines.append("- " + role)
        else:
            lines.append("- none")

        if file_record.get("entry_markers"):
            lines.append("")
            lines.append("ENTRY MARKERS")
            for marker in file_record["entry_markers"]:
                lines.append("- " + marker)

        if file_record.get("docstring"):
            lines.append("")
            lines.append("DOCSTRING")
            lines.append(file_record["docstring"])

        if file_record.get("functions"):
            lines.append("")
            lines.append("FUNCTIONS")
            for fn in file_record["functions"][:40]:
                lines.append("- " + fn.get("qualname", "") + " (line " + str(fn.get("lineno", "")) + ")")

        if file_record.get("classes"):
            lines.append("")
            lines.append("CLASSES")
            for cls in file_record["classes"][:30]:
                line = "- " + cls.get("name", "") + " (line " + str(cls.get("lineno", "")) + ")"
                bases = cls.get("bases", [])
                if bases:
                    line += " bases: " + ", ".join(bases)
                lines.append(line)
                for method in cls.get("methods", [])[:15]:
                    lines.append("    * " + method.get("qualname", "") + " (line " + str(method.get("lineno", "")) + ")")

        imports_out = sorted(self.import_graph_out.get(path, []))
        if imports_out:
            lines.append("")
            lines.append("IMPORTS OUT")
            for item in imports_out[:50]:
                lines.append("- " + item)

        calls_out = sorted(self.call_graph_out.get(path, []))
        if calls_out:
            lines.append("")
            lines.append("CALLS OUT")
            for item in calls_out[:80]:
                lines.append("- " + item)

        return "\n".join(lines)

    def _show_result_detail(self, current: QListWidgetItem, previous: QListWidgetItem) -> None:
        _ = previous
        if not current:
            self.detail_text.clear()
            return

        payload = current.data(Qt.UserRole)
        if not payload:
            return

        self.detail_text.setPlainText(payload.get("detail", ""))
        self._load_source_preview(payload.get("path", ""), int(payload.get("line", 1)))

    def run_graph_view(self, mode: str) -> None:
        if not self.index_data:
            QMessageBox.warning(self, "No JSON", "Please load a JSON file first.")
            return

        self.graph_list.clear()
        self.graph_text.clear()
        self.graph_canvas.clear_graph()
        self.tabs.setCurrentIndex(1)

        self._current_graph_mode = mode
        self._base_graph_mode = mode
        self._isolated_node_id = ""

        nodes, edges = self._collect_graph_nodes_and_edges(mode)
        self._current_graph_nodes = nodes
        self._current_graph_edges = edges

        self._repaint_graph_view()

        self.append_log("Graph view: " + mode)
        self.append_log("Graph nodes: " + str(len(nodes)))
        self.append_log("Graph edges: " + str(len(edges)))

    def _collect_graph_nodes_and_edges(self, mode: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        entry_files = set(self.index_data.get("entry_files", []))
        nodes = []
        edges: list[dict[str, Any]] = []

        selected_paths = []

        for path, file_record in self.files_by_path.items():
            roles = self.semantic_roles.get(path, {}).get("roles", [])
            title = path + " | " + file_record.get("module_name", "")
            text = self._all_text(path)

            matched = False
            reasons = []

            if mode == "startup":
                if path in entry_files or "startup" in roles or "main_window" in roles:
                    matched = True
                    reasons.append("startup related")
            elif mode == "tabs":
                if "tabs" in roles or "notebook" in text or "addtab" in text:
                    matched = True
                    reasons.append("tab related")
            elif mode == "topomap":
                if "topomap" in roles or "topomap" in text or "amplitude_map" in text:
                    matched = True
                    reasons.append("topomap related")
            elif mode == "timeline":
                if "timeline" in roles or "timeline" in text:
                    matched = True
                    reasons.append("timeline related")
            elif mode == "splash":
                if "splash" in roles or "splash" in text:
                    matched = True
                    reasons.append("splash related")
            elif mode == "reset":
                if "state_reset" in roles or "reset" in text or "snapshot" in text:
                    matched = True
                    reasons.append("reset or snapshot related")

            if matched:
                best_line = self._best_line_for_graph_mode(file_record, mode)
                selected_paths.append(path)
                nodes.append(
                    {
                        "id": path,
                        "title": title,
                        "label": shorten_path(path),
                        "detail": self._build_graph_detail(path, reasons),
                        "path": path,
                        "line": best_line,
                        "roles": roles,
                    }
                )

        selected_path_set = set(selected_paths)

        for path in selected_paths:
            for imported in self.import_graph_out.get(path, set()):
                resolved = self._resolve_module_to_path(imported)
                if resolved and resolved in selected_path_set:
                    edges.append(
                        {
                            "source": path,
                            "target": resolved,
                            "type": "import",
                        }
                    )

            for call_name in self.call_graph_out.get(path, set()):
                for candidate_path, candidate_record in self.files_by_path.items():
                    if candidate_path == path:
                        continue
                    if candidate_path not in selected_path_set:
                        continue
                    if self._file_contains_symbol(candidate_record, call_name):
                        edges.append(
                            {
                                "source": path,
                                "target": candidate_path,
                                "type": "call",
                            }
                        )

        edges = dedupe_edge_dicts(edges)
        nodes.sort(key=lambda item: item["path"])
        return nodes[:90], edges[:260]

    def _best_line_for_graph_mode(self, file_record: dict[str, Any], mode: str) -> int:
        keywords_by_mode = {
            "startup": ["QApplication", "app.exec", "create_main_window", "display_pyside6_eeg_visualizer"],
            "tabs": ["addTab", "Notebook", "Tab", "TopInTabBar"],
            "topomap": ["topomap", "amplitude_map", "plot_topomap"],
            "timeline": ["timeline", "TimelineManager", "TimelineWidget"],
            "splash": ["splash", "SplashManager", "KandaSplashImageText"],
            "reset": ["reset", "snapshot", "reset_to_initial_eeg_state", "capture_initial_eeg_state"],
        }

        wanted = [norm_text(x) for x in keywords_by_mode.get(mode, [])]

        for fn in file_record.get("functions", []):
            blob = norm_text(fn.get("qualname", "") + " " + fn.get("name", ""))
            for item in wanted:
                if item in blob:
                    return int(fn.get("lineno", 1))

        for cls in file_record.get("classes", []):
            blob = norm_text(cls.get("name", ""))
            for item in wanted:
                if item in blob:
                    return int(cls.get("lineno", 1))
            for method in cls.get("methods", []):
                blob2 = norm_text(method.get("qualname", "") + " " + method.get("name", ""))
                for item in wanted:
                    if item in blob2:
                        return int(method.get("lineno", 1))

        return 1

    def _all_text(self, path: str) -> str:
        file_record = self.files_by_path[path]
        parts = [
            path,
            file_record.get("module_name", ""),
            file_record.get("docstring", ""),
            " ".join(file_record.get("strings", [])),
            " ".join(file_record.get("comments", [])),
            " ".join(file_record.get("entry_markers", [])),
            " ".join(file_record.get("ui_keyword_hits", [])),
            " ".join(file_record.get("eeg_keyword_hits", [])),
            " ".join(file_record.get("semantic_hints", [])),
        ]

        for fn in file_record.get("functions", []):
            parts.append(fn.get("qualname", ""))
            for call in fn.get("calls", []):
                parts.append(call.get("call_name", ""))

        for cls in file_record.get("classes", []):
            parts.append(cls.get("name", ""))
            for method in cls.get("methods", []):
                parts.append(method.get("qualname", ""))
                for call in method.get("calls", []):
                    parts.append(call.get("call_name", ""))

        return norm_text(" ".join(parts))

    def _build_graph_detail(self, path: str, reasons: list[str]) -> str:
        file_record = self.files_by_path[path]
        roles = self.semantic_roles.get(path, {}).get("roles", [])

        lines = []
        lines.append("NODE")
        lines.append(path)
        lines.append("")
        lines.append("WHY INCLUDED")
        for reason in reasons:
            lines.append("- " + reason)

        lines.append("")
        lines.append("ROLES")
        if roles:
            for role in roles:
                lines.append("- " + role)
        else:
            lines.append("- none")

        lines.append("")
        lines.append("OUTGOING IMPORTS")
        imports_out = sorted(self.import_graph_out.get(path, []))
        if imports_out:
            for item in imports_out[:50]:
                lines.append("- " + item)
        else:
            lines.append("- none")

        lines.append("")
        lines.append("OUTGOING CALLS")
        calls_out = sorted(self.call_graph_out.get(path, []))
        if calls_out:
            for item in calls_out[:80]:
                lines.append("- " + item)
        else:
            lines.append("- none")

        lines.append("")
        lines.append("NEIGHBOR FILE HINTS")
        neighbors = self._infer_neighbor_files(path)
        if neighbors:
            for item in neighbors[:40]:
                lines.append("- " + item)
        else:
            lines.append("- none")

        lines.append("")
        lines.append("FILE SUMMARY")
        lines.append(self._build_file_detail(path, reasons))

        return "\n".join(lines)

    def _infer_neighbor_files(self, path: str) -> list[str]:
        neighbors = set()

        for module_target in self.import_graph_out.get(path, set()):
            resolved = self._resolve_module_to_path(module_target)
            if resolved:
                neighbors.add(resolved)

        for call_name in self.call_graph_out.get(path, set()):
            for file_path, file_record in self.files_by_path.items():
                if self._file_contains_symbol(file_record, call_name):
                    neighbors.add(file_path)

        return sorted(neighbors)

    def _file_contains_symbol(self, file_record: dict[str, Any], symbol_name: str) -> bool:
        for fn in file_record.get("functions", []):
            if fn.get("name") == symbol_name or fn.get("qualname") == symbol_name:
                return True
        for cls in file_record.get("classes", []):
            if cls.get("name") == symbol_name:
                return True
            for method in cls.get("methods", []):
                if method.get("name") == symbol_name or method.get("qualname") == symbol_name:
                    return True
        return False

    def _show_graph_detail(self, current: QListWidgetItem, previous: QListWidgetItem) -> None:
        _ = previous
        if not current:
            self.graph_text.clear()
            return

        payload = current.data(Qt.UserRole)
        if not payload:
            return

        self.graph_text.setPlainText(payload.get("detail", ""))
        self._load_source_preview(payload.get("path", ""), int(payload.get("line", 1)))

    def _graph_node_selected(self, node_id: str) -> None:
        for row in range(self.graph_list.count()):
            item = self.graph_list.item(row)
            payload = item.data(Qt.UserRole)
            if payload and payload.get("path") == node_id:
                self.graph_list.setCurrentRow(row)
                self.graph_text.setPlainText(payload.get("detail", ""))
                self._load_source_preview(payload.get("path", ""), int(payload.get("line", 1)))
                break

    def _graph_node_double_selected(self, node_id: str) -> None:
        self.isolate_subgraph(node_id)

    def isolate_subgraph(self, center_path: str) -> None:
        if not center_path:
            return

        node_map = {node["id"]: node for node in self._current_graph_nodes}
        if center_path not in node_map:
            return

        connected = {center_path}
        for edge in self._current_graph_edges:
            if edge["source"] == center_path:
                connected.add(edge["target"])
            if edge["target"] == center_path:
                connected.add(edge["source"])

        isolated_nodes = [node_map[node_id] for node_id in connected if node_id in node_map]
        isolated_edges = [
            edge
            for edge in self._current_graph_edges
            if edge["source"] in connected and edge["target"] in connected
        ]

        self._isolated_node_id = center_path
        self.graph_canvas.build_graph(isolated_nodes, isolated_edges)

        self.graph_list.clear()
        for node in isolated_nodes:
            item = QListWidgetItem(node["title"])
            item.setData(Qt.UserRole, node)
            self.graph_list.addItem(item)

        self.append_log("Isolated subgraph around: " + center_path)

    def expand_current_graph_neighbors(self) -> None:
        if not self._current_graph_nodes:
            QMessageBox.information(self, "No Graph", "Build a graph view first.")
            return

        current_item = self.graph_list.currentItem()
        if not current_item:
            QMessageBox.information(self, "No Selection", "Select a graph node first.")
            return

        payload = current_item.data(Qt.UserRole)
        if not payload:
            return

        base_path = payload.get("path", "")
        if not base_path:
            return

        neighbor_paths = self._infer_neighbor_files(base_path)
        existing = {node["id"] for node in self._current_graph_nodes}
        node_map = {node["id"]: node for node in self._current_graph_nodes}
        edge_map = {(edge["source"], edge["target"], edge["type"]): edge for edge in self._current_graph_edges}

        for neighbor_path in neighbor_paths[:20]:
            if neighbor_path not in self.files_by_path:
                continue

            if neighbor_path not in existing:
                roles = self.semantic_roles.get(neighbor_path, {}).get("roles", [])
                rec = self.files_by_path[neighbor_path]
                node_map[neighbor_path] = {
                    "id": neighbor_path,
                    "title": neighbor_path + " | " + rec.get("module_name", ""),
                    "label": shorten_path(neighbor_path),
                    "detail": self._build_graph_detail(neighbor_path, ["expanded neighbor"]),
                    "path": neighbor_path,
                    "line": 1,
                    "roles": roles,
                }
                existing.add(neighbor_path)

            edge_key = (base_path, neighbor_path, "call")
            edge_map[edge_key] = {
                "source": base_path,
                "target": neighbor_path,
                "type": "call",
            }

        self._current_graph_nodes = sorted(node_map.values(), key=lambda item: item["path"])
        self._current_graph_edges = sorted(edge_map.values(), key=lambda item: (item["source"], item["target"], item["type"]))

        self._repaint_graph_view()
        self.append_log("Expanded neighbors for: " + base_path)

    def rebuild_current_graph(self) -> None:
        if not self._base_graph_mode:
            QMessageBox.information(self, "No Graph", "Build a graph view first.")
            return
        self.run_graph_view(self._base_graph_mode)

    def export_current_graph_png(self) -> None:
        if not self._current_graph_nodes:
            QMessageBox.information(self, "No Graph", "Build a graph view first.")
            return

        output_path, _filter = QFileDialog.getSaveFileName(
            self,
            "Export Graph PNG",
            os.path.join(os.getcwd(), "project_graph.png"),
            "PNG Files (*.png)",
        )
        if not output_path:
            return

        if not output_path.lower().endswith(".png"):
            output_path += ".png"

        try:
            self.graph_canvas.export_png(output_path)
            self.append_log("Graph exported to: " + output_path)
            QMessageBox.information(self, "Exported", "Graph exported successfully.")
        except Exception as exc:
            QMessageBox.critical(self, "Error", "Failed to export PNG:\n" + str(exc))

    def _repaint_graph_view(self) -> None:
        self.graph_canvas.build_graph(self._current_graph_nodes, self._current_graph_edges)

        self.graph_list.clear()
        for node in self._current_graph_nodes:
            item = QListWidgetItem(node["title"])
            item.setData(Qt.UserRole, node)
            self.graph_list.addItem(item)

        if self._current_graph_nodes:
            self.graph_list.setCurrentRow(0)

    def _absolute_source_path(self, relative_path: str) -> str:
        if not self.project_root:
            return ""
        return os.path.normpath(os.path.join(self.project_root, relative_path))

    def _load_source_preview(self, relative_path: str, line_number: int) -> None:
        abs_path = self._absolute_source_path(relative_path)
        self.source_path_label.setText("Source: " + abs_path if abs_path else "Source: -")

        if not abs_path or not os.path.exists(abs_path):
            self.source_preview.setPlainText("Source file not found:\n" + abs_path)
            return

        try:
            source = safe_read_text(abs_path)
        except Exception as exc:
            self.source_preview.setPlainText("Failed to read source:\n" + str(exc))
            return

        numbered = []
        for idx, line in enumerate(source.splitlines(), start=1):
            numbered.append(str(idx).rjust(5) + " | " + line)

        self.source_preview.setPlainText("\n".join(numbered))
        self._scroll_preview_to_line(line_number)
        self.append_log("Preview loaded: " + relative_path + " @ line " + str(line_number))

    def _scroll_preview_to_line(self, line_number: int) -> None:
        if line_number < 1:
            line_number = 1

        block = self.source_preview.document().findBlockByLineNumber(line_number - 1)
        if not block.isValid():
            return

        cursor = QTextCursor(block)
        self.source_preview.setTextCursor(cursor)
        self.source_preview.centerCursor()

    def refresh_source_preview(self) -> None:
        payload = self._current_payload()
        if not payload:
            QMessageBox.information(self, "No Selection", "Select a result first.")
            return
        self._load_source_preview(payload.get("path", ""), int(payload.get("line", 1)))

    def open_selected_source_file(self) -> None:
        payload = self._current_payload()
        if not payload:
            QMessageBox.information(self, "No Selection", "Select a result first.")
            return

        relative_path = payload.get("path", "")
        line_number = int(payload.get("line", 1))
        abs_path = self._absolute_source_path(relative_path)

        if not abs_path or not os.path.exists(abs_path):
            QMessageBox.warning(self, "File Not Found", "Source file not found:\n" + abs_path)
            return

        self._load_source_preview(relative_path, line_number)

        QMessageBox.information(
            self,
            "Source Opened In Preview",
            "Loaded source preview for:\n"
            + abs_path
            + "\n\nApproximate line: "
            + str(line_number),
        )

    def find_in_source(self) -> None:
        query = self.source_search_edit.text().strip()
        if not query:
            QMessageBox.information(self, "No Search Text", "Type text to search in source preview.")
            return

        found = self.source_preview.find(query)
        if not found:
            cursor = self.source_preview.textCursor()
            cursor.movePosition(QTextCursor.Start)
            self.source_preview.setTextCursor(cursor)
            found = self.source_preview.find(query)

        if not found:
            QMessageBox.information(self, "Not Found", "Text not found in source preview.")
        else:
            self.append_log("Found in source: " + query)

    def _current_payload(self) -> dict[str, Any] | None:
        current_tab = self.tabs.currentIndex()

        if current_tab == 0:
            item = self.result_list.currentItem()
        else:
            item = self.graph_list.currentItem()

        if not item:
            return None

        payload = item.data(Qt.UserRole)
        if not isinstance(payload, dict):
            return None

        return payload


def dedupe_edge_dicts(edges: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen = set()
    result = []

    for edge in edges:
        key = (edge["source"], edge["target"], edge["type"])
        if key in seen:
            continue
        seen.add(key)
        result.append(edge)

    result.sort(key=lambda item: (item["source"], item["target"], item["type"]))
    return result


def main() -> None:
    app = QApplication(sys.argv)
    window = ProjectJsonExplorerV5()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

What version 5 adds:
left-to-right layered graph layout
blue import edges
red call edges
legend on the graph
PNG export
search inside source preview
double-click node to isolate local subgraph
rebuild graph after isolation

Best next step would be version 6 with:
true symbol-level graph, not only file-level
filters for edge type
path tracing between two files
side panel showing exact matched symbols instead of only file summaries

go
Thought for 4s

Here is version 6.

This one adds the next major upgrade:
symbol-level exploration on top of the file-level graph.

New capabilities:
file-level graph and symbol-level graph
filter visible edges by type:
all
imports only
calls only
path tracing between two nodes
exact matched symbols panel
symbol neighbors
better graph inspection for startup, tabs, topomap, timeline, splash, reset

This is the most useful version so far for answering questions like:
which exact method creates the top tab
which exact function wires the timeline
which symbol is responsible for topomap
how startup flows from one module to another

from __future__ import annotations

import json
import os
import re
import sys
from collections import defaultdict, deque
from typing import Any

from PySide6.QtCore import QRectF, Qt, Signal
from PySide6.QtGui import QBrush, QColor, QFont, QImage, QPainter, QPen, QTextCursor
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QGraphicsEllipseItem,
    QGraphicsItem,
    QGraphicsLineItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsSimpleTextItem,
    QGraphicsView,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QSplitter,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


IMPORT_EDGE_COLOR = QColor("#4C78A8")
CALL_EDGE_COLOR = QColor("#E45756")
SYMBOL_EDGE_COLOR = QColor("#54A24B")
DEFAULT_BORDER_COLOR = QColor("#333333")
HOVER_BORDER_COLOR = QColor("#FF8800")


def norm_text(value: Any) -> str:
    return str(value).strip().lower() if value is not None else ""


def tokenize_query(text: str) -> list[str]:
    tokens = re.findall(r"[a-zA-Z0-9_\.]+", text.lower())
    stop_words = {
        "the",
        "is",
        "are",
        "a",
        "an",
        "of",
        "to",
        "me",
        "show",
        "which",
        "what",
        "where",
        "who",
        "does",
        "do",
        "in",
        "on",
        "for",
        "and",
        "or",
        "with",
        "code",
        "module",
        "file",
        "implementing",
        "implements",
        "created",
        "creates",
        "create",
        "that",
        "this",
        "app",
    }
    return [token for token in tokens if token not in stop_words]


def safe_read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return handle.read()


def shorten_path(path: str, max_len: int = 28) -> str:
    if len(path) <= max_len:
        return path
    parts = path.replace("\\", "/").split("/")
    if len(parts) >= 2:
        short = parts[-2] + "/" + parts[-1]
        if len(short) <= max_len:
            return short
    return "..." + path[-(max_len - 3):]


def shorten_symbol(symbol: str, max_len: int = 38) -> str:
    if len(symbol) <= max_len:
        return symbol
    return "..." + symbol[-(max_len - 3):]


def role_to_color(roles: list[str]) -> QColor:
    if "startup" in roles:
        return QColor("#D6ECFF")
    if "tabs" in roles:
        return QColor("#E9DDFF")
    if "topomap" in roles:
        return QColor("#D8FFD8")
    if "timeline" in roles:
        return QColor("#FFF0C9")
    if "splash" in roles:
        return QColor("#FFDCE5")
    if "state_reset" in roles:
        return QColor("#FFE0C7")
    if "main_window" in roles:
        return QColor("#D9F5F0")
    return QColor("#F0F0F0")


class GraphNodeItem(QGraphicsEllipseItem):
    node_clicked = Signal(str)
    node_double_clicked = Signal(str)

    def __init__(
        self,
        node_id: str,
        label: str,
        rect: QRectF,
        fill_color: QColor,
        border_color: QColor,
    ) -> None:
        super().__init__(rect)
        self.node_id = node_id
        self.label = label
        self.setBrush(QBrush(fill_color))
        self.setPen(QPen(border_color, 2))
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setAcceptHoverEvents(True)

        self.text_item = QGraphicsSimpleTextItem(label, self)
        font = QFont("Segoe UI", 9)
        self.text_item.setFont(font)

        text_rect = self.text_item.boundingRect()
        x_pos = rect.center().x() - (text_rect.width() / 2.0)
        y_pos = rect.center().y() - (text_rect.height() / 2.0)
        self.text_item.setPos(x_pos, y_pos)

    def hoverEnterEvent(self, event) -> None:
        self.setPen(QPen(HOVER_BORDER_COLOR, 3))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event) -> None:
        self.setPen(QPen(DEFAULT_BORDER_COLOR, 2))
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event) -> None:
        self.node_clicked.emit(self.node_id)
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event) -> None:
        self.node_double_clicked.emit(self.node_id)
        super().mouseDoubleClickEvent(event)


class GraphCanvas(QGraphicsView):
    node_selected = Signal(str)
    node_double_selected = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    def clear_graph(self) -> None:
        self._scene.clear()

    def wheelEvent(self, event) -> None:
        if event.modifiers() & Qt.ControlModifier:
            factor = 1.15 if event.angleDelta().y() > 0 else (1.0 / 1.15)
            self.scale(factor, factor)
            event.accept()
            return
        super().wheelEvent(event)

    def build_graph(
        self,
        nodes: list[dict[str, Any]],
        edges: list[dict[str, Any]],
    ) -> None:
        self.clear_graph()

        if not nodes:
            return

        positions = compute_layered_positions(nodes, edges)

        for edge in edges:
            source_id = edge["source"]
            target_id = edge["target"]
            edge_type = edge["type"]

            if source_id not in positions or target_id not in positions:
                continue

            x1, y1 = positions[source_id]
            x2, y2 = positions[target_id]

            line = QGraphicsLineItem(x1, y1, x2, y2)
            if edge_type == "import":
                line.setPen(QPen(IMPORT_EDGE_COLOR, 2))
            elif edge_type == "call":
                line.setPen(QPen(CALL_EDGE_COLOR, 2))
            else:
                line.setPen(QPen(SYMBOL_EDGE_COLOR, 2))
            self._scene.addItem(line)

        node_width = 220.0
        node_height = 74.0

        for node in nodes:
            node_id = node["id"]
            x_pos, y_pos = positions[node_id]
            roles = node.get("roles", [])
            fill_color = role_to_color(roles) if roles else QColor("#F8F8F8")

            item = GraphNodeItem(
                node_id=node_id,
                label=node["label"],
                rect=QRectF(
                    x_pos - node_width / 2.0,
                    y_pos - node_height / 2.0,
                    node_width,
                    node_height,
                ),
                fill_color=fill_color,
                border_color=DEFAULT_BORDER_COLOR,
            )
            item.node_clicked.connect(self.node_selected.emit)
            item.node_double_clicked.connect(self.node_double_selected.emit)
            self._scene.addItem(item)

        self._build_legend()

        scene_rect = self._scene.itemsBoundingRect().adjusted(-80, -80, 80, 80)
        self.setSceneRect(scene_rect)
        self.fitInView(scene_rect, Qt.KeepAspectRatio)

    def _build_legend(self) -> None:
        x0 = -40
        y0 = -40

        bg = QGraphicsRectItem(x0, y0, 290, 92)
        bg.setBrush(QBrush(QColor("#FFFFFF")))
        bg.setPen(QPen(QColor("#BBBBBB"), 1))
        self._scene.addItem(bg)

        title = QGraphicsSimpleTextItem("Legend")
        title.setPos(x0 + 8, y0 + 4)
        title.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self._scene.addItem(title)

        import_line = QGraphicsLineItem(x0 + 10, y0 + 28, x0 + 60, y0 + 28)
        import_line.setPen(QPen(IMPORT_EDGE_COLOR, 2))
        self._scene.addItem(import_line)
        import_text = QGraphicsSimpleTextItem("Import edge")
        import_text.setPos(x0 + 70, y0 + 18)
        self._scene.addItem(import_text)

        call_line = QGraphicsLineItem(x0 + 10, y0 + 50, x0 + 60, y0 + 50)
        call_line.setPen(QPen(CALL_EDGE_COLOR, 2))
        self._scene.addItem(call_line)
        call_text = QGraphicsSimpleTextItem("Call edge")
        call_text.setPos(x0 + 70, y0 + 40)
        self._scene.addItem(call_text)

        symbol_line = QGraphicsLineItem(x0 + 10, y0 + 72, x0 + 60, y0 + 72)
        symbol_line.setPen(QPen(SYMBOL_EDGE_COLOR, 2))
        self._scene.addItem(symbol_line)
        symbol_text = QGraphicsSimpleTextItem("Symbol edge")
        symbol_text.setPos(x0 + 70, y0 + 62)
        self._scene.addItem(symbol_text)

    def export_png(self, output_path: str) -> None:
        rect = self._scene.itemsBoundingRect().adjusted(-40, -40, 40, 40)
        image = QImage(int(rect.width()), int(rect.height()), QImage.Format_ARGB32)
        image.fill(QColor("#FFFFFF"))

        painter = QPainter(image)
        self._scene.render(painter, QRectF(image.rect()), rect)
        painter.end()

        image.save(output_path)


def compute_layered_positions(
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> dict[str, tuple[float, float]]:
    node_ids = [node["id"] for node in nodes]
    indegree: dict[str, int] = {node_id: 0 for node_id in node_ids}
    outgoing: dict[str, list[str]] = {node_id: [] for node_id in node_ids}

    for edge in edges:
        source_id = edge["source"]
        target_id = edge["target"]
        if source_id in outgoing and target_id in indegree:
            outgoing[source_id].append(target_id)
            indegree[target_id] += 1

    roots = [node_id for node_id in node_ids if indegree[node_id] == 0]
    if not roots:
        roots = node_ids[:1]

    levels: dict[str, int] = {}
    queue = deque()

    for root in roots:
        levels[root] = 0
        queue.append(root)

    while queue:
        current = queue.popleft()
        current_level = levels[current]
        for neighbor in outgoing.get(current, []):
            next_level = current_level + 1
            if neighbor not in levels or next_level > levels[neighbor]:
                levels[neighbor] = next_level
                queue.append(neighbor)

    for node_id in node_ids:
        levels.setdefault(node_id, 0)

    layers: dict[int, list[str]] = defaultdict(list)
    for node_id, level in levels.items():
        layers[level].append(node_id)

    x_spacing = 340.0
    y_spacing = 150.0
    positions: dict[str, tuple[float, float]] = {}

    for level in sorted(layers.keys()):
        layer_nodes = sorted(layers[level])
        total_height = (len(layer_nodes) - 1) * y_spacing
        start_y = -total_height / 2.0

        for index, node_id in enumerate(layer_nodes):
            x_pos = level * x_spacing
            y_pos = start_y + (index * y_spacing)
            positions[node_id] = (x_pos, y_pos)

    return positions


def dedupe_edge_dicts(edges: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen = set()
    result = []

    for edge in edges:
        key = (edge["source"], edge["target"], edge["type"])
        if key in seen:
            continue
        seen.add(key)
        result.append(edge)

    result.sort(key=lambda item: (item["source"], item["target"], item["type"]))
    return result


class ProjectJsonExplorerV6(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Project JSON Explorer v6")
        self.resize(1860, 1080)

        self.index_data: dict[str, Any] | None = None
        self.project_root: str = ""
        self.files_by_path: dict[str, dict[str, Any]] = {}
        self.files_by_module: dict[str, dict[str, Any]] = {}
        self.symbol_to_file: dict[str, set[str]] = defaultdict(set)
        self.symbol_details: dict[str, dict[str, Any]] = {}
        self.call_graph_out: dict[str, set[str]] = defaultdict(set)
        self.import_graph_out: dict[str, set[str]] = defaultdict(set)
        self.semantic_roles: dict[str, dict[str, Any]] = {}

        self.json_path_edit = QLineEdit()
        self.question_edit = QLineEdit()
        self.source_search_edit = QLineEdit()
        self.path_from_edit = QLineEdit()
        self.path_to_edit = QLineEdit()

        self.load_button = QPushButton("Load JSON")
        self.ask_button = QPushButton("Ask")
        self.clear_button = QPushButton("Clear")
        self.open_source_button = QPushButton("Open Source File")
        self.refresh_source_button = QPushButton("Refresh Source Preview")
        self.expand_neighbors_button = QPushButton("Expand Neighbors")
        self.rebuild_graph_button = QPushButton("Rebuild Graph")
        self.export_png_button = QPushButton("Export Graph PNG")
        self.find_in_source_button = QPushButton("Find In Source")
        self.trace_path_button = QPushButton("Trace Path")
        self.build_symbol_graph_button = QPushButton("Build Symbol Graph")

        self.quick_startup_button = QPushButton("Startup")
        self.quick_tabs_button = QPushButton("Tabs")
        self.quick_topomap_button = QPushButton("Topomap")
        self.quick_timeline_button = QPushButton("Timeline")
        self.quick_splash_button = QPushButton("Splash")
        self.quick_reset_button = QPushButton("Reset")

        self.edge_filter_combo = QComboBox()
        self.edge_filter_combo.addItems(["all", "imports only", "calls only", "symbols only"])

        self.graph_level_combo = QComboBox()
        self.graph_level_combo.addItems(["file graph", "symbol graph"])

        self.result_list = QListWidget()
        self.detail_text = QPlainTextEdit()
        self.detail_text.setReadOnly(True)

        self.graph_list = QListWidget()
        self.graph_text = QPlainTextEdit()
        self.graph_text.setReadOnly(True)

        self.symbol_match_list = QListWidget()
        self.symbol_detail_text = QPlainTextEdit()
        self.symbol_detail_text.setReadOnly(True)

        self.source_preview = QPlainTextEdit()
        self.source_preview.setReadOnly(True)
        self.source_path_label = QLabel("Source: -")

        self.graph_canvas = GraphCanvas()
        self.graph_canvas.node_selected.connect(self._graph_node_selected)
        self.graph_canvas.node_double_selected.connect(self._graph_node_double_selected)

        self.log_box = QPlainTextEdit()
        self.log_box.setReadOnly(True)

        self.tabs = QTabWidget()

        self._current_graph_mode = ""
        self._base_graph_mode = ""
        self._current_graph_nodes: list[dict[str, Any]] = []
        self._current_graph_edges: list[dict[str, Any]] = []
        self._isolated_node_id = ""

        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

        load_row = QHBoxLayout()
        load_row.addWidget(QLabel("JSON:"))
        load_row.addWidget(self.json_path_edit)
        load_row.addWidget(self.load_button)

        query_row = QHBoxLayout()
        query_row.addWidget(QLabel("Question:"))
        query_row.addWidget(self.question_edit)
        query_row.addWidget(self.ask_button)
        query_row.addWidget(self.clear_button)

        quick_row = QHBoxLayout()
        quick_row.addWidget(self.quick_startup_button)
        quick_row.addWidget(self.quick_tabs_button)
        quick_row.addWidget(self.quick_topomap_button)
        quick_row.addWidget(self.quick_timeline_button)
        quick_row.addWidget(self.quick_splash_button)
        quick_row.addWidget(self.quick_reset_button)
        quick_row.addStretch()
        quick_row.addWidget(QLabel("Graph level:"))
        quick_row.addWidget(self.graph_level_combo)
        quick_row.addWidget(QLabel("Edge filter:"))
        quick_row.addWidget(self.edge_filter_combo)
        quick_row.addWidget(self.expand_neighbors_button)
        quick_row.addWidget(self.rebuild_graph_button)
        quick_row.addWidget(self.export_png_button)

        source_tools_row = QHBoxLayout()
        source_tools_row.addWidget(QLabel("Find in source:"))
        source_tools_row.addWidget(self.source_search_edit)
        source_tools_row.addWidget(self.find_in_source_button)
        source_tools_row.addStretch()
        source_tools_row.addWidget(self.refresh_source_button)
        source_tools_row.addWidget(self.open_source_button)

        path_tools_row = QHBoxLayout()
        path_tools_row.addWidget(QLabel("Path from:"))
        path_tools_row.addWidget(self.path_from_edit)
        path_tools_row.addWidget(QLabel("to:"))
        path_tools_row.addWidget(self.path_to_edit)
        path_tools_row.addWidget(self.trace_path_button)
        path_tools_row.addWidget(self.build_symbol_graph_button)

        search_page = QWidget()
        search_layout = QVBoxLayout(search_page)
        search_splitter = QSplitter(Qt.Horizontal)
        search_splitter.addWidget(self.result_list)
        search_splitter.addWidget(self.detail_text)
        search_splitter.addWidget(self.source_preview)
        search_splitter.setSizes([340, 540, 900])
        search_layout.addWidget(self.source_path_label)
        search_layout.addLayout(source_tools_row)
        search_layout.addWidget(search_splitter)

        graph_page = QWidget()
        graph_layout = QVBoxLayout(graph_page)

        upper_splitter = QSplitter(Qt.Horizontal)
        upper_splitter.addWidget(self.graph_list)
        upper_splitter.addWidget(self.graph_canvas)
        upper_splitter.setSizes([320, 1060])

        lower_splitter = QSplitter(Qt.Horizontal)
        lower_splitter.addWidget(self.graph_text)
        lower_splitter.addWidget(self.source_preview)
        lower_splitter.setSizes([520, 920])

        graph_layout.addWidget(self.source_path_label)
        graph_layout.addLayout(source_tools_row)
        graph_layout.addLayout(path_tools_row)
        graph_layout.addWidget(upper_splitter, stretch=2)
        graph_layout.addWidget(lower_splitter, stretch=1)

        symbol_page = QWidget()
        symbol_layout = QVBoxLayout(symbol_page)
        symbol_splitter = QSplitter(Qt.Horizontal)
        symbol_splitter.addWidget(self.symbol_match_list)
        symbol_splitter.addWidget(self.symbol_detail_text)
        symbol_splitter.setSizes([420, 980])
        symbol_layout.addWidget(symbol_splitter)

        self.tabs.addTab(search_page, "Search")
        self.tabs.addTab(graph_page, "Graph Views")
        self.tabs.addTab(symbol_page, "Matched Symbols")

        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout(log_group)
        log_layout.addWidget(self.log_box)

        main_layout.addLayout(load_row)
        main_layout.addLayout(query_row)
        main_layout.addLayout(quick_row)
        main_layout.addWidget(self.tabs, stretch=1)
        main_layout.addWidget(log_group, stretch=0)

    def _connect_signals(self) -> None:
        self.load_button.clicked.connect(self.load_json)
        self.ask_button.clicked.connect(self.ask_question)
        self.clear_button.clicked.connect(self.clear_all)
        self.question_edit.returnPressed.connect(self.ask_question)

        self.quick_startup_button.clicked.connect(lambda: self.run_graph_view("startup"))
        self.quick_tabs_button.clicked.connect(lambda: self.run_graph_view("tabs"))
        self.quick_topomap_button.clicked.connect(lambda: self.run_graph_view("topomap"))
        self.quick_timeline_button.clicked.connect(lambda: self.run_graph_view("timeline"))
        self.quick_splash_button.clicked.connect(lambda: self.run_graph_view("splash"))
        self.quick_reset_button.clicked.connect(lambda: self.run_graph_view("reset"))

        self.result_list.currentItemChanged.connect(self._show_result_detail)
        self.graph_list.currentItemChanged.connect(self._show_graph_detail)
        self.symbol_match_list.currentItemChanged.connect(self._show_symbol_detail)

        self.refresh_source_button.clicked.connect(self.refresh_source_preview)
        self.open_source_button.clicked.connect(self.open_selected_source_file)
        self.expand_neighbors_button.clicked.connect(self.expand_current_graph_neighbors)
        self.rebuild_graph_button.clicked.connect(self.rebuild_current_graph)
        self.export_png_button.clicked.connect(self.export_current_graph_png)
        self.find_in_source_button.clicked.connect(self.find_in_source)
        self.source_search_edit.returnPressed.connect(self.find_in_source)
        self.trace_path_button.clicked.connect(self.trace_path_between_nodes)
        self.build_symbol_graph_button.clicked.connect(self.build_symbol_graph_from_inputs)

        self.edge_filter_combo.currentTextChanged.connect(self._apply_edge_filter)
        self.graph_canvas.node_selected.connect(self._graph_node_selected)
        self.graph_canvas.node_double_selected.connect(self._graph_node_double_selected)

    def append_log(self, text: str) -> None:
        self.log_box.appendPlainText(text)

    def clear_all(self) -> None:
        self.result_list.clear()
        self.graph_list.clear()
        self.symbol_match_list.clear()
        self.detail_text.clear()
        self.graph_text.clear()
        self.symbol_detail_text.clear()
        self.source_preview.clear()
        self.graph_canvas.clear_graph()
        self.source_path_label.setText("Source: -")
        self.log_box.clear()
        self._current_graph_mode = ""
        self._base_graph_mode = ""
        self._current_graph_nodes = []
        self._current_graph_edges = []
        self._isolated_node_id = ""

    def load_json(self) -> None:
        current = self.json_path_edit.text().strip()
        start_dir = os.path.dirname(current) if current else os.getcwd()

        file_path, _filter = QFileDialog.getOpenFileName(
            self,
            "Load project_structure_index.json",
            start_dir,
            "JSON Files (*.json)",
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as handle:
                self.index_data = json.load(handle)

            self.json_path_edit.setText(file_path)
            self.project_root = (
                self.index_data.get("project_summary", {}).get("project_root", "") or ""
            )
            self.semantic_roles = self.index_data.get("semantic_roles", {})
            self._rebuild_indexes()

            self.append_log("Loaded JSON: " + file_path)
            self.append_log("Project root: " + self.project_root)

            summary = self.index_data.get("project_summary", {})
            self.append_log("Python files: " + str(summary.get("python_file_count", "unknown")))
            self.append_log("Entry files: " + str(summary.get("entry_file_count", "unknown")))

            QMessageBox.information(self, "Loaded", "JSON loaded successfully.")
        except Exception as exc:
            QMessageBox.critical(self, "Error", "Failed to load JSON:\n" + str(exc))
            self.append_log("ERROR loading JSON: " + str(exc))

    def _rebuild_indexes(self) -> None:
        self.files_by_path.clear()
        self.files_by_module.clear()
        self.symbol_to_file.clear()
        self.symbol_details.clear()
        self.call_graph_out.clear()
        self.import_graph_out.clear()

        if not self.index_data:
            return

        for file_record in self.index_data.get("files", []):
            path = file_record.get("path", "")
            module_name = file_record.get("module_name", "")
            if path:
                self.files_by_path[path] = file_record
            if module_name:
                self.files_by_module[module_name] = file_record

            for fn in file_record.get("functions", []):
                qualname = fn.get("qualname", "")
                if qualname:
                    self.symbol_to_file[qualname].add(path)
                    self.symbol_details[qualname] = {
                        "file": path,
                        "line": int(fn.get("lineno", 1)),
                        "kind": "function",
                        "record": fn,
                    }

            for cls in file_record.get("classes", []):
                cls_name = cls.get("name", "")
                if cls_name:
                    self.symbol_to_file[cls_name].add(path)
                    self.symbol_details[cls_name] = {
                        "file": path,
                        "line": int(cls.get("lineno", 1)),
                        "kind": "class",
                        "record": cls,
                    }
                for method in cls.get("methods", []):
                    qualname = method.get("qualname", "")
                    if qualname:
                        self.symbol_to_file[qualname].add(path)
                        self.symbol_details[qualname] = {
                            "file": path,
                            "line": int(method.get("lineno", 1)),
                            "kind": "method",
                            "record": method,
                        }

        for src_module, targets in self.index_data.get("import_graph", {}).items():
            src_path = self._resolve_module_to_path(src_module) or src_module
            for target in targets:
                self.import_graph_out[src_path].add(target)

        for edge in self.index_data.get("call_edges", []):
            from_file = edge.get("from_file", "")
            to_call = edge.get("to_call", "")
            if from_file and to_call:
                self.call_graph_out[from_file].add(to_call)

    def _resolve_module_to_path(self, module_name: str) -> str | None:
        record = self.files_by_module.get(module_name)
        if record:
            return record.get("path")
        return None

    def ask_question(self) -> None:
        if not self.index_data:
            QMessageBox.warning(self, "No JSON", "Please load a JSON file first.")
            return

        question = self.question_edit.text().strip()
        if not question:
            QMessageBox.warning(self, "No Question", "Please type a question.")
            return

        self.result_list.clear()
        self.detail_text.clear()
        self.symbol_match_list.clear()
        self.symbol_detail_text.clear()
        self.tabs.setCurrentIndex(0)

        results, symbol_matches = self._search(question)

        self.append_log("Question: " + question)
        self.append_log("Search results: " + str(len(results)))
        self.append_log("Matched symbols: " + str(len(symbol_matches)))

        for result in results:
            item = QListWidgetItem(result["title"])
            item.setData(Qt.UserRole, result)
            self.result_list.addItem(item)

        for match in symbol_matches:
            item = QListWidgetItem(match["title"])
            item.setData(Qt.UserRole, match)
            self.symbol_match_list.addItem(item)

        if results:
            self.result_list.setCurrentRow(0)
        if symbol_matches:
            self.symbol_match_list.setCurrentRow(0)

    def _search(self, question: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        q = norm_text(question)
        tokens = tokenize_query(q)
        entry_files = set(self.index_data.get("entry_files", []))

        scored_files: list[dict[str, Any]] = []
        scored_symbols: list[dict[str, Any]] = []

        for path, file_record in self.files_by_path.items():
            module_name = file_record.get("module_name", "")
            docstring = file_record.get("docstring", "")
            strings = " ".join(file_record.get("strings", []))
            comments = " ".join(file_record.get("comments", []))
            ui_hits = " ".join(file_record.get("ui_keyword_hits", []))
            eeg_hits = " ".join(file_record.get("eeg_keyword_hits", []))
            semantic_hints = " ".join(file_record.get("semantic_hints", []))
            entry_markers = " ".join(file_record.get("entry_markers", []))

            function_names = []
            call_names = []
            class_names = []

            for fn in file_record.get("functions", []):
                function_names.append(fn.get("name", ""))
                function_names.append(fn.get("qualname", ""))
                for call in fn.get("calls", []):
                    call_names.append(call.get("call_name", ""))

            for cls in file_record.get("classes", []):
                class_names.append(cls.get("name", ""))
                for method in cls.get("methods", []):
                    function_names.append(method.get("name", ""))
                    function_names.append(method.get("qualname", ""))
                    for call in method.get("calls", []):
                        call_names.append(call.get("call_name", ""))

            haystack = " ".join([
                norm_text(path),
                norm_text(module_name),
                norm_text(docstring),
                norm_text(strings),
                norm_text(comments),
                norm_text(ui_hits),
                norm_text(eeg_hits),
                norm_text(semantic_hints),
                norm_text(entry_markers),
                norm_text(" ".join(function_names)),
                norm_text(" ".join(call_names)),
                norm_text(" ".join(class_names)),
            ])

            roles = self.semantic_roles.get(path, {}).get("roles", [])
            score = 0
            reasons = []

            for token in tokens:
                if token in haystack:
                    score += 3
                    reasons.append("token match: " + token)

            if path in entry_files and ("start" in q or "main" in q or "entry" in q or "launch" in q):
                score += 20
                reasons.append("entry file")

            if "topomap" in q and ("topomap" in haystack or "amplitude_map" in haystack or "topomap" in roles):
                score += 18
                reasons.append("topomap match")

            if "tab" in q and ("addtab" in haystack or "notebook" in haystack or "tabs" in roles):
                score += 15
                reasons.append("tab match")

            if "timeline" in q and ("timeline" in haystack or "timeline" in roles):
                score += 15
                reasons.append("timeline match")

            if "splash" in q and ("splash" in haystack or "splash" in roles):
                score += 15
                reasons.append("splash match")

            if ("reset" in q or "snapshot" in q) and (
                "reset" in haystack or "snapshot" in haystack or "state_reset" in roles
            ):
                score += 15
                reasons.append("reset or snapshot match")

            if score > 0:
                best_line = self._best_line_for_file(file_record, q)
                scored_files.append(
                    {
                        "score": score,
                        "title": "[" + str(score) + "] " + path + " | " + module_name,
                        "detail": self._build_file_detail(path, reasons),
                        "path": path,
                        "line": best_line,
                    }
                )

        for symbol_name, detail in self.symbol_details.items():
            blob = norm_text(symbol_name)
            record = detail["record"]
            docstring = norm_text(record.get("docstring", ""))
            calls_blob = ""

            if detail["kind"] in ("function", "method"):
                calls_blob = norm_text(" ".join([c.get("call_name", "") for c in record.get("calls", [])]))

            haystack = " ".join([blob, docstring, calls_blob])

            score = 0
            reasons = []
            for token in tokens:
                if token in haystack:
                    score += 4
                    reasons.append("symbol token match: " + token)

            if score > 0:
                path = detail["file"]
                line = detail["line"]
                scored_symbols.append(
                    {
                        "score": score,
                        "title": "[" + str(score) + "] " + symbol_name + " | " + path + ":" + str(line),
                        "detail": self._build_symbol_detail(symbol_name),
                        "path": path,
                        "line": line,
                        "symbol": symbol_name,
                    }
                )

        scored_files.sort(key=lambda item: (-item["score"], item["path"]))
        scored_symbols.sort(key=lambda item: (-item["score"], item["symbol"]))

        return scored_files[:50], scored_symbols[:80]

    def _best_line_for_file(self, file_record: dict[str, Any], question: str) -> int:
        q = norm_text(question)

        for fn in file_record.get("functions", []):
            if norm_text(fn.get("qualname", "")) in q or norm_text(fn.get("name", "")) in q:
                return int(fn.get("lineno", 1))

        for cls in file_record.get("classes", []):
            if norm_text(cls.get("name", "")) in q:
                return int(cls.get("lineno", 1))
            for method in cls.get("methods", []):
                if norm_text(method.get("qualname", "")) in q or norm_text(method.get("name", "")) in q:
                    return int(method.get("lineno", 1))

        if file_record.get("functions"):
            return int(file_record["functions"][0].get("lineno", 1))
        if file_record.get("classes"):
            return int(file_record["classes"][0].get("lineno", 1))
        return 1

    def _build_file_detail(self, path: str, reasons: list[str]) -> str:
        file_record = self.files_by_path[path]
        roles = self.semantic_roles.get(path, {}).get("roles", [])

        lines = []
        lines.append("FILE")
        lines.append(path)
        lines.append("")
        lines.append("MODULE")
        lines.append(file_record.get("module_name", ""))
        lines.append("")
        lines.append("WHY THIS MATCHED")
        for reason in sorted(set(reasons)):
            lines.append("- " + reason)

        lines.append("")
        lines.append("ROLES")
        if roles:
            for role in roles:
                lines.append("- " + role)
        else:
            lines.append("- none")

        if file_record.get("entry_markers"):
            lines.append("")
            lines.append("ENTRY MARKERS")
            for marker in file_record["entry_markers"]:
                lines.append("- " + marker)

        if file_record.get("docstring"):
            lines.append("")
            lines.append("DOCSTRING")
            lines.append(file_record["docstring"])

        if file_record.get("functions"):
            lines.append("")
            lines.append("FUNCTIONS")
            for fn in file_record["functions"][:40]:
                lines.append("- " + fn.get("qualname", "") + " (line " + str(fn.get("lineno", "")) + ")")

        if file_record.get("classes"):
            lines.append("")
            lines.append("CLASSES")
            for cls in file_record["classes"][:30]:
                line = "- " + cls.get("name", "") + " (line " + str(cls.get("lineno", "")) + ")"
                bases = cls.get("bases", [])
                if bases:
                    line += " bases: " + ", ".join(bases)
                lines.append(line)
                for method in cls.get("methods", [])[:15]:
                    lines.append("    * " + method.get("qualname", "") + " (line " + str(method.get("lineno", "")) + ")")

        imports_out = sorted(self.import_graph_out.get(path, []))
        if imports_out:
            lines.append("")
            lines.append("IMPORTS OUT")
            for item in imports_out[:50]:
                lines.append("- " + item)

        calls_out = sorted(self.call_graph_out.get(path, []))
        if calls_out:
            lines.append("")
            lines.append("CALLS OUT")
            for item in calls_out[:80]:
                lines.append("- " + item)

        return "\n".join(lines)

    def _build_symbol_detail(self, symbol_name: str) -> str:
        detail = self.symbol_details[symbol_name]
        path = detail["file"]
        line = detail["line"]
        kind = detail["kind"]
        record = detail["record"]

        lines = []
        lines.append("SYMBOL")
        lines.append(symbol_name)
        lines.append("")
        lines.append("KIND")
        lines.append(kind)
        lines.append("")
        lines.append("FILE")
        lines.append(path + ":" + str(line))
        lines.append("")

        if record.get("docstring"):
            lines.append("DOCSTRING")
            lines.append(record.get("docstring", ""))
            lines.append("")

        if kind in ("function", "method"):
            lines.append("CALLS")
            for call in record.get("calls", [])[:80]:
                lines.append("- " + call.get("call_name", ""))
            lines.append("")

        lines.append("POSSIBLE FILE TARGETS")
        for target_path in sorted(self.symbol_to_file.get(symbol_name, [])):
            lines.append("- " + target_path)

        return "\n".join(lines)

    def _show_result_detail(self, current: QListWidgetItem, previous: QListWidgetItem) -> None:
        _ = previous
        if not current:
            self.detail_text.clear()
            return

        payload = current.data(Qt.UserRole)
        if not payload:
            return

        self.detail_text.setPlainText(payload.get("detail", ""))
        self._load_source_preview(payload.get("path", ""), int(payload.get("line", 1)))

    def _show_symbol_detail(self, current: QListWidgetItem, previous: QListWidgetItem) -> None:
        _ = previous
        if not current:
            self.symbol_detail_text.clear()
            return

        payload = current.data(Qt.UserRole)
        if not payload:
            return

        self.symbol_detail_text.setPlainText(payload.get("detail", ""))
        self._load_source_preview(payload.get("path", ""), int(payload.get("line", 1)))

    def run_graph_view(self, mode: str) -> None:
        if not self.index_data:
            QMessageBox.warning(self, "No JSON", "Please load a JSON file first.")
            return

        if self.graph_level_combo.currentText() == "symbol graph":
            self.build_symbol_graph_for_mode(mode)
            return

        self.graph_list.clear()
        self.graph_text.clear()
        self.graph_canvas.clear_graph()
        self.tabs.setCurrentIndex(1)

        self._current_graph_mode = mode
        self._base_graph_mode = mode
        self._isolated_node_id = ""

        nodes, edges = self._collect_file_graph_nodes_and_edges(mode)
        self._current_graph_nodes = nodes
        self._current_graph_edges = edges

        self._repaint_graph_view()

        self.append_log("Graph view: " + mode)
        self.append_log("Graph nodes: " + str(len(nodes)))
        self.append_log("Graph edges: " + str(len(edges)))

    def _collect_file_graph_nodes_and_edges(self, mode: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        entry_files = set(self.index_data.get("entry_files", []))
        nodes = []
        edges: list[dict[str, Any]] = []
        selected_paths = []

        for path, file_record in self.files_by_path.items():
            roles = self.semantic_roles.get(path, {}).get("roles", [])
            title = path + " | " + file_record.get("module_name", "")
            text = self._all_text(path)

            matched = False
            reasons = []

            if mode == "startup":
                if path in entry_files or "startup" in roles or "main_window" in roles:
                    matched = True
                    reasons.append("startup related")
            elif mode == "tabs":
                if "tabs" in roles or "notebook" in text or "addtab" in text:
                    matched = True
                    reasons.append("tab related")
            elif mode == "topomap":
                if "topomap" in roles or "topomap" in text or "amplitude_map" in text:
                    matched = True
                    reasons.append("topomap related")
            elif mode == "timeline":
                if "timeline" in roles or "timeline" in text:
                    matched = True
                    reasons.append("timeline related")
            elif mode == "splash":
                if "splash" in roles or "splash" in text:
                    matched = True
                    reasons.append("splash related")
            elif mode == "reset":
                if "state_reset" in roles or "reset" in text or "snapshot" in text:
                    matched = True
                    reasons.append("reset or snapshot related")

            if matched:
                selected_paths.append(path)
                best_line = self._best_line_for_graph_mode(file_record, mode)
                nodes.append(
                    {
                        "id": path,
                        "title": title,
                        "label": shorten_path(path),
                        "detail": self._build_graph_detail(path, reasons),
                        "path": path,
                        "line": best_line,
                        "roles": roles,
                    }
                )

        selected_path_set = set(selected_paths)

        for path in selected_paths:
            for imported in self.import_graph_out.get(path, set()):
                resolved = self._resolve_module_to_path(imported)
                if resolved and resolved in selected_path_set:
                    edges.append({"source": path, "target": resolved, "type": "import"})

            for call_name in self.call_graph_out.get(path, set()):
                for candidate_path, candidate_record in self.files_by_path.items():
                    if candidate_path == path:
                        continue
                    if candidate_path not in selected_path_set:
                        continue
                    if self._file_contains_symbol(candidate_record, call_name):
                        edges.append({"source": path, "target": candidate_path, "type": "call"})

        return nodes[:90], dedupe_edge_dicts(edges)[:260]

    def build_symbol_graph_for_mode(self, mode: str) -> None:
        if not self.index_data:
            return

        self.graph_list.clear()
        self.graph_text.clear()
        self.graph_canvas.clear_graph()
        self.tabs.setCurrentIndex(1)

        self._current_graph_mode = "symbol:" + mode
        self._base_graph_mode = "symbol:" + mode
        self._isolated_node_id = ""

        nodes, edges = self._collect_symbol_graph_nodes_and_edges(mode)
        self._current_graph_nodes = nodes
        self._current_graph_edges = edges

        self._repaint_graph_view()

        self.append_log("Symbol graph view: " + mode)
        self.append_log("Symbol nodes: " + str(len(nodes)))
        self.append_log("Symbol edges: " + str(len(edges)))

    def _collect_symbol_graph_nodes_and_edges(self, mode: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        file_nodes, _file_edges = self._collect_file_graph_nodes_and_edges(mode)
        selected_paths = {node["path"] for node in file_nodes}

        symbol_nodes = []
        symbol_edges = []

        selected_symbols = set()

        for path in selected_paths:
            file_record = self.files_by_path[path]

            for fn in file_record.get("functions", []):
                symbol_name = fn.get("qualname", "")
                if symbol_name:
                    selected_symbols.add(symbol_name)
                    symbol_nodes.append(
                        {
                            "id": symbol_name,
                            "title": symbol_name + " | " + path,
                            "label": shorten_symbol(symbol_name),
                            "detail": self._build_symbol_detail(symbol_name),
                            "path": path,
                            "line": int(fn.get("lineno", 1)),
                            "roles": self.semantic_roles.get(path, {}).get("roles", []),
                        }
                    )
                    for call in fn.get("calls", []):
                        target_symbol = call.get("call_name", "")
                        if target_symbol:
                            symbol_edges.append(
                                {
                                    "source": symbol_name,
                                    "target": target_symbol,
                                    "type": "symbol",
                                }
                            )

            for cls in file_record.get("classes", []):
                for method in cls.get("methods", []):
                    symbol_name = method.get("qualname", "")
                    if symbol_name:
                        selected_symbols.add(symbol_name)
                        symbol_nodes.append(
                            {
                                "id": symbol_name,
                                "title": symbol_name + " | " + path,
                                "label": shorten_symbol(symbol_name),
                                "detail": self._build_symbol_detail(symbol_name),
                                "path": path,
                                "line": int(method.get("lineno", 1)),
                                "roles": self.semantic_roles.get(path, {}).get("roles", []),
                            }
                        )
                        for call in method.get("calls", []):
                            target_symbol = call.get("call_name", "")
                            if target_symbol:
                                symbol_edges.append(
                                    {
                                        "source": symbol_name,
                                        "target": target_symbol,
                                        "type": "symbol",
                                    }
                                )

        available_nodes = {node["id"] for node in symbol_nodes}
        symbol_edges = [
            edge
            for edge in symbol_edges
            if edge["source"] in available_nodes and edge["target"] in available_nodes
        ]

        symbol_nodes.sort(key=lambda item: item["id"])
        return symbol_nodes[:140], dedupe_edge_dicts(symbol_edges)[:400]

    def _best_line_for_graph_mode(self, file_record: dict[str, Any], mode: str) -> int:
        keywords_by_mode = {
            "startup": ["QApplication", "app.exec", "create_main_window", "display_pyside6_eeg_visualizer"],
            "tabs": ["addTab", "Notebook", "Tab", "TopInTabBar"],
            "topomap": ["topomap", "amplitude_map", "plot_topomap"],
            "timeline": ["timeline", "TimelineManager", "TimelineWidget"],
            "splash": ["splash", "SplashManager", "KandaSplashImageText"],
            "reset": ["reset", "snapshot", "reset_to_initial_eeg_state", "capture_initial_eeg_state"],
        }

        wanted = [norm_text(x) for x in keywords_by_mode.get(mode, [])]

        for fn in file_record.get("functions", []):
            blob = norm_text(fn.get("qualname", "") + " " + fn.get("name", ""))
            for item in wanted:
                if item in blob:
                    return int(fn.get("lineno", 1))

        for cls in file_record.get("classes", []):
            blob = norm_text(cls.get("name", ""))
            for item in wanted:
                if item in blob:
                    return int(cls.get("lineno", 1))
            for method in cls.get("methods", []):
                blob2 = norm_text(method.get("qualname", "") + " " + method.get("name", ""))
                for item in wanted:
                    if item in blob2:
                        return int(method.get("lineno", 1))

        return 1

    def _all_text(self, path: str) -> str:
        file_record = self.files_by_path[path]
        parts = [
            path,
            file_record.get("module_name", ""),
            file_record.get("docstring", ""),
            " ".join(file_record.get("strings", [])),
            " ".join(file_record.get("comments", [])),
            " ".join(file_record.get("entry_markers", [])),
            " ".join(file_record.get("ui_keyword_hits", [])),
            " ".join(file_record.get("eeg_keyword_hits", [])),
            " ".join(file_record.get("semantic_hints", [])),
        ]

        for fn in file_record.get("functions", []):
            parts.append(fn.get("qualname", ""))
            for call in fn.get("calls", []):
                parts.append(call.get("call_name", ""))

        for cls in file_record.get("classes", []):
            parts.append(cls.get("name", ""))
            for method in cls.get("methods", []):
                parts.append(method.get("qualname", ""))
                for call in method.get("calls", []):
                    parts.append(call.get("call_name", ""))

        return norm_text(" ".join(parts))

    def _build_graph_detail(self, path: str, reasons: list[str]) -> str:
        file_record = self.files_by_path[path]
        roles = self.semantic_roles.get(path, {}).get("roles", [])

        lines = []
        lines.append("NODE")
        lines.append(path)
        lines.append("")
        lines.append("WHY INCLUDED")
        for reason in reasons:
            lines.append("- " + reason)

        lines.append("")
        lines.append("ROLES")
        if roles:
            for role in roles:
                lines.append("- " + role)
        else:
            lines.append("- none")

        lines.append("")
        lines.append("OUTGOING IMPORTS")
        imports_out = sorted(self.import_graph_out.get(path, []))
        if imports_out:
            for item in imports_out[:50]:
                lines.append("- " + item)
        else:
            lines.append("- none")

        lines.append("")
        lines.append("OUTGOING CALLS")
        calls_out = sorted(self.call_graph_out.get(path, []))
        if calls_out:
            for item in calls_out[:80]:
                lines.append("- " + item)
        else:
            lines.append("- none")

        lines.append("")
        lines.append("FILE SUMMARY")
        lines.append(self._build_file_detail(path, reasons))

        return "\n".join(lines)

    def _show_graph_detail(self, current: QListWidgetItem, previous: QListWidgetItem) -> None:
        _ = previous
        if not current:
            self.graph_text.clear()
            return

        payload = current.data(Qt.UserRole)
        if not payload:
            return

        self.graph_text.setPlainText(payload.get("detail", ""))
        self._load_source_preview(payload.get("path", ""), int(payload.get("line", 1)))

    def _graph_node_selected(self, node_id: str) -> None:
        for row in range(self.graph_list.count()):
            item = self.graph_list.item(row)
            payload = item.data(Qt.UserRole)
            if payload and payload.get("id") == node_id:
                self.graph_list.setCurrentRow(row)
                self.graph_text.setPlainText(payload.get("detail", ""))
                self._load_source_preview(payload.get("path", ""), int(payload.get("line", 1)))
                break

    def _graph_node_double_selected(self, node_id: str) -> None:
        self.isolate_subgraph(node_id)

    def isolate_subgraph(self, center_id: str) -> None:
        if not center_id:
            return

        node_map = {node["id"]: node for node in self._current_graph_nodes}
        if center_id not in node_map:
            return

        connected = {center_id}
        for edge in self._current_graph_edges:
            if edge["source"] == center_id:
                connected.add(edge["target"])
            if edge["target"] == center_id:
                connected.add(edge["source"])

        isolated_nodes = [node_map[node_id] for node_id in connected if node_id in node_map]
        isolated_edges = [
            edge
            for edge in self._current_graph_edges
            if edge["source"] in connected and edge["target"] in connected
        ]

        self._isolated_node_id = center_id
        self._draw_graph_and_list(isolated_nodes, isolated_edges)
        self.append_log("Isolated subgraph around: " + center_id)

    def expand_current_graph_neighbors(self) -> None:
        if not self._current_graph_nodes:
            QMessageBox.information(self, "No Graph", "Build a graph view first.")
            return

        current_item = self.graph_list.currentItem()
        if not current_item:
            QMessageBox.information(self, "No Selection", "Select a graph node first.")
            return

        payload = current_item.data(Qt.UserRole)
        if not payload:
            return

        base_id = payload.get("id", "")
        if not base_id:
            return

        if self.graph_level_combo.currentText() == "symbol graph":
            self._expand_symbol_neighbors(base_id)
        else:
            self._expand_file_neighbors(base_id)

    def _expand_file_neighbors(self, base_path: str) -> None:
        neighbor_paths = self._infer_neighbor_files(base_path)
        existing = {node["id"] for node in self._current_graph_nodes}
        node_map = {node["id"]: node for node in self._current_graph_nodes}
        edge_map = {(edge["source"], edge["target"], edge["type"]): edge for edge in self._current_graph_edges}

        for neighbor_path in neighbor_paths[:20]:
            if neighbor_path not in self.files_by_path:
                continue

            if neighbor_path not in existing:
                roles = self.semantic_roles.get(neighbor_path, {}).get("roles", [])
                rec = self.files_by_path[neighbor_path]
                node_map[neighbor_path] = {
                    "id": neighbor_path,
                    "title": neighbor_path + " | " + rec.get("module_name", ""),
                    "label": shorten_path(neighbor_path),
                    "detail": self._build_graph_detail(neighbor_path, ["expanded neighbor"]),
                    "path": neighbor_path,
                    "line": 1,
                    "roles": roles,
                }
                existing.add(neighbor_path)

            edge_map[(base_path, neighbor_path, "call")] = {
                "source": base_path,
                "target": neighbor_path,
                "type": "call",
            }

        self._current_graph_nodes = sorted(node_map.values(), key=lambda item: item["id"])
        self._current_graph_edges = sorted(edge_map.values(), key=lambda item: (item["source"], item["target"], item["type"]))
        self._repaint_graph_view()
        self.append_log("Expanded file neighbors for: " + base_path)

    def _expand_symbol_neighbors(self, base_symbol: str) -> None:
        existing = {node["id"] for node in self._current_graph_nodes}
        node_map = {node["id"]: node for node in self._current_graph_nodes}
        edge_map = {(edge["source"], edge["target"], edge["type"]): edge for edge in self._current_graph_edges}

        detail = self.symbol_details.get(base_symbol)
        if not detail:
            return

        record = detail["record"]
        for call in record.get("calls", [])[:40]:
            target_symbol = call.get("call_name", "")
            if not target_symbol:
                continue

            if target_symbol in self.symbol_details and target_symbol not in existing:
                t_detail = self.symbol_details[target_symbol]
                t_path = t_detail["file"]
                node_map[target_symbol] = {
                    "id": target_symbol,
                    "title": target_symbol + " | " + t_path,
                    "label": shorten_symbol(target_symbol),
                    "detail": self._build_symbol_detail(target_symbol),
                    "path": t_path,
                    "line": t_detail["line"],
                    "roles": self.semantic_roles.get(t_path, {}).get("roles", []),
                }
                existing.add(target_symbol)

            if target_symbol in self.symbol_details:
                edge_map[(base_symbol, target_symbol, "symbol")] = {
                    "source": base_symbol,
                    "target": target_symbol,
                    "type": "symbol",
                }

        self._current_graph_nodes = sorted(node_map.values(), key=lambda item: item["id"])
        self._current_graph_edges = sorted(edge_map.values(), key=lambda item: (item["source"], item["target"], item["type"]))
        self._repaint_graph_view()
        self.append_log("Expanded symbol neighbors for: " + base_symbol)

    def rebuild_current_graph(self) -> None:
        if not self._base_graph_mode:
            QMessageBox.information(self, "No Graph", "Build a graph view first.")
            return

        if self._base_graph_mode.startswith("symbol:"):
            self.build_symbol_graph_for_mode(self._base_graph_mode.split(":", 1)[1])
        else:
            self.run_graph_view(self._base_graph_mode)

    def export_current_graph_png(self) -> None:
        if not self._current_graph_nodes:
            QMessageBox.information(self, "No Graph", "Build a graph view first.")
            return

        output_path, _filter = QFileDialog.getSaveFileName(
            self,
            "Export Graph PNG",
            os.path.join(os.getcwd(), "project_graph.png"),
            "PNG Files (*.png)",
        )
        if not output_path:
            return

        if not output_path.lower().endswith(".png"):
            output_path += ".png"

        try:
            self.graph_canvas.export_png(output_path)
            self.append_log("Graph exported to: " + output_path)
            QMessageBox.information(self, "Exported", "Graph exported successfully.")
        except Exception as exc:
            QMessageBox.critical(self, "Error", "Failed to export PNG:\n" + str(exc))

    def trace_path_between_nodes(self) -> None:
        source_id = self.path_from_edit.text().strip()
        target_id = self.path_to_edit.text().strip()

        if not source_id or not target_id:
            QMessageBox.information(self, "Missing Input", "Fill both 'from' and 'to'.")
            return

        path = self._bfs_trace(source_id, target_id)
        if not path:
            QMessageBox.information(self, "No Path", "No path found between the given nodes.")
            return

        lines = ["TRACE PATH"]
        for step in path:
            lines.append("- " + step)

        self.graph_text.setPlainText("\n".join(lines))
        self.tabs.setCurrentIndex(1)
        self.append_log("Path traced from " + source_id + " to " + target_id)

    def _bfs_trace(self, source_id: str, target_id: str) -> list[str]:
        adjacency: dict[str, set[str]] = defaultdict(set)
        for edge in self._filtered_edges():
            adjacency[edge["source"]].add(edge["target"])

        queue = deque([(source_id, [source_id])])
        visited = {source_id}

        while queue:
            current, path = queue.popleft()
            if current == target_id:
                return path

            for neighbor in adjacency.get(current, set()):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return []

    def build_symbol_graph_from_inputs(self) -> None:
        source_symbol = self.path_from_edit.text().strip()
        if not source_symbol:
            QMessageBox.information(self, "Missing Symbol", "Type a symbol in 'Path from' to build a local symbol graph.")
            return

        if source_symbol not in self.symbol_details:
            QMessageBox.warning(self, "Unknown Symbol", "Symbol not found in indexed data.")
            return

        node_map = {}
        edge_map = {}

        self._add_symbol_node(node_map, source_symbol)

        detail = self.symbol_details[source_symbol]
        record = detail["record"]

        for call in record.get("calls", [])[:50]:
            target_symbol = call.get("call_name", "")
            if target_symbol in self.symbol_details:
                self._add_symbol_node(node_map, target_symbol)
                edge_map[(source_symbol, target_symbol, "symbol")] = {
                    "source": source_symbol,
                    "target": target_symbol,
                    "type": "symbol",
                }

        self._current_graph_nodes = sorted(node_map.values(), key=lambda item: item["id"])
        self._current_graph_edges = sorted(edge_map.values(), key=lambda item: (item["source"], item["target"], item["type"]))
        self._current_graph_mode = "symbol:manual"
        self._base_graph_mode = "symbol:manual"
        self._repaint_graph_view()
        self.tabs.setCurrentIndex(1)
        self.append_log("Built local symbol graph for: " + source_symbol)

    def _add_symbol_node(self, node_map: dict[str, dict[str, Any]], symbol_name: str) -> None:
        if symbol_name in node_map:
            return
        detail = self.symbol_details[symbol_name]
        path = detail["file"]
        node_map[symbol_name] = {
            "id": symbol_name,
            "title": symbol_name + " | " + path,
            "label": shorten_symbol(symbol_name),
            "detail": self._build_symbol_detail(symbol_name),
            "path": path,
            "line": detail["line"],
            "roles": self.semantic_roles.get(path, {}).get("roles", []),
        }

    def _apply_edge_filter(self) -> None:
        if not self._current_graph_nodes:
            return
        self._draw_graph_and_list(self._current_graph_nodes, self._filtered_edges())

    def _filtered_edges(self) -> list[dict[str, Any]]:
        mode = self.edge_filter_combo.currentText()
        if mode == "all":
            return list(self._current_graph_edges)
        if mode == "imports only":
            return [edge for edge in self._current_graph_edges if edge["type"] == "import"]
        if mode == "calls only":
            return [edge for edge in self._current_graph_edges if edge["type"] == "call"]
        if mode == "symbols only":
            return [edge for edge in self._current_graph_edges if edge["type"] == "symbol"]
        return list(self._current_graph_edges)

    def _draw_graph_and_list(self, nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> None:
        self.graph_canvas.build_graph(nodes, edges)
        self.graph_list.clear()
        for node in nodes:
            item = QListWidgetItem(node["title"])
            item.setData(Qt.UserRole, node)
            self.graph_list.addItem(item)
        if nodes:
            self.graph_list.setCurrentRow(0)

    def _repaint_graph_view(self) -> None:
        self._draw_graph_and_list(self._current_graph_nodes, self._filtered_edges())

    def _infer_neighbor_files(self, path: str) -> list[str]:
        neighbors = set()

        for module_target in self.import_graph_out.get(path, set()):
            resolved = self._resolve_module_to_path(module_target)
            if resolved:
                neighbors.add(resolved)

        for call_name in self.call_graph_out.get(path, set()):
            for file_path, file_record in self.files_by_path.items():
                if self._file_contains_symbol(file_record, call_name):
                    neighbors.add(file_path)

        return sorted(neighbors)

    def _file_contains_symbol(self, file_record: dict[str, Any], symbol_name: str) -> bool:
        for fn in file_record.get("functions", []):
            if fn.get("name") == symbol_name or fn.get("qualname") == symbol_name:
                return True
        for cls in file_record.get("classes", []):
            if cls.get("name") == symbol_name:
                return True
            for method in cls.get("methods", []):
                if method.get("name") == symbol_name or method.get("qualname") == symbol_name:
                    return True
        return False

    def _absolute_source_path(self, relative_path: str) -> str:
        if not self.project_root:
            return ""
        return os.path.normpath(os.path.join(self.project_root, relative_path))

    def _load_source_preview(self, relative_path: str, line_number: int) -> None:
        abs_path = self._absolute_source_path(relative_path)
        self.source_path_label.setText("Source: " + abs_path if abs_path else "Source: -")

        if not abs_path or not os.path.exists(abs_path):
            self.source_preview.setPlainText("Source file not found:\n" + abs_path)
            return

        try:
            source = safe_read_text(abs_path)
        except Exception as exc:
            self.source_preview.setPlainText("Failed to read source:\n" + str(exc))
            return

        numbered = []
        for idx, line in enumerate(source.splitlines(), start=1):
            numbered.append(str(idx).rjust(5) + " | " + line)

        self.source_preview.setPlainText("\n".join(numbered))
        self._scroll_preview_to_line(line_number)
        self.append_log("Preview loaded: " + relative_path + " @ line " + str(line_number))

    def _scroll_preview_to_line(self, line_number: int) -> None:
        if line_number < 1:
            line_number = 1

        block = self.source_preview.document().findBlockByLineNumber(line_number - 1)
        if not block.isValid():
            return

        cursor = QTextCursor(block)
        self.source_preview.setTextCursor(cursor)
        self.source_preview.centerCursor()

    def refresh_source_preview(self) -> None:
        payload = self._current_payload()
        if not payload:
            QMessageBox.information(self, "No Selection", "Select a result first.")
            return
        self._load_source_preview(payload.get("path", ""), int(payload.get("line", 1)))

    def open_selected_source_file(self) -> None:
        payload = self._current_payload()
        if not payload:
            QMessageBox.information(self, "No Selection", "Select a result first.")
            return

        relative_path = payload.get("path", "")
        line_number = int(payload.get("line", 1))
        abs_path = self._absolute_source_path(relative_path)

        if not abs_path or not os.path.exists(abs_path):
            QMessageBox.warning(self, "File Not Found", "Source file not found:\n" + abs_path)
            return

        self._load_source_preview(relative_path, line_number)

        QMessageBox.information(
            self,
            "Source Opened In Preview",
            "Loaded source preview for:\n"
            + abs_path
            + "\n\nApproximate line: "
            + str(line_number),
        )

    def find_in_source(self) -> None:
        query = self.source_search_edit.text().strip()
        if not query:
            QMessageBox.information(self, "No Search Text", "Type text to search in source preview.")
            return

        found = self.source_preview.find(query)
        if not found:
            cursor = self.source_preview.textCursor()
            cursor.movePosition(QTextCursor.Start)
            self.source_preview.setTextCursor(cursor)
            found = self.source_preview.find(query)

        if not found:
            QMessageBox.information(self, "Not Found", "Text not found in source preview.")
        else:
            self.append_log("Found in source: " + query)

    def _current_payload(self) -> dict[str, Any] | None:
        current_tab = self.tabs.currentIndex()

        if current_tab == 0:
            item = self.result_list.currentItem()
        elif current_tab == 1:
            item = self.graph_list.currentItem()
        else:
            item = self.symbol_match_list.currentItem()

        if not item:
            return None

        payload = item.data(Qt.UserRole)
        if not isinstance(payload, dict):
            return None

        return payload


def main() -> None:
    app = QApplication(sys.argv)
    window = ProjectJsonExplorerV6()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

What version 6 adds:
symbol-level graph mode
matched symbols tab
exact symbol detail panel
path tracing between two nodes
edge filtering
manual local symbol graph from a chosen symbol

Most valuable uses now:
set graph level to symbol graph
click Topomap or Timeline
inspect exact methods and calls instead of only files

Best next step would be version 7 with:
graph node search box
multi-hop path highlighting on the canvas
separate file and symbol source previews
clickable edge inspection
save/load graph sessions

make a version7 that  makes my local Ai read json and answer complex  questions about the app


"""
pykanda_ai/connectors/qwen_model_wrapper.py
------------------------------------------------------------
FINAL PRODUCTION WRAPPER

Features:
- Async queue (no GUI freeze)
- Streaming tokens
- Disk cache (persistent)
- Auto model switching (fast/smart)
- No QThread
- Stable with Ollama

Notes:
- Canonical governance and cache paths are injected by orchestration
- Package-relative governance fallback exists only for runtime safety
------------------------------------------------------------
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, Dict

import requests

from pykanda_ai.cortex.governance_state_reader import GovernanceStateReader
from pykanda_ai.runtime.ai_disk_cache import AIDiskCache
from pykanda_ai.runtime.ai_request_queue import AIRequestQueue


# =========================================================
# Config
# =========================================================
OLLAMA_URL = "http://127.0.0.1:11434/v1/chat/completions"

FAST_MODEL = "qwen2.5-coder:7b"
SMART_MODEL = "qwen2.5-coder:32b"

AUTO_THRESHOLD = 3000
TIMEOUT = 600


# =========================================================
# Wrapper
# =========================================================
class QwenModelWrapper:
    """
    Production-ready AI wrapper.

    Capabilities:
    - queue serialized GPU usage
    - streaming tokens
    - persistent disk cache
    - automatic model selection
    - snippet-only explanation
    """

    def __init__(self) -> None:
        self._governance_state_path = (
            Path(__file__).resolve().parent.parent
            / "runtime"
            / "governance_state.json"
        )

    def set_cache_dir(self, cache_dir: Path) -> None:
        AIDiskCache().set_cache_dir(Path(cache_dir).expanduser().resolve())

    def set_governance_state_path(self, state_path: Path) -> None:
        self._governance_state_path = Path(state_path).expanduser().resolve()

    def _get_cache(self) -> AIDiskCache:
        return AIDiskCache()

    # =========================================================
    # Governance Mode Modifier
    # =========================================================
    def _get_governance_modifier(self) -> str:
        state_reader = GovernanceStateReader(self._governance_state_path)
        mode = state_reader.get_mode()

        if mode == 0:
            return (
                "Operate normally. Prefer clarity and modularity. "
                "Allow reasonable refactoring."
            )

        if mode == 1:
            return (
                "Operate under elevated architectural caution. "
                "Avoid speculative refactors. "
                "Prioritize safety and stability."
            )

        if mode == 2:
            return (
                "SYSTEM IS IN FREEZE MODE. "
                "Do NOT propose structural changes. "
                "Only analyze and explain. "
                "No refactoring or architectural modification."
            )

        return ""

    # =========================================================
    # Generic Chat (Cortex primitive)
    # =========================================================
    def chat(
        self,
        messages: list[dict[str, Any]],
        *,
        model: str | None = None,
        temperature: float = 0.2,
        max_tokens: int | None = None,
    ) -> str:
        """
        Minimal synchronous chat endpoint.

        Used by Cortex for dynamic reasoning.
        No cache.
        No memory append.
        No RAG.
        Pure transport layer.
        """

        model_to_use = model or FAST_MODEL
        modifier = self._get_governance_modifier()

        prepared_messages = [dict(message) for message in messages]

        if prepared_messages and prepared_messages[0].get("role") == "system":
            original_content = prepared_messages[0].get("content", "")
            prepared_messages[0]["content"] = f"{original_content}\n\n{modifier}"
        else:
            prepared_messages.insert(
                0,
                {
                    "role": "system",
                    "content": modifier,
                },
            )

        payload: Dict[str, Any] = {
            "model": model_to_use,
            "messages": prepared_messages,
            "options": {
                "temperature": temperature,
            },
        }

        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        response = self._post(payload)

        return (
            response.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )

    # ---------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------
    def _choose_model(self, text: str) -> str:
        return FAST_MODEL if len(text) < AUTO_THRESHOLD else SMART_MODEL

    def _post(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(OLLAMA_URL, json=payload, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()

    # =========================================================
    # Summarize (sync compatibility wrapper)
    # =========================================================
    def summarize_module(self, code: str, module: str) -> str:
        """
        Synchronous compatibility wrapper used by root orchestration layers.
        """

        cache = self._get_cache()

        key_data = {
            "task": "summarize",
            "module": module,
            "code": code,
        }

        cached = cache.get(key_data)
        if cached:
            return cached

        model = self._choose_model(code)

        messages = [
            {
                "role": "system",
                "content": "You are a senior Python engineer.",
            },
            {
                "role": "user",
                "content": f"Summarize module '{module}'.\n\n
python\n{code}\n
",
            },
        ]

        payload = {
            "model": model,
            "messages": messages,
        }

        response = self._post(payload)

        text = (
            response.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )

        cache.set(key_data, text)
        return text

    # =========================================================
    # Similarity (sync compatibility wrapper)
    # =========================================================
    def get_similarity(self, map_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synchronous compatibility wrapper used by root orchestration layers.
        """

        cache = self._get_cache()

        key_data = {
            "task": "similarity",
            "map_data": map_data,
        }

        cached = cache.get(key_data)
        if cached:
            return cached

        model = self._choose_model(str(map_data))

        messages = [
            {
                "role": "system",
                "content": "You are a senior Python engineer.",
            },
            {
                "role": "user",
                "content": str(map_data),
            },
        ]

        payload = {
            "model": model,
            "messages": messages,
        }

        response = self._post(payload)

        cache.set(key_data, response)
        return response

    # =========================================================
    # Summarize (async + cache)
    # =========================================================
    def summarize_module_async(
        self,
        code: str,
        module: str,
        on_success: Callable[[str], None],
        on_error: Callable[[str], None] | None = None,
    ) -> None:
        def task() -> None:
            try:
                cache = self._get_cache()

                key_data = {
                    "task": "summarize",
                    "module": module,
                    "code": code,
                }

                cached = cache.get(key_data)
                if cached:
                    on_success(cached)
                    return

                model = self._choose_model(code)

                messages = [
                    {
                        "role": "system",
                        "content": "You are a senior Python engineer.",
                    },
                    {
                        "role": "user",
                        "content": f"Summarize module '{module}'.\n\n
python\n{code}\n
",
                    },
                ]

                payload = {
                    "model": model,
                    "messages": messages,
                }

                response = self._post(payload)

                text = (
                    response.get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "")
                )

                cache.set(key_data, text)
                on_success(text)

            except Exception as exc:
                if on_error:
                    on_error(str(exc))

        AIRequestQueue().submit(task)

    # =========================================================
    # Streaming summarize (async + cache)
    # =========================================================
    def stream_summarize_module(
        self,
        code: str,
        module: str,
        on_token: Callable[[str], None],
        on_done: Callable[[str], None],
        on_error: Callable[[str], None] | None = None,
    ) -> None:
        def task() -> None:
            try:
                cache = self._get_cache()

                key_data = {
                    "task": "summarize",
                    "module": module,
                    "code": code,
                }

                cached = cache.get(key_data)
                if cached:
                    if on_token:
                        on_token(cached)
                    if on_done:
                        on_done(cached)
                    return

                model = self._choose_model(code)

                messages = [
                    {
                        "role": "system",
                        "content": "You are a senior Python engineer.",
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Summarize module '{module}'.\n\n"
                            f"
python\n{code}\n
"
                        ),
                    },
                ]

                payload = {
                    "model": model,
                    "messages": messages,
                    "stream": True,
                }

                full = ""

                with requests.post(
                    OLLAMA_URL,
                    json=payload,
                    stream=True,
                    timeout=TIMEOUT,
                ) as response:
                    response.raise_for_status()

                    for line in response.iter_lines():
                        if not line:
                            continue

                        if isinstance(line, (bytes, bytearray)):
                            line_str = line.decode("utf-8", errors="ignore").strip()
                        else:
                            line_str = str(line).strip()

                        if not line_str:
                            continue

                        if line_str.startswith("data:"):
                            line_str = line_str[len("data:"):].strip()

                        if not line_str or line_str == "[DONE]":
                            continue

                        try:
                            data = json.loads(line_str)
                        except Exception:
                            continue

                        token = (
                            data.get("choices", [{}])[0]
                            .get("delta", {})
                            .get("content", "")
                            or ""
                        )

                        if token:
                            full += token
                            if on_token:
                                on_token(token)

                cache.set(key_data, full)

                if on_done:
                    on_done(full)

            except Exception as exc:
                if on_error:
                    on_error(str(exc))

        AIRequestQueue().submit(task)

    # =========================================================
    # Similarity (async + cache)
    # =========================================================
    def get_similarity_async(
        self,
        map_data: Dict[str, Any],
        on_success: Callable[[Dict[str, Any]], None],
        on_error: Callable[[str], None] | None = None,
    ) -> None:
        def task() -> None:
            try:
                cache = self._get_cache()

                key_data = {
                    "task": "similarity",
                    "map_data": map_data,
                }

                cached = cache.get(key_data)
                if cached:
                    on_success(cached)
                    return

                model = self._choose_model(str(map_data))

                messages = [
                    {
                        "role": "system",
                        "content": "You are a senior Python engineer.",
                    },
                    {
                        "role": "user",
                        "content": str(map_data),
                    },
                ]

                payload = {
                    "model": model,
                    "messages": messages,
                }

                response = self._post(payload)

                cache.set(key_data, response)
                on_success(response)

            except Exception as exc:
                if on_error:
                    on_error(str(exc))

        AIRequestQueue().submit(task)

    # =========================================================
    # Explain Selection (async + stream + cache)
    # =========================================================
    def stream_explain_selection(
        self,
        code: str,
        *,
        filename: str = "",
        on_token: Callable[[str], None] | None = None,
        on_done: Callable[[str], None] | None = None,
        on_error: Callable[[str], None] | None = None,
    ) -> None:
        """
        Explain only the provided selected code snippet.
        Cached on disk and streamed to callbacks.
        """

        def task() -> None:
            try:
                cache = self._get_cache()

                key_data = {
                    "task": "explain_selection",
                    "filename": filename or "",
                    "code": code,
                }

                cached = cache.get(key_data)
                if cached:
                    if on_token:
                        for index in range(0, len(cached), 120):
                            on_token(cached[index:index + 120])
                    if on_done:
                        on_done(cached)
                    return

                system_prompt = (
                    "You are a senior Python engineer.\n"
                    "Explain ONLY the provided code selection.\n"
                    "Rules:\n"
                    "- Focus ONLY on the code shown. Do NOT assume other files exist.\n"
                    "- If identifiers are undefined, say what they likely are.\n"
                    "- Be concrete: inputs, outputs, side effects, data structures.\n"
                    "- Mention visible bugs, edge-cases, and limitations.\n"
                )

                user_content = (
                    f"File: {filename or '<unknown>'}\n\n"
                    "Code selection:\n"
                    "
python\n"
                    f"{code}\n"
                    "
\n\n"
                    "Explain what this selection does."
                )

                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ]

                model = self._choose_model(code)

                payload = {
                    "model": model,
                    "messages": messages,
                    "stream": True,
                    "options": {
                        "temperature": 0.2,
                        "num_ctx": 8192,
                    },
                }

                full = ""

                with requests.post(
                    OLLAMA_URL,
                    json=payload,
                    stream=True,
                    timeout=TIMEOUT,
                ) as response:
                    response.raise_for_status()

                    for line in response.iter_lines():
                        if not line:
                            continue

                        if isinstance(line, (bytes, bytearray)):
                            line_str = line.decode("utf-8", errors="ignore").strip()
                        else:
                            line_str = str(line).strip()

                        if not line_str:
                            continue

                        if line_str.startswith("data:"):
                            line_str = line_str[len("data:"):].strip()

                        if not line_str:
                            continue

                        if line_str == "[DONE]":
                            break

                        try:
                            data = json.loads(line_str)
                        except Exception:
                            continue

                        delta = ""

                        if "choices" in data:
                            delta = (
                                data.get("choices", [{}])[0]
                                .get("delta", {})
                                .get("content", "")
                                or ""
                            )
                        elif "message" in data:
                            delta = data.get("message", {}).get("content", "") or ""

                        if delta:
                            full += delta
                            if on_token:
                                on_token(delta)

                cache.set(key_data, full)

                if on_done:
                    on_done(full)

            except Exception as exc:
                if on_error:
                    on_error(str(exc))

        AIRequestQueue().submit(task)
Thought for 16s

Below is a Version 7 that adds an "Ask Local AI" layer on top of the JSON explorer idea.

What this version does:
loads your project JSON
retrieves the most relevant files and symbols from the JSON for a question
builds a compact evidence pack
sends that evidence pack to your local Qwen wrapper
returns an architecture answer grounded in the JSON
keeps the GUI responsive by using your existing AIRequestQueue through the wrapper side

Main goal:
make your local AI answer questions like:
which module starts the app
how does topomap get created and updated
what is the startup chain from window builder to tabs to timeline
where is reset handled and which modules are involved
what code wires splash, timeline, tabs, topomap, close flow

You can save this as something like:
tools\project_json_explorer_v7_ai.py

from __future__ import annotations

import json
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Any

from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from pykanda_ai.connectors.qwen_model_wrapper import QwenModelWrapper


def norm_text(value: Any) -> str:
    return str(value).strip().lower() if value is not None else ""


def tokenize_query(text: str) -> list[str]:
    tokens = re.findall(r"[a-zA-Z0-9_\.]+", text.lower())
    stop_words = {
        "the",
        "is",
        "are",
        "a",
        "an",
        "of",
        "to",
        "me",
        "show",
        "which",
        "what",
        "where",
        "who",
        "does",
        "do",
        "in",
        "on",
        "for",
        "and",
        "or",
        "with",
        "code",
        "module",
        "file",
        "implementing",
        "implements",
        "created",
        "creates",
        "create",
        "that",
        "this",
        "app",
        "about",
        "how",
        "from",
    }
    return [token for token in tokens if token not in stop_words]


def shorten_path(path: str, max_len: int = 80) -> str:
    if len(path) <= max_len:
        return path
    return "..." + path[-(max_len - 3):]


@dataclass
class EvidenceItem:
    evidence_id: str
    score: int
    path: str
    module_name: str
    reason: str
    detail: str


class AIWorkerBridge(QObject):
    answer_ready = Signal(str)
    error_ready = Signal(str)
    status_ready = Signal(str)


class JsonProjectReasonerV7(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Project JSON Explorer v7 - Local AI Reasoner")
        self.resize(1700, 980)

        self.index_data: dict[str, Any] | None = None
        self.project_root: str = ""
        self.files_by_path: dict[str, dict[str, Any]] = {}
        self.files_by_module: dict[str, dict[str, Any]] = {}
        self.semantic_roles: dict[str, dict[str, Any]] = {}
        self.symbol_details: dict[str, dict[str, Any]] = {}
        self.symbol_to_file: dict[str, set[str]] = defaultdict(set)
        self.import_graph_out: dict[str, set[str]] = defaultdict(set)
        self.call_graph_out: dict[str, set[str]] = defaultdict(set)

        self.ai = QwenModelWrapper()
        self.bridge = AIWorkerBridge()

        self.json_path_edit = QLineEdit()
        self.question_edit = QLineEdit()
        self.cache_dir_edit = QLineEdit()
        self.governance_path_edit = QLineEdit()

        self.load_button = QPushButton("Load JSON")
        self.ask_ai_button = QPushButton("Ask Local AI")
        self.clear_button = QPushButton("Clear")
        self.pick_cache_dir_button = QPushButton("Set Cache Dir")
        self.pick_governance_button = QPushButton("Set Governance State")

        self.quick_startup_button = QPushButton("Startup")
        self.quick_tabs_button = QPushButton("Tabs")
        self.quick_topomap_button = QPushButton("Topomap")
        self.quick_timeline_button = QPushButton("Timeline")
        self.quick_splash_button = QPushButton("Splash")
        self.quick_reset_button = QPushButton("Reset")

        self.evidence_list = QListWidget()
        self.evidence_detail = QPlainTextEdit()
        self.evidence_detail.setReadOnly(True)

        self.answer_box = QPlainTextEdit()
        self.answer_box.setReadOnly(True)

        self.prompt_preview = QPlainTextEdit()
        self.prompt_preview.setReadOnly(True)

        self.log_box = QPlainTextEdit()
        self.log_box.setReadOnly(True)

        self._last_evidence: list[EvidenceItem] = []
        self._last_prompt: str = ""

        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

        top_group = QGroupBox("Project JSON")
        top_layout = QGridLayout(top_group)
        top_layout.addWidget(QLabel("JSON file:"), 0, 0)
        top_layout.addWidget(self.json_path_edit, 0, 1)
        top_layout.addWidget(self.load_button, 0, 2)

        cfg_group = QGroupBox("Local AI Runtime")
        cfg_layout = QGridLayout(cfg_group)
        cfg_layout.addWidget(QLabel("Cache dir:"), 0, 0)
        cfg_layout.addWidget(self.cache_dir_edit, 0, 1)
        cfg_layout.addWidget(self.pick_cache_dir_button, 0, 2)
        cfg_layout.addWidget(QLabel("Governance state:"), 1, 0)
        cfg_layout.addWidget(self.governance_path_edit, 1, 1)
        cfg_layout.addWidget(self.pick_governance_button, 1, 2)

        ask_group = QGroupBox("Ask Complex Architecture Questions")
        ask_layout = QGridLayout(ask_group)
        ask_layout.addWidget(QLabel("Question:"), 0, 0)
        ask_layout.addWidget(self.question_edit, 0, 1)
        ask_layout.addWidget(self.ask_ai_button, 0, 2)
        ask_layout.addWidget(self.clear_button, 0, 3)

        quick_row = QHBoxLayout()
        quick_row.addWidget(self.quick_startup_button)
        quick_row.addWidget(self.quick_tabs_button)
        quick_row.addWidget(self.quick_topomap_button)
        quick_row.addWidget(self.quick_timeline_button)
        quick_row.addWidget(self.quick_splash_button)
        quick_row.addWidget(self.quick_reset_button)
        quick_row.addStretch()

        main_splitter = QSplitter(Qt.Horizontal)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(QLabel("Retrieved Evidence"))
        left_layout.addWidget(self.evidence_list)
        left_layout.addWidget(QLabel("Selected Evidence Detail"))
        left_layout.addWidget(self.evidence_detail)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.addWidget(QLabel("Local AI Answer"))
        right_layout.addWidget(self.answer_box, stretch=2)
        right_layout.addWidget(QLabel("Prompt / Evidence Pack Sent To AI"))
        right_layout.addWidget(self.prompt_preview, stretch=1)

        main_splitter.addWidget(left_panel)
        main_splitter.addWidget(right_panel)
        main_splitter.setSizes([620, 1000])

        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout(log_group)
        log_layout.addWidget(self.log_box)

        main_layout.addWidget(top_group)
        main_layout.addWidget(cfg_group)
        main_layout.addWidget(ask_group)
        main_layout.addLayout(quick_row)
        main_layout.addWidget(main_splitter, stretch=1)
        main_layout.addWidget(log_group)

    def _connect_signals(self) -> None:
        self.load_button.clicked.connect(self.load_json)
        self.ask_ai_button.clicked.connect(self.ask_local_ai)
        self.clear_button.clicked.connect(self.clear_all)

        self.pick_cache_dir_button.clicked.connect(self.pick_cache_dir)
        self.pick_governance_button.clicked.connect(self.pick_governance_path)

        self.quick_startup_button.clicked.connect(
            lambda: self._run_quick_question("Which module starts the app and what is the startup chain?")
        )
        self.quick_tabs_button.clicked.connect(
            lambda: self._run_quick_question("Which code creates the superior tab and how are tabs constructed?")
        )
        self.quick_topomap_button.clicked.connect(
            lambda: self._run_quick_question("Show me which code is implementing topomap and how it is wired.")
        )
        self.quick_timeline_button.clicked.connect(
            lambda: self._run_quick_question("Explain the timeline architecture and which modules wire it.")
        )
        self.quick_splash_button.clicked.connect(
            lambda: self._run_quick_question("Where is splash created, shown, and hidden in the app?")
        )
        self.quick_reset_button.clicked.connect(
            lambda: self._run_quick_question("Explain reset and snapshot flow for EEG session state.")
        )

        self.question_edit.returnPressed.connect(self.ask_local_ai)
        self.evidence_list.currentItemChanged.connect(self._show_selected_evidence_detail)

        self.bridge.answer_ready.connect(self._on_ai_answer_ready)
        self.bridge.error_ready.connect(self._on_ai_error_ready)
        self.bridge.status_ready.connect(self._append_log)

    def _append_log(self, text: str) -> None:
        self.log_box.appendPlainText(text)

    def clear_all(self) -> None:
        self.evidence_list.clear()
        self.evidence_detail.clear()
        self.answer_box.clear()
        self.prompt_preview.clear()
        self.log_box.clear()
        self._last_evidence = []
        self._last_prompt = ""

    def _run_quick_question(self, question: str) -> None:
        self.question_edit.setText(question)
        self.ask_local_ai()

    def pick_cache_dir(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Select cache directory")
        if not path:
            return
        self.cache_dir_edit.setText(path)
        try:
            self.ai.set_cache_dir(pathlib_path(path))
            self._append_log("Cache dir set: " + path)
        except Exception as exc:
            QMessageBox.warning(self, "Cache dir error", str(exc))

    def pick_governance_path(self) -> None:
        path, _filter = QFileDialog.getOpenFileName(
            self,
            "Select governance_state.json",
            os.getcwd(),
            "JSON Files (*.json)",
        )
        if not path:
            return
        self.governance_path_edit.setText(path)
        try:
            self.ai.set_governance_state_path(pathlib_path(path))
            self._append_log("Governance state set: " + path)
        except Exception as exc:
            QMessageBox.warning(self, "Governance path error", str(exc))

    def load_json(self) -> None:
        current_path = self.json_path_edit.text().strip()
        start_dir = os.path.dirname(current_path) if current_path else os.getcwd()

        file_path, _filter = QFileDialog.getOpenFileName(
            self,
            "Select project_structure_index.json",
            start_dir,
            "JSON Files (*.json)",
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as handle:
                self.index_data = json.load(handle)

            self.json_path_edit.setText(file_path)
            self.project_root = (
                self.index_data.get("project_summary", {}).get("project_root", "") or ""
            )
            self.semantic_roles = self.index_data.get("semantic_roles", {})
            self._rebuild_indexes()

            summary = self.index_data.get("project_summary", {})
            self._append_log("Loaded JSON: " + file_path)
            self._append_log("Project root: " + self.project_root)
            self._append_log("Python files: " + str(summary.get("python_file_count", "unknown")))
            self._append_log("Entry files: " + str(summary.get("entry_file_count", "unknown")))

            QMessageBox.information(self, "Loaded", "JSON loaded successfully.")
        except Exception as exc:
            QMessageBox.critical(self, "Error", "Failed to load JSON:\n" + str(exc))

    def _rebuild_indexes(self) -> None:
        self.files_by_path.clear()
        self.files_by_module.clear()
        self.symbol_details.clear()
        self.symbol_to_file.clear()
        self.import_graph_out.clear()
        self.call_graph_out.clear()

        if not self.index_data:
            return

        for file_record in self.index_data.get("files", []):
            path = file_record.get("path", "")
            module_name = file_record.get("module_name", "")
            if path:
                self.files_by_path[path] = file_record
            if module_name:
                self.files_by_module[module_name] = file_record

            for fn in file_record.get("functions", []):
                qualname = fn.get("qualname", "")
                if qualname:
                    self.symbol_details[qualname] = {
                        "file": path,
                        "line": int(fn.get("lineno", 1)),
                        "kind": "function",
                        "record": fn,
                    }
                    self.symbol_to_file[qualname].add(path)

            for cls in file_record.get("classes", []):
                cls_name = cls.get("name", "")
                if cls_name:
                    self.symbol_details[cls_name] = {
                        "file": path,
                        "line": int(cls.get("lineno", 1)),
                        "kind": "class",
                        "record": cls,
                    }
                    self.symbol_to_file[cls_name].add(path)

                for method in cls.get("methods", []):
                    qualname = method.get("qualname", "")
                    if qualname:
                        self.symbol_details[qualname] = {
                            "file": path,
                            "line": int(method.get("lineno", 1)),
                            "kind": "method",
                            "record": method,
                        }
                        self.symbol_to_file[qualname].add(path)

        for src_module, targets in self.index_data.get("import_graph", {}).items():
            src_path = self._resolve_module_to_path(src_module) or src_module
            for target in targets:
                self.import_graph_out[src_path].add(target)

        for edge in self.index_data.get("call_edges", []):
            from_file = edge.get("from_file", "")
            to_call = edge.get("to_call", "")
            if from_file and to_call:
                self.call_graph_out[from_file].add(to_call)

    def _resolve_module_to_path(self, module_name: str) -> str | None:
        record = self.files_by_module.get(module_name)
        if record:
            return record.get("path")
        return None

    def ask_local_ai(self) -> None:
        if not self.index_data:
            QMessageBox.warning(self, "No JSON", "Please load a JSON file first.")
            return

        question = self.question_edit.text().strip()
        if not question:
            QMessageBox.warning(self, "No Question", "Please type a question.")
            return

        evidence = self._retrieve_evidence(question, limit=14)
        if not evidence:
            QMessageBox.information(self, "No Evidence", "No relevant evidence was retrieved from the JSON.")
            return

        self._last_evidence = evidence
        self._populate_evidence_list(evidence)

        prompt = self._build_ai_prompt(question, evidence)
        self._last_prompt = prompt
        self.prompt_preview.setPlainText(prompt)
        self.answer_box.setPlainText("Thinking...")

        self.bridge.status_ready.emit("Submitting question to local AI...")

        try:
            self.ai.chat_async = None
        except Exception:
            pass

        from pykanda_ai.runtime.ai_request_queue import AIRequestQueue

        def task() -> None:
            try:
                messages = [
                    {
                        "role": "system",
                        "content": (
                            "You are a senior Python architecture analyst. "
                            "Answer only from the supplied JSON-derived evidence pack. "
                            "Do not invent files, classes, or flows. "
                            "If evidence is insufficient, say so clearly. "
                            "Always cite evidence ids like [E01], [E02]. "
                            "Prefer concrete startup chains, module names, function names, class names, "
                            "and relationships between modules."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ]

                answer = self.ai.chat(
                    messages,
                    temperature=0.1,
                    max_tokens=1800,
                )
                self.bridge.answer_ready.emit(answer)
            except Exception as exc:
                self.bridge.error_ready.emit(str(exc))

        AIRequestQueue().submit(task)

    def _retrieve_evidence(self, question: str, limit: int = 14) -> list[EvidenceItem]:
        q = norm_text(question)
        tokens = tokenize_query(q)
        entry_files = set(self.index_data.get("entry_files", []))

        scored: list[EvidenceItem] = []

        for path, file_record in self.files_by_path.items():
            module_name = file_record.get("module_name", "")
            docstring = file_record.get("docstring", "")
            strings = " ".join(file_record.get("strings", []))
            comments = " ".join(file_record.get("comments", []))
            entry_markers = " ".join(file_record.get("entry_markers", []))
            ui_hits = " ".join(file_record.get("ui_keyword_hits", []))
            eeg_hits = " ".join(file_record.get("eeg_keyword_hits", []))
            semantic_hints = " ".join(file_record.get("semantic_hints", []))

            function_names = []
            class_names = []
            called_symbols = []

            for fn in file_record.get("functions", []):
                function_names.append(fn.get("qualname", ""))
                function_names.append(fn.get("name", ""))
                for call in fn.get("calls", []):
                    called_symbols.append(call.get("call_name", ""))

            for cls in file_record.get("classes", []):
                class_names.append(cls.get("name", ""))
                for method in cls.get("methods", []):
                    function_names.append(method.get("qualname", ""))
                    function_names.append(method.get("name", ""))
                    for call in method.get("calls", []):
                        called_symbols.append(call.get("call_name", ""))

            roles = self.semantic_roles.get(path, {}).get("roles", [])

            haystack = " ".join(
                [
                    norm_text(path),
                    norm_text(module_name),
                    norm_text(docstring),
                    norm_text(strings),
                    norm_text(comments),
                    norm_text(entry_markers),
                    norm_text(ui_hits),
                    norm_text(eeg_hits),
                    norm_text(semantic_hints),
                    norm_text(" ".join(function_names)),
                    norm_text(" ".join(class_names)),
                    norm_text(" ".join(called_symbols)),
                    norm_text(" ".join(roles)),
                ]
            )

            score = 0
            reasons = []

            for token in tokens:
                if token in haystack:
                    score += 3
                    reasons.append("token:" + token)

            if path in entry_files and any(key in q for key in ["start", "startup", "main", "launch", "open app"]):
                score += 14
                reasons.append("entry-file")

            if "topomap" in q and ("topomap" in haystack or "amplitude_map" in haystack):
                score += 12
                reasons.append("topomap-related")

            if "timeline" in q and "timeline" in haystack:
                score += 12
                reasons.append("timeline-related")

            if "splash" in q and "splash" in haystack:
                score += 12
                reasons.append("splash-related")

            if "tab" in q and ("tab" in haystack or "notebook" in haystack or "addtab" in haystack):
                score += 12
                reasons.append("tab-related")

            if ("reset" in q or "snapshot" in q) and ("reset" in haystack or "snapshot" in haystack):
                score += 12
                reasons.append("reset-related")

            if score <= 0:
                continue

            detail = self._build_compact_file_evidence(path, reasons)
            evidence_id = "E" + str(len(scored) + 1).zfill(2)

            scored.append(
                EvidenceItem(
                    evidence_id=evidence_id,
                    score=score,
                    path=path,
                    module_name=module_name,
                    reason=", ".join(sorted(set(reasons))),
                    detail=detail,
                )
            )

        scored.sort(key=lambda item: (-item.score, item.path))
        scored = scored[:limit]

        reindexed: list[EvidenceItem] = []
        for idx, item in enumerate(scored, start=1):
            reindexed.append(
                EvidenceItem(
                    evidence_id="E" + str(idx).zfill(2),
                    score=item.score,
                    path=item.path,
                    module_name=item.module_name,
                    reason=item.reason,
                    detail=item.detail,
                )
            )
        return reindexed

    def _build_compact_file_evidence(self, path: str, reasons: list[str]) -> str:
        file_record = self.files_by_path[path]
        roles = self.semantic_roles.get(path, {}).get("roles", [])

        lines: list[str] = []
        lines.append("Path: " + path)
        lines.append("Module: " + str(file_record.get("module_name", "")))
        lines.append("Reasons: " + ", ".join(sorted(set(reasons))))

        if roles:
            lines.append("Roles: " + ", ".join(roles))

        entry_markers = file_record.get("entry_markers", [])
        if entry_markers:
            lines.append("Entry markers: " + "; ".join(entry_markers[:6]))

        top_functions: list[str] = []
        for fn in file_record.get("functions", [])[:8]:
            top_functions.append(fn.get("qualname", "") + "@" + str(fn.get("lineno", "")))
        if top_functions:
            lines.append("Functions: " + " | ".join(top_functions))

        top_classes: list[str] = []
        for cls in file_record.get("classes", [])[:6]:
            class_text = cls.get("name", "") + "@" + str(cls.get("lineno", ""))
            methods = cls.get("methods", [])[:4]
            if methods:
                class_text += " methods=" + ",".join([m.get("name", "") for m in methods])
            top_classes.append(class_text)
        if top_classes:
            lines.append("Classes: " + " | ".join(top_classes))

        imports_out = sorted(self.import_graph_out.get(path, []))
        if imports_out:
            lines.append("Imports out: " + " | ".join(imports_out[:8]))

        calls_out = sorted(self.call_graph_out.get(path, []))
        if calls_out:
            lines.append("Calls out: " + " | ".join(calls_out[:10]))

        docstring = str(file_record.get("docstring", "")).strip()
        if docstring:
            docstring = re.sub(r"\s+", " ", docstring)
            lines.append("Docstring: " + docstring[:500])

        return "\n".join(lines)

    def _build_ai_prompt(self, question: str, evidence: list[EvidenceItem]) -> str:
        summary = self.index_data.get("project_summary", {})
        lines: list[str] = []

        lines.append("USER QUESTION")
        lines.append(question)
        lines.append("")
        lines.append("PROJECT SUMMARY")
        lines.append("Project root: " + str(summary.get("project_root", "")))
        lines.append("Python files indexed: " + str(summary.get("python_file_count", "")))
        lines.append("Entry files: " + ", ".join(self.index_data.get("entry_files", [])[:12]))
        lines.append("")
        lines.append("RETRIEVED EVIDENCE")
        for item in evidence:
            lines.append("[" + item.evidence_id + "] score=" + str(item.score))
            lines.append(item.detail)
            lines.append("")

        lines.append("INSTRUCTIONS")
        lines.append(
            "Answer the user question using only the evidence above. "
            "Explain the architecture in concrete terms. "
            "When describing flows, mention module names, class names, and function names if present. "
            "Cite evidence ids inline like [E01]. "
            "If evidence is partial, explicitly say what is known and what is uncertain."
        )

        return "\n".join(lines)

    def _populate_evidence_list(self, evidence: list[EvidenceItem]) -> None:
        self.evidence_list.clear()
        self.evidence_detail.clear()

        for item in evidence:
            label = (
                "[" + item.evidence_id + "] "
                + shorten_path(item.path, 90)
                + " | score="
                + str(item.score)
            )
            widget_item = QListWidgetItem(label)
            widget_item.setData(Qt.UserRole, item.evidence_id)
            self.evidence_list.addItem(widget_item)

        if evidence:
            self.evidence_list.setCurrentRow(0)

    def _show_selected_evidence_detail(self, current: QListWidgetItem, previous: QListWidgetItem) -> None:
        _ = previous
        if not current:
            self.evidence_detail.clear()
            return

        evidence_id = current.data(Qt.UserRole)
        for item in self._last_evidence:
            if item.evidence_id == evidence_id:
                self.evidence_detail.setPlainText(item.detail)
                return

        self.evidence_detail.clear()

    def _on_ai_answer_ready(self, text: str) -> None:
        self.answer_box.setPlainText(text)
        self._append_log("Local AI answer received.")

    def _on_ai_error_ready(self, error_text: str) -> None:
        self.answer_box.setPlainText("AI error:\n" + error_text)
        self._append_log("AI error: " + error_text)

    def _current_payload_from_evidence(self) -> EvidenceItem | None:
        item = self.evidence_list.currentItem()
        if not item:
            return None
        evidence_id = item.data(Qt.UserRole)
        for evidence in self._last_evidence:
            if evidence.evidence_id == evidence_id:
                return evidence
        return None


def pathlib_path(path: str):
    from pathlib import Path
    return Path(path).expanduser().resolve()


def main() -> None:
    app = QApplication(sys.argv)
    window = JsonProjectReasonerV7()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

How this Version 7 works

It does not send the entire JSON blindly to the model.
Instead it does retrieval first, which is much better for local models.

Flow:
load project_structure_index.json
score files against the question
build a ranked evidence pack
send only the top evidence to QwenModelWrapper.chat(...)
show the answer and the exact prompt sent to the model

Why this is better for local AI

A local model like Qwen 7B or 32B usually performs much better when:
you give it a focused evidence set
you force grounded answers
you require inline evidence references
you avoid flooding it with thousands of lines of unrelated JSON

Questions it should handle well

Which module starts the app and what is the startup chain?
Which code creates the superior tab?
Show me which code is implementing topomap and how it is wired.
Explain the timeline architecture and which modules wire it.
Where is splash created, shown, and hidden?
Explain reset and snapshot flow for EEG session state.
Which modules participate in closing EEG and resetting UI state?

Best next upgrade for Version 8

Version 8 should make the local AI even stronger by adding:
symbol-level retrieval, not only file-level retrieval
optional source snippet injection from the real .py files for top evidence
conversation history so you can ask follow-up questions like:
and after that?
which method calls that?
show me only timeline-related modules
structured answer modes:
summary
chain of execution
responsibility map
uncertainty report

If you want, next I will build Version 8 with:
symbol retrieval
source snippet extraction
follow-up memory
and a "Explain startup chain" button that generates a full execution-path report automatically.

gimme version 8 but it is becoming long, create helps files and call them in main file
Thought for 4s

Yes. Below is a cleaner Version 8 split into helper files.

Suggested structure:

tools/
    project_reasoner_v8/
        __init__.py
        v8_main_window.py
        v8_models.py
        v8_index_loader.py
        v8_retriever.py
        v8_prompt_builder.py
        v8_ai_bridge.py

File 1
tools/project_reasoner_v8/v8_models.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class EvidenceItem:
    evidence_id: str
    score: int
    path: str
    module_name: str
    reason: str
    detail: str


@dataclass
class SymbolEvidenceItem:
    evidence_id: str
    score: int
    symbol_name: str
    kind: str
    path: str
    line: int
    reason: str
    detail: str


@dataclass
class RetrievalBundle:
    file_evidence: list[EvidenceItem]
    symbol_evidence: list[SymbolEvidenceItem]
    snippet_evidence: list[dict[str, Any]]

File 2
tools/project_reasoner_v8/v8_index_loader.py

from __future__ import annotations

import json
from collections import defaultdict
from typing import Any


class JsonProjectIndex:
    def __init__(self) -> None:
        self.index_data: dict[str, Any] | None = None
        self.project_root: str = ""
        self.files_by_path: dict[str, dict[str, Any]] = {}
        self.files_by_module: dict[str, dict[str, Any]] = {}
        self.semantic_roles: dict[str, dict[str, Any]] = {}
        self.symbol_details: dict[str, dict[str, Any]] = {}
        self.symbol_to_file: dict[str, set[str]] = defaultdict(set)
        self.import_graph_out: dict[str, set[str]] = defaultdict(set)
        self.call_graph_out: dict[str, set[str]] = defaultdict(set)

    def load_json(self, file_path: str) -> None:
        with open(file_path, "r", encoding="utf-8") as handle:
            self.index_data = json.load(handle)

        self.project_root = (
            self.index_data.get("project_summary", {}).get("project_root", "") or ""
        )
        self.semantic_roles = self.index_data.get("semantic_roles", {})
        self._rebuild_indexes()

    def _rebuild_indexes(self) -> None:
        self.files_by_path.clear()
        self.files_by_module.clear()
        self.symbol_details.clear()
        self.symbol_to_file.clear()
        self.import_graph_out.clear()
        self.call_graph_out.clear()

        if not self.index_data:
            return

        for file_record in self.index_data.get("files", []):
            path = file_record.get("path", "")
            module_name = file_record.get("module_name", "")

            if path:
                self.files_by_path[path] = file_record
            if module_name:
                self.files_by_module[module_name] = file_record

            for fn in file_record.get("functions", []):
                qualname = fn.get("qualname", "")
                if qualname:
                    self.symbol_details[qualname] = {
                        "file": path,
                        "line": int(fn.get("lineno", 1)),
                        "kind": "function",
                        "record": fn,
                    }
                    self.symbol_to_file[qualname].add(path)

            for cls in file_record.get("classes", []):
                cls_name = cls.get("name", "")
                if cls_name:
                    self.symbol_details[cls_name] = {
                        "file": path,
                        "line": int(cls.get("lineno", 1)),
                        "kind": "class",
                        "record": cls,
                    }
                    self.symbol_to_file[cls_name].add(path)

                for method in cls.get("methods", []):
                    qualname = method.get("qualname", "")
                    if qualname:
                        self.symbol_details[qualname] = {
                            "file": path,
                            "line": int(method.get("lineno", 1)),
                            "kind": "method",
                            "record": method,
                        }
                        self.symbol_to_file[qualname].add(path)

        for src_module, targets in self.index_data.get("import_graph", {}).items():
            src_path = self.resolve_module_to_path(src_module) or src_module
            for target in targets:
                self.import_graph_out[src_path].add(target)

        for edge in self.index_data.get("call_edges", []):
            from_file = edge.get("from_file", "")
            to_call = edge.get("to_call", "")
            if from_file and to_call:
                self.call_graph_out[from_file].add(to_call)

    def resolve_module_to_path(self, module_name: str) -> str | None:
        record = self.files_by_module.get(module_name)
        if record:
            return record.get("path")
        return None

File 3
tools/project_reasoner_v8/v8_retriever.py

from __future__ import annotations

import os
import re
from typing import Any

from .v8_models import EvidenceItem, RetrievalBundle, SymbolEvidenceItem
from .v8_index_loader import JsonProjectIndex


def norm_text(value: Any) -> str:
    return str(value).strip().lower() if value is not None else ""


def tokenize_query(text: str) -> list[str]:
    tokens = re.findall(r"[a-zA-Z0-9_\.]+", text.lower())
    stop_words = {
        "the",
        "is",
        "are",
        "a",
        "an",
        "of",
        "to",
        "me",
        "show",
        "which",
        "what",
        "where",
        "who",
        "does",
        "do",
        "in",
        "on",
        "for",
        "and",
        "or",
        "with",
        "code",
        "module",
        "file",
        "implementing",
        "implements",
        "created",
        "creates",
        "create",
        "that",
        "this",
        "app",
        "about",
        "how",
        "from",
    }
    return [token for token in tokens if token not in stop_words]


def safe_read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return handle.read()


class ProjectRetriever:
    def __init__(self, project_index: JsonProjectIndex) -> None:
        self.idx = project_index

    def retrieve(
        self,
        question: str,
        *,
        file_limit: int = 10,
        symbol_limit: int = 10,
        snippet_limit: int = 6,
    ) -> RetrievalBundle:
        file_evidence = self._retrieve_files(question, file_limit)
        symbol_evidence = self._retrieve_symbols(question, symbol_limit)
        snippet_evidence = self._retrieve_snippets(file_evidence, symbol_evidence, snippet_limit)
        return RetrievalBundle(
            file_evidence=file_evidence,
            symbol_evidence=symbol_evidence,
            snippet_evidence=snippet_evidence,
        )

    def _retrieve_files(self, question: str, limit: int) -> list[EvidenceItem]:
        q = norm_text(question)
        tokens = tokenize_query(q)
        entry_files = set((self.idx.index_data or {}).get("entry_files", []))
        scored: list[EvidenceItem] = []

        for path, file_record in self.idx.files_by_path.items():
            module_name = file_record.get("module_name", "")
            docstring = file_record.get("docstring", "")
            strings = " ".join(file_record.get("strings", []))
            comments = " ".join(file_record.get("comments", []))
            entry_markers = " ".join(file_record.get("entry_markers", []))
            ui_hits = " ".join(file_record.get("ui_keyword_hits", []))
            eeg_hits = " ".join(file_record.get("eeg_keyword_hits", []))
            semantic_hints = " ".join(file_record.get("semantic_hints", []))
            roles = self.idx.semantic_roles.get(path, {}).get("roles", [])

            function_names: list[str] = []
            class_names: list[str] = []
            called_symbols: list[str] = []

            for fn in file_record.get("functions", []):
                function_names.append(fn.get("qualname", ""))
                function_names.append(fn.get("name", ""))
                for call in fn.get("calls", []):
                    called_symbols.append(call.get("call_name", ""))

            for cls in file_record.get("classes", []):
                class_names.append(cls.get("name", ""))
                for method in cls.get("methods", []):
                    function_names.append(method.get("qualname", ""))
                    function_names.append(method.get("name", ""))
                    for call in method.get("calls", []):
                        called_symbols.append(call.get("call_name", ""))

            haystack = " ".join(
                [
                    norm_text(path),
                    norm_text(module_name),
                    norm_text(docstring),
                    norm_text(strings),
                    norm_text(comments),
                    norm_text(entry_markers),
                    norm_text(ui_hits),
                    norm_text(eeg_hits),
                    norm_text(semantic_hints),
                    norm_text(" ".join(function_names)),
                    norm_text(" ".join(class_names)),
                    norm_text(" ".join(called_symbols)),
                    norm_text(" ".join(roles)),
                ]
            )

            score = 0
            reasons: list[str] = []

            for token in tokens:
                if token in haystack:
                    score += 3
                    reasons.append("token:" + token)

            if path in entry_files and any(key in q for key in ["start", "startup", "main", "launch", "open app"]):
                score += 14
                reasons.append("entry-file")

            if "topomap" in q and ("topomap" in haystack or "amplitude_map" in haystack):
                score += 12
                reasons.append("topomap-related")

            if "timeline" in q and "timeline" in haystack:
                score += 12
                reasons.append("timeline-related")

            if "splash" in q and "splash" in haystack:
                score += 12
                reasons.append("splash-related")

            if "tab" in q and ("tab" in haystack or "notebook" in haystack or "addtab" in haystack):
                score += 12
                reasons.append("tab-related")

            if ("reset" in q or "snapshot" in q) and ("reset" in haystack or "snapshot" in haystack):
                score += 12
                reasons.append("reset-related")

            if score <= 0:
                continue

            detail = self._build_compact_file_evidence(path, reasons)
            scored.append(
                EvidenceItem(
                    evidence_id="",
                    score=score,
                    path=path,
                    module_name=module_name,
                    reason=", ".join(sorted(set(reasons))),
                    detail=detail,
                )
            )

        scored.sort(key=lambda item: (-item.score, item.path))
        scored = scored[:limit]

        reindexed: list[EvidenceItem] = []
        for idx, item in enumerate(scored, start=1):
            reindexed.append(
                EvidenceItem(
                    evidence_id="F" + str(idx).zfill(2),
                    score=item.score,
                    path=item.path,
                    module_name=item.module_name,
                    reason=item.reason,
                    detail=item.detail,
                )
            )
        return reindexed

    def _retrieve_symbols(self, question: str, limit: int) -> list[SymbolEvidenceItem]:
        q = norm_text(question)
        tokens = tokenize_query(q)
        scored: list[SymbolEvidenceItem] = []

        for symbol_name, detail in self.idx.symbol_details.items():
            record = detail["record"]
            blob = norm_text(symbol_name)
            docstring = norm_text(record.get("docstring", ""))
            calls_blob = ""

            if detail["kind"] in ("function", "method"):
                calls_blob = norm_text(" ".join([c.get("call_name", "") for c in record.get("calls", [])]))

            haystack = " ".join([blob, docstring, calls_blob])

            score = 0
            reasons: list[str] = []
            for token in tokens:
                if token in haystack:
                    score += 4
                    reasons.append("symbol-token:" + token)

            if score <= 0:
                continue

            scored.append(
                SymbolEvidenceItem(
                    evidence_id="",
                    score=score,
                    symbol_name=symbol_name,
                    kind=detail["kind"],
                    path=detail["file"],
                    line=detail["line"],
                    reason=", ".join(sorted(set(reasons))),
                    detail=self._build_symbol_evidence(symbol_name),
                )
            )

        scored.sort(key=lambda item: (-item.score, item.symbol_name))
        scored = scored[:limit]

        reindexed: list[SymbolEvidenceItem] = []
        for idx, item in enumerate(scored, start=1):
            reindexed.append(
                SymbolEvidenceItem(
                    evidence_id="S" + str(idx).zfill(2),
                    score=item.score,
                    symbol_name=item.symbol_name,
                    kind=item.kind,
                    path=item.path,
                    line=item.line,
                    reason=item.reason,
                    detail=item.detail,
                )
            )
        return reindexed

    def _retrieve_snippets(
        self,
        file_evidence: list[EvidenceItem],
        symbol_evidence: list[SymbolEvidenceItem],
        limit: int,
    ) -> list[dict[str, Any]]:
        snippets: list[dict[str, Any]] = []
        seen: set[tuple[str, int]] = set()

        for item in symbol_evidence:
            abs_path = os.path.join(self.idx.project_root, item.path)
            if not os.path.exists(abs_path):
                continue
            key = (item.path, item.line)
            if key in seen:
                continue
            seen.add(key)
            snippet_text = self._read_snippet(abs_path, item.line, radius=20)
            snippets.append(
                {
                    "snippet_id": "SN" + str(len(snippets) + 1).zfill(2),
                    "path": item.path,
                    "line": item.line,
                    "anchor": item.symbol_name,
                    "text": snippet_text,
                }
            )
            if len(snippets) >= limit:
                return snippets

        for item in file_evidence:
            abs_path = os.path.join(self.idx.project_root, item.path)
            if not os.path.exists(abs_path):
                continue
            key = (item.path, 1)
            if key in seen:
                continue
            seen.add(key)
            snippet_text = self._read_snippet(abs_path, 1, radius=40)
            snippets.append(
                {
                    "snippet_id": "SN" + str(len(snippets) + 1).zfill(2),
                    "path": item.path,
                    "line": 1,
                    "anchor": "file-start",
                    "text": snippet_text,
                }
            )
            if len(snippets) >= limit:
                return snippets

        return snippets

    def _read_snippet(self, abs_path: str, line: int, radius: int) -> str:
        text = safe_read_text(abs_path)
        lines = text.splitlines()
        if not lines:
            return ""

        start = max(1, line - radius)
        end = min(len(lines), line + radius)
        out: list[str] = []

        for idx in range(start, end + 1):
            out.append(str(idx).rjust(5) + " | " + lines[idx - 1])

        return "\n".join(out)

    def _build_compact_file_evidence(self, path: str, reasons: list[str]) -> str:
        file_record = self.idx.files_by_path[path]
        roles = self.idx.semantic_roles.get(path, {}).get("roles", [])

        lines: list[str] = []
        lines.append("Path: " + path)
        lines.append("Module: " + str(file_record.get("module_name", "")))
        lines.append("Reasons: " + ", ".join(sorted(set(reasons))))

        if roles:
            lines.append("Roles: " + ", ".join(roles))

        entry_markers = file_record.get("entry_markers", [])
        if entry_markers:
            lines.append("Entry markers: " + "; ".join(entry_markers[:6]))

        top_functions: list[str] = []
        for fn in file_record.get("functions", [])[:8]:
            top_functions.append(fn.get("qualname", "") + "@" + str(fn.get("lineno", "")))
        if top_functions:
            lines.append("Functions: " + " | ".join(top_functions))

        top_classes: list[str] = []
        for cls in file_record.get("classes", [])[:6]:
            class_text = cls.get("name", "") + "@" + str(cls.get("lineno", ""))
            methods = cls.get("methods", [])[:4]
            if methods:
                class_text += " methods=" + ",".join([m.get("name", "") for m in methods])
            top_classes.append(class_text)
        if top_classes:
            lines.append("Classes: " + " | ".join(top_classes))

        imports_out = sorted(self.idx.import_graph_out.get(path, []))
        if imports_out:
            lines.append("Imports out: " + " | ".join(imports_out[:8]))

        calls_out = sorted(self.idx.call_graph_out.get(path, []))
        if calls_out:
            lines.append("Calls out: " + " | ".join(calls_out[:10]))

        docstring = str(file_record.get("docstring", "")).strip()
        if docstring:
            docstring = re.sub(r"\s+", " ", docstring)
            lines.append("Docstring: " + docstring[:500])

        return "\n".join(lines)

    def _build_symbol_evidence(self, symbol_name: str) -> str:
        detail = self.idx.symbol_details[symbol_name]
        path = detail["file"]
        line = detail["line"]
        kind = detail["kind"]
        record = detail["record"]

        lines: list[str] = []
        lines.append("Symbol: " + symbol_name)
        lines.append("Kind: " + kind)
        lines.append("Location: " + path + ":" + str(line))

        if record.get("docstring"):
            docstring = re.sub(r"\s+", " ", str(record.get("docstring", "")).strip())
            lines.append("Docstring: " + docstring[:500])

        if kind in ("function", "method"):
            calls = [c.get("call_name", "") for c in record.get("calls", [])[:20]]
            if calls:
                lines.append("Calls: " + " | ".join(calls))

        return "\n".join(lines)

File 4
tools/project_reasoner_v8/v8_prompt_builder.py

from __future__ import annotations

from .v8_models import RetrievalBundle


class PromptBuilder:
    def build(self, question: str, bundle: RetrievalBundle, project_root: str, summary: dict) -> str:
        lines: list[str] = []

        lines.append("USER QUESTION")
        lines.append(question)
        lines.append("")
        lines.append("PROJECT SUMMARY")
        lines.append("Project root: " + str(project_root))
        lines.append("Python files indexed: " + str(summary.get("python_file_count", "")))
        lines.append("Entry files: " + ", ".join(summary.get("entry_files", [])))
        lines.append("")
        lines.append("FILE EVIDENCE")
        for item in bundle.file_evidence:
            lines.append("[" + item.evidence_id + "] score=" + str(item.score))
            lines.append(item.detail)
            lines.append("")

        lines.append("SYMBOL EVIDENCE")
        for item in bundle.symbol_evidence:
            lines.append("[" + item.evidence_id + "] score=" + str(item.score))
            lines.append(item.detail)
            lines.append("")

        lines.append("SOURCE SNIPPETS")
        for item in bundle.snippet_evidence:
            lines.append(
                "[" + item["snippet_id"] + "] "
                + item["path"]
                + ":"
                + str(item["line"])
                + " anchor="
                + item["anchor"]
            )
            lines.append(item["text"])
            lines.append("")

        lines.append("INSTRUCTIONS")
        lines.append(
            "Answer strictly from the evidence above. "
            "Do not invent modules or flows. "
            "Use concrete names of files, classes, methods, and functions whenever present. "
            "Cite file evidence ids like [F01], symbol evidence ids like [S01], "
            "and snippet ids like [SN01]. "
            "For execution chains, present the chain step by step. "
            "If evidence is incomplete, say exactly what is uncertain."
        )

        return "\n".join(lines)

File 5
tools/project_reasoner_v8/v8_ai_bridge.py

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject, Signal

from pykanda_ai.connectors.qwen_model_wrapper import QwenModelWrapper
from pykanda_ai.runtime.ai_request_queue import AIRequestQueue


class AIWorkerBridge(QObject):
    answer_ready = Signal(str)
    error_ready = Signal(str)
    status_ready = Signal(str)


class LocalAIReasoner:
    def __init__(self) -> None:
        self.wrapper = QwenModelWrapper()
        self.bridge = AIWorkerBridge()

    def set_cache_dir(self, cache_dir: str) -> None:
        self.wrapper.set_cache_dir(Path(cache_dir).expanduser().resolve())

    def set_governance_state_path(self, state_path: str) -> None:
        self.wrapper.set_governance_state_path(Path(state_path).expanduser().resolve())

    def ask(self, prompt: str) -> None:
        self.bridge.status_ready.emit("Submitting question to local AI...")

        def task() -> None:
            try:
                messages = [
                    {
                        "role": "system",
                        "content": (
                            "You are a senior Python architecture analyst. "
                            "Answer only from the supplied evidence pack. "
                            "Do not invent files, classes, functions, or execution flows. "
                            "If evidence is insufficient, say so clearly. "
                            "Always cite ids like [F01], [S01], [SN01]."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ]
                answer = self.wrapper.chat(
                    messages,
                    temperature=0.1,
                    max_tokens=2200,
                )
                self.bridge.answer_ready.emit(answer)
            except Exception as exc:
                self.bridge.error_ready.emit(str(exc))

        AIRequestQueue().submit(task)

File 6
tools/project_reasoner_v8/v8_main_window.py

from __future__ import annotations

import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from .v8_ai_bridge import LocalAIReasoner
from .v8_index_loader import JsonProjectIndex
from .v8_models import EvidenceItem, RetrievalBundle, SymbolEvidenceItem
from .v8_prompt_builder import PromptBuilder
from .v8_retriever import ProjectRetriever


def shorten_path(path: str, max_len: int = 90) -> str:
    if len(path) <= max_len:
        return path
    return "..." + path[-(max_len - 3):]


class JsonProjectReasonerV8(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Project JSON Explorer v8 - Local AI Reasoner")
        self.resize(1800, 1040)

        self.project_index = JsonProjectIndex()
        self.retriever = ProjectRetriever(self.project_index)
        self.prompt_builder = PromptBuilder()
        self.ai = LocalAIReasoner()

        self._last_bundle = RetrievalBundle([], [], [])
        self._last_prompt = ""

        self.json_path_edit = QLineEdit()
        self.question_edit = QLineEdit()
        self.cache_dir_edit = QLineEdit()
        self.governance_path_edit = QLineEdit()

        self.load_button = QPushButton("Load JSON")
        self.ask_ai_button = QPushButton("Ask Local AI")
        self.clear_button = QPushButton("Clear")
        self.pick_cache_dir_button = QPushButton("Set Cache Dir")
        self.pick_governance_button = QPushButton("Set Governance State")

        self.quick_startup_button = QPushButton("Startup")
        self.quick_tabs_button = QPushButton("Tabs")
        self.quick_topomap_button = QPushButton("Topomap")
        self.quick_timeline_button = QPushButton("Timeline")
        self.quick_splash_button = QPushButton("Splash")
        self.quick_reset_button = QPushButton("Reset")

        self.file_evidence_list = QListWidget()
        self.symbol_evidence_list = QListWidget()
        self.detail_box = QPlainTextEdit()
        self.detail_box.setReadOnly(True)

        self.answer_box = QPlainTextEdit()
        self.answer_box.setReadOnly(True)

        self.prompt_preview = QPlainTextEdit()
        self.prompt_preview.setReadOnly(True)

        self.log_box = QPlainTextEdit()
        self.log_box.setReadOnly(True)

        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

        top_group = QGroupBox("Project JSON")
        top_layout = QGridLayout(top_group)
        top_layout.addWidget(QLabel("JSON file:"), 0, 0)
        top_layout.addWidget(self.json_path_edit, 0, 1)
        top_layout.addWidget(self.load_button, 0, 2)

        cfg_group = QGroupBox("Local AI Runtime")
        cfg_layout = QGridLayout(cfg_group)
        cfg_layout.addWidget(QLabel("Cache dir:"), 0, 0)
        cfg_layout.addWidget(self.cache_dir_edit, 0, 1)
        cfg_layout.addWidget(self.pick_cache_dir_button, 0, 2)
        cfg_layout.addWidget(QLabel("Governance state:"), 1, 0)
        cfg_layout.addWidget(self.governance_path_edit, 1, 1)
        cfg_layout.addWidget(self.pick_governance_button, 1, 2)

        ask_group = QGroupBox("Ask Complex Architecture Questions")
        ask_layout = QGridLayout(ask_group)
        ask_layout.addWidget(QLabel("Question:"), 0, 0)
        ask_layout.addWidget(self.question_edit, 0, 1)
        ask_layout.addWidget(self.ask_ai_button, 0, 2)
        ask_layout.addWidget(self.clear_button, 0, 3)

        quick_row = QHBoxLayout()
        quick_row.addWidget(self.quick_startup_button)
        quick_row.addWidget(self.quick_tabs_button)
        quick_row.addWidget(self.quick_topomap_button)
        quick_row.addWidget(self.quick_timeline_button)
        quick_row.addWidget(self.quick_splash_button)
        quick_row.addWidget(self.quick_reset_button)
        quick_row.addStretch()

        splitter = QSplitter(Qt.Horizontal)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(QLabel("File Evidence"))
        left_layout.addWidget(self.file_evidence_list)
        left_layout.addWidget(QLabel("Symbol Evidence"))
        left_layout.addWidget(self.symbol_evidence_list)
        left_layout.addWidget(QLabel("Selected Detail"))
        left_layout.addWidget(self.detail_box)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.addWidget(QLabel("Local AI Answer"))
        right_layout.addWidget(self.answer_box, stretch=2)
        right_layout.addWidget(QLabel("Prompt / Evidence Pack"))
        right_layout.addWidget(self.prompt_preview, stretch=1)

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([700, 1000])

        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout(log_group)
        log_layout.addWidget(self.log_box)

        main_layout.addWidget(top_group)
        main_layout.addWidget(cfg_group)
        main_layout.addWidget(ask_group)
        main_layout.addLayout(quick_row)
        main_layout.addWidget(splitter, stretch=1)
        main_layout.addWidget(log_group)

    def _connect_signals(self) -> None:
        self.load_button.clicked.connect(self.load_json)
        self.ask_ai_button.clicked.connect(self.ask_local_ai)
        self.clear_button.clicked.connect(self.clear_all)

        self.pick_cache_dir_button.clicked.connect(self.pick_cache_dir)
        self.pick_governance_button.clicked.connect(self.pick_governance_path)

        self.quick_startup_button.clicked.connect(
            lambda: self._run_quick_question("Which module starts the app and what is the startup chain?")
        )
        self.quick_tabs_button.clicked.connect(
            lambda: self._run_quick_question("Which code creates the superior tab and how are tabs constructed?")
        )
        self.quick_topomap_button.clicked.connect(
            lambda: self._run_quick_question("Show me which code is implementing topomap and how it is wired.")
        )
        self.quick_timeline_button.clicked.connect(
            lambda: self._run_quick_question("Explain the timeline architecture and which modules wire it.")
        )
        self.quick_splash_button.clicked.connect(
            lambda: self._run_quick_question("Where is splash created, shown, and hidden in the app?")
        )
        self.quick_reset_button.clicked.connect(
            lambda: self._run_quick_question("Explain reset and snapshot flow for EEG session state.")
        )

        self.question_edit.returnPressed.connect(self.ask_local_ai)
        self.file_evidence_list.currentItemChanged.connect(self._show_selected_file_detail)
        self.symbol_evidence_list.currentItemChanged.connect(self._show_selected_symbol_detail)

        self.ai.bridge.answer_ready.connect(self._on_ai_answer_ready)
        self.ai.bridge.error_ready.connect(self._on_ai_error_ready)
        self.ai.bridge.status_ready.connect(self._append_log)

    def _append_log(self, text: str) -> None:
        self.log_box.appendPlainText(text)

    def clear_all(self) -> None:
        self.file_evidence_list.clear()
        self.symbol_evidence_list.clear()
        self.detail_box.clear()
        self.answer_box.clear()
        self.prompt_preview.clear()
        self.log_box.clear()
        self._last_bundle = RetrievalBundle([], [], [])
        self._last_prompt = ""

    def _run_quick_question(self, question: str) -> None:
        self.question_edit.setText(question)
        self.ask_local_ai()

    def pick_cache_dir(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Select cache directory")
        if not path:
            return
        self.cache_dir_edit.setText(path)
        try:
            self.ai.set_cache_dir(path)
            self._append_log("Cache dir set: " + path)
        except Exception as exc:
            QMessageBox.warning(self, "Cache dir error", str(exc))

    def pick_governance_path(self) -> None:
        path, _filter = QFileDialog.getOpenFileName(
            self,
            "Select governance_state.json",
            os.getcwd(),
            "JSON Files (*.json)",
        )
        if not path:
            return
        self.governance_path_edit.setText(path)
        try:
            self.ai.set_governance_state_path(path)
            self._append_log("Governance state set: " + path)
        except Exception as exc:
            QMessageBox.warning(self, "Governance path error", str(exc))

    def load_json(self) -> None:
        current_path = self.json_path_edit.text().strip()
        start_dir = os.path.dirname(current_path) if current_path else os.getcwd()

        file_path, _filter = QFileDialog.getOpenFileName(
            self,
            "Select project_structure_index.json",
            start_dir,
            "JSON Files (*.json)",
        )
        if not file_path:
            return

        try:
            self.project_index.load_json(file_path)
            self.json_path_edit.setText(file_path)

            summary = (self.project_index.index_data or {}).get("project_summary", {})
            self._append_log("Loaded JSON: " + file_path)
            self._append_log("Project root: " + self.project_index.project_root)
            self._append_log("Python files: " + str(summary.get("python_file_count", "unknown")))
            self._append_log("Entry files: " + str(summary.get("entry_file_count", "unknown")))

            QMessageBox.information(self, "Loaded", "JSON loaded successfully.")
        except Exception as exc:
            QMessageBox.critical(self, "Error", "Failed to load JSON:\n" + str(exc))

    def ask_local_ai(self) -> None:
        if not self.project_index.index_data:
            QMessageBox.warning(self, "No JSON", "Please load a JSON file first.")
            return

        question = self.question_edit.text().strip()
        if not question:
            QMessageBox.warning(self, "No Question", "Please type a question.")
            return

        bundle = self.retriever.retrieve(
            question,
            file_limit=10,
            symbol_limit=10,
            snippet_limit=6,
        )

        if not bundle.file_evidence and not bundle.symbol_evidence:
            QMessageBox.information(self, "No Evidence", "No relevant evidence was retrieved.")
            return

        self._last_bundle = bundle
        self._populate_evidence_lists(bundle)

        summary = dict((self.project_index.index_data or {}).get("project_summary", {}))
        summary["entry_files"] = (self.project_index.index_data or {}).get("entry_files", [])

        prompt = self.prompt_builder.build(
            question=question,
            bundle=bundle,
            project_root=self.project_index.project_root,
            summary=summary,
        )
        self._last_prompt = prompt
        self.prompt_preview.setPlainText(prompt)
        self.answer_box.setPlainText("Thinking...")

        self.ai.ask(prompt)

    def _populate_evidence_lists(self, bundle: RetrievalBundle) -> None:
        self.file_evidence_list.clear()
        self.symbol_evidence_list.clear()
        self.detail_box.clear()

        for item in bundle.file_evidence:
            label = "[" + item.evidence_id + "] " + shorten_path(item.path) + " | score=" + str(item.score)
            list_item = QListWidgetItem(label)
            list_item.setData(Qt.UserRole, item.evidence_id)
            self.file_evidence_list.addItem(list_item)

        for item in bundle.symbol_evidence:
            label = (
                "[" + item.evidence_id + "] "
                + item.symbol_name
                + " @ "
                + shorten_path(item.path, 70)
                + ":"
                + str(item.line)
            )
            list_item = QListWidgetItem(label)
            list_item.setData(Qt.UserRole, item.evidence_id)
            self.symbol_evidence_list.addItem(list_item)

        if bundle.file_evidence:
            self.file_evidence_list.setCurrentRow(0)
        elif bundle.symbol_evidence:
            self.symbol_evidence_list.setCurrentRow(0)

    def _show_selected_file_detail(self, current: QListWidgetItem, previous: QListWidgetItem) -> None:
        _ = previous
        if not current:
            return
        evidence_id = current.data(Qt.UserRole)
        for item in self._last_bundle.file_evidence:
            if item.evidence_id == evidence_id:
                self.detail_box.setPlainText(item.detail)
                return

    def _show_selected_symbol_detail(self, current: QListWidgetItem, previous: QListWidgetItem) -> None:
        _ = previous
        if not current:
            return
        evidence_id = current.data(Qt.UserRole)
        for item in self._last_bundle.symbol_evidence:
            if item.evidence_id == evidence_id:
                self.detail_box.setPlainText(item.detail)
                return

    def _on_ai_answer_ready(self, text: str) -> None:
        self.answer_box.setPlainText(text)
        self._append_log("Local AI answer received.")

    def _on_ai_error_ready(self, error_text: str) -> None:
        self.answer_box.setPlainText("AI error:\n" + error_text)
        self._append_log("AI error: " + error_text)


def main() -> None:
    app = QApplication(sys.argv)
    window = JsonProjectReasonerV8()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

File 7
tools/project_reasoner_v8/__init__.py

from .v8_main_window import JsonProjectReasonerV8, main

How to run

From project root:

python -m tools.project_reasoner_v8.v8_main_window

Or create a tiny launcher:

tools/run_project_reasoner_v8.py

from tools.project_reasoner_v8.v8_main_window import main

if __name__ == "__main__":
    main()

Then run:

python tools\run_project_reasoner_v8.py

What Version 8 improves over Version 7

It is modular now.
Main window is much shorter.
Retrieval logic is separated.
Prompt building is separated.
AI bridge is separated.
Models are separated.

And functionally it is stronger because it now adds:
symbol retrieval
source snippet injection
file evidence + symbol evidence + snippet evidence in one prompt

Best next step after this

Version 9 should add conversation memory inside the GUI:
follow-up questions over the same loaded JSON
reuse previous evidence when relevant
buttons like:
Explain startup chain
Explain topomap chain
Explain timeline chain
Responsibility map
Uncertainty report

If you want, next I will build Version 9 in the same modular style, with a dedicated conversation memory helper file.

Version 9 should add conversation memory inside the GUI:
follow-up questions over the same loaded JSON
reuse previous evidence when relevant
buttons like:
Explain startup chain
Explain topomap chain
Explain timeline chain
Responsibility map
Uncertainty report

verify models present and  insert a dropdown to select model
Thought for 7s

Yes. Below is a modular Version 9 with:

conversation memory inside the GUI
follow-up questions over the same loaded JSON
reuse of prior evidence when relevant
quick buttons:
Explain startup chain
Explain topomap chain
Explain timeline chain
Responsibility map
Uncertainty report
local model verification against Ollama
a model dropdown populated from models that are actually present
manual refresh models button

Suggested structure:

tools/
    project_reasoner_v9/
        __init__.py
        v9_models.py
        v9_index_loader.py
        v9_retriever.py
        v9_prompt_builder.py
        v9_ai_bridge.py
        v9_model_registry.py
        v9_conversation_memory.py
        v9_main_window.py

tools/project_reasoner_v9/v9_models.py

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class EvidenceItem:
    evidence_id: str
    score: int
    path: str
    module_name: str
    reason: str
    detail: str


@dataclass
class SymbolEvidenceItem:
    evidence_id: str
    score: int
    symbol_name: str
    kind: str
    path: str
    line: int
    reason: str
    detail: str


@dataclass
class RetrievalBundle:
    file_evidence: list[EvidenceItem] = field(default_factory=list)
    symbol_evidence: list[SymbolEvidenceItem] = field(default_factory=list)
    snippet_evidence: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ConversationTurn:
    question: str
    answer: str
    prompt: str
    retrieval: RetrievalBundle
    selected_model: str

tools/project_reasoner_v9/v9_index_loader.py

from __future__ import annotations

import json
from collections import defaultdict
from typing import Any


class JsonProjectIndex:
    def __init__(self) -> None:
        self.index_data: dict[str, Any] | None = None
        self.project_root: str = ""
        self.files_by_path: dict[str, dict[str, Any]] = {}
        self.files_by_module: dict[str, dict[str, Any]] = {}
        self.semantic_roles: dict[str, dict[str, Any]] = {}
        self.symbol_details: dict[str, dict[str, Any]] = {}
        self.symbol_to_file: dict[str, set[str]] = defaultdict(set)
        self.import_graph_out: dict[str, set[str]] = defaultdict(set)
        self.call_graph_out: dict[str, set[str]] = defaultdict(set)

    def load_json(self, file_path: str) -> None:
        with open(file_path, "r", encoding="utf-8") as handle:
            self.index_data = json.load(handle)

        self.project_root = (
            self.index_data.get("project_summary", {}).get("project_root", "") or ""
        )
        self.semantic_roles = self.index_data.get("semantic_roles", {})
        self._rebuild_indexes()

    def _rebuild_indexes(self) -> None:
        self.files_by_path.clear()
        self.files_by_module.clear()
        self.symbol_details.clear()
        self.symbol_to_file.clear()
        self.import_graph_out.clear()
        self.call_graph_out.clear()

        if not self.index_data:
            return

        for file_record in self.index_data.get("files", []):
            path = file_record.get("path", "")
            module_name = file_record.get("module_name", "")

            if path:
                self.files_by_path[path] = file_record
            if module_name:
                self.files_by_module[module_name] = file_record

            for fn in file_record.get("functions", []):
                qualname = fn.get("qualname", "")
                if qualname:
                    self.symbol_details[qualname] = {
                        "file": path,
                        "line": int(fn.get("lineno", 1)),
                        "kind": "function",
                        "record": fn,
                    }
                    self.symbol_to_file[qualname].add(path)

            for cls in file_record.get("classes", []):
                cls_name = cls.get("name", "")
                if cls_name:
                    self.symbol_details[cls_name] = {
                        "file": path,
                        "line": int(cls.get("lineno", 1)),
                        "kind": "class",
                        "record": cls,
                    }
                    self.symbol_to_file[cls_name].add(path)

                for method in cls.get("methods", []):
                    qualname = method.get("qualname", "")
                    if qualname:
                        self.symbol_details[qualname] = {
                            "file": path,
                            "line": int(method.get("lineno", 1)),
                            "kind": "method",
                            "record": method,
                        }
                        self.symbol_to_file[qualname].add(path)

        for src_module, targets in self.index_data.get("import_graph", {}).items():
            src_path = self.resolve_module_to_path(src_module) or src_module
            for target in targets:
                self.import_graph_out[src_path].add(target)

        for edge in self.index_data.get("call_edges", []):
            from_file = edge.get("from_file", "")
            to_call = edge.get("to_call", "")
            if from_file and to_call:
                self.call_graph_out[from_file].add(to_call)

    def resolve_module_to_path(self, module_name: str) -> str | None:
        record = self.files_by_module.get(module_name)
        if record:
            return record.get("path")
        return None

tools/project_reasoner_v9/v9_retriever.py

from __future__ import annotations

import os
import re
from typing import Any

from .v9_index_loader import JsonProjectIndex
from .v9_models import EvidenceItem, RetrievalBundle, SymbolEvidenceItem


def norm_text(value: Any) -> str:
    return str(value).strip().lower() if value is not None else ""


def tokenize_query(text: str) -> list[str]:
    tokens = re.findall(r"[a-zA-Z0-9_\.]+", text.lower())
    stop_words = {
        "the",
        "is",
        "are",
        "a",
        "an",
        "of",
        "to",
        "me",
        "show",
        "which",
        "what",
        "where",
        "who",
        "does",
        "do",
        "in",
        "on",
        "for",
        "and",
        "or",
        "with",
        "code",
        "module",
        "file",
        "implementing",
        "implements",
        "created",
        "creates",
        "create",
        "that",
        "this",
        "app",
        "about",
        "how",
        "from",
        "explain",
    }
    return [token for token in tokens if token not in stop_words]


def safe_read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return handle.read()


class ProjectRetriever:
    def __init__(self, project_index: JsonProjectIndex) -> None:
        self.idx = project_index

    def retrieve(
        self,
        question: str,
        *,
        file_limit: int = 10,
        symbol_limit: int = 10,
        snippet_limit: int = 6,
    ) -> RetrievalBundle:
        file_evidence = self._retrieve_files(question, file_limit)
        symbol_evidence = self._retrieve_symbols(question, symbol_limit)
        snippet_evidence = self._retrieve_snippets(file_evidence, symbol_evidence, snippet_limit)
        return RetrievalBundle(
            file_evidence=file_evidence,
            symbol_evidence=symbol_evidence,
            snippet_evidence=snippet_evidence,
        )

    def merge_with_previous(
        self,
        current_bundle: RetrievalBundle,
        previous_bundle: RetrievalBundle,
        *,
        max_files: int = 14,
        max_symbols: int = 14,
        max_snippets: int = 10,
    ) -> RetrievalBundle:
        file_map: dict[str, EvidenceItem] = {}
        for item in current_bundle.file_evidence + previous_bundle.file_evidence:
            key = item.path
            old = file_map.get(key)
            if old is None or item.score > old.score:
                file_map[key] = item

        symbol_map: dict[str, SymbolEvidenceItem] = {}
        for item in current_bundle.symbol_evidence + previous_bundle.symbol_evidence:
            key = item.symbol_name
            old = symbol_map.get(key)
            if old is None or item.score > old.score:
                symbol_map[key] = item

        snippet_map: dict[tuple[str, int, str], dict[str, Any]] = {}
        for item in current_bundle.snippet_evidence + previous_bundle.snippet_evidence:
            key = (item.get("path", ""), int(item.get("line", 0)), item.get("anchor", ""))
            snippet_map[key] = item

        merged_files = sorted(file_map.values(), key=lambda x: (-x.score, x.path))[:max_files]
        merged_symbols = sorted(symbol_map.values(), key=lambda x: (-x.score, x.symbol_name))[:max_symbols]
        merged_snippets = list(snippet_map.values())[:max_snippets]

        for idx, item in enumerate(merged_files, start=1):
            item.evidence_id = "F" + str(idx).zfill(2)

        for idx, item in enumerate(merged_symbols, start=1):
            item.evidence_id = "S" + str(idx).zfill(2)

        for idx, item in enumerate(merged_snippets, start=1):
            item["snippet_id"] = "SN" + str(idx).zfill(2)

        return RetrievalBundle(
            file_evidence=merged_files,
            symbol_evidence=merged_symbols,
            snippet_evidence=merged_snippets,
        )

    def _retrieve_files(self, question: str, limit: int) -> list[EvidenceItem]:
        q = norm_text(question)
        tokens = tokenize_query(q)
        entry_files = set((self.idx.index_data or {}).get("entry_files", []))
        scored: list[EvidenceItem] = []

        for path, file_record in self.idx.files_by_path.items():
            module_name = file_record.get("module_name", "")
            docstring = file_record.get("docstring", "")
            strings = " ".join(file_record.get("strings", []))
            comments = " ".join(file_record.get("comments", []))
            entry_markers = " ".join(file_record.get("entry_markers", []))
            ui_hits = " ".join(file_record.get("ui_keyword_hits", []))
            eeg_hits = " ".join(file_record.get("eeg_keyword_hits", []))
            semantic_hints = " ".join(file_record.get("semantic_hints", []))
            roles = self.idx.semantic_roles.get(path, {}).get("roles", [])

            function_names: list[str] = []
            class_names: list[str] = []
            called_symbols: list[str] = []

            for fn in file_record.get("functions", []):
                function_names.append(fn.get("qualname", ""))
                function_names.append(fn.get("name", ""))
                for call in fn.get("calls", []):
                    called_symbols.append(call.get("call_name", ""))

            for cls in file_record.get("classes", []):
                class_names.append(cls.get("name", ""))
                for method in cls.get("methods", []):
                    function_names.append(method.get("qualname", ""))
                    function_names.append(method.get("name", ""))
                    for call in method.get("calls", []):
                        called_symbols.append(call.get("call_name", ""))

            haystack = " ".join(
                [
                    norm_text(path),
                    norm_text(module_name),
                    norm_text(docstring),
                    norm_text(strings),
                    norm_text(comments),
                    norm_text(entry_markers),
                    norm_text(ui_hits),
                    norm_text(eeg_hits),
                    norm_text(semantic_hints),
                    norm_text(" ".join(function_names)),
                    norm_text(" ".join(class_names)),
                    norm_text(" ".join(called_symbols)),
                    norm_text(" ".join(roles)),
                ]
            )

            score = 0
            reasons: list[str] = []

            for token in tokens:
                if token in haystack:
                    score += 3
                    reasons.append("token:" + token)

            if path in entry_files and any(key in q for key in ["start", "startup", "main", "launch", "open app"]):
                score += 14
                reasons.append("entry-file")

            if "topomap" in q and ("topomap" in haystack or "amplitude_map" in haystack):
                score += 12
                reasons.append("topomap-related")

            if "timeline" in q and "timeline" in haystack:
                score += 12
                reasons.append("timeline-related")

            if "splash" in q and "splash" in haystack:
                score += 12
                reasons.append("splash-related")

            if "tab" in q and ("tab" in haystack or "notebook" in haystack or "addtab" in haystack):
                score += 12
                reasons.append("tab-related")

            if ("reset" in q or "snapshot" in q) and ("reset" in haystack or "snapshot" in haystack):
                score += 12
                reasons.append("reset-related")

            if "responsibility" in q and ("manager" in haystack or "builder" in haystack or "controller" in haystack):
                score += 10
                reasons.append("responsibility-related")

            if "uncertainty" in q and ("warning" in haystack or "try" in haystack or "exception" in haystack):
                score += 8
                reasons.append("uncertainty-related")

            if score <= 0:
                continue

            detail = self._build_compact_file_evidence(path, reasons)
            scored.append(
                EvidenceItem(
                    evidence_id="",
                    score=score,
                    path=path,
                    module_name=module_name,
                    reason=", ".join(sorted(set(reasons))),
                    detail=detail,
                )
            )

        scored.sort(key=lambda item: (-item.score, item.path))
        scored = scored[:limit]

        reindexed: list[EvidenceItem] = []
        for idx, item in enumerate(scored, start=1):
            reindexed.append(
                EvidenceItem(
                    evidence_id="F" + str(idx).zfill(2),
                    score=item.score,
                    path=item.path,
                    module_name=item.module_name,
                    reason=item.reason,
                    detail=item.detail,
                )
            )
        return reindexed

    def _retrieve_symbols(self, question: str, limit: int) -> list[SymbolEvidenceItem]:
        q = norm_text(question)
        tokens = tokenize_query(q)
        scored: list[SymbolEvidenceItem] = []

        for symbol_name, detail in self.idx.symbol_details.items():
            record = detail["record"]
            blob = norm_text(symbol_name)
            docstring = norm_text(record.get("docstring", ""))
            calls_blob = ""

            if detail["kind"] in ("function", "method"):
                calls_blob = norm_text(" ".join([c.get("call_name", "") for c in record.get("calls", [])]))

            haystack = " ".join([blob, docstring, calls_blob])

            score = 0
            reasons: list[str] = []
            for token in tokens:
                if token in haystack:
                    score += 4
                    reasons.append("symbol-token:" + token)

            if score <= 0:
                continue

            scored.append(
                SymbolEvidenceItem(
                    evidence_id="",
                    score=score,
                    symbol_name=symbol_name,
                    kind=detail["kind"],
                    path=detail["file"],
                    line=detail["line"],
                    reason=", ".join(sorted(set(reasons))),
                    detail=self._build_symbol_evidence(symbol_name),
                )
            )

        scored.sort(key=lambda item: (-item.score, item.symbol_name))
        scored = scored[:limit]

        reindexed: list[SymbolEvidenceItem] = []
        for idx, item in enumerate(scored, start=1):
            reindexed.append(
                SymbolEvidenceItem(
                    evidence_id="S" + str(idx).zfill(2),
                    score=item.score,
                    symbol_name=item.symbol_name,
                    kind=item.kind,
                    path=item.path,
                    line=item.line,
                    reason=item.reason,
                    detail=item.detail,
                )
            )
        return reindexed

    def _retrieve_snippets(
        self,
        file_evidence: list[EvidenceItem],
        symbol_evidence: list[SymbolEvidenceItem],
        limit: int,
    ) -> list[dict[str, Any]]:
        snippets: list[dict[str, Any]] = []
        seen: set[tuple[str, int]] = set()

        for item in symbol_evidence:
            abs_path = os.path.join(self.idx.project_root, item.path)
            if not os.path.exists(abs_path):
                continue
            key = (item.path, item.line)
            if key in seen:
                continue
            seen.add(key)
            snippet_text = self._read_snippet(abs_path, item.line, radius=20)
            snippets.append(
                {
                    "snippet_id": "SN" + str(len(snippets) + 1).zfill(2),
                    "path": item.path,
                    "line": item.line,
                    "anchor": item.symbol_name,
                    "text": snippet_text,
                }
            )
            if len(snippets) >= limit:
                return snippets

        for item in file_evidence:
            abs_path = os.path.join(self.idx.project_root, item.path)
            if not os.path.exists(abs_path):
                continue
            key = (item.path, 1)
            if key in seen:
                continue
            seen.add(key)
            snippet_text = self._read_snippet(abs_path, 1, radius=40)
            snippets.append(
                {
                    "snippet_id": "SN" + str(len(snippets) + 1).zfill(2),
                    "path": item.path,
                    "line": 1,
                    "anchor": "file-start",
                    "text": snippet_text,
                }
            )
            if len(snippets) >= limit:
                return snippets

        return snippets

    def _read_snippet(self, abs_path: str, line: int, radius: int) -> str:
        text = safe_read_text(abs_path)
        lines = text.splitlines()
        if not lines:
            return ""

        start = max(1, line - radius)
        end = min(len(lines), line + radius)
        out: list[str] = []

        for idx in range(start, end + 1):
            out.append(str(idx).rjust(5) + " | " + lines[idx - 1])

        return "\n".join(out)

    def _build_compact_file_evidence(self, path: str, reasons: list[str]) -> str:
        file_record = self.idx.files_by_path[path]
        roles = self.idx.semantic_roles.get(path, {}).get("roles", [])

        lines: list[str] = []
        lines.append("Path: " + path)
        lines.append("Module: " + str(file_record.get("module_name", "")))
        lines.append("Reasons: " + ", ".join(sorted(set(reasons))))

        if roles:
            lines.append("Roles: " + ", ".join(roles))

        entry_markers = file_record.get("entry_markers", [])
        if entry_markers:
            lines.append("Entry markers: " + "; ".join(entry_markers[:6]))

        top_functions: list[str] = []
        for fn in file_record.get("functions", [])[:8]:
            top_functions.append(fn.get("qualname", "") + "@" + str(fn.get("lineno", "")))
        if top_functions:
            lines.append("Functions: " + " | ".join(top_functions))

        top_classes: list[str] = []
        for cls in file_record.get("classes", [])[:6]:
            class_text = cls.get("name", "") + "@" + str(cls.get("lineno", ""))
            methods = cls.get("methods", [])[:4]
            if methods:
                class_text += " methods=" + ",".join([m.get("name", "") for m in methods])
            top_classes.append(class_text)
        if top_classes:
            lines.append("Classes: " + " | ".join(top_classes))

        imports_out = sorted(self.idx.import_graph_out.get(path, []))
        if imports_out:
            lines.append("Imports out: " + " | ".join(imports_out[:8]))

        calls_out = sorted(self.idx.call_graph_out.get(path, []))
        if calls_out:
            lines.append("Calls out: " + " | ".join(calls_out[:10]))

        docstring = str(file_record.get("docstring", "")).strip()
        if docstring:
            docstring = re.sub(r"\s+", " ", docstring)
            lines.append("Docstring: " + docstring[:500])

        return "\n".join(lines)

    def _build_symbol_evidence(self, symbol_name: str) -> str:
        detail = self.idx.symbol_details[symbol_name]
        path = detail["file"]
        line = detail["line"]
        kind = detail["kind"]
        record = detail["record"]

        lines: list[str] = []
        lines.append("Symbol: " + symbol_name)
        lines.append("Kind: " + kind)
        lines.append("Location: " + path + ":" + str(line))

        if record.get("docstring"):
            docstring = re.sub(r"\s+", " ", str(record.get("docstring", "")).strip())
            lines.append("Docstring: " + docstring[:500])

        if kind in ("function", "method"):
            calls = [c.get("call_name", "") for c in record.get("calls", [])[:20]]
            if calls:
                lines.append("Calls: " + " | ".join(calls))

        return "\n".join(lines)

tools/project_reasoner_v9/v9_prompt_builder.py

from __future__ import annotations

from .v9_models import ConversationTurn, RetrievalBundle


class PromptBuilder:
    def build(
        self,
        question: str,
        bundle: RetrievalBundle,
        project_root: str,
        summary: dict,
        memory_turns: list[ConversationTurn],
    ) -> str:
        lines: list[str] = []

        lines.append("USER QUESTION")
        lines.append(question)
        lines.append("")
        lines.append("PROJECT SUMMARY")
        lines.append("Project root: " + str(project_root))
        lines.append("Python files indexed: " + str(summary.get("python_file_count", "")))
        lines.append("Entry files: " + ", ".join(summary.get("entry_files", [])))
        lines.append("")

        if memory_turns:
            lines.append("CONVERSATION MEMORY")
            for idx, turn in enumerate(memory_turns[-3:], start=1):
                lines.append("Previous question " + str(idx) + ": " + turn.question)
                lines.append("Previous answer " + str(idx) + ": " + turn.answer[:900])
                lines.append("Model: " + turn.selected_model)
                lines.append("")
        else:
            lines.append("CONVERSATION MEMORY")
            lines.append("None")
            lines.append("")

        lines.append("FILE EVIDENCE")
        for item in bundle.file_evidence:
            lines.append("[" + item.evidence_id + "] score=" + str(item.score))
            lines.append(item.detail)
            lines.append("")

        lines.append("SYMBOL EVIDENCE")
        for item in bundle.symbol_evidence:
            lines.append("[" + item.evidence_id + "] score=" + str(item.score))
            lines.append(item.detail)
            lines.append("")

        lines.append("SOURCE SNIPPETS")
        for item in bundle.snippet_evidence:
            lines.append(
                "[" + item["snippet_id"] + "] "
                + item["path"]
                + ":"
                + str(item["line"])
                + " anchor="
                + item["anchor"]
            )
            lines.append(item["text"])
            lines.append("")

        lines.append("INSTRUCTIONS")
        lines.append(
            "Answer strictly from the evidence above. "
            "Do not invent modules or flows. "
            "Use concrete names of files, classes, methods, and functions whenever present. "
            "Cite file evidence ids like [F01], symbol evidence ids like [S01], and snippet ids like [SN01]. "
            "For follow-up questions, reuse relevant earlier context only when consistent with current evidence. "
            "If evidence is incomplete, say exactly what is uncertain. "
            "When asked for responsibility map, group modules by responsibility. "
            "When asked for uncertainty report, explicitly list knowns, unknowns, and weak-evidence areas."
        )

        return "\n".join(lines)

tools/project_reasoner_v9/v9_model_registry.py

from __future__ import annotations

from typing import Any

import requests


OLLAMA_TAGS_URL = "http://127.0.0.1:11434/api/tags"
OLLAMA_MODELS_URL = "http://127.0.0.1:11434/v1/models"
TIMEOUT = 20


class LocalModelRegistry:
    def list_models(self) -> list[str]:
        models = self._from_tags()
        if models:
            return models

        models = self._from_v1_models()
        return models

    def _from_tags(self) -> list[str]:
        try:
            response = requests.get(OLLAMA_TAGS_URL, timeout=TIMEOUT)
            response.raise_for_status()
            data = response.json()
            items = data.get("models", [])
            out: list[str] = []
            for item in items:
                name = str(item.get("name", "")).strip()
                if name:
                    out.append(name)
            return sorted(set(out))
        except Exception:
            return []

    def _from_v1_models(self) -> list[str]:
        try:
            response = requests.get(OLLAMA_MODELS_URL, timeout=TIMEOUT)
            response.raise_for_status()
            data = response.json()
            items = data.get("data", [])
            out: list[str] = []
            for item in items:
                model_id = str(item.get("id", "")).strip()
                if model_id:
                    out.append(model_id)
            return sorted(set(out))
        except Exception:
            return []

tools/project_reasoner_v9/v9_conversation_memory.py

from __future__ import annotations

from .v9_models import ConversationTurn


class ConversationMemory:
    def __init__(self) -> None:
        self._turns: list[ConversationTurn] = []

    def add_turn(self, turn: ConversationTurn) -> None:
        self._turns.append(turn)

    def clear(self) -> None:
        self._turns.clear()

    def turns(self) -> list[ConversationTurn]:
        return list(self._turns)

    def last_turn(self) -> ConversationTurn | None:
        if not self._turns:
            return None
        return self._turns[-1]

tools/project_reasoner_v9/v9_ai_bridge.py

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject, Signal

from pykanda_ai.connectors.qwen_model_wrapper import QwenModelWrapper
from pykanda_ai.runtime.ai_request_queue import AIRequestQueue


class AIWorkerBridge(QObject):
    answer_ready = Signal(str)
    error_ready = Signal(str)
    status_ready = Signal(str)


class LocalAIReasoner:
    def __init__(self) -> None:
        self.wrapper = QwenModelWrapper()
        self.bridge = AIWorkerBridge()

    def set_cache_dir(self, cache_dir: str) -> None:
        self.wrapper.set_cache_dir(Path(cache_dir).expanduser().resolve())

    def set_governance_state_path(self, state_path: str) -> None:
        self.wrapper.set_governance_state_path(Path(state_path).expanduser().resolve())

    def ask(self, prompt: str, model_name: str) -> None:
        self.bridge.status_ready.emit("Submitting question to local AI using model: " + model_name)

        def task() -> None:
            try:
                messages = [
                    {
                        "role": "system",
                        "content": (
                            "You are a senior Python architecture analyst. "
                            "Answer only from the supplied evidence pack. "
                            "Do not invent files, classes, functions, or execution flows. "
                            "If evidence is insufficient, say so clearly. "
                            "Always cite ids like [F01], [S01], [SN01]."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ]
                answer = self.wrapper.chat(
                    messages,
                    model=model_name,
                    temperature=0.1,
                    max_tokens=2200,
                )
                self.bridge.answer_ready.emit(answer)
            except Exception as exc:
                self.bridge.error_ready.emit(str(exc))

        AIRequestQueue().submit(task)

tools/project_reasoner_v9/v9_main_window.py

from __future__ import annotations

import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from .v9_ai_bridge import LocalAIReasoner
from .v9_conversation_memory import ConversationMemory
from .v9_index_loader import JsonProjectIndex
from .v9_model_registry import LocalModelRegistry
from .v9_models import ConversationTurn, RetrievalBundle
from .v9_prompt_builder import PromptBuilder
from .v9_retriever import ProjectRetriever


def shorten_path(path: str, max_len: int = 90) -> str:
    if len(path) <= max_len:
        return path
    return "..." + path[-(max_len - 3):]


class JsonProjectReasonerV9(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Project JSON Explorer v9 - Local AI Reasoner")
        self.resize(1880, 1080)

        self.project_index = JsonProjectIndex()
        self.retriever = ProjectRetriever(self.project_index)
        self.prompt_builder = PromptBuilder()
        self.ai = LocalAIReasoner()
        self.memory = ConversationMemory()
        self.model_registry = LocalModelRegistry()

        self._last_bundle = RetrievalBundle([], [], [])
        self._last_prompt = ""
        self._last_selected_model = ""
        self._pending_question = ""

        self.json_path_edit = QLineEdit()
        self.question_edit = QLineEdit()
        self.cache_dir_edit = QLineEdit()
        self.governance_path_edit = QLineEdit()

        self.model_combo = QComboBox()
        self.refresh_models_button = QPushButton("Refresh Models")

        self.load_button = QPushButton("Load JSON")
        self.ask_ai_button = QPushButton("Ask Local AI")
        self.clear_button = QPushButton("Clear")
        self.clear_memory_button = QPushButton("Clear Memory")
        self.pick_cache_dir_button = QPushButton("Set Cache Dir")
        self.pick_governance_button = QPushButton("Set Governance State")

        self.quick_startup_button = QPushButton("Explain startup chain")
        self.quick_topomap_button = QPushButton("Explain topomap chain")
        self.quick_timeline_button = QPushButton("Explain timeline chain")
        self.quick_responsibility_button = QPushButton("Responsibility map")
        self.quick_uncertainty_button = QPushButton("Uncertainty report")

        self.file_evidence_list = QListWidget()
        self.symbol_evidence_list = QListWidget()
        self.history_list = QListWidget()

        self.detail_box = QPlainTextEdit()
        self.detail_box.setReadOnly(True)

        self.answer_box = QPlainTextEdit()
        self.answer_box.setReadOnly(True)

        self.prompt_preview = QPlainTextEdit()
        self.prompt_preview.setReadOnly(True)

        self.log_box = QPlainTextEdit()
        self.log_box.setReadOnly(True)

        self._build_ui()
        self._connect_signals()
        self.refresh_models()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

        top_group = QGroupBox("Project JSON")
        top_layout = QGridLayout(top_group)
        top_layout.addWidget(QLabel("JSON file:"), 0, 0)
        top_layout.addWidget(self.json_path_edit, 0, 1)
        top_layout.addWidget(self.load_button, 0, 2)

        cfg_group = QGroupBox("Local AI Runtime")
        cfg_layout = QGridLayout(cfg_group)
        cfg_layout.addWidget(QLabel("Cache dir:"), 0, 0)
        cfg_layout.addWidget(self.cache_dir_edit, 0, 1)
        cfg_layout.addWidget(self.pick_cache_dir_button, 0, 2)
        cfg_layout.addWidget(QLabel("Governance state:"), 1, 0)
        cfg_layout.addWidget(self.governance_path_edit, 1, 1)
        cfg_layout.addWidget(self.pick_governance_button, 1, 2)
        cfg_layout.addWidget(QLabel("Model:"), 2, 0)
        cfg_layout.addWidget(self.model_combo, 2, 1)
        cfg_layout.addWidget(self.refresh_models_button, 2, 2)

        ask_group = QGroupBox("Ask Complex Architecture Questions")
        ask_layout = QGridLayout(ask_group)
        ask_layout.addWidget(QLabel("Question:"), 0, 0)
        ask_layout.addWidget(self.question_edit, 0, 1)
        ask_layout.addWidget(self.ask_ai_button, 0, 2)
        ask_layout.addWidget(self.clear_button, 0, 3)
        ask_layout.addWidget(self.clear_memory_button, 0, 4)

        quick_row = QHBoxLayout()
        quick_row.addWidget(self.quick_startup_button)
        quick_row.addWidget(self.quick_topomap_button)
        quick_row.addWidget(self.quick_timeline_button)
        quick_row.addWidget(self.quick_responsibility_button)
        quick_row.addWidget(self.quick_uncertainty_button)
        quick_row.addStretch()

        splitter = QSplitter(Qt.Horizontal)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(QLabel("Conversation History"))
        left_layout.addWidget(self.history_list)
        left_layout.addWidget(QLabel("File Evidence"))
        left_layout.addWidget(self.file_evidence_list)
        left_layout.addWidget(QLabel("Symbol Evidence"))
        left_layout.addWidget(self.symbol_evidence_list)
        left_layout.addWidget(QLabel("Selected Detail"))
        left_layout.addWidget(self.detail_box)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.addWidget(QLabel("Local AI Answer"))
        right_layout.addWidget(self.answer_box, stretch=2)
        right_layout.addWidget(QLabel("Prompt / Evidence Pack"))
        right_layout.addWidget(self.prompt_preview, stretch=1)

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([720, 1050])

        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout(log_group)
        log_layout.addWidget(self.log_box)

        main_layout.addWidget(top_group)
        main_layout.addWidget(cfg_group)
        main_layout.addWidget(ask_group)
        main_layout.addLayout(quick_row)
        main_layout.addWidget(splitter, stretch=1)
        main_layout.addWidget(log_group)

    def _connect_signals(self) -> None:
        self.load_button.clicked.connect(self.load_json)
        self.ask_ai_button.clicked.connect(self.ask_local_ai)
        self.clear_button.clicked.connect(self.clear_visuals_only)
        self.clear_memory_button.clicked.connect(self.clear_memory)

        self.pick_cache_dir_button.clicked.connect(self.pick_cache_dir)
        self.pick_governance_button.clicked.connect(self.pick_governance_path)
        self.refresh_models_button.clicked.connect(self.refresh_models)

        self.quick_startup_button.clicked.connect(
            lambda: self._run_quick_question("Explain startup chain for the app step by step.")
        )
        self.quick_topomap_button.clicked.connect(
            lambda: self._run_quick_question("Explain topomap chain and how it is wired into the app.")
        )
        self.quick_timeline_button.clicked.connect(
            lambda: self._run_quick_question("Explain timeline chain and the flow between timeline modules.")
        )
        self.quick_responsibility_button.clicked.connect(
            lambda: self._run_quick_question("Create a responsibility map of the main modules in this app.")
        )
        self.quick_uncertainty_button.clicked.connect(
            lambda: self._run_quick_question("Create an uncertainty report about the architecture based on current evidence.")
        )

        self.question_edit.returnPressed.connect(self.ask_local_ai)
        self.file_evidence_list.currentItemChanged.connect(self._show_selected_file_detail)
        self.symbol_evidence_list.currentItemChanged.connect(self._show_selected_symbol_detail)
        self.history_list.currentItemChanged.connect(self._show_selected_history_turn)

        self.ai.bridge.answer_ready.connect(self._on_ai_answer_ready)
        self.ai.bridge.error_ready.connect(self._on_ai_error_ready)
        self.ai.bridge.status_ready.connect(self._append_log)

    def _append_log(self, text: str) -> None:
        self.log_box.appendPlainText(text)

    def refresh_models(self) -> None:
        self.model_combo.clear()
        models = self.model_registry.list_models()

        if not models:
            self.model_combo.addItem("qwen2.5-coder:7b")
            self.model_combo.addItem("qwen2.5-coder:32b")
            self._append_log("Could not verify models from Ollama. Added fallback model names.")
            return

        for model_name in models:
            self.model_combo.addItem(model_name)

        preferred = "qwen2.5-coder:7b"
        idx = self.model_combo.findText(preferred)
        if idx >= 0:
            self.model_combo.setCurrentIndex(idx)

        self._append_log("Verified models from Ollama: " + ", ".join(models))

    def clear_visuals_only(self) -> None:
        self.file_evidence_list.clear()
        self.symbol_evidence_list.clear()
        self.detail_box.clear()
        self.answer_box.clear()
        self.prompt_preview.clear()
        self.log_box.clear()
        self._last_bundle = RetrievalBundle([], [], [])
        self._last_prompt = ""

    def clear_memory(self) -> None:
        self.memory.clear()
        self.history_list.clear()
        self._append_log("Conversation memory cleared.")

    def _run_quick_question(self, question: str) -> None:
        self.question_edit.setText(question)
        self.ask_local_ai()

    def pick_cache_dir(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Select cache directory")
        if not path:
            return
        self.cache_dir_edit.setText(path)
        try:
            self.ai.set_cache_dir(path)
            self._append_log("Cache dir set: " + path)
        except Exception as exc:
            QMessageBox.warning(self, "Cache dir error", str(exc))

    def pick_governance_path(self) -> None:
        path, _filter = QFileDialog.getOpenFileName(
            self,
            "Select governance_state.json",
            os.getcwd(),
            "JSON Files (*.json)",
        )
        if not path:
            return
        self.governance_path_edit.setText(path)
        try:
            self.ai.set_governance_state_path(path)
            self._append_log("Governance state set: " + path)
        except Exception as exc:
            QMessageBox.warning(self, "Governance path error", str(exc))

    def load_json(self) -> None:
        current_path = self.json_path_edit.text().strip()
        start_dir = os.path.dirname(current_path) if current_path else os.getcwd()

        file_path, _filter = QFileDialog.getOpenFileName(
            self,
            "Select project_structure_index.json",
            start_dir,
            "JSON Files (*.json)",
        )
        if not file_path:
            return

        try:
            self.project_index.load_json(file_path)
            self.json_path_edit.setText(file_path)

            summary = (self.project_index.index_data or {}).get("project_summary", {})
            self._append_log("Loaded JSON: " + file_path)
            self._append_log("Project root: " + self.project_index.project_root)
            self._append_log("Python files: " + str(summary.get("python_file_count", "unknown")))
            self._append_log("Entry files: " + str(summary.get("entry_file_count", "unknown")))

            QMessageBox.information(self, "Loaded", "JSON loaded successfully.")
        except Exception as exc:
            QMessageBox.critical(self, "Error", "Failed to load JSON:\n" + str(exc))

    def ask_local_ai(self) -> None:
        if not self.project_index.index_data:
            QMessageBox.warning(self, "No JSON", "Please load a JSON file first.")
            return

        question = self.question_edit.text().strip()
        if not question:
            QMessageBox.warning(self, "No Question", "Please type a question.")
            return

        selected_model = self.model_combo.currentText().strip()
        if not selected_model:
            QMessageBox.warning(self, "No Model", "Please select a model.")
            return

        current_bundle = self.retriever.retrieve(
            question,
            file_limit=10,
            symbol_limit=10,
            snippet_limit=6,
        )

        if not current_bundle.file_evidence and not current_bundle.symbol_evidence:
            QMessageBox.information(self, "No Evidence", "No relevant evidence was retrieved.")
            return

        previous_turn = self.memory.last_turn()
        if previous_turn is not None:
            merged_bundle = self.retriever.merge_with_previous(
                current_bundle=current_bundle,
                previous_bundle=previous_turn.retrieval,
                max_files=14,
                max_symbols=14,
                max_snippets=10,
            )
        else:
            merged_bundle = current_bundle

        self._last_bundle = merged_bundle
        self._last_selected_model = selected_model
        self._pending_question = question
        self._populate_evidence_lists(merged_bundle)

        summary = dict((self.project_index.index_data or {}).get("project_summary", {}))
        summary["entry_files"] = (self.project_index.index_data or {}).get("entry_files", [])

        prompt = self.prompt_builder.build(
            question=question,
            bundle=merged_bundle,
            project_root=self.project_index.project_root,
            summary=summary,
            memory_turns=self.memory.turns(),
        )
        self._last_prompt = prompt
        self.prompt_preview.setPlainText(prompt)
        self.answer_box.setPlainText("Thinking...")

        self.ai.ask(prompt, selected_model)

    def _populate_evidence_lists(self, bundle: RetrievalBundle) -> None:
        self.file_evidence_list.clear()
        self.symbol_evidence_list.clear()
        self.detail_box.clear()

        for item in bundle.file_evidence:
            label = "[" + item.evidence_id + "] " + shorten_path(item.path) + " | score=" + str(item.score)
            list_item = QListWidgetItem(label)
            list_item.setData(Qt.UserRole, item.evidence_id)
            self.file_evidence_list.addItem(list_item)

        for item in bundle.symbol_evidence:
            label = (
                "[" + item.evidence_id + "] "
                + item.symbol_name
                + " @ "
                + shorten_path(item.path, 70)
                + ":"
                + str(item.line)
            )
            list_item = QListWidgetItem(label)
            list_item.setData(Qt.UserRole, item.evidence_id)
            self.symbol_evidence_list.addItem(list_item)

        if bundle.file_evidence:
            self.file_evidence_list.setCurrentRow(0)
        elif bundle.symbol_evidence:
            self.symbol_evidence_list.setCurrentRow(0)

    def _show_selected_file_detail(self, current: QListWidgetItem, previous: QListWidgetItem) -> None:
        _ = previous
        if not current:
            return
        evidence_id = current.data(Qt.UserRole)
        for item in self._last_bundle.file_evidence:
            if item.evidence_id == evidence_id:
                self.detail_box.setPlainText(item.detail)
                return

    def _show_selected_symbol_detail(self, current: QListWidgetItem, previous: QListWidgetItem) -> None:
        _ = previous
        if not current:
            return
        evidence_id = current.data(Qt.UserRole)
        for item in self._last_bundle.symbol_evidence:
            if item.evidence_id == evidence_id:
                self.detail_box.setPlainText(item.detail)
                return

    def _show_selected_history_turn(self, current: QListWidgetItem, previous: QListWidgetItem) -> None:
        _ = previous
        if not current:
            return
        row = self.history_list.row(current)
        turns = self.memory.turns()
        if row < 0 or row >= len(turns):
            return
        turn = turns[row]
        self.answer_box.setPlainText(turn.answer)
        self.prompt_preview.setPlainText(turn.prompt)

    def _refresh_history_list(self) -> None:
        self.history_list.clear()
        for idx, turn in enumerate(self.memory.turns(), start=1):
            label = str(idx) + ". " + turn.question
            item = QListWidgetItem(label)
            self.history_list.addItem(item)

    def _on_ai_answer_ready(self, text: str) -> None:
        self.answer_box.setPlainText(text)
        self._append_log("Local AI answer received.")

        turn = ConversationTurn(
            question=self._pending_question,
            answer=text,
            prompt=self._last_prompt,
            retrieval=self._last_bundle,
            selected_model=self._last_selected_model,
        )
        self.memory.add_turn(turn)
        self._refresh_history_list()

    def _on_ai_error_ready(self, error_text: str) -> None:
        self.answer_box.setPlainText("AI error:\n" + error_text)
        self._append_log("AI error: " + error_text)


def main() -> None:
    app = QApplication(sys.argv)
    window = JsonProjectReasonerV9()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

tools/project_reasoner_v9/__init__.py

from .v9_main_window import JsonProjectReasonerV9, main

Run it with:

python -m tools.project_reasoner_v9.v9_main_window

What changed in Version 9

It now has conversation memory inside the GUI.
Each new question can reuse prior evidence.
The last turn's retrieval bundle is merged with the current one.
There is a conversation history list on the left.
Selecting a past turn restores its answer and prompt preview.

It also verifies local models present.
It queries Ollama using:
/api/tags
and falls back to:
/v1/models

Then it fills a dropdown with the models that are actually installed locally.

The selected model is passed into:
QwenModelWrapper.chat(..., model=model_name)

Quick buttons now are:
Explain startup chain
Explain topomap chain
Explain timeline chain
Responsibility map
Uncertainty report

Recommended next step

Version 10 should add:
streaming answer display in the GUI
pinning evidence items so they persist across turns
a "strict follow-up mode" toggle that prefers previous context even more
export conversation as JSON or Markdown

create a tiny launcher:
Thought for 5s

Use this tiny launcher:

tools/run_project_reasoner_v9.py

from tools.project_reasoner_v9.v9_main_window import main


if __name__ == "__main__":
    main()

Run with:

python tools\run_project_reasoner_v9.py
streaming answer display in the GUI what is this?
Thought for a few seconds

It means the AI answer appears gradually in the text box while the model is generating, instead of waiting for the full response to finish.

Without streaming:
you click Ask
the GUI shows "Thinking..."
nothing appears for several seconds
then the full answer arrives at once

With streaming:
you click Ask
the first words start appearing almost immediately
the text keeps growing token by token or chunk by chunk
the user can watch the reasoning summary form live

In your GUI, that would mean:
the answer_box is cleared first
each incoming token is appended to answer_box
when generation finishes, the final text is saved into conversation memory

Why it is useful:
it feels much faster
better for long answers
you can see if the model is going in the wrong direction early
better UX for local models, which can be slower

In practice with your wrapper:
you already have a streaming method pattern in stream_summarize_module(...)
Version 10 would add a similar streamed chat method for general architecture questions, something like:
stream_chat(...)
Then the GUI would connect:
token callback -> append text to answer_box
done callback -> store final answer in memory/history

So the visible difference is:
now:
full answer appears only at the end

with streaming:
answer types itself live inside the GUI

If you want, next I can give you the exact minimal code changes to add streaming into your Version 9 without rewriting the whole app.

give you the exact minimal code changes to add streaming into your Version 9 without rewriting the whole app.
Thought for a couple of seconds

Yes. Here are the minimal changes.

Goal:
keep your Version 9 structure
do not rewrite the app
only add a streamed general chat path
append tokens live into answer_box
save final answer into memory when done

You need changes in only 2 files:

pykanda_ai/connectors/qwen_model_wrapper.py
tools/project_reasoner_v9/v9_ai_bridge.py

And one very small update in:
tools/project_reasoner_v9/v9_main_window.py

Update pykanda_ai/connectors/qwen_model_wrapper.py

Add this new method inside QwenModelWrapper class.

def stream_chat(
    self,
    messages: list[dict[str, Any]],
    *,
    model: str | None = None,
    temperature: float = 0.2,
    max_tokens: int | None = None,
    on_token: Callable[[str], None] | None = None,
    on_done: Callable[[str], None] | None = None,
    on_error: Callable[[str], None] | None = None,
) -> None:
    """
    Stream a generic chat completion.

    This is the streamed counterpart of chat(...).
    It applies the same governance modifier and emits text chunks live.
    """

    def task() -> None:
        try:
            model_to_use = model or FAST_MODEL
            modifier = self._get_governance_modifier()

            prepared_messages = [dict(message) for message in messages]

            if prepared_messages and prepared_messages[0].get("role") == "system":
                original_content = prepared_messages[0].get("content", "")
                prepared_messages[0]["content"] = f"{original_content}\n\n{modifier}"
            else:
                prepared_messages.insert(
                    0,
                    {
                        "role": "system",
                        "content": modifier,
                    },
                )

            payload: Dict[str, Any] = {
                "model": model_to_use,
                "messages": prepared_messages,
                "stream": True,
                "options": {
                    "temperature": temperature,
                },
            }

            if max_tokens is not None:
                payload["max_tokens"] = max_tokens

            full = ""

            with requests.post(
                OLLAMA_URL,
                json=payload,
                stream=True,
                timeout=TIMEOUT,
            ) as response:
                response.raise_for_status()

                for line in response.iter_lines():
                    if not line:
                        continue

                    if isinstance(line, (bytes, bytearray)):
                        line_str = line.decode("utf-8", errors="ignore").strip()
                    else:
                        line_str = str(line).strip()

                    if not line_str:
                        continue

                    if line_str.startswith("data:"):
                        line_str = line_str[len("data:"):].strip()

                    if not line_str or line_str == "[DONE]":
                        continue

                    try:
                        data = json.loads(line_str)
                    except Exception:
                        continue

                    token = (
                        data.get("choices", [{}])[0]
                        .get("delta", {})
                        .get("content", "")
                        or ""
                    )

                    if token:
                        full += token
                        if on_token:
                            on_token(token)

            if on_done:
                on_done(full)

        except Exception as exc:
            if on_error:
                on_error(str(exc))

    AIRequestQueue().submit(task)

Update tools/project_reasoner_v9/v9_ai_bridge.py

Replace the file with this updated version.

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject, Signal

from pykanda_ai.connectors.qwen_model_wrapper import QwenModelWrapper


class AIWorkerBridge(QObject):
    answer_ready = Signal(str)
    token_ready = Signal(str)
    error_ready = Signal(str)
    status_ready = Signal(str)


class LocalAIReasoner:
    def __init__(self) -> None:
        self.wrapper = QwenModelWrapper()

        self.bridge = AIWorkerBridge()

    def set_cache_dir(self, cache_dir: str) -> None:
        self.wrapper.set_cache_dir(Path(cache_dir).expanduser().resolve())

    def set_governance_state_path(self, state_path: str) -> None:
        self.wrapper.set_governance_state_path(Path(state_path).expanduser().resolve())

    def ask(self, prompt: str, model_name: str) -> None:
        self.bridge.status_ready.emit("Submitting question to local AI using model: " + model_name)

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a senior Python architecture analyst. "
                    "Answer only from the supplied evidence pack. "
                    "Do not invent files, classes, functions, or execution flows. "
                    "If evidence is insufficient, say so clearly. "
                    "Always cite ids like [F01], [S01], [SN01]."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]

        self.wrapper.stream_chat(
            messages,
            model=model_name,
            temperature=0.1,
            max_tokens=2200,
            on_token=self.bridge.token_ready.emit,
            on_done=self.bridge.answer_ready.emit,
            on_error=self.bridge.error_ready.emit,
        )

Update tools/project_reasoner_v9/v9_main_window.py

A. Add one signal connection inside _connect_signals

Find this block:

        self.ai.bridge.answer_ready.connect(self._on_ai_answer_ready)
        self.ai.bridge.error_ready.connect(self._on_ai_error_ready)
        self.ai.bridge.status_ready.connect(self._append_log)

Change to:

        self.ai.bridge.answer_ready.connect(self._on_ai_answer_ready)
        self.ai.bridge.token_ready.connect(self._on_ai_token_ready)
        self.ai.bridge.error_ready.connect(self._on_ai_error_ready)
        self.ai.bridge.status_ready.connect(self._append_log)

B. When asking, clear the answer box before streaming begins

Inside ask_local_ai, keep this line:

        self.answer_box.setPlainText("Thinking...")

Replace it with:

        self.answer_box.clear()

C. Add this new method inside JsonProjectReasonerV9

    def _on_ai_token_ready(self, token: str) -> None:
        cursor = self.answer_box.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(token)
        self.answer_box.setTextCursor(cursor)
        self.answer_box.ensureCursorVisible()

D. Keep _on_ai_answer_ready mostly the same

It should remain like this:

    def _on_ai_answer_ready(self, text: str) -> None:
        self.answer_box.setPlainText(text)
        self._append_log("Local AI answer received.")

        turn = ConversationTurn(
            question=self._pending_question,
            answer=text,
            prompt=self._last_prompt,
            retrieval=self._last_bundle,
            selected_model=self._last_selected_model,
        )
        self.memory.add_turn(turn)
        self._refresh_history_list()

This is okay because:
during generation, tokens appear live
at the end, the final full answer replaces the box content with the completed text
then it gets saved into memory

Result

After these changes, behavior becomes:

click Ask Local AI
answer_box starts empty
tokens appear live as they arrive
when finished, final answer is saved into history and memory

Optional tiny improvement

If you want a nicer UX, change:

        self.answer_box.clear()

to:

        self.answer_box.setPlainText("[Streaming...]\n\n")

Then change _on_ai_token_ready to append after that header.

Example:

    def _on_ai_token_ready(self, token: str) -> None:
        current = self.answer_box.toPlainText()
        if current == "[Streaming...]\n\n":
            self.answer_box.setPlainText("")
        cursor = self.answer_box.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(token)
        self.answer_box.setTextCursor(cursor)
        self.answer_box.ensureCursorVisible()

What this does not change

It does not change:
retrieval
conversation memory
model dropdown
prompt building
history storage

It only changes transport from:
full answer at end
to:
live streamed answer

Simple test

Run your launcher:

python tools\run_project_reasoner_v9.py

Then ask something long, for example:
Explain startup chain for the app step by step.

If streaming is working, text should appear gradually in the answer box instead of all at once.

If you want, next I can give you the fully merged final versions of those 3 files already patched for copy-paste.

pykanda_ai/connectors/qwen_model_wrapper.py

create a new connector exclusive for v9 in  v9_qwen_AI_models.py
Thought for 4s

Yes. That is a cleaner design.

Instead of modifying the global connector, create a V9-only connector and let the GUI use it.

Suggested new file:
tools/project_reasoner_v9/v9_qwen_ai_models.py

Use this full module:

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

import requests

from pykanda_ai.cortex.governance_state_reader import GovernanceStateReader
from pykanda_ai.runtime.ai_disk_cache import AIDiskCache
from pykanda_ai.runtime.ai_request_queue import AIRequestQueue


OLLAMA_URL = "http://127.0.0.1:11434/v1/chat/completions"

FAST_MODEL = "qwen2.5-coder:7b"
SMART_MODEL = "qwen2.5-coder:32b"

AUTO_THRESHOLD = 3000
TIMEOUT = 600


class V9QwenAIModels:
    """
    V9-exclusive local AI connector for project reasoner.

    Responsibilities:
    - generic non-stream chat
    - generic stream chat
    - model override support
    - governance modifier injection
    - optional persistent disk cache
    - async execution through AIRequestQueue
    """

    def __init__(self) -> None:
        self._governance_state_path = (
            Path(__file__).resolve().parent.parent.parent
            / "pykanda_ai"
            / "runtime"
            / "governance_state.json"
        )

    def set_cache_dir(self, cache_dir: Path) -> None:
        AIDiskCache().set_cache_dir(Path(cache_dir).expanduser().resolve())

    def set_governance_state_path(self, state_path: Path) -> None:
        self._governance_state_path = Path(state_path).expanduser().resolve()

    def _get_cache(self) -> AIDiskCache:
        return AIDiskCache()

    def _choose_model(self, text: str) -> str:
        return FAST_MODEL if len(text) < AUTO_THRESHOLD else SMART_MODEL

    def _post(self, payload: dict[str, Any]) -> dict[str, Any]:
        response = requests.post(OLLAMA_URL, json=payload, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()

    def _get_governance_modifier(self) -> str:
        state_reader = GovernanceStateReader(self._governance_state_path)
        mode = state_reader.get_mode()

        if mode == 0:
            return (
                "Operate normally. Prefer clarity and modularity. "
                "Allow reasonable refactoring."
            )

        if mode == 1:
            return (
                "Operate under elevated architectural caution. "
                "Avoid speculative refactors. "
                "Prioritize safety and stability."
            )

        if mode == 2:
            return (
                "SYSTEM IS IN FREEZE MODE. "
                "Do NOT propose structural changes. "
                "Only analyze and explain. "
                "No refactoring or architectural modification."
            )

        return ""

    def _prepare_messages(
        self,
        messages: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        modifier = self._get_governance_modifier()
        prepared_messages = [dict(message) for message in messages]

        if prepared_messages and prepared_messages[0].get("role") == "system":
            original_content = prepared_messages[0].get("content", "")
            prepared_messages[0]["content"] = f"{original_content}\n\n{modifier}"
        else:
            prepared_messages.insert(
                0,
                {
                    "role": "system",
                    "content": modifier,
                },
            )

        return prepared_messages

    def chat(
        self,
        messages: list[dict[str, Any]],
        *,
        model: str | None = None,
        temperature: float = 0.2,
        max_tokens: int | None = None,
        use_cache: bool = False,
        cache_key_data: dict[str, Any] | None = None,
    ) -> str:
        """
        Synchronous generic chat.

        Set use_cache=True only when the caller provides a stable cache_key_data.
        """
        cache = self._get_cache()

        if use_cache and cache_key_data:
            cached = cache.get(cache_key_data)
            if cached:
                return str(cached)

        model_to_use = model or self._choose_model(str(messages))
        prepared_messages = self._prepare_messages(messages)

        payload: dict[str, Any] = {
            "model": model_to_use,
            "messages": prepared_messages,
            "options": {
                "temperature": temperature,
            },
        }

        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        response = self._post(payload)

        text = (
            response.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )

        if use_cache and cache_key_data:
            cache.set(cache_key_data, text)

        return text

    def chat_async(
        self,
        messages: list[dict[str, Any]],
        *,
        model: str | None = None,
        temperature: float = 0.2,
        max_tokens: int | None = None,
        use_cache: bool = False,
        cache_key_data: dict[str, Any] | None = None,
        on_success: Callable[[str], None] | None = None,
        on_error: Callable[[str], None] | None = None,
    ) -> None:
        """
        Async generic chat.
        """

        def task() -> None:
            try:
                text = self.chat(
                    messages,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    use_cache=use_cache,
                    cache_key_data=cache_key_data,
                )
                if on_success:
                    on_success(text)
            except Exception as exc:
                if on_error:
                    on_error(str(exc))

        AIRequestQueue().submit(task)

    def stream_chat(
        self,
        messages: list[dict[str, Any]],
        *,
        model: str | None = None,
        temperature: float = 0.2,
        max_tokens: int | None = None,
        use_cache: bool = False,
        cache_key_data: dict[str, Any] | None = None,
        on_token: Callable[[str], None] | None = None,
        on_done: Callable[[str], None] | None = None,
        on_error: Callable[[str], None] | None = None,
    ) -> None:
        """
        Async streamed generic chat.

        Emits text chunks through on_token and the final full text through on_done.
        """

        def task() -> None:
            try:
                cache = self._get_cache()

                if use_cache and cache_key_data:
                    cached = cache.get(cache_key_data)
                    if cached:
                        cached_text = str(cached)
                        if on_token:
                            on_token(cached_text)
                        if on_done:
                            on_done(cached_text)
                        return

                model_to_use = model or self._choose_model(str(messages))
                prepared_messages = self._prepare_messages(messages)

                payload: dict[str, Any] = {
                    "model": model_to_use,
                    "messages": prepared_messages,
                    "stream": True,
                    "options": {
                        "temperature": temperature,
                    },
                }

                if max_tokens is not None:
                    payload["max_tokens"] = max_tokens

                full = ""

                with requests.post(
                    OLLAMA_URL,
                    json=payload,
                    stream=True,
                    timeout=TIMEOUT,
                ) as response:
                    response.raise_for_status()

                    for line in response.iter_lines():
                        if not line:
                            continue

                        if isinstance(line, (bytes, bytearray)):
                            line_str = line.decode("utf-8", errors="ignore").strip()
                        else:
                            line_str = str(line).strip()

                        if not line_str:
                            continue

                        if line_str.startswith("data:"):
                            line_str = line_str[len("data:"):].strip()

                        if not line_str or line_str == "[DONE]":
                            continue

                        try:
                            data = json.loads(line_str)
                        except Exception:
                            continue

                        token = (
                            data.get("choices", [{}])[0]
                            .get("delta", {})
                            .get("content", "")
                            or ""
                        )

                        if token:
                            full += token
                            if on_token:
                                on_token(token)

                if use_cache and cache_key_data:
                    cache.set(cache_key_data, full)

                if on_done:
                    on_done(full)

            except Exception as exc:
                if on_error:
                    on_error(str(exc))

        AIRequestQueue().submit(task)

Then update tools/project_reasoner_v9/v9_ai_bridge.py to import this V9-only connector instead of the shared one.

Use this full file:

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject, Signal

from tools.project_reasoner_v9.v9_qwen_ai_models import V9QwenAIModels


class AIWorkerBridge(QObject):
    answer_ready = Signal(str)
    token_ready = Signal(str)
    error_ready = Signal(str)
    status_ready = Signal(str)


class LocalAIReasoner:
    def __init__(self) -> None:
        self.wrapper = V9QwenAIModels()
        self.bridge = AIWorkerBridge()

    def set_cache_dir(self, cache_dir: str) -> None:
        self.wrapper.set_cache_dir(Path(cache_dir).expanduser().resolve())

    def set_governance_state_path(self, state_path: str) -> None:
        self.wrapper.set_governance_state_path(Path(state_path).expanduser().resolve())

    def ask(self, prompt: str, model_name: str) -> None:
        self.bridge.status_ready.emit(
            "Submitting question to local AI using model: " + model_name
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a senior Python architecture analyst. "
                    "Answer only from the supplied evidence pack. "
                    "Do not invent files, classes, functions, or execution flows. "
                    "If evidence is insufficient, say so clearly. "
                    "Always cite ids like [F01], [S01], [SN01]."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]

        cache_key_data = {
            "task": "v9_reasoner_chat",
            "model": model_name,
            "prompt": prompt,
        }

        self.wrapper.stream_chat(
            messages,
            model=model_name,
            temperature=0.1,
            max_tokens=2200,
            use_cache=True,
            cache_key_data=cache_key_data,
            on_token=self.bridge.token_ready.emit,
            on_done=self.bridge.answer_ready.emit,
            on_error=self.bridge.error_ready.emit,
        )

And in tools/project_reasoner_v9/v9_main_window.py, you do not need major changes if you already added streaming support. It should keep using:

self.ai.ask(prompt, selected_model)

Why this is better:
V9 becomes isolated from the global connector
you can evolve V9 behavior without touching the rest of PyKanda
you can add V9-specific cache keys, prompts, and streaming rules safely

If you want, next I can give you:
tools/project_reasoner_v9/v9_ai_bridge.py
and
tools/project_reasoner_v9/v9_main_window.py
already fully patched together for copy-paste.

I have ollama interface installed in window  how install and add deepseek to ollama models?
Thought for 10s

Sim. No Windows com Ollama, o caminho mais simples é puxar um modelo oficial da biblioteca do Ollama pelo terminal. O Ollama já oferece variantes oficiais do DeepSeek-R1, incluindo 1.5B, 7B, 8B, 14B, 32B, 70B e 671B, e a página da biblioteca mostra os comandos ollama run deepseek-r1:8b e as tags disponíveis.

O passo a passo:

Abra o terminal do Windows
Pode ser PowerShell, Prompt de Comando ou o terminal embutido da interface, se ela expuser o CLI do Ollama.

Confirme que o Ollama está funcionando
Execute:

ollama list

Se esse comando responder, o Ollama está instalado e acessível.

Veja quais modelos DeepSeek estão disponíveis
Você pode consultar a biblioteca oficial, que lista deepseek-r1, deepseek-v3.1, deepseek-v3.2 e outros modelos relacionados.

Puxe o modelo desejado
Exemplos comuns:

ollama pull deepseek-r1:1.5b
ollama pull deepseek-r1:7b
ollama pull deepseek-r1:8b
ollama pull deepseek-r1:14b
ollama pull deepseek-r1:32b

A tag deepseek-r1:latest aparece na biblioteca com cerca de 5.2 GB e 128K de contexto; a tag 32b aparece com cerca de 20 GB.

Rode o modelo
Depois do download:

ollama run deepseek-r1:7b

ou:

ollama run deepseek-r1:8b

A própria página oficial mostra esse padrão de uso.

Verifique se apareceu na sua interface
Depois do pull, rode:

ollama list

Se sua interface usa a mesma instalação local do Ollama, o modelo normalmente passa a aparecer na lista de modelos disponíveis.

Qual modelo escolher no seu PC
Como regra prática:

Se sua máquina tem pouca VRAM/RAM, comece por deepseek-r1:1.5b ou deepseek-r1:7b.
Se ela aguenta bem modelos médios, deepseek-r1:8b ou deepseek-r1:14b tendem a ser opções melhores.
deepseek-r1:32b já é bem pesado.
Os modelos muito grandes, como 70b e 671b, geralmente não são viáveis em um PC comum.

Se quiser um modelo DeepSeek mais focado em código
O Ollama também tem deepseek-coder, com exemplos como:

ollama pull deepseek-coder

ou

ollama pull deepseek-coder:6.7b

A biblioteca oficial do Ollama lista deepseek-coder com variantes 1.3B, 6.7B e 33B.

Se quiser algo mais novo da família DeepSeek
A biblioteca também lista deepseek-v3.1 e deepseek-v3.2. Além disso, a página do deepseek-v3 observa que ele requer Ollama 0.5.5 ou posterior.

Comandos mais úteis
Instalar:

ollama pull deepseek-r1:7b

Executar:

ollama run deepseek-r1:7b

Listar modelos instalados:

ollama list

Remover um modelo:

ollama rm deepseek-r1:7b

Se o modelo não aparecer na interface
Os motivos mais comuns são:
a interface está conectada a outra instância do Ollama
a interface precisa ser reiniciada
o pull não terminou
o nome da tag usada na interface não bate exatamente com o nome instalado

O que eu faria primeiro:
instalar deepseek-r1:7b
testar com ollama run deepseek-r1:7b
depois abrir sua interface e atualizar a lista de modelos

Se você me disser sua CPU, GPU, VRAM e RAM, eu te digo qual variante do DeepSeek vale mais a pena no seu computador.

minha placa é nvidea 4080rtx , qual versão do deepseek ollama é a adequada?
Thought for 11s

Com uma RTX 4080, a escolha mais equilibrada no Ollama costuma ser o DeepSeek-R1 14B para uso local sério, e o DeepSeek-R1 8B como opção mais leve e responsiva. A biblioteca oficial do Ollama lista as variantes do deepseek-r1 em 1.5B, 7B, 8B, 14B, 32B, 70B e 671B.

Na prática, eu recomendaria assim:

Melhor escolha geral para sua 4080:
deepseek-r1:14b

Melhor escolha para resposta mais rápida e menor consumo:
deepseek-r1:8b

Para programação especificamente, mais leve:
deepseek-coder:6.7b ou deepseek-coder-v2:16b (se quiser testar algo mais focado em código). O Ollama lista deepseek-coder em 1.3B, 6.7B e 33B, e também tem deepseek-coder-v2.

O que eu não escolheria como primeira opção na sua máquina:
deepseek-r1:32b para uso cotidiano local. Embora exista oficialmente no Ollama, ele já entra numa faixa bem mais pesada, e as variantes maiores da família vão muito além do que é confortável para uma 4080 doméstica. As tags oficiais incluem 32B, 70B e 671B; além disso, o deepseek-v3:latest aparece com cerca de 404 GB, claramente fora do alvo para uso local comum.

Minha recomendação objetiva para você:

Se quer qualidade + viabilidade local:

ollama pull deepseek-r1:14b

Se quer agilidade e menos chance de dor de cabeça:

ollama pull deepseek-r1:8b

Se quer foco em código:

ollama pull deepseek-coder:6.7b

E para testar:

ollama run deepseek-r1:14b

ou

ollama run deepseek-r1:8b

Se eu estivesse configurando o seu app de reasoner local agora, eu começaria com:
deepseek-r1:14b como modelo principal
e deixaria deepseek-r1:8b como fallback rápido.

how incorporate deepseek to v9 or it is automatically recognized?
Thought for 7s

In your V9 design, DeepSeek is automatically recognized if Ollama reports it.

Why:
your v9_model_registry.py already calls Ollama to list installed models
it checks:
/api/tags
and falls back to:
/v1/models

So if you install a model like:

ollama pull deepseek-r1:14b

then press Refresh Models in V9, it should appear in the dropdown automatically.

What happens next:
the selected dropdown value is passed into:

self.ai.ask(prompt, selected_model)

then into:

self.wrapper.stream_chat(..., model=model_name, ...)

So V9 does not need DeepSeek-specific code just to use it.
It is model-agnostic as long as Ollama exposes the model name.

When you do not need to change anything
You do not need code changes if all of these are true:
DeepSeek is installed in Ollama
Refresh Models shows it in the dropdown
you select it
V9 sends that exact model string to the connector

In that case, it is already incorporated.

When you may want a small improvement
You may still want to improve V9 so DeepSeek becomes nicer to use.

Useful upgrades:

Set DeepSeek as preferred default if installed
Right now V9 prefers qwen2.5-coder:7b.
You can change that so if deepseek-r1:14b exists, it becomes the default selected model.

In v9_main_window.py, inside refresh_models(), replace the preferred-model block with:

preferred_order = [
    "deepseek-r1:14b",
    "deepseek-r1:8b",
    "qwen2.5-coder:32b",
    "qwen2.5-coder:7b",
]

for preferred in preferred_order:
    idx = self.model_combo.findText(preferred)
    if idx >= 0:
        self.model_combo.setCurrentIndex(idx)
        break

Add model-specific system behavior
DeepSeek-R1 is often stronger for reasoning-style architecture answers.
You can tweak the system prompt in v9_ai_bridge.py depending on selected model.

Example:

system_prompt = (
    "You are a senior Python architecture analyst. "
    "Answer only from the supplied evidence pack. "
    "Do not invent files, classes, functions, or execution flows. "
    "If evidence is insufficient, say so clearly. "
    "Always cite ids like [F01], [S01], [SN01]."
)

if "deepseek" in model_name.lower():
    system_prompt += (
        " Think step by step internally, but present only the final concise architectural answer. "
        "Prefer execution chains, dependency flow, and responsibility decomposition."
    )

Then use system_prompt in the messages list.

Add a model badge in the GUI
This is optional, but useful so you always know whether the answer came from Qwen or DeepSeek.

Add per-model presets
Example:
DeepSeek: larger max tokens, lower temperature
Qwen coder: slightly shorter answers, more code-oriented style

Example in v9_ai_bridge.py:

temperature = 0.1
max_tokens = 2200

if "deepseek" in model_name.lower():
    temperature = 0.05
    max_tokens = 2600

Then pass those values into stream_chat(...).

Practical answer
So the answer is:

automatic recognition:
yes, if DeepSeek is installed in Ollama and your V9 model refresh sees it

manual incorporation:
only needed if you want DeepSeek-specific defaults or behavior

Best test
Do this:

Install DeepSeek in Ollama

ollama pull deepseek-r1:14b

Confirm it exists

ollama list

Open V9

Click Refresh Models

See whether deepseek-r1:14b appears in the dropdown

Select it

Ask a question

If it appears in the dropdown, then V9 is already using it correctly.

If you want, I can now give you the exact patched refresh_models() and v9_ai_bridge.py blocks so DeepSeek becomes the preferred default automatically.

and version 3 of deepseek do they fit my gforce 4080 16giga ? are they better programing python?
Thought for 8s

Provavelmente não. Para uma RTX 4080 de 16 GB, os modelos DeepSeek V3 da linha Ollama não são a escolha adequada para rodar localmente de forma confortável. No Ollama, o deepseek-v3:latest aparece com 404 GB de tamanho, muito além do que faz sentido para 16 GB de VRAM.

O mesmo vale para a linha mais nova exposta no Ollama:
deepseek-v3.1 aparece como cloud 671b, e deepseek-v3.2 também aparece como oferta em nuvem no catálogo, não como um modelo local leve para uma GPU de 16 GB.

Então, objetivamente:

DeepSeek V3 / V3.1 / V3.2
Não são boas opções para a sua 4080 16 GB, se a ideia é rodar localmente via Ollama.

DeepSeek-R1 8B ou 14B
Esses sim entram muito melhor no seu perfil de hardware. E, para uso local, são escolhas muito mais realistas. A biblioteca do Ollama lista essas variantes oficialmente.

Sobre “são melhores para programar Python?”:

Depende do que você chama de “melhor”.

Se você estiver comparando:
DeepSeek V3 grande na nuvem vs DeepSeek-R1 8B/14B local, a linha V3 é um modelo mais ambicioso e mais forte em termos gerais segundo a própria descrição oficial, mas isso não ajuda muito se ele não cabe no seu hardware local.

Para o seu uso real numa 4080 local, a comparação útil é:
DeepSeek-R1 14B
vs
Qwen coder 7B/32B
vs
DeepSeek-Coder 6.7B

Se o foco for programação Python local, eu colocaria assim:

Melhor equilíbrio geral para sua GPU
deepseek-r1:14b

Melhor foco específico em código leve
deepseek-coder:6.7b

O deepseek-coder continua sendo uma opção mais diretamente orientada a código do que V3/R1 em muitos fluxos práticos de desenvolvimento, e o Ollama mantém essa família disponível.

Minha recomendação prática para você:

Para arquitetura, reasoning e perguntas complexas sobre app:
deepseek-r1:14b

Para tarefas mais diretamente de código Python:
deepseek-coder:6.7b

Para resposta mais rápida e leve:
deepseek-r1:8b

Eu não investiria tempo tentando encaixar DeepSeek V3 localmente na sua 4080 16 GB. Ele simplesmente não é a categoria certa para esse hardware.

Comandos mais adequados para você:

ollama pull deepseek-r1:14b
ollama pull deepseek-r1:8b
ollama pull deepseek-coder:6.7b

Se quiser, eu posso te dizer qual deles faz mais sentido especificamente para o seu V9 reasoner GUI e qual faz mais sentido para programar Python no dia a dia.

create a small runner for v9
Thought for a couple of seconds

Use this small runner:

tools/run_project_reasoner_v9.py

from tools.project_reasoner_v9.v9_main_window import main


if __name__ == "__main__":
    main()

Run it with:

python tools\run_project_reasoner_v9.py
E:\mne_py3.10\python.exe "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9\run_project_reasoner_v9.py" 
Traceback (most recent call last):
  File "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9\run_project_reasoner_v9.py", line 1, in <module>
    from v9_main_window import main
  File "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9\v9_main_window.py", line 27, in <module>
    from .v9_ai_bridge import LocalAIReasoner
ImportError: attempted relative import with no known parent package

Process finished with exit code 1

all projecreareasoner  v9 files are in DEVELOPER TOOLS/FULL_INSPECTOR_JSON_APP/project_reasoner_v9
Thought for a couple of seconds

You are getting that error because v9_main_window.py uses relative imports like:

from .v9_ai_bridge import LocalAIReasoner

and you are launching run_project_reasoner_v9.py as a plain script inside that folder, so Python does not treat it as a package.

Use one of these fixes.

Best fix

Make sure this file exists:

DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9\__init__.py

It can be empty.

Move the runner one level above the package folder.

Create:

DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\run_project_reasoner_v9.py

with:

from project_reasoner_v9.v9_main_window import main


if __name__ == "__main__":
    main()

Run this file instead:

E:\mne_py3.10\python.exe "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\run_project_reasoner_v9.py"

Alternative fix

Keep the runner inside project_reasoner_v9, but then you must remove all relative imports in the V9 files and replace them with direct imports, for example:

in v9_main_window.py

from v9_ai_bridge import LocalAIReasoner
from v9_conversation_memory import ConversationMemory
from v9_index_loader import JsonProjectIndex
from v9_model_registry import LocalModelRegistry
from v9_models import ConversationTurn, RetrievalBundle
from v9_prompt_builder import PromptBuilder
from v9_retriever import ProjectRetriever

and do the same in the other V9 files.

I do not recommend that version. The package-based fix is cleaner.

So your final structure should be:

DEVELOPER TOOLS/
    FULL_INSPECTOR_JSON_APP/
        run_project_reasoner_v9.py
        project_reasoner_v9/
            __init__.py
            v9_main_window.py
            v9_ai_bridge.py
            v9_conversation_memory.py
            v9_index_loader.py
            v9_model_registry.py
            v9_models.py
            v9_prompt_builder.py
            v9_retriever.py
            v9_qwen_ai_models.py

If you want, paste your current run_project_reasoner_v9.py and I will adapt it exactly to your folder layout.

E:\mne_py3.10\python.exe "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9\run_project_reasoner_v9.py" 
Traceback (most recent call last):
  File "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9\run_project_reasoner_v9.py", line 1, in <module>
    from v9_main_window import main
  File "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9\v9_main_window.py", line 27, in <module>
    from v9_ai_bridge import LocalAIReasoner
  File "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9\v9_ai_bridge.py", line 7, in <module>
    from tools.project_reasoner_v9.v9_qwen_ai_models import V9QwenAIModels
ModuleNotFoundError: No module named 'tools'

# DEVELOPER TOOLS/FULL_INSPECTOR_JSON_APP/project_reasoner_v9/run_project_reasoner_v9.py

from v9_main_window import main


if __name__ == "__main__":
    main()
Thought for 6s

The error is now simpler:

v9_ai_bridge.py still has this import:

from tools.project_reasoner_v9.v9_qwen_ai_models import V9QwenAIModels

But in your real folder layout there is no tools package.
All V9 files are together in:

DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9

So for your current layout, use local same-folder imports.

Change this file:

DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9\v9_ai_bridge.py

Replace:

from tools.project_reasoner_v9.v9_qwen_ai_models import V9QwenAIModels

with:

from v9_qwen_ai_models import V9QwenAIModels

Your runner can stay as:

DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9\run_project_reasoner_v9.py

from v9_main_window import main


if __name__ == "__main__":
    main()

Also make sure the other V9 files are using same-folder imports, not package imports.

For your current layout, they should look like this:

In v9_main_window.py:

from v9_ai_bridge import LocalAIReasoner
from v9_conversation_memory import ConversationMemory
from v9_index_loader import JsonProjectIndex
from v9_model_registry import LocalModelRegistry
from v9_models import ConversationTurn, RetrievalBundle
from v9_prompt_builder import PromptBuilder
from v9_retriever import ProjectRetriever

In v9_prompt_builder.py:

from v9_models import ConversationTurn, RetrievalBundle

In v9_retriever.py:

from v9_index_loader import JsonProjectIndex
from v9_models import EvidenceItem, RetrievalBundle, SymbolEvidenceItem

In v9_conversation_memory.py:

from v9_models import ConversationTurn

After that, run again with:

E:\mne_py3.10\python.exe "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9\run_project_reasoner_v9.py"

If you want, paste the first 15 lines of:
v9_main_window.py
v9_ai_bridge.py
v9_retriever.py
v9_prompt_builder.py

and I will normalize all imports exactly for your folder layout.

E:\mne_py3.10\python.exe "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9\run_project_reasoner_v9.py" 
Traceback (most recent call last):
  File "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9\run_project_reasoner_v9.py", line 3, in <module>
    from v9_main_window import main
  File "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9\v9_main_window.py", line 27, in <module>
    from v9_ai_bridge import LocalAIReasoner
  File "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9\v9_ai_bridge.py", line 7, in <module>
    from v9_qwen_ai_models import V9QwenAIModels
  File "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9\v9_qwen_ai_models.py", line 9, in <module>
    from pykanda_ai.cortex.governance_state_reader import GovernanceStateReader
ModuleNotFoundError: No module named 'pykanda_ai'

use exclusive ai file 

# DEVELOPER TOOLS/FULL_INSPECTOR_JSON_APP/project_reasoner_v9/v9_qwen_ai_models.py

from __future__ import annotations



import json
from pathlib import Path
from typing import Any, Callable

import requests

from pykanda_ai.cortex.governance_state_reader import GovernanceStateReader
from pykanda_ai.runtime.ai_disk_cache import AIDiskCache
from pykanda_ai.runtime.ai_request_queue import AIRequestQueue


OLLAMA_URL = "http://127.0.0.1:11434/v1/chat/completions"

FAST_MODEL = "qwen2.5-coder:7b"
SMART_MODEL = "qwen2.5-coder:32b"

AUTO_THRESHOLD = 3000
TIMEOUT = 600


class V9QwenAIModels:
    """
    V9-exclusive local AI connector for project reasoner.

    Responsibilities:
    - generic non-stream chat
    - generic stream chat
    - model override support
    - governance modifier injection
    - optional persistent disk cache
    - async execution through AIRequestQueue
    """

    def __init__(self) -> None:
        self._governance_state_path = (
            Path(__file__).resolve().parent.parent.parent
            / "pykanda_ai"
            / "runtime"
            / "governance_state.json"
        )

    def set_cache_dir(self, cache_dir: Path) -> None:
        AIDiskCache().set_cache_dir(Path(cache_dir).expanduser().resolve())

    def set_governance_state_path(self, state_path: Path) -> None:
        self._governance_state_path = Path(state_path).expanduser().resolve()

    def _get_cache(self) -> AIDiskCache:
        return AIDiskCache()

    def _choose_model(self, text: str) -> str:
        return FAST_MODEL if len(text) < AUTO_THRESHOLD else SMART_MODEL

    def _post(self, payload: dict[str, Any]) -> dict[str, Any]:
        response = requests.post(OLLAMA_URL, json=payload, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()

    def _get_governance_modifier(self) -> str:
        state_reader = GovernanceStateReader(self._governance_state_path)
        mode = state_reader.get_mode()

        if mode == 0:
            return (
                "Operate normally. Prefer clarity and modularity. "
                "Allow reasonable refactoring."
            )

        if mode == 1:
            return (
                "Operate under elevated architectural caution. "
                "Avoid speculative refactors. "
                "Prioritize safety and stability."
            )

        if mode == 2:
            return (
                "SYSTEM IS IN FREEZE MODE. "
                "Do NOT propose structural changes. "
                "Only analyze and explain. "
                "No refactoring or architectural modification."
            )

        return ""

    def _prepare_messages(
        self,
        messages: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        modifier = self._get_governance_modifier()
        prepared_messages = [dict(message) for message in messages]

        if prepared_messages and prepared_messages[0].get("role") == "system":
            original_content = prepared_messages[0].get("content", "")
            prepared_messages[0]["content"] = f"{original_content}\n\n{modifier}"
        else:
            prepared_messages.insert(
                0,
                {
                    "role": "system",
                    "content": modifier,
                },
            )

        return prepared_messages

    def chat(
        self,
        messages: list[dict[str, Any]],
        *,
        model: str | None = None,
        temperature: float = 0.2,
        max_tokens: int | None = None,
        use_cache: bool = False,
        cache_key_data: dict[str, Any] | None = None,
    ) -> str:
        """
        Synchronous generic chat.

        Set use_cache=True only when the caller provides a stable cache_key_data.
        """
        cache = self._get_cache()

        if use_cache and cache_key_data:
            cached = cache.get(cache_key_data)
            if cached:
                return str(cached)

        model_to_use = model or self._choose_model(str(messages))
        prepared_messages = self._prepare_messages(messages)

        payload: dict[str, Any] = {
            "model": model_to_use,
            "messages": prepared_messages,
            "options": {
                "temperature": temperature,
            },
        }

        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        response = self._post(payload)

        text = (
            response.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )

        if use_cache and cache_key_data:
            cache.set(cache_key_data, text)

        return text

    def chat_async(
        self,
        messages: list[dict[str, Any]],
        *,
        model: str | None = None,
        temperature: float = 0.2,
        max_tokens: int | None = None,
        use_cache: bool = False,
        cache_key_data: dict[str, Any] | None = None,
        on_success: Callable[[str], None] | None = None,
        on_error: Callable[[str], None] | None = None,
    ) -> None:
        """
        Async generic chat.
        """

        def task() -> None:
            try:
                text = self.chat(
                    messages,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    use_cache=use_cache,
                    cache_key_data=cache_key_data,
                )
                if on_success:
                    on_success(text)
            except Exception as exc:
                if on_error:
                    on_error(str(exc))

        AIRequestQueue().submit(task)

    def stream_chat(
        self,
        messages: list[dict[str, Any]],
        *,
        model: str | None = None,
        temperature: float = 0.2,
        max_tokens: int | None = None,
        use_cache: bool = False,
        cache_key_data: dict[str, Any] | None = None,
        on_token: Callable[[str], None] | None = None,
        on_done: Callable[[str], None] | None = None,
        on_error: Callable[[str], None] | None = None,
    ) -> None:
        """
        Async streamed generic chat.

        Emits text chunks through on_token and the final full text through on_done.
        """

        def task() -> None:
            try:
                cache = self._get_cache()

                if use_cache and cache_key_data:
                    cached = cache.get(cache_key_data)
                    if cached:
                        cached_text = str(cached)
                        if on_token:
                            on_token(cached_text)
                        if on_done:
                            on_done(cached_text)
                        return

                model_to_use = model or self._choose_model(str(messages))
                prepared_messages = self._prepare_messages(messages)

                payload: dict[str, Any] = {
                    "model": model_to_use,
                    "messages": prepared_messages,
                    "stream": True,
                    "options": {
                        "temperature": temperature,
                    },
                }

                if max_tokens is not None:
                    payload["max_tokens"] = max_tokens

                full = ""

                with requests.post(
                    OLLAMA_URL,
                    json=payload,
                    stream=True,
                    timeout=TIMEOUT,
                ) as response:
                    response.raise_for_status()

                    for line in response.iter_lines():
                        if not line:
                            continue

                        if isinstance(line, (bytes, bytearray)):
                            line_str = line.decode("utf-8", errors="ignore").strip()
                        else:
                            line_str = str(line).strip()

                        if not line_str:
                            continue

                        if line_str.startswith("data:"):
                            line_str = line_str[len("data:"):].strip()

                        if not line_str or line_str == "[DONE]":
                            continue

                        try:
                            data = json.loads(line_str)
                        except Exception:
                            continue

                        token = (
                            data.get("choices", [{}])[0]
                            .get("delta", {})
                            .get("content", "")
                            or ""
                        )

                        if token:
                            full += token
                            if on_token:
                                on_token(token)

                if use_cache and cache_key_data:
                    cache.set(cache_key_data, full)

                if on_done:
                    on_done(full)

            except Exception as exc:
                if on_error:
                    on_error(str(exc))

        AIRequestQueue().submit(task)
Thought for 5s

Yes. The problem is that your current v9_qwen_ai_models.py still depends on pykanda_ai, so it is not truly exclusive.

Below is a fully self-contained replacement for:

DEVELOPER TOOLS/FULL_INSPECTOR_JSON_APP/project_reasoner_v9/v9_qwen_ai_models.py

It removes these external dependencies:
pykanda_ai.cortex.governance_state_reader
pykanda_ai.runtime.ai_disk_cache
pykanda_ai.runtime.ai_request_queue

It includes:
a tiny local governance reader
a tiny local disk cache
a tiny local single-worker request queue

Copy-paste this whole file.

from __future__ import annotations

import hashlib
import json
import queue
import threading
from pathlib import Path
from typing import Any, Callable

import requests


OLLAMA_URL = "http://127.0.0.1:11434/v1/chat/completions"

FAST_MODEL = "qwen2.5-coder:7b"
SMART_MODEL = "qwen2.5-coder:32b"

AUTO_THRESHOLD = 3000
TIMEOUT = 600


class _LocalGovernanceStateReader:
    """
    Minimal local governance reader for V9 only.

    Expected JSON shape:
    {
        "mode": 0
    }

    If file is missing or invalid, mode 0 is used.
    """

    def __init__(self, state_path: Path) -> None:
        self.state_path = Path(state_path).expanduser().resolve()

    def get_mode(self) -> int:
        try:
            if not self.state_path.exists():
                return 0

            with open(self.state_path, "r", encoding="utf-8", errors="replace") as handle:
                data = json.load(handle)

            mode = data.get("mode", 0)
            return int(mode)
        except Exception:
            return 0


class _LocalDiskCache:
    """
    Tiny JSON-on-disk cache for V9 only.
    """

    def __init__(self) -> None:
        self._cache_dir = Path(__file__).resolve().parent / "_v9_cache"
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def set_cache_dir(self, cache_dir: Path) -> None:
        resolved = Path(cache_dir).expanduser().resolve()
        resolved.mkdir(parents=True, exist_ok=True)
        self._cache_dir = resolved

    def _key_to_path(self, key_data: dict[str, Any]) -> Path:
        stable_text = json.dumps(key_data, sort_keys=True, ensure_ascii=True)
        digest = hashlib.sha256(stable_text.encode("utf-8", errors="replace")).hexdigest()
        return self._cache_dir / (digest + ".json")

    def get(self, key_data: dict[str, Any]) -> Any | None:
        try:
            cache_path = self._key_to_path(key_data)
            if not cache_path.exists():
                return None

            with self._lock:
                with open(cache_path, "r", encoding="utf-8", errors="replace") as handle:
                    payload = json.load(handle)

            return payload.get("value")
        except Exception:
            return None

    def set(self, key_data: dict[str, Any], value: Any) -> None:
        try:
            cache_path = self._key_to_path(key_data)
            payload = {
                "key": key_data,
                "value": value,
            }

            with self._lock:
                with open(cache_path, "w", encoding="utf-8", errors="replace") as handle:
                    json.dump(payload, handle, ensure_ascii=False, indent=2)
        except Exception:
            pass


class _LocalAIRequestQueue:
    """
    Tiny single-worker background queue for V9 only.
    Prevents GUI freeze and serializes model calls.
    """

    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._init_once()
        return cls._instance

    def _init_once(self) -> None:
        self._queue: queue.Queue[Callable[[], None]] = queue.Queue()
        self._worker = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker.start()

    def _worker_loop(self) -> None:
        while True:
            task = self._queue.get()
            try:
                task()
            except Exception:
                pass
            finally:
                self._queue.task_done()

    def submit(self, task: Callable[[], None]) -> None:
        self._queue.put(task)


class V9QwenAIModels:
    """
    V9-exclusive local AI connector.

    Responsibilities:
    - generic non-stream chat
    - generic stream chat
    - model override support
    - governance modifier injection
    - optional persistent disk cache
    - async execution through a local single-worker queue
    """

    def __init__(self) -> None:
        self._governance_state_path = (
            Path(__file__).resolve().parent / "governance_state.json"
        )
        self._cache = _LocalDiskCache()
        self._request_queue = _LocalAIRequestQueue()

    def set_cache_dir(self, cache_dir: Path) -> None:
        self._cache.set_cache_dir(Path(cache_dir).expanduser().resolve())

    def set_governance_state_path(self, state_path: Path) -> None:
        self._governance_state_path = Path(state_path).expanduser().resolve()

    def _choose_model(self, text: str) -> str:
        return FAST_MODEL if len(text) < AUTO_THRESHOLD else SMART_MODEL

    def _post(self, payload: dict[str, Any]) -> dict[str, Any]:
        response = requests.post(OLLAMA_URL, json=payload, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()

    def _get_governance_modifier(self) -> str:
        state_reader = _LocalGovernanceStateReader(self._governance_state_path)
        mode = state_reader.get_mode()

        if mode == 0:
            return (
                "Operate normally. Prefer clarity and modularity. "
                "Allow reasonable refactoring."
            )

        if mode == 1:
            return (
                "Operate under elevated architectural caution. "
                "Avoid speculative refactors. "
                "Prioritize safety and stability."
            )

        if mode == 2:
            return (
                "SYSTEM IS IN FREEZE MODE. "
                "Do NOT propose structural changes. "
                "Only analyze and explain. "
                "No refactoring or architectural modification."
            )

        return ""

    def _prepare_messages(
        self,
        messages: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        modifier = self._get_governance_modifier()
        prepared_messages = [dict(message) for message in messages]

        if prepared_messages and prepared_messages[0].get("role") == "system":
            original_content = prepared_messages[0].get("content", "")
            prepared_messages[0]["content"] = f"{original_content}\n\n{modifier}"
        else:
            prepared_messages.insert(
                0,
                {
                    "role": "system",
                    "content": modifier,
                },
            )

        return prepared_messages

    def chat(
        self,
        messages: list[dict[str, Any]],
        *,
        model: str | None = None,
        temperature: float = 0.2,
        max_tokens: int | None = None,
        use_cache: bool = False,
        cache_key_data: dict[str, Any] | None = None,
    ) -> str:
        """
        Synchronous generic chat.
        """

        if use_cache and cache_key_data:
            cached = self._cache.get(cache_key_data)
            if cached is not None:
                return str(cached)

        model_to_use = model or self._choose_model(str(messages))
        prepared_messages = self._prepare_messages(messages)

        payload: dict[str, Any] = {
            "model": model_to_use,
            "messages": prepared_messages,
            "options": {
                "temperature": temperature,
            },
        }

        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        response = self._post(payload)

        text = (
            response.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )

        if use_cache and cache_key_data:
            self._cache.set(cache_key_data, text)

        return text

    def chat_async(
        self,
        messages: list[dict[str, Any]],
        *,
        model: str | None = None,
        temperature: float = 0.2,
        max_tokens: int | None = None,
        use_cache: bool = False,
        cache_key_data: dict[str, Any] | None = None,
        on_success: Callable[[str], None] | None = None,
        on_error: Callable[[str], None] | None = None,
    ) -> None:
        """
        Async generic chat.
        """

        def task() -> None:
            try:
                text = self.chat(
                    messages,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    use_cache=use_cache,
                    cache_key_data=cache_key_data,
                )
                if on_success:
                    on_success(text)
            except Exception as exc:
                if on_error:
                    on_error(str(exc))

        self._request_queue.submit(task)

    def stream_chat(
        self,
        messages: list[dict[str, Any]],
        *,
        model: str | None = None,
        temperature: float = 0.2,
        max_tokens: int | None = None,
        use_cache: bool = False,
        cache_key_data: dict[str, Any] | None = None,
        on_token: Callable[[str], None] | None = None,
        on_done: Callable[[str], None] | None = None,
        on_error: Callable[[str], None] | None = None,
    ) -> None:
        """
        Async streamed generic chat.
        Emits text chunks through on_token and the final full text through on_done.
        """

        def task() -> None:
            try:
                if use_cache and cache_key_data:
                    cached = self._cache.get(cache_key_data)
                    if cached is not None:
                        cached_text = str(cached)
                        if on_token:
                            on_token(cached_text)
                        if on_done:
                            on_done(cached_text)
                        return

                model_to_use = model or self._choose_model(str(messages))
                prepared_messages = self._prepare_messages(messages)

                payload: dict[str, Any] = {
                    "model": model_to_use,
                    "messages": prepared_messages,
                    "stream": True,
                    "options": {
                        "temperature": temperature,
                    },
                }

                if max_tokens is not None:
                    payload["max_tokens"] = max_tokens

                full = ""

                with requests.post(
                    OLLAMA_URL,
                    json=payload,
                    stream=True,
                    timeout=TIMEOUT,
                ) as response:
                    response.raise_for_status()

                    for line in response.iter_lines():
                        if not line:
                            continue

                        if isinstance(line, (bytes, bytearray)):
                            line_str = line.decode("utf-8", errors="ignore").strip()
                        else:
                            line_str = str(line).strip()

                        if not line_str:
                            continue

                        if line_str.startswith("data:"):
                            line_str = line_str[len("data:"):].strip()

                        if not line_str or line_str == "[DONE]":
                            continue

                        try:
                            data = json.loads(line_str)
                        except Exception:
                            continue

                        token = (
                            data.get("choices", [{}])[0]
                            .get("delta", {})
                            .get("content", "")
                            or ""
                        )

                        if token:
                            full += token
                            if on_token:
                                on_token(token)

                if use_cache and cache_key_data:
                    self._cache.set(cache_key_data, full)

                if on_done:
                    on_done(full)

            except Exception as exc:
                if on_error:
                    on_error(str(exc))

        self._request_queue.submit(task)

Now your v9_ai_bridge.py can stay very small, using only the local V9 connector.

Use this:

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject, Signal

from v9_qwen_ai_models import V9QwenAIModels


class AIWorkerBridge(QObject):
    answer_ready = Signal(str)
    token_ready = Signal(str)
    error_ready = Signal(str)
    status_ready = Signal(str)


class LocalAIReasoner:
    def __init__(self) -> None:
        self.wrapper = V9QwenAIModels()
        self.bridge = AIWorkerBridge()

    def set_cache_dir(self, cache_dir: str) -> None:
        self.wrapper.set_cache_dir(Path(cache_dir).expanduser().resolve())

    def set_governance_state_path(self, state_path: str) -> None:
        self.wrapper.set_governance_state_path(Path(state_path).expanduser().resolve())

    def ask(self, prompt: str, model_name: str) -> None:
        self.bridge.status_ready.emit(
            "Submitting question to local AI using model: " + model_name
        )

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a senior Python architecture analyst. "
                    "Answer only from the supplied evidence pack. "
                    "Do not invent files, classes, functions, or execution flows. "
                    "If evidence is insufficient, say so clearly. "
                    "Always cite ids like [F01], [S01], [SN01]."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]

        cache_key_data = {
            "task": "v9_reasoner_chat",
            "model": model_name,
            "prompt": prompt,
        }

        self.wrapper.stream_chat(
            messages,
            model=model_name,
            temperature=0.1,
            max_tokens=2200,
            use_cache=True,
            cache_key_data=cache_key_data,
            on_token=self.bridge.token_ready.emit,
            on_done=self.bridge.answer_ready.emit,
            on_error=self.bridge.error_ready.emit,
        )

Then run again.

If you still get an import error after this, paste the first 20 lines of:
v9_main_window.py
v9_ai_bridge.py
and I will normalize the remaining imports exactly for your folder.

E:\mne_py3.10\python.exe "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9\run_project_reasoner_v9.py" 
Traceback (most recent call last):
  File "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9\run_project_reasoner_v9.py", line 3, in <module>
    from v9_main_window import main
  File "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9\v9_main_window.py", line 28, in <module>
    from v9_conversation_memory import ConversationMemory
  File "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9\v9_conversation_memory.py", line 3, in <module>
    from .v9_models import ConversationTurn
ImportError: attempted relative import with no known parent package




from __future__ import annotations

import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from v9_ai_bridge import LocalAIReasoner
from v9_conversation_memory import ConversationMemory
from v9_index_loader import JsonProjectIndex
from v9_model_registry import LocalModelRegistry
from v9_models import ConversationTurn, RetrievalBundle
from v9_prompt_builder import PromptBuilder
from v9_retriever import ProjectRetriever


def shorten_path(path: str, max_len: int = 90) -> str:
    if len(path) <= max_len:
        return path
    return "..." + path[-(max_len - 3):]


class JsonProjectReasonerV9(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Project JSON Explorer v9 - Local AI Reasoner")
        self.resize(1880, 1080)



from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject, Signal

from v9_qwen_ai_models import V9QwenAIModels


class AIWorkerBridge(QObject):
    answer_ready = Signal(str)
    token_ready = Signal(str)
    error_ready = Signal(str)
    status_ready = Signal(str)


class LocalAIReasoner:
    def __init__(self) -> None:
        self.wrapper = V9QwenAIModels()
        self.bridge = AIWorkerBridge()

    def set_cache_dir(self, cache_dir: str) -> None:
        self.wrapper.set_cache_dir(Path(cache_dir).expanduser().resolve())

Thought for a couple of seconds

The error now is exactly this:

v9_conversation_memory.py still uses a relative import:

from .v9_models import ConversationTurn

Since you are running everything as plain same-folder scripts, all V9 files must use same-folder imports, not relative imports.

Use these exact import lines.

In v9_conversation_memory.py, replace:

from .v9_models import ConversationTurn

with:

from v9_models import ConversationTurn

In v9_prompt_builder.py, replace:

from .v9_models import ConversationTurn, RetrievalBundle

with:

from v9_models import ConversationTurn, RetrievalBundle

In v9_retriever.py, replace:

from .v9_index_loader import JsonProjectIndex
from .v9_models import EvidenceItem, RetrievalBundle, SymbolEvidenceItem

with:

from v9_index_loader import JsonProjectIndex
from v9_models import EvidenceItem, RetrievalBundle, SymbolEvidenceItem

In v9_main_window.py, keep:

from v9_ai_bridge import LocalAIReasoner
from v9_conversation_memory import ConversationMemory
from v9_index_loader import JsonProjectIndex
from v9_model_registry import LocalModelRegistry
from v9_models import ConversationTurn, RetrievalBundle
from v9_prompt_builder import PromptBuilder
from v9_retriever import ProjectRetriever

In v9_ai_bridge.py, keep:

from v9_qwen_ai_models import V9QwenAIModels

So for your current folder layout, the rule is:

every V9 file imports sibling files like this:

from v9_xxx import Something

and never like this:

from .v9_xxx import Something

Quick way to find remaining broken imports

Run this in that folder:

import pathlib
root = pathlib.Path(r"E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9")
for path in root.glob("*.py"):
    text = path.read_text(encoding="utf-8", errors="ignore")
    if "from ." in text:
        print(path.name)

If you want the one-line terminal version for PowerShell:

python -c "import pathlib; root=pathlib.Path(r'E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9'); [print(p.name) for p in root.glob('*.py') if 'from .' in p.read_text(encoding='utf-8', errors='ignore')]"

After fixing all from . imports, run again:

E:\mne_py3.10\python.exe "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9\run_project_reasoner_v9.py"

If you want, paste the first 10 lines of:
v9_conversation_memory.py
v9_prompt_builder.py
v9_retriever.py

and I will verify the final import normalization.

project_structure_index.json
File
project_reasoner_v9_1.0_DATA_COLECTOR.py
Python
NOW looking back to that beautifull structure of project-reasoner_v9 , how can we improve data colection from project to project_reasoner_v9_1.0_DATA_COLECTOR.py to disponibilize maximum information about the project to ai have maximum performance when answering?
Thought for 28s

Yes. The current collector is a good base, but to make project_reasoner_v9_1.0_DATA_COLECTOR.py much better for AI reasoning, I would push it from a “rich static index” into an “architectural evidence pack.”

Right now it already collects a strong first layer:
imports, classes, inheritance, functions, methods, call sites, docstrings, comments, string literals, keyword hits, entry markers, UI hints, EEG hints, symbol index, import graph, and simple call edges. That is explicitly stated in the file header and reflected in build_project_index(), which emits files, symbol_index, import_graph, call_edges, semantic_roles, and keyword_index.

Also, your current output already shows why the next step matters: the generated index includes 912 Python files and 161 entry-like files, but it is also heavily polluted by .venv and third-party code, which creates a very large parse-error surface and a lot of irrelevant UI/semantic noise.

So the main improvement is not “collect more random data.”
It is:
collect higher-value data,
reduce noise,
and structure evidence for question answering.

My recommendation for project_reasoner_v9_1.0_DATA_COLECTOR.py is to add these layers.

Strong project filtering first

This is the highest-impact change.

Your current collector walks every .py file recursively. That is why the JSON is flooded with .venv\\Lib\\site-packages\\... entries and hundreds of irrelevant parse errors.

Add ignore rules for:
.venv
venv
__pycache__
.git
.idea
.mypy_cache
.pytest_cache
build
dist
site-packages
temporary backup folders
old migration dump folders if you want

Also add an optional GUI checkbox:
Include third-party/venv files

Default should be off.

That single change will improve AI answer quality a lot, because the retriever will stop ranking pip internals beside your real EEG modules.

Add file-level architectural role inference

You already have summarize_file_semantics(record) with roles like startup, main_window, tabs, timeline, topomap, filters, splash, state_reset, and memory_monitoring. That is excellent, and the produced JSON already shows these roles being assigned to files such as main_win_builder.py and visualizer helper modules.

The next step is to make this much more explicit.

For each file, add:
primary_role
secondary_roles
confidence
evidence_terms

Example:
main_win_builder.py
primary_role: main_window_builder
secondary_roles: startup, tabs
confidence: 0.92
evidence_terms: ["QMainWindow", "setCentralWidget", "addTab", "showMaximized"]

That helps the AI answer questions like:
“which code creates the top tab?”
“what starts the app?”
“where is timeline attached?”

Add semantic execution chains

This is the most important upgrade for V9.

Today you have:
import graph
simple call edges
symbol index

That is good, but AI needs higher-order chains.

Add derived chains such as:
startup chain
UI build chain
tab construction chain
timeline chain
topomap chain
EEG load chain
reset/cleanup chain

For each chain, store ordered evidence like:

startup_chain:
entry file -> main() -> create_main_window -> NotebookBuilder -> TabFactory -> EEG tab load

timeline_chain:
TimelineWidget -> TimelineManager -> move_window_to_time -> visualizer.on_timeline_moved

topomap_chain:
toggle action -> amplitude map initializer -> topomap renderer -> redraw/update

This should be a derived section in the JSON, not just raw AST.

Add object ownership and responsibility maps

AI answers become much stronger when it knows:
who creates what
who stores what
who updates what
who destroys what

So derive and store:

object_ownership
Example:
visualizer.main_window created by EEGMainWindowBuilder.build_and_show
visualizer.timeline_widget attached by timeline attachment helper
visualizer.splash created by splash manager

responsibility_map
Example:
SignalManager: connects EEG Qt signals
MemoryManager: creates detector and initial snapshot
TimelineManager: syncs EEG view and bracket movement

That lets the AI answer “which module is responsible for X?” instead of only “where does X appear?”

Add attribute mutation maps

For EEG-style GUI projects, many important flows are state-based, not just function-based.

Track writes to core attributes like:
self.main_window
self.notebook
self.timeline_widget
self.splash
self.current_start
self.window_size
self.amplitude_scale
self.raw
self.data
self.mcrvlt_snapshot_map

Store:
where initialized
where updated
where reset
where read frequently

This is one of the best additions for answering:
“what changes when I click timeline?”
“who resets the EEG state?”
“who updates amplitude scale?”

Add signal-slot maps

This is critical in PySide6.

Your current collector sees connect as text and call sites, but not as a structured signal graph. The project clearly uses Qt signals heavily.

Add a dedicated section:

qt_signal_map:
signal owner
signal name
connected target
source file
line
confidence

Example:
eeg_loaded_signal -> initialize_mcrvlt_snapshot_map
window_moved -> visualizer.on_timeline_moved

This will massively improve answers about runtime behavior in the GUI.

Add method body summaries for AI retrieval

Right now you store docstrings and call lists, but not a compact semantic summary per function.

Generate, for every important function/method:
one short deterministic summary from static heuristics

Example:
build_and_show()
“Creates QApplication font, captures initial EEG snapshot, builds main window, creates nav bars, notebook, tabs, loads EEG tab, shows window, installs key handling.”

handle_timeline_clicked()
“Computes safe start time from click, updates EEG current_start, redraws plot, emits internal window_moved and external timeline_moved.”

These can be heuristic, not LLM-generated.
This is probably the single best retrieval improvement after filtering.

Add code snippets for high-value symbols

For retrieval, store short source excerpts for:
entry points
builders
managers
renderers
signal handlers
cleanup/reset methods

Not the whole file.
Only focused excerpts like:
signature
docstring
first 20-40 lines of body
connect calls
attribute writes
returns

That gives the local AI concrete evidence to quote mentally when answering.

Add duplicate and alias detection

Your project has evolution/refactor history.
AI gets confused when there are multiple modules doing nearly the same thing.

Add:
duplicate class/function names across files
same symbol name with multiple candidate files
deprecated vs active path candidates
old/new migration pairs

Example sections:
duplicate_symbols
possible_replacements
deprecated_candidates

This is especially useful in a project with older helper paths and migration remnants.

Add test coverage linkage

For each production file or symbol, link nearby tests if they exist.

Store:
tested_by_files
tests_for_symbol
test_confidence

This helps the AI answer:
“is this module already tested?”
“which tests validate timeline behavior?”

Add directory-level and subsystem summaries

Your project already naturally clusters into subsystems:
main window builder
visualizer core
timeline
tabs
combobox/filter system
topomap/amplitude map
templates
tools

Create a subsystems section:
subsystem name
root folders/files
main symbols
main responsibilities
cross-subsystem dependencies

That makes answers much more global and much less file-fragmented.

Add retrieval-oriented indexes

For V9 specifically, I would add these indexes:

symbol_to_summary
role_to_files
keyword_to_symbols
attribute_to_writers
attribute_to_readers
signal_to_targets
entry_chain_index
subsystem_index

These make follow-up questions much faster and much more reliable.

Add confidence and ambiguity fields everywhere

Very important.

When static inference is weak, say so in data.

Example:
role_confidence
call_resolution_confidence
owner_confidence
entry_confidence

That allows V9 to generate better uncertainty reports instead of sounding overconfident.

Add project snapshot metadata for reasoning quality

Add:
collector version
collection timestamp
ignored folders
included roots
file counts by subsystem
noise counts
syntax error counts after filtering
active entrypoint candidates
top 50 most connected modules

This helps the AI understand how trustworthy and complete the evidence pack is.

Best practical V9 output design

I would split the collector output into 4 layers:

Layer A: raw structural facts
files, classes, functions, imports, calls, comments, strings

Layer B: normalized indexes
symbol_index, import_graph, attribute map, signal map, keyword maps

Layer C: derived architecture
startup chain, timeline chain, topomap chain, subsystem summaries, responsibility maps

Layer D: retrieval pack
short summaries, focused code snippets, ambiguity/confidence markers

That gives the AI both precision and high-level understanding.

My priority order for implementation

If you want maximum gain quickly, do it in this order:

Exclude .venv and other noise folders

Add method/function semantic summaries

Add Qt signal-slot map

Add attribute write/read map

Add derived execution chains

Add subsystem summaries

Add test linkage

Add duplicate/deprecated symbol detection

Most important diagnosis from your current output

The current collector is already strong enough to prove the concept, but the generated JSON is still too noisy because it includes a lot of virtualenv and vendor content. The project summary showing 912 Python files plus many .venv parse-error entries is the clearest sign that filtering should be your first upgrade.

So my short architectural recommendation is:

turn project_reasoner_v9_1.0_DATA_COLECTOR.py from a generic AST dumper into a filtered architectural compiler focused on:
active project files,
execution chains,
responsibility ownership,
state mutations,
and retrieval-ready summaries.

If you want, next I can draft a concrete project_reasoner_v9_1.1_DATA_COLECTOR.py roadmap with exact new JSON sections and the exact functions to add.

go
Thought for 12s
continue
Thought for 7s

Good. Here is a concrete plan for project_reasoner_v9_1.1_DATA_COLECTOR.py.

The goal of 1.1 is not just “more data.”
It is:
less noise,
better structure,
better architectural inference,
better retrieval for V9.

1. Target output shape

Your current collector already gives a strong structural index.
Version 1.1 should produce a JSON with these top-level sections:

{
  "collector_info": {},
  "project_summary": {},
  "collection_config": {},
  "files": [],
  "symbol_index": {},
  "import_graph": {},
  "call_edges": [],
  "keyword_index": {},
  "semantic_roles": {},
  "qt_signal_map": [],
  "attribute_state_map": {},
  "object_ownership": [],
  "execution_chains": {},
  "subsystems": [],
  "symbol_summaries": {},
  "snippet_index": {},
  "duplicate_symbols": [],
  "test_links": [],
  "errors": []
}

That is the architectural target.

2. New sections to add
collector_info

Tells V9 how trustworthy and recent the index is.

Example:

{
  "collector_version": "1.1",
  "generated_at": "2026-03-13T12:45:00",
  "python_version": "3.10",
  "root_path": "E:\\eeg_kernel_ai_neural_data_analysis"
}
collection_config

Very important for uncertainty.

Example:

{
  "excluded_dirs": [
    ".venv",
    "venv",
    "__pycache__",
    ".git",
    ".idea",
    "site-packages",
    "build",
    "dist"
  ],
  "include_tests": true,
  "include_vendor_code": false,
  "max_snippet_lines": 40
}
qt_signal_map

Structured signal-slot evidence.

Example:

[
  {
    "source_file": "shell/viewer/eeg_signal_manager.py",
    "source_symbol": "SignalManager.init_signals",
    "signal_owner": "v",
    "signal_name": "eeg_loaded_signal",
    "target": "v.initialize_mcrvlt_snapshot_map",
    "line": 18,
    "confidence": 0.95
  }
]
attribute_state_map

Tracks who writes/reads core state.

Example:

{
  "main_window": {
    "writers": [
      {
        "file": "shell/viewer/eeg_main_window_builder.py",
        "symbol": "EEGMainWindowBuilder.build_and_show",
        "line": 62
      }
    ],
    "readers": [
      {
        "file": "shell/viewer/eeg_visualizer_core.py",
        "symbol": "EEGVisualizerCore._toggle_max_restore",
        "line": 200
      }
    ]
  }
}
object_ownership

Who creates and owns UI/runtime objects.

Example:

[
  {
    "object_name": "visualizer.main_window",
    "created_by_file": "shell/viewer/eeg_main_window_builder.py",
    "created_by_symbol": "EEGMainWindowBuilder.build_and_show",
    "kind": "QMainWindow",
    "confidence": 0.95
  }
]
execution_chains

Derived architectural chains.

Example:

{
  "startup_chain": [
    {
      "step": 1,
      "file": "shell/viewer/eeg_display_launcher.py",
      "symbol": "display_pyside6_eeg_visualizer",
      "why": "main window entry for UI display"
    },
    {
      "step": 2,
      "file": "shell/viewer/eeg_main_window_builder.py",
      "symbol": "EEGMainWindowBuilder.build_and_show",
      "why": "creates main window, notebook, and tabs"
    }
  ],
  "timeline_chain": [],
  "topomap_chain": [],
  "reset_chain": []
}
subsystems

Directory-level and role-level summaries.

Example:

[
  {
    "name": "timeline",
    "files": [
      "shell/timeline/eeg_timeline_widget.py",
      "shell/timeline/eeg_timeline_manager.py",
      "shell/viewer/eeg_timeline_manager_core.py"
    ],
    "main_symbols": [
      "TimelineWidget",
      "TimelineManager",
      "EEGVisualizerCore.on_timeline_moved"
    ],
    "responsibility": "timeline UI, bracket movement, and synchronization with EEG window state"
  }
]
symbol_summaries

Deterministic semantic summaries per function/method/class.

Example:

{
  "EEGMainWindowBuilder.build_and_show": {
    "file": "shell/viewer/eeg_main_window_builder.py",
    "kind": "method",
    "summary": "Builds application window, nav bars, notebook, tabs, loads EEG tab, shows main window, and installs focus/key handlers."
  }
}
snippet_index

Short retrieval-ready code excerpts.

Example:

{
  "EEGMainWindowBuilder.build_and_show": {
    "file": "shell/viewer/eeg_main_window_builder.py",
    "line_start": 45,
    "line_end": 120,
    "snippet": "def build_and_show(self):\n    app = QApplication.instance()..."
  }
}
duplicate_symbols

Useful for ambiguity reports.

Example:

[
  {
    "symbol_name": "TimelineManager",
    "occurrences": [
      "shell/timeline/eeg_timeline_manager.py",
      "shell/viewer/eeg_timeline_manager_core.py"
    ],
    "kind": "class_name_collision"
  }
]
test_links

Map production files to tests.

Example:

[
  {
    "source_file": "shell/viewer/eeg_main_window_builder.py",
    "linked_tests": [
      "tests/test_eeg_main_window_builder.py"
    ],
    "confidence": 0.72
  }
]
3. Exact functions to add

Below is the function inventory I would add to project_reasoner_v9_1.1_DATA_COLECTOR.py.

Phase A: filtering and normalization
should_exclude_dir(dirname: str) -> bool

Returns true for:
.venv
venv
__pycache__
.git
.idea
site-packages
build
dist

should_exclude_file(path: Path) -> bool

Lets you skip:
generated files
temporary backups
obviously irrelevant vendor artifacts

walk_python_files_filtered(root: Path) -> list[Path]

Replacement for naive recursive glob.
This is one of the most important upgrades.

Phase B: richer AST extraction
extract_assignments_from_body(body_nodes: list[ast.AST]) -> list[dict]

Capture writes like:
self.main_window = ...
self.timeline_widget = ...
v.splash = ...

Store:
target
line
value type
raw source if available

extract_attribute_reads_from_body(body_nodes: list[ast.AST]) -> list[dict]

Capture reads like:
self.main_window.isMaximized()
self.timeline_widget.manager

extract_qt_connections_from_body(body_nodes: list[ast.AST]) -> list[dict]

Look for .connect(...) calls and infer:
signal owner
signal name
target callable
line

This powers qt_signal_map.

extract_object_creations_from_body(body_nodes: list[ast.AST]) -> list[dict]

Look for patterns like:
self.main_window = create_main_window()
self.timeline_widget = TimelineWidget(...)
self.splash = KandaSplashImageText(...)

This powers object_ownership.

Phase C: semantic summaries
summarize_symbol_semantics(symbol_record: dict) -> str

Heuristic one-line summary for:
functions
methods
classes

Rules:
mention if it creates widgets
connects signals
updates state
renders plot
resets state
builds tabs
loads EEG
handles timeline

build_symbol_summaries(files_payload: list[dict]) -> dict

Collects summaries for all major symbols.

build_snippet_index(project_root: Path, files_payload: list[dict], max_lines: int = 40) -> dict

Extract snippets for:
entry points
builder methods
manager methods
reset functions
signal wiring methods

Phase D: derived architecture
build_attribute_state_map(files_payload: list[dict]) -> dict

Aggregates all attribute reads/writes.

build_qt_signal_map(files_payload: list[dict]) -> list[dict]

Aggregates all connect calls.

build_object_ownership_map(files_payload: list[dict]) -> list[dict]

Aggregates object creation evidence.

derive_startup_chain(files_payload: list[dict], entry_files: list[str]) -> list[dict]

Heuristics:
find entry files
find display/build/show functions
find builder chain
find notebook/tab setup

derive_timeline_chain(files_payload: list[dict]) -> list[dict]

Heuristics:
timeline widget
timeline manager
visualizer handlers
signals between them

derive_topomap_chain(files_payload: list[dict]) -> list[dict]

Heuristics:
topomap/amplitude map/toggle/initializer/update

derive_reset_chain(files_payload: list[dict]) -> list[dict]

Heuristics:
snapshot capture
reset helpers
cleanup
close callbacks

build_execution_chains(files_payload: list[dict], entry_files: list[str]) -> dict

Wrapper that builds all chains.

build_subsystem_summaries(files_payload: list[dict]) -> list[dict]

Group files into logical subsystems by path and roles:
viewer
timeline
splash
tabs
filter panel
topomap/amplitude map
snapshot/reset
templates

Phase E: ambiguity and quality
find_duplicate_symbols(files_payload: list[dict]) -> list[dict]

Detect repeated class/function names.

link_tests_to_sources(files_payload: list[dict]) -> list[dict]

Heuristic:
same basename
same subsystem path
test references in imports or strings

build_collection_config(...) -> dict

Stores all collector settings used.

build_collector_info(...) -> dict

Stores metadata about this collection.

4. New per-file payload fields

Each file record should now include more than it does today.

Add these fields per file:

{
  "path": "...",
  "module_name": "...",
  "imports": [],
  "classes": [],
  "functions": [],
  "docstring": "...",
  "comments": [],
  "strings": [],
  "entry_markers": [],
  "ui_keyword_hits": [],
  "eeg_keyword_hits": [],
  "semantic_hints": [],
  "semantic_roles": [],
  "primary_role": "",
  "secondary_roles": [],
  "role_confidence": 0.0,
  "attribute_writes": [],
  "attribute_reads": [],
  "qt_connections": [],
  "object_creations": [],
  "summary": ""
}

That way V9 can answer both:
“which file?”
and
“what is its responsibility?”

5. Heuristic rules that matter most

These are the rules I would prioritize.

Startup heuristics

If a file has:
if __name__ == "__main__"
or QApplication(
or .show()
or .showMaximized()
or main()

then boost startup role.

Main window heuristics

If a file contains:
QMainWindow
setCentralWidget
NotebookBuilder
addTab
build_and_show

then boost main window / tabs / startup.

Timeline heuristics

If a file contains:
TimelineWidget
TimelineManager
window_moved
time_clicked
on_timeline_moved
move_window_to_time

then boost timeline.

Topomap heuristics

If a file contains:
topomap
amplitude_map
mcrvlt_snapshot_map
toggle_topomap
colorbar

then boost topomap.

Reset heuristics

If a file contains:
reset
snapshot
cleanup
hide_amplitude_map_elements
close
destroyed.connect

then boost reset/cleanup.

Signal heuristics

If a file contains .connect( and named signals like:
eeg_loaded_signal
timeline_moved
window_moved

then extract structured signal map entries.

6. How V9 benefits from 1.1 collector

This new collector directly improves V9 in five ways.

Better retrieval precision

Less venv noise.
Less irrelevant hits.
Better ranking.

Better follow-up memory

If previous turn mentioned a chain, V9 can reuse chain evidence instead of only file evidence.

Better uncertainty reports

Because ambiguity and confidence are stored explicitly.

Better responsibility answers

Because subsystem summaries and object ownership exist.

Better architecture Q&A

Because execution chains become first-class data instead of being inferred from scattered raw AST.

7. Practical implementation order

I would implement 1.1 in this order:

Step 1
Add filtered file walking

Step 2
Add per-symbol summaries

Step 3
Add attribute reads/writes

Step 4
Add Qt signal extraction

Step 5
Add object creation extraction

Step 6
Add execution chain derivation

Step 7
Add subsystem summaries

Step 8
Add duplicate symbol detection and test links

That sequence gives the highest value early.

8. Minimal first upgrade that already helps a lot

If you want a fast 1.1 without making it huge yet, do only these four:

walk_python_files_filtered
build_symbol_summaries
build_qt_signal_map
build_execution_chains

That alone would already make V9 noticeably stronger.

9. Recommended filename

I would name it:

project_reasoner_v9_1_1_data_collector.py

Use underscores, not dots in the filename, to avoid odd import behavior on Windows.

10. Next thing I can do

I can now draft the actual code skeleton for:
project_reasoner_v9_1_1_data_collector.py

with:
the new top-level JSON schema
the filtered walker
the new helper function stubs
and the updated build_project_index() pipeline.

greate implement all but

file is becoming to long , divide in smaller modules in DEVELOPER TOOLS/FULL_INSPECTOR_JSON_APP/project_reasoner_v9_data _collector and create a small runner.py file 
Thought for a couple of seconds

Perfect. Below is a modular project_reasoner_v9_data_collector package layout for:

DEVELOPER TOOLS/FULL_INSPECTOR_JSON_APP/project_reasoner_v9_data_collector

It implements the 1.1-style collector in smaller files and includes a tiny runner.py.

Recommended folder structure:

DEVELOPER TOOLS/FULL_INSPECTOR_JSON_APP/project_reasoner_v9_data_collector/
    __init__.py
    runner.py
    collector_main.py
    collector_config.py
    collector_utils.py
    collector_filters.py
    collector_walker.py
    collector_ast.py
    collector_roles.py
    collector_qt.py
    collector_state.py
    collector_ownership.py
    collector_chains.py
    collector_subsystems.py
    collector_duplicates.py
    collector_tests.py
    collector_output.py
1. __init__.py
from collector_main import run_collector
2. collector_config.py
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CollectorConfig:
    excluded_dirs: list[str] = field(
        default_factory=lambda: [
            ".venv",
            "venv",
            "__pycache__",
            ".git",
            ".idea",
            ".mypy_cache",
            ".pytest_cache",
            "site-packages",
            "build",
            "dist",
        ]
    )
    include_tests: bool = True
    include_vendor_code: bool = False
    max_snippet_lines: int = 40
    max_docstring_length: int = 1000
3. collector_utils.py
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def safe_read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def normalize_path(path: Path, root: Path) -> str:
    return str(path.resolve().relative_to(root.resolve())).replace("\\", "/")


def short_hash(value: str) -> str:
    return hashlib.sha1(value.encode("utf-8", errors="replace")).hexdigest()[:12]


def compact_whitespace(text: str) -> str:
    return " ".join(str(text).split())


def safe_json_dump(data: Any, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
4. collector_filters.py
from __future__ import annotations

from pathlib import Path

from collector_config import CollectorConfig


def should_exclude_dir(dirname: str, config: CollectorConfig) -> bool:
    lowered = dirname.strip().lower()
    return lowered in {item.lower() for item in config.excluded_dirs}


def should_exclude_file(path: Path, config: CollectorConfig) -> bool:
    lowered = path.name.lower()

    if lowered.endswith(".pyc"):
        return True

    if lowered.startswith("."):
        return True

    if not config.include_tests and "test" in lowered:
        return True

    return False
5. collector_walker.py
from __future__ import annotations

from pathlib import Path

from collector_config import CollectorConfig
from collector_filters import should_exclude_dir, should_exclude_file


def walk_python_files_filtered(root: Path, config: CollectorConfig) -> list[Path]:
    results: list[Path] = []

    def _walk(current: Path) -> None:
        try:
            entries = list(current.iterdir())
        except Exception:
            return

        for entry in entries:
            if entry.is_dir():
                if should_exclude_dir(entry.name, config):
                    continue
                _walk(entry)
                continue

            if entry.is_file() and entry.suffix == ".py":
                if should_exclude_file(entry, config):
                    continue
                results.append(entry)

    _walk(root)
    return sorted(results)
6. collector_ast.py
from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

from collector_utils import compact_whitespace, safe_read_text


def _get_docstring(node: ast.AST) -> str:
    try:
        return ast.get_docstring(node) or ""
    except Exception:
        return ""


def _extract_comments_and_strings(source: str) -> tuple[list[str], list[str]]:
    comments: list[str] = []
    strings: list[str] = []

    for line in source.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            comments.append(stripped)

    try:
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                value = compact_whitespace(node.value)
                if value:
                    strings.append(value)
    except Exception:
        pass

    return comments, strings


def _name_from_node(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _name_from_node(node.value)
        return base + "." + node.attr if base else node.attr
    if isinstance(node, ast.Call):
        return _name_from_node(node.func)
    return ""


def _extract_calls(body: list[ast.stmt]) -> list[dict[str, Any]]:
    calls: list[dict[str, Any]] = []

    class Visitor(ast.NodeVisitor):
        def visit_Call(self, node: ast.Call) -> None:
            calls.append(
                {
                    "call_name": _name_from_node(node.func),
                    "lineno": getattr(node, "lineno", None),
                }
            )
            self.generic_visit(node)

    visitor = Visitor()
    for stmt in body:
        visitor.visit(stmt)
    return calls


def _extract_assignments(body: list[ast.stmt]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []

    class Visitor(ast.NodeVisitor):
        def visit_Assign(self, node: ast.Assign) -> None:
            for target in node.targets:
                target_name = _name_from_node(target)
                if target_name:
                    items.append(
                        {
                            "target": target_name,
                            "value_type": type(node.value).__name__,
                            "lineno": getattr(node, "lineno", None),
                        }
                    )
            self.generic_visit(node)

        def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
            target_name = _name_from_node(node.target)
            if target_name:
                items.append(
                    {
                        "target": target_name,
                        "value_type": type(node.value).__name__ if node.value else "",
                        "lineno": getattr(node, "lineno", None),
                    }
                )
            self.generic_visit(node)

    visitor = Visitor()
    for stmt in body:
        visitor.visit(stmt)
    return items


def _extract_attribute_reads(body: list[ast.stmt]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []

    class Visitor(ast.NodeVisitor):
        def visit_Attribute(self, node: ast.Attribute) -> None:
            name = _name_from_node(node)
            if name:
                items.append(
                    {
                        "attribute": name,
                        "lineno": getattr(node, "lineno", None),
                    }
                )
            self.generic_visit(node)

    visitor = Visitor()
    for stmt in body:
        visitor.visit(stmt)
    return items


def parse_python_file(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        source = safe_read_text(path)
        tree = ast.parse(source)
    except Exception as exc:
        return None, str(exc)

    comments, strings = _extract_comments_and_strings(source)

    module_docstring = _get_docstring(tree)
    imports: list[str] = []
    classes: list[dict[str, Any]] = []
    functions: list[dict[str, Any]] = []

    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            module_name = node.module or ""
            imports.append(module_name)

        elif isinstance(node, ast.FunctionDef):
            functions.append(
                {
                    "name": node.name,
                    "qualname": node.name,
                    "lineno": getattr(node, "lineno", None),
                    "docstring": _get_docstring(node),
                    "calls": _extract_calls(node.body),
                    "assignments": _extract_assignments(node.body),
                    "attribute_reads": _extract_attribute_reads(node.body),
                }
            )

        elif isinstance(node, ast.ClassDef):
            methods: list[dict[str, Any]] = []
            bases = [_name_from_node(base) for base in node.bases]

            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    methods.append(
                        {
                            "name": item.name,
                            "qualname": node.name + "." + item.name,
                            "lineno": getattr(item, "lineno", None),
                            "docstring": _get_docstring(item),
                            "calls": _extract_calls(item.body),
                            "assignments": _extract_assignments(item.body),
                            "attribute_reads": _extract_attribute_reads(item.body),
                        }
                    )

            classes.append(
                {
                    "name": node.name,
                    "lineno": getattr(node, "lineno", None),
                    "docstring": _get_docstring(node),
                    "bases": bases,
                    "methods": methods,
                }
            )

    payload = {
        "module_docstring": module_docstring,
        "imports": sorted(set(filter(None, imports))),
        "classes": classes,
        "functions": functions,
        "comments": comments,
        "strings": strings,
        "source": source,
    }
    return payload, None
7. collector_roles.py
from __future__ import annotations

from typing import Any

from collector_utils import compact_whitespace


ROLE_HINTS = {
    "startup": ["__main__", "qapplication", "main(", "show(", "showmaximized"],
    "main_window": ["qmainwindow", "setcentralwidget", "main_window", "build_and_show"],
    "tabs": ["addtab", "notebook", "tabfactory", "currentchanged"],
    "timeline": ["timelinewidget", "timelinemanager", "window_moved", "time_clicked", "on_timeline_moved"],
    "topomap": ["topomap", "amplitude_map", "mcrvlt_snapshot_map", "colorbar"],
    "filters": ["filter", "dropdown", "combobox", "toolbar"],
    "splash": ["splash", "kandasplash"],
    "state_reset": ["reset", "snapshot", "cleanup", "destroyed.connect"],
    "memory_monitoring": ["memory", "memoryleakdetector"],
}


def summarize_file_semantics(record: dict[str, Any]) -> dict[str, Any]:
    blob_parts: list[str] = []

    blob_parts.extend(record.get("imports", []))
    blob_parts.extend(record.get("comments", []))
    blob_parts.extend(record.get("strings", []))
    blob_parts.append(record.get("docstring", ""))

    for fn in record.get("functions", []):
        blob_parts.append(fn.get("name", ""))
        blob_parts.append(fn.get("docstring", ""))
        for call in fn.get("calls", []):
            blob_parts.append(call.get("call_name", ""))

    for cls in record.get("classes", []):
        blob_parts.append(cls.get("name", ""))
        blob_parts.append(cls.get("docstring", ""))
        for method in cls.get("methods", []):
            blob_parts.append(method.get("name", ""))
            blob_parts.append(method.get("docstring", ""))
            for call in method.get("calls", []):
                blob_parts.append(call.get("call_name", ""))

    blob = compact_whitespace(" ".join(blob_parts)).lower()

    roles: list[str] = []
    evidence_terms: list[str] = []
    score_map: dict[str, int] = {}

    for role, hints in ROLE_HINTS.items():
        score = 0
        for hint in hints:
            if hint.lower() in blob:
                score += 1
                evidence_terms.append(hint)
        if score > 0:
            roles.append(role)
            score_map[role] = score

    primary_role = ""
    secondary_roles: list[str] = []
    confidence = 0.0

    if score_map:
        ordered = sorted(score_map.items(), key=lambda item: item[1], reverse=True)
        primary_role = ordered[0][0]
        secondary_roles = [item[0] for item in ordered[1:4]]
        confidence = min(0.99, 0.5 + (ordered[0][1] * 0.1))

    return {
        "roles": roles,
        "primary_role": primary_role,
        "secondary_roles": secondary_roles,
        "confidence": round(confidence, 2),
        "evidence_terms": sorted(set(evidence_terms)),
    }


def summarize_symbol_semantics(symbol_record: dict[str, Any], kind: str) -> str:
    name = symbol_record.get("qualname") or symbol_record.get("name", "")
    calls = [call.get("call_name", "") for call in symbol_record.get("calls", [])]

    text = " ".join(calls).lower()

    if "connect" in text:
        return f"{kind} {name} wires or reacts to signals."
    if "show" in text or "addtab" in text or "setcentralwidget" in text:
        return f"{kind} {name} builds or displays UI components."
    if "reset" in text or "cleanup" in text:
        return f"{kind} {name} resets or cleans application state."
    if "timeline" in text:
        return f"{kind} {name} manages timeline-related behavior."
    if "topomap" in text or "amplitude_map" in text:
        return f"{kind} {name} manages topomap or amplitude-map behavior."
    if "update_plot" in text or "draw" in text:
        return f"{kind} {name} updates rendered visual state."
    return f"{kind} {name} contributes to project behavior."
8. collector_qt.py
from __future__ import annotations

from typing import Any


def extract_qt_signal_map(files_payload: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    for file_record in files_payload:
        path = file_record["path"]

        for fn in file_record.get("functions", []):
            for call in fn.get("calls", []):
                call_name = call.get("call_name", "")
                if ".connect" in call_name or call_name.endswith("connect"):
                    results.append(
                        {
                            "source_file": path,
                            "source_symbol": fn.get("qualname", fn.get("name", "")),
                            "signal_name": call_name,
                            "target": "unknown",
                            "line": call.get("lineno"),
                            "confidence": 0.65,
                        }
                    )

        for cls in file_record.get("classes", []):
            for method in cls.get("methods", []):
                for call in method.get("calls", []):
                    call_name = call.get("call_name", "")
                    if ".connect" in call_name or call_name.endswith("connect"):
                        results.append(
                            {
                                "source_file": path,
                                "source_symbol": method.get("qualname", method.get("name", "")),
                                "signal_name": call_name,
                                "target": "unknown",
                                "line": call.get("lineno"),
                                "confidence": 0.65,
                            }
                        )

    return results
9. collector_state.py
from __future__ import annotations

from collections import defaultdict


def build_attribute_state_map(files_payload: list[dict]) -> dict:
    state_map: dict = defaultdict(lambda: {"writers": [], "readers": []})

    for file_record in files_payload:
        path = file_record["path"]

        for fn in file_record.get("functions", []):
            symbol = fn.get("qualname", fn.get("name", ""))

            for item in fn.get("assignments", []):
                state_map[item["target"]]["writers"].append(
                    {
                        "file": path,
                        "symbol": symbol,
                        "line": item.get("lineno"),
                    }
                )

            for item in fn.get("attribute_reads", []):
                state_map[item["attribute"]]["readers"].append(
                    {
                        "file": path,
                        "symbol": symbol,
                        "line": item.get("lineno"),
                    }
                )

        for cls in file_record.get("classes", []):
            for method in cls.get("methods", []):
                symbol = method.get("qualname", method.get("name", ""))

                for item in method.get("assignments", []):
                    state_map[item["target"]]["writers"].append(
                        {
                            "file": path,
                            "symbol": symbol,
                            "line": item.get("lineno"),
                        }
                    )

                for item in method.get("attribute_reads", []):
                    state_map[item["attribute"]]["readers"].append(
                        {
                            "file": path,
                            "symbol": symbol,
                            "line": item.get("lineno"),
                        }
                    )

    return dict(state_map)
10. collector_ownership.py
from __future__ import annotations


def build_object_ownership_map(files_payload: list[dict]) -> list[dict]:
    results: list[dict] = []

    for file_record in files_payload:
        path = file_record["path"]

        for fn in file_record.get("functions", []):
            symbol = fn.get("qualname", fn.get("name", ""))
            for item in fn.get("assignments", []):
                target = item.get("target", "")
                if "." in target:
                    results.append(
                        {
                            "object_name": target,
                            "created_by_file": path,
                            "created_by_symbol": symbol,
                            "kind": item.get("value_type", ""),
                            "confidence": 0.7,
                        }
                    )

        for cls in file_record.get("classes", []):
            for method in cls.get("methods", []):
                symbol = method.get("qualname", method.get("name", ""))
                for item in method.get("assignments", []):
                    target = item.get("target", "")
                    if "." in target:
                        results.append(
                            {
                                "object_name": target,
                                "created_by_file": path,
                                "created_by_symbol": symbol,
                                "kind": item.get("value_type", ""),
                                "confidence": 0.7,
                            }
                        )

    return results
11. collector_chains.py
from __future__ import annotations


def _find_matching_symbols(files_payload: list[dict], terms: list[str]) -> list[dict]:
    matches: list[dict] = []

    for file_record in files_payload:
        path = file_record["path"]

        for fn in file_record.get("functions", []):
            name = fn.get("qualname", fn.get("name", "")).lower()
            if any(term in name for term in terms):
                matches.append(
                    {
                        "file": path,
                        "symbol": fn.get("qualname", fn.get("name", "")),
                    }
                )

        for cls in file_record.get("classes", []):
            cls_name = cls.get("name", "").lower()
            if any(term in cls_name for term in terms):
                matches.append(
                    {
                        "file": path,
                        "symbol": cls.get("name", ""),
                    }
                )
            for method in cls.get("methods", []):
                name = method.get("qualname", method.get("name", "")).lower()
                if any(term in name for term in terms):
                    matches.append(
                        {
                            "file": path,
                            "symbol": method.get("qualname", method.get("name", "")),
                        }
                    )

    return matches


def derive_startup_chain(files_payload: list[dict], entry_files: list[str]) -> list[dict]:
    steps: list[dict] = []

    for idx, entry in enumerate(entry_files[:8], start=1):
        steps.append(
            {
                "step": idx,
                "file": entry,
                "symbol": "__main__",
                "why": "entrypoint candidate",
            }
        )

    for item in _find_matching_symbols(files_payload, ["display", "build_and_show", "main", "launcher"])[:12]:
        steps.append(
            {
                "step": len(steps) + 1,
                "file": item["file"],
                "symbol": item["symbol"],
                "why": "startup-related symbol",
            }
        )

    return steps


def derive_timeline_chain(files_payload: list[dict]) -> list[dict]:
    matches = _find_matching_symbols(files_payload, ["timeline"])
    return [
        {
            "step": idx,
            "file": item["file"],
            "symbol": item["symbol"],
            "why": "timeline-related symbol",
        }
        for idx, item in enumerate(matches[:20], start=1)
    ]


def derive_topomap_chain(files_payload: list[dict]) -> list[dict]:
    matches = _find_matching_symbols(files_payload, ["topomap", "amplitude_map", "mcrvlt"])
    return [
        {
            "step": idx,
            "file": item["file"],
            "symbol": item["symbol"],
            "why": "topomap-related symbol",
        }
        for idx, item in enumerate(matches[:20], start=1)
    ]


def derive_reset_chain(files_payload: list[dict]) -> list[dict]:
    matches = _find_matching_symbols(files_payload, ["reset", "snapshot", "cleanup", "close"])
    return [
        {
            "step": idx,
            "file": item["file"],
            "symbol": item["symbol"],
            "why": "reset-related symbol",
        }
        for idx, item in enumerate(matches[:20], start=1)
    ]


def build_execution_chains(files_payload: list[dict], entry_files: list[str]) -> dict:
    return {
        "startup_chain": derive_startup_chain(files_payload, entry_files),
        "timeline_chain": derive_timeline_chain(files_payload),
        "topomap_chain": derive_topomap_chain(files_payload),
        "reset_chain": derive_reset_chain(files_payload),
    }
12. collector_subsystems.py
from __future__ import annotations

from collections import defaultdict


def build_subsystem_summaries(files_payload: list[dict]) -> list[dict]:
    groups: dict[str, list[dict]] = defaultdict(list)

    for file_record in files_payload:
        path = file_record["path"]
        head = path.split("/", 1)[0]
        groups[head].append(file_record)

    results: list[dict] = []

    for name, records in sorted(groups.items()):
        files = [record["path"] for record in records]
        main_symbols: list[str] = []

        for record in records[:10]:
            for cls in record.get("classes", [])[:3]:
                main_symbols.append(cls.get("name", ""))
            for fn in record.get("functions", [])[:3]:
                main_symbols.append(fn.get("qualname", fn.get("name", "")))

        results.append(
            {
                "name": name,
                "files": files[:50],
                "main_symbols": main_symbols[:25],
                "responsibility": f"Subsystem rooted in folder '{name}'.",
            }
        )

    return results
13. collector_duplicates.py
from __future__ import annotations

from collections import defaultdict


def find_duplicate_symbols(files_payload: list[dict]) -> list[dict]:
    symbol_map: dict[str, list[str]] = defaultdict(list)

    for file_record in files_payload:
        path = file_record["path"]

        for fn in file_record.get("functions", []):
            symbol_map[fn.get("name", "")].append(path)

        for cls in file_record.get("classes", []):
            symbol_map[cls.get("name", "")].append(path)
            for method in cls.get("methods", []):
                symbol_map[method.get("name", "")].append(path)

    results: list[dict] = []

    for symbol_name, occurrences in sorted(symbol_map.items()):
        unique_occurrences = sorted(set(occurrences))
        if symbol_name and len(unique_occurrences) > 1:
            results.append(
                {
                    "symbol_name": symbol_name,
                    "occurrences": unique_occurrences,
                    "kind": "name_collision",
                }
            )

    return results
14. collector_tests.py
from __future__ import annotations

from pathlib import Path


def link_tests_to_sources(files_payload: list[dict]) -> list[dict]:
    paths = [record["path"] for record in files_payload]
    test_files = [path for path in paths if "test" in Path(path).name.lower()]

    results: list[dict] = []

    for source_path in paths:
        if source_path in test_files:
            continue

        stem = Path(source_path).stem.lower()
        linked = []

        for test_path in test_files:
            test_stem = Path(test_path).stem.lower()
            if stem in test_stem or test_stem in stem:
                linked.append(test_path)

        if linked:
            results.append(
                {
                    "source_file": source_path,
                    "linked_tests": sorted(set(linked)),
                    "confidence": 0.7,
                }
            )

    return results
15. collector_output.py
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from collector_config import CollectorConfig


def build_collector_info(root: Path) -> dict:
    return {
        "collector_version": "1.1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "root_path": str(root),
    }


def build_collection_config(config: CollectorConfig) -> dict:
    return {
        "excluded_dirs": config.excluded_dirs,
        "include_tests": config.include_tests,
        "include_vendor_code": config.include_vendor_code,
        "max_snippet_lines": config.max_snippet_lines,
        "max_docstring_length": config.max_docstring_length,
    }
16. collector_main.py
from __future__ import annotations

from pathlib import Path

from collector_ast import parse_python_file
from collector_chains import build_execution_chains
from collector_config import CollectorConfig
from collector_duplicates import find_duplicate_symbols
from collector_output import build_collection_config, build_collector_info
from collector_ownership import build_object_ownership_map
from collector_qt import extract_qt_signal_map
from collector_roles import summarize_file_semantics, summarize_symbol_semantics
from collector_state import build_attribute_state_map
from collector_subsystems import build_subsystem_summaries
from collector_tests import link_tests_to_sources
from collector_utils import normalize_path, safe_json_dump
from collector_walker import walk_python_files_filtered


def _build_symbol_index(files_payload: list[dict]) -> dict:
    out: dict = {}

    for file_record in files_payload:
        path = file_record["path"]

        for fn in file_record.get("functions", []):
            symbol = fn.get("qualname", fn.get("name", ""))
            out[symbol] = {
                "file": path,
                "line": fn.get("lineno"),
                "kind": "function",
            }

        for cls in file_record.get("classes", []):
            cls_name = cls.get("name", "")
            out[cls_name] = {
                "file": path,
                "line": cls.get("lineno"),
                "kind": "class",
            }

            for method in cls.get("methods", []):
                symbol = method.get("qualname", method.get("name", ""))
                out[symbol] = {
                    "file": path,
                    "line": method.get("lineno"),
                    "kind": "method",
                }

    return out


def _build_import_graph(files_payload: list[dict]) -> dict:
    return {
        record["module_name"]: record.get("imports", [])
        for record in files_payload
    }


def _build_call_edges(files_payload: list[dict]) -> list[dict]:
    edges: list[dict] = []

    for file_record in files_payload:
        path = file_record["path"]

        for fn in file_record.get("functions", []):
            from_symbol = fn.get("qualname", fn.get("name", ""))
            for call in fn.get("calls", []):
                if call.get("call_name"):
                    edges.append(
                        {
                            "from_file": path,
                            "from_symbol": from_symbol,
                            "to_call": call.get("call_name"),
                            "line": call.get("lineno"),
                        }
                    )

        for cls in file_record.get("classes", []):
            for method in cls.get("methods", []):
                from_symbol = method.get("qualname", method.get("name", ""))
                for call in method.get("calls", []):
                    if call.get("call_name"):
                        edges.append(
                            {
                                "from_file": path,
                                "from_symbol": from_symbol,
                                "to_call": call.get("call_name"),
                                "line": call.get("lineno"),
                            }
                        )

    return edges


def _build_symbol_summaries(files_payload: list[dict]) -> dict:
    summaries: dict = {}

    for file_record in files_payload:
        path = file_record["path"]

        for fn in file_record.get("functions", []):
            symbol = fn.get("qualname", fn.get("name", ""))
            summaries[symbol] = {
                "file": path,
                "kind": "function",
                "summary": summarize_symbol_semantics(fn, "function"),
            }

        for cls in file_record.get("classes", []):
            symbol = cls.get("name", "")
            summaries[symbol] = {
                "file": path,
                "kind": "class",
                "summary": summarize_symbol_semantics(cls, "class"),
            }

            for method in cls.get("methods", []):
                symbol = method.get("qualname", method.get("name", ""))
                summaries[symbol] = {
                    "file": path,
                    "kind": "method",
                    "summary": summarize_symbol_semantics(method, "method"),
                }

    return summaries


def _build_snippet_index(files_payload: list[dict], max_lines: int) -> dict:
    _ = max_lines
    snippets: dict = {}

    for file_record in files_payload:
        path = file_record["path"]
        source = file_record.get("source", "")
        lines = source.splitlines()

        def get_block(lineno: int | None) -> str:
            if not lineno or not lines:
                return ""
            start = max(1, lineno - 8)
            end = min(len(lines), lineno + 20)
            return "\n".join(
                f"{idx:>5} | {lines[idx - 1]}"
                for idx in range(start, end + 1)
            )

        for fn in file_record.get("functions", []):
            symbol = fn.get("qualname", fn.get("name", ""))
            snippets[symbol] = {
                "file": path,
                "line_start": fn.get("lineno"),
                "line_end": fn.get("lineno"),
                "snippet": get_block(fn.get("lineno")),
            }

        for cls in file_record.get("classes", []):
            symbol = cls.get("name", "")
            snippets[symbol] = {
                "file": path,
                "line_start": cls.get("lineno"),
                "line_end": cls.get("lineno"),
                "snippet": get_block(cls.get("lineno")),
            }

            for method in cls.get("methods", []):
                symbol = method.get("qualname", method.get("name", ""))
                snippets[symbol] = {
                    "file": path,
                    "line_start": method.get("lineno"),
                    "line_end": method.get("lineno"),
                    "snippet": get_block(method.get("lineno")),
                }

    return snippets


def run_collector(project_root: str, output_json: str) -> dict:
    root = Path(project_root).expanduser().resolve()
    output_path = Path(output_json).expanduser().resolve()
    config = CollectorConfig()

    files_payload: list[dict] = []
    entry_files: list[str] = []
    errors: list[dict] = []

    python_files = walk_python_files_filtered(root, config)

    for path in python_files:
        rel_path = normalize_path(path, root)
        parsed, error = parse_python_file(path)

        if error is not None:
            errors.append({"file": rel_path, "error": error})
            continue

        module_name = rel_path[:-3].replace("/", ".")
        comments = parsed["comments"]
        strings = parsed["strings"]
        docstring = parsed["module_docstring"]
        semantic = summarize_file_semantics(
            {
                "functions": parsed["functions"],
                "classes": parsed["classes"],
                "comments": comments,
                "strings": strings,
                "imports": parsed["imports"],
                "docstring": docstring,
            }
        )

        entry_markers = []
        joined_source = parsed["source"]
        if '__name__ == "__main__"' in joined_source or "QApplication(" in joined_source:
            entry_markers.append("entry_candidate")
            entry_files.append(rel_path)

        file_record = {
            "path": rel_path,
            "module_name": module_name,
            "imports": parsed["imports"],
            "classes": parsed["classes"],
            "functions": parsed["functions"],
            "docstring": docstring,
            "comments": comments,
            "strings": strings,
            "entry_markers": entry_markers,
            "ui_keyword_hits": [],
            "eeg_keyword_hits": [],
            "semantic_hints": semantic["evidence_terms"],
            "semantic_roles": semantic["roles"],
            "primary_role": semantic["primary_role"],
            "secondary_roles": semantic["secondary_roles"],
            "role_confidence": semantic["confidence"],
            "summary": f"{semantic['primary_role']} file" if semantic["primary_role"] else "general python module",
            "source": parsed["source"],
        }
        files_payload.append(file_record)

    symbol_index = _build_symbol_index(files_payload)
    import_graph = _build_import_graph(files_payload)
    call_edges = _build_call_edges(files_payload)
    qt_signal_map = extract_qt_signal_map(files_payload)
    attribute_state_map = build_attribute_state_map(files_payload)
    object_ownership = build_object_ownership_map(files_payload)
    execution_chains = build_execution_chains(files_payload, entry_files)
    subsystems = build_subsystem_summaries(files_payload)
    symbol_summaries = _build_symbol_summaries(files_payload)
    snippet_index = _build_snippet_index(files_payload, config.max_snippet_lines)
    duplicate_symbols = find_duplicate_symbols(files_payload)
    test_links = link_tests_to_sources(files_payload)

    output = {
        "collector_info": build_collector_info(root),
        "project_summary": {
            "project_root": str(root),
            "python_file_count": len(files_payload),
            "entry_file_count": len(entry_files),
            "entry_files": sorted(set(entry_files)),
            "parse_error_count": len(errors),
        },
        "collection_config": build_collection_config(config),
        "files": files_payload,
        "symbol_index": symbol_index,
        "import_graph": import_graph,
        "call_edges": call_edges,
        "keyword_index": {},
        "semantic_roles": {
            record["path"]: {
                "roles": record["semantic_roles"],
                "primary_role": record["primary_role"],
                "secondary_roles": record["secondary_roles"],
                "confidence": record["role_confidence"],
                "evidence_terms": record["semantic_hints"],
            }
            for record in files_payload
        },
        "qt_signal_map": qt_signal_map,
        "attribute_state_map": attribute_state_map,
        "object_ownership": object_ownership,
        "execution_chains": execution_chains,
        "subsystems": subsystems,
        "symbol_summaries": symbol_summaries,
        "snippet_index": snippet_index,
        "duplicate_symbols": duplicate_symbols,
        "test_links": test_links,
        "errors": errors,
    }

    safe_json_dump(output, output_path)
    return output
17. runner.py
from __future__ import annotations

import sys
from pathlib import Path

from collector_main import run_collector


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage:")
        print("python runner.py <project_root> <output_json>")
        return

    project_root = sys.argv[1]
    output_json = sys.argv[2]

    result = run_collector(project_root, output_json)

    print("Collector finished.")
    print("Project root:", result["project_summary"]["project_root"])
    print("Python files:", result["project_summary"]["python_file_count"])
    print("Entry files:", result["project_summary"]["entry_file_count"])
    print("Parse errors:", result["project_summary"]["parse_error_count"])
    print("Output JSON:", str(Path(output_json).resolve()))


if __name__ == "__main__":
    main()
18. Example run

From inside:

DEVELOPER TOOLS/FULL_INSPECTOR_JSON_APP/project_reasoner_v9_data_collector

python runner.py "E:\eeg_kernel_ai_neural_data_analysis" "E:\eeg_kernel_ai_neural_data_analysis\project_structure_index_v11.json"
19. Immediate next upgrade I recommend

After this modular collector is running, the next best step is:
add a small PySide6 GUI runner for the collector

with:
project folder picker
output JSON picker
checkboxes for:
include tests
include vendor code
exclude venv
and a log box

That would make your collector much easier to use repeatedly.

gime a terminal code tha create all folders in E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9_data _collector

DEVELOPER TOOLS/FULL_INSPECTOR_JSON_APP/project_reasoner_v9_data_collector/
    __init__.py
    runner.py
    collector_main.py
    collector_config.py
    collector_utils.py
    collector_filters.py
    collector_walker.py
    collector_ast.py
    collector_roles.py
    collector_qt.py
    collector_state.py
    collector_ownership.py
    collector_chains.py
    collector_subsystems.py
    collector_duplicates.py
    collector_tests.py
    collector_output.py

Use this PowerShell command:

$root = "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9_data_collector"; New-Item -ItemType Directory -Force -Path $root | Out-Null; @("__init__.py","runner.py","collector_main.py","collector_config.py","collector_utils.py","collector_filters.py","collector_walker.py","collector_ast.py","collector_roles.py","collector_qt.py","collector_state.py","collector_ownership.py","collector_chains.py","collector_subsystems.py","collector_duplicates.py","collector_tests.py","collector_output.py") | ForEach-Object { New-Item -ItemType File -Force -Path (Join-Path $root $_) | Out-Null }; Write-Host "Created:" $root

If you want to confirm everything after creation, run:

Get-ChildItem "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9_data_collector"
run runner.py

E:\mne_py3.10\python.exe "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9_data_collector\runner.py" 
Usage:
python runner.py <project_root> <output_json>

Process finished with exit code 0

That is correct. runner.py requires 2 arguments.

Run it like this:

E:\mne_py3.10\python.exe "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9_data_collector\runner.py" "E:\eeg_kernel_ai_neural_data_analysis" "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_structure_index_v11.json"

If you want the output JSON inside the collector folder itself, use:

E:\mne_py3.10\python.exe "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9_data_collector\runner.py" "E:\eeg_kernel_ai_neural_data_analysis" "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9_data_collector\project_structure_index_v11.json"

If you want, I can also give you a tiny run_collector.bat file so you can double-click it.

correct thi script

from __future__ import annotations

import sys
from pathlib import Path

from collector_main import run_collector


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage:")
        print("python runner.py <project_root> <output_json>")
        return

    project_root = sys.argv[1]
    output_json = sys.argv[2]

    result = run_collector(project_root, output_json)

    print("Collector finished.")
    print("Project root:", result["project_summary"]["project_root"])
    print("Python files:", result["project_summary"]["python_file_count"])
    print("Entry files:", result["project_summary"]["entry_file_count"])
    print("Parse errors:", result["project_summary"]["parse_error_count"])
    print("Output JSON:", str(Path(output_json).resolve()))


if __name__ == "__main__":
    main()
Thought for a couple of seconds

Use this corrected runner.py.

It keeps CLI support, but also works when launched directly without arguments by using sensible defaults for your project.

from __future__ import annotations

import sys
from pathlib import Path

from collector_main import run_collector


DEFAULT_PROJECT_ROOT = Path(r"E:\eeg_kernel_ai_neural_data_analysis")
DEFAULT_OUTPUT_JSON = (
    DEFAULT_PROJECT_ROOT
    / "DEVELOPER TOOLS"
    / "FULL_INSPECTOR_JSON_APP"
    / "project_reasoner_v9_data_collector"
    / "project_structure_index_v11.json"
)


def main() -> None:
    if len(sys.argv) >= 3:
        project_root = Path(sys.argv[1]).expanduser().resolve()
        output_json = Path(sys.argv[2]).expanduser().resolve()
    else:
        project_root = DEFAULT_PROJECT_ROOT.resolve()
        output_json = DEFAULT_OUTPUT_JSON.resolve()

        print("No arguments provided. Using default paths:")
        print("Project root:", str(project_root))
        print("Output JSON:", str(output_json))

    if not project_root.exists():
        print("Error: project root does not exist:")
        print(str(project_root))
        sys.exit(1)

    output_json.parent.mkdir(parents=True, exist_ok=True)

    try:
        result = run_collector(str(project_root), str(output_json))
    except Exception as exc:
        print("Collector failed:")
        print(str(exc))
        sys.exit(1)

    print("Collector finished.")
    print("Project root:", result["project_summary"]["project_root"])
    print("Python files:", result["project_summary"]["python_file_count"])
    print("Entry files:", result["project_summary"]["entry_file_count"])
    print("Parse errors:", result["project_summary"]["parse_error_count"])
    print("Output JSON:", str(output_json))


if __name__ == "__main__":
    main()

Now you can run it directly like this:

E:\mne_py3.10\python.exe "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9_data_collector\runner.py"

Or still pass arguments manually:

E:\mne_py3.10\python.exe "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9_data_collector\runner.py" "E:\eeg_kernel_ai_neural_data_analysis" "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9_data_collector\project_structure_index_v11.json"
I want to use gui and start from  script
Thought for 5s

Great. Then the best approach is:

make runner.py start a small PySide6 GUI
let the GUI choose:
project root
output JSON
then call run_collector(...)

Use this as your new runner.py:

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)

from collector_main import run_collector


DEFAULT_PROJECT_ROOT = Path(r"E:\eeg_kernel_ai_neural_data_analysis")
DEFAULT_OUTPUT_JSON = (
    DEFAULT_PROJECT_ROOT
    / "DEVELOPER TOOLS"
    / "FULL_INSPECTOR_JSON_APP"
    / "project_reasoner_v9_data_collector"
    / "project_structure_index_v11.json"
)


class CollectorRunnerWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Project Reasoner V9 Data Collector")
        self.resize(900, 500)

        self.project_root_edit = QLineEdit(str(DEFAULT_PROJECT_ROOT))
        self.output_json_edit = QLineEdit(str(DEFAULT_OUTPUT_JSON))

        self.browse_project_button = QPushButton("Browse Project")
        self.browse_output_button = QPushButton("Browse Output")
        self.run_button = QPushButton("Run Collector")

        self.log_box = QPlainTextEdit()
        self.log_box.setReadOnly(True)

        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

        grid = QGridLayout()
        grid.addWidget(QLabel("Project root:"), 0, 0)
        grid.addWidget(self.project_root_edit, 0, 1)
        grid.addWidget(self.browse_project_button, 0, 2)

        grid.addWidget(QLabel("Output JSON:"), 1, 0)
        grid.addWidget(self.output_json_edit, 1, 1)
        grid.addWidget(self.browse_output_button, 1, 2)

        button_row = QHBoxLayout()
        button_row.addStretch()
        button_row.addWidget(self.run_button)

        main_layout.addLayout(grid)
        main_layout.addLayout(button_row)
        main_layout.addWidget(QLabel("Log:"))
        main_layout.addWidget(self.log_box)

    def _connect_signals(self) -> None:
        self.browse_project_button.clicked.connect(self._browse_project_root)
        self.browse_output_button.clicked.connect(self._browse_output_json)
        self.run_button.clicked.connect(self._run_collector)

    def _append_log(self, text: str) -> None:
        self.log_box.appendPlainText(text)

    def _browse_project_root(self) -> None:
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select project root",
            self.project_root_edit.text().strip() or str(DEFAULT_PROJECT_ROOT),
        )
        if folder:
            self.project_root_edit.setText(folder)

    def _browse_output_json(self) -> None:
        file_path, _selected_filter = QFileDialog.getSaveFileName(
            self,
            "Select output JSON",
            self.output_json_edit.text().strip() or str(DEFAULT_OUTPUT_JSON),
            "JSON Files (*.json)",
        )
        if file_path:
            self.output_json_edit.setText(file_path)

    def _run_collector(self) -> None:
        project_root = Path(self.project_root_edit.text().strip()).expanduser().resolve()
        output_json = Path(self.output_json_edit.text().strip()).expanduser().resolve()

        if not project_root.exists():
            QMessageBox.warning(
                self,
                "Invalid project root",
                "Project root does not exist:\n" + str(project_root),
            )
            return

        output_json.parent.mkdir(parents=True, exist_ok=True)

        self.log_box.clear()
        self._append_log("Running collector...")
        self._append_log("Project root: " + str(project_root))
        self._append_log("Output JSON: " + str(output_json))

        try:
            result = run_collector(str(project_root), str(output_json))
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Collector failed",
                str(exc),
            )
            self._append_log("Collector failed:")
            self._append_log(str(exc))
            return

        self._append_log("")
        self._append_log("Collector finished.")
        self._append_log("Project root: " + result["project_summary"]["project_root"])
        self._append_log("Python files: " + str(result["project_summary"]["python_file_count"]))
        self._append_log("Entry files: " + str(result["project_summary"]["entry_file_count"]))
        self._append_log("Parse errors: " + str(result["project_summary"]["parse_error_count"]))
        self._append_log("Output JSON: " + str(output_json))

        QMessageBox.information(
            self,
            "Done",
            "Collector finished successfully.\n\nOutput:\n" + str(output_json),
        )


def main() -> None:
    app = QApplication(sys.argv)
    window = CollectorRunnerWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

Now you can start it exactly from script:

E:\mne_py3.10\python.exe "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9_data_collector\runner.py"

If you want, next I can also give you a second version where the collector runs in a background thread so the GUI does not freeze during large scans.

runner error  utf-8 codec cant encoder charachters  in positino 7552... surrogates no allowed , correct an also ignore emojis
Thought for 6s

Yes. The fix is to sanitize all text before writing JSON and before appending to the GUI log.

The safest solution is:

replace invalid surrogate characters
ignore characters that cannot be encoded
optionally strip emojis from output text

Do these 2 changes.

Update collector_utils.py to this:

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


_EMOJI_PATTERN = re.compile(
    "["
    "\U0001F300-\U0001F5FF"
    "\U0001F600-\U0001F64F"
    "\U0001F680-\U0001F6FF"
    "\U0001F700-\U0001F77F"
    "\U0001F780-\U0001F7FF"
    "\U0001F800-\U0001F8FF"
    "\U0001F900-\U0001F9FF"
    "\U0001FA00-\U0001FA6F"
    "\U0001FA70-\U0001FAFF"
    "\u2600-\u26FF"
    "\u2700-\u27BF"
    "]+",
    flags=re.UNICODE,
)


def _sanitize_text(value: str, remove_emojis: bool = True) -> str:
    if not isinstance(value, str):
        value = str(value)

    value = value.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")

    if remove_emojis:
        value = _EMOJI_PATTERN.sub("", value)

    return value


def sanitize_for_json(data: Any, remove_emojis: bool = True) -> Any:
    if isinstance(data, dict):
        clean_dict = {}
        for key, value in data.items():
            clean_key = _sanitize_text(key, remove_emojis=remove_emojis)
            clean_dict[clean_key] = sanitize_for_json(value, remove_emojis=remove_emojis)
        return clean_dict

    if isinstance(data, list):
        return [sanitize_for_json(item, remove_emojis=remove_emojis) for item in data]

    if isinstance(data, tuple):
        return [sanitize_for_json(item, remove_emojis=remove_emojis) for item in data]

    if isinstance(data, str):
        return _sanitize_text(data, remove_emojis=remove_emojis)

    return data


def safe_read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def normalize_path(path: Path, root: Path) -> str:
    return str(path.resolve().relative_to(root.resolve())).replace("\\", "/")


def short_hash(value: str) -> str:
    return hashlib.sha1(value.encode("utf-8", errors="replace")).hexdigest()[:12]


def compact_whitespace(text: str) -> str:
    return " ".join(str(text).split())


def safe_json_dump(data: Any, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    clean_data = sanitize_for_json(data, remove_emojis=True)
    json_text = json.dumps(
        clean_data,
        indent=2,
        ensure_ascii=False,
    )

    json_text = json_text.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")

    output_path.write_text(
        json_text,
        encoding="utf-8",
        errors="ignore",
    )

Now update runner.py so the log also sanitizes text before showing it:

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)

from collector_main import run_collector
from collector_utils import sanitize_for_json


DEFAULT_PROJECT_ROOT = Path(r"E:\eeg_kernel_ai_neural_data_analysis")
DEFAULT_OUTPUT_JSON = (
    DEFAULT_PROJECT_ROOT
    / "DEVELOPER TOOLS"
    / "FULL_INSPECTOR_JSON_APP"
    / "project_reasoner_v9_data_collector"
    / "project_structure_index_v11.json"
)


class CollectorRunnerWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Project Reasoner V9 Data Collector")
        self.resize(900, 500)

        self.project_root_edit = QLineEdit(str(DEFAULT_PROJECT_ROOT))
        self.output_json_edit = QLineEdit(str(DEFAULT_OUTPUT_JSON))

        self.browse_project_button = QPushButton("Browse Project")
        self.browse_output_button = QPushButton("Browse Output")
        self.run_button = QPushButton("Run Collector")

        self.log_box = QPlainTextEdit()
        self.log_box.setReadOnly(True)

        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

        grid = QGridLayout()
        grid.addWidget(QLabel("Project root:"), 0, 0)
        grid.addWidget(self.project_root_edit, 0, 1)
        grid.addWidget(self.browse_project_button, 0, 2)

        grid.addWidget(QLabel("Output JSON:"), 1, 0)
        grid.addWidget(self.output_json_edit, 1, 1)
        grid.addWidget(self.browse_output_button, 1, 2)

        button_row = QHBoxLayout()
        button_row.addStretch()
        button_row.addWidget(self.run_button)

        main_layout.addLayout(grid)
        main_layout.addLayout(button_row)
        main_layout.addWidget(QLabel("Log:"))
        main_layout.addWidget(self.log_box)

    def _connect_signals(self) -> None:
        self.browse_project_button.clicked.connect(self._browse_project_root)
        self.browse_output_button.clicked.connect(self._browse_output_json)
        self.run_button.clicked.connect(self._run_collector)

    def _append_log(self, text: str) -> None:
        clean_text = sanitize_for_json(str(text), remove_emojis=True)
        self.log_box.appendPlainText(clean_text)

    def _browse_project_root(self) -> None:
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select project root",
            self.project_root_edit.text().strip() or str(DEFAULT_PROJECT_ROOT),
        )
        if folder:
            self.project_root_edit.setText(folder)

    def _browse_output_json(self) -> None:
        file_path, _selected_filter = QFileDialog.getSaveFileName(
            self,
            "Select output JSON",
            self.output_json_edit.text().strip() or str(DEFAULT_OUTPUT_JSON),
            "JSON Files (*.json)",
        )
        if file_path:
            self.output_json_edit.setText(file_path)

    def _run_collector(self) -> None:
        project_root = Path(self.project_root_edit.text().strip()).expanduser().resolve()
        output_json = Path(self.output_json_edit.text().strip()).expanduser().resolve()

        if not project_root.exists():
            QMessageBox.warning(
                self,
                "Invalid project root",
                "Project root does not exist:\n" + str(project_root),
            )
            return

        output_json.parent.mkdir(parents=True, exist_ok=True)

        self.log_box.clear()
        self._append_log("Running collector...")
        self._append_log("Project root: " + str(project_root))
        self._append_log("Output JSON: " + str(output_json))

        try:
            result = run_collector(str(project_root), str(output_json))
        except Exception as exc:
            clean_error = sanitize_for_json(str(exc), remove_emojis=True)
            QMessageBox.critical(
                self,
                "Collector failed",
                clean_error,
            )
            self._append_log("Collector failed:")
            self._append_log(clean_error)
            return

        self._append_log("")
        self._append_log("Collector finished.")
        self._append_log("Project root: " + result["project_summary"]["project_root"])
        self._append_log("Python files: " + str(result["project_summary"]["python_file_count"]))
        self._append_log("Entry files: " + str(result["project_summary"]["entry_file_count"]))
        self._append_log("Parse errors: " + str(result["project_summary"]["parse_error_count"]))
        self._append_log("Output JSON: " + str(output_json))

        QMessageBox.information(
            self,
            "Done",
            "Collector finished successfully.\n\nOutput:\n" + str(output_json),
        )


def main() -> None:
    app = QApplication(sys.argv)
    window = CollectorRunnerWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

Why this fixes it:
the JSON is sanitized before saving
bad surrogate characters are dropped
emoji characters are removed
GUI log text is also sanitized before display

If the error still appears after this, then the source is probably inside AST extraction or snippet collection, and the next place to harden is collector_ast.py by sanitizing comments, strings, docstrings, and source before returning them.

how do lyou evaluate this cata collection , how much ai will know about project with this json?
Thought for a couple of seconds

It is already a strong collection for structural reasoning, but not yet a full project understanding.

My honest evaluation:

It gives the AI a very good map of the project.
It does not give the AI full human-level understanding of the project.
It is much better than raw grep.
It is still weaker than a combination of:
good index + curated architectural summaries + selected source snippets + real runtime traces.

How much the AI will know from this JSON

With the current collector, the AI will know reasonably well:

which files exist
which modules import which
which classes and functions exist
rough call relationships
which files look like startup, timeline, splash, topomap, filters, reset, tabs
where symbols are located
some docstrings, comments, and strings
some likely execution chains
some ownership/state patterns
some subsystem grouping
some duplicate symbol ambiguity

That means it can answer many questions like:

which file likely starts the app
which module builds the main window
which modules are related to timeline
which symbols are involved in topomap
which module owns reset logic
which subsystems exist
where a class or method is defined
which files look most relevant to a given feature

For those questions, this JSON can make the AI quite effective.

My approximate score

For architecture Q&A based only on static project data, I would rate it:

around 7/10 for structural understanding
around 5.5/10 for behavioral understanding
around 4/10 for precise runtime truth

Why 7/10 structurally
Because the collector captures many of the things an architectural assistant needs:
file graph
symbol graph
role inference
chains
ownership/state summaries
subsystems

Why only 5.5/10 behaviorally
Because behavior is not only in AST structure.
A lot of truth in a GUI app depends on:
dynamic signal connections
which branch actually executes
which object instance is active
what gets reassigned later
which old path is deprecated but still present
which imported helper is the real one in runtime

Why only 4/10 for runtime truth
Because static JSON does not know:
actual runtime object states
actual startup path chosen by the user
which code paths are dead
which try/except silently fail
which dynamically imported modules load
which callbacks are really firing
what data values flow during execution

What this JSON is best at

This collector is best for:
architectural navigation
symbol discovery
responsibility mapping
feature-to-file mapping
follow-up reasoning over static structure
retrieval for local AI

It is not best for:
debugging real runtime bugs
confirming exact execution order in all situations
understanding hidden side effects from dynamic code
knowing whether a feature actually works

Biggest strengths

The strongest part of your approach is that you are not giving the AI only code blobs.
You are giving it a compressed architectural representation.

That is much better for questions like:
where is timeline implemented
who creates the superior tab
what module starts the app
what owns splash
what resets EEG state

In those cases, this kind of JSON is extremely useful.

Biggest weaknesses

The main weaknesses are:

static only
The AI sees inferred structure, not actual runtime behavior.

heuristic roles
Roles like startup, topomap, timeline are inferred from text patterns, not guaranteed.

call graph is partial
AST call extraction sees names, not always exact resolved targets.

Qt signal mapping is still heuristic
It sees connect-like patterns, but not always exact sender/receiver semantics.

no confidence-aware retrieval yet
Even though you plan confidence fields, many answers may still sound more certain than the data deserves unless V9 uses those fields carefully.

duplicate/legacy code contamination
If the repo has old/deprecated modules, the AI may still partially confuse them unless the collector marks active vs legacy.

What the AI will probably answer well right now

It should do well on:

Which module starts the app?
Which code creates tabs?
Where is timeline wired?
Where is splash created?
Where is reset logic?
Which modules are involved in topomap?
What are the major subsystems?
Which class owns a given responsibility?
Which symbols are duplicated?

What it may still answer imperfectly

It may struggle or become partially speculative on:

Which exact path runs first at runtime in all cases?
Which of two similar modules is the truly active one?
Which signal connection is actually effective at runtime?
Why a GUI element flashes then disappears?
Why a callback did not fire?
Which branch is used only after a file is loaded?
What state changes after a specific click in the running app?

For those, static collection alone is not enough.

What would make AI know much more

To move from “good architectural map” to “near-expert project memory,” I would add three more data sources on top of this JSON.

First: runtime trace layer
Capture:
startup trace
signal connect trace
object creation trace
major state changes
tab switch trace
timeline click trace
topomap toggle trace

Second: curated architectural notes
A small manually written file per subsystem:
startup
window builder
timeline
topomap
filters
reset
splash

Third: active vs deprecated labeling
Mark modules as:
active
legacy
backup
experimental
deprecated

That would reduce one of the biggest sources of AI confusion in large evolving projects.

My bottom-line judgment

This collector is good enough to make a local AI meaningfully useful for project questions.
It is not enough to make the AI “fully know” the project in the way a maintainer knows it.

A fair statement would be:

The AI will know the project's static architecture fairly well, but not its full runtime truth.

If you combine this JSON with:
targeted snippets,
conversation memory,
and a small runtime trace layer,

then the AI can become very strong for this project.

My practical estimate

With your current improved JSON, for architecture questions:
the AI may answer correctly or near-correctly in maybe 70 to 85 percent of common navigation questions

For exact runtime/debugging questions:
it may drop to maybe 40 to 60 percent unless supported by runtime traces or code snippets from the real execution path

Best next step

The highest-value next improvement is not adding even more raw static fields.
It is adding a second collector:
a lightweight runtime evidence collector.

That would dramatically raise the AI's effective understanding.

do it and we present 2 files to AI?
Thought for 5s

Yes. That is the right next step.

Use 2 complementary files:

File 1
Static architecture index
This is your current collector output.

File 2
Runtime evidence trace
This will capture what actually happened when the app ran.

That combination is much stronger than trying to force one file to do everything.

Why 2 files is better

The static file tells the AI:
what exists
where it is
who imports whom
which symbols and likely chains exist

The runtime file tells the AI:
what actually executed
which objects were created
which signals fired
which state changed
what path was really taken

So the AI can answer with both:
architectural possibility
and runtime reality

Best design

I would present both files to AI, but with different roles.

Static JSON
source of truth for project structure

Runtime JSON
source of truth for actual observed behavior

Then the AI prompt should say something like:
Use static JSON for architecture and code ownership.
Use runtime JSON for actual execution evidence.
If they disagree, mention the disagreement explicitly.

Recommended names

project_structure_index_v11.json
project_runtime_trace_v1.json

What the runtime collector should capture

Not everything.
Only high-value events.

I would collect:

startup events
window creation
tab creation
tab switch
signal connection
signal emission
timeline click
timeline move
EEG load
topomap toggle
reset/cleanup
exceptions
warnings
state changes for core attributes

Good runtime schema

{
  "trace_info": {},
  "session_info": {},
  "events": [],
  "state_snapshots": [],
  "errors": [],
  "warnings": []
}

Better detailed schema

{
  "trace_info": {
    "trace_version": "1.0",
    "generated_at": "2026-03-13T14:20:00"
  },
  "session_info": {
    "project_root": "E:/eeg_kernel_ai_neural_data_analysis",
    "entry_script": "shell/viewer/eeg_display_launcher.py"
  },
  "events": [
    {
      "id": 1,
      "time": "2026-03-13T14:20:01.103",
      "type": "startup",
      "source_file": "shell/viewer/eeg_display_launcher.py",
      "source_symbol": "display_pyside6_eeg_visualizer",
      "message": "Display launcher entered"
    },
    {
      "id": 2,
      "time": "2026-03-13T14:20:01.205",
      "type": "object_created",
      "object_name": "visualizer.main_window",
      "object_type": "QMainWindow",
      "source_file": "shell/viewer/eeg_main_window_builder.py",
      "source_symbol": "EEGMainWindowBuilder.build_and_show"
    }
  ],
  "state_snapshots": [
    {
      "time": "2026-03-13T14:20:01.500",
      "label": "after_main_window",
      "state": {
        "main_window_exists": true,
        "notebook_exists": true,
        "current_tab": "EEG Traces"
      }
    }
  ],
  "errors": [],
  "warnings": []
}

How to collect runtime evidence

Three possible levels.

Level 1
Manual instrumentation
Fastest and best first step.

Insert logging calls in important methods:
startup
builder
timeline
topomap
reset
signals

Each writes structured JSON line events.

Level 2
Decorator-based tracer
Create a decorator like:
@trace_event("timeline")
and apply it to selected functions.

Level 3
Qt signal and object monkey-patching
Most powerful, but more invasive.
Do this later.

My recommendation:
start with Level 1 plus a tiny helper API.

Best implementation architecture

Create a second package:

DEVELOPER TOOLS/FULL_INSPECTOR_JSON_APP/project_reasoner_v9_runtime_collector

Suggested files:

project_reasoner_v9_runtime_collector/
    __init__.py
    runtime_trace_writer.py
    runtime_trace_state.py
    runtime_trace_helpers.py
    runtime_trace_decorators.py
    runner.py

Core idea

A single writer class:

RuntimeTraceWriter

Methods:
trace_event(...)
trace_warning(...)
trace_error(...)
trace_state_snapshot(...)
save()

Then in your app, important places call it.

Example usage in real modules

In startup:

trace_writer.trace_event(
    event_type="startup",
    source_file="shell/viewer/eeg_display_launcher.py",
    source_symbol="display_pyside6_eeg_visualizer",
    message="Display launcher entered",
)

In main window builder:

trace_writer.trace_event(
    event_type="object_created",
    source_file="shell/viewer/eeg_main_window_builder.py",
    source_symbol="EEGMainWindowBuilder.build_and_show",
    object_name="visualizer.main_window",
    message="Main window created",
)

In timeline click:

trace_writer.trace_event(
    event_type="timeline_click",
    source_file="shell/viewer/eeg_timeline_manager_core.py",
    source_symbol="TimelineManager.handle_timeline_clicked",
    message=f"Clicked time: {clicked_time}",
)

In reset:

trace_writer.trace_event(
    event_type="reset",
    source_file="core/snapshot/eeg_session_snapshot.py",
    source_symbol="reset_to_initial_eeg_state",
    message="Reset to initial EEG state started",
)

How AI should use the 2 files

Yes, present both files to the AI.

Best prompt policy:

First use static JSON to locate relevant files, symbols, and chains.
Then use runtime JSON to validate what really happened.
If runtime evidence exists, prefer it for actual behavior.
If only static evidence exists, say behavior is inferred.
If static and runtime disagree, report both.

That makes the AI much more trustworthy.

What questions become much better with 2 files

With both files, the AI can answer much better:

Which code starts the app?
Which path actually ran in this last session?
Why did splash disappear?
Was timeline really connected?
Did topomap initializer actually run?
Was reset called when close happened?
Which object was created first?
Which tab was active after startup?
What state changed after timeline click?

This is the jump from:
good static architect
to
useful debugging assistant

My recommendation

Yes:
keep the static collector
add a runtime collector
present both files to AI

That is exactly the right architecture.

Next step

I can now draft the full modular package for the runtime collector, with:
folder structure
all file contents
a tiny JSON writer
and example instrumentation points for your EEG app.

go
Thought for 9s

Excellent. Below is a full modular runtime collector package you can create and then instrument into the EEG app.

Goal:
produce a second JSON file with real execution evidence

Suggested folder:

DEVELOPER TOOLS/FULL_INSPECTOR_JSON_APP/project_reasoner_v9_runtime_collector/
    __init__.py
    runtime_trace_models.py
    runtime_trace_utils.py
    runtime_trace_writer.py
    runtime_trace_state.py
    runtime_trace_decorators.py
    runtime_trace_api.py
    runner.py

Use these files.

__init__.py

from runtime_trace_api import (
    configure_runtime_trace,
    get_runtime_trace_writer,
    save_runtime_trace,
    trace_error,
    trace_event,
    trace_state_snapshot,
    trace_warning,
)

runtime_trace_models.py

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class TraceEvent:
    event_id: int
    time: str
    event_type: str
    source_file: str
    source_symbol: str
    message: str = ""
    object_name: str = ""
    object_type: str = ""
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class TraceStateSnapshot:
    snapshot_id: int
    time: str
    label: str
    state: dict[str, Any] = field(default_factory=dict)


@dataclass
class TraceIssue:
    issue_id: int
    time: str
    source_file: str
    source_symbol: str
    message: str
    extra: dict[str, Any] = field(default_factory=dict)

runtime_trace_utils.py

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


def now_iso() -> str:
    return datetime.now().isoformat(timespec="milliseconds")


def sanitize_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value)
    return text.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")


def sanitize_data(data: Any) -> Any:
    if isinstance(data, dict):
        return {
            sanitize_text(key): sanitize_data(value)
            for key, value in data.items()
        }
    if isinstance(data, list):
        return [sanitize_data(item) for item in data]
    if isinstance(data, tuple):
        return [sanitize_data(item) for item in data]
    if isinstance(data, str):
        return sanitize_text(data)
    return data


def safe_json_dump(data: Any, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    clean_data = sanitize_data(data)
    json_text = json.dumps(clean_data, indent=2, ensure_ascii=False)
    json_text = json_text.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")
    output_path.write_text(json_text, encoding="utf-8", errors="ignore")

runtime_trace_writer.py

from __future__ import annotations

from pathlib import Path
from typing import Any

from runtime_trace_models import TraceEvent, TraceIssue, TraceStateSnapshot
from runtime_trace_utils import now_iso, safe_json_dump, sanitize_data, sanitize_text


class RuntimeTraceWriter:
    def __init__(self) -> None:
        self.project_root: str = ""
        self.entry_script: str = ""
        self.output_path: Path | None = None

        self._event_counter = 0
        self._snapshot_counter = 0
        self._issue_counter = 0

        self.events: list[TraceEvent] = []
        self.state_snapshots: list[TraceStateSnapshot] = []
        self.errors: list[TraceIssue] = []
        self.warnings: list[TraceIssue] = []

    def configure(
        self,
        *,
        project_root: str,
        output_path: str,
        entry_script: str = "",
    ) -> None:
        self.project_root = sanitize_text(project_root)
        self.entry_script = sanitize_text(entry_script)
        self.output_path = Path(output_path).expanduser().resolve()

    def trace_event(
        self,
        *,
        event_type: str,
        source_file: str,
        source_symbol: str,
        message: str = "",
        object_name: str = "",
        object_type: str = "",
        extra: dict[str, Any] | None = None,
    ) -> None:
        self._event_counter += 1
        self.events.append(
            TraceEvent(
                event_id=self._event_counter,
                time=now_iso(),
                event_type=sanitize_text(event_type),
                source_file=sanitize_text(source_file),
                source_symbol=sanitize_text(source_symbol),
                message=sanitize_text(message),
                object_name=sanitize_text(object_name),
                object_type=sanitize_text(object_type),
                extra=sanitize_data(extra or {}),
            )
        )

    def trace_state_snapshot(
        self,
        *,
        label: str,
        state: dict[str, Any],
    ) -> None:
        self._snapshot_counter += 1
        self.state_snapshots.append(
            TraceStateSnapshot(
                snapshot_id=self._snapshot_counter,
                time=now_iso(),
                label=sanitize_text(label),
                state=sanitize_data(state),
            )
        )

    def trace_error(
        self,
        *,
        source_file: str,
        source_symbol: str,
        message: str,
        extra: dict[str, Any] | None = None,
    ) -> None:
        self._issue_counter += 1
        self.errors.append(
            TraceIssue(
                issue_id=self._issue_counter,
                time=now_iso(),
                source_file=sanitize_text(source_file),
                source_symbol=sanitize_text(source_symbol),
                message=sanitize_text(message),
                extra=sanitize_data(extra or {}),
            )
        )

    def trace_warning(
        self,
        *,
        source_file: str,
        source_symbol: str,
        message: str,
        extra: dict[str, Any] | None = None,
    ) -> None:
        self._issue_counter += 1
        self.warnings.append(
            TraceIssue(
                issue_id=self._issue_counter,
                time=now_iso(),
                source_file=sanitize_text(source_file),
                source_symbol=sanitize_text(source_symbol),
                message=sanitize_text(message),
                extra=sanitize_data(extra or {}),
            )
        )

    def build_payload(self) -> dict[str, Any]:
        return {
            "trace_info": {
                "trace_version": "1.0",
                "generated_at": now_iso(),
            },
            "session_info": {
                "project_root": self.project_root,
                "entry_script": self.entry_script,
            },
            "events": [
                {
                    "id": item.event_id,
                    "time": item.time,
                    "type": item.event_type,
                    "source_file": item.source_file,
                    "source_symbol": item.source_symbol,
                    "message": item.message,
                    "object_name": item.object_name,
                    "object_type": item.object_type,
                    "extra": item.extra,
                }
                for item in self.events
            ],
            "state_snapshots": [
                {
                    "id": item.snapshot_id,
                    "time": item.time,
                    "label": item.label,
                    "state": item.state,
                }
                for item in self.state_snapshots
            ],
            "errors": [
                {
                    "id": item.issue_id,
                    "time": item.time,
                    "source_file": item.source_file,
                    "source_symbol": item.source_symbol,
                    "message": item.message,
                    "extra": item.extra,
                }
                for item in self.errors
            ],
            "warnings": [
                {
                    "id": item.issue_id,
                    "time": item.time,
                    "source_file": item.source_file,
                    "source_symbol": item.source_symbol,
                    "message": item.message,
                    "extra": item.extra,
                }
                for item in self.warnings
            ],
        }

    def save(self) -> Path:
        if self.output_path is None:
            raise RuntimeError("RuntimeTraceWriter is not configured.")
        payload = self.build_payload()
        safe_json_dump(payload, self.output_path)
        return self.output_path

runtime_trace_state.py

from __future__ import annotations

from typing import Any


def collect_visualizer_state(visualizer: Any) -> dict[str, Any]:
    state: dict[str, Any] = {}

    state["main_window_exists"] = getattr(visualizer, "main_window", None) is not None
    state["notebook_exists"] = getattr(visualizer, "notebook", None) is not None
    state["splash_exists"] = getattr(visualizer, "splash", None) is not None
    state["timeline_widget_exists"] = getattr(visualizer, "timeline_widget", None) is not None
    state["canvas_exists"] = getattr(visualizer, "canvas", None) is not None
    state["raw_exists"] = getattr(visualizer, "raw", None) is not None
    state["data_exists"] = getattr(visualizer, "data", None) is not None

    state["current_start"] = getattr(visualizer, "current_start", None)
    state["window_size"] = getattr(visualizer, "window_size", None)
    state["amplitude_scale"] = getattr(visualizer, "amplitude_scale", None)
    state["total_duration"] = getattr(visualizer, "total_duration", None)

    notebook = getattr(visualizer, "notebook", None)
    if notebook is not None:
        try:
            state["current_tab"] = notebook.tabText(notebook.currentIndex())
        except Exception:
            state["current_tab"] = ""
    else:
        state["current_tab"] = ""

    return state

runtime_trace_decorators.py

from __future__ import annotations

from functools import wraps
from typing import Any, Callable

from runtime_trace_api import get_runtime_trace_writer


def trace_runtime_event(
    event_type: str,
    source_file: str,
    source_symbol: str,
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any):
            writer = get_runtime_trace_writer()
            if writer is not None:
                writer.trace_event(
                    event_type=event_type,
                    source_file=source_file,
                    source_symbol=source_symbol,
                    message="entered",
                )

            try:
                result = func(*args, **kwargs)
            except Exception as exc:
                writer = get_runtime_trace_writer()
                if writer is not None:
                    writer.trace_error(
                        source_file=source_file,
                        source_symbol=source_symbol,
                        message=str(exc),
                    )
                raise

            writer = get_runtime_trace_writer()
            if writer is not None:
                writer.trace_event(
                    event_type=event_type,
                    source_file=source_file,
                    source_symbol=source_symbol,
                    message="completed",
                )

            return result

        return wrapper

    return decorator

runtime_trace_api.py

from __future__ import annotations

from pathlib import Path
from typing import Any

from runtime_trace_writer import RuntimeTraceWriter


_TRACE_WRITER: RuntimeTraceWriter | None = None


def configure_runtime_trace(
    *,
    project_root: str,
    output_path: str,
    entry_script: str = "",
) -> RuntimeTraceWriter:
    global _TRACE_WRITER
    _TRACE_WRITER = RuntimeTraceWriter()
    _TRACE_WRITER.configure(
        project_root=project_root,
        output_path=output_path,
        entry_script=entry_script,
    )
    return _TRACE_WRITER


def get_runtime_trace_writer() -> RuntimeTraceWriter | None:
    return _TRACE_WRITER


def trace_event(
    *,
    event_type: str,
    source_file: str,
    source_symbol: str,
    message: str = "",
    object_name: str = "",
    object_type: str = "",
    extra: dict[str, Any] | None = None,
) -> None:
    writer = get_runtime_trace_writer()
    if writer is None:
        return
    writer.trace_event(
        event_type=event_type,
        source_file=source_file,
        source_symbol=source_symbol,
        message=message,
        object_name=object_name,
        object_type=object_type,
        extra=extra,
    )


def trace_state_snapshot(
    *,
    label: str,
    state: dict[str, Any],
) -> None:
    writer = get_runtime_trace_writer()
    if writer is None:
        return
    writer.trace_state_snapshot(label=label, state=state)


def trace_error(
    *,
    source_file: str,
    source_symbol: str,
    message: str,
    extra: dict[str, Any] | None = None,
) -> None:
    writer = get_runtime_trace_writer()
    if writer is None:
        return
    writer.trace_error(
        source_file=source_file,
        source_symbol=source_symbol,
        message=message,
        extra=extra,
    )


def trace_warning(
    *,
    source_file: str,
    source_symbol: str,
    message: str,
    extra: dict[str, Any] | None = None,
) -> None:
    writer = get_runtime_trace_writer()
    if writer is None:
        return
    writer.trace_warning(
        source_file=source_file,
        source_symbol=source_symbol,
        message=message,
        extra=extra,
    )


def save_runtime_trace() -> Path | None:
    writer = get_runtime_trace_writer()
    if writer is None:
        return None
    return writer.save()

runner.py

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)

from runtime_trace_api import configure_runtime_trace, save_runtime_trace


DEFAULT_PROJECT_ROOT = Path(r"E:\eeg_kernel_ai_neural_data_analysis")
DEFAULT_OUTPUT_JSON = (
    DEFAULT_PROJECT_ROOT
    / "DEVELOPER TOOLS"
    / "FULL_INSPECTOR_JSON_APP"
    / "project_runtime_trace_v1.json"
)


class RuntimeCollectorWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Project Reasoner V9 Runtime Collector")
        self.resize(900, 460)

        self.project_root_edit = QLineEdit(str(DEFAULT_PROJECT_ROOT))
        self.output_json_edit = QLineEdit(str(DEFAULT_OUTPUT_JSON))
        self.entry_script_edit = QLineEdit("manual_session")

        self.browse_project_button = QPushButton("Browse Project")
        self.browse_output_button = QPushButton("Browse Output")
        self.configure_button = QPushButton("Configure Trace")
        self.save_button = QPushButton("Save Trace")

        self.log_box = QPlainTextEdit()
        self.log_box.setReadOnly(True)

        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

        grid = QGridLayout()
        grid.addWidget(QLabel("Project root:"), 0, 0)
        grid.addWidget(self.project_root_edit, 0, 1)
        grid.addWidget(self.browse_project_button, 0, 2)

        grid.addWidget(QLabel("Output JSON:"), 1, 0)
        grid.addWidget(self.output_json_edit, 1, 1)
        grid.addWidget(self.browse_output_button, 1, 2)

        grid.addWidget(QLabel("Entry script label:"), 2, 0)
        grid.addWidget(self.entry_script_edit, 2, 1)

        row = QHBoxLayout()
        row.addStretch()
        row.addWidget(self.configure_button)
        row.addWidget(self.save_button)

        main_layout.addLayout(grid)
        main_layout.addLayout(row)
        main_layout.addWidget(QLabel("Log:"))
        main_layout.addWidget(self.log_box)

    def _connect_signals(self) -> None:
        self.browse_project_button.clicked.connect(self._browse_project_root)
        self.browse_output_button.clicked.connect(self._browse_output_json)
        self.configure_button.clicked.connect(self._configure_trace)
        self.save_button.clicked.connect(self._save_trace)

    def _append_log(self, text: str) -> None:
        self.log_box.appendPlainText(str(text))

    def _browse_project_root(self) -> None:
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select project root",
            self.project_root_edit.text().strip() or str(DEFAULT_PROJECT_ROOT),
        )
        if folder:
            self.project_root_edit.setText(folder)

    def _browse_output_json(self) -> None:
        file_path, _selected_filter = QFileDialog.getSaveFileName(
            self,
            "Select output JSON",
            self.output_json_edit.text().strip() or str(DEFAULT_OUTPUT_JSON),
            "JSON Files (*.json)",
        )
        if file_path:
            self.output_json_edit.setText(file_path)

    def _configure_trace(self) -> None:
        project_root = self.project_root_edit.text().strip()
        output_json = self.output_json_edit.text().strip()
        entry_script = self.entry_script_edit.text().strip()

        configure_runtime_trace(
            project_root=project_root,
            output_path=output_json,
            entry_script=entry_script,
        )

        self._append_log("Runtime trace configured.")
        self._append_log("Project root: " + project_root)
        self._append_log("Output JSON: " + output_json)
        self._append_log("Entry script: " + entry_script)

    def _save_trace(self) -> None:
        try:
            output_path = save_runtime_trace()
        except Exception as exc:
            QMessageBox.critical(self, "Save failed", str(exc))
            self._append_log("Save failed: " + str(exc))
            return

        if output_path is None:
            QMessageBox.warning(self, "No trace", "Trace writer is not configured.")
            self._append_log("Trace writer is not configured.")
            return

        self._append_log("Trace saved to: " + str(output_path))
        QMessageBox.information(self, "Done", "Trace saved to:\n" + str(output_path))


def main() -> None:
    app = QApplication(sys.argv)
    window = RuntimeCollectorWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

Now, how to instrument the EEG app.

Minimal instrumentation points:

In shell/viewer/eeg_display_launcher.py, near the start of display_pyside6_eeg_visualizer(core):

from runtime_trace_api import trace_event

trace_event(
    event_type="startup",
    source_file="shell/viewer/eeg_display_launcher.py",
    source_symbol="display_pyside6_eeg_visualizer",
    message="Display launcher entered",
)

In shell/viewer/eeg_main_window_builder.py, inside build_and_show() after creating main window:

from runtime_trace_api import trace_event, trace_state_snapshot
from runtime_trace_state import collect_visualizer_state

trace_event(
    event_type="object_created",
    source_file="shell/viewer/eeg_main_window_builder.py",
    source_symbol="EEGMainWindowBuilder.build_and_show",
    object_name="visualizer.main_window",
    object_type="QMainWindow",
    message="Main window created",
)

trace_state_snapshot(
    label="after_main_window_build",
    state=collect_visualizer_state(self.v),
)

In shell/viewer/eeg_signal_manager.py, after connecting EEG loaded signal:

from runtime_trace_api import trace_event

trace_event(
    event_type="signal_connected",
    source_file="shell/viewer/eeg_signal_manager.py",
    source_symbol="SignalManager.init_signals",
    message="Connected eeg_loaded_signal to initialize_mcrvlt_snapshot_map",
)

In shell/viewer/eeg_timeline_manager_core.py, inside handle_timeline_clicked():

from runtime_trace_api import trace_event

trace_event(
    event_type="timeline_click",
    source_file="shell/viewer/eeg_timeline_manager_core.py",
    source_symbol="TimelineManager.handle_timeline_clicked",
    message=f"Clicked time: {clicked_time}",
)

In core/snapshot/eeg_session_snapshot.py, at the start of reset_to_initial_eeg_state():

from runtime_trace_api import trace_event

trace_event(
    event_type="reset",
    source_file="core/snapshot/eeg_session_snapshot.py",
    source_symbol="reset_to_initial_eeg_state",
    message="Reset to initial EEG state started",
)

In modules where exceptions happen often:

from runtime_trace_api import trace_error

try:
    ...
except Exception as exc:
    trace_error(
        source_file="some/file.py",
        source_symbol="SomeClass.some_method",
        message=str(exc),
    )
    raise

How to use the 2 files with AI

Yes, present both files.

File 1:
project_structure_index_v11.json

File 2:
project_runtime_trace_v1.json

Best interpretation rule:
static file = architectural map
runtime file = actual observed behavior

This combination is exactly what you want for V9.

If you want, next I can give you:
a PowerShell command to create the entire runtime collector folder and files,
or a tiny version of V9 that loads both JSON files together.

gimme a script to create folders in folder DEVELOPER TOOLS/FULL_INSPECTOR_JSON_APP/project_reasoner_v9_runtime_collector



Use this PowerShell command:

$root = "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9_runtime_collector"; New-Item -ItemType Directory -Force -Path $root | Out-Null; @("__init__.py","runtime_trace_models.py","runtime_trace_utils.py","runtime_trace_writer.py","runtime_trace_state.py","runtime_trace_decorators.py","runtime_trace_api.py","runner.py") | ForEach-Object { New-Item -ItemType File -Force -Path (Join-Path $root $_) | Out-Null }; Write-Host "Created:" $root

To verify:

Get-ChildItem "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9_runtime_collector"
we have these paths
E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP\project_reasoner_v9
DEVELOPER TOOLS/FULL_INSPECTOR_JSON_APP/project_reasoner_v9_data_collector

DEVELOPER TOOLS/FULL_INSPECTOR_JSON_APP/project_reasoner_v9_runtime_collector

update paths to :

developer_tools/project_reasoner/project_reasoner_v9
developer_tools/project_reasoner/project_reasoner_v9_data_collector
developer_tools/project_reasoner/project_reasoner_v9_runtime_collector

Thought for 6s

Good. Standardize everything to:

developer_tools/project_reasoner/project_reasoner_v9
developer_tools/project_reasoner/project_reasoner_v9_data_collector
developer_tools/project_reasoner/project_reasoner_v9_runtime_collector

Recommended final tree:

E:\eeg_kernel_ai_neural_data_analysis\
    developer_tools\
        project_reasoner\
            project_reasoner_v9\
            project_reasoner_v9_data_collector\
            project_reasoner_v9_runtime_collector\

Use this PowerShell command to create the new folders:

$root = "E:\eeg_kernel_ai_neural_data_analysis\developer_tools\project_reasoner"; New-Item -ItemType Directory -Force -Path $root | Out-Null; @("project_reasoner_v9","project_reasoner_v9_data_collector","project_reasoner_v9_runtime_collector") | ForEach-Object { New-Item -ItemType Directory -Force -Path (Join-Path $root $_) | Out-Null }; Write-Host "Created project_reasoner structure at:" $root

If you also want the empty files created inside the two collector folders, use this:

$root = "E:\eeg_kernel_ai_neural_data_analysis\developer_tools\project_reasoner"; $v9 = Join-Path $root "project_reasoner_v9"; $data = Join-Path $root "project_reasoner_v9_data_collector"; $runtime = Join-Path $root "project_reasoner_v9_runtime_collector"; New-Item -ItemType Directory -Force -Path $v9,$data,$runtime | Out-Null; @("__init__.py","runner.py","collector_main.py","collector_config.py","collector_utils.py","collector_filters.py","collector_walker.py","collector_ast.py","collector_roles.py","collector_qt.py","collector_state.py","collector_ownership.py","collector_chains.py","collector_subsystems.py","collector_duplicates.py","collector_tests.py","collector_output.py") | ForEach-Object { New-Item -ItemType File -Force -Path (Join-Path $data $_) | Out-Null }; @("__init__.py","runtime_trace_models.py","runtime_trace_utils.py","runtime_trace_writer.py","runtime_trace_state.py","runtime_trace_decorators.py","runtime_trace_api.py","runner.py") | ForEach-Object { New-Item -ItemType File -Force -Path (Join-Path $runtime $_) | Out-Null }; Write-Host "Created folders and files under:" $root

Now update your default paths in the scripts.

For project_reasoner_v9_data_collector\runner.py, use:

DEFAULT_PROJECT_ROOT = Path(r"E:\eeg_kernel_ai_neural_data_analysis")
DEFAULT_OUTPUT_JSON = (
    DEFAULT_PROJECT_ROOT
    / "developer_tools"
    / "project_reasoner"
    / "project_reasoner_v9_data_collector"
    / "project_structure_index_v11.json"
)

For project_reasoner_v9_runtime_collector\runner.py, use:

DEFAULT_PROJECT_ROOT = Path(r"E:\eeg_kernel_ai_neural_data_analysis")
DEFAULT_OUTPUT_JSON = (
    DEFAULT_PROJECT_ROOT
    / "developer_tools"
    / "project_reasoner"
    / "project_reasoner_v9_runtime_collector"
    / "project_runtime_trace_v1.json"
)

And for project_reasoner_v9, any runner or helper should point to:

Path(r"E:\eeg_kernel_ai_neural_data_analysis\developer_tools\project_reasoner\project_reasoner_v9")

If you want to move existing files from the old folders to the new ones, use this PowerShell block:

$oldBase = "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP"
$newBase = "E:\eeg_kernel_ai_neural_data_analysis\developer_tools\project_reasoner"
New-Item -ItemType Directory -Force -Path $newBase | Out-Null
Move-Item -Force "$oldBase\project_reasoner_v9" "$newBase\project_reasoner_v9"
Move-Item -Force "$oldBase\project_reasoner_v9_data_collector" "$newBase\project_reasoner_v9_data_collector"
Move-Item -Force "$oldBase\project_reasoner_v9_runtime_collector" "$newBase\project_reasoner_v9_runtime_collector"
Write-Host "Moved folders to:" $newBase

If the folders may not all exist yet, safer version:

$oldBase = "E:\eeg_kernel_ai_neural_data_analysis\DEVELOPER TOOLS\FULL_INSPECTOR_JSON_APP"
$newBase = "E:\eeg_kernel_ai_neural_data_analysis\developer_tools\project_reasoner"
New-Item -ItemType Directory -Force -Path $newBase | Out-Null
@("project_reasoner_v9","project_reasoner_v9_data_collector","project_reasoner_v9_runtime_collector") | ForEach-Object { $src = Join-Path $oldBase $_; $dst = Join-Path $newBase $_; if (Test-Path $src) { Move-Item -Force $src $dst; Write-Host "Moved:" $src "->" $dst } else { Write-Host "Not found:" $src } }

To verify final structure:

Get-ChildItem "E:\eeg_kernel_ai_neural_data_analysis\developer_tools\project_reasoner"

Next important cleanup:
all imports and hardcoded paths in your V9 files should stop referring to:
DEVELOPER TOOLS
FULL_INSPECTOR_JSON_APP
or tools.project_reasoner_v9

and instead use same-folder imports or the new developer_tools/project_reasoner/... base consistently.





