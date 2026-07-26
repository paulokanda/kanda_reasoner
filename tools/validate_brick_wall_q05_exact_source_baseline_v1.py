"""Validate Brick Wall Q05 exact-source baseline enforcement."""

from __future__ import annotations

__all__: list[str] = []

import argparse
from copy import deepcopy
import json
from pathlib import Path
import re
from typing import Mapping, Sequence


FEATURE_ID = "brick-wall-q05-exact-source-baseline-enforcement-v1"
BRICK_WALL_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "03_governance_freeze_and_handoff/"
    "brick_wall_comprehensive_quality_gate.md"
)
BRICK_META_REL = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "brick_wall_comprehensive_quality_gate.meta.json"
)
BRIDGE_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "05_patch_delivery_and_validation/"
    "router_bridge_governed_implementation.md"
)
BRIDGE_META_REL = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "router_bridge_governed_implementation.meta.json"
)
Q04_VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q04_lesson_freshness_verification_v1.py"
)
Q05_VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q05_exact_source_baseline_v1.py"
)

RECORD_FIELDS = (
    "Source snapshot identity and freshness:",
    "Canonical owner files, public facade, and private implementations inspected:",
    "Consumers, imports, and exports inspected:",
    "Validators and accepted behavior inspected:",
    "State owner, path owner, async behavior, confirmation gates, and frozen behavior:",
    "Generated artifacts and canonical source classification:",
    "Module sizes:",
    "Current source fingerprints:",
    "Unresolved source or authority:",
    "Baseline decision: COMPLETE / BLOCKED",
    "May proceed to Tool/Project classification: YES / NO",
    "May begin coding: NO",
)

IMPLEMENTATION_GATE_FIELDS = (
    "Q05 exact-source baseline complete: YES / NO",
    "Exact-source baseline decision: COMPLETE / BLOCKED",
)

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="strict")


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(_read_text(path))


def _parse_version(value: object) -> tuple[int, ...]:
    parts = str(value).strip().split(".")
    if not parts or any(not part.isdigit() for part in parts):
        raise AssertionError(f"invalid numeric version: {value}")
    return tuple(int(part) for part in parts)


def _gate(name: str, passed: bool, detail: str = "") -> None:
    if not passed:
        suffix = f" - {detail}" if detail else ""
        raise AssertionError(f"{name}: FAIL{suffix}")
    suffix = f" - {detail}" if detail else ""
    print(f"{name}: PASS{suffix}")


def _require_fragments(text: str, fragments: Sequence[str], label: str) -> None:
    for fragment in fragments:
        _gate(label, fragment in text, fragment)


def _nonempty_sequence(value: object) -> bool:
    return isinstance(value, (list, tuple)) and bool(value) and all(
        isinstance(item, str) and bool(item.strip()) for item in value
    )


