# project-path: scripts/validate_startup_box_logic_bridge_visible_v1.py
"""Validate startup-visible Box Logic hard gate bridge v1."""

from __future__ import annotations

import runpy
import sys
import zipfile
from pathlib import Path

__all__ = [
    "main",
]


FEATURE_ID = "startup-box-logic-bridge-visible-v1"
MAX_CODE_LINES = 500

SOURCE_START_FILES = [
    Path(
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
        "01_session_start_and_navigation/start_of_day_master_stack.md"
    ),
    Path(
        "prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/"
        "start_of_day_master_stack.md"
    ),
]

META_FILES = [
    Path("kanda_prompt_workspace/prompt_library/METADATA/start_of_day_master_stack.meta.json"),
    Path("prompt_library/METADATA/start_of_day_master_stack.meta.json"),
]

PYTHON_FILES = [
    Path("kanda_prompt_workspace/prompt_tools/startup_kernel/boot_text.py"),
    Path("kanda_prompt_workspace/prompt_tools/startup_kernel/start_here_lists.py"),
    Path("scripts/validate_startup_box_logic_bridge_visible_v1.py"),
]

SOURCE_MARKERS = [
    "BEGINNING_OF_DAY_BOX_LOGIC_BRIDGE",
    "BEGINNING_OF_DAY_BOX_LOGIC_SHIELD_V1_START",
    "BOX_LOGIC_STARTUP_SHIELD",
    "mandatory beginning-of-day",
    "Keep code and responsibility inside the owning box.",
    "Do not let code, imports, mutable state, UI logic, domain logic",
    "`box_architecture_canon.md` before implementation or delivery",
    "BEGINNING_OF_DAY_BOX_LOGIC_SHIELD_V1_END",
]

BRIDGE_REPORT_MARKERS = [
    "2. Box Logic Startup Bridge - loaded/missing",
    "identify active box",
    "owner paths",
    "allowed files",
    "out-of-scope files",
    "cross-box touches",
    "public contracts",
    "validation scope",
    "boundary risks",
    "route boundary-risk work to box_architecture_canon on demand",
    "6. Terminal Cleanup Bridge - loaded/missing",
]


class ValidationError(Exception):
    """Raised when a validation check fails."""


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValidationError(f"Could not read {path}: {exc}") from exc


def _require_file(path: Path) -> None:
    if not path.is_file():
        raise ValidationError(f"Missing required file: {path}")


def _require_markers(label: str, text: str, markers: list[str]) -> None:
    missing = [marker for marker in markers if marker not in text]
    if missing:
        raise ValidationError(f"{label} missing markers: {missing}")


def _validate_source_start_files(project_root: Path) -> None:
    canonical = project_root / SOURCE_START_FILES[0]
    mirror = project_root / SOURCE_START_FILES[1]
    _require_file(canonical)
    _require_file(mirror)
    _require_markers(str(SOURCE_START_FILES[0]), _read_text(canonical), SOURCE_MARKERS)
    _require_markers(
        str(SOURCE_START_FILES[1]),
        _read_text(mirror),
        [
            "Deprecated duplicate source",
            "not canonical",
            "KPR-01-001 start_of_day_master_stack",
        ],
    )


def _validate_metadata(project_root: Path) -> None:
    canonical_path = project_root / META_FILES[0]
    mirror_path = project_root / META_FILES[1]
    _require_file(canonical_path)
    _require_file(mirror_path)
    _require_markers(
        str(META_FILES[0]),
        _read_text(canonical_path),
        [
            "BOX_LOGIC_STARTUP_SHIELD",
            "BEGINNING_OF_DAY_BOX_LOGIC_SHIELD_V1_START",
        ],
    )
    _require_markers(
        str(META_FILES[1]),
        _read_text(mirror_path),
        ["deprecated", "do_not_use_as_source_authority"],
    )


