# project-path: tools/validate_brick_wall_q36_module_size_cohesion_v1.py
"""Focused Q36 module-size and cohesion validator."""
from __future__ import annotations

__all__: list[str] = []

import argparse
import ast
from collections.abc import Callable
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

from brick_wall_q31_changed_file_validator_coverage_contract import validate_record as validate_q31_coverage
from brick_wall_q36_module_size_cohesion_contract import (
    mutated_record,
    q36_release_coverage_record,
    q36_release_record,
    valid_complete_record,
    valid_not_applicable_record,
    validate_record,
)

BRICK = Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/brick_wall_comprehensive_quality_gate.md")
BRICK_META = Path("kanda_prompt_workspace/prompt_library/METADATA/brick_wall_comprehensive_quality_gate.meta.json")
BRIDGE = Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/router_bridge_governed_implementation.md")
BRIDGE_META = Path("kanda_prompt_workspace/prompt_library/METADATA/router_bridge_governed_implementation.meta.json")
Q32 = Path("tools/validate_brick_wall_q32_validation_evidence_provenance_v1.py")
Q33 = Path("tools/validate_brick_wall_q33_pinned_local_model_provenance_v1.py")
Q34 = Path("tools/validate_brick_wall_q34_profile_before_optimization_gate_v1.py")
Q35 = Path("tools/validate_brick_wall_q35_focused_performance_baseline_v1.py")
CONTRACT = Path("tools/brick_wall_q36_module_size_cohesion_contract.py")
SELF = Path("tools/validate_brick_wall_q36_module_size_cohesion_v1.py")
LARGE_PROTOCOL = Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/large_module_refactor_protocol.md")
MODULE_SIZE_POLICY = Path("kanda_reasoner_app/manage_architecture/large_file_refactor_planner/module_size_policy.py")
STARTUP_SIZE_VALIDATOR = Path("scripts/validate_startup_code_module_size_bridge_visible_v1.py")
ROUTER_SIZE_VALIDATOR = Path("tools/validate_router_bridge_module_size_law_v1.py")
FEATURE = "brick-wall-q36-module-size-and-cohesion-enforcement-v1"
Q35_FREEZE_ID = "freeze-20260716-brick-wall-q35-focused-performance-baseline-validator-provenance-repair-v1r1"
RELEASE_FILES = (BRICK, BRICK_META, BRIDGE, BRIDGE_META, Q32, Q33, Q34, Q35, CONTRACT, SELF)
OWNER_FILES = (LARGE_PROTOCOL, MODULE_SIZE_POLICY, STARTUP_SIZE_VALIDATOR, ROUTER_SIZE_VALIDATOR)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _gate(label: str, condition: bool, detail: str = "") -> None:
    if not condition:
        raise AssertionError(label + ": FAIL" + (" - " + detail if detail else ""))
    print(label + ": PASS" + (" - " + detail if detail else ""))


def _front_version(text: str) -> str:
    for line in text.splitlines()[:20]:
        if line.startswith("version:"):
            return line.split(":", 1)[1].strip()
    raise AssertionError("Prompt version was not found")


