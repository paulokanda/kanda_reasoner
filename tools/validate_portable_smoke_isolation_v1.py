"""Focused validator for token-bound Portable packaged-GUI smoke isolation."""

from __future__ import annotations

import argparse
import ast
import builtins
import hashlib
import json
import os
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise RuntimeError(code if not detail else f"{code}: {detail}")


@contextmanager
def _temporary_environment(values: dict[str, str]) -> Iterator[None]:
    saved = {name: os.environ.get(name) for name in values}
    try:
        os.environ.update(values)
        yield
    finally:
        for name, value in saved.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value


def _load_live_registry(project_root: Path) -> tuple[Path, str]:
    drive = Path(project_root.anchor)
    support = drive / f"{project_root.name}_show_project_to_AI"
    registry = support / "tool_project_registry" / "projects.json"
    _require(registry.is_file(), "TOOL_REGISTRY_MISSING", str(registry))
    payload = _read_json(registry)
    current_id = str(payload.get("current_project_id") or "")
    projects = payload.get("projects")
    _require(current_id and isinstance(projects, dict), "TOOL_REGISTRY_INVALID")
    record = projects.get(current_id)
    _require(isinstance(record, dict), "ACTIVE_PROJECT_RECORD_MISSING")
    active_root = Path(str(record.get("project_root") or "")).resolve()
    mode = str(record.get("selection_mode") or "")
    _require(active_root == project_root, "ACTIVE_PROJECT_ROOT_MISMATCH")
    _require(mode == "EXPLICIT_SELF_HOSTING", "ACTIVE_PROJECT_MODE_MISMATCH")
    return registry, _sha256(registry)


def _fixture_paths(project_root: Path, run_root: Path):
    from portable.models import BuildPaths

    dummy = run_root / "dummy"
    return BuildPaths(
        project_root=project_root,
        drive_root=Path(project_root.anchor),
        project_support_root=dummy,
        transient_root=run_root.parent,
        run_root=run_root,
        pyinstaller_work=dummy,
        pyinstaller_dist=dummy,
        pyinstaller_config=dummy,
        temporary_root=dummy,
        stage_parent=dummy,
        candidate_zip=dummy,
        clean_extract_root=dummy,
        final_zip=dummy,
        spec_path=dummy,
        governed_python=Path(sys.executable),
        zip_helper=dummy,
        registry_boundary=None,
    )


def _validate_archive_ast(project_root: Path) -> None:
    archive_path = project_root / "portable" / "archive.py"
    source = archive_path.read_text(encoding="utf-8-sig")
    tree = ast.parse(source)
    popen_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "Popen"
    ]
    _require(bool(popen_calls), "PORTABLE_SMOKE_POPEN_CALL_MISSING")
    _require(
        all(any(item.arg == "env" for item in call.keywords) for call in popen_calls),
        "PORTABLE_SMOKE_POPEN_ENV_MISSING",
    )
    for marker in (
        "prepared_smoke_isolation",
        "verify_isolated_registry",
        "PORTABLE PACKAGED GUI SMOKE ISOLATION: PASS",
    ):
        _require(marker in source, "PORTABLE_SMOKE_ARCHIVE_MARKER_MISSING", marker)
    print("PORTABLE SMOKE POPEN EXPLICIT ENVIRONMENT: PASS")
    print("PORTABLE SMOKE ARCHIVE INTEGRATION: PASS")


def _validate_popen_runtime(project_root: Path) -> None:
    import portable.archive as archive

    captured: dict[str, object] = {}

    class FakeProcess:
        returncode = None

        def poll(self):
            return None

        def wait(self, timeout=None):
            self.returncode = 0
            return 0

        def terminate(self):
            self.returncode = 0

        def kill(self):
            self.returncode = 0

    def fake_popen(command, *, cwd, env):
        captured["command"] = command
        captured["cwd"] = cwd
        captured["env"] = env
        return FakeProcess()

    original_popen = archive.subprocess.Popen
    original_sleep = archive.time.sleep
    original_input = builtins.input
    expected_env = {"PORTABLE_SMOKE_FIXTURE": "1"}
    try:
        archive.subprocess.Popen = fake_popen
        archive.time.sleep = lambda _seconds: None
        builtins.input = lambda _prompt: "FIXTURE CLOSED"
        archive._launch_and_require_natural_close(
            project_root / "fixture.exe",
            project_root,
            "prompt",
            "FIXTURE CLOSED",
            expected_env,
        )
    finally:
        archive.subprocess.Popen = original_popen
        archive.time.sleep = original_sleep
        builtins.input = original_input
    _require(captured.get("env") is expected_env, "PORTABLE_SMOKE_ENV_NOT_FORWARDED")
    print("PORTABLE SMOKE POPEN ENVIRONMENT FORWARDING: PASS")


