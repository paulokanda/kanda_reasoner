"""Validate the canonical no-Project direct-PyInstaller Tool build commands."""
from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

FEATURE_ID = "kanda-reasoner-tool-portable-direct-pyinstaller-v1r2"


def require(condition: bool, code: str) -> None:
    if not condition:
        raise RuntimeError(code)


def load_module(path: Path, name: str = "kanda_tool_portable_module"):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "MODULE_SPEC_FAILED")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    sys.path.insert(0, str(path.parent))
    try:
        spec.loader.exec_module(module)
    finally:
        try:
            sys.path.remove(str(path.parent))
        except ValueError:
            pass
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.tool_root.resolve()
    unload_py = root / "tools" / "unload_project_for_tool_portable.py"
    unload_ps1 = root / "tools" / "UNLOAD_PROJECT_FOR_TOOL_PORTABLE.ps1"
    build_py = root / "tools" / "build_kanda_reasoner_tool_portable.py"
    build_ps1 = root / "tools" / "BUILD_KANDA_REASONER_TOOL_PORTABLE.ps1"
    smoke_helper = root / "tools" / "tool_portable_functional_smoke.py"
    runtime_report = root / "kanda_reasoner_app" / "portable_smoke_runtime_report.py"
    smoke_boundary = root / "kanda_reasoner_app" / "portable_smoke_isolation.py"
    lazy_tabs = root / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "lazy_tabs.py"
    error_paths = root / "kanda_reasoner_app" / "error_memory_gui" / "_project_paths_mixin.py"
    for path in (
        unload_py,
        unload_ps1,
        build_py,
        build_ps1,
        smoke_helper,
        runtime_report,
        smoke_boundary,
        lazy_tabs,
        error_paths,
    ):
        require(path.is_file(), "TOOL_PORTABLE_BUILD_FILE_MISSING:" + str(path))

    for path in (
        unload_py,
        build_py,
        smoke_helper,
        runtime_report,
        smoke_boundary,
        lazy_tabs,
        error_paths,
    ):
        source = path.read_text(encoding="utf-8")
        source.encode("ascii")
        ast.parse(source, filename=str(path))

    unload_text = unload_ps1.read_text(encoding="utf-8")
    build_text = build_ps1.read_text(encoding="utf-8")
    builder_text = build_py.read_text(encoding="utf-8")
    require(
        build_text.index("& $Unload") < build_text.index("& $Python @Arguments"),
        "PROJECT_UNLOAD_NOT_FIRST_IN_BUILD_WRAPPER",
    )
    for token in (
        "--clean",
        "--noconfirm",
        "KandaReasonerWindows.spec",
        "require_unselected",
        "selected_project_during_build",
        "smoke_no_project",
        "smoke_external_project",
        "tool_portable_functional_smoke",
        "source_registry_path",
        "portable_built_unverified",
        "PROJECT CONTENT PACKAGED: NO",
    ):
        require(token in builder_text, "DIRECT_BUILDER_CONTRACT_MISSING:" + token)
    for token in (
        "SELECTED PROJECT: NONE",
        "SELF-HOSTING MODE: OFF",
        "UNLOAD PROJECT FOR TOOL PORTABLE: PASS",
    ):
        require(token in unload_py.read_text(encoding="utf-8"), "UNLOAD_MARKER_MISSING:" + token)

    module = load_module(unload_py, "kanda_tool_portable_unload")
    build_module = load_module(build_py, "kanda_tool_portable_build")
    smoke_module = load_module(smoke_helper, "kanda_tool_portable_functional_smoke")
    report_module = load_module(runtime_report, "kanda_portable_smoke_runtime_report")
    environment = {
        "PATH": "safe",
        "KANDA_REASONER_PROJECT_ROOT": "unsafe",
        "KANDA_OTHER": "unsafe",
        "PROJECT_REASONER_SCAN_ROOT": "unsafe",
    }
    removed = module.scrub_project_environment(environment)
    require(environment == {"PATH": "safe"}, "PROJECT_ENVIRONMENT_SCRUB_FAILED")
    require(len(removed) == 3, "PROJECT_ENVIRONMENT_SCRUB_COUNT_MISMATCH")

    with tempfile.TemporaryDirectory() as temporary:
        temp = Path(temporary)
        registry = temp / "projects.json"
        registry.write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "current_project_id": "project-1",
                    "projects": {
                        "project-1": {
                            "stable_project_id": "project-1",
                            "project_slug": "fixture",
                            "project_root": str(temp / "fixture"),
                            "project_root_fingerprint": "f" * 64,
                            "project_support_root": str(temp / "fixture_support"),
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
        before_projects = json.loads(registry.read_text(encoding="utf-8"))["projects"]
        evidence = module.clear_active_project(root, registry_path=registry)
        after = json.loads(registry.read_text(encoding="utf-8"))
        require(after["current_project_id"] == "", "FUNCTIONAL_UNLOAD_CURRENT_ID_REMAINS")
        require(after["projects"] == before_projects, "FUNCTIONAL_UNLOAD_HISTORY_CHANGED")
        require(evidence["self_hosting_after"] is False, "FUNCTIONAL_UNLOAD_SELF_HOSTING_REMAINS")

        fake_app = temp / "fake_app"
        fake_app.mkdir()
        (fake_app / "kanda_reasoner.exe").write_bytes(b"MZ")
        (fake_app / "_internal").mkdir()
        (fake_app / "_internal" / "runtime.dat").write_bytes(b"runtime")
        stage = build_module.stage_application(fake_app, temp / "stage_parent")
        archive = temp / "portable.zip"
        first_zip = build_module.create_deterministic_zip(stage, archive)
        first_bytes = archive.read_bytes()
        second_zip = build_module.create_deterministic_zip(stage, archive)
        require(archive.read_bytes() == first_bytes, "DETERMINISTIC_ZIP_BYTES_MISMATCH")
        require(first_zip["sha256"] == second_zip["sha256"], "DETERMINISTIC_ZIP_HASH_MISMATCH")
        forbidden = temp / "forbidden_app"
        forbidden.mkdir()
        (forbidden / "project_freeze_after_update").mkdir()
        try:
            build_module.assert_no_project_capture(forbidden)
        except RuntimeError as exc:
            require("PROJECT_OR_SUPPORT_CAPTURED" in str(exc), "PROJECT_CAPTURE_WRONG_ERROR")
        else:
            raise RuntimeError("PROJECT_CAPTURE_FIXTURE_ACCEPTED")

        report_root = temp / "runtime_report"
        report_path = report_root / "functional_smoke_report.json"
        token = "fixture-token"
        prior_environment = {
            report_module.PORTABLE_SMOKE_REPORT_PATH_ENV: os.environ.get(
                report_module.PORTABLE_SMOKE_REPORT_PATH_ENV
            ),
            report_module.PORTABLE_SMOKE_REPORT_ROOT_ENV: os.environ.get(
                report_module.PORTABLE_SMOKE_REPORT_ROOT_ENV
            ),
            report_module.PORTABLE_SMOKE_REPORT_TOKEN_ENV: os.environ.get(
                report_module.PORTABLE_SMOKE_REPORT_TOKEN_ENV
            ),
        }
        os.environ[report_module.PORTABLE_SMOKE_REPORT_PATH_ENV] = str(report_path)
        os.environ[report_module.PORTABLE_SMOKE_REPORT_ROOT_ENV] = str(report_root)
        os.environ[report_module.PORTABLE_SMOKE_REPORT_TOKEN_ENV] = token
        try:
            for source in (
                "kanda_reasoner_app/reasoner_context_collector/runner.py",
                "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window.py",
                "kanda_reasoner_app/error_memory_gui/error_memory_tab.py",
            ):
                report_module.record_portable_smoke_event(
                    status="PASS",
                    kind="lazy_tab",
                    source=source,
                    message="LOADED",
                )
            report_module.record_portable_smoke_event(
                status="PASS",
                kind="error_memory_state",
                source="selected_project",
                message="fixture",
            )
        finally:
            for key, value in prior_environment.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value
        report_result = smoke_module.validate_runtime_report(
            report_path,
            smoke_module._sha256_text(token),
            expected_error_memory_state="selected_project",
        )
        require(report_result["status"] == "PASS", "FUNCTIONAL_REPORT_FIXTURE_FAILED")

        source_registry = temp / "source_registry.json"
        project_root = temp / "external_project"
        project_root.mkdir()
        support_root = Path(project_root.anchor) / (
            project_root.name + "_show_project_to_AI"
        )
        stable_id = "794ec078-9a3e-4c2f-abab-3150dc2c727a"
        source_registry.write_text(
            json.dumps(
                {
                    "schema_version": "1.0",
                    "current_project_id": "",
                    "projects": {
                        stable_id: {
                            "stable_project_id": stable_id,
                            "project_slug": project_root.name,
                            "project_root": str(project_root),
                            "project_root_fingerprint": "9" * 64,
                            "project_support_root": str(support_root),
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
        target_registry = temp / "target_registry.json"
        seeded = smoke_module.seed_external_smoke_registry(
            target_registry,
            source_registry,
            project_root,
        )
        require(seeded == stable_id, "EXTERNAL_STABLE_ID_REUSE_FIXTURE_FAILED")
        seeded_payload = json.loads(target_registry.read_text(encoding="utf-8"))
        require(
            seeded_payload["current_project_id"] == stable_id,
            "EXTERNAL_STABLE_ID_CURRENT_SELECTION_FAILED",
        )

        boundary_module = load_module(
            smoke_boundary,
            "kanda_portable_smoke_isolation_boundary",
        )
        runtime_root = temp / "runtime"
        runtime_child = runtime_root / "_internal" / "kanda_reasoner_app"
        runtime_child.mkdir(parents=True)
        placeholder = temp / "placeholder"
        placeholder.mkdir()
        boundary = boundary_module.PortableSmokeIsolationBoundary(
            root=temp,
            runtime_root=runtime_root,
            project_root=placeholder,
            token_sha256="a" * 64,
        )
        require(
            boundary._require_owner(runtime_child) == runtime_root,
            "RUNTIME_DESCENDANT_OWNER_CANONICALIZATION_FAILED",
        )

    current_validator = root / "portable" / "validate_installed.py"
    completed = subprocess.run(
        [
            sys.executable,
            str(current_validator),
            "--portable-root",
            str(root / "portable"),
        ],
        cwd=str(root),
        text=True,
        capture_output=True,
        check=False,
        timeout=900,
    )
    output = (completed.stdout or "") + (completed.stderr or "")
    print(output, end="" if output.endswith("\n") else "\n")
    require(completed.returncode == 0, "CURRENT_STAGE_1_6_VALIDATOR_FAILED")
    require(
        "VALIDATION OK: kanda-reasoner-portable-builder-install-v1r12" in output,
        "CURRENT_STAGE_1_6_VALIDATOR_MARKER_MISSING",
    )

    print("TOOL PORTABLE PROJECT UNLOAD COMMAND: PASS")
    print("TOOL PORTABLE PROJECT HISTORY PRESERVATION: PASS")
    print("TOOL PORTABLE BUILD REQUIRES SELECTED PROJECT NONE: PASS")
    print("TOOL PORTABLE DIRECT PYINSTALLER CONTRACT: PASS")
    print("TOOL PORTABLE DETERMINISTIC ZIP FIXTURE: PASS")
    print("TOOL PORTABLE PROJECT CAPTURE REJECTION FIXTURE: PASS")
    print("TOOL PORTABLE FIRST SMOKE NO PROJECT: PASS")
    print("TOOL PORTABLE SECOND SMOKE EXTERNAL PROJECT: PASS")
    print("TOOL PORTABLE FUNCTIONAL RUNTIME REPORT: PASS")
    print("TOOL PORTABLE EXTERNAL STABLE PROJECT ID REUSE: PASS")
    print("TOOL PORTABLE RUNTIME DESCENDANT SMOKE OWNER: PASS")
    print("TOOL PORTABLE LEGACY SELF-HOSTING GATE UNCHANGED: PASS")
    print("TOOL PORTABLE PORTABLE BUILDER MANIFEST UNCHANGED: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
