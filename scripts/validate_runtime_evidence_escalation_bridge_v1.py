# project-path: scripts/validate_runtime_evidence_escalation_bridge_v1.py
"""Validate the startup-visible Runtime Evidence Escalation Bridge v1."""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import zipfile

__all__ = ["main"]

FEATURE_ID = "runtime-evidence-escalation-startup-bridge-v1"
MAX_CODE_LINES = 500

AI_PROMPT = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "01_session_start_and_navigation/ai_prompt_request_canon.md"
)
AI_META = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "ai_prompt_request_canon.meta.json"
)
STACK = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "01_session_start_and_navigation/start_of_day_master_stack.md"
)
STACK_META = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "start_of_day_master_stack.meta.json"
)
SOURCE_MAP = Path(
    "kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json"
)
SOURCE_MAP_PY = Path(
    "kanda_prompt_workspace/prompt_tools/startup_kernel/startup_source_map.py"
)
START_HERE_LISTS = Path(
    "kanda_prompt_workspace/prompt_tools/startup_kernel/start_here_lists.py"
)
GENERATOR = Path(
    "kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py"
)


class ValidationError(RuntimeError):
    """Raised when the focused contract fails."""


def _read(root: Path, relative: Path) -> str:
    path = root / relative
    if not path.is_file():
        raise ValidationError(f"Missing required file: {relative}")
    return path.read_text(encoding="utf-8")


def _require(label: str, text: str, markers: tuple[str, ...]) -> None:
    missing = [marker for marker in markers if marker not in text]
    if missing:
        raise ValidationError(f"{label} missing semantic markers: {missing}")


def _version(value: object) -> tuple[int, ...]:
    try:
        return tuple(int(part) for part in str(value).split("."))
    except ValueError as exc:
        raise ValidationError(f"Invalid version: {value!r}") from exc


def _validate_canonical_owners(root: Path) -> None:
    prompt = _read(root, AI_PROMPT)
    _require(
        "AI request canon",
        prompt,
        (
            "## Runtime Evidence Escalation",
            "Qt signal, callback, worker, or thread ordering",
            "existing KANDA runtime collector",
            "RUNTIME EVIDENCE REQUEST",
            "May proceed without it:",
            "Static source inference must remain labeled as inference",
            "HARD STOP",
            "STEP PAUSE",
            "DEGRADED WARNING",
        ),
    )
    if prompt.count("## Runtime Evidence Escalation") < 1:
        raise ValidationError("Runtime evidence section is absent")

    stack = _read(root, STACK)
    _require(
        "start-of-day bridge",
        stack,
        (
            "BEGINNING_OF_DAY_RUNTIME_EVIDENCE_ESCALATION_BRIDGE_V1_START",
            "RUNTIME_EVIDENCE_ESCALATION_BRIDGE_V1",
            "request the smallest scenario-specific runtime evidence package",
            "Do not over-request runtime evidence",
            "Static-only conclusions remain labeled as inference",
            "BEGINNING_OF_DAY_RUNTIME_EVIDENCE_ESCALATION_BRIDGE_V1_END",
        ),
    )
    forbidden_prompt = root / (
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
        "01_session_start_and_navigation/runtime_evidence_escalation_bridge.md"
    )
    if forbidden_prompt.exists():
        raise ValidationError("Duplicate standalone runtime-evidence prompt created")
    print("RUNTIME_EVIDENCE_CANON_OWNER: PASS")


def _validate_metadata(root: Path) -> None:
    ai = json.loads(_read(root, AI_META))
    stack = json.loads(_read(root, STACK_META))
    if _version(ai.get("version")) < (3, 1):
        raise ValidationError("AI Prompt Request Canon version is below 3.1")
    if _version(stack.get("version")) < (2, 1):
        raise ValidationError("Start-of-Day bridge version is below 2.1")
    if ai.get("source_stage") != ai.get("updated_for"):
        raise ValidationError("AI prompt metadata provenance is not aligned")
    if stack.get("source_stage") != stack.get("updated_for"):
        raise ValidationError("Startup metadata provenance is not aligned")
    markers = set(stack.get("startup_markers", []))
    required = {
        "BEGINNING_OF_DAY_RUNTIME_EVIDENCE_ESCALATION_BRIDGE_V1_START",
        "RUNTIME_EVIDENCE_ESCALATION_BRIDGE_V1",
    }
    if not required.issubset(markers):
        raise ValidationError("Runtime evidence startup metadata markers missing")
    print("RUNTIME_EVIDENCE_METADATA_ALIGNMENT: PASS")


def _validate_source_maps(root: Path) -> None:
    data = json.loads(_read(root, SOURCE_MAP))
    entries = data.get("startup_sources", [])
    ai_entries = [item for item in entries if item.get("prompt_id") == "ai_prompt_request_canon"]
    stack_entries = [item for item in entries if item.get("prompt_id") == "start_of_day_master_stack"]
    if len(ai_entries) != 1 or len(stack_entries) != 1:
        raise ValidationError("Startup source map owner cardinality drift")
    if "runtime-only" not in str(ai_entries[0].get("role", "")):
        raise ValidationError("AI request source-map role lacks runtime escalation")
    if "runtime-evidence escalation" not in str(stack_entries[0].get("role", "")):
        raise ValidationError("Startup stack source-map role lacks runtime bridge")
    source_map_py = _read(root, SOURCE_MAP_PY)
    ast.parse(source_map_py, filename=str(root / SOURCE_MAP_PY))
    _require(
        "fallback source map",
        source_map_py,
        ("runtime-only conclusions", "runtime-evidence escalation"),
    )
    print("RUNTIME_EVIDENCE_SOURCE_MAP: PASS")


