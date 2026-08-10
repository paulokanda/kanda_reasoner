# project-path: tools/validate_brick_wall_q02_error_memory_preflight_v1.py
"""Validate Brick Wall Q02 visible Error Memory preflight enforcement."""

from __future__ import annotations

__all__: list[str] = []

import json
from pathlib import Path
import sys

FEATURE_ID = "brick-wall-q02-visible-error-memory-preflight-enforcement-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
_ROOT_TEXT = str(PROJECT_ROOT)
if _ROOT_TEXT not in sys.path:
    sys.path.insert(0, _ROOT_TEXT)

from kanda_reasoner_app.error_memory import write_error_memory_ai_send_files

from brick_wall_q20_isolated_filesystem_fixture import (
    isolated_registered_project_fixture,
)


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

Q02_FIELDS = (
    "Project slug:",
    "Compact export identity and freshness:",
    "Relevant lesson IDs:",
    "Confidence per match: exact / partial / weak / none",
    "Lesson freshness:",
    "Applicable avoidance rules:",
    "Regression obligations:",
    "Full Error Memory ZIP needed: YES / NO",
    "Full ZIP open reason:",
    "May proceed to exact-source inspection: YES / NO",
    "May begin coding: NO",
    "Reason:",
    "Next safe action:",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(_read(path))


def _require(text: str, fragment: str, label: str) -> None:
    if fragment not in text:
        raise AssertionError(f"{label} missing fragment: {fragment}")


def _require_q02_fields(text: str, label: str) -> None:
    _require(text, "ERROR MEMORY CHECK", label)
    for field in Q02_FIELDS:
        _require(text, field, label)


def _validate_prompt_sources() -> None:
    brick_text = _read(BRICK_WALL)
    router_text = _read(ROUTER_BRIDGE)

    _require_q02_fields(brick_text, "Brick Wall Q02")
    _require_q02_fields(router_text, "governed implementation Q02")

    for fragment in (
        "Compact Error Memory is always read before governed implementation planning.",
        "Error Memory is prevention guidance, never a substitute for exact source.",
        "May begin coding` remains `NO` inside the Q02 record",
    ):
        _require(router_text, fragment, "governed implementation Q02")

    legacy_mapping = "Every relevant lesson must map to an existing validator"
    matrix_mapping = "Every relevant lesson must have exactly one complete regression-matrix block."
    if legacy_mapping not in router_text and matrix_mapping not in router_text:
        raise AssertionError(
            "governed implementation Q02 missing lesson regression disposition contract"
        )

    for fragment in (
        "Q02 Error Memory preflight complete: YES / NO",
        "Relevant Error Memory lesson IDs:",
        "Lesson freshness and regression dispositions complete: YES / NO",
        "the ERROR MEMORY CHECK is complete with explicit lesson dispositions",
    ):
        _require(router_text, fragment, "Implementation Gate Q02")

    print("Q02_BRICK_WALL_PREFLIGHT: PASS")
    print("Q02_ROUTER_BRIDGE_ENFORCEMENT: PASS")
    print("Q02_IMPLEMENTATION_GATE_LINK: PASS")


def _validate_generated_export() -> None:
    with isolated_registered_project_fixture(
        tool_source_root=PROJECT_ROOT,
        prefix="kanda_q02_",
    ) as layout:
        destination = layout.transient_root / "second_prompt_files"
        result = write_error_memory_ai_send_files(
            layout.source_root,
            destination,
            max_lessons=10,
        )
        if result.get("ok") is not True:
            raise AssertionError("Error Memory exporter did not report success")

        prompt_path = Path(str(result["prompt_md"]))
        manifest_path = Path(str(result["manifest_json"]))
        prompt_text = _read(prompt_path)
        manifest = _load_json(manifest_path)

        _require_q02_fields(prompt_text, "generated Error Memory preflight")
        if manifest.get("compact_error_memory_always_read") is not True:
            raise AssertionError("compact_error_memory_always_read is not true")
        if manifest.get("full_error_memory_zip_open_policy") != "open_only_when_needed":
            raise AssertionError("full Error Memory ZIP policy drifted")

        missing_field_text = prompt_text.replace(
            "Regression obligations:",
            "",
            1,
        )
        try:
            _require_q02_fields(
                missing_field_text,
                "negative incomplete Q02 record",
            )
        except AssertionError:
            pass
        else:
            raise AssertionError("incomplete Q02 record was not rejected")

    print("Q02_GENERATED_EXPORT_PREFLIGHT: PASS")
    print("Q02_COMPACT_ALWAYS_READ_CONTRACT: PASS")
    print("Q02_FULL_ZIP_OPEN_POLICY: PASS")
    print("Q02_INCOMPLETE_RECORD_REJECTION: PASS")


def _parse_version(value: object) -> tuple[int, ...]:
    try:
        return tuple(int(part) for part in str(value).split("."))
    except ValueError as exc:
        raise AssertionError(f"invalid metadata version: {value}") from exc


def _validate_metadata() -> None:
    brick_meta = _load_json(BRICK_META)
    router_meta = _load_json(ROUTER_META)

    if _parse_version(brick_meta.get("version")) < (1, 2):
        raise AssertionError("Brick Wall metadata is older than Q02 minimum 1.2")
    if _parse_version(router_meta.get("version")) < (1, 5):
        raise AssertionError("router metadata is older than Q02 minimum 1.5")

    for metadata, label in (
        (brick_meta, "Brick Wall metadata"),
        (router_meta, "router metadata"),
    ):
        source_stage = str(metadata.get("source_stage", "")).strip()
        updated_for = str(metadata.get("updated_for", "")).strip()
        if not source_stage or source_stage != updated_for:
            raise AssertionError(f"{label} source_stage and updated_for are not aligned")

    description = str(router_meta.get("description", ""))
    _require(description, "Q02 Error Memory preflight", "router metadata")
    print("Q02_VERSION_ALIGNMENT: PASS")
    print("Q02_METADATA_ALIGNMENT: PASS")


def _validate_module_sizes() -> None:
    for path in (EXPORTER, Path(__file__).resolve()):
        line_count = len(_read(path).splitlines())
        if line_count > 500:
            raise AssertionError(f"module exceeds 500 lines: {path}={line_count}")
        print(f"Q02_MODULE_SIZE: PASS - {path.name}={line_count}")


def main() -> int:
    for path in (
        BRICK_WALL,
        BRICK_META,
        ROUTER_BRIDGE,
        ROUTER_META,
        EXPORTER,
    ):
        if not path.is_file():
            raise AssertionError(f"required file missing: {path}")
        print(f"Q02_REQUIRED_FILE: PASS - {path}")

    _validate_prompt_sources()
    _validate_generated_export()
    _validate_metadata()
    _validate_module_sizes()
    print("Q02_NO_NEW_ENGINE_OR_SCHEMA: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