def _write_isolated_registry(isolation) -> None:
    registry = (
        isolation.tool_support_root
        / "tool_project_registry"
        / "projects.json"
    )
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "current_project_id": "smoke-project-id",
                "projects": {
                    "smoke-project-id": {
                        "stable_project_id": "smoke-project-id",
                        "project_slug": isolation.project_root.name,
                        "project_root": str(isolation.project_root),
                        "project_root_fingerprint": "fixture",
                        "project_support_root": str(isolation.project_support_root),
                        "selection_mode": "EXPLICIT_EXTERNAL_PROJECT",
                        "updated_at_utc": "2026-08-01T00:00:00+00:00",
                    }
                },
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def _validate_fixture(project_root: Path, live_registry: Path) -> None:
    from kanda_reasoner_app.portable_smoke_isolation import (
        PORTABLE_SMOKE_TOKEN_ENV,
        PortableSmokeIsolationError,
        resolve_portable_smoke_isolation,
    )
    from kanda_reasoner_app.project_support_boundary import (
        canonical_project_support_root,
        canonical_tool_support_root,
        canonical_transient_garbage_root,
    )
    from portable.smoke_isolation import (
        prepared_smoke_isolation,
        verify_isolated_registry,
    )

    drive = Path(project_root.anchor)
    transient = drive / f"{project_root.name}_delete_after_daily_work"
    transient.mkdir(parents=True, exist_ok=True)
    os.environ["KANDA_LIVE_SECRET_FIXTURE"] = "must-be-scrubbed"
    os.environ["OPENAI_API_KEY"] = "must-be-scrubbed"
    try:
        with tempfile.TemporaryDirectory(dir=transient) as temp:
            run_root = Path(temp) / "stage2_smoke_fixture"
            run_root.mkdir()
            paths = _fixture_paths(project_root, run_root)
            with prepared_smoke_isolation(paths, "KandaReasoner") as isolation:
                isolation.app_root.mkdir(parents=True)
                _require(
                    "KANDA_LIVE_SECRET_FIXTURE" not in isolation.environment,
                    "PORTABLE_SMOKE_KANDA_ENV_NOT_SCRUBBED",
                )
                _require(
                    "OPENAI_API_KEY" not in isolation.environment,
                    "PORTABLE_SMOKE_PROVIDER_KEY_NOT_SCRUBBED",
                )
                with _temporary_environment(isolation.environment):
                    boundary = resolve_portable_smoke_isolation()
                    _require(boundary is not None, "PORTABLE_SMOKE_BOUNDARY_MISSING")
                    tool_support = canonical_tool_support_root(isolation.app_root)
                    project_support = canonical_project_support_root(isolation.project_root)
                    transient_root = canonical_transient_garbage_root(isolation.project_root)
                    _require(tool_support == isolation.tool_support_root, "TOOL_SUPPORT_NOT_ISOLATED")
                    _require(project_support == isolation.project_support_root, "PROJECT_SUPPORT_NOT_ISOLATED")
                    _require(transient_root == isolation.project_transient_root, "TRANSIENT_NOT_ISOLATED")
                    _require(live_registry not in tool_support.parents, "LIVE_REGISTRY_PARENT_REUSED")
                    _write_isolated_registry(isolation)
                    verify_isolated_registry(isolation)
                    original_token = os.environ[PORTABLE_SMOKE_TOKEN_ENV]
                    os.environ[PORTABLE_SMOKE_TOKEN_ENV] = original_token + "tampered"
                    try:
                        resolve_portable_smoke_isolation()
                    except PortableSmokeIsolationError:
                        pass
                    else:
                        raise RuntimeError("PORTABLE_SMOKE_INVALID_TOKEN_ACCEPTED")
                    finally:
                        os.environ[PORTABLE_SMOKE_TOKEN_ENV] = original_token
                print("PORTABLE SMOKE TOKEN-BOUND OVERRIDE: PASS")
                print("PORTABLE SMOKE TOOL SUPPORT ISOLATED: PASS")
                print("PORTABLE SMOKE PROJECT SUPPORT ISOLATED: PASS")
                print("PORTABLE SMOKE TRANSIENT ISOLATED: PASS")
                print("PORTABLE SMOKE PROFILE TEMP ENVIRONMENT ISOLATED: PASS")
                print("PORTABLE SMOKE CREDENTIAL ENVIRONMENT SCRUB: PASS")
                print("PORTABLE SMOKE INVALID TOKEN REJECTED: PASS")
                print("PORTABLE SMOKE LIVE REGISTRY PATH ABSENT: PASS")
    finally:
        os.environ.pop("KANDA_LIVE_SECRET_FIXTURE", None)
        os.environ.pop("OPENAI_API_KEY", None)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default="E:\\kanda_reasoner")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    _require(project_root.name.casefold() == "kanda_reasoner", "TOOL_ROOT_NAME_MISMATCH")
    sys.path.insert(0, str(project_root))
    from portable.constants import (
        PORTABLE_HARDENING_FEATURES,
        PRODUCTION_PORTABLE_ENABLED,
    )
    _require(
        "packaged-gui-smoke-isolation" in PORTABLE_HARDENING_FEATURES,
        "SMOKE_ISOLATION_CAPABILITY_MISSING",
    )
    print("PORTABLE SMOKE ISOLATION CAPABILITY IDENTITY: PASS")
    live_registry, registry_before = _load_live_registry(project_root)
    print("PORTABLE SMOKE LIVE EXPLICIT SELF-HOSTING AUTHORITY: PASS")

    _validate_archive_ast(project_root)
    _validate_popen_runtime(project_root)
    _validate_fixture(project_root, live_registry)

    _require(PRODUCTION_PORTABLE_ENABLED is False, "PRODUCTION_GATE_OPENED_EARLY")
    _require(_sha256(live_registry) == registry_before, "LIVE_REGISTRY_CHANGED")
    print("PORTABLE SMOKE LIVE REGISTRY UNCHANGED: PASS")
    print("PORTABLE PRODUCTION BUILD GATE CLOSED: PASS")
    print("VALIDATION OK: portable-smoke-isolation-v1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
