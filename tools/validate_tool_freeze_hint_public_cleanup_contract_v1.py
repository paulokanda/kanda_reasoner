"""Validate the complete Freeze Hint Intake public cleanup boundary."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

FEATURE_ID = "kanda-reasoner-tool-freeze-hint-public-cleanup-contract-v1"
PACKAGE_REVISION = "v1r2"
PRIVATE_CLEANUP = "_clean_stale_pending_text_after_local_validation"
PUBLIC_CLEANUP = "clean_stale_pending_text_after_local_validation"
PRIVATE_MODULE = "kanda_reasoner_app.freeze_hint_intake.form_normalization"
INTAKE_PREFIX = "kanda_reasoner_app/freeze_hint_intake/"
CANONICAL_HELPERS = frozenset(
    {
        "_append_missing_lines",
        "_append_text",
        "_clean_stale_pending_text_after_local_validation",
        "_field_to_text",
        "_has_local_validation_completion_marker",
        "_has_recognizable_validation_marker",
        "_has_safe_validation_evidence_marker",
        "_has_stale_local_validation_pending_text",
        "_hint_to_form_inputs",
        "_normalize_form_inputs",
        "_normalize_line",
        "_normalize_validation_evidence_summary",
        "_strip_stale_pending_validation_sentences",
        "_strip_stale_pending_validation_text",
    }
)
PAYLOAD_PATHS = {
    "kanda_reasoner_app/freeze_hint_intake/local_validation_cleanup.py",
    "tests/test_tool_freeze_hint_public_cleanup_contract.py",
    "tools/validate_tool_freeze_hint_public_cleanup_contract_v1.py",
}
PREEXISTING = {
    ("DEAD_CODE_UNREACHABLE_FILE", "kanda_prompt_workspace/prompt_tools/startup_kernel/constants.py"),
    ("DEAD_CODE_UNREACHABLE_FILE", "kanda_prompt_workspace/prompt_tools/startup_kernel/generic_helpers.py"),
    ("DEAD_CODE_UNREACHABLE_FILE", "kanda_prompt_workspace/prompt_tools/startup_kernel/source_resolution.py"),
    ("DEAD_CODE_UNREACHABLE_FILE", "kanda_reasoner_app/daily_rfctr_report/daily_refactor_report.py"),
    ("DEAD_CODE_UNREACHABLE_FILE", "kanda_reasoner_app/reasoner_context_collector/collector_runtime_scenarios_help/normalization.py"),
    ("DEAD_CODE_UNREACHABLE_FILE", "kanda_reasoner_app/reasoner_context_collector/collector_widget_registry_help/_widget_registry_part1_layout.py"),
    ("DEAD_CODE_UNREACHABLE_FILE", "kanda_reasoner_app/reasoner_context_collector/collector_widget_registry_help/_widget_registry_part1_registration.py"),
    ("DEAD_CODE_UNREACHABLE_FILE", "kanda_reasoner_app/reasoner_context_collector/collector_widget_registry_help/widget_registry_methods_part_1_private_impl.py"),
    ("DEAD_CODE_UNREACHABLE_FILE", "kanda_reasoner_app/reasoner_context_collector/collector_widget_ui_action_bridge_help/indexing.py"),
    ("DEAD_CODE_UNREACHABLE_FILE", "kanda_reasoner_app/reasoner_context_collector/collector_widget_ui_action_bridge_help/matching.py"),
    ("DEAD_CODE_UNREACHABLE_FILE", "kanda_reasoner_app/reasoner_runtime_collector/hooks/qt_connection_monitor.py"),
    ("DEAD_CODE_UNREACHABLE_FILE", "kanda_reasoner_app/reasoner_runtime_collector/runtime_trace_decorators.py"),
    ("DEAD_CODE_UNREACHABLE_FILE", "kanda_reasoner_app/reasoner_runtime_collector/runtime_trace_state.py"),
    ("DEAD_CODE_UNREACHABLE_FILE", "kanda_reasoner_app/routing_signal_scorer/prompt_intake_boundary/prompt_artifact_contract.py"),
    ("DEAD_CODE_UNREACHABLE_FILE", "kanda_reasoner_app/routing_signal_scorer/prompt_intake_boundary/prompt_output_firewall.py"),
    ("DEAD_CODE_UNREACHABLE_FILE", "kanda_reasoner_app/runtime_scenarios/runtime_hotspot_hooks.py"),
    ("DEAD_CODE_UNREACHABLE_FILE", "kanda_reasoner_app/runtime_scenarios/runtime_scenario_runtime.py"),
    ("DEAD_CODE_UNREACHABLE_FILE", "kanda_reasoner_app/tab3_manual_review_runtime/scan_report_lifecycle_runtime.py"),
    ("DEAD_CODE_UNREACHABLE_FILE", "scripts/merge_freeze_validation_evidence.py"),
    ("DEAD_CODE_UNREACHABLE_FILE", "scripts/migrate_freeze_after_update_external_root.py"),
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _sha256_if_exists(path: Path) -> str | None:
    if not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run(command: list[str], env: dict[str, str]) -> str:
    result = subprocess.run(
        command,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        check=False,
    )
    output = result.stdout + result.stderr
    print(output, end="")
    _require(result.returncode == 0, "COMMAND_FAILED: " + " ".join(command))
    return output


def _parse_architecture(output: str) -> set[tuple[str, str]]:
    pattern = re.compile(r"^WARNING\s+(\S+)\s+(\S+)\s+::", re.MULTILINE)
    return {
        (match.group(1), match.group(2).replace("\\", "/"))
        for match in pattern.finditer(output)
    }


def _latest_receipt(tool_root: Path) -> dict[str, object]:
    root = (
        tool_root.parent
        / (tool_root.name + "_delete_after_daily_work")
        / "tool_freeze_cleanup_install_transactions"
    )
    receipts = sorted(
        root.glob("*/install_receipt.json"),
        key=lambda path: path.stat().st_mtime_ns,
        reverse=True,
    )
    _require(bool(receipts), "INSTALL_RECEIPT_MISSING")
    receipt = json.loads(receipts[0].read_text(encoding="utf-8"))
    _require(receipt.get("feature_id") == FEATURE_ID, "INSTALL_RECEIPT_IDENTITY_MISMATCH")
    _require(receipt.get("package_revision") == PACKAGE_REVISION, "INSTALL_RECEIPT_REVISION_MISMATCH")
    return receipt


def _loaded_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    return {
        node.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    }


def _imports(path: Path, module: str) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    result: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.ImportFrom):
            continue
        if node.level == 1 and node.module == module:
            result.update(
                alias.name for alias in node.names if alias.name in CANONICAL_HELPERS
            )
    return result


def _definition_locations(tool_root: Path) -> dict[str, list[str]]:
    result = {name: [] for name in CANONICAL_HELPERS}
    intake = tool_root / "kanda_reasoner_app/freeze_hint_intake"
    for path in intake.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name in result:
                    result[node.name].append(path.relative_to(tool_root).as_posix())
    return result


def _consumer_graph_violations(tool_root: Path) -> list[str]:
    result: list[str] = []
    intake = tool_root / "kanda_reasoner_app/freeze_hint_intake"
    excluded = {"form_text_validation.py", "local_validation_cleanup.py", "__init__.py"}
    for path in intake.rglob("*.py"):
        if path.name in excluded:
            continue
        used = CANONICAL_HELPERS & _loaded_names(path)
        indirect = _imports(path, "form_normalization")
        direct = _imports(path, "form_text_validation")
        relative = path.relative_to(tool_root).as_posix()
        if indirect:
            result.append(relative + " indirect=" + repr(sorted(indirect)))
        if direct != used:
            result.append(
                relative
                + " direct="
                + repr(sorted(direct))
                + " used="
                + repr(sorted(used))
            )
    return result


def _external_private_reach_ins(tool_root: Path) -> list[str]:
    result: list[str] = []
    app_root = tool_root / "kanda_reasoner_app"
    for path in app_root.rglob("*.py"):
        relative = path.relative_to(tool_root).as_posix()
        if relative.startswith(INTAKE_PREFIX):
            continue
        text = path.read_text(encoding="utf-8-sig")
        if PRIVATE_CLEANUP in text or PRIVATE_MODULE in text:
            result.append(relative)
    return sorted(result)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool-root", required=True)
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--evidence-path", required=True)
    args = parser.parse_args()
    tool_root = Path(args.tool_root).expanduser().resolve(strict=True)
    project_root = Path(args.project_root).expanduser().resolve(strict=True)
    evidence_path = Path(args.evidence_path).expanduser().resolve(strict=False)
    _require(
        os.path.normcase(str(tool_root)) == os.path.normcase(str(project_root)),
        "SELF_HOSTING_ROOTS_MUST_MATCH",
    )
    if str(tool_root) not in sys.path:
        sys.path.insert(0, str(tool_root))
    env = dict(os.environ)
    env["PYTHONPATH"] = str(tool_root)
    env.setdefault("QT_QPA_PLATFORM", "offscreen")
    receipt = _latest_receipt(tool_root)
    values = receipt.get("all_changed_relative_paths", [])
    if not isinstance(values, list):
        values = receipt.get("changed_relative_paths", [])
    touched_paths = {str(item) for item in values if str(item).strip()} | PAYLOAD_PATHS
    registry_module = importlib.import_module("kanda_reasoner_app.project_selection_registry")
    registry = registry_module.ProjectSelectionRegistry(tool_source_root=tool_root)
    registry_before = _sha256_if_exists(registry.registry_path)
    locations = _definition_locations(tool_root)
    owner_path = "kanda_reasoner_app/freeze_hint_intake/form_text_validation.py"
    for name, paths in locations.items():
        _require(paths == [owner_path], "SINGLE_OWNER_INVALID: " + name + ": " + repr(paths))
    violations = _consumer_graph_violations(tool_root)
    _require(not violations, "CONSUMER_GRAPH_VIOLATIONS: " + repr(violations))
    reach_ins = _external_private_reach_ins(tool_root)
    _require(not reach_ins, "EXTERNAL_PRIVATE_REACH_INS: " + repr(reach_ins))
    modules = (
        "kanda_reasoner_app.freeze_hint_intake",
        "kanda_reasoner_app.freeze_hint_intake.contract",
        "kanda_reasoner_app.freeze_hint_intake.records",
        "kanda_reasoner_app.freeze_hint_intake.scanner",
        "kanda_reasoner_app.freeze_hint_intake.autofill",
    )
    imported = [importlib.import_module(name) for name in modules]
    _require(all(imported), "COMPLETE_INTAKE_IMPORT_GRAPH_FAILED")
    intake = imported[0]
    cleanup = getattr(intake, PUBLIC_CLEANUP, None)
    _require(callable(cleanup), "PUBLIC_CLEANUP_CONTRACT_MISSING")
    cleaned = cleanup(
        {
            "validation_evidence_summary": (
                "VALIDATION OK: x\nSTATUS: IN_SYNC\nLocal validation pending."
            ),
            "planned_next_step": "Local validation pending. Freeze next.",
        }
    )
    _require("pending" not in cleaned["validation_evidence_summary"].lower(), "STALE_TEXT_REMAINS")
    for relative in touched_paths:
        path = tool_root / relative
        _require(path.is_file(), "TOUCHED_PATH_MISSING: " + relative)
        source = path.read_text(encoding="utf-8-sig")
        compile(source, relative, "exec")
        _require(len(source.splitlines()) <= 500, "MODULE_SIZE_LIMIT: " + relative)
    importlib.import_module("kanda_reasoner_app.freeze_after_update_gui.freeze_after_update_tab")
    registry_after = _sha256_if_exists(registry.registry_path)
    _require(registry_before == registry_after, "TOOL_REGISTRY_MUTATED_BY_TAB_IMPORT")
    test_output = _run(
        [sys.executable, "-m", "unittest", "-v", "tests.test_tool_freeze_hint_public_cleanup_contract"],
        env,
    )
    _require("Ran 3 tests" in test_output and "OK" in test_output, "FOCUSED_TEST_MARKER_MISSING")
    architecture_output = _run(
        [
            sys.executable,
            str(tool_root / "kanda_reasoner_app/manage_architecture/manage_architecture.py"),
            "--root",
            str(tool_root),
            "--validate",
        ],
        env,
    )
    issues = _parse_architecture(architecture_output)
    new_issues = issues - PREEXISTING
    touched_issues = {item for item in issues if item[1] in touched_paths}
    _require(not new_issues, "NEW_ARCHITECTURE_ISSUES: " + repr(sorted(new_issues)))
    _require(not touched_issues, "TOUCHED_PATH_ARCHITECTURE_ISSUES: " + repr(sorted(touched_issues)))
    lines = [
        "PACKAGE REVISION: " + PACKAGE_REVISION,
        "TOOL ROOT RESOLVED: " + str(tool_root),
        "PROJECT ROOT RESOLVED: " + str(project_root),
        "SELF-HOSTING PHYSICAL ROOT: YES",
        "TOOL PROJECT LOGICAL ROLE SEPARATION: PASS",
        "FULL INTAKE CONSUMER GRAPH DISCOVERY: PASS",
        "FREEZE HINT TRUE TEXT VALIDATION OWNER COUNT: 14",
        "FREEZE HINT INDIRECT HELPER REEXPORT IMPORTS: 0",
        "FREEZE HINT INTERNAL CONSUMER IMPORTS: PASS",
        "FREEZE GUI PRIVATE INTAKE REACH-IN: 0",
        "FREEZE HINT PUBLIC CLEANUP CONTRACT: PASS",
        "FREEZE HINT COMPLETE PACKAGE IMPORT: PASS",
        "FREEZE GUI LAZY TAB IMPORT: PASS",
        "TOOL PROJECT SELECTION REGISTRY MUTATED: NO",
        "FOCUSED PUBLIC CONTRACT TESTS: 3/3 PASS",
        "ARCHITECTURE PREEXISTING BASELINE: 20",
        "ARCHITECTURE CURRENT ISSUES: " + str(len(issues)),
        "NEW ARCHITECTURE ISSUES: 0",
        "TOUCHED PATH ARCHITECTURE ISSUES: 0",
        "ARCHITECTURE NON-REGRESSION: PASS",
        "VALIDATION OK: " + FEATURE_ID,
        "STATUS: IN_SYNC",
    ]
    evidence_path.parent.mkdir(parents=True, exist_ok=True)
    evidence_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    for line in lines:
        print(line)
    print("VALIDATION EVIDENCE WRITTEN: " + str(evidence_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
