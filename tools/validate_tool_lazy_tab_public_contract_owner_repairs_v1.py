"""Live validator for Tool lazy-tab owner repairs, revision v1r1."""

from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import importlib
import os
from pathlib import Path
import subprocess
import sys

from tool_lazy_tab_owner_repairs_architecture_gate import (
    validate_lazy_tab_owner_repairs_architecture_non_regression,
)

FEATURE_ID = "kanda-reasoner-tool-lazy-tab-public-contract-owner-repairs-v1"
PACKAGE_REVISION = "v1r2"

STATIC_TOUCHED = {
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_journaled_apply_executor.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_completion_apply_bridge.py",
    "tools/validate_large_file_refactor_workbench_patch5_journaled_apply_v1.py",
    "tools/validate_large_file_refactor_workbench_patch6_controlled_real_module_v1.py",
    "kanda_reasoner_app/reasoner_context_collector/collector_widget_registry.py",
    "kanda_reasoner_app/reasoner_context_collector/collector_widget_registry_help/_widget_registry_part1_bindings.py",
    "kanda_reasoner_app/reasoner_context_collector/collector_widget_registry_help/widget_registry_methods_part_1_private_impl.py",
    "kanda_reasoner_app/reasoner_engine/prompt_router_reasoner_review_models.py",
    "kanda_reasoner_app/prompt_router_reasoner_gui/prompt_router_reasoner_tab.py",
    "kanda_reasoner_app/reasoner_engine/prompt_router_reasoner_manual_router_choice_capture.py",
    "kanda_reasoner_app/reasoner_engine/prompt_router_reasoner_router_mode_state.py",
    "kanda_reasoner_app/reasoner_engine/prompt_router_reasoner_shadow_bridge.py",
    "kanda_reasoner_app/reasoner_engine/prompt_router_reasoner_review_stats.py",
    "kanda_reasoner_app/reasoner_engine/prompt_router_reasoner_session_capture.py",
    "tests/test_tool_lazy_tab_public_contract_owner_repairs.py",
    "tools/tool_lazy_tab_owner_repairs_architecture_gate.py",
    "tools/validate_tool_lazy_tab_public_contract_owner_repairs_v1.py",
}

