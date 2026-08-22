"""Functional smoke evidence and canonical Project identity reuse helpers."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any

_TOOL_ROOT = Path(__file__).resolve().parents[1]
_TOOL_ROOT_TEXT = str(_TOOL_ROOT)
_TOOL_ROOT_WAS_PRESENT = _TOOL_ROOT_TEXT in sys.path
_PREVIOUS_DONT_WRITE_BYTECODE = sys.dont_write_bytecode
if not _TOOL_ROOT_WAS_PRESENT:
    sys.path.insert(0, _TOOL_ROOT_TEXT)
sys.dont_write_bytecode = True
try:
    from portable.packaged_worker_runtime import validate_packaged_worker_runtime
    from tool_portable_project_agnostic_smoke import (
        smoke_project_agnostic_startup_generation,
    )
finally:
    sys.dont_write_bytecode = _PREVIOUS_DONT_WRITE_BYTECODE
    if not _TOOL_ROOT_WAS_PRESENT:
        try:
            sys.path.remove(_TOOL_ROOT_TEXT)
        except ValueError:
            pass

__all__ = [
    "validate_runtime_report",
    "seed_external_smoke_registry",
    "smoke_no_project",
    "smoke_external_project",
    "smoke_project_agnostic_startup_generation",
]

SMOKE_REPORT_PATH_ENV = "KANDA_PORTABLE_SMOKE_RUNTIME_REPORT"
SMOKE_REPORT_ROOT_ENV = "KANDA_PORTABLE_SMOKE_RUNTIME_REPORT_ROOT"
SMOKE_REPORT_TOKEN_ENV = "KANDA_PORTABLE_SMOKE_RUNTIME_REPORT_TOKEN"
REQUIRED_LAZY_TAB_SOURCES = (
    "reasoner_context_collector",
    "ai_reasoner_main_window",
    "error_memory_gui",
)


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalized_path(path: str | Path) -> str:
    resolved = Path(path).expanduser().resolve(strict=False)
    return os.path.normcase(os.path.normpath(str(resolved)))


def prepare_runtime_report(
    environment: dict[str, str],
    root: Path,
    *,
    token: str,
) -> tuple[Path, str]:
    resolved = root.expanduser().resolve(strict=False)
    resolved.mkdir(parents=True, exist_ok=True)
    report = resolved / "functional_smoke_report.json"
    report.unlink(missing_ok=True)
    environment.update(
        {
            SMOKE_REPORT_PATH_ENV: str(report),
            SMOKE_REPORT_ROOT_ENV: str(resolved),
            SMOKE_REPORT_TOKEN_ENV: token,
        }
    )
    return report, _sha256_text(token)


def read_runtime_report(path: Path, expected_token_sha256: str) -> dict[str, Any]:
    if not path.is_file():
        raise RuntimeError("PORTABLE_FUNCTIONAL_SMOKE_REPORT_MISSING:" + str(path))
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(
            "PORTABLE_FUNCTIONAL_SMOKE_REPORT_UNREADABLE:" + str(path)
        ) from exc
    if not isinstance(payload, dict):
        raise RuntimeError("PORTABLE_FUNCTIONAL_SMOKE_REPORT_NOT_OBJECT")
    if payload.get("schema_version") != "1.0":
        raise RuntimeError("PORTABLE_FUNCTIONAL_SMOKE_REPORT_SCHEMA_MISMATCH")
    if payload.get("token_sha256") != expected_token_sha256:
        raise RuntimeError("PORTABLE_FUNCTIONAL_SMOKE_REPORT_TOKEN_MISMATCH")
    events = payload.get("events")
    if not isinstance(events, list):
        raise RuntimeError("PORTABLE_FUNCTIONAL_SMOKE_EVENTS_INVALID")
    return payload


def validate_runtime_report(
    path: Path,
    expected_token_sha256: str,
    *,
    expected_error_memory_state: str,
) -> dict[str, Any]:
    payload = read_runtime_report(path, expected_token_sha256)
    events = payload["events"]
    failures = [
        event for event in events
        if isinstance(event, dict)
        and str(event.get("status") or "").strip().upper() == "FAIL"
    ]
    if failures:
        first = failures[0]
        raise RuntimeError(
            "PORTABLE_FUNCTIONAL_SMOKE_REPORTED_FAILURE:"
            + str(first.get("kind") or "")
            + ":"
            + str(first.get("source") or "")
            + ":"
            + str(first.get("message") or "")[:1000]
        )

    lazy_sources = {
        str(event.get("source") or "").replace("\\", "/").casefold()
        for event in events
        if isinstance(event, dict)
        and str(event.get("status") or "").strip().upper() == "PASS"
        and str(event.get("kind") or "").strip() == "lazy_tab"
    }
    missing = [
        fragment for fragment in REQUIRED_LAZY_TAB_SOURCES
        if not any(fragment.casefold() in source for source in lazy_sources)
    ]
    if missing:
        raise RuntimeError(
            "PORTABLE_FUNCTIONAL_SMOKE_REQUIRED_TABS_NOT_LOADED:"
            + ",".join(missing)
        )

    state_found = any(
        isinstance(event, dict)
        and str(event.get("status") or "").strip().upper() == "PASS"
        and str(event.get("kind") or "").strip() == "error_memory_state"
        and str(event.get("source") or "").strip() == expected_error_memory_state
        for event in events
    )
    if not state_found:
        raise RuntimeError(
            "PORTABLE_FUNCTIONAL_SMOKE_ERROR_MEMORY_STATE_MISSING:"
            + expected_error_memory_state
        )
    return {
        "report_path": str(path),
        "event_count": len(events),
        "required_lazy_tabs": list(REQUIRED_LAZY_TAB_SOURCES),
        "error_memory_state": expected_error_memory_state,
        "status": "PASS",
    }


def canonical_external_project_record(
    source_registry_path: Path,
    project_root: Path,
) -> tuple[str, dict[str, Any]]:
    try:
        payload = json.loads(source_registry_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(
            "SOURCE_TOOL_REGISTRY_UNREADABLE:" + str(source_registry_path)
        ) from exc
    projects = payload.get("projects")
    if not isinstance(projects, dict):
        raise RuntimeError("SOURCE_TOOL_REGISTRY_PROJECTS_INVALID")
    expected_root = normalized_path(project_root)
    matches: list[tuple[str, dict[str, Any]]] = []
    for key, value in projects.items():
        if not isinstance(value, dict):
            continue
        if normalized_path(str(value.get("project_root") or "")) == expected_root:
            matches.append((str(key), dict(value)))
    if len(matches) != 1:
        raise RuntimeError(
            "SOURCE_TOOL_REGISTRY_EXTERNAL_PROJECT_MATCH_COUNT:"
            + str(len(matches))
        )
    stable_id, record = matches[0]
    if str(record.get("stable_project_id") or "") != stable_id:
        raise RuntimeError("SOURCE_TOOL_REGISTRY_STABLE_ID_MISMATCH")
    if str(record.get("selection_mode") or "") != "EXPLICIT_EXTERNAL_PROJECT":
        raise RuntimeError("SOURCE_TOOL_REGISTRY_EXTERNAL_MODE_MISMATCH")
    if len(str(record.get("project_root_fingerprint") or "")) != 64:
        raise RuntimeError("SOURCE_TOOL_REGISTRY_FINGERPRINT_INVALID")
    expected_support = (
        Path(project_root.anchor)
        / f"{project_root.name}_show_project_to_AI"
    ).resolve(strict=False)
    if normalized_path(str(record.get("project_support_root") or "")) != normalized_path(
        expected_support
    ):
        raise RuntimeError("SOURCE_TOOL_REGISTRY_SUPPORT_ROOT_MISMATCH")
    return stable_id, record


def seed_external_smoke_registry(
    target_registry_path: Path,
    source_registry_path: Path,
    project_root: Path,
) -> str:
    stable_id, record = canonical_external_project_record(
        source_registry_path,
        project_root,
    )
    target_registry_path.parent.mkdir(parents=True, exist_ok=True)
    target_registry_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "current_project_id": stable_id,
                "projects": {stable_id: record},
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return stable_id

TOP_LEVEL_NAME = "KandaReasoner-Windows-Portable"
PRODUCT_EXE = "kanda_reasoner.exe"
PROJECT_ENV = "KANDA_REASONER_PROJECT_ROOT"
SMOKE_ENABLED_ENV = "KANDA_PORTABLE_SMOKE_ISOLATION_ENABLED"
SMOKE_ROOT_ENV = "KANDA_PORTABLE_SMOKE_ISOLATION_ROOT"
SMOKE_TOKEN_ENV = "KANDA_PORTABLE_SMOKE_ISOLATION_TOKEN"
SMOKE_MARKER = "KANDA_PORTABLE_SMOKE_ISOLATION.json"
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


def _clean_environment() -> dict[str, str]:
    environment = {
        key: value
        for key, value in os.environ.items()
        if key not in SCRUB_NAMES
        and not any(key.startswith(prefix) for prefix in SCRUB_PREFIXES)
    }
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return environment


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _profile_environment(base: Path) -> dict[str, str]:
    environment = _clean_environment()
    profile = base / "profile"
    appdata = profile / "AppData" / "Roaming"
    localappdata = profile / "AppData" / "Local"
    temp = base / "temp"
    cache = base / "cache"
    for directory in (profile, appdata, localappdata, temp, cache):
        directory.mkdir(parents=True, exist_ok=True)
    environment.update(
        {
            "APPDATA": str(appdata),
            "LOCALAPPDATA": str(localappdata),
            "USERPROFILE": str(profile),
            "HOME": str(profile),
            "TEMP": str(temp),
            "TMP": str(temp),
            "XDG_CONFIG_HOME": str(profile / "xdg_config"),
            "XDG_DATA_HOME": str(profile / "xdg_data"),
            "XDG_CACHE_HOME": str(cache),
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONPYCACHEPREFIX": str(cache / "pycache"),
        }
    )
    return environment


def _launch(executable: Path, environment: dict[str, str], message: str) -> None:
    print(message)
    completed = subprocess.run(
        [str(executable)],
        cwd=str(executable.parent),
        env=environment,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "PACKAGED_GUI_EXIT_NONZERO:" + str(completed.returncode)
        )



def _validate_worker_reentry(
    executable: Path,
    environment: dict[str, str],
) -> None:
    validate_packaged_worker_runtime(
        executable.parent,
        executable,
        environment=environment,
    )
    print("PACKAGED TOOL WORKER REENTRY: PASS")


def smoke_no_project(zip_path: Path, run_root: Path) -> dict[str, Any]:
    root = run_root / "smoke_no_project"
    extract = root / "extract"
    project_placeholder = root / "projects" / "unselected_placeholder"
    project_placeholder.mkdir(parents=True)
    with zipfile.ZipFile(zip_path, "r") as archive:
        archive.extractall(extract)
    runtime = extract / TOP_LEVEL_NAME
    executable = runtime / PRODUCT_EXE
    token = hashlib.sha256(os.urandom(32)).hexdigest()
    marker = {
        "schema_version": "1.0",
        "root": str(root.resolve(strict=False)),
        "runtime_root": str(runtime.resolve(strict=False)),
        "project_root": str(project_placeholder.resolve(strict=False)),
        "token_sha256": hashlib.sha256(token.encode("utf-8")).hexdigest(),
    }
    _write_json(root / SMOKE_MARKER, marker)
    environment = _profile_environment(root)
    environment.update(
        {
            SMOKE_ENABLED_ENV: "1",
            SMOKE_ROOT_ENV: str(root.resolve(strict=False)),
            SMOKE_TOKEN_ENV: token,
        }
    )
    report_path, report_token_sha256 = prepare_runtime_report(
        environment,
        root,
        token=hashlib.sha256(os.urandom(32)).hexdigest(),
    )
    environment.pop(PROJECT_ENV, None)
    _validate_worker_reentry(executable, environment)
    _launch(
        executable,
        environment,
        "FIRST GUI SMOKE: required tabs auto-load. Verify Project is NONE and "
        "the GUI is responsive, then close the Tool normally.",
    )
    functional = validate_runtime_report(
        report_path,
        report_token_sha256,
        expected_error_memory_state="no_project",
    )
    registry = (
        root
        / "tool_support"
        / f"{TOP_LEVEL_NAME}_show_project_to_AI"
        / "tool_project_registry"
        / "projects.json"
    )
    if registry.is_file():
        payload = json.loads(registry.read_text(encoding="utf-8"))
        if str(payload.get("current_project_id") or "").strip():
            raise RuntimeError("FIRST_SMOKE_SELECTED_PROJECT_NOT_NONE")
    print("PACKAGED TOOL FIRST LAUNCH SELECTED PROJECT NONE: PASS")
    print("PACKAGED TOOL FIRST FUNCTIONAL TAB SMOKE: PASS")
    return {
        "selected_project": None,
        "isolated": True,
        "functional_smoke": functional,
    }


def smoke_external_project(
    stage: Path,
    external_project: Path,
    run_root: Path,
    *,
    source_registry_path: Path,
) -> dict[str, Any]:
    project = external_project.expanduser().resolve(strict=False)
    if not project.is_dir():
        raise RuntimeError("EXTERNAL_SMOKE_PROJECT_MISSING:" + str(project))
    executable = stage / PRODUCT_EXE
    profile_root = run_root / "smoke_external_project_profile"
    environment = _profile_environment(profile_root)
    environment[PROJECT_ENV] = str(project)
    drive = Path(stage.anchor).resolve()
    tool_support = drive / f"{stage.name}_show_project_to_AI"
    registry = tool_support / "tool_project_registry" / "projects.json"
    expected_project_id = seed_external_smoke_registry(
        registry,
        source_registry_path,
        project,
    )
    report_token = hashlib.sha256(os.urandom(32)).hexdigest()
    report_path, report_token_sha256 = prepare_runtime_report(
        environment,
        profile_root,
        token=report_token,
    )
    _validate_worker_reentry(executable, environment)
    _launch(
        executable,
        environment,
        "SECOND GUI SMOKE: required tabs auto-load. Verify the explicitly selected "
        "external Project and real JSON; optionally inspect Project Structure 3D, "
        "then close normally.",
    )
    functional = validate_runtime_report(
        report_path,
        report_token_sha256,
        expected_error_memory_state="selected_project",
    )
    if not registry.is_file():
        raise RuntimeError("EXTERNAL_SMOKE_TOOL_REGISTRY_MISSING:" + str(registry))
    payload = json.loads(registry.read_text(encoding="utf-8"))
    current = str(payload.get("current_project_id") or "").strip()
    if current != expected_project_id:
        raise RuntimeError(
            "EXTERNAL_SMOKE_STABLE_PROJECT_ID_MISMATCH:"
            + current
            + ";expected="
            + expected_project_id
        )
    projects = payload.get("projects")
    record = projects.get(current) if current and isinstance(projects, dict) else None
    if not isinstance(record, dict):
        raise RuntimeError("EXTERNAL_SMOKE_ACTIVE_RECORD_MISSING")
    actual = Path(str(record.get("project_root") or "")).resolve(strict=False)
    if actual != project:
        raise RuntimeError(
            "EXTERNAL_SMOKE_PROJECT_ROOT_MISMATCH:"
            + str(actual)
            + ";expected="
            + str(project)
        )
    if str(record.get("selection_mode") or "") != "EXPLICIT_EXTERNAL_PROJECT":
        raise RuntimeError("EXTERNAL_SMOKE_SELECTION_MODE_MISMATCH")
    print("PACKAGED TOOL EXTERNAL PROJECT: PASS")
    print("PACKAGED TOOL EXTERNAL PROJECT STABLE ID REUSE: PASS")
    print("PACKAGED TOOL SECOND FUNCTIONAL TAB SMOKE: PASS")
    print("TOOL/PROJECT DISTINCTION: PASS")
    return {
        "selected_project": str(project),
        "stable_project_id": expected_project_id,
        "selection_mode": "EXPLICIT_EXTERNAL_PROJECT",
        "tool_support_root": str(tool_support),
        "functional_smoke": functional,
    }
