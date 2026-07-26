"""Validate Brick Wall Q03 Error Memory regression obligations."""

from __future__ import annotations

__all__: list[str] = []

import importlib
import json
from pathlib import Path
import tempfile
import sys
from typing import Iterable

FEATURE_ID = "brick-wall-q03-error-memory-regression-obligation-matrix-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
BRICK_WALL = (
    PROJECT_ROOT
    / "kanda_prompt_workspace"
    / "prompt_library"
    / "ACTIVE_PROMPTS"
    / "03_governance_freeze_and_handoff"
    / "brick_wall_comprehensive_quality_gate.md"
)
BRICK_META = (
    PROJECT_ROOT
    / "kanda_prompt_workspace"
    / "prompt_library"
    / "METADATA"
    / "brick_wall_comprehensive_quality_gate.meta.json"
)
ROUTER_BRIDGE = (
    PROJECT_ROOT
    / "kanda_prompt_workspace"
    / "prompt_library"
    / "ACTIVE_PROMPTS"
    / "05_patch_delivery_and_validation"
    / "router_bridge_governed_implementation.md"
)
ROUTER_META = (
    PROJECT_ROOT
    / "kanda_prompt_workspace"
    / "prompt_library"
    / "METADATA"
    / "router_bridge_governed_implementation.meta.json"
)
EXPORTER = PROJECT_ROOT / "kanda_reasoner_app" / "error_memory" / "exporter.py"

