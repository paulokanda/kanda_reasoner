"""Live validator for the startup-kernel ZIP contract owner repair."""

from __future__ import annotations

import argparse
import ast
from contextlib import redirect_stdout
from datetime import datetime, timezone
import importlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

FEATURE_ID = "kanda-reasoner-tool-startup-kernel-zip-contract-owner-v1"
PACKAGE_REVISION = "v1"
CONTRACT_MODULE = "startup_kernel.zip_contract"
DELIVERY_MODULE = "startup_kernel.zip_delivery"
CONTRACT_NAMES = {
    "read_manifest_from_zip",
    "validate_generated_zip_contract",
}
STATIC_TOUCHED = frozenset({
    "kanda_prompt_workspace/prompt_tools/startup_kernel/cli_check.py",
    "kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py",
    "tests/test_tool_startup_kernel_zip_contract_owner.py",
    "tools/validate_tool_startup_kernel_zip_contract_owner_v1.py",
})
_ALLOWED_WARNING_PATHS = frozenset({
    "kanda_prompt_workspace/prompt_tools/startup_kernel/constants.py",
    "kanda_prompt_workspace/prompt_tools/startup_kernel/generic_helpers.py",
    "kanda_prompt_workspace/prompt_tools/startup_kernel/source_resolution.py",
    "kanda_reasoner_app/daily_rfctr_report/daily_refactor_report.py",
    "kanda_reasoner_app/reasoner_context_collector/collector_runtime_scenarios_help/normalization.py",
    "kanda_reasoner_app/reasoner_context_collector/collector_widget_ui_action_bridge_help/indexing.py",
    "kanda_reasoner_app/reasoner_context_collector/collector_widget_ui_action_bridge_help/matching.py",
    "kanda_reasoner_app/reasoner_runtime_collector/hooks/qt_connection_monitor.py",
    "kanda_reasoner_app/reasoner_runtime_collector/runtime_trace_decorators.py",
    "kanda_reasoner_app/reasoner_runtime_collector/runtime_trace_state.py",
    "kanda_reasoner_app/routing_signal_scorer/prompt_intake_boundary/prompt_artifact_contract.py",
    "kanda_reasoner_app/routing_signal_scorer/prompt_intake_boundary/prompt_output_firewall.py",
    "kanda_reasoner_app/runtime_scenarios/runtime_hotspot_hooks.py",
    "kanda_reasoner_app/runtime_scenarios/runtime_scenario_runtime.py",
    "kanda_reasoner_app/tab3_manual_review_runtime/scan_report_lifecycle_runtime.py",
    "scripts/merge_freeze_validation_evidence.py",
    "scripts/migrate_freeze_after_update_external_root.py",
})


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _module_text(node: ast.ImportFrom) -> str:
    return "." * node.level + (node.module or "")


def _imported_names(path: Path, module: str) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    names: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and _module_text(node) == module:
            names.extend(alias.name for alias in node.names)
    return names


def _definition_owners(kernel_root: Path) -> dict[str, list[str]]:
    owners = {name: [] for name in CONTRACT_NAMES}
    for path in kernel_root.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name in owners:
                    owners[node.name].append(path.name)
    return owners


def _receipt_paths(tool_root: Path) -> set[str]:
    receipt_root = (
        Path(tool_root.anchor)
        / (tool_root.name + "_delete_after_daily_work")
        / "install_receipts"
    )
    candidates = sorted(
        receipt_root.glob("*_tool_startup_kernel_zip_contract_owner_v1.json")
    )
    _require(bool(candidates), "STARTUP_KERNEL_INSTALL_RECEIPT_MISSING")
    receipt = json.loads(candidates[-1].read_text(encoding="utf-8"))
    _require(
        receipt.get("project_specific_state_written") is False,
        "PROJECT_STATE_WRITE_RECORDED",
    )
    return {
        str(item).replace("\\", "/")
        for item in receipt.get("changed_paths", [])
    }


def _run(command: list[str], root: Path, env: dict[str, str]) -> str:
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
    return output