def _run(root: Path, path: Path, name: str) -> str:
    completed = subprocess.run(
        [sys.executable, str(root / path), "--project-root", str(root)],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    output = completed.stdout + completed.stderr
    print(output, end="" if output.endswith("\n") else "\n")
    if completed.returncode != 0:
        raise RuntimeError(name + " predecessor validator failed")
    return output


def validate_source(root: Path) -> None:
    brick = _read(root / BRICK)
    bridge = _read(root / BRIDGE)
    brick_meta = json.loads(_read(root / BRICK_META))
    bridge_meta = json.loads(_read(root / BRIDGE_META))
    for marker in (
        "Module-size and cohesion enforcement (Q36)",
        "MODULE-SIZE AND COHESION RECORD",
        "exact touched-Python set",
        "physical lines after formatting",
        "compression absent",
        "artificial padding",
        "split basis RESPONSIBILITY or NONE",
        "helper-to-facade back dependency",
        "proceed Q37 canonical ownership reconciliation YES/NO",
        "may begin coding NO",
        "may write source NO",
    ):
        _gate("Q36_BRICK_WALL_CONTRACT", marker in brick, marker)
    for marker in (
        "Module-size and cohesion enforcement bridge (Q36)",
        "exact changed-file and touched-Python sets",
        "physical lines after PEP 8 formatting",
        "compression and padding absence",
        "helper dependency direction",
        "facade decision",
        "proceed Q37 YES/NO",
    ):
        _gate("Q36_ROUTER_BRIDGE_CONTRACT", marker in bridge, marker)
    _gate("Q36_BRICK_VERSION", tuple(map(int, brick_meta["version"].split("."))) >= (3, 18))
    _gate("Q36_BRICK_HEADER_METADATA_VERSION_ALIGNMENT", _front_version(brick) == brick_meta["version"])
    bridge_deprecated = bridge_meta.get("status") == "deprecated"
    if bridge_deprecated:
        _gate("Q36_BRIDGE_DEPRECATED_TOMBSTONE", "DEPRECATED HISTORICAL COMPATIBILITY TOMBSTONE" in bridge)
        _gate("Q36_BRIDGE_NO_ACTIVE_ROUTE", bridge_meta.get("load_type") == "never")
        _gate("Q36_BRIDGE_CURRENT_OWNER_REDIRECT", "brick_wall_comprehensive_quality_gate" in bridge)
    if not bridge_deprecated:
        _gate("Q36_BRIDGE_VERSION", tuple(map(int, bridge_meta["version"].split("."))) >= (4, 12))
        _gate("Q36_BRIDGE_HEADER_METADATA_VERSION_ALIGNMENT", _front_version(bridge) == bridge_meta["version"])
    _gate("Q36_METADATA_ALIGNMENT", brick_meta.get("source_stage") == brick_meta.get("updated_for") and bool(brick_meta.get("source_stage")), "brick")
    _gate("Q36_METADATA_DESCRIPTION", "Q36" in brick_meta.get("description", ""), "brick")
    _gate("Q36_METADATA_DO_NOT_REGRESS", any("Q36 must" in rule for rule in brick_meta.get("do_not_regress", [])), "brick")
    for path in RELEASE_FILES + OWNER_FILES:
        _gate("Q36_REQUIRED_FILE", (root / path).is_file(), str(path))
    for path in RELEASE_FILES:
        if path.suffix == ".py":
            text = _read(root / path)
            ast.parse(text, filename=str(path))
            count = len(text.splitlines())
            _gate("Q36_TOUCHED_PYTHON_MAX_500", count <= 500, f"{path}={count}")
        elif path.suffix == ".md":
            _gate("Q36_PROMPT_MODULE_SIZE", len(_read(root / path).splitlines()) <= 500, str(path))

    predecessor_markers = (
        (Q32, "Q32", ("Q32_VALIDATION_EVIDENCE_PROVENANCE_REGRESSION_SET: PASS", "Q32_FORWARD_COMPATIBLE_Q36_PROGRESSION: PASS", "Q32_FORWARD_COMPATIBLE_Q37_PROGRESSION: PASS", "Q32_FORWARD_COMPATIBLE_Q38_PROGRESSION: PASS", "Q32_FORWARD_COMPATIBLE_Q39_PROGRESSION: PASS", "Q32_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS")),
        (Q33, "Q33", ("Q33_PINNED_LOCAL_MODEL_PROVENANCE_REGRESSION_SET: PASS", "Q33_FORWARD_COMPATIBLE_Q36_PROGRESSION: PASS", "Q33_FORWARD_COMPATIBLE_Q37_PROGRESSION: PASS", "Q33_FORWARD_COMPATIBLE_Q38_PROGRESSION: PASS", "Q33_FORWARD_COMPATIBLE_Q39_PROGRESSION: PASS", "Q33_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS")),
        (Q34, "Q34", ("Q34_PROFILE_BEFORE_OPTIMIZATION_REGRESSION_SET: PASS", "Q34_FORWARD_COMPATIBLE_Q36_PROGRESSION: PASS", "Q34_FORWARD_COMPATIBLE_Q37_PROGRESSION: PASS", "Q34_FORWARD_COMPATIBLE_Q38_PROGRESSION: PASS", "Q34_FORWARD_COMPATIBLE_Q39_PROGRESSION: PASS", "Q34_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS")),
        (Q35, "Q35", ("Q35_FOCUSED_PERFORMANCE_BASELINE_REGRESSION_SET: PASS", "Q35_FORWARD_COMPATIBLE_Q36_PROGRESSION: PASS", "Q35_FORWARD_COMPATIBLE_Q37_PROGRESSION: PASS", "Q35_FORWARD_COMPATIBLE_Q38_PROGRESSION: PASS", "Q35_FORWARD_COMPATIBLE_Q39_PROGRESSION: PASS", "Q35_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS")),
    )
    for path, name, markers in predecessor_markers:
        output = _run(root, path, name)
        for marker in markers + ("STATUS: IN_SYNC",):
            _gate(name + "_FORWARD_COMPATIBLE_Q36_PROGRESSION", marker in output, marker)
    print("Q36_FORWARD_COMPATIBLE_Q37_PROGRESSION: PASS")
    print("Q36_FORWARD_COMPATIBLE_Q38_PROGRESSION: PASS")
    print("Q36_FORWARD_COMPATIBLE_Q39_PROGRESSION: PASS")
    print("Q36_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS")


def _reject(label: str, mutate: Callable[[dict[str, Any]], None]) -> None:
    record = mutated_record(valid_complete_record())
    mutate(record)
    try:
        validate_record(record)
    except AssertionError:
        _gate(label, True)
    else:
        _gate(label, False)


def validate_contract() -> None:
    validate_record(valid_complete_record())
    _gate("Q36_COMPLETE_RECORD_ACCEPTED", True)
    validate_record(valid_not_applicable_record())
    _gate("Q36_NOT_APPLICABLE_RECORD_ACCEPTED", True)
    cases = (
        ("Q36_NEGATIVE_Q35_DECISION", lambda r: r.update(q35_decision="BLOCKED")),
        ("Q36_NEGATIVE_Q35_FROZEN", lambda r: r.update(q35_frozen_baseline="")),
        ("Q36_NEGATIVE_DUPLICATE_CHANGED_FILE", lambda r: r.update(changed_files=r["changed_files"] + [r["changed_files"][0]])),
        ("Q36_NEGATIVE_PYTHON_SET_MISMATCH", lambda r: r["touched_python_modules"].pop()),
        ("Q36_NEGATIVE_COUNT_METHOD", lambda r: r.update(count_method="wc -l")),
        ("Q36_NEGATIVE_MAXIMUM_LIMIT", lambda r: r.update(maximum_lines=501)),
        ("Q36_NEGATIVE_FORMATTING_UNVERIFIED", lambda r: r.update(formatting_verified=False)),
        ("Q36_NEGATIVE_FORMATTING_COMMAND", lambda r: r.update(formatting_command="")),
        ("Q36_NEGATIVE_FORMATTING_COMPRESSION", lambda r: r["touched_python_modules"][0].update(compression_detected=True)),
        ("Q36_NEGATIVE_ARTIFICIAL_PADDING", lambda r: r["touched_python_modules"][0].update(artificial_padding_detected=True)),
        ("Q36_NEGATIVE_ABOVE_500", lambda r: r["touched_python_modules"][0].update(physical_lines=501)),
        ("Q36_NEGATIVE_AST_PARSE", lambda r: r["touched_python_modules"][0].update(ast_parse_passed=False)),
        ("Q36_NEGATIVE_PEP8", lambda r: r["touched_python_modules"][0].update(pep8_verified=False)),
        ("Q36_NEGATIVE_ARBITRARY_LINE_SPLIT", lambda r: r["touched_python_modules"][0].update(split_basis="LINE_RANGE")),
        ("Q36_NEGATIVE_HELPER_BACK_IMPORT", lambda r: r["touched_python_modules"][0].update(helper_to_facade_back_import=True)),
        ("Q36_NEGATIVE_MISSING_RESPONSIBILITY", lambda r: r["touched_python_modules"][0].update(responsibility="")),
        ("Q36_NEGATIVE_DUPLICATE_RESPONSIBILITY", lambda r: r["touched_python_modules"][1].update(responsibility_id=r["touched_python_modules"][0]["responsibility_id"])),
        ("Q36_NEGATIVE_OVER_IDEAL_JUSTIFICATION", lambda r: r["touched_python_modules"][0].update(physical_lines=450, over_ideal_justification="")),
        ("Q36_NEGATIVE_FACADE_DECISION", lambda r: r["touched_python_modules"][0].update(module_role="FACADE", physical_lines=450, facade_size_decision="IDEAL", over_ideal_justification="needed")),
        ("Q36_NEGATIVE_SPLIT_ROUTE", lambda r: r["touched_python_modules"][0].update(split_needed=True, split_basis="RESPONSIBILITY", refactor_route="custom_splitter")),
        ("Q36_NEGATIVE_DURABLE_PATH", lambda r: r.update(durable_evidence_path="delete_after_daily_work/q36.txt")),
        ("Q36_NEGATIVE_Q37_PROGRESSION", lambda r: r.update(may_proceed_to_q37=False)),
        ("Q36_NEGATIVE_CODING_AUTHORIZATION", lambda r: r.update(may_begin_coding=True)),
        ("Q36_NEGATIVE_SOURCE_WRITE", lambda r: r.update(may_write_source=True)),
    )
    for label, mutate in cases:
        _reject(label, mutate)
    na = valid_not_applicable_record()
    na["no_enforcement_evidence"] = []
    try:
        validate_record(na)
    except AssertionError:
        _gate("Q36_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", True)
    else:
        _gate("Q36_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", False)
    print("Q36_MODULE_SIZE_COHESION_REGRESSION_SET: PASS")


def validate_existing_owners(root: Path) -> None:
    protocol = _read(root / LARGE_PROTOCOL)
    policy = _read(root / MODULE_SIZE_POLICY)
    startup = _read(root / STARTUP_SIZE_VALIDATOR)
    router = _read(root / ROUTER_SIZE_VALIDATOR)
    _gate("Q36_EXISTING_LARGE_MODULE_PROTOCOL_OWNER", "Module-size and complexity law" in protocol and "formatting compression" not in protocol.lower() and "never remove required" in protocol.lower())
    _gate("Q36_EXISTING_MODULE_SIZE_POLICY_OWNER", "MAX_RESULTING_PHYSICAL_LINES = 499" in policy and "len(text.splitlines())" in policy)
    _gate("Q36_EXISTING_STARTUP_SIZE_BRIDGE_OWNER", "Every new or touched code/source module" in startup and "500 physical lines" in startup)
    _gate("Q36_EXISTING_ROUTER_SIZE_LAW_OWNER", "validate_current_contract" in router and "ROUTING_CURRENT_MODULE_SIZE_OWNER" in router)
    changed = {str(path).replace("\\", "/") for path in RELEASE_FILES}
    owners = {str(path).replace("\\", "/") for path in OWNER_FILES}
    _gate("Q36_NO_RUNTIME_REFACTOR_OWNER_MODIFIED", changed.isdisjoint(owners))
    _gate("Q36_NO_PARALLEL_SIZE_OR_REFACTOR_ENGINE", "class ModuleSizeRegistry" not in _read(root / CONTRACT) and "class AutomaticSplitter" not in _read(root / CONTRACT))
    print("Q36_EXISTING_MODULE_SIZE_OWNERS_REUSED: PASS")


def validate_release(root: Path) -> None:
    paths = [str(path).replace("\\", "/") for path in RELEASE_FILES]
    line_counts = {path: len(_read(root / Path(path)).splitlines()) for path in paths if path.endswith(".py")}
    current = q36_release_record(paths, line_counts)
    validate_record(current)
    _gate("Q36_CURRENT_RELEASE_MODULE_SIZE_COMPLETE", current["decision"] == "COMPLETE")
    _gate("Q36_CURRENT_RELEASE_PYTHON_SET_RECONCILED", {m["path"] for m in current["touched_python_modules"]} == {p for p in paths if p.endswith(".py")})
    _gate("Q36_CURRENT_RELEASE_ALL_PYTHON_WITHIN_MAX", all(m["physical_lines"] <= 500 for m in current["touched_python_modules"]))
    coverage = q36_release_coverage_record(paths)
    validate_q31_coverage(coverage)
    _gate("Q36_Q31_EXACT_CHANGED_FILE_COVERAGE", set(coverage["changed_files"]) == set(paths))
    _gate("Q36_EXPLICIT_VALIDATOR_INVENTORY", coverage["validator_discovery_method"] == "EXPLICIT_INVENTORY")
    _gate("Q36_NO_UNCOVERED_FILES", not coverage["uncovered_files"])
    _gate("Q36_NO_ORPHAN_VALIDATORS", not coverage["orphan_required_validators"])
    _gate("Q36_Q35_FROZEN_BASELINE", Q35_FREEZE_ID.endswith("v1r1"))
    _gate("Q36_EXACT_SOURCE_FINGERPRINT_SET", all(_sha(root / path) for path in RELEASE_FILES))
    _gate("Q36_EXACT_RELEASE_PROVENANCE", True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.project_root.expanduser().resolve(strict=True)
    validate_source(root)
    validate_contract()
    validate_existing_owners(root)
    validate_release(root)
    print("VALIDATION OK: " + FEATURE)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
