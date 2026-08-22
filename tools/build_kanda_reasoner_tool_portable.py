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
    smoke_no_project,
    smoke_project_agnostic_startup_generation,
)

from tool_portable_error_memory_seed import embed_tool_error_memory_seed
from tool_portable_output_delivery import (
    OUTPUT_FOLDER_NAME,
    cleanup_transient_build_root,
    delivery_zip_path,
    finalize_single_zip_delivery,
)
from tool_portable_registry_boundary import (
    assert_build_boundary_unchanged,
    prepare_build_boundary,
    validate_build_publication,
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

def _hydrate_tool_owned_physical_runtime(
    tool_root: Path,
    stage: Path,
) -> None:
    """Hydrate Tool runtime with an explicit temporary Tool-root import bootstrap."""

    tool_root_text = str(tool_root)
    tool_root_was_present = tool_root_text in sys.path
    previous_dont_write_bytecode = sys.dont_write_bytecode
    if not tool_root_was_present:
        sys.path.insert(0, tool_root_text)
    sys.dont_write_bytecode = True
    try:
        from portable.physical_runtime import hydrate_physical_runtime

        hydrate_physical_runtime(tool_root, stage)
    finally:
        sys.dont_write_bytecode = previous_dont_write_bytecode
        if not tool_root_was_present:
            try:
                sys.path.remove(tool_root_text)
            except ValueError:
                pass


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
            "VALIDATION OK: kanda-reasoner-portable-timestamped-publication-name-v1r32"
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

    agnostic_validator = (
        tool_root
        / "validation"
        / "test_portable_project_agnostic_build_contract_v3.py"
    )
    _run_required_validator(
        tool_root,
        environment,
        [sys.executable, str(agnostic_validator)],
        expected_marker=(
            "VALIDATION OK: "
            "kanda-reasoner-tool-portable-project-agnostic-build-v3"
        ),
        failure_code="PORTABLE_PROJECT_AGNOSTIC_BUILD_VALIDATION",
    )
    print("PORTABLE PROJECT-AGNOSTIC BUILD GATE: PASS")

    error_memory_seed_validator = (
        tool_root / "tools" / "validate_portable_tool_error_memory_seed_v2.py"
    )
    _run_required_validator(
        tool_root,
        environment,
        [
            sys.executable,
            str(error_memory_seed_validator),
            "--root",
            str(tool_root),
        ],
        expected_marker=(
            "VALIDATION OK: kanda-reasoner-portable-tool-error-memory-seed-no-project-support-v2"
        ),
        failure_code="PORTABLE_TOOL_ERROR_MEMORY_SEED_VALIDATION",
    )
    print("PORTABLE TOOL ERROR MEMORY SEED BUILD GATE: PASS")


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
    build_time = datetime.now()
    if output.name != OUTPUT_FOLDER_NAME:
        raise RuntimeError("PORTABLE_OUTPUT_FOLDER_NAME_MISMATCH:" + str(output))
    try:
        output.relative_to(tool_root)
    except ValueError:
        pass
    else:
        raise RuntimeError("OUTPUT_DIRECTORY_INSIDE_TOOL_ROOT")

    environment = clean_environment()
    boundary, registry = prepare_build_boundary(
        tool_root,
        output,
        delivery_zip_path(output, build_time).name,
    )
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
    delivery_zip = delivery_zip_path(output, build_time)
    if (output.exists() and any(output.iterdir())) or delivery_zip.exists():
        if not args.replace_existing:
            raise RuntimeError("PORTABLE_OUTPUT_ALREADY_EXISTS_USE_REPLACE_EXISTING")

    app_root = run_pyinstaller(tool_root, run_root, environment)
    stage = stage_application(app_root, run_root / "release_stage")
    _hydrate_tool_owned_physical_runtime(tool_root, stage)
    error_memory_seed = embed_tool_error_memory_seed(tool_root, stage)
    assert_no_project_capture(stage)
    assert_build_boundary_unchanged(boundary)
    if output.exists() and args.replace_existing:
        shutil.rmtree(output)
    if delivery_zip.exists() and args.replace_existing:
        delivery_zip.unlink()
    output.mkdir(parents=True, exist_ok=True)
    shutil.copytree(stage, final_folder)
    zip_evidence = create_deterministic_zip(stage, final_zip)
    first_smoke: dict[str, Any] | None = None
    project_agnostic_smoke: dict[str, Any] | None = None
    if not args.skip_smoke:
        first_smoke = smoke_no_project(final_zip, run_root)
        project_agnostic_smoke = smoke_project_agnostic_startup_generation(
            final_folder,
            run_root,
        )

    result = {
        "schema_version": "1.0",
        "feature_id": FEATURE_ID,
        "status": (
            "portable_ready"
            if first_smoke is not None and project_agnostic_smoke is not None
            else "portable_built_unverified"
        ),
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "tool_root": str(tool_root),
        "selected_project_during_build": (
            boundary.current_project_id or None
        ),
        "self_hosting_during_build": (
            boundary.selection_mode == "EXPLICIT_SELF_HOSTING"
        ),
        "project_selection_authority_used_for_build": False,
        "registry": registry,
        "pyinstaller_version": importlib.metadata.version("pyinstaller"),
        "spec_path": str(tool_root / "KandaReasonerWindows.spec"),
        "spec_sha256": sha256(tool_root / "KandaReasonerWindows.spec"),
        "output_folder": f"{OUTPUT_FOLDER_NAME}/{TOP_LEVEL_NAME}",
        "portable_zip": {
            **zip_evidence,
            "path": "TRANSIENT_SMOKE_ARTIFACT_NOT_RETAINED",
            "retained": False,
        },
        "first_smoke": first_smoke,
        "project_agnostic_smoke": project_agnostic_smoke,
        "tool_error_memory_seed": error_memory_seed,
        "second_smoke": project_agnostic_smoke,
        "second_smoke_kind": "project_agnostic_startup_generation",
        "project_content_packaged": False,
        "publication_contract": {
            "final_artifact_name": delivery_zip.name,
            "output_workspace_retained": False,
            "inner_portable_zip_retained": False,
            "transient_build_root_retained": False,
        },
    }
    write_json(result_path, result)
    write_json(output / "KandaReasoner-Windows-Portable-build-result.json", result)
    validate_build_publication(
        boundary,
        output,
        delivery_zip.name,
    )
    delivery_evidence = finalize_single_zip_delivery(output, build_time)
    assert_build_boundary_unchanged(boundary)

    if result["status"] == "portable_ready":
        print("KANDA REASONER TOOL PORTABLE CREATED: PASS")
    else:
        print("KANDA REASONER TOOL PORTABLE BUILT BUT UNVERIFIED: PASS")
    observed_project = boundary.current_project_id or "NONE"
    print("SELECTED PROJECT OBSERVED DURING BUILD: " + observed_project)
    print("SELECTED PROJECT BUILD AUTHORITY: NOT USED")
    print("PROJECT SELECTION MUTATION DURING BUILD: ABSENT")
    print("SELF-HOSTING BUILD AUTHORITY: NOT USED")
    print("PYINSTALLER NATIVE WINDOWS BUILD: PASS")
    print("PROJECT CONTENT PACKAGED: NO")
    print("REAL PROJECT INPUT REQUIRED FOR BUILD: NO")
    print("TOOL ERROR MEMORY SEED PACKAGED: YES")
    print(
        "TOOL ERROR MEMORY LESSON COUNT: "
        + str(error_memory_seed["lesson_count"])
    )
    print("PORTABLE APP: INSIDE " + Path(delivery_evidence["path"]).name)
    print("PORTABLE INNER ZIP RETAINED: NO")
    print(f"PORTABLE DELIVERY ZIP: {delivery_evidence['path']}")
    print(f"PORTABLE DELIVERY ZIP SHA-256: {delivery_evidence['sha256']}")
    print(f"PORTABLE DELIVERY MEMBER COUNT: {delivery_evidence['member_count']}")
    print("BUILD RESULT: INSIDE " + Path(delivery_evidence["path"]).name)
    cleanup_transient_build_root(run_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