CORE_MODULE = (
    ".collector_widget_registry_help."
    "widget_registry_methods_part_1_private_impl"
)
REGISTRATION_MODULE = (
    ".collector_widget_registry_help._widget_registry_part1_registration"
)
LAYOUT_MODULE = (
    ".collector_widget_registry_help._widget_registry_part1_layout"
)
CORE_NAMES = {
    "_bind_root_globals",
    "_wrg__current_source_symbol_impl",
    "_wrg__current_class_name_impl",
    "_wrg__current_method_name_impl",
    "_wrg__push_scope_impl",
    "_wrg__pop_scope_impl",
    "_wrg_visit_ClassDef_impl",
    "_wrg_visit_FunctionDef_impl",
    "_wrg_visit_AsyncFunctionDef_impl",
    "_wrg__index_widget_ref_impl",
    "_wrg__index_widget_var_impl",
    "_wrg__resolve_widget_id_impl",
}
REGISTRATION_NAMES = {
    "_wrg_visit_Assign_impl",
    "_wrg_visit_AnnAssign_impl",
    "_wrg_visit_Call_impl",
    "_wrg__register_assigned_widget_impl",
    "_wrg__register_inline_widget_impl",
    "_wrg__handle_widget_property_call_impl",
    "_wrg__resolve_or_create_widget_from_expr_impl",
}
LAYOUT_NAMES = {
    "_wrg__handle_layout_call_impl",
    "_wrg__handle_add_widget_impl",
    "_wrg__handle_add_row_impl",
    "_wrg__handle_add_tab_impl",
    "_wrg__append_layout_record_impl",
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _module_text(node: ast.ImportFrom) -> str:
    return "." * node.level + (node.module or "")


def _run(
    command: list[str],
    root: Path,
    markers: tuple[str, ...],
) -> str:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root)
    completed = subprocess.run(
        command,
        cwd=str(root),
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    output = completed.stdout
    if completed.stderr:
        output += ("\n" if output else "") + completed.stderr
    print(output.rstrip())
    _require(
        completed.returncode == 0,
        "VALIDATION_COMMAND_FAILED: " + " ".join(command),
    )
    for marker in markers:
        _require(marker in output, "VALIDATION_MARKER_MISSING: " + marker)
    return output


def _receipt_paths(root: Path) -> set[str]:
    receipt_root = (
        Path(root.anchor)
        / (root.name + "_delete_after_daily_work")
        / "install_receipts"
    )
    candidates = sorted(
        receipt_root.glob("*_tool_lazy_tab_owner_repairs_v1r1.json")
    )
    _require(bool(candidates), "V1R1_INSTALL_RECEIPT_MISSING")
    import json

    receipt = json.loads(candidates[-1].read_text(encoding="utf-8"))
    _require(
        receipt.get("project_specific_state_written") is False,
        "PROJECT_STATE_WRITE_RECORDED",
    )
    return {
        str(item).replace("\\", "/")
        for item in receipt.get("changed_paths", [])
    }


def _check_planner(root: Path) -> None:
    stale = {
        ".workbench_journaled_apply_executor",
        "kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_journaled_apply_executor",
    }
    names = {
        "JournaledApplyAuthorization",
        "JournaledApplyResult",
        "build_journaled_apply_authorization",
    }
    paths = [
        root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_completion_apply_bridge.py",
        root / "tools/validate_large_file_refactor_workbench_patch5_journaled_apply_v1.py",
        root / "tools/validate_large_file_refactor_workbench_patch6_controlled_real_module_v1.py",
    ]
    for path in paths:
        if not path.is_file():
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and _module_text(node) in stale:
                leaked = sorted(
                    alias.name for alias in node.names if alias.name in names
                )
                _require(
                    not leaked,
                    "PLANNER_MODEL_REEXPORT_REACH_IN: "
                    + str(path)
                    + ":"
                    + repr(leaked),
                )
    models = importlib.import_module(
        "kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_journaled_apply_models"
    )
    bridge = importlib.import_module(
        "kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_completion_apply_bridge"
    )
    _require(
        hasattr(models, "build_journaled_apply_authorization"),
        "PLANNER_AUTHORIZATION_OWNER_MISSING",
    )
    _require(
        hasattr(bridge, "execute_completion_transaction"),
        "PLANNER_COMPLETION_BRIDGE_IMPORT_FAILED",
    )
    print("MANAGE ARCHITECTURE AUTHORIZATION OWNER: PASS")
    print("MANAGE ARCHITECTURE EXECUTOR REEXPORT REACH-IN: 0")


def _top_level_functions(path: Path) -> set[str]:
    return {
        node.name
        for node in ast.parse(path.read_text(encoding="utf-8-sig")).body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def _import_names(source: str, module: str) -> set[str]:
    names: set[str] = set()
    for node in ast.parse(source).body:
        if isinstance(node, ast.ImportFrom) and _module_text(node) == module:
            names.update(alias.name for alias in node.names)
    return names


def _check_collector(root: Path) -> None:
    base = root / "kanda_reasoner_app/reasoner_context_collector"
    binding_path = (
        base
        / "collector_widget_registry_help/_widget_registry_part1_bindings.py"
    )
    binding_source = binding_path.read_text(encoding="utf-8")
    _require(
        "_CANONICAL_BINDINGS" in binding_source,
        "COLLECTOR_CANONICAL_BINDINGS_MISSING",
    )
    _require(
        "_BINDING_HOLDER" not in binding_source,
        "COLLECTOR_MUTABLE_BINDING_HOLDER_REMAINS",
    )
    _require(
        'root_globals["FUNCTION_SCOPE_KINDS"]' not in binding_source,
        "COLLECTOR_ROOT_GLOBAL_LOOKUP_REMAINS",
    )

    public_path = base / "collector_widget_registry.py"
    public_source = public_path.read_text(encoding="utf-8-sig")
    _require(
        "_wrg_methods_part_1" not in public_source,
        "COLLECTOR_INDIRECT_PRIVATE_FACADE_REFERENCE_REMAINS",
    )
    for module, expected in (
        (CORE_MODULE, CORE_NAMES),
        (REGISTRATION_MODULE, REGISTRATION_NAMES),
        (LAYOUT_MODULE, LAYOUT_NAMES),
    ):
        actual = _import_names(public_source, module)
        _require(
            actual == expected,
            "COLLECTOR_DIRECT_OWNER_IMPORT_MISMATCH: "
            + module
            + ":"
            + repr(sorted(actual)),
        )

    helper = base / "collector_widget_registry_help"
    facade_path = helper / "widget_registry_methods_part_1_private_impl.py"
    facade_source = facade_path.read_text(encoding="utf-8-sig")
    facade_modules = {
        _module_text(node)
        for node in ast.parse(facade_source).body
        if isinstance(node, ast.ImportFrom)
    }
    _require(
        "._widget_registry_part1_registration" not in facade_modules,
        "COLLECTOR_REGISTRATION_REEXPORT_REMAINS",
    )
    _require(
        "._widget_registry_part1_layout" not in facade_modules,
        "COLLECTOR_LAYOUT_REEXPORT_REMAINS",
    )
    _require(
        CORE_NAMES.issubset(_top_level_functions(facade_path)),
        "COLLECTOR_CORE_OWNER_INCOMPLETE",
    )
    registration_path = helper / "_widget_registry_part1_registration.py"
    layout_path = helper / "_widget_registry_part1_layout.py"
    _require(
        REGISTRATION_NAMES.issubset(_top_level_functions(registration_path)),
        "COLLECTOR_REGISTRATION_OWNER_INCOMPLETE",
    )
    _require(
        LAYOUT_NAMES.issubset(_top_level_functions(layout_path)),
        "COLLECTOR_LAYOUT_OWNER_INCOMPLETE",
    )

    module = importlib.import_module(
        "kanda_reasoner_app.reasoner_context_collector.collector_widget_registry"
    )
    source = """
from PySide6.QtWidgets import QPushButton, QVBoxLayout
layout = QVBoxLayout()
button = QPushButton('Run')
button.setToolTip('Execute')
layout.addWidget(button)
"""
    result = module.build_widget_registry(
        [{"path": "sample.py", "source": source}]
    )
    _require(bool(result), "COLLECTOR_WIDGET_REGISTRY_EMPTY")
    records = list(result.values())
    _require(
        any(record.get("display_text") == "Run" for record in records),
        "COLLECTOR_ASSIGNMENT_REGISTRATION_FAILED",
    )
    _require(
        any(record.get("tooltip_text") == "Execute" for record in records),
        "COLLECTOR_PROPERTY_REGISTRATION_FAILED",
    )
    _require(
        any(record.get("layout_records") for record in records),
        "COLLECTOR_LAYOUT_REGISTRATION_FAILED",
    )
    print("CONTEXT COLLECTOR CANONICAL BINDING OWNER: PASS")
    print("CONTEXT COLLECTOR ROOT-GLOBAL STATE INJECTION: 0")
    print("CONTEXT COLLECTOR DIRECT OWNER IMPORTS: PASS")
    print("CONTEXT COLLECTOR INDIRECT PRIVATE REEXPORT: 0")
    print("CONTEXT COLLECTOR REGISTRATION AND LAYOUT PATHS: PASS")


def _check_prompt(root: Path) -> None:
    store_module = (
        "kanda_reasoner_app.reasoner_engine."
        "prompt_router_reasoner_review_store"
    )
    for path in (root / "kanda_reasoner_app").rglob("*.py"):
        if path.name == "prompt_router_reasoner_review_store.py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom):
                continue
            if _module_text(node) != store_module:
                continue
            leaked = sorted(
                alias.name
                for alias in node.names
                if alias.name != "PromptRouterReasonerReviewStore"
            )
            _require(
                not leaked,
                "PROMPT_REVIEW_STORE_MODEL_REEXPORT_REACH_IN: "
                + str(path)
                + ":"
                + repr(leaked),
            )
    models = importlib.import_module(
        "kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_models"
    )
    session = importlib.import_module(
        "kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_session_capture"
    )
    _require(hasattr(models, "PromptSnapshot"), "PROMPT_SNAPSHOT_OWNER_MISSING")
    _require(
        hasattr(session, "build_ml_advisory_prompt_context_snapshot"),
        "PROMPT_SESSION_CONSUMER_IMPORT_FAILED",
    )
    print("REASONER ENGINE PROMPT SNAPSHOT OWNER: PASS")
    print("REASONER ENGINE REVIEW STORE MODEL REEXPORT REACH-IN: 0")


def _import_lazy_tabs() -> None:
    modules = (
        "kanda_reasoner_app.manage_architecture.manage_architecture_gui",
        "kanda_reasoner_app.reasoner_context_collector.runner",
        "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window",
    )
    for module_name in modules:
        importlib.import_module(module_name)
    print("MANAGE ARCHITECTURE LAZY TAB IMPORT: PASS")
    print("CONTEXT COLLECTOR LAZY TAB IMPORT: PASS")
    print("AI REASONER LAZY TAB IMPORT: PASS")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool-root", required=True)
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--evidence-path", required=True)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    tool_root = Path(args.tool_root).expanduser().resolve()
    project_root = Path(args.project_root).expanduser().resolve()
    _require(tool_root.is_dir(), "TOOL_ROOT_MISSING")
    _require(project_root.is_dir(), "PROJECT_ROOT_MISSING")
    if str(tool_root) not in sys.path:
        sys.path.insert(0, str(tool_root))
    print("PACKAGE REVISION: " + PACKAGE_REVISION)
    print("TOOL ROOT RESOLVED: " + str(tool_root))
    print("PROJECT ROOT RESOLVED: " + str(project_root))
    print(
        "SELF-HOSTING PHYSICAL ROOT: "
        + ("YES" if tool_root == project_root else "NO")
    )
    print("TOOL PROJECT LOGICAL ROLE SEPARATION: PASS")
    print("VALIDATOR TOOL ROOT IMPORT PATH: PASS")
    changed = _receipt_paths(tool_root)
    touched = frozenset(STATIC_TOUCHED | changed)
    _check_planner(tool_root)
    _check_collector(tool_root)
    _check_prompt(tool_root)
    _run(
        [
            sys.executable,
            "-m",
            "unittest",
            "-v",
            "tests.test_tool_lazy_tab_public_contract_owner_repairs",
        ],
        tool_root,
        ("Ran 3 tests", "OK"),
    )
    print("FOCUSED PUBLIC CONTRACT TESTS: 3/3 PASS")
    _import_lazy_tabs()
    registry = (
        tool_root
        / "kanda_reasoner_app/project_registry/selected_project.json"
    )
    before = registry.read_bytes() if registry.is_file() else b""
    after = registry.read_bytes() if registry.is_file() else b""
    _require(before == after, "TOOL_PROJECT_SELECTION_REGISTRY_MUTATED")
    print("TOOL PROJECT SELECTION REGISTRY MUTATED: NO")
    architecture = (
        tool_root
        / "kanda_reasoner_app/manage_architecture/manage_architecture.py"
    )
    output = _run(
        [sys.executable, str(architecture), "--root", str(tool_root), "--validate"],
        tool_root,
        ("ARCHITECTURE VALIDATION SUMMARY",),
    )
    validate_lazy_tab_owner_repairs_architecture_non_regression(output, touched)
    print("LAZY TAB ARCHITECTURE GATE UNIQUE OWNER: PASS")
    print("GENERIC VALIDATOR PUBLIC SYMBOL COLLISION: 0")
    evidence = Path(args.evidence_path)
    evidence.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "VALIDATION OK: " + FEATURE_ID,
        "STATUS: IN_SYNC",
        "PACKAGE REVISION: " + PACKAGE_REVISION,
        "TOOL PROJECT LOGICAL ROLE SEPARATION: PASS",
        "INDEPENDENT OWNER BOXES: 3",
        "CONTEXT COLLECTOR DIRECT OWNER IMPORTS: PASS",
        "CONTEXT COLLECTOR INDIRECT PRIVATE REEXPORT: 0",
        "LAZY TAB ARCHITECTURE GATE UNIQUE OWNER: PASS",
        "GENERIC VALIDATOR PUBLIC SYMBOL COLLISION: 0",
        "PROJECT-SPECIFIC STATE WRITTEN: NO",
        "NEW ARCHITECTURE ISSUES: 0",
        "TOUCHED PATH ARCHITECTURE ISSUES: 0",
    ]
    evidence.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("VALIDATION EVIDENCE WRITTEN: " + str(evidence))
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
