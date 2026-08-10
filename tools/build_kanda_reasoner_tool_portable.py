"""Direct native-Windows PyInstaller build for the KANDA Reasoner Tool."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

__all__ = [
    "assert_no_project_capture",
    "stage_application",
    "create_deterministic_zip",
    "main",
]

from tool_portable_functional_smoke import (
    smoke_external_project,
    smoke_no_project,
)

FEATURE_ID = "kanda-reasoner-tool-portable-direct-pyinstaller-v1r2"
TOP_LEVEL_NAME = "KandaReasoner-Windows-Portable"
FINAL_ZIP_NAME = TOP_LEVEL_NAME + ".zip"
PRODUCT_EXE = "kanda_reasoner.exe"
EXPECTED_PYTHON = (3, 12)
EXPECTED_PYINSTALLER = "6.21.0"
SCRUB_PREFIXES = ("KANDA_", "PROJECT_REASONER_")
SCRUB_NAMES = {
    "kanda_reasoner_project_root",
    "KANDA_REASONER_PROJECT_ROOT",
    "KANDA_RUNTIME_PROJECT_ROOT",
    "PROJECT_REASONER_PROJECT_ROOT",
    "PROJECT_REASONER_SCAN_ROOT",
    "KANDA_REASONER_SCAN_ROOT",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GOOGLE_API_KEY",
    "GEMINI_API_KEY",
    "AZURE_OPENAI_API_KEY",
}
FORBIDDEN_OUTPUT_PARTS = {
    "tool_project_registry",
    "project_freeze_after_update",
    "project_error_memory",
    "first_prompt_files",
    "second_prompt_files",
    "second_prompt_files_building",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def clean_environment() -> dict[str, str]:
    environment = {
        key: value
        for key, value in os.environ.items()
        if key not in SCRUB_NAMES
        and not any(key.startswith(prefix) for prefix in SCRUB_PREFIXES)
    }
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return environment


def require_unselected(tool_root: Path) -> dict[str, Any]:
    sys.path.insert(0, str(tool_root))
    try:
        from kanda_reasoner_app.project_selection_registry import (
            ProjectSelectionRegistry,
        )
        registry = ProjectSelectionRegistry(tool_source_root=tool_root)
        record = registry.load_current_record()
        path = registry.registry_path.resolve(strict=False)
    finally:
        try:
            sys.path.remove(str(tool_root))
        except ValueError:
            pass
    if record is not None:
        raise RuntimeError(
            "TOOL_PORTABLE_BUILD_REQUIRES_SELECTED_PROJECT_NONE:"
            + record.project_root
        )
    payload = json.loads(path.read_text(encoding="utf-8"))
    if str(payload.get("current_project_id") or "").strip():
        raise RuntimeError("TOOL_PORTABLE_BUILD_CURRENT_PROJECT_ID_NOT_EMPTY")
    return {
        "registry_path": str(path),
        "registry_sha256": sha256(path),
        "current_project_id": "",
        "selection_mode": "UNSELECTED",
    }


def _run_required_validator(
    tool_root: Path,
    environment: dict[str, str],
    command: list[str],
    *,
    expected_marker: str,
    failure_code: str,
    timeout: int = 900,
) -> None:
    """Run one pre-build validator and require its exact success marker."""
    completed = subprocess.run(
        command,
        cwd=str(tool_root),
        env=environment,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
    )
    output = (completed.stdout or "") + (completed.stderr or "")
    print(output, end="" if output.endswith("\n") else "\n")
    if completed.returncode != 0:
        raise RuntimeError(failure_code + "_FAILED")
    if expected_marker not in output:
        raise RuntimeError(failure_code + "_MARKER_MISSING")


def validate_core_builder(tool_root: Path, environment: dict[str, str]) -> None:
    """Validate the Portable builder and Local AI Project authority gate."""
    validator = tool_root / "portable" / "validate_installed.py"
    _run_required_validator(
        tool_root,
        environment,
        [
            sys.executable,
            str(validator),
            "--portable-root",
            str(tool_root / "portable"),
        ],
        expected_marker=(
            "VALIDATION OK: kanda-reasoner-portable-builder-install-v1r12"
        ),
        failure_code="CURRENT_PORTABLE_BUILDER_VALIDATION",
    )
    print("CURRENT STAGE 1-6 PORTABLE BUILDER: PASS")

    authority_validator = (
        tool_root
        / "tools"
        / "validate_tool_portable_local_ai_project_authority_v1r1.py"
    )
    _run_required_validator(
        tool_root,
        environment,
        [
            sys.executable,
            str(authority_validator),
            "--tool-root",
            str(tool_root),
            "--skip-existing-validators",
        ],
        expected_marker=(
            "VALIDATION OK: "
            "kanda-reasoner-tool-portable-local-ai-project-authority-v1r1"
        ),
        failure_code="LOCAL_AI_PROJECT_AUTHORITY_VALIDATION",
    )
    print("LOCAL AI PROJECT AUTHORITY PRE-BUILD GATE: PASS")


def run_pyinstaller(
    tool_root: Path,
    run_root: Path,
    environment: dict[str, str],
) -> Path:
    if sys.version_info[:2] != EXPECTED_PYTHON:
        raise RuntimeError(
            f"PYTHON_VERSION_MISMATCH:{sys.version_info.major}.{sys.version_info.minor}"
        )
    version = importlib.metadata.version("pyinstaller")
    if version != EXPECTED_PYINSTALLER:
        raise RuntimeError(
            f"PYINSTALLER_VERSION_MISMATCH:{version};expected={EXPECTED_PYINSTALLER}"
        )
    spec = tool_root / "KandaReasonerWindows.spec"
    if not spec.is_file():
        raise RuntimeError("PYINSTALLER_SPEC_MISSING:" + str(spec))
    dist = run_root / "pyinstaller_dist"
    work = run_root / "pyinstaller_work"
    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--clean",
        "--noconfirm",
        "--distpath",
        str(dist),
        "--workpath",
        str(work),
        str(spec),
    ]
    print("PYINSTALLER TOOL BUILD COMMAND: PASS")
    completed = subprocess.run(
        command,
        cwd=str(tool_root),
        env=environment,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "PYINSTALLER_TOOL_BUILD_FAILED:" + str(completed.returncode)
        )
    app_root = dist / "kanda_reasoner"
    executable = app_root / PRODUCT_EXE
    if not executable.is_file():
        raise RuntimeError("PYINSTALLER_PRODUCT_EXE_MISSING:" + str(executable))
    print("PYINSTALLER KANDA REASONER TOOL BUILD: PASS")
    return app_root


def assert_no_project_capture(app_root: Path) -> None:
    violations: list[str] = []
    for path in app_root.rglob("*"):
        relative = path.relative_to(app_root)
        lowered = {part.casefold() for part in relative.parts}
        if lowered.intersection(FORBIDDEN_OUTPUT_PARTS):
            violations.append(relative.as_posix())
        if any(part.casefold().endswith("_show_project_to_ai") for part in relative.parts):
            violations.append(relative.as_posix())
        if any(part.casefold().endswith("_delete_after_daily_work") for part in relative.parts):
            violations.append(relative.as_posix())
    if violations:
        raise RuntimeError(
            "PROJECT_OR_SUPPORT_CAPTURED_IN_TOOL_PORTABLE:"
            + ";".join(sorted(set(violations))[:25])
        )
    print("TOOL PORTABLE PROJECT/SUPPORT CAPTURE: ABSENT")


def stage_application(app_root: Path, stage_parent: Path) -> Path:
    stage = stage_parent / TOP_LEVEL_NAME
    if stage_parent.exists():
        shutil.rmtree(stage_parent)
    stage_parent.mkdir(parents=True)
    shutil.copytree(app_root, stage)
    assert_no_project_capture(stage)
    return stage


def create_deterministic_zip(stage: Path, destination: Path) -> dict[str, Any]:
    temporary = destination.with_name(destination.name + ".tmp")
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary.unlink(missing_ok=True)
    member_count = 0
    with zipfile.ZipFile(
        temporary,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for path in sorted(stage.rglob("*"), key=lambda p: p.as_posix().casefold()):
            if not path.is_file():
                continue
            relative = Path(TOP_LEVEL_NAME) / path.relative_to(stage)
            info = zipfile.ZipInfo(relative.as_posix())
            info.date_time = (2020, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
            member_count += 1
    with zipfile.ZipFile(temporary, "r") as archive:
        if archive.testzip() is not None:
            raise RuntimeError("TOOL_PORTABLE_ZIP_CRC_FAILURE")
        names = archive.namelist()
        if not names or {Path(name).parts[0] for name in names} != {TOP_LEVEL_NAME}:
            raise RuntimeError("TOOL_PORTABLE_ZIP_TOP_LEVEL_MISMATCH")
    os.replace(temporary, destination)
    return {
        "path": str(destination),
        "sha256": sha256(destination),
        "size_bytes": destination.stat().st_size,
        "member_count": member_count,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool-root", type=Path, required=True)
    parser.add_argument("--output-directory", type=Path, required=True)
    parser.add_argument(
        "--external-project-root",
        type=Path,
        default=Path(r"E:\eeg_kanda"),
    )
    parser.add_argument("--yes", action="store_true")
    parser.add_argument("--replace-existing", action="store_true")
    parser.add_argument("--skip-smoke", action="store_true")
    args = parser.parse_args()

    if os.name != "nt":
        raise RuntimeError("TOOL_PORTABLE_BUILD_REQUIRES_WINDOWS")
    if not args.yes:
        raise RuntimeError("EXPLICIT_BUILD_CONFIRMATION_REQUIRED")
    tool_root = args.tool_root.expanduser().resolve(strict=True)
    if tool_root.name.casefold() != "kanda_reasoner":
        raise RuntimeError("TOOL_ROOT_NAME_MISMATCH:" + str(tool_root))
    output = args.output_directory.expanduser().resolve(strict=False)
    try:
        output.relative_to(tool_root)
    except ValueError:
        pass
    else:
        raise RuntimeError("OUTPUT_DIRECTORY_INSIDE_TOOL_ROOT")

    environment = clean_environment()
    registry = require_unselected(tool_root)
    validate_core_builder(tool_root, environment)

    drive = Path(tool_root.anchor).resolve()
    transient = drive / f"{tool_root.name}_delete_after_daily_work"
    run_root = transient / "tool_portable_direct_pyinstaller_v1r1" / (
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    )
    run_root.mkdir(parents=True, exist_ok=False)
    result_path = run_root / "build_result.json"
    final_zip = output / FINAL_ZIP_NAME
    final_folder = output / TOP_LEVEL_NAME
    if (final_zip.exists() or final_folder.exists()) and not args.replace_existing:
        raise RuntimeError("PORTABLE_OUTPUT_ALREADY_EXISTS_USE_REPLACE_EXISTING")

    app_root = run_pyinstaller(tool_root, run_root, environment)
    stage = stage_application(app_root, run_root / "release_stage")
    output.mkdir(parents=True, exist_ok=True)
    if final_folder.exists():
        shutil.rmtree(final_folder)
    shutil.copytree(stage, final_folder)
    zip_evidence = create_deterministic_zip(stage, final_zip)
    first_smoke: dict[str, Any] | None = None
    second_smoke: dict[str, Any] | None = None
    if not args.skip_smoke:
        first_smoke = smoke_no_project(final_zip, run_root)
        second_smoke = smoke_external_project(
            final_folder,
            args.external_project_root,
            run_root,
            source_registry_path=Path(registry["registry_path"]),
        )

    result = {
        "schema_version": "1.0",
        "feature_id": FEATURE_ID,
        "status": (
            "portable_ready"
            if first_smoke is not None and second_smoke is not None
            else "portable_built_unverified"
        ),
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "tool_root": str(tool_root),
        "selected_project_during_build": None,
        "self_hosting_during_build": False,
        "registry": registry,
        "pyinstaller_version": importlib.metadata.version("pyinstaller"),
        "spec_path": str(tool_root / "KandaReasonerWindows.spec"),
        "spec_sha256": sha256(tool_root / "KandaReasonerWindows.spec"),
        "output_folder": str(final_folder),
        "portable_zip": zip_evidence,
        "first_smoke": first_smoke,
        "second_smoke": second_smoke,
        "project_content_packaged": False,
    }
    write_json(result_path, result)
    write_json(output / "KandaReasoner-Windows-Portable-build-result.json", result)

    if result["status"] == "portable_ready":
        print("KANDA REASONER TOOL PORTABLE CREATED: PASS")
    else:
        print("KANDA REASONER TOOL PORTABLE BUILT BUT UNVERIFIED: PASS")
    print("SELECTED PROJECT DURING BUILD: NONE")
    print("SELF-HOSTING DURING BUILD: OFF")
    print("PYINSTALLER NATIVE WINDOWS BUILD: PASS")
    print("PROJECT CONTENT PACKAGED: NO")
    print(f"PORTABLE FOLDER: {final_folder}")
    print(f"PORTABLE ZIP: {final_zip}")
    print(f"PORTABLE ZIP SHA-256: {zip_evidence['sha256']}")
    print(f"BUILD RESULT: {result_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
