"""Validate Brick Wall Q27 control-byte and encoding guards."""
from __future__ import annotations

import argparse
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import re
from tempfile import TemporaryDirectory
from typing import Callable, Sequence

from brick_wall_q27_control_byte_encoding_contract import (
    mutated_record,
    valid_complete_record,
    valid_not_applicable_record,
    validate_powershell_bytes,
    validate_record,
)

__all__: list[str] = []
FEATURE_ID = "brick-wall-q27-control-byte-encoding-guards-enforcement-v1"
PLIB = Path("kanda_prompt_workspace/prompt_library")
BRICK_REL = PLIB / (
    "ACTIVE_PROMPTS/03_governance_freeze_and_handoff/"
    "brick_wall_comprehensive_quality_gate.md"
)
BRIDGE_REL = PLIB / (
    "ACTIVE_PROMPTS/05_patch_delivery_and_validation/"
    "router_bridge_governed_implementation.md"
)
BRICK_META_REL = PLIB / "METADATA/brick_wall_comprehensive_quality_gate.meta.json"
BRIDGE_META_REL = PLIB / "METADATA/router_bridge_governed_implementation.meta.json"
MERGE_REL = Path("scripts/merge_freeze_validation_evidence.py")
Q26_REL = Path(
    "tools/validate_brick_wall_q26_zip_containment_collision_hardening_v1.py"
)
CONTRACT_REL = Path("tools/brick_wall_q27_control_byte_encoding_contract.py")
VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q27_control_byte_encoding_guards_v1.py"
)
BRICK_MARKERS = (
    "### Control-byte and encoding guards (Q27)",
    "CONTROL-BYTE AND ENCODING GUARDS RECORD",
    "UTF-8 no-BOM producer contract",
    "UTF-16LE fixture",
    "proceed to Q28 structured exception provenance YES/NO",
)
BRIDGE_MARKERS = (
    "## Control-byte and encoding guards gate (Q27)",
    "Q27 control-byte and encoding guards record complete: YES / NO",
    "Q28 structured exception provenance record complete: YES / NO",
    "## Control-byte and encoding guards bridge",
)


def _read(path: Path) -> str:
    if not path.is_file():
        raise AssertionError("missing file: " + str(path))
    return path.read_text(encoding="utf-8-sig", errors="strict")


def _load(path: Path) -> dict[str, object]:
    return json.loads(_read(path))


def _gate(label: str, ok: bool, detail: str = "") -> None:
    if not ok:
        raise AssertionError(label + ": FAIL" + (" - " + detail if detail else ""))
    print(label + ": PASS" + (" - " + detail if detail else ""))


def _require(text: str, markers: Sequence[str], label: str) -> None:
    missing = [marker for marker in markers if marker not in text]
    _gate(label, not missing, ", ".join(missing))


def _version(value: object) -> tuple[int, ...]:
    try:
        return tuple(int(item) for item in str(value).split("."))
    except ValueError:
        return ()


def _precode(text: str, minimum: int) -> bool:
    match = re.search(
        r"After Q(\d+), all applicable pre-code items.*?Q01-Q(\d+) complete YES/NO",
        text,
        re.DOTALL,
    )
    return bool(
        match
        and match.group(1) == match.group(2)
        and int(match.group(1)) >= minimum
    )


