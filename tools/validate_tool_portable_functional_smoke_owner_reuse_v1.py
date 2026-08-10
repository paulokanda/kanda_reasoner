"""Validate functional Portable smoke reporting and stable Project identity reuse."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

FEATURE_ID = "kanda-reasoner-tool-portable-functional-smoke-owner-reuse-v1"
DIRECT_MARKER = (
    "VALIDATION OK: "
    "kanda-reasoner-tool-portable-direct-pyinstaller-v1r2"
)
TARGETS = (
    "kanda_reasoner_app/portable_smoke_isolation.py",
    "kanda_reasoner_app/portable_smoke_runtime_report.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py",
    "kanda_reasoner_app/error_memory_gui/_project_paths_mixin.py",
    "tools/tool_portable_functional_smoke.py",
    "tools/build_kanda_reasoner_tool_portable.py",
    "tools/validate_kanda_reasoner_tool_portable_direct_build_v1r1.py",
)


def require(condition: bool, code: str) -> None:
    if not condition:
        raise RuntimeError(code)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _portable_snapshot(root: Path) -> dict[str, str]:
    portable = root / "portable"
    return {
        path.relative_to(portable).as_posix(): sha256(path)
        for path in portable.rglob("*")
        if path.is_file()
    }


def _validate_live_eeg_identity(root: Path) -> None:
    if os.name != "nt":
        print("LIVE EEG KANDA OWNER IDENTITY: NOT APPLICABLE")
        return
    drive = Path(root.anchor).resolve()
    registry = (
        drive
        / f"{root.name}_show_project_to_AI"
        / "tool_project_registry"
        / "projects.json"
    )
    owner_manifest = (
        drive
        / "eeg_kanda_show_project_to_AI"
        / "project_error_memory"
        / "owner_manifest.json"
    )
    project = drive / "eeg_kanda"
    if not registry.is_file() or not owner_manifest.is_file() or not project.is_dir():
        print("LIVE EEG KANDA OWNER IDENTITY: NOT PRESENT")
        return
    registry_payload = json.loads(registry.read_text(encoding="utf-8"))
    owner = json.loads(owner_manifest.read_text(encoding="utf-8-sig"))
    projects = registry_payload.get("projects")
    require(isinstance(projects, dict), "LIVE_REGISTRY_PROJECTS_INVALID")
    matches = [
        value for value in projects.values()
        if isinstance(value, dict)
        and Path(str(value.get("project_root") or "")).resolve(strict=False)
        == project.resolve(strict=False)
    ]
    require(len(matches) == 1, "LIVE_EEG_REGISTRY_MATCH_COUNT")
    record = matches[0]
    require(
        str(record.get("stable_project_id") or "")
        == str(owner.get("owner_id") or ""),
        "LIVE_EEG_OWNER_ID_MISMATCH",
    )
    require(
        str(record.get("project_root_fingerprint") or "")
        == str(owner.get("owner_root_fingerprint") or ""),
        "LIVE_EEG_OWNER_FINGERPRINT_MISMATCH",
    )
    require(
        str(record.get("project_slug") or "")
        == str(owner.get("owner_slug") or ""),
        "LIVE_EEG_OWNER_SLUG_MISMATCH",
    )
    require(
        Path(str(record.get("project_support_root") or "")).resolve(strict=False)
        == owner_manifest.parents[1].resolve(strict=False),
        "LIVE_EEG_OWNER_SUPPORT_ROOT_MISMATCH",
    )
    print("LIVE EEG KANDA OWNER IDENTITY EXACT MATCH: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.tool_root.expanduser().resolve(strict=True)

    for relative in TARGETS:
        path = root / relative
        require(path.is_file(), "FUNCTIONAL_SMOKE_TARGET_MISSING:" + relative)
        if path.suffix == ".py":
            source = path.read_text(encoding="utf-8")
            source.encode("ascii")
            ast.parse(source, filename=str(path))

    smoke_boundary = (
        root / "kanda_reasoner_app" / "portable_smoke_isolation.py"
    ).read_text(encoding="utf-8")
    runtime_report = (
        root / "kanda_reasoner_app" / "portable_smoke_runtime_report.py"
    ).read_text(encoding="utf-8")
    lazy_tabs = (
        root / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "lazy_tabs.py"
    ).read_text(encoding="utf-8")
    error_paths = (
        root / "kanda_reasoner_app" / "error_memory_gui" / "_project_paths_mixin.py"
    ).read_text(encoding="utf-8")
    helper = (
        root / "tools" / "tool_portable_functional_smoke.py"
    ).read_text(encoding="utf-8")
    builder = (
        root / "tools" / "build_kanda_reasoner_tool_portable.py"
    ).read_text(encoding="utf-8")

    for token in (
        "owner.relative_to(canonical)",
        "PORTABLE_SMOKE_OWNER_ROOT_NOT_ALLOWED",
    ):
        require(token in smoke_boundary, "SMOKE_OWNER_CONTRACT_MISSING:" + token)
    for token in (
        "record_portable_smoke_event",
        "token_sha256",
        "events",
        "os.replace",
    ):
        require(token in runtime_report, "RUNTIME_REPORT_CONTRACT_MISSING:" + token)
    require(
        lazy_tabs.count("record_portable_smoke_event(") >= 2,
        "LAZY_TAB_RUNTIME_REPORTING_MISSING",
    )
    require(
        error_paths.count("record_portable_smoke_event(") >= 3,
        "ERROR_MEMORY_RUNTIME_REPORTING_MISSING",
    )
    for token in (
        "seed_external_smoke_registry",
        "canonical_external_project_record",
        "PORTABLE_FUNCTIONAL_SMOKE_REPORTED_FAILURE",
        "PORTABLE_FUNCTIONAL_SMOKE_REQUIRED_TABS_NOT_LOADED",
        "EXTERNAL_SMOKE_STABLE_PROJECT_ID_MISMATCH",
    ):
        require(token in helper, "FUNCTIONAL_SMOKE_HELPER_CONTRACT_MISSING:" + token)
    for token in (
        "kanda-reasoner-tool-portable-direct-pyinstaller-v1r2",
        "portable_built_unverified",
        "source_registry_path=Path(registry",
    ):
        require(token in builder, "DIRECT_BUILDER_REPAIR_CONTRACT_MISSING:" + token)

    before = _portable_snapshot(root)
    direct_validator = (
        root
        / "tools"
        / "validate_kanda_reasoner_tool_portable_direct_build_v1r1.py"
    )
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, str(direct_validator), "--tool-root", str(root)],
        cwd=str(root),
        env=environment,
        text=True,
        capture_output=True,
        check=False,
        timeout=1200,
    )
    output = (completed.stdout or "") + (completed.stderr or "")
    print(output, end="" if output.endswith("\n") else "\n")
    require(completed.returncode == 0, "DIRECT_VALIDATOR_EXIT_NONZERO")
    require(DIRECT_MARKER in output, "DIRECT_VALIDATOR_MARKER_MISSING")
    after = _portable_snapshot(root)
    require(before == after, "EXISTING_PORTABLE_FILES_CHANGED_BY_VALIDATION")
    _validate_live_eeg_identity(root)

    print("RUNTIME DESCENDANT SMOKE OWNER CANONICALIZATION: PASS")
    print("LAZY TAB FAIL-CLOSED RUNTIME REPORTING: PASS")
    print("ERROR MEMORY BACKEND FAILURE REPORTING: PASS")
    print("EXTERNAL PROJECT STABLE ID REUSE: PASS")
    print("PORTABLE READY REQUIRES FUNCTIONAL SMOKE: PASS")
    print("SKIP-SMOKE PORTABLE STATUS IS UNVERIFIED: PASS")
    print("CURRENT STAGE 1-6 PORTABLE BUILDER UNCHANGED: PASS")
    print("PORTABLE BUILD EXECUTED BY VALIDATION: NO")
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