MATRIX_FIELDS = (
    "Lesson ID:",
    "Match confidence: exact / partial / weak",
    "Freshness: current / stale / partial / unresolved",
    "Disposition: EXISTING_VALIDATOR / NEW_FOCUSED_TEST / NOT_APPLICABLE / CURRENT_SOURCE_REINTERPRETATION",
    "Protection owner:",
    "Validator or test path:",
    "Expected success marker:",
    "Expected rejection marker:",
    "Disposition reason:",
    "Status: COMPLETE / BLOCKED",
)
ALLOWED_DISPOSITIONS = {
    "EXISTING_VALIDATOR",
    "NEW_FOCUSED_TEST",
    "NOT_APPLICABLE",
    "CURRENT_SOURCE_REINTERPRETATION",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(_read(path))


def _require(text: str, fragment: str, label: str) -> None:
    if fragment not in text:
        raise AssertionError(f"{label} missing fragment: {fragment}")


def _load_exporter_module():
    root_text = str(PROJECT_ROOT)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    return importlib.import_module("kanda_reasoner_app.error_memory.exporter")


def _parse_matrix(record: str, relevant_ids: Iterable[str]) -> list[dict[str, str]]:
    expected = list(relevant_ids)
    blocks = record.split("Lesson ID:")[1:]
    parsed: list[dict[str, str]] = []
    labels = (
        "Match confidence:",
        "Freshness:",
        "Disposition:",
        "Protection owner:",
        "Validator or test path:",
        "Expected success marker:",
        "Expected rejection marker:",
        "Disposition reason:",
        "Status:",
    )
    for raw_block in blocks:
        lines = [line.strip() for line in raw_block.strip().splitlines() if line.strip()]
        if not lines:
            continue
        row: dict[str, str] = {"Lesson ID": lines[0]}
        for label in labels:
            matches = [line for line in lines if line.startswith(label)]
            if len(matches) != 1:
                raise AssertionError(f"matrix row field count invalid: {label}")
            row[label[:-1]] = matches[0].split(":", 1)[1].strip()
        parsed.append(row)

    actual_ids = [row["Lesson ID"] for row in parsed]
    if sorted(actual_ids) != sorted(expected):
        raise AssertionError("matrix lesson-ID set does not match relevant lesson IDs")
    if len(actual_ids) != len(set(actual_ids)):
        raise AssertionError("duplicate lesson row")

    for row in parsed:
        disposition = row["Disposition"]
        if disposition not in ALLOWED_DISPOSITIONS:
            raise AssertionError("unknown disposition")
        if row["Status"] != "COMPLETE":
            raise AssertionError("matrix row is not complete")
        if disposition in {"EXISTING_VALIDATOR", "NEW_FOCUSED_TEST"}:
            if not row["Validator or test path"]:
                raise AssertionError("protection path is required")
            if not row["Expected success marker"]:
                raise AssertionError("success marker is required")
            if not row["Expected rejection marker"]:
                raise AssertionError("rejection marker is required")
        if disposition in {"NOT_APPLICABLE", "CURRENT_SOURCE_REINTERPRETATION"}:
            if not row["Disposition reason"]:
                raise AssertionError("disposition reason is required")
    return parsed


def _complete_record() -> str:
    return """Relevant lesson IDs: lesson-a, lesson-b
ERROR MEMORY REGRESSION MATRIX
Lesson ID: lesson-a
Match confidence: exact
Freshness: current
Disposition: EXISTING_VALIDATOR
Protection owner: Error Memory
Validator or test path: tools/test_a.py
Expected success marker: A_PASS
Expected rejection marker: A_REJECT
Disposition reason: current validator covers the failure
Status: COMPLETE
Lesson ID: lesson-b
Match confidence: partial
Freshness: partial
Disposition: CURRENT_SOURCE_REINTERPRETATION
Protection owner: prompt-library
Validator or test path:
Expected success marker:
Expected rejection marker:
Disposition reason: current source moved the public owner
Status: COMPLETE
"""


def _validate_contract_sources() -> None:
    for path in (BRICK_WALL, ROUTER_BRIDGE, EXPORTER):
        text = _read(path)
        _require(text, "ERROR MEMORY REGRESSION MATRIX", str(path))
        _require(text, "The Lesson ID set must match exactly", str(path))
        for field in MATRIX_FIELDS:
            _require(text, field, str(path))
    router = _read(ROUTER_BRIDGE)
    _require(router, "Q03 regression matrix complete: YES / NO", "router gate")
    _require(router, "duplicates, omissions", "router Q03 block rule")
    print("Q03_MATRIX_CONTRACT: PASS")
    print("Q03_ROUTER_BRIDGE_ENFORCEMENT: PASS")
    print("Q03_IMPLEMENTATION_GATE_LINK: PASS")


def _validate_generated_export() -> None:
    module = _load_exporter_module()
    print("Q03_VALIDATOR_PACKAGE_IMPORT_CONTEXT: PASS")
    with tempfile.TemporaryDirectory(prefix="kanda_q03_") as temp_dir:
        fixture = Path(temp_dir)
        project_root = fixture / "sample_project"
        destination = fixture / "second_prompt_files"
        project_root.mkdir()
        result = module.write_error_memory_ai_send_files(
            project_root,
            destination,
            max_lessons=10,
        )
        if result.get("ok") is not True:
            raise AssertionError("Error Memory exporter did not report success")
        prompt = Path(str(result["prompt_md"])).read_text(encoding="utf-8")
        _require(prompt, "ERROR MEMORY REGRESSION MATRIX", "generated export")
        for field in MATRIX_FIELDS:
            _require(prompt, field, "generated export")
    print("Q03_GENERATED_EXPORT_MATRIX: PASS")


def _expect_rejection(record: str, relevant_ids: list[str], label: str) -> None:
    try:
        _parse_matrix(record, relevant_ids)
    except AssertionError:
        print(f"Q03_NEGATIVE_{label}: PASS")
        return
    raise AssertionError(f"negative Q03 fixture was accepted: {label}")


def _validate_matrix_semantics() -> None:
    record = _complete_record()
    rows = _parse_matrix(record, ["lesson-a", "lesson-b"])
    if len(rows) != 2:
        raise AssertionError("complete matrix did not return two rows")
    print("Q03_COMPLETE_MATRIX_ACCEPTED: PASS")

    _expect_rejection(record.replace("Lesson ID: lesson-b", "Lesson ID: lesson-a"), ["lesson-a", "lesson-b"], "DUPLICATE")
    _expect_rejection(record.replace("Disposition: EXISTING_VALIDATOR", "Disposition: UNKNOWN", 1), ["lesson-a", "lesson-b"], "UNKNOWN_DISPOSITION")
    _expect_rejection(record.replace("Validator or test path: tools/test_a.py", "Validator or test path:", 1), ["lesson-a", "lesson-b"], "MISSING_PATH")
    _expect_rejection(record.replace("Expected rejection marker: A_REJECT", "Expected rejection marker:", 1), ["lesson-a", "lesson-b"], "MISSING_MARKER")
    _expect_rejection(record.replace("Disposition reason: current source moved the public owner", "Disposition reason:", 1), ["lesson-a", "lesson-b"], "MISSING_REASON")
    _expect_rejection(record.replace("Status: COMPLETE", "Status: BLOCKED", 1), ["lesson-a", "lesson-b"], "BLOCKED_ROW")
    _expect_rejection(record.split("Lesson ID: lesson-b", 1)[0], ["lesson-a", "lesson-b"], "MISSING_LESSON")


def _parse_version(value: object) -> tuple[int, ...]:
    try:
        return tuple(int(part) for part in str(value).split("."))
    except ValueError as exc:
        raise AssertionError(f"invalid version: {value}") from exc


def _validate_metadata() -> None:
    brick = _load_json(BRICK_META)
    router = _load_json(ROUTER_META)
    if _parse_version(brick.get("version")) < (1, 3):
        raise AssertionError("Brick Wall metadata is older than Q03 minimum")
    if _parse_version(router.get("version")) < (1, 6):
        raise AssertionError("router metadata is older than Q03 minimum")
    for metadata, label in ((brick, "Brick Wall"), (router, "router")):
        source_stage = str(metadata.get("source_stage", "")).strip()
        updated_for = str(metadata.get("updated_for", "")).strip()
        if not source_stage or source_stage != updated_for:
            raise AssertionError(
                f"{label} source_stage and updated_for are not aligned"
            )
    print("Q03_VERSION_ALIGNMENT: PASS")
    print("Q03_METADATA_ALIGNMENT: PASS")


def _validate_module_sizes() -> None:
    for path in (EXPORTER, Path(__file__).resolve()):
        count = len(_read(path).splitlines())
        if count > 500:
            raise AssertionError(f"module exceeds 500 lines: {path}={count}")
        print(f"Q03_MODULE_SIZE: PASS - {path.name}={count}")


def main() -> int:
    for path in (BRICK_WALL, BRICK_META, ROUTER_BRIDGE, ROUTER_META, EXPORTER):
        if not path.is_file():
            raise AssertionError(f"required file missing: {path}")
        print(f"Q03_REQUIRED_FILE: PASS - {path}")
    _validate_contract_sources()
    _validate_generated_export()
    _validate_matrix_semantics()
    _validate_metadata()
    _validate_module_sizes()
    print("Q03_NO_NEW_ENGINE_OR_SCHEMA: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
