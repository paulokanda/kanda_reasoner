"""Validate the KANDA Tool Error Memory marker public contract."""
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
FEATURE_ID = "kanda-reasoner-tool-error-memory-marker-public-contract-v1"
PACKAGE_REVISION = "v1"
MARKERS = ("ERROR_LESSON_JSON_BEGIN", "ERROR_LESSON_JSON_END")
PAYLOAD_PATHS = {
    "tests/test_tool_error_memory_marker_public_contract.py",
    "tools/validate_tool_error_memory_marker_public_contract_v1.py",
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
def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)
def sha_if_exists(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
def run(command: list[str], env: dict[str, str]) -> str:
    result = subprocess.run(command, text=True, capture_output=True, encoding="utf-8", errors="replace", env=env, check=False)
    output = result.stdout + result.stderr
    print(output, end="")
    require(result.returncode == 0, "COMMAND_FAILED: " + " ".join(command))
    return output
def parse_architecture(output: str) -> set[tuple[str, str]]:
    pattern = re.compile(r"^WARNING\s+(\S+)\s+(\S+)\s+::", re.MULTILINE)
    return {(match.group(1), match.group(2).replace("\\", "/")) for match in pattern.finditer(output)}
def latest_receipt(tool_root: Path) -> dict[str, object]:
    root = tool_root.parent / (tool_root.name + "_delete_after_daily_work") / "tool_error_memory_marker_install_transactions"
    receipts = sorted(root.glob("*/install_receipt.json"), key=lambda path: path.stat().st_mtime_ns, reverse=True)
    require(bool(receipts), "INSTALL_RECEIPT_MISSING")
    receipt = json.loads(receipts[0].read_text(encoding="utf-8"))
    require(receipt.get("feature_id") == FEATURE_ID, "INSTALL_RECEIPT_IDENTITY_MISMATCH")
    return receipt
def definition_owners(tool_root: Path) -> dict[str, list[str]]:
    owners = {name: [] for name in MARKERS}
    for path in (tool_root / "kanda_reasoner_app/error_memory").rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        for node in tree.body:
            targets = node.targets if isinstance(node, ast.Assign) else [node.target] if isinstance(node, ast.AnnAssign) else []
            for target in targets:
                if isinstance(target, ast.Name) and target.id in owners:
                    owners[target.id].append(path.relative_to(tool_root).as_posix())
    return owners
def gui_reach_ins(tool_root: Path) -> list[str]:
    violations = []
    for path in (tool_root / "kanda_reasoner_app/error_memory_gui").rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module in {
                "kanda_reasoner_app.error_memory.intake",
                "kanda_reasoner_app.error_memory.intake_normalization",
            } and any(alias.name in MARKERS for alias in node.names):
                violations.append(path.relative_to(tool_root).as_posix())
    return sorted(set(violations))
def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool-root", required=True)
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--evidence-path", required=True)
    args = parser.parse_args()
    tool_root = Path(args.tool_root).expanduser().resolve(strict=True)
    project_root = Path(args.project_root).expanduser().resolve(strict=True)
    evidence_path = Path(args.evidence_path).expanduser().resolve(strict=False)
    require(os.path.normcase(str(tool_root)) == os.path.normcase(str(project_root)), "SELF_HOSTING_ROOTS_MUST_MATCH")
    if str(tool_root) not in sys.path:
        sys.path.insert(0, str(tool_root))
    env = dict(os.environ)
    env["PYTHONPATH"] = str(tool_root)
    env.setdefault("QT_QPA_PLATFORM", "offscreen")
    receipt = latest_receipt(tool_root)
    values = receipt.get("all_changed_relative_paths", [])
    if not isinstance(values, list):
        values = receipt.get("changed_relative_paths", [])
    touched = {str(value) for value in values if str(value).strip()} | PAYLOAD_PATHS
    registry_module = importlib.import_module("kanda_reasoner_app.project_selection_registry")
    registry = registry_module.ProjectSelectionRegistry(tool_source_root=tool_root)
    before = sha_if_exists(registry.registry_path)
    owners = definition_owners(tool_root)
    expected = ["kanda_reasoner_app/error_memory/intake_normalization.py"]
    for marker in MARKERS:
        require(owners[marker] == expected, "ERROR_MEMORY_DUPLICATE_MARKER_OWNER: " + marker + ": " + repr(owners[marker]))
    reach_ins = gui_reach_ins(tool_root)
    require(not reach_ins, "ERROR_MEMORY_EXTERNAL_MARKER_IMPORT_REACH_IN: " + repr(reach_ins))
    public = importlib.import_module("kanda_reasoner_app.error_memory")
    require(getattr(public, MARKERS[0], None) == "KANDA_ERROR_LESSON_JSON_BEGIN", "ERROR_MEMORY_BEGIN_PUBLIC_EXPORT_MISSING")
    require(getattr(public, MARKERS[1], None) == "KANDA_ERROR_LESSON_JSON_END", "ERROR_MEMORY_END_PUBLIC_EXPORT_MISSING")
    importlib.import_module("kanda_reasoner_app.error_memory.intake")
    importlib.import_module("kanda_reasoner_app.error_memory_gui._text_payloads")
    importlib.import_module("kanda_reasoner_app.error_memory_gui._table_view")
    importlib.import_module("kanda_reasoner_app.error_memory_gui.error_memory_tab")
    after = sha_if_exists(registry.registry_path)
    require(before == after, "TOOL_REGISTRY_MUTATED_BY_ERROR_MEMORY_TAB_IMPORT")
    for relative in touched:
        path = tool_root / relative
        require(path.is_file(), "TOUCHED_PATH_MISSING: " + relative)
        source = path.read_text(encoding="utf-8-sig")
        compile(source, relative, "exec")
        require(len(source.splitlines()) <= 500, "MODULE_SIZE_LIMIT: " + relative)
    test_output = run([sys.executable, "-m", "unittest", "-v", "tests.test_tool_error_memory_marker_public_contract"], env)
    require("Ran 3 tests" in test_output and "OK" in test_output, "FOCUSED_TEST_MARKER_MISSING")
    architecture_output = run([
        sys.executable,
        str(tool_root / "kanda_reasoner_app/manage_architecture/manage_architecture.py"),
        "--root", str(tool_root), "--validate",
    ], env)
    issues = parse_architecture(architecture_output)
    new_issues = issues - PREEXISTING
    touched_issues = {item for item in issues if item[1] in touched}
    require(not new_issues, "NEW_ARCHITECTURE_ISSUES: " + repr(sorted(new_issues)))
    require(not touched_issues, "TOUCHED_PATH_ARCHITECTURE_ISSUES: " + repr(sorted(touched_issues)))
    lines = [
        "PACKAGE REVISION: " + PACKAGE_REVISION,
        "TOOL ROOT RESOLVED: " + str(tool_root),
        "PROJECT ROOT RESOLVED: " + str(project_root),
        "SELF-HOSTING PHYSICAL ROOT: YES",
        "TOOL PROJECT LOGICAL ROLE SEPARATION: PASS",
        "VALIDATOR TOOL ROOT IMPORT PATH: PASS",
        "ERROR MEMORY SINGLE MARKER OWNER: PASS",
        "ERROR MEMORY PUBLIC MARKER FACADE: PASS",
        "ERROR MEMORY GUI MARKER REACH-IN: 0",
        "ERROR MEMORY COMPLETE IMPORT GRAPH: PASS",
        "ERROR MEMORY LAZY TAB IMPORT: PASS",
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
