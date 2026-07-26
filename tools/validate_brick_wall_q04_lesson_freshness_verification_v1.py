"""Validate Brick Wall Q04 Error Memory lesson freshness verification."""

from __future__ import annotations

__all__: list[str] = []

import importlib
import json
from pathlib import Path
import sys
import tempfile
from typing import Iterable

FEATURE_ID = "brick-wall-q04-error-memory-lesson-freshness-verification-v1"
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
MODELS = PROJECT_ROOT / "kanda_reasoner_app" / "error_memory" / "models.py"
Q03_VALIDATOR = (
    PROJECT_ROOT
    / "tools"
    / "validate_brick_wall_q03_regression_obligation_matrix_v1.py"
)

FRESHNESS_HEADING = "ERROR MEMORY LESSON FRESHNESS VERIFICATION"
FRESHNESS_FIELDS = (
    "Freshness lesson key:",
    "Lesson status: active / draft / deprecated / superseded",
    "Superseded by:",
    "Referenced file:",
    "File exists: YES / NO / N/A",
    "Referenced symbol:",
    "Symbol exists: YES / NO / N/A",
    "Current public facade:",
    "Current facade verified: YES / NO / N/A",
    "Current box:",
    "Current owner:",
    "Current source fingerprint:",
    "Lesson fingerprint comparison: EXACT / PARTIAL / MISMATCH / UNRESOLVED",
    "Invalidation conditions reviewed:",
    "Invalidation condition triggered: YES / NO / UNRESOLVED",
    "Freshness decision: CURRENT / STALE / PARTIAL / BLOCKED",
    "Freshness evidence:",
    "Freshness status: COMPLETE / BLOCKED",
)
ROW_LABELS = (
    "Lesson status:",
    "Superseded by:",
    "Referenced file:",
    "File exists:",
    "Referenced symbol:",
    "Symbol exists:",
    "Current public facade:",
    "Current facade verified:",
    "Current box:",
    "Current owner:",
    "Current source fingerprint:",
    "Lesson fingerprint comparison:",
    "Invalidation conditions reviewed:",
    "Invalidation condition triggered:",
    "Freshness decision:",
    "Freshness evidence:",
    "Freshness status:",
)
ALLOWED_LESSON_STATUS = {"active", "draft", "deprecated", "superseded"}
ALLOWED_TRISTATE = {"YES", "NO", "N/A"}
ALLOWED_FINGERPRINT = {"EXACT", "PARTIAL", "MISMATCH", "UNRESOLVED"}
ALLOWED_INVALIDATION = {"YES", "NO", "UNRESOLVED"}
ALLOWED_DECISIONS = {"CURRENT", "STALE", "PARTIAL", "BLOCKED"}

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

def _is_not_applicable(value: str) -> bool:
    return value.strip().lower() in {"", "n/a", "na", "none", "null"}

def _freshness_section(record: str) -> str:
    if FRESHNESS_HEADING not in record:
        raise AssertionError("freshness verification heading is missing")
    section = record.split(FRESHNESS_HEADING, 1)[1]
    return section.split("Full Error Memory ZIP needed:", 1)[0]