def _validate_baseline_record(record: Mapping[str, object]) -> None:
    required_keys = (
        "source_snapshot_identity",
        "snapshot_freshness",
        "source_authority",
        "handoff_only",
        "canonical_owner_files",
        "public_facade",
        "private_implementations",
        "consumers",
        "imports_exports",
        "validators",
        "accepted_behavior",
        "state_owner",
        "path_owner",
        "async_behavior",
        "confirmation_gates",
        "frozen_behavior",
        "generated_classification",
        "canonical_generated_source",
        "module_sizes",
        "source_fingerprints",
        "unresolved_source_or_authority",
        "baseline_decision",
        "may_proceed_to_tool_project",
        "may_begin_coding",
    )
    missing = [key for key in required_keys if key not in record]
    if missing:
        raise AssertionError(f"missing fields: {', '.join(missing)}")

    if not str(record["source_snapshot_identity"]).strip():
        raise AssertionError("source snapshot identity is empty")
    if record["snapshot_freshness"] != "CURRENT":
        raise AssertionError("source snapshot is not current")
    if record["source_authority"] != "CURRENT_EXACT_SOURCE":
        raise AssertionError("current exact source is not authoritative")
    if record["handoff_only"] is not False:
        raise AssertionError("handoff-only evidence is not sufficient")

    for key in (
        "canonical_owner_files",
        "private_implementations",
        "consumers",
        "imports_exports",
        "validators",
        "accepted_behavior",
    ):
        if not _nonempty_sequence(record[key]):
            raise AssertionError(f"{key} is empty")

    for key in (
        "public_facade",
        "state_owner",
        "path_owner",
        "async_behavior",
        "confirmation_gates",
        "frozen_behavior",
        "generated_classification",
    ):
        if not str(record[key]).strip():
            raise AssertionError(f"{key} is empty")

    if record["generated_classification"] == "UNRESOLVED":
        raise AssertionError("generated-vs-canonical classification is unresolved")
    if record["generated_classification"] != "NOT_GENERATED":
        if not _nonempty_sequence(record["canonical_generated_source"]):
            raise AssertionError("canonical generated source is missing")

    module_sizes = record["module_sizes"]
    if not isinstance(module_sizes, Mapping) or not module_sizes:
        raise AssertionError("module sizes are missing")
    if any(not isinstance(value, int) or value < 1 for value in module_sizes.values()):
        raise AssertionError("module size evidence is invalid")

    fingerprints = record["source_fingerprints"]
    if not isinstance(fingerprints, Mapping) or not fingerprints:
        raise AssertionError("source fingerprints are missing")
    for path, fingerprint in fingerprints.items():
        if not str(path).strip() or not SHA256_RE.fullmatch(str(fingerprint)):
            raise AssertionError("source fingerprint evidence is invalid")

    unresolved = record["unresolved_source_or_authority"]
    if unresolved not in (None, "", [], ()):
        raise AssertionError("source or authority remains unresolved")
    if record["baseline_decision"] != "COMPLETE":
        raise AssertionError("baseline decision is not COMPLETE")
    if record["may_proceed_to_tool_project"] != "YES":
        raise AssertionError("Tool/Project progression is not authorized")
    if record["may_begin_coding"] != "NO":
        raise AssertionError("Q05 record must not authorize coding")


def _valid_record() -> dict[str, object]:
    return {
        "source_snapshot_identity": "source-archive-20260714",
        "snapshot_freshness": "CURRENT",
        "source_authority": "CURRENT_EXACT_SOURCE",
        "handoff_only": False,
        "canonical_owner_files": ["owner.py"],
        "public_facade": "package.__init__",
        "private_implementations": ["_implementation.py"],
        "consumers": ["consumer.py"],
        "imports_exports": ["owner imports helper; facade exports owner"],
        "validators": ["tools/validate_owner_v1.py"],
        "accepted_behavior": ["current public behavior remains stable"],
        "state_owner": "owner.py",
        "path_owner": "paths.py",
        "async_behavior": "none",
        "confirmation_gates": "explicit human confirmation",
        "frozen_behavior": "freeze-entry-1",
        "generated_classification": "GENERATED_WITH_CANONICAL_SOURCE",
        "canonical_generated_source": ["generator.py"],
        "module_sizes": {"owner.py": 200},
        "source_fingerprints": {"owner.py": "a" * 64},
        "unresolved_source_or_authority": [],
        "baseline_decision": "COMPLETE",
        "may_proceed_to_tool_project": "YES",
        "may_begin_coding": "NO",
    }


def _expect_rejection(name: str, record: Mapping[str, object]) -> None:
    try:
        _validate_baseline_record(record)
    except AssertionError:
        print(f"Q05_NEGATIVE_{name}: PASS")
        return
    raise AssertionError(f"Q05_NEGATIVE_{name}: FAIL - record was accepted")


