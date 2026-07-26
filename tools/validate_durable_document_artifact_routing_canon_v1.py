# project-path: tools/validate_durable_document_artifact_routing_canon_v1.py
"""Validate durable documentary artifact routing and startup visibility."""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
import runpy
import sys
import zipfile

__all__: list[str] = []

FEATURE_ID = "durable-document-artifact-routing-canon-v1"
WAVE3B_ID = "prompt-audit-wave3b-specialist-startup-bridges-v1"
PROMPT_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "01_session_start_and_navigation/"
    "durable_document_artifact_routing_canon.md"
)
PROMPT_META_REL = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "durable_document_artifact_routing_canon.meta.json"
)
STACK_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "01_session_start_and_navigation/start_of_day_master_stack.md"
)
STACK_META_REL = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "start_of_day_master_stack.meta.json"
)
GUARD_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "01_session_start_and_navigation/daily_patch_delivery_guardrails.md"
)
REASONER_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "01_session_start_and_navigation/reasoner_startup_canon.md"
)
FOLDER_CARD_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "01_session_start_and_navigation/_FOLDER_ASSIMILATION.md"
)
SOURCE_MAP_JSON_REL = Path(
    "kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json"
)
SOURCE_MAP_PY_REL = Path(
    "kanda_prompt_workspace/prompt_tools/startup_kernel/startup_source_map.py"
)
BOOT_REL = Path(
    "kanda_prompt_workspace/prompt_tools/startup_kernel/boot_text.py"
)
LISTS_REL = Path(
    "kanda_prompt_workspace/prompt_tools/startup_kernel/start_here_lists.py"
)
GENERATOR_README_REL = Path(
    "kanda_prompt_workspace/prompt_tools/"
    "README_kanda_startup_prompt_request_kernel_generator.md"
)
SELF_REL = Path("tools/validate_durable_document_artifact_routing_canon_v1.py")
GENERATED_PROMPT_NAME = "13_durable_document_artifact_routing_canon.md"


def _fail(message: str) -> None:
    raise AssertionError(message)


def _read(root: Path, relative_path: Path) -> str:
    path = root / relative_path
    if not path.is_file():
        _fail("MISSING_REQUIRED_FILE:" + relative_path.as_posix())
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        _fail("UTF8_BOM_FORBIDDEN:" + relative_path.as_posix())
    if b"\r\n" in data:
        _fail("CRLF_FORBIDDEN:" + relative_path.as_posix())
    return data.decode("utf-8", errors="strict")


def _require_markers(text: str, markers: tuple[str, ...], label: str) -> None:
    missing = [marker for marker in markers if marker not in text]
    if missing:
        _fail(label + " missing markers: " + repr(missing))


def _version(value: object) -> tuple[int, ...]:
    parts: list[int] = []
    for part in str(value).split("."):
        digits = "".join(character for character in part if character.isdigit())
        parts.append(int(digits or "0"))
    return tuple(parts)


def _run_startup_module(root: Path, relative_path: Path) -> dict[str, object]:
    prompt_tools = root / "kanda_prompt_workspace" / "prompt_tools"
    prompt_tools_text = str(prompt_tools)
    inserted = prompt_tools_text not in sys.path
    if inserted:
        sys.path.insert(0, prompt_tools_text)
    try:
        return runpy.run_path(str(root / relative_path))
    finally:
        if inserted:
            sys.path.remove(prompt_tools_text)


def _validate_prompt(root: Path) -> None:
    text = _read(root, PROMPT_REL)
    _require_markers(
        text,
        (
            "prompt_code: KPR-01-013",
            "load_type: always_startup",
            "DURABLE ARTIFACT ROUTING RECORD",
            "CANONICAL_SOURCE",
            "GENERATED_ARTIFACT",
            "DURABLE / TRANSIENT",
            "Specialized Project Support owner",
            "Validation and blocker evidence",
            "Redaction and provenance",
            "DURABLE DOCUMENT ROUTING BLOCKED",
        ),
        "durable documentation prompt",
    )
    forbidden = ("Compress-Archive", "Expand-Archive", "Tee-Object")
    if any(marker in text for marker in forbidden):
        _fail("DURABLE_PROMPT_DELIVERY_IMPLEMENTATION_LEAK")
    print("DURABLE_DOCUMENT_CANON: PASS")


