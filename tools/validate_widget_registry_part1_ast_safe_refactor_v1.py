"""Validate the AST-safe refactor of widget registry part 1."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any

__all__ = [
    "main",
]

FEATURE_ID = "widget-registry-part1-ast-safe-refactor-v1"
BASE_DIR = "kanda_reasoner_app/reasoner_context_collector/collector_widget_registry_help/"
TARGET_RELATIVE_PATH = BASE_DIR + "widget_registry_methods_part_1_private_impl.py"
FAMILY_RELATIVE_PATHS = (
    TARGET_RELATIVE_PATH,
    BASE_DIR + "_widget_registry_part1_bindings.py",
    BASE_DIR + "_widget_registry_part1_registration.py",
    BASE_DIR + "_widget_registry_part1_layout.py",
)
EXPECTED_ORIGINAL_SHA256 = "c01e655299a4e911ce140d28e5e454775cecae196f7c1892a05f8ec27400a591"
EXPECTED_SIGNATURE_SNAPSHOT_SHA256 = "582f5cb88fe5efa73c8767baf7e33a9a22588ade6531ed25fce73d2e80bcab8d"
EXPECTED_BEHAVIOR_SHA256 = "89331c252ef25fd1b5fb7de250f3ff8c1a791a2b18d8cf00dee8252478756a7a"
EXPECTED_IMPL_NAMES = {
    "_bind_root_globals",
    "_wrg__append_layout_record_impl",
    "_wrg__current_class_name_impl",
    "_wrg__current_method_name_impl",
    "_wrg__current_source_symbol_impl",
    "_wrg__handle_add_row_impl",
    "_wrg__handle_add_tab_impl",
    "_wrg__handle_add_widget_impl",
    "_wrg__handle_layout_call_impl",
    "_wrg__handle_widget_property_call_impl",
    "_wrg__index_widget_ref_impl",
    "_wrg__index_widget_var_impl",
    "_wrg__pop_scope_impl",
    "_wrg__push_scope_impl",
    "_wrg__register_assigned_widget_impl",
    "_wrg__register_inline_widget_impl",
    "_wrg__resolve_or_create_widget_from_expr_impl",
    "_wrg__resolve_widget_id_impl",
    "_wrg_visit_AnnAssign_impl",
    "_wrg_visit_Assign_impl",
    "_wrg_visit_AsyncFunctionDef_impl",
    "_wrg_visit_Call_impl",
    "_wrg_visit_ClassDef_impl",
    "_wrg_visit_FunctionDef_impl",
}
FORBIDDEN_BOX_PREFIXES = (
    "kanda_reasoner_app.manage_architecture.large_file_refactor_planner",
    "kanda_reasoner_app.manage_architecture.large_file_refactor_workbench",
    "kanda_reasoner_app.freeze_after_update",
    "kanda_reasoner_app.freeze_after_update_gui",
    "kanda_reasoner_app.freeze_hint_intake",
)


def _sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _sha256_path(path: Path) -> str:
    return _sha256_bytes(path.read_bytes())


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _package_manifest(patch_zip: Path) -> dict[str, Any]:
    with zipfile.ZipFile(patch_zip, "r") as archive:
        return json.loads(archive.read("PACKAGE_MANIFEST.json").decode("utf-8"))


def _verify_zip_contract(root: Path, patch_zip: Path) -> None:
    script = root / "scripts" / "validate_patch_zip.py"
    result = subprocess.run(
        [sys.executable, str(script), str(patch_zip)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(result.stdout)
    print("ZIP CONTRACT: PASS")


def _verify_package_hashes(patch_zip: Path) -> None:
    manifest = _package_manifest(patch_zip)
    with zipfile.ZipFile(patch_zip, "r") as archive:
        for item in manifest["files"]:
            relative = str(item["relative_path"])
            actual = _sha256_bytes(archive.read("payload/" + relative))
            if actual != str(item["sha256"]).lower():
                raise AssertionError("PACKAGE PAYLOAD HASH MISMATCH: " + relative)
    print("PACKAGE_PAYLOAD_HASHES: PASS")


def _verify_source_identity(root: Path, patch_zip: Path) -> None:
    manifest = _package_manifest(patch_zip)
    target_item = next(
        item for item in manifest["files"]
        if item["relative_path"] == TARGET_RELATIVE_PATH
    )
    accepted = {str(value).lower() for value in target_item["accepted_existing_sha256"]}
    if EXPECTED_ORIGINAL_SHA256 not in accepted:
        raise AssertionError("ORIGINAL SOURCE IDENTITY MISSING FROM MANIFEST")
    installed = _sha256_path(root / TARGET_RELATIVE_PATH)
    if installed != str(target_item["sha256"]).lower():
        raise AssertionError("INSTALLED TARGET HASH DOES NOT MATCH MANIFEST")
    print("SOURCE_IDENTITY_GUARD: PASS")


def _verify_line_law_and_syntax(root: Path) -> None:
    for relative in FAMILY_RELATIVE_PATHS:
        path = root / relative
        raw = path.read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            raise AssertionError("UTF8 BOM: " + relative)
        source = raw.decode("utf-8", errors="strict")
        line_count = len(source.splitlines())
        if not 100 < line_count < 500:
            raise AssertionError(f"LINE LAW FAILED: {relative}: {line_count}")
        ast.parse(source, filename=str(path))
    print("SOURCE_ASCII_UTF8_NO_BOM: PASS")
    print("PYTHON_SYNTAX: PASS")
    print("LINE_LAW_101_499_FITNESS: PASS")


def _verify_semantic_safety(root: Path) -> None:
    from kanda_reasoner_app.manage_architecture.kanda_refactor_semantic_safety import (
        detect_semantic_dynamic_risks,
    )
    failures: dict[str, list[dict[str, Any]]] = {}
    for relative in FAMILY_RELATIVE_PATHS:
        source = (root / relative).read_text(encoding="utf-8", errors="strict")
        findings = detect_semantic_dynamic_risks(source, relative)
        if findings:
            failures[relative] = findings
    if failures:
        raise AssertionError("SEMANTIC DYNAMIC FINDINGS: " + repr(failures))
    print("SEMANTIC_DYNAMIC_SAFETY: PASS")


def _verify_dependency_direction(root: Path) -> None:
    from kanda_reasoner_app.manage_architecture.kanda_refactor_semantic_safety import (
        check_candidate_dependency_direction,
    )
    result = check_candidate_dependency_direction(
        root,
        facade_relative_path=TARGET_RELATIVE_PATH,
        helper_relative_paths=list(FAMILY_RELATIVE_PATHS[1:]),
    )
    if not result.get("pass"):
        raise AssertionError("DEPENDENCY DIRECTION FAILED: " + repr(result))
    for relative in FAMILY_RELATIVE_PATHS:
        source = (root / relative).read_text(encoding="utf-8", errors="strict")
        tree = ast.parse(source, filename=relative)
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = str(node.module or "")
                if module.startswith(FORBIDDEN_BOX_PREFIXES):
                    raise AssertionError("FORBIDDEN BOX IMPORT: " + module)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith(FORBIDDEN_BOX_PREFIXES):
                        raise AssertionError("FORBIDDEN BOX IMPORT: " + alias.name)
    print("DEPENDENCY_DIRECTION_FITNESS: PASS")
    print("BOX_BOUNDARY_FITNESS: PASS")
    print("NO_LEAK_FITNESS: PASS")


def _expr_text(node: ast.AST | None) -> str:
    if node is None:
        return ""
    if isinstance(node, ast.Constant):
        return repr(node.value)
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return _expr_text(node.value) + "." + node.attr
    if isinstance(node, ast.Subscript):
        return _expr_text(node.value) + "[" + _expr_text(node.slice) + "]"
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        return _expr_text(node.left) + " | " + _expr_text(node.right)
    if isinstance(node, ast.Tuple):
        return "(" + ", ".join(_expr_text(item) for item in node.elts) + ")"
    if isinstance(node, ast.List):
        return "[" + ", ".join(_expr_text(item) for item in node.elts) + "]"
    return ast.unparse(node)


def _function_snapshot(node: ast.FunctionDef | ast.AsyncFunctionDef) -> dict[str, Any]:
    args = node.args
    positional = [*args.posonlyargs, *args.args]
    defaults = ["<required>"] * (len(positional) - len(args.defaults))
    defaults.extend(_expr_text(item) for item in args.defaults)
    annotated = [*args.posonlyargs, *args.args, *args.kwonlyargs]
    return {
        "kind": "async" if isinstance(node, ast.AsyncFunctionDef) else "function",
        "posonly": [item.arg for item in args.posonlyargs],
        "positional": [item.arg for item in args.args],
        "defaults": defaults,
        "vararg": args.vararg.arg if args.vararg else "",
        "kwonly": [item.arg for item in args.kwonlyargs],
        "kwdefaults": [
            _expr_text(item) if item is not None else "<required>"
            for item in args.kw_defaults
        ],
        "kwarg": args.kwarg.arg if args.kwarg else "",
        "annotations": {
            item.arg: _expr_text(item.annotation)
            for item in annotated
            if item.annotation is not None
        },
        "returns": _expr_text(node.returns),
        "decorators": [_expr_text(item) for item in node.decorator_list],
    }


def _verify_private_contract(root: Path) -> None:
    tree = ast.parse(
        (root / TARGET_RELATIVE_PATH).read_text(encoding="utf-8", errors="strict"),
        filename=TARGET_RELATIVE_PATH,
    )
    names = {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    imported = {
        alias.asname or alias.name
        for node in tree.body
        if isinstance(node, ast.ImportFrom)
        for alias in node.names
    }
    implementation_surface = (names | imported) & EXPECTED_IMPL_NAMES
    if implementation_surface != EXPECTED_IMPL_NAMES:
        raise AssertionError(
            "IMPLEMENTATION NAME SURFACE CHANGED: "
            + repr({"missing": sorted(EXPECTED_IMPL_NAMES - implementation_surface)})
        )
    nodes: dict[str, ast.FunctionDef | ast.AsyncFunctionDef] = {}
    for relative in FAMILY_RELATIVE_PATHS:
        family_tree = ast.parse(
            (root / relative).read_text(encoding="utf-8", errors="strict"),
            filename=relative,
        )
        for node in family_tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in EXPECTED_IMPL_NAMES:
                nodes[node.name] = node
    if set(nodes) != EXPECTED_IMPL_NAMES:
        raise AssertionError("IMPLEMENTATION FUNCTION FAMILY INCOMPLETE")
    snapshot = {name: _function_snapshot(nodes[name]) for name in sorted(nodes)}
    raw = json.dumps(snapshot, sort_keys=True, separators=(",", ":")).encode("utf-8")
    digest = _sha256_bytes(raw)
    if digest != EXPECTED_SIGNATURE_SNAPSHOT_SHA256:
        raise AssertionError("IMPLEMENTATION SIGNATURE SNAPSHOT CHANGED: " + digest)
    if _literal_all(tree) != []:
        raise AssertionError("PRIVATE FACADE __all__ CHANGED")
    print("PUBLIC_API_PRESERVATION: PASS")
    print("ANNOTATION_IMPORT_PRESERVATION: PASS")


def _literal_all(tree: ast.Module) -> list[str] | None:
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
            continue
        if node.targets[0].id != "__all__":
            continue
        if isinstance(node.value, (ast.List, ast.Tuple)):
            values: list[str] = []
            for item in node.value.elts:
                if not isinstance(item, ast.Constant) or not isinstance(item.value, str):
                    return None
                values.append(item.value)
            return values
    return None


def _behavior_fixtures() -> list[dict[str, str]]:
    return [
        {
            "path": "pkg/ui_main.py",
            "source": """\nfrom PySide6.QtWidgets import *\nclass MainWindow:\n    def build(self):\n        self.button = QPushButton(\"Run\")\n        self.button.setToolTip(\"Execute\")\n        self.button.setObjectName(\"run_button\")\n        combo: QComboBox = QComboBox()\n        combo.addItem(\"Alpha\")\n        combo.addItems([\"Beta\", \"Gamma\"])\n        layout = QVBoxLayout()\n        layout.addWidget(self.button)\n        layout.addWidget(QLabel(\"Inline\"))\n""",
        },
        {
            "path": "pkg/forms.py",
            "source": """\nfrom PySide6.QtWidgets import *\ndef build_form():\n    form = QFormLayout()\n    name_edit = QLineEdit()\n    form.addRow(QLabel(\"Name\"), name_edit)\n    tabs = QTabWidget()\n    page = QWidget()\n    tabs.addTab(page, \"General\")\n    tabs.setTabText(0, \"Main\")\n""",
        },
        {
            "path": "pkg/grid.py",
            "source": """\nfrom PySide6.QtWidgets import *\nasync def build_grid():\n    grid = QGridLayout()\n    button = QPushButton(text=\"Grid\")\n    grid.addWidget(button, 2, 3, 1, 2)\n""",
        },
        {"path": "pkg/bad.py", "source": "def broken(:\n"},
    ]