def _load_merge_module(root: Path):
    path = root / MERGE_REL
    spec = importlib.util.spec_from_file_location("kanda_q27_merge_evidence", path)
    if spec is None or spec.loader is None:
        raise AssertionError("Could not load merge evidence command")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_source(root: Path) -> None:
    brick = _read(root / BRICK_REL)
    bridge = _read(root / BRIDGE_REL)
    brick_meta = _load(root / BRICK_META_REL)
    bridge_meta = _load(root / BRIDGE_META_REL)
    merge = _read(root / MERGE_REL)
    q26 = _read(root / Q26_REL)
    _require(brick, BRICK_MARKERS, "Q27_BRICK_WALL_CONTRACT")
    _require(bridge, BRIDGE_MARKERS, "Q27_ROUTER_BRIDGE_CONTRACT")
    _gate("Q27_BRICK_VERSION", _version(brick_meta.get("version")) >= (3, 7))
    _gate("Q27_BRIDGE_VERSION", _version(bridge_meta.get("version")) >= (4, 1))
    for label, meta in (("brick", brick_meta), ("bridge", bridge_meta)):
        source_stage = str(meta.get("source_stage") or "")
        updated_for = str(meta.get("updated_for") or "")
        _gate(
            "Q27_METADATA_ALIGNMENT",
            bool(source_stage) and source_stage == updated_for,
            label,
        )
    _gate("Q27_PRECODE_PROGRESSION", _precode(brick, 27))
    _gate(
        "Q27_FORWARD_COMPATIBLE_Q28_PROGRESSION",
        "### Structured exception provenance (Q28)" in brick
        and "## Structured exception provenance gate (Q28)" in bridge,
    )
    _require(
        merge,
        (
            "def _decode_evidence_bytes",
            'data.decode("utf-16", errors="strict")',
            'data.decode("utf-8", errors="strict")',
            "FORBIDDEN_CONTROL_CHARACTER",
            "EVIDENCE_ENCODING_INVALID",
        ),
        "Q27_EVIDENCE_READER_CONTRACT",
    )
    _gate(
        "Q26_FORWARD_COMPATIBLE_Q27_PROGRESSION",
        "Q26_FORWARD_COMPATIBLE_Q27_PROGRESSION" in q26,
    )
    for rel in (
        BRICK_REL,
        BRIDGE_REL,
        MERGE_REL,
        Q26_REL,
        CONTRACT_REL,
        VALIDATOR_REL,
    ):
        _gate("Q27_MODULE_SIZE", len(_read(root / rel).splitlines()) <= 500, str(rel))


def _reject_record(label: str, mutate: Callable[[dict[str, object]], None]) -> None:
    record = mutated_record()
    mutate(record)
    try:
        validate_record(record)
    except AssertionError:
        _gate(label, True)
    else:
        _gate(label, False)


def validate_governance_record() -> None:
    validate_record(valid_complete_record())
    _gate("Q27_COMPLETE_RECORD_ACCEPTED", True)
    validate_record(valid_not_applicable_record())
    _gate("Q27_NOT_APPLICABLE_RECORD_ACCEPTED", True)
    tests = (
        ("Q27_NEGATIVE_Q26_BASELINE", lambda r: r.update(q26_decision_complete=False)),
        ("Q27_NEGATIVE_EVIDENCE_READER", lambda r: r.update(evidence_reader="other.py")),
        ("Q27_NEGATIVE_OUTPUT_ENCODING", lambda r: r.update(output_encoding="host default")),
        (
            "Q27_NEGATIVE_LEGACY_ENCODING",
            lambda r: r["legacy_read_encodings"].remove("UTF-16LE BOM"),
        ),
        ("Q27_NEGATIVE_C0_INVENTORY", lambda r: r.update(allowed_c0_codes=[10, 13])),
        (
            "Q27_NEGATIVE_CONTROL_REJECTION",
            lambda r: r.update(forbidden_control_bytes_rejected=False),
        ),
        (
            "Q27_NEGATIVE_INVALID_ENCODING",
            lambda r: r.update(invalid_encoding_rejected=False),
        ),
        (
            "Q27_NEGATIVE_PATH_GENERATION",
            lambda r: r.update(safe_windows_path_generation=False),
        ),
        ("Q27_NEGATIVE_Q28_PROGRESSION", lambda r: r.update(may_proceed_to_q28=False)),
        ("Q27_NEGATIVE_CODING_AUTHORIZATION", lambda r: r.update(may_begin_coding=True)),
        ("Q27_NEGATIVE_SOURCE_WRITE", lambda r: r.update(may_write_source=True)),
    )
    for label, mutate in tests:
        _reject_record(label, mutate)
    record = deepcopy(valid_not_applicable_record())
    record["no_guard_evidence"] = []
    try:
        validate_record(record)
    except AssertionError:
        _gate("Q27_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", True)
    else:
        _gate("Q27_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", False)
    print("Q27_CONTROL_BYTE_ENCODING_GUARDS_REGRESSION_SET: PASS")