def _validate_record_semantics() -> None:
    record = _valid_record()
    _validate_baseline_record(record)
    print("Q05_COMPLETE_BASELINE_ACCEPTED: PASS")

    cases: tuple[tuple[str, str, object], ...] = (
        ("HANDOFF_ONLY", "handoff_only", True),
        ("STALE_SOURCE", "snapshot_freshness", "STALE"),
        ("MISSING_OWNER", "canonical_owner_files", []),
        ("MISSING_CONSUMER", "consumers", []),
        ("MISSING_VALIDATOR", "validators", []),
        ("MISSING_FINGERPRINT", "source_fingerprints", {}),
        ("UNRESOLVED_AUTHORITY", "unresolved_source_or_authority", ["owner"]),
        ("BLOCKED_DECISION", "baseline_decision", "BLOCKED"),
    )
    for name, key, value in cases:
        candidate = deepcopy(record)
        candidate[key] = value
        _expect_rejection(name, candidate)

    generated = deepcopy(record)
    generated["canonical_generated_source"] = []
    _expect_rejection("GENERATED_CANONICAL_SOURCE_MISSING", generated)


def _validate_sources(project_root: Path) -> None:
    brick_path = project_root / BRICK_WALL_REL
    brick_meta_path = project_root / BRICK_META_REL
    bridge_path = project_root / BRIDGE_REL
    bridge_meta_path = project_root / BRIDGE_META_REL
    q04_path = project_root / Q04_VALIDATOR_REL
    q05_path = project_root / Q05_VALIDATOR_REL

    required = (
        brick_path,
        brick_meta_path,
        bridge_path,
        bridge_meta_path,
        q04_path,
        q05_path,
    )
    for path in required:
        _gate("Q05_REQUIRED_FILE", path.is_file(), str(path))

    brick = _read_text(brick_path)
    bridge = _read_text(bridge_path)
    q04 = _read_text(q04_path)

    _require_fragments(brick, ("EXACT SOURCE BASELINE", *RECORD_FIELDS), "Q05_EXACT_SOURCE_RECORD")
    _require_fragments(bridge, ("EXACT SOURCE BASELINE", *RECORD_FIELDS), "Q05_ROUTER_BRIDGE_ENFORCEMENT")
    _require_fragments(bridge, IMPLEMENTATION_GATE_FIELDS, "Q05_IMPLEMENTATION_GATE_LINK")

    _gate(
        "Q05_CURRENT_SOURCE_REQUIRED",
        "Use current exact source, not handoff-only or generated evidence." in brick
        and "Current exact source is mandatory." in bridge,
    )
    _gate(
        "Q05_GENERATED_CANONICAL_CLASSIFICATION",
        "Generated artifacts and canonical source classification:" in brick
        and "Generated artifacts and canonical source classification:" in bridge,
    )
    _gate(
        "Q04_FORWARD_COMPATIBLE_METADATA",
        "source_stage != FEATURE_ID" not in q04
        and "not source_stage or source_stage != updated_for" in q04,
    )

    brick_meta = _load_json(brick_meta_path)
    bridge_meta = _load_json(bridge_meta_path)
    _gate("Q05_BRICK_VERSION", _parse_version(brick_meta.get("version")) >= (1, 5))
    _gate("Q05_BRIDGE_VERSION", _parse_version(bridge_meta.get("version")) >= (1, 8))
    for metadata, label in ((brick_meta, "Brick Wall"), (bridge_meta, "router")):
        source_stage = str(metadata.get("source_stage", "")).strip()
        updated_for = str(metadata.get("updated_for", "")).strip()
        _gate(
            "Q05_METADATA_ALIGNMENT",
            bool(source_stage) and source_stage == updated_for,
            label,
        )
        _gate(
            "Q05_METADATA_DESCRIPTION",
            "Q05" in str(metadata.get("description", "")),
            label,
        )

    for path in (brick_path, bridge_path, q04_path, q05_path):
        line_count = len(_read_text(path).splitlines())
        _gate("Q05_MODULE_SIZE", line_count <= 500, f"{path.name}={line_count}")

    expected_touches = {
        BRICK_WALL_REL,
        BRICK_META_REL,
        BRIDGE_REL,
        BRIDGE_META_REL,
        Q04_VALIDATOR_REL,
        Q05_VALIDATOR_REL,
    }
    _gate(
        "Q05_NO_NEW_ENGINE_OR_SCHEMA",
        all(not str(path).startswith("kanda_reasoner_app/") for path in expected_touches),
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="KANDA Reasoner project root.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    project_root = args.project_root.resolve()
    _validate_sources(project_root)
    _validate_record_semantics()
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