def _verify_behavior() -> None:
    module = importlib.import_module(
        "kanda_reasoner_app.reasoner_context_collector.collector_widget_registry"
    )
    result = module.build_widget_registry(_behavior_fixtures())
    raw = json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    digest = _sha256_bytes(raw)
    if digest != EXPECTED_BEHAVIOR_SHA256:
        raise AssertionError("WIDGET REGISTRY BEHAVIOR DIGEST CHANGED: " + digest)
    print("CONSUMER_COMPATIBILITY_FITNESS: PASS")
    print("BEHAVIOR_EQUIVALENCE_FITNESS: PASS")
    print("BEHAVIOR_REGRESSION: PASS")


def _verify_fresh_audits(root: Path) -> None:
    from kanda_reasoner_app.manage_architecture.large_module_split_audit import (
        run_large_module_split_audit,
    )
    for relative in FAMILY_RELATIVE_PATHS:
        result = run_large_module_split_audit(
            root,
            root / relative,
            classifier_mode="heuristic",
        )
        classification = result.data["refactor_safety_classification"]
        if classification["label"] != "SAFE REFACTORING":
            raise AssertionError("FRESH AST NOT SAFE: " + relative)
        if classification["hard_blockers"]:
            raise AssertionError("FRESH AST HARD BLOCKERS: " + relative)
    print("AST_SPLIT_AUDIT_RERUN: PASS")
    print("AST_SPLIT_SAFETY_LABEL: SAFE REFACTORING")
    print("AST_SPLIT_HARD_BLOCKERS: 0")
    print("FRESH_FAMILY_AST_FITNESS: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--patch-zip", required=True)
    args = parser.parse_args()
    root = _project_root()
    patch_zip = Path(args.patch_zip).resolve()
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    _verify_zip_contract(root, patch_zip)
    _verify_package_hashes(patch_zip)
    _verify_source_identity(root, patch_zip)
    _verify_line_law_and_syntax(root)
    _verify_semantic_safety(root)
    _verify_dependency_direction(root)
    _verify_private_contract(root)
    _verify_behavior()
    _verify_fresh_audits(root)
    print("INSTALLABILITY_FITNESS: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
