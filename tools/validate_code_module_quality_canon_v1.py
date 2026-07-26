# project-path: tools/validate_code_module_quality_canon_v1.py
"""Validate canonical PEP 8, SOLID, and DRY module-size precedence."""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
import runpy
import sys
import zipfile

__all__ = [
    "main",
]


FEATURE_ID = "code-module-quality-canon-v1"
STARTUP_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "01_session_start_and_navigation/start_of_day_master_stack.md"
)
STARTUP_MIRROR_REL = Path(
    "prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/"
    "start_of_day_master_stack.md"
)
REASONER_STARTUP_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "01_session_start_and_navigation/reasoner_startup_canon.md"
)
ROUTER_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "05_patch_delivery_and_validation/router_bridge_governed_implementation.md"
)
PROTOCOL_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "06_refactor_and_architecture_hardening/large_module_refactor_protocol.md"
)
STARTUP_META_REL = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "start_of_day_master_stack.meta.json"
)
ROUTER_META_REL = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "router_bridge_governed_implementation.meta.json"
)
PROTOCOL_META_REL = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "large_module_refactor_protocol.meta.json"
)
BOOT_REL = Path("kanda_prompt_workspace/prompt_tools/startup_kernel/boot_text.py")
LISTS_REL = Path(
    "kanda_prompt_workspace/prompt_tools/startup_kernel/start_here_lists.py"
)
SOURCE_MAP_PY_REL = Path(
    "kanda_prompt_workspace/prompt_tools/startup_kernel/startup_source_map.py"
)
SOURCE_MAP_JSON_REL = Path(
    "kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json"
)
SELF_REL = Path("tools/validate_code_module_quality_canon_v1.py")


def _fail(message: str) -> None:
    raise AssertionError(message)


def _read(root: Path, relative_path: Path) -> str:
    path = root / relative_path
    if not path.is_file():
        _fail("MISSING_REQUIRED_FILE: " + relative_path.as_posix())
    return path.read_text(encoding="utf-8-sig", errors="strict")


def _require_markers(text: str, markers: tuple[str, ...], label: str) -> None:
    missing = [marker for marker in markers if marker not in text]
    if missing:
        _fail(label + " missing markers: " + repr(missing))


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


def _validate_startup_bridge(root: Path) -> None:
    markers = (
        "BEGINNING_OF_DAY_CODE_MODULE_SIZE_HARD_GATE_V1_START",
        "CODE_MODULE_HARD_MAX_500_LINES",
        "CODE_MODULE_QUALITY_CANON_V1",
        "PEP 8 compliance",
        "SOLID responsibility and dependency design",
        "DRY implementation",
        "Measure Python physical line counts only after PEP 8-compliant formatting",
        "Never remove required blank lines",
        "create as many cohesive helper modules as needed",
        "Every helper must follow the same quality and line-count rules",
        "BEGINNING_OF_DAY_CODE_MODULE_SIZE_HARD_GATE_V1_END",
    )
    _require_markers(_read(root, STARTUP_REL), markers, "canonical startup bridge")
    _require_markers(
        _read(root, STARTUP_MIRROR_REL),
        (
            "Deprecated duplicate source",
            "not canonical",
            "KPR-01-001 start_of_day_master_stack",
        ),
        "startup bridge mirror redirect",
    )
    print("STARTUP_CODE_MODULE_QUALITY_CANON: PASS")


def _validate_detailed_canons(root: Path) -> None:
    reasoner = _read(root, REASONER_STARTUP_REL)
    _require_markers(
        reasoner,
        (
            "Reasoner Startup Canon Compatibility Record",
            "legacy KANDA Reasoner startup mega-canon is retired",
            "cannot serve as startup source",
        ),
        "reasoner startup compatibility record",
    )

    router = _read(root, ROUTER_REL)
    _require_markers(
        router,
        (
            "Ideal module size: <= 400 physical lines",
            "Maximum module size: <= 500 physical lines",
            "PEP 8 compliance: canonical",
            "SOLID responsibility/dependency design: canonical",
            "DRY implementation ownership: canonical",
            "route through the Large Module Creation and Refactor Protocol",
            "PEP 8/SOLID/DRY preserved YES/NO",
        ),
        "governed implementation router",
    )

    protocol = _read(root, PROTOCOL_REL)
    _require_markers(
        protocol,
        (
            "## Module-size and complexity law",
            "ideal size: 400 physical lines or fewer",
            "absolute hard maximum: 500 physical lines or fewer",
            "measure physical lines after normal PEP 8-compliant formatting",
            "preserve required top-level and class-level blank lines",
            "preserve SOLID responsibility and dependency direction",
            "preserve one authoritative DRY implementation owner",
            "split by cohesive responsibility, not arbitrary line ranges",
            "A line-count pass produced by compressed or non-readable "
            "formatting is invalid.",
            "No universal minimum file size is imposed.",
        ),
        "large module protocol",
    )
    print("DETAILED_PEP8_SOLID_DRY_CANONS: PASS")