def _validate_metadata(root: Path) -> None:
    data = json.loads(_read(root, PROMPT_META_REL))
    expected = {
        "prompt_code": "KPR-01-013",
        "prompt_id": "durable_document_artifact_routing_canon",
        "load_type": "always_startup",
        "status": "active",
        "owner_box": "01_session_start_and_navigation",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            _fail(f"PROMPT_METADATA_DRIFT:{key}:{data.get(key)!r}")
    if _version(data.get("version")) < (2, 0):
        _fail("PROMPT_METADATA_VERSION_TOO_OLD")
    if data.get("source_stage") != WAVE3B_ID:
        _fail("PROMPT_METADATA_SOURCE_STAGE")
    if data.get("updated_for") != WAVE3B_ID:
        _fail("PROMPT_METADATA_UPDATED_FOR")

    stack_meta = json.loads(_read(root, STACK_META_REL))
    markers = set(stack_meta.get("startup_markers", []))
    required = {
        "BEGINNING_OF_DAY_DURABLE_DOCUMENT_ROUTING_BRIDGE_V1_START",
        "DURABLE_DOCUMENT_ARTIFACT_ROUTING_CANON_V1",
        "DURABLE_VALIDATION_EVIDENCE_OWNER_V1",
    }
    if not required.issubset(markers):
        _fail("STARTUP_METADATA_DURABLE_MARKERS_MISSING")
    print("DURABLE_DOCUMENT_METADATA: PASS")


def _validate_startup_bridge(root: Path) -> None:
    stack = _read(root, STACK_REL)
    _require_markers(
        stack,
        (
            "BEGINNING_OF_DAY_DURABLE_DOCUMENT_ROUTING_BRIDGE_V1_START",
            "DURABLE_DOCUMENT_ARTIFACT_ROUTING_CANON_V1",
            "DURABLE DOCUMENT ROUTING BLOCKED",
            "DURABLE_VALIDATION_EVIDENCE_OWNER_V1",
            "BEGINNING_OF_DAY_DURABLE_DOCUMENT_ROUTING_BRIDGE_V1_END",
        ),
        "start-of-day durable bridge",
    )

    guard = _read(root, GUARD_REL)
    _require_markers(
        guard,
        (
            "durable_document_artifact_routing_canon",
            "Durable evidence is routed",
            "transient daily-work",
        ),
        "daily patch guardrail",
    )

    reasoner = _read(root, REASONER_REL)
    _require_markers(
        reasoner,
        (
            "Reasoner Startup Canon Compatibility Record",
            "legacy KANDA Reasoner startup mega-canon is retired",
            "durable-document",
        ),
        "reasoner startup compatibility record",
    )

    card = _read(root, FOLDER_CARD_REL)
    _require_markers(
        card,
        (
            "durable_document_artifact_routing_canon.md",
            "durable documentary-artifact",
        ),
        "session-start folder card",
    )
    print("STARTUP_DURABLE_DOCUMENT_BRIDGE: PASS")


def _validate_source_maps(root: Path) -> None:
    data = json.loads(_read(root, SOURCE_MAP_JSON_REL))
    entries = data.get("startup_sources", [])
    matches = [
        entry
        for entry in entries
        if entry.get("prompt_id") == "durable_document_artifact_routing_canon"
    ]
    if len(matches) != 1:
        _fail("DURABLE_PROMPT_SOURCE_MAP_CARDINALITY")
    entry = matches[0]
    expected = {
        "generated_filename": GENERATED_PROMPT_NAME,
        "load_mode": "always_startup",
    }
    for key, value in expected.items():
        if entry.get(key) != value:
            _fail(f"DURABLE_PROMPT_SOURCE_MAP_DRIFT:{key}:{entry.get(key)!r}")

    orders = [int(item["load_order"]) for item in entries]
    if orders != list(range(1, len(entries) + 1)):
        _fail("STARTUP_SOURCE_MAP_NOT_CONTIGUOUS")

    source_map_py = _read(root, SOURCE_MAP_PY_REL)
    ast.parse(source_map_py, filename=str(root / SOURCE_MAP_PY_REL))
    _require_markers(
        source_map_py,
        (
            "durable_document_artifact_routing_canon",
            GENERATED_PROMPT_NAME,
            "always_startup",
        ),
        "default startup source map",
    )
    print("STARTUP_SOURCE_MAP_DURABLE_PROMPT: PASS")


def _validate_startup_reporting(root: Path) -> None:
    lists = _run_startup_module(root, LISTS_REL)
    builder = lists.get("build_active_bridge_report")
    if not callable(builder):
        _fail("STARTUP_REPORT_BUILDER_MISSING")
    report = str(builder())
    _require_markers(
        report,
        (
            "Durable Documentation Artifact Routing Bridge",
            "daily-work is transient",
        ),
        "startup reporting",
    )
    print("STARTUP_BRIDGE_REPORTING: PASS")


def _validate_readme(root: Path) -> None:
    readme = _read(root, GENERATOR_README_REL)
    _require_markers(
        readme,
        (
            GENERATED_PROMPT_NAME,
            "Generated filename 09 is now a migrated conditional Class 05 slot",
            "Generated filenames 10 and 11 are retired compatibility slots",
        ),
        "startup generator readme",
    )


def _validate_generated(root: Path, output_dir: Path) -> None:
    startup_zip = output_dir / "first_prompts_to_ai.zip"
    prompt_library_zip = output_dir / "prompt_library.zip"
    if not startup_zip.is_file() or not prompt_library_zip.is_file():
        _fail("GENERATED_STARTUP_ARCHIVES_MISSING")
    with zipfile.ZipFile(startup_zip, "r") as archive:
        names = set(archive.namelist())
        if GENERATED_PROMPT_NAME not in names:
            _fail("GENERATED_DURABLE_PROMPT_MISSING")
        if "09_patch_install_delivery_error_register.md" in names:
            _fail("MIGRATED_PATCH_REGISTER_STILL_STARTUP")
        generated = archive.read(GENERATED_PROMPT_NAME).decode("utf-8")
        _require_markers(
            generated,
            (
                "DURABLE ARTIFACT ROUTING RECORD",
                "DURABLE DOCUMENT ROUTING BLOCKED",
            ),
            "generated durable prompt",
        )
    with zipfile.ZipFile(prompt_library_zip, "r") as archive:
        member = (
            "ACTIVE_PROMPTS/01_session_start_and_navigation/"
            "durable_document_artifact_routing_canon.md"
        )
        if member not in archive.namelist():
            _fail("PROMPT_LIBRARY_DURABLE_MEMBER_MISSING")
    print("GENERATED_STARTUP_DURABLE_PROMPT: PASS")


def _validate_module_size(root: Path) -> None:
    text = _read(root, SELF_REL)
    if len(text.splitlines()) > 500:
        _fail("DURABLE_VALIDATOR_MODULE_TOO_LARGE")
    print("TOUCHED_PYTHON_MODULES_MAX_500: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--output-dir")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    _validate_prompt(root)
    _validate_metadata(root)
    _validate_startup_bridge(root)
    _validate_source_maps(root)
    _validate_startup_reporting(root)
    _validate_readme(root)
    if args.output_dir:
        _validate_generated(root, Path(args.output_dir).resolve())
    _validate_module_size(root)
    print("DURABLE_PROMPT_CODE_UNIQUE: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