def _validate_generator_sources(project_root: Path) -> None:
    boot_path = project_root / Path(
        "kanda_prompt_workspace/prompt_tools/startup_kernel/boot_text.py"
    )
    lists_path = project_root / Path(
        "kanda_prompt_workspace/prompt_tools/startup_kernel/start_here_lists.py"
    )
    _require_file(boot_path)
    _require_file(lists_path)
    prompt_tools = project_root / "kanda_prompt_workspace" / "prompt_tools"
    prompt_tools_text = str(prompt_tools)
    inserted = prompt_tools_text not in sys.path
    if inserted:
        sys.path.insert(0, prompt_tools_text)
    try:
        namespace = runpy.run_path(str(lists_path))
        bridge_report = namespace["build_active_bridge_report"]()
    finally:
        if inserted:
            sys.path.remove(prompt_tools_text)
    _require_markers(
        str(lists_path),
        bridge_report,
        BRIDGE_REPORT_MARKERS,
    )
    _require_markers(
        str(boot_path),
        _read_text(boot_path),
        [
            "from startup_kernel.start_here_lists import build_active_bridge_report",
            "active_bridge_report = build_active_bridge_report()",
        ],
    )


def _line_count(path: Path) -> int:
    return len(_read_text(path).splitlines())


def _validate_touched_python_line_counts(project_root: Path) -> None:
    for relative_path in PYTHON_FILES:
        path = project_root / relative_path
        _require_file(path)
        line_count = _line_count(path)
        if line_count > MAX_CODE_LINES:
            raise ValidationError(
                f"Touched Python file exceeds {MAX_CODE_LINES} lines: "
                f"{relative_path} has {line_count} lines"
            )


def _candidate_first_prompt_dirs(project_root: Path) -> list[Path]:
    project_name = project_root.name
    candidates: list[Path] = []
    anchor = Path(project_root.anchor) if project_root.anchor else None
    if anchor is not None:
        candidates.append(anchor / f"{project_name}_show_project_to_AI" / "first_prompt_files")
    candidates.append(project_root.parent / f"{project_name}_show_project_to_AI" / "first_prompt_files")
    candidates.append(project_root / "first_prompt_files")
    unique: list[Path] = []
    for candidate in candidates:
        if candidate not in unique:
            unique.append(candidate)
    return unique


def _find_first_prompt_dir(project_root: Path) -> Path:
    for candidate in _candidate_first_prompt_dirs(project_root):
        if (candidate / "first_prompts_to_ai.zip").is_file():
            return candidate
    checked = ", ".join(str(path) for path in _candidate_first_prompt_dirs(project_root))
    raise ValidationError(f"Generated first_prompts_to_ai.zip not found. Checked: {checked}")


def _read_zip_member(zip_path: Path, member_name: str) -> str:
    try:
        with zipfile.ZipFile(zip_path, "r") as archive:
            return archive.read(member_name).decode("utf-8")
    except KeyError as exc:
        raise ValidationError(f"Missing {member_name} in {zip_path}") from exc
    except (OSError, zipfile.BadZipFile, UnicodeDecodeError) as exc:
        raise ValidationError(f"Could not read {member_name} in {zip_path}: {exc}") from exc


def _validate_generated_startup(project_root: Path) -> None:
    first_prompt_dir = _find_first_prompt_dir(project_root)
    startup_zip = first_prompt_dir / "first_prompts_to_ai.zip"
    read_before_all = first_prompt_dir / "tell_AI_read_before_all.md"
    prompt_library_zip = first_prompt_dir / "prompt_library.zip"

    for path in [startup_zip, read_before_all, prompt_library_zip]:
        _require_file(path)

    _require_markers(
        "tell_AI_read_before_all.md",
        _read_text(read_before_all),
        BRIDGE_REPORT_MARKERS,
    )
    _require_markers(
        "00_START_HERE_FOR_AI.md",
        _read_zip_member(startup_zip, "00_START_HERE_FOR_AI.md"),
        BRIDGE_REPORT_MARKERS,
    )
    _require_markers(
        "05_start_of_day_master_stack.md",
        _read_zip_member(startup_zip, "05_start_of_day_master_stack.md"),
        SOURCE_MARKERS,
    )
    _require_markers(
        "prompt_library.zip start_of_day_master_stack.md",
        _read_zip_member(
            prompt_library_zip,
            "ACTIVE_PROMPTS/01_session_start_and_navigation/start_of_day_master_stack.md",
        ),
        SOURCE_MARKERS,
    )


def main() -> int:
    project_root = Path.cwd().resolve()
    try:
        _validate_source_start_files(project_root)
        _validate_metadata(project_root)
        _validate_generator_sources(project_root)
        _validate_touched_python_line_counts(project_root)
        _validate_generated_startup(project_root)
    except ValidationError as exc:
        print(f"VALIDATION ERROR: {FEATURE_ID}")
        print(str(exc))
        return 1

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("BOX LOGIC BRIDGE: VISIBLE")
    print("CODE MODULE LINE COUNTS: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