def _validate_startup_reporting(root: Path) -> None:
    prompt_tools = root / "kanda_prompt_workspace/prompt_tools"
    inserted = str(prompt_tools) not in sys.path
    if inserted:
        sys.path.insert(0, str(prompt_tools))
    try:
        namespace = runpy.run_path(str(root / START_HERE_LISTS))
        report = str(namespace["build_active_bridge_report"]())
    finally:
        if inserted:
            sys.path.remove(str(prompt_tools))
    _require(
        "startup bridge report",
        report,
        (
            "7. Runtime Evidence Escalation Bridge - loaded/missing",
            "smallest scenario-specific trace",
            "source-sufficient questions",
            "static-only conclusions labeled as inference",
        ),
    )
    print("RUNTIME_EVIDENCE_STARTUP_REPORT: PASS")


def _validate_python(root: Path) -> None:
    paths = [SOURCE_MAP_PY, START_HERE_LISTS, Path("scripts/validate_runtime_evidence_escalation_bridge_v1.py")]
    for relative in paths:
        text = _read(root, relative)
        ast.parse(text, filename=str(root / relative))
        lines = len(text.splitlines())
        if lines > MAX_CODE_LINES:
            raise ValidationError(f"Touched Python module exceeds {MAX_CODE_LINES}: {relative}={lines}")
    print("RUNTIME_EVIDENCE_PYTHON_CONTRACT: PASS")


def _run_generator(root: Path, output_dir: Path, mode: str) -> str:
    command = [
        sys.executable,
        str(root / GENERATOR),
        mode,
        "--yes",
        "--workspace",
        str(root / "kanda_prompt_workspace"),
        "--project-root",
        str(root),
        "--output-dir",
        str(output_dir),
    ]
    completed = subprocess.run(
        command,
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        timeout=180,
    )
    output = completed.stdout + completed.stderr
    if completed.returncode != 0:
        raise ValidationError(f"Generator {mode} failed ({completed.returncode}):\n{output}")
    return output


def _zip_text(path: Path, member: str) -> str:
    with zipfile.ZipFile(path, "r") as archive:
        return archive.read(member).decode("utf-8")


def _validate_generated(root: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    dry_output = _run_generator(root, output_dir, "--dry-run")
    if "DRY RUN" not in dry_output.upper():
        raise ValidationError("Startup generator dry-run marker missing")
    sync_output = _run_generator(root, output_dir, "--sync")
    if "STATUS: IN_SYNC" not in sync_output:
        raise ValidationError("Startup generator did not report STATUS: IN_SYNC")
    check_output = _run_generator(root, output_dir, "--check")
    if "STATUS: IN_SYNC" not in check_output:
        raise ValidationError("Startup post-check did not report STATUS: IN_SYNC")

    startup_zip = output_dir / "first_prompts_to_ai.zip"
    library_zip = output_dir / "prompt_library.zip"
    tell = output_dir / "tell_AI_read_before_all.md"
    for path in (startup_zip, library_zip, tell):
        if not path.is_file():
            raise ValidationError(f"Generated startup artifact missing: {path.name}")
    report_markers = (
        "Runtime Evidence Escalation Bridge",
        "scenario-specific trace",
        "static-only conclusions labeled as inference",
    )
    _require("tell_AI_read_before_all.md", tell.read_text(encoding="utf-8"), report_markers)
    _require("00_START_HERE_FOR_AI.md", _zip_text(startup_zip, "00_START_HERE_FOR_AI.md"), report_markers)
    _require(
        "generated AI request canon",
        _zip_text(startup_zip, "01_ai_prompt_request_canon.md"),
        ("## Runtime Evidence Escalation", "RUNTIME EVIDENCE REQUEST"),
    )
    _require(
        "generated start-of-day stack",
        _zip_text(startup_zip, "05_start_of_day_master_stack.md"),
        ("RUNTIME_EVIDENCE_ESCALATION_BRIDGE_V1", "Do not over-request runtime evidence"),
    )
    _require(
        "prompt library ZIP AI request canon",
        _zip_text(
            library_zip,
            "ACTIVE_PROMPTS/01_session_start_and_navigation/ai_prompt_request_canon.md",
        ),
        ("## Runtime Evidence Escalation", "RUNTIME EVIDENCE REQUEST"),
    )
    print("RUNTIME_EVIDENCE_STARTUP_GENERATION: PASS")
    print("STATUS: IN_SYNC")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args(argv)
    root = args.project_root.resolve()
    output_dir = args.output_dir
    temp_context = None
    if output_dir is None:
        temp_context = tempfile.TemporaryDirectory(prefix="runtime_evidence_startup_")
        output_dir = Path(temp_context.name)
    try:
        _validate_canonical_owners(root)
        _validate_metadata(root)
        _validate_source_maps(root)
        _validate_startup_reporting(root)
        _validate_python(root)
        _validate_generated(root, output_dir.resolve())
    except (OSError, ValueError, json.JSONDecodeError, subprocess.TimeoutExpired, zipfile.BadZipFile, ValidationError) as exc:
        print(f"VALIDATION ERROR: {FEATURE_ID}")
        print(str(exc))
        return 1
    finally:
        if temp_context is not None:
            temp_context.cleanup()
    print("RUNTIME_EVIDENCE_ESCALATION_OUTPUT_CONTRACT: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
