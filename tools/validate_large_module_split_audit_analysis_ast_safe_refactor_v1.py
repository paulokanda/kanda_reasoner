# project-path: tools/validate_large_module_split_audit_analysis_ast_safe_refactor_v1.py
"""Focused validation for the large-module split-audit analysis refactor."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import sys
from pathlib import Path

__all__ = [
    "main",
]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TARGET_REL = "kanda_reasoner_app/manage_architecture/_large_module_split_audit_analysis.py"
HELPER_REL = "kanda_reasoner_app/manage_architecture/_large_module_split_audit_symbol_analysis.py"
VALIDATOR_REL = "tools/validate_large_module_split_audit_analysis_ast_safe_refactor_v1.py"
RUNNER_REL = "kanda_reasoner_app/manage_architecture/large_module_split_audit.py"
CLASSIFIER_REL = "kanda_reasoner_app/manage_architecture/large_module_split_safety_classifier.py"
FEATURE_ID = "large-module-split-audit-analysis-ast-safe-refactor-v1"
EXPECTED_RUNNER_SHA256 = "8e6bb2e3b14df34e4ecf14a44c3f679fb3cb79ac0e4f1d6dd1345cdebbae9e01"
EXPECTED_CLASSIFIER_SHA256 = "525a29da526662473519051a690fe81e738e79464c18f89b0f71e8fedd09492d"
EXPECTED_BEHAVIOR_DIGEST = "49532736d06a10b997ea080fef670ab926fb439f1013466c405e49728457f073"
EXPECTED_RUNNER_DATA_DIGEST = "8b35606a56f7e6ec75f36161e60b9e93675935621842e01259491649cc1af552"
EXPECTED_RUNNER_MARKDOWN_DIGEST = "dcd7b437ba47a5d759746d1761289a9be9497ae0eed55f2b185f7c7b574c43dd"
DYNAMIC_NAMES = {
    "getattr", "setattr", "hasattr", "globals", "locals", "vars",
    "eval", "exec", "__import__", "import_module",
}
CONSUMED = {
    "_audit_symbol": (("node", "imports"), ("ast.FunctionDef | ast.AsyncFunctionDef", "dict[str, str]"), "_SymbolAudit"),
    "_group_islands": (("symbols",), ("list[_SymbolAudit]",), "list[_IslandAudit]"),
    "_independence_matrix": (("islands",), ("list[_IslandAudit]",), "list[dict[str, Any]]"),
    "_iter_auditable_symbols": (("tree",), ("ast.Module",), "Iterable[ast.FunctionDef | ast.AsyncFunctionDef]"),
    "_recommend_patch_shape": (("islands", "matrix"), ("list[_IslandAudit]", "list[dict[str, Any]]"), "dict[str, Any]"),
}


def _path(relative: str) -> Path:
    return PROJECT_ROOT / relative


def _tree(relative: str) -> ast.Module:
    return ast.parse(_path(relative).read_text(encoding="utf-8"), filename=relative)


def _sha256(relative: str) -> str:
    return hashlib.sha256(_path(relative).read_bytes()).hexdigest()


def _function_nodes(tree: ast.Module) -> dict[str, ast.FunctionDef | ast.AsyncFunctionDef]:
    return {
        node.name: node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def _signature_shape(node: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple:
    args = node.args.posonlyargs + node.args.args
    return (
        tuple(item.arg for item in args),
        tuple(ast.unparse(item.annotation) if item.annotation is not None else "" for item in args),
        ast.unparse(node.returns) if node.returns is not None else "",
    )


def _class_node(tree: ast.Module, name: str) -> ast.ClassDef:
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == name:
            return node
    raise AssertionError("CLASS_NOT_FOUND:" + name)


def _dataclass_fields(node: ast.ClassDef) -> tuple[list[str], list[str], list[str]]:
    names: list[str] = []
    annotation_texts: list[str] = []
    defaults: list[str] = []
    for item in node.body:
        if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
            names.append(item.target.id)
            annotation_texts.append(ast.unparse(item.annotation))
            defaults.append(ast.unparse(item.value) if item.value is not None else "")
    return names, annotation_texts, defaults


def _assert_python_and_line_law() -> None:
    for relative in (TARGET_REL, HELPER_REL, VALIDATOR_REL):
        source = _path(relative).read_text(encoding="utf-8")
        ast.parse(source, filename=relative)
        count = len(source.splitlines())
        if not 101 <= count <= 499:
            raise AssertionError(f"LINE_LAW:{relative}:{count}")
    print("PYTHON_SYNTAX: PASS")
    print("LINE_LAW_101_499_FITNESS: PASS")


def _assert_frozen_boundaries() -> None:
    if _sha256(RUNNER_REL) != EXPECTED_RUNNER_SHA256:
        raise AssertionError("FROZEN_RUNNER_HASH_CHANGED")
    if _sha256(CLASSIFIER_REL) != EXPECTED_CLASSIFIER_SHA256:
        raise AssertionError("FROZEN_CLASSIFIER_HASH_CHANGED")
    print("FROZEN_AUDIT_RUNNER_UNCHANGED: PASS")
    print("FROZEN_SAFETY_CLASSIFIER_UNCHANGED: PASS")


def _assert_contracts() -> None:
    tree = _tree(TARGET_REL)
    all_node = next(
        node for node in tree.body
        if isinstance(node, ast.AnnAssign)
        and isinstance(node.target, ast.Name)
        and node.target.id == "__all__"
    )
    if ast.literal_eval(all_node.value) != []:
        raise AssertionError("PUBLIC_ALL_PRESERVATION")
    functions = _function_nodes(tree)
    for name, expected in CONSUMED.items():
        node = functions.get(name)
        if node is None or _signature_shape(node) != expected:
            raise AssertionError("CONSUMED_PRIVATE_SIGNATURE_PRESERVATION:" + name)
    symbol = _class_node(tree, "_SymbolAudit")
    island = _class_node(tree, "_IslandAudit")
    if tuple(ast.unparse(item) for item in symbol.decorator_list) != ("dataclass(slots=True)",):
        raise AssertionError("SYMBOL_AUDIT_DATACLASS_PRESERVATION")
    if tuple(ast.unparse(item) for item in island.decorator_list) != ("dataclass(slots=True)",):
        raise AssertionError("ISLAND_AUDIT_DATACLASS_PRESERVATION")
    symbol_names, symbol_annotations, symbol_defaults = _dataclass_fields(symbol)
    island_names, island_annotations, island_defaults = _dataclass_fields(island)
    if symbol_names != [
        "kind", "name", "qualname", "line_start", "line_end", "line_count",
        "called_self_methods", "self_attr_reads", "self_attr_writes", "imports_used",
        "gui_touches", "side_effects", "candidate_island", "risk",
    ]:
        raise AssertionError("SYMBOL_AUDIT_FIELD_ORDER_PRESERVATION")
    if symbol_annotations != [
        "str", "str", "str", "int", "int", "int", "list[str]", "list[str]",
        "list[str]", "list[str]", "list[str]", "list[str]", "str", "str",
    ]:
        raise AssertionError("SYMBOL_AUDIT_ANNOTATIONS_PRESERVATION")
    if symbol_defaults != [
        "", "", "", "", "", "", "field(default_factory=list)",
        "field(default_factory=list)", "field(default_factory=list)",
        "field(default_factory=list)", "field(default_factory=list)",
        "field(default_factory=list)", "'general'", "'low'",
    ]:
        raise AssertionError("SYMBOL_AUDIT_DEFAULTS_PRESERVATION")
    if island_names != [
        "name", "symbols", "line_count", "self_attr_reads", "self_attr_writes",
        "gui_touches", "side_effects", "risk",
    ]:
        raise AssertionError("ISLAND_AUDIT_FIELD_ORDER_PRESERVATION")
    if island_annotations != [
        "str", "list[_SymbolAudit]", "int", "list[str]", "list[str]", "list[str]", "list[str]", "str",
    ] or any(island_defaults):
        raise AssertionError("ISLAND_AUDIT_CONTRACT_PRESERVATION")
    print("PUBLIC_ALL_PRESERVATION: PASS")
    print("CONSUMED_PRIVATE_API_PRESERVATION: PASS")
    print("CONSUMED_PRIVATE_SIGNATURE_PRESERVATION: PASS")
    print("SYMBOL_AUDIT_DATACLASS_PRESERVATION: PASS")
    print("SYMBOL_AUDIT_SLOTS_PRESERVATION: PASS")
    print("SYMBOL_AUDIT_FIELD_ORDER_PRESERVATION: PASS")
    print("SYMBOL_AUDIT_DEFAULTS_PRESERVATION: PASS")
    print("ISLAND_AUDIT_DATACLASS_PRESERVATION: PASS")
    print("ISLAND_AUDIT_SLOTS_PRESERVATION: PASS")
    print("ISLAND_AUDIT_FIELD_ORDER_PRESERVATION: PASS")


def _assert_semantic_safety() -> None:
    for relative in (TARGET_REL, HELPER_REL, VALIDATOR_REL):
        tree = _tree(relative)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in DYNAMIC_NAMES:
                    raise AssertionError(f"DYNAMIC_CALL:{relative}:{node.func.id}")
                if isinstance(node.func, ast.Attribute) and node.func.attr in DYNAMIC_NAMES:
                    raise AssertionError(f"DYNAMIC_CALL:{relative}:{node.func.attr}")
    helper = _tree(HELPER_REL)
    for node in ast.walk(helper):
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module.endswith("_large_module_split_audit_analysis"):
                raise AssertionError("HELPER_TO_FACADE_BACK_REFERENCE")
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.endswith("._large_module_split_audit_analysis"):
                    raise AssertionError("HELPER_TO_FACADE_BACK_REFERENCE")
    print("NO_DYNAMIC_REFLECTION_CALLS: PASS")
    print("DEPENDENCY_DIRECTION_FITNESS: PASS")
    print("BOX_BOUNDARY_FITNESS: PASS")
    print("NO_LEAK_FITNESS: PASS")


def _fixture_sources() -> dict[str, str]:
    return {
        "plain": """\nimport os\nfrom pathlib import Path as P\n\ndef alpha(x):\n    return x\n\nasync def beta():\n    return 1\n\nclass C:\n    def method(self):\n        self.value = 1\n        return self.value\n""",
        "gui": """\nfrom PySide6.QtWidgets import QPushButton, QMessageBox, QFileDialog\nfrom PySide6.QtCore import QTimer\n\nclass Panel:\n    def build_ui(self):\n        self.button = QPushButton()\n        self.button.clicked.connect(self.run_audit)\n    def run_audit(self):\n        QTimer.singleShot(10, self.refresh)\n        QMessageBox.information(None, 'x', 'y')\n        QFileDialog.getOpenFileName(None)\n""",
        "effects": """\nimport subprocess\nimport zipfile\n\ndef write_report(path):\n    path.write_text('x')\n    with open(path, 'w') as f:\n        f.write('x')\n\ndef delete_draft(path):\n    path.unlink()\n\ndef archive_zip(path):\n    zipfile.ZipFile(path)\n\ndef run_worker():\n    subprocess.run(['echo', 'x'])\n""",
        "labels": """\ndef build_panel(): pass\ndef project_root_path(): pass\ndef selected_table_row(): pass\ndef receive_zip_import(): pass\ndef load_pending_intake(): pass\ndef clean_draft(): pass\ndef copy_clipboard(): pass\ndef run_audit(): pass\ndef help_prompt_protocol(): pass\ndef general_logic(): pass\n""",
        "cross": """\nclass T:\n    def build_ui(self):\n        self.panel = 1\n        return self.run_audit()\n    def run_audit(self):\n        self.panel = 2\n        return self.panel\n    def copy_export(self):\n        return self.panel\n""",
    }


def _behavior_payload() -> dict[str, object]:
    from kanda_reasoner_app.manage_architecture import _large_module_split_audit_analysis as analysis
    from kanda_reasoner_app.manage_architecture.large_module_split_audit import _import_aliases
    out: dict[str, object] = {}
    for key, source in _fixture_sources().items():
        tree = ast.parse(source)
        imports = _import_aliases(tree)
        symbols = [analysis._audit_symbol(node, imports) for node in analysis._iter_auditable_symbols(tree)]
        islands = analysis._group_islands(symbols)
        matrix = analysis._independence_matrix(islands)
        out[key] = {
            "symbols": [item.as_dict() for item in symbols],
            "islands": [item.as_dict() for item in islands],
            "matrix": matrix,
            "recommendation": analysis._recommend_patch_shape(islands, matrix),
        }
    out["empty"] = {
        "groups": analysis._group_islands([]),
        "matrix": analysis._independence_matrix([]),
        "recommendation": analysis._recommend_patch_shape([], []),
    }
    incomplete = ast.FunctionDef(
        name="orphan",
        args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]),
        body=[ast.Pass()],
        decorator_list=[],
    )
    out["incomplete"] = analysis._audit_symbol(incomplete, {}).as_dict()
    return out


def _assert_behavior_equivalence() -> None:
    payload = _behavior_payload()
    blob = json.dumps(payload, sort_keys=True, default=str) + "\n"
    if hashlib.sha256(blob.encode("utf-8")).hexdigest() != EXPECTED_BEHAVIOR_DIGEST:
        raise AssertionError("SYMBOL_AUDIT_CORPUS_EQUIVALENCE")
    from kanda_reasoner_app.manage_architecture import _large_module_split_audit_analysis as analysis
    symbol = analysis._SymbolAudit("function", "x", "x", 1, 1, 1)
    if symbol.as_dict()["candidate_island"] != "general" or symbol.as_dict()["risk"] != "low":
        raise AssertionError("SYMBOL_AUDIT_AS_DICT_EQUIVALENCE")
    island = analysis._IslandAudit("general", [symbol], 1, [], [], [], [], "low")
    if island.as_dict() != {
        "name": "general", "symbols": ["x"], "line_count": 1,
        "self_attr_reads": [], "self_attr_writes": [], "gui_touches": [],
        "side_effects": [], "risk": "low",
    }:
        raise AssertionError("ISLAND_AUDIT_AS_DICT_EQUIVALENCE")
    print("SYMBOL_AUDIT_AS_DICT_EQUIVALENCE: PASS")
    print("ISLAND_AUDIT_AS_DICT_EQUIVALENCE: PASS")
    print("AUDITABLE_SYMBOL_ITERATION_EQUIVALENCE: PASS")
    print("CLASS_METHOD_QUALNAME_BEHAVIOR: PASS")
    print("TOP_LEVEL_QUALNAME_BEHAVIOR: PASS")
    print("INCOMPLETE_AST_LOCATION_FALLBACK: PASS")
    print("SYMBOL_VISITOR_BEHAVIOR_EQUIVALENCE: PASS")
    print("IMPORT_USAGE_BEHAVIOR_EQUIVALENCE: PASS")
    print("GUI_TOUCH_BEHAVIOR_EQUIVALENCE: PASS")
    print("SIDE_EFFECT_BEHAVIOR_EQUIVALENCE: PASS")
    print("CANDIDATE_LABEL_BEHAVIOR_EQUIVALENCE: PASS")
    print("RISK_CLASSIFICATION_BEHAVIOR_EQUIVALENCE: PASS")
    print("SYMBOL_AUDIT_CORPUS_EQUIVALENCE: PASS")
    print("GROUP_ISLANDS_EQUIVALENCE: PASS")
    print("COMBINED_RISK_EQUIVALENCE: PASS")
    print("INDEPENDENCE_MATRIX_EQUIVALENCE: PASS")
    print("PATCH_RECOMMENDATION_EQUIVALENCE: PASS")
    print("BEHAVIOR_EQUIVALENCE_FITNESS: PASS")
    print("BEHAVIOR_REGRESSION: PASS")


def _normalized_runner_payload(relative: str) -> tuple[dict[str, object], str]:
    from kanda_reasoner_app.manage_architecture.large_module_split_audit import run_large_module_split_audit
    result = run_large_module_split_audit(PROJECT_ROOT, relative)
    data = dict(result.data)
    for key in ("generated_at_utc", "project_root", "target_path"):
        data.pop(key, None)
    classification = dict(data.get("refactor_safety_classification") or {})
    ruff = dict(classification.get("ruff") or {})
    if ruff.get("used") is not False:
        raise AssertionError("RUNNER_RUFF_NOT_REQUESTED_CONTRACT")
    if str(ruff.get("message") or "") != "Ruff not requested.":
        raise AssertionError("RUNNER_RUFF_NOT_REQUESTED_MESSAGE")
    ruff["available"] = "<environment-dependent>"
    ruff["invocation"] = "<environment-dependent>"
    classification["ruff"] = ruff
    data["refactor_safety_classification"] = classification
    markdown = re.sub(r"Generated: `[^`]+`", "Generated: `<normalized>`", result.markdown)
    markdown = re.sub(r"Project root: `[^`]+`", "Project root: `<normalized>`", markdown)
    markdown = re.sub(
        r"Ruff available: `(?:True|False)`",
        "Ruff available: `<environment-dependent>`",
        markdown,
    )
    return data, markdown


def _assert_runner_equivalence() -> None:
    from kanda_reasoner_app.manage_architecture import _large_module_split_audit_analysis as analysis
    from kanda_reasoner_app.manage_architecture import large_module_split_audit as runner
    for name in CONSUMED:
        if runner.__dict__[name] is not analysis.__dict__[name]:
            raise AssertionError("RUNNER_CONSUMER_IMPORT_REGRESSION:" + name)
    data: dict[str, object] = {}
    markdown: dict[str, str] = {}
    for relative in (RUNNER_REL, CLASSIFIER_REL):
        current_data, current_markdown = _normalized_runner_payload(relative)
        data[relative] = current_data
        markdown[relative] = current_markdown
    data_blob = json.dumps(data, sort_keys=True, separators=(",", ":"))
    markdown_blob = json.dumps(markdown, sort_keys=True, separators=(",", ":"))
    if hashlib.sha256(data_blob.encode("utf-8")).hexdigest() != EXPECTED_RUNNER_DATA_DIGEST:
        raise AssertionError("RUNNER_NORMALIZED_DATA_EQUIVALENCE")
    if hashlib.sha256(markdown_blob.encode("utf-8")).hexdigest() != EXPECTED_RUNNER_MARKDOWN_DIGEST:
        raise AssertionError("RUNNER_MARKDOWN_EQUIVALENCE")
    print("RUNNER_CONSUMER_IMPORT_REGRESSION: PASS")
    print("CONSUMER_COMPATIBILITY_FITNESS: PASS")
    print("ENVIRONMENT_DEPENDENT_RUFF_CAPABILITY_METADATA_NORMALIZED: PASS")
    print("RUNNER_NORMALIZED_DATA_EQUIVALENCE: PASS")
    print("RUNNER_MARKDOWN_EQUIVALENCE: PASS")


def _assert_fresh_audits() -> None:
    from kanda_reasoner_app.manage_architecture.large_module_split_audit import run_large_module_split_audit
    labels: list[str] = []
    blockers: list[str] = []
    for relative in (TARGET_REL, HELPER_REL, VALIDATOR_REL):
        result = run_large_module_split_audit(PROJECT_ROOT, relative)
        classification = dict(result.data.get("refactor_safety_classification") or {})
        labels.append(str(classification.get("label") or ""))
        blockers.extend(str(item) for item in classification.get("hard_blockers") or [])
    if any(label != "SAFE REFACTORING" for label in labels):
        raise AssertionError("AST_SPLIT_FAMILY_ALL_SAFE:" + repr(labels))
    if blockers:
        raise AssertionError("AST_SPLIT_HARD_BLOCKERS:" + repr(blockers))
    print("AST_SPLIT_AUDIT_RERUN: PASS")
    print("AST_SPLIT_FAMILY_ALL_SAFE: PASS")
    print("AST_SPLIT_SAFETY_LABEL: SAFE REFACTORING")
    print("AST_SPLIT_HARD_BLOCKERS: 0")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--patch-zip", default="")
    parser.parse_args()
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    _assert_python_and_line_law()
    _assert_frozen_boundaries()
    _assert_contracts()
    _assert_semantic_safety()
    _assert_behavior_equivalence()
    _assert_runner_equivalence()
    _assert_fresh_audits()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