def _expect_merge_error(label: str, func: Callable[[], object], code: str) -> None:
    try:
        func()
    except Exception as exc:
        _gate(label, code in str(exc), str(exc))
    else:
        _gate(label, False, "input was accepted")


def validate_runtime(root: Path) -> None:
    module = _load_merge_module(root)
    marker = "VALIDATION OK: q27-fixture\nSTATUS: IN_SYNC\n"
    with TemporaryDirectory(prefix="kanda_q27_encoding_") as temp:
        directory = Path(temp)
        utf8 = directory / "utf8.txt"
        utf8.write_bytes(marker.encode("utf-8"))
        _gate("Q27_UTF8_OUTPUT", module._read_text_file(str(utf8)) == marker)

        utf8_bom = directory / "utf8_bom.txt"
        utf8_bom.write_bytes(b"\xef\xbb\xbf" + marker.encode("utf-8"))
        _gate("Q27_UTF8_BOM_LEGACY_READ", module._read_text_file(str(utf8_bom)) == marker)

        utf16 = directory / "utf16le.txt"
        utf16.write_bytes(b"\xff\xfe" + marker.encode("utf-16le"))
        _gate("Q27_UTF16LE_FIXTURE", module._read_text_file(str(utf16)) == marker)
        print("Q27_BOM_AWARE_LEGACY_READS: PASS")

        invalid = directory / "invalid.txt"
        invalid.write_bytes(b"VALIDATION OK: q27\xff")
        _expect_merge_error(
            "Q27_INVALID_UTF8_REJECTED",
            lambda: module._read_text_file(str(invalid)),
            "EVIDENCE_ENCODING_INVALID",
        )

        vertical_tab = directory / "vertical_tab.txt"
        vertical_tab.write_bytes(b"VALIDATION OK: q27\x0bSTATUS: IN_SYNC")
        _expect_merge_error(
            "Q27_VERTICAL_TAB_REJECTED",
            lambda: module._read_text_file(str(vertical_tab)),
            "FORBIDDEN_CONTROL_CHARACTER",
        )

        nul = directory / "nul.txt"
        nul.write_bytes(b"VALIDATION OK: q27\x00STATUS: IN_SYNC")
        _expect_merge_error(
            "Q27_NUL_REJECTED",
            lambda: module._read_text_file(str(nul)),
            "FORBIDDEN_CONTROL_CHARACTER",
        )

    safe_script = (
        '$ToolsRoot = Join-Path $PROJECT_ROOT "tools"\r\n'
        '$Validator = Join-Path $ToolsRoot "validate_example.py"\r\n'
    ).encode("utf-8")
    validate_powershell_bytes(safe_script)
    _gate("Q27_SAFE_WINDOWS_PATH_GENERATION", True)
    try:
        validate_powershell_bytes(b'$Validator = "tools\x0balidate_example.py"')
    except AssertionError as exc:
        _gate(
            "Q27_POWERSHELL_VERTICAL_TAB_REJECTED",
            "POWERSHELL_FORBIDDEN_CONTROL_BYTE" in str(exc),
        )
    else:
        _gate("Q27_POWERSHELL_VERTICAL_TAB_REJECTED", False)
    try:
        validate_powershell_bytes(b"\xff\xfeI\x00N\x00S\x00T\x00A\x00L\x00L\x00")
    except AssertionError as exc:
        message = str(exc)
        _gate(
            "Q27_POWERSHELL_NON_UTF8_REJECTED",
            "POWERSHELL_ENCODING_INVALID" in message
            or "POWERSHELL_FORBIDDEN_CONTROL_BYTE" in message,
        )
    else:
        _gate("Q27_POWERSHELL_NON_UTF8_REJECTED", False)
    print("Q27_CONTROL_BYTE_REJECTION: PASS")
    print("Q27_RUNTIME_CONTROL_BYTE_ENCODING_GUARDS: PASS")


def run_validation(root: Path) -> None:
    validate_source(root)
    validate_governance_record()
    validate_runtime(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    run_validation(args.project_root.expanduser().resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