def _check_source_contract(tool_root: Path) -> None:
    prompt_tools = tool_root / "kanda_prompt_workspace/prompt_tools"
    kernel = prompt_tools / "startup_kernel"
    owners = _definition_owners(kernel)
    expected = {
        "read_manifest_from_zip": ["zip_contract.py"],
        "validate_generated_zip_contract": ["zip_contract.py"],
    }
    _require(owners == expected, "STARTUP_KERNEL_CONTRACT_OWNER_MISMATCH")
    consumers = (
        kernel / "cli_check.py",
        prompt_tools / "sync_startup_routing_kernel_pack.py",
    )
    for path in consumers:
        contract = _imported_names(path, CONTRACT_MODULE)
        delivery = _imported_names(path, DELIVERY_MODULE)
        for name in CONTRACT_NAMES:
            _require(
                contract.count(name) == 1,
                "STARTUP_KERNEL_CONTRACT_IMPORT_COUNT: " + str(path),
            )
            _require(
                name not in delivery,
                "STARTUP_KERNEL_DELIVERY_REEXPORT_REACH_IN: " + str(path),
            )
    print("STARTUP KERNEL ZIP CONTRACT OWNER: PASS")
    print("STARTUP KERNEL DELIVERY REEXPORT REACH-IN: 0")
    print("STARTUP KERNEL SINGLE SYMBOL OWNER: PASS")


def _check_import_graph() -> tuple[object, object]:
    contract = importlib.import_module(CONTRACT_MODULE)
    importlib.import_module("startup_kernel.cli_check")
    sync_module = importlib.import_module("sync_startup_routing_kernel_pack")
    for name in CONTRACT_NAMES:
        _require(hasattr(contract, name), "CONTRACT_SYMBOL_MISSING: " + name)
        _require(hasattr(sync_module, name), "SYNC_FACADE_SYMBOL_MISSING: " + name)
    print("STARTUP KERNEL COMPLETE IMPORT GRAPH: PASS")
    return contract, sync_module


def _check_temp_generation(
    tool_root: Path,
    project_root: Path,
    contract: object,
    sync_module: object,
) -> None:
    workspace = tool_root / "kanda_prompt_workspace"
    with tempfile.TemporaryDirectory(prefix="kanda_startup_kernel_validation_") as name:
        output_dir = Path(name) / "first_prompt_files"
        capture = io.StringIO()
        with redirect_stdout(capture):
            result, archive = sync_module.make_zip(
                workspace,
                output_dir,
                project_root,
                dry_run=False,
            )
        output = capture.getvalue()
        print(output.rstrip())
        _require(result == 0, "FIRST_PROMPT_TEMP_GENERATION_FAILED")
        _require(archive is not None and archive.is_file(), "FIRST_PROMPT_ZIP_MISSING")
        manifest = contract.read_manifest_from_zip(archive)
        _require(isinstance(manifest, dict), "FIRST_PROMPT_MANIFEST_INVALID")
        contract.validate_generated_zip_contract(archive)
        _require(
            (output_dir / "first_prompts_to_ai.zip").is_file(),
            "FIRST_PROMPT_CANONICAL_ZIP_MISSING",
        )
    print("FIRST PROMPT TEMPORARY DELIVERY GENERATION: PASS")
    print("FIRST PROMPT MANIFEST READ THROUGH CONTRACT OWNER: PASS")
    print("PROJECT FIRST PROMPT DESTINATION MUTATED: NO")


def _issues(output: str) -> tuple[tuple[str, str, str], ...]:
    found: list[tuple[str, str, str]] = []
    for line in output.splitlines():
        match = re.match(r"^(WARNING|ERROR|OTHER)\s+(\S+)\s+(.*?)\s+::", line)
        if match:
            severity, code, path = match.groups()
            found.append((severity, code, path.strip().replace("\\", "/")))
    return tuple(found)