def _validate_metadata(root: Path) -> None:
    startup_meta = json.loads(_read(root, STARTUP_META_REL))
    if "CODE_MODULE_QUALITY_CANON_V1" not in startup_meta.get(
        "startup_markers", []
    ):
        _fail("STARTUP_METADATA_QUALITY_MARKER_MISSING")
    notes = "\n".join(startup_meta.get("notes", []))
    _require_markers(
        notes,
        ("PEP 8 formatting", "SOLID", "DRY", "create cohesive helpers"),
        "startup metadata notes",
    )

    router_meta = json.loads(_read(root, ROUTER_META_REL))
    law = router_meta.get("module_size_law") or {}
    expected = {
        "ideal_lines": 400,
        "maximum_lines": 500,
        "pep8_canonical": True,
        "solid_canonical": True,
        "dry_canonical": True,
        "count_after_pep8_formatting": True,
        "never_break_pep8_to_fit": True,
        "over_limit_resolution": "create_cohesive_helper_modules",
    }
    for key, value in expected.items():
        if law.get(key) != value:
            _fail(f"ROUTER_METADATA_LAW_DRIFT:{key}:{law.get(key)!r}")

    protocol_meta = json.loads(_read(root, PROTOCOL_META_REL))
    rules = "\n".join(protocol_meta.get("do_not_regress", []))
    _require_markers(
        rules,
        (
            "PEP 8 compliance",
            "SOLID responsibility/dependency design",
            "DRY implementation",
            "create cohesive helpers",
        ),
        "large module metadata",
    )
    print("MODULE_QUALITY_METADATA: PASS")


def _validate_startup_generation_surfaces(root: Path) -> None:
    report_markers = (
        "PEP 8, SOLID, and DRY are canonical",
        "never compress formatting",
        "create cohesive helpers when needed",
        "PEP 8 formatting and create",
        "route above-limit code work to large_module_refactor_protocol on demand",
    )
    lists_text = _read(root, LISTS_REL)
    ast.parse(lists_text, filename=str(root / LISTS_REL))
    lists_namespace = _run_startup_module(root, LISTS_REL)
    bridge_report = lists_namespace["build_active_bridge_report"]()
    _require_markers(bridge_report, report_markers, LISTS_REL.as_posix())

    boot_text = _read(root, BOOT_REL)
    ast.parse(boot_text, filename=str(root / BOOT_REL))
    _require_markers(
        boot_text,
        (
            "from startup_kernel.start_here_lists import "
            "build_active_bridge_report",
            "active_bridge_report = build_active_bridge_report()",
        ),
        BOOT_REL.as_posix(),
    )

    role_marker = (
        "beginning-of-day Code Module Size Bridge with canonical PEP 8, SOLID, "
        "and DRY precedence"
    )
    source_map_py = _read(root, SOURCE_MAP_PY_REL)
    ast.parse(source_map_py, filename=str(root / SOURCE_MAP_PY_REL))
    source_namespace = _run_startup_module(root, SOURCE_MAP_PY_REL)
    default_entries = source_namespace["DEFAULT_SOURCE_MAP"]
    default_matches = [
        entry
        for entry in default_entries
        if entry.get("prompt_id") == "start_of_day_master_stack"
    ]
    if (
        len(default_matches) != 1
        or role_marker not in str(default_matches[0].get("role", ""))
    ):
        _fail("STARTUP_DEFAULT_SOURCE_MAP_QUALITY_ROLE_MISSING")

    source_map_json = json.loads(_read(root, SOURCE_MAP_JSON_REL))
    entries = source_map_json.get("startup_sources", [])
    matches = [
        entry
        for entry in entries
        if entry.get("prompt_id") == "start_of_day_master_stack"
    ]
    if len(matches) != 1 or role_marker not in str(matches[0].get("role", "")):
        _fail("STARTUP_SOURCE_MAP_QUALITY_ROLE_MISSING")
    print("STARTUP_GENERATOR_QUALITY_VISIBILITY: PASS")



def _validate_generated_startup_zip(path: Path) -> None:
    if not path.is_file():
        _fail("GENERATED_STARTUP_ZIP_MISSING:" + str(path))
    with zipfile.ZipFile(path) as archive:
        try:
            text = archive.read("05_start_of_day_master_stack.md").decode(
                "utf-8-sig"
            )
        except KeyError as error:
            raise AssertionError("GENERATED_STARTUP_STACK_MISSING") from error
    _require_markers(
        text,
        (
            "CODE_MODULE_QUALITY_CANON_V1",
            "PEP 8 compliance",
            "SOLID responsibility and dependency design",
            "DRY implementation",
            "Never remove required blank lines",
            "create as many cohesive helper modules as needed",
        ),
        "generated startup stack",
    )
    print("GENERATED_STARTUP_QUALITY_CANON: PASS")


def _validate_python_files(root: Path) -> None:
    for relative_path in (BOOT_REL, LISTS_REL, SOURCE_MAP_PY_REL, SELF_REL):
        text = _read(root, relative_path)
        ast.parse(text, filename=str(root / relative_path))
        line_count = len(text.splitlines())
        if line_count > 500:
            _fail(
                f"TOUCHED_PYTHON_MAX_500:{relative_path.as_posix()}:{line_count}"
            )
    self_lines = len(_read(root, SELF_REL).splitlines())
    if self_lines < 101:
        _fail(f"FOCUSED_VALIDATOR_TOO_SMALL:{self_lines}")
    print("TOUCHED_PYTHON_MODULES_MAX_500: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--generated-startup-zip", type=Path)
    args = parser.parse_args()
    root = args.project_root.resolve()

    _validate_startup_bridge(root)
    _validate_detailed_canons(root)
    _validate_metadata(root)
    _validate_startup_generation_surfaces(root)
    if args.generated_startup_zip is not None:
        _validate_generated_startup_zip(args.generated_startup_zip.resolve())
    _validate_python_files(root)

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