def _parse_freshness(
    record: str,
    relevant_ids: Iterable[str],
) -> list[dict[str, str]]:
    expected = list(relevant_ids)
    section = _freshness_section(record)
    blocks = section.split("Freshness lesson key:")[1:]
    parsed: list[dict[str, str]] = []

    for raw_block in blocks:
        lines = [line.strip() for line in raw_block.splitlines() if line.strip()]
        if not lines:
            continue
        row: dict[str, str] = {"Freshness lesson key": lines[0]}
        for label in ROW_LABELS:
            matches = [line for line in lines if line.startswith(label)]
            if len(matches) != 1:
                raise AssertionError(
                    f"freshness row field count invalid: {label}"
                )
            row[label[:-1]] = matches[0].split(":", 1)[1].strip()
        parsed.append(row)

    actual_ids = [row["Freshness lesson key"] for row in parsed]
    if sorted(actual_ids) != sorted(expected):
        raise AssertionError(
            "freshness lesson-key set does not match relevant lesson IDs"
        )
    if len(actual_ids) != len(set(actual_ids)):
        raise AssertionError("duplicate freshness lesson key")

    for row in parsed:
        lesson_status = row["Lesson status"]
        file_state = row["File exists"]
        symbol_state = row["Symbol exists"]
        facade_state = row["Current facade verified"]
        fingerprint_state = row["Lesson fingerprint comparison"]
        invalidation_state = row["Invalidation condition triggered"]
        decision = row["Freshness decision"]
        status = row["Freshness status"]

        if lesson_status not in ALLOWED_LESSON_STATUS:
            raise AssertionError("unknown lesson status")
        if file_state not in ALLOWED_TRISTATE:
            raise AssertionError("unknown file-existence state")
        if symbol_state not in ALLOWED_TRISTATE:
            raise AssertionError("unknown symbol-existence state")
        if facade_state not in ALLOWED_TRISTATE:
            raise AssertionError("unknown facade-verification state")
        if fingerprint_state not in ALLOWED_FINGERPRINT:
            raise AssertionError("unknown fingerprint comparison")
        if invalidation_state not in ALLOWED_INVALIDATION:
            raise AssertionError("unknown invalidation state")
        if decision not in ALLOWED_DECISIONS:
            raise AssertionError("unknown freshness decision")
        if status != "COMPLETE" or decision == "BLOCKED":
            raise AssertionError("freshness row is blocked or incomplete")

        if not row["Current box"] or not row["Current owner"]:
            raise AssertionError("current box and owner are required")
        if not row["Current source fingerprint"]:
            raise AssertionError("current source fingerprint is required")
        if not row["Invalidation conditions reviewed"]:
            raise AssertionError("invalidation review is required")
        if not row["Freshness evidence"]:
            raise AssertionError("freshness evidence is required")

        reference_pairs = (
            (row["Referenced file"], file_state, "file"),
            (row["Referenced symbol"], symbol_state, "symbol"),
            (row["Current public facade"], facade_state, "facade"),
        )
        for reference, state, label in reference_pairs:
            if _is_not_applicable(reference) and state != "N/A":
                raise AssertionError(f"{label} N/A evidence is inconsistent")
            if not _is_not_applicable(reference) and state == "N/A":
                raise AssertionError(f"{label} existence evidence is missing")

        superseded_by = row["Superseded by"]
        if lesson_status == "active" and not _is_not_applicable(superseded_by):
            raise AssertionError("active lesson has superseded_by")
        if lesson_status == "superseded" and _is_not_applicable(superseded_by):
            raise AssertionError("superseded lesson lacks superseded_by")
        if lesson_status != "active" and decision == "CURRENT":
            raise AssertionError("inactive lesson cannot be current")

        if decision == "CURRENT":
            if file_state == "NO" or symbol_state == "NO" or facade_state == "NO":
                raise AssertionError("current lesson has missing current source")
            if fingerprint_state in {"MISMATCH", "UNRESOLVED"}:
                raise AssertionError("current lesson fingerprint is not current")
            if invalidation_state != "NO":
                raise AssertionError("current lesson has triggered invalidation")
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
Freshness: stale
Disposition: NOT_APPLICABLE
Protection owner: Error Memory
Validator or test path:
Expected success marker:
Expected rejection marker:
Disposition reason: lesson was superseded by current source
Status: COMPLETE
ERROR MEMORY LESSON FRESHNESS VERIFICATION
Freshness lesson key: lesson-a
Lesson status: active
Superseded by: N/A
Referenced file: kanda_reasoner_app/error_memory/exporter.py
File exists: YES
Referenced symbol: _prompt_text
Symbol exists: YES
Current public facade: write_error_memory_ai_send_files
Current facade verified: YES
Current box: kanda_reasoner_app/error_memory
Current owner: exporter.py
Current source fingerprint: sha256:current-a
Lesson fingerprint comparison: EXACT
Invalidation conditions reviewed: owner move, file removal, symbol removal
Invalidation condition triggered: NO
Freshness decision: CURRENT
Freshness evidence: exact file, symbol, facade, owner, and validator inspected
Freshness status: COMPLETE
Freshness lesson key: lesson-b
Lesson status: superseded
Superseded by: lesson-c
Referenced file: retired.py
File exists: NO
Referenced symbol: N/A
Symbol exists: N/A
Current public facade: N/A
Current facade verified: N/A
Current box: kanda_reasoner_app/error_memory
Current owner: exporter.py
Current source fingerprint: sha256:current-b
Lesson fingerprint comparison: MISMATCH
Invalidation conditions reviewed: retired file and supersession
Invalidation condition triggered: YES
Freshness decision: STALE
Freshness evidence: saved status and current source prove retirement
Freshness status: COMPLETE
Full Error Memory ZIP needed: NO
"""


def _validate_contract_sources() -> None:
    for path in (BRICK_WALL, ROUTER_BRIDGE, EXPORTER):
        text = _read(path)
        _require(text, FRESHNESS_HEADING, str(path))
        _require(
            text,
            "The freshness lesson-key set must match exactly",
            str(path),
        )
        for field in FRESHNESS_FIELDS:
            _require(text, field, str(path))
    router = _read(ROUTER_BRIDGE)
    _require(
        router,
        "Q04 lesson freshness verification complete: YES / NO",
        "router gate",
    )
    _require(router, "blocks Q04", "router Q04 block rule")
    print("Q04_FRESHNESS_CONTRACT: PASS")
    print("Q04_ROUTER_BRIDGE_ENFORCEMENT: PASS")
    print("Q04_IMPLEMENTATION_GATE_LINK: PASS")


def _validate_compact_lesson_inputs() -> None:
    text = _read(MODELS)
    for field in (
        '"status": lesson.get("status", "")',
        '"exception": dict(lesson.get("exception", {}) or {})',
        '"fingerprint": dict(lesson.get("fingerprint", {}) or {})',
        '"regression_check": dict(lesson.get("regression_check", {}) or {})',
        '"superseded_by": lesson.get("superseded_by", "")',
    ):
        _require(text, field, "compact lesson freshness inputs")
    print("Q04_COMPACT_LESSON_FRESHNESS_INPUTS: PASS")


def _validate_generated_export() -> None:
    module = _load_exporter_module()
    with tempfile.TemporaryDirectory(prefix="kanda_q04_") as temp_dir:
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
        _require(prompt, FRESHNESS_HEADING, "generated export")
        for field in FRESHNESS_FIELDS:
            _require(prompt, field, "generated export")
    print("Q04_GENERATED_EXPORT_FRESHNESS: PASS")


def _expect_rejection(
    record: str,
    relevant_ids: list[str],
    label: str,
) -> None:
    try:
        _parse_freshness(record, relevant_ids)
    except AssertionError:
        print(f"Q04_NEGATIVE_{label}: PASS")
        return
    raise AssertionError(f"negative Q04 fixture was accepted: {label}")


def _validate_freshness_semantics() -> None:
    record = _complete_record()
    rows = _parse_freshness(record, ["lesson-a", "lesson-b"])
    if len(rows) != 2:
        raise AssertionError("complete freshness record did not return two rows")
    print("Q04_COMPLETE_FRESHNESS_ACCEPTED: PASS")

    _expect_rejection(
        record.replace(
            "Freshness lesson key: lesson-b",
            "Freshness lesson key: lesson-a",
        ),
        ["lesson-a", "lesson-b"],
        "DUPLICATE",
    )
    _expect_rejection(
        record.replace("Lesson status: active", "Lesson status: unknown", 1),
        ["lesson-a", "lesson-b"],
        "UNKNOWN_STATUS",
    )
    _expect_rejection(
        record.replace("Superseded by: N/A", "Superseded by: lesson-z", 1),
        ["lesson-a", "lesson-b"],
        "ACTIVE_SUPERSEDED",
    )
    _expect_rejection(
        record.replace("File exists: YES", "File exists: NO", 1),
        ["lesson-a", "lesson-b"],
        "CURRENT_FILE_MISSING",
    )
    _expect_rejection(
        record.replace(
            "Lesson fingerprint comparison: EXACT",
            "Lesson fingerprint comparison: UNRESOLVED",
            1,
        ),
        ["lesson-a", "lesson-b"],
        "CURRENT_FINGERPRINT_UNRESOLVED",
    )
    _expect_rejection(
        record.replace(
            "Invalidation condition triggered: NO",
            "Invalidation condition triggered: YES",
            1,
        ),
        ["lesson-a", "lesson-b"],
        "CURRENT_INVALIDATED",
    )
    _expect_rejection(
        record.replace("Current owner: exporter.py", "Current owner:", 1),
        ["lesson-a", "lesson-b"],
        "MISSING_OWNER",
    )
    _expect_rejection(
        record.replace(
            "Freshness evidence: exact file, symbol, facade, owner, and validator inspected",
            "Freshness evidence:",
            1,
        ),
        ["lesson-a", "lesson-b"],
        "MISSING_EVIDENCE",
    )
    _expect_rejection(
        record.replace(
            "Freshness status: COMPLETE",
            "Freshness status: BLOCKED",
            1,
        ),
        ["lesson-a", "lesson-b"],
        "BLOCKED_ROW",
    )
    _expect_rejection(
        record.split("Freshness lesson key: lesson-b", 1)[0]
        + "Full Error Memory ZIP needed: NO\n",
        ["lesson-a", "lesson-b"],
        "MISSING_LESSON",
    )


def _parse_version(value: object) -> tuple[int, ...]:
    try:
        return tuple(int(part) for part in str(value).split("."))
    except ValueError as exc:
        raise AssertionError(f"invalid version: {value}") from exc


def _validate_metadata() -> None:
    brick = _load_json(BRICK_META)
    router = _load_json(ROUTER_META)
    if _parse_version(brick.get("version")) < (1, 4):
        raise AssertionError("Brick Wall metadata is older than Q04 minimum")
    if _parse_version(router.get("version")) < (1, 7):
        raise AssertionError("router metadata is older than Q04 minimum")
    for metadata, label in ((brick, "Brick Wall"), (router, "router")):
        source_stage = str(metadata.get("source_stage", "")).strip()
        updated_for = str(metadata.get("updated_for", "")).strip()
        if not source_stage or source_stage != updated_for:
            raise AssertionError(f"{label} provenance is missing or misaligned")
        _require(str(metadata.get("description", "")), "Q04", label)
    print("Q04_METADATA_ALIGNMENT: PASS")


def _validate_module_sizes() -> None:
    for path in (
        EXPORTER,
        BRICK_WALL,
        ROUTER_BRIDGE,
        Q03_VALIDATOR,
        Path(__file__).resolve(),
    ):
        count = len(_read(path).splitlines())
        if count > 500:
            raise AssertionError(f"module exceeds 500 lines: {path}={count}")
        print(f"Q04_MODULE_SIZE: PASS - {path.name}={count}")


def main() -> int:
    for path in (
        BRICK_WALL,
        BRICK_META,
        ROUTER_BRIDGE,
        ROUTER_META,
        EXPORTER,
        MODELS,
        Q03_VALIDATOR,
    ):
        if not path.is_file():
            raise AssertionError(f"required file missing: {path}")
        print(f"Q04_REQUIRED_FILE: PASS - {path}")
    _validate_contract_sources()
    _validate_compact_lesson_inputs()
    _validate_generated_export()
    _validate_freshness_semantics()
    _validate_metadata()
    _validate_module_sizes()
    print("Q04_NO_NEW_ENGINE_OR_SCHEMA: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
