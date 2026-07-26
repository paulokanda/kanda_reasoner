"""Validate Sync Startup Routing Kernel Refactor Train Car 3 v1."""

from __future__ import annotations

import importlib
import py_compile
import sys
from pathlib import Path

__all__: list[str] = []


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMPT_TOOLS = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_tools"
STARTUP_KERNEL = PROMPT_TOOLS / "startup_kernel"

FEATURE_ID = "sync-startup-kernel-refactor-train-car-3-v1"

REQUIRED_FILES = [
    STARTUP_KERNEL / "constants.py",
    STARTUP_KERNEL / "startup_names.py",
    STARTUP_KERNEL / "startup_literal_texts.py",
    STARTUP_KERNEL / "startup_source_map.py",
]

COMPILE_FILES = REQUIRED_FILES + [
    PROMPT_TOOLS / "sync_startup_routing_kernel_pack.py",
    STARTUP_KERNEL / "boot_text.py",
    STARTUP_KERNEL / "cli.py",
    STARTUP_KERNEL / "core_helpers.py",
    STARTUP_KERNEL / "maintenance_text.py",
    STARTUP_KERNEL / "paste_readme_text.py",
    STARTUP_KERNEL / "prompt_library_zip.py",
    STARTUP_KERNEL / "read_order.py",
    STARTUP_KERNEL / "start_here_text.py",
    STARTUP_KERNEL / "start_here_body_intro.py",
    STARTUP_KERNEL / "start_here_body_routing.py",
    STARTUP_KERNEL / "start_here_lists.py",
    STARTUP_KERNEL / "zip_delivery.py",
]


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _line_count(path: Path) -> int:
    return len(_read(path).splitlines())


def validate_files_exist() -> None:
    for path in REQUIRED_FILES:
        _assert(path.exists(), "missing required file: " + str(path))


def validate_compile() -> None:
    for path in COMPILE_FILES:
        _assert(path.exists(), "missing compile target: " + str(path))
        py_compile.compile(str(path), doraise=True)


def validate_line_counts() -> None:
    for path in STARTUP_KERNEL.glob("*.py"):
        _assert(_line_count(path) <= 500, "startup_kernel module above 500 lines: " + path.name)
    _assert(_line_count(STARTUP_KERNEL / "constants.py") <= 80, "constants.py should stay a small re-export module")
    _assert(_line_count(STARTUP_KERNEL / "startup_names.py") <= 120, "startup_names.py is too large")
    _assert(_line_count(STARTUP_KERNEL / "startup_literal_texts.py") <= 400, "startup_literal_texts.py is too large")
    _assert(_line_count(STARTUP_KERNEL / "startup_source_map.py") <= 120, "startup_source_map.py is too large")


def validate_refactor_shape() -> None:
    constants_text = _read(STARTUP_KERNEL / "constants.py")
    _assert("from startup_kernel.startup_literal_texts import *" in constants_text, "constants.py must re-export startup literal text constants")
    _assert("from startup_kernel.startup_names import *" in constants_text, "constants.py must re-export startup names")
    _assert("from startup_kernel.startup_source_map import *" in constants_text, "constants.py must re-export startup source map")
    _assert("DEFAULT_SOURCE_MAP = [" not in constants_text, "constants.py must not regain DEFAULT_SOURCE_MAP body")
    _assert("BOOT_COMMAND_TEXT =" not in constants_text, "constants.py must not regain boot command body")
    _assert("RG-028 FREEZE-WORKFLOW" not in constants_text, "constants.py must not regain long override literal bodies")

    literal_text = _read(STARTUP_KERNEL / "startup_literal_texts.py")
    _assert("BOOT_COMMAND_TEXT =" in literal_text, "startup_literal_texts.py must own BOOT_COMMAND_TEXT")
    _assert("RG-028 FREEZE-WORKFLOW" in literal_text, "startup_literal_texts.py must own freeze-workflow literal")
    _assert("PRE-OUTPUT CONTRACT GATES HOOK" in literal_text, "startup_literal_texts.py must own pre-output contract gate literal")

    source_map_text = _read(STARTUP_KERNEL / "startup_source_map.py")
    _assert("DEFAULT_SOURCE_MAP = [" in source_map_text, "startup_source_map.py must own DEFAULT_SOURCE_MAP")
    _assert("class SourceEntry" in source_map_text, "startup_source_map.py must own SourceEntry")


def validate_public_import_surface() -> None:
    sys.path.insert(0, str(PROMPT_TOOLS))
    constants = importlib.import_module("startup_kernel.constants")
    _assert(constants.DEFAULT_ZIP_NAME == "first_prompts_to_ai.zip", "DEFAULT_ZIP_NAME changed")
    _assert(constants.PROMPT_LIBRARY_ZIP_NAME == "prompt_library.zip", "PROMPT_LIBRARY_ZIP_NAME changed")
    _assert(constants.MANIFEST_FILENAME == "STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json", "MANIFEST_FILENAME changed")
    _assert("STARTUP PACK LOAD CHECK" in constants.BOOT_COMMAND_TEXT, "BOOT_COMMAND_TEXT lost startup load check")
    _assert("RG-015 FIRST-POSITION EXACT OVERRIDE" in constants.T9T013_RG015_FIRST_POSITION_OVERRIDE_RULE_V8, "RG-015 override missing")
    _assert(len(constants.DEFAULT_SOURCE_MAP) >= 8, "DEFAULT_SOURCE_MAP unexpectedly short")
    entry = constants.SourceEntry(
        load_order=1,
        canonical_source="a",
        generated_filename="b",
        prompt_id="c",
        load_mode="always_startup",
        role="role",
    )
    _assert(entry.generated_filename == "b", "SourceEntry dataclass import failed")


def validate_generator_output_smoke() -> None:
    sys.path.insert(0, str(PROMPT_TOOLS))
    start_here = importlib.import_module("startup_kernel.start_here_text")
    text = start_here.make_start_here_file(
        "CERT-TEST",
        "2026-06-29T00:00:00Z",
        [
            "01_ai_prompt_request_canon.md",
            "02_prompt_navigation_index.md",
            "09_active_project_freeze_context.md",
        ],
    )[1]
    for fragment in (
        "STARTUP PACK LOAD CHECK",
        "Beginning-of-day active bridges",
        "Code Module Size Bridge",
        "Prompt library ZIP direct retrieval rule",
        "second-upload order",
    ):
        _assert(fragment in text, "generated start-here text missing: " + fragment)


def main() -> int:
    validate_files_exist()
    validate_compile()
    validate_line_counts()
    validate_refactor_shape()
    validate_public_import_surface()
    validate_generator_output_smoke()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