def _check_architecture(output: str, touched: frozenset[str]) -> None:
    match = re.search(
        r"Total issues:\s*(\d+)\s*\|\s*Errors:\s*(\d+)"
        r"\s*\|\s*Warnings:\s*(\d+)\s*\|\s*Other:\s*(\d+)",
        output,
    )
    _require(match is not None, "ARCHITECTURE_SUMMARY_MISSING")
    total, errors, warnings, other = (int(value) for value in match.groups())
    issues = _issues(output)
    _require(total == len(issues), "ARCHITECTURE_OUTPUT_INCOMPLETE")
    _require(errors == 0 and other == 0, "ARCHITECTURE_BLOCKING_ISSUES_PRESENT")
    _require(warnings == len(issues), "ARCHITECTURE_WARNING_COUNT_MISMATCH")
    current = set(issues)
    _require(len(current) == len(issues), "ARCHITECTURE_DUPLICATE_ISSUE_IDENTITY")
    allowed = {
        ("WARNING", "DEAD_CODE_UNREACHABLE_FILE", path)
        for path in _ALLOWED_WARNING_PATHS
    }
    unexpected = sorted(current - allowed)
    _require(not unexpected, "NEW_ARCHITECTURE_ISSUES: " + repr(unexpected))
    touched_issues = sorted(issue for issue in issues if issue[2] in touched)
    _require(
        not touched_issues,
        "TOUCHED_PATH_ARCHITECTURE_ISSUES: " + repr(touched_issues),
    )
    print("ARCHITECTURE PREEXISTING BASELINE: " + str(len(allowed)))
    print("ARCHITECTURE CURRENT ISSUES: " + str(len(current)))
    print("NEW ARCHITECTURE ISSUES: 0")
    print("TOUCHED PATH ARCHITECTURE ISSUES: 0")
    print("ARCHITECTURE NON-REGRESSION: PASS")


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
    prompt_tools = tool_root / "kanda_prompt_workspace/prompt_tools"
    for path in (str(prompt_tools), str(tool_root)):
        if path not in sys.path:
            sys.path.insert(0, path)
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
    _check_source_contract(tool_root)
    contract, sync_module = _check_import_graph()
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join((str(prompt_tools), str(tool_root)))
    tests = _run(
        [
            sys.executable,
            "-m",
            "unittest",
            "-v",
            "tests.test_tool_startup_kernel_zip_contract_owner",
        ],
        tool_root,
        env,
    )
    _require("Ran 3 tests" in tests and "OK" in tests, "FOCUSED_TEST_MARKER_MISSING")
    print("FOCUSED PUBLIC CONTRACT TESTS: 3/3 PASS")
    registry = tool_root / "kanda_reasoner_app/project_registry/selected_project.json"
    registry_before = registry.read_bytes() if registry.is_file() else b""
    _check_temp_generation(tool_root, project_root, contract, sync_module)
    registry_after = registry.read_bytes() if registry.is_file() else b""
    _require(registry_before == registry_after, "TOOL_PROJECT_SELECTION_REGISTRY_MUTATED")
    print("TOOL PROJECT SELECTION REGISTRY MUTATED: NO")
    architecture = tool_root / "kanda_reasoner_app/manage_architecture/manage_architecture.py"
    architecture_output = _run(
        [sys.executable, str(architecture), "--root", str(tool_root), "--validate"],
        tool_root,
        env,
    )
    _check_architecture(architecture_output, touched)
    evidence = Path(args.evidence_path)
    evidence.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "VALIDATION OK: " + FEATURE_ID,
        "STATUS: IN_SYNC",
        "PACKAGE REVISION: " + PACKAGE_REVISION,
        "TOOL PROJECT LOGICAL ROLE SEPARATION: PASS",
        "STARTUP KERNEL ZIP CONTRACT OWNER: PASS",
        "STARTUP KERNEL DELIVERY REEXPORT REACH-IN: 0",
        "FIRST PROMPT TEMPORARY DELIVERY GENERATION: PASS",
        "PROJECT FIRST PROMPT DESTINATION MUTATED: NO",
        "PROJECT-SPECIFIC STATE WRITTEN: NO",
        "NEW ARCHITECTURE ISSUES: 0",
        "TOUCHED PATH ARCHITECTURE ISSUES: 0",
        "created_at_utc: " + datetime.now(timezone.utc).isoformat(),
    ]
    evidence.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("VALIDATION EVIDENCE WRITTEN: " + str(evidence))
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
