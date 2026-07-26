"""Validate the code module helper expansion bridge update.

This validation is intentionally focused. It checks the canonical prompt text,
confirms the startup source map still routes the bridge source into the startup
pack, regenerates startup delivery into the project daily-work area, and checks
that generated delivery artifacts expose the new helper expansion rule.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

FEATURE_ID = "code-module-helper-expansion-bridge-v1"

PROTOCOL_PATH = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "06_refactor_and_architecture_hardening/large_module_refactor_protocol.md"
)
TEMPLATE_PATH = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "06_refactor_and_architecture_hardening/large_module_refactor_template.md"
)
STARTUP_PATH = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "01_session_start_and_navigation/start_of_day_master_stack.md"
)
SOURCE_MAP_PATH = Path("kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json")
SYNC_SCRIPT_PATH = Path("kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py")

CANONICAL_MARKERS = [
    "as many cohesive helper, auxiliary, derived, adapter, or complementary modules as needed",
    "Every helper, auxiliary, derived, adapter, or complementary code/source module must obey the same size law",
    "practical minimum around 100 substantive lines unless a documented exception applies",
    "no-leak ownership boundary",
]

STARTUP_MARKERS = [
    "create as many cohesive helper, auxiliary, derived, adapter, or complementary",
    "Every helper module must have a clear responsibility",
    "500 physical lines",
    "roughly 100 substantive lines unless a documented exception applies",
    "no-leak ownership boundary",
]

TEMPLATE_MARKERS = [
    "create as many cohesive helper, auxiliary, derived, adapter, or complementary modules as needed",
    "Do not let helper modules accidentally own facade public API",
    "Facades own public compatibility",
]


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _read_text(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"Missing required file: {path}")
    return path.read_text(encoding="utf-8")


def _assert_contains_all(label: str, text: str, markers: list[str]) -> None:
    missing = [marker for marker in markers if marker not in text]
    if missing:
        joined = "\n".join(f"- {marker}" for marker in missing)
        raise AssertionError(f"{label} is missing required marker(s):\n{joined}")


def _assert_source_map_routes_startup_bridge(root: Path) -> None:
    source_map_text = _read_text(root / SOURCE_MAP_PATH)
    data = json.loads(source_map_text)
    entries = data.get("startup_sources", [])
    matches = [
        entry
        for entry in entries
        if entry.get("canonical_source")
        == "prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/start_of_day_master_stack.md"
    ]
    if len(matches) != 1:
        raise AssertionError("Startup source map must contain exactly one start_of_day_master_stack entry")
    entry = matches[0]
    if entry.get("generated_filename") != "05_start_of_day_master_stack.md":
        raise AssertionError("start_of_day_master_stack must generate 05_start_of_day_master_stack.md")
    role = entry.get("role", "")
    if "Code Module Size Bridge" not in role:
        raise AssertionError("Startup source map role must mention Code Module Size Bridge")


def _assert_all_startup_sources_exist(root: Path) -> None:
    data = json.loads(_read_text(root / SOURCE_MAP_PATH))
    workspace = root / "kanda_prompt_workspace"
    missing: list[str] = []
    for entry in data.get("startup_sources", []):
        rel = entry.get("canonical_source", "")
        if not rel:
            missing.append("<blank canonical_source>")
            continue
        if not (workspace / rel).exists():
            missing.append(rel)
    if missing:
        joined = "\n".join(f"- {item}" for item in missing)
        raise AssertionError(f"Startup source map has missing source(s):\n{joined}")


def _run_startup_sync_to_daily_work(root: Path) -> Path:
    daily_root = root.parent / f"{root.name}_delete_after_daily_work"
    output_dir = daily_root / "code_module_helper_expansion_bridge_v1_first_prompt_files"
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    command = [
        sys.executable,
        str(root / SYNC_SCRIPT_PATH),
        "--sync",
        "--yes",
        "--workspace",
        str(root / "kanda_prompt_workspace"),
        "--project-root",
        str(root),
        "--output-dir",
        str(output_dir),
    ]
    result = subprocess.run(command, cwd=str(root), text=True, capture_output=True)
    if result.returncode != 0:
        message = [
            "Startup sync failed.",
            "STDOUT:",
            result.stdout,
            "STDERR:",
            result.stderr,
        ]
        raise AssertionError("\n".join(message))
    if "STATUS: IN_SYNC" not in result.stdout:
        raise AssertionError("Startup sync output did not include STATUS: IN_SYNC")
    return output_dir


def _assert_generated_startup_contains_rule(output_dir: Path) -> None:
    startup_zip = output_dir / "first_prompts_to_ai.zip"
    prompt_zip = output_dir / "prompt_library.zip"
    tell_file = output_dir / "tell_AI_read_before_all.md"
    if not startup_zip.exists():
        raise AssertionError("Generated first_prompts_to_ai.zip is missing")
    if not prompt_zip.exists():
        raise AssertionError("Generated prompt_library.zip is missing")
    if not tell_file.exists():
        raise AssertionError("Generated tell_AI_read_before_all.md is missing")

    with zipfile.ZipFile(startup_zip) as archive:
        generated_startup = archive.read("05_start_of_day_master_stack.md").decode("utf-8")
    _assert_contains_all("generated startup bridge", generated_startup, STARTUP_MARKERS)

    with zipfile.ZipFile(prompt_zip) as archive:
        protocol_text = archive.read(
            "ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/"
            "large_module_refactor_protocol.md"
        ).decode("utf-8")
        template_text = archive.read(
            "ACTIVE_PROMPTS/06_refactor_and_architecture_hardening/"
            "large_module_refactor_template.md"
        ).decode("utf-8")
    _assert_contains_all("generated prompt-library protocol", protocol_text, CANONICAL_MARKERS)
    _assert_contains_all("generated prompt-library template", template_text, TEMPLATE_MARKERS)


def _assert_validation_module_size(root: Path) -> None:
    path = root / "validation/test_code_module_helper_expansion_bridge_v1.py"
    line_count = len(path.read_text(encoding="utf-8").splitlines())
    if line_count > 500:
        raise AssertionError(f"Validation script exceeds 500 physical lines: {line_count}")


def main() -> int:
    root = _project_root()
    protocol_text = _read_text(root / PROTOCOL_PATH)
    template_text = _read_text(root / TEMPLATE_PATH)
    startup_text = _read_text(root / STARTUP_PATH)

    _assert_contains_all("large module refactor protocol", protocol_text, CANONICAL_MARKERS)
    _assert_contains_all("large module refactor template", template_text, TEMPLATE_MARKERS)
    _assert_contains_all("startup code module size bridge", startup_text, STARTUP_MARKERS)
    _assert_source_map_routes_startup_bridge(root)
    _assert_all_startup_sources_exist(root)
    _assert_validation_module_size(root)

    output_dir = _run_startup_sync_to_daily_work(root)
    _assert_generated_startup_contains_rule(output_dir)

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
