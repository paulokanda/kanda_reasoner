# project-path: tools/validate_engineering_safety_source_hygiene_ruff_quality_v1.py
"""Focused validation for the Engineering Safety Ruff quality action."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import sys
from typing import Iterator
from zipfile import ZipFile

FEATURE_ID = "engineering-safety-source-hygiene-ruff-quality-v1"
EXPECTED_PATCH_FILES = {
    "KANDA_FREEZE_HINT.json",
    "KANDA_ERROR_LESSON_JSON_ruff_quality_project_exclusion_scope_v1.txt",
    "KANDA_ERROR_LESSON_JSON_ruff_quality_formatter_scope_cli_compatibility_v1.txt",
    "kanda_reasoner_app/source_hygiene/ruff_quality.py",
    "kanda_reasoner_app/source_hygiene/ruff_quality_scope.py",
    "tools/validate_engineering_safety_source_hygiene_ruff_quality_v1.py",
}
TOUCHED_PYTHON_FILES = tuple(
    sorted(path for path in EXPECTED_PATCH_FILES if path.endswith(".py"))
)


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def _write_fake_ruff_module(parent: Path) -> Path:
    package = parent / "ruff"
    package.mkdir(parents=True, exist_ok=True)
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "__main__.py").write_text(
        """import json
import sys

args = sys.argv[1:]


def require_flag(flag):
    if flag not in args:
        print("missing required flag: " + flag, file=sys.stderr)
        raise SystemExit(9)


def require_pair(flag, value):
    require_flag(flag)
    index = args.index(flag)
    if index + 1 >= len(args) or args[index + 1] != value:
        print("invalid flag value: " + flag, file=sys.stderr)
        raise SystemExit(9)


def forbid_flag(flag):
    if flag in args:
        print("forbidden mutating flag: " + flag, file=sys.stderr)
        raise SystemExit(9)


def require_config_exclusion(pattern):
    values = [
        args[index + 1]
        for index, value in enumerate(args[:-1])
        if value == "--config"
    ]
    quoted = '"' + pattern + '"'
    if not any("extend-exclude" in value and quoted in value for value in values):
        print("missing config exclusion: " + pattern, file=sys.stderr)
        raise SystemExit(9)


def require_global_config_before(command):
    require_flag("--config")
    if args.index("--config") > args.index(command):
        print("config override must precede subcommand", file=sys.stderr)
        raise SystemExit(9)


if args == ["--version"]:
    print("ruff 0.15.20")
    raise SystemExit(0)
if "check" in args:
    require_global_config_before("check")
    require_pair("--output-format", "json")
    require_pair("--color", "never")
    require_flag("--exit-zero")
    require_flag("--no-cache")
    require_flag("--force-exclude")
    require_config_exclusion(".project_reference")
    require_config_exclusion("snippets")
    forbid_flag("--extend-exclude")
    forbid_flag("--fix")
    forbid_flag("--fix-only")
    forbid_flag("--unsafe-fixes")
    root = args[-1]
    print(json.dumps([{
        "code": "F401",
        "message": "os imported but unused",
        "filename": root + "/sample.py",
        "location": {"row": 1, "column": 1},
        "fix": {"applicability": "safe"}
    }]))
    raise SystemExit(0)
if "format" in args:
    require_global_config_before("format")
    require_pair("--color", "never")
    require_flag("--check")
    require_flag("--no-cache")
    require_flag("--force-exclude")
    require_config_exclusion(".project_reference")
    require_config_exclusion("snippets")
    forbid_flag("--extend-exclude")
    forbid_flag("--diff")
    if "--output-format" in args:
        raise SystemExit(44)
    root = args[-1]
    print("Would reformat: " + root + "/sample.py")
    print("1 file would be reformatted")
    raise SystemExit(1)
raise SystemExit(2)
""",
        encoding="utf-8",
        newline="\n",
    )
    return parent


@contextmanager
def _temporary_environment(**updates: str) -> Iterator[None]:
    original = {key: os.environ.get(key) for key in updates}
    try:
        for key, value in updates.items():
            os.environ[key] = value
        yield
    finally:
        for key, value in original.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def _validate_patch_zip(path: Path) -> None:
    _assert(path.is_file(), "PATCH_ZIP_MISSING")
    with ZipFile(path) as archive:
        members = archive.namelist()
        names = set(members)
        _assert(len(members) == len(names), "PATCH_ZIP_DUPLICATE_MEMBER")
        _assert(names == EXPECTED_PATCH_FILES, "PATCH_ZIP_FILE_SET_MISMATCH")
        payload = json.loads(archive.read("KANDA_FREEZE_HINT.json"))
    _assert(payload.get("feature_id") == FEATURE_ID, "FREEZE_HINT_FEATURE_ID_MISMATCH")
    _assert(
        payload.get("freeze_readiness") == "requires_local_validation",
        "FREEZE_HINT_READINESS_MISMATCH",
    )
    _assert(
        payload.get("local_validation_status") == "not_run",
        "FREEZE_HINT_LOCAL_STATUS_MISMATCH",
    )
    summary = str(payload.get("validation_evidence_summary") or "")
    forbidden_markers = ("validation ok:", "local validation passed")
    _assert(
        not any(
            line.strip().casefold().startswith(forbidden_markers)
            for line in summary.splitlines()
        ),
        "FREEZE_HINT_INVENTED_LOCAL_VALIDATION",
    )
    print("PATCH_ZIP_CONTRACT: PASS")
    print("ZIP CONTRACT: PASS")


def _validate_source(project_root: Path) -> None:
    for relative in TOUCHED_PYTHON_FILES:
        path = project_root / relative
        _assert(path.is_file(), "TOUCHED_FILE_MISSING:" + relative)
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        _assert(_line_count(path) < 500, "MODULE_SIZE_LIMIT_EXCEEDED:" + relative)
    print("PYTHON_COMPILE: PASS")
    print("MODULE_SIZE_LAW_BELOW_500: PASS")


def _validate_catalog_and_cli(project_root: Path) -> None:
    sys.path.insert(0, str(project_root))
    try:
        import reasoner_tools_gui_engineering_safety_panel as panel
        from kanda_reasoner_app.safety_suite_cli.commands import (
            available_cli_commands,
        )

        matches = [
            item
            for item in panel.get_engineering_safety_panel_catalog()
            if item.command_name == "ruff-quality"
        ]
        _assert(len(matches) == 1, "RUFF_QUALITY_GUI_ENTRY_COUNT")
        _assert(matches[0].section == "Source Hygiene", "RUFF_QUALITY_GUI_SECTION")
        args = panel.build_engineering_safety_panel_cli_args(
            "ruff-quality",
            str(project_root),
        )
        _assert(
            list(args) == ["ruff-quality", "--root", str(project_root)],
            "RUFF_QUALITY_GUI_ARGS",
        )
        _assert("ruff-quality" in available_cli_commands(), "RUFF_QUALITY_CLI_CATALOG")
    finally:
        if sys.path and sys.path[0] == str(project_root):
            sys.path.pop(0)
    print("RUFF_QUALITY_GUI_CATALOG: PASS")
    print("RUFF_QUALITY_CLI_ROUTE: PASS")


def _validate_read_only_execution(project_root: Path, workspace: Path) -> None:
    fake_modules = _write_fake_ruff_module(workspace / "fake_modules")
    sample_root = workspace / "sample_project"
    sample_root.mkdir(parents=True, exist_ok=True)
    sample = sample_root / "sample.py"
    sample.write_text("import os\nprint( 1 )\n", encoding="utf-8", newline="\n")
    reference = sample_root / ".project_reference" / "broken.py"
    snippet = sample_root / "snippets" / "broken.py"
    reference.parent.mkdir(parents=True, exist_ok=True)
    snippet.parent.mkdir(parents=True, exist_ok=True)
    reference.write_text("value =\n", encoding="utf-8", newline="\n")
    snippet.write_text("other =\n", encoding="utf-8", newline="\n")
    before = {path: _sha256(path) for path in (sample, reference, snippet)}

    sys.path.insert(0, str(project_root))
    try:
        from kanda_reasoner_app.safety_suite_cli.commands import run_cli
        from kanda_reasoner_app.source_hygiene.ruff_quality import (
            build_ruff_quality_report,
        )

        current_pythonpath = os.environ.get("PYTHONPATH", "")
        new_pythonpath = str(fake_modules)
        if current_pythonpath:
            new_pythonpath += os.pathsep + current_pythonpath
        scope_rules = json.dumps({"folders": ["snippets"]})
        with _temporary_environment(
            PATH="",
            PYTHONPATH=new_pythonpath,
            PROJECT_REASONER_IGNORE_RULES_JSON=scope_rules,
        ):
            report = build_ruff_quality_report(sample_root)
            output = io.StringIO()
            error = io.StringIO()
            status = run_cli(
                ["ruff-quality", "--root", str(sample_root)],
                stdout=output,
                stderr=error,
            )
    finally:
        if sys.path and sys.path[0] == str(project_root):
            sys.path.pop(0)

    data = report.to_dict()
    codes = {item["code"] for item in data["findings"]}
    _assert("F401" in codes, "RUFF_LINT_FINDING_NOT_PARSED")
    _assert("RUFF_FORMAT_REQUIRED" in codes, "RUFF_FORMAT_FINDING_NOT_PARSED")
    _assert("ruff 0.15.20" in data["summary"], "RUFF_VERSION_NOT_RECORDED")
    _assert(status == 0, "RUFF_QUALITY_CLI_STATUS")
    _assert("Report type: ruff_quality" in output.getvalue(), "RUFF_QUALITY_CLI_OUTPUT")
    _assert(not error.getvalue().strip(), "RUFF_QUALITY_CLI_STDERR")
    _assert(
        all(_sha256(path) == digest for path, digest in before.items()),
        "RUFF_QUALITY_MUTATED_SOURCE",
    )
    _assert(not (sample_root / ".ruff_cache").exists(), "RUFF_CACHE_LEAKED_TO_PROJECT")
    inputs = set(data.get("input_sources") or [])
    _assert(
        "ruff_scope_policy:project_exclusion_policy" in inputs,
        "RUFF_SCOPE_POLICY_EVIDENCE_MISSING",
    )
    _assert(
        any(str(item).startswith("ruff_scope_fingerprint:") for item in inputs),
        "RUFF_SCOPE_FINGERPRINT_MISSING",
    )
    print("RUFF_QUALITY_PROJECT_EXCLUSION_SCOPE: PASS")
    print("RUFF_QUALITY_FORMAT_SCOPE_CLI_COMPATIBILITY: PASS")
    print("RUFF_QUALITY_LINT_PARSE: PASS")
    print("RUFF_QUALITY_FORMAT_PARSE: PASS")
    print("RUFF_QUALITY_COMMAND_CONTRACT: PASS")
    print("RUFF_QUALITY_READ_ONLY: PASS")
    print("RUFF_QUALITY_NO_PROJECT_CACHE: PASS")


def _validate_unavailable(project_root: Path, workspace: Path) -> None:
    sys.path.insert(0, str(project_root))
    try:
        from kanda_reasoner_app.source_hygiene.ruff_quality import (
            build_ruff_quality_report,
        )

        empty_root = workspace / "unavailable_project"
        empty_root.mkdir(parents=True, exist_ok=True)
        missing_command = workspace / "missing_ruff_executable"
        report = build_ruff_quality_report(
            empty_root,
            ruff_argv_prefix=(str(missing_command),),
        )
    finally:
        if sys.path and sys.path[0] == str(project_root):
            sys.path.pop(0)
    codes = {item["code"] for item in report.to_dict()["findings"]}
    _assert("RUFF_QUALITY_BLOCKED" in codes, "RUFF_UNAVAILABLE_NOT_BLOCKED")
    print("RUFF_QUALITY_UNAVAILABLE_FAILS_CLOSED: PASS")


def _validate_runtime_ruff(project_root: Path) -> None:
    """Require a real read-only Ruff project scan for local freeze validation."""
    sys.path.insert(0, str(project_root))
    try:
        from kanda_reasoner_app.source_hygiene.ruff_quality import (
            build_ruff_quality_report,
        )

        report = build_ruff_quality_report(
            project_root,
            timeout_seconds=300.0,
        )
    finally:
        if sys.path and sys.path[0] == str(project_root):
            sys.path.pop(0)

    data = report.to_dict()
    codes = {item["code"] for item in data["findings"]}
    blockers = {
        "RUFF_QUALITY_BLOCKED",
        "RUFF_LINT_EXECUTION_FAILED",
        "RUFF_FORMAT_EXECUTION_FAILED",
        "RUFF_FORMAT_CHECK_BLOCKED",
    }
    active_blockers = sorted(codes.intersection(blockers))
    details = "; ".join(
        str(item.get("message") or "")
        for item in data["findings"]
        if item.get("code") in blockers
    )
    _assert(
        not active_blockers,
        "RUNTIME_RUFF_PROJECT_SCAN_BLOCKED:"
        + ",".join(active_blockers)
        + (":" + details if details else ""),
    )
    inputs = set(data.get("input_sources") or [])
    _assert(
        any(str(item).startswith("ruff_version:") for item in inputs),
        "RUNTIME_RUFF_VERSION_EVIDENCE_MISSING",
    )
    _assert(
        any(str(item).startswith("ruff_command_source:") for item in inputs),
        "RUNTIME_RUFF_COMMAND_EVIDENCE_MISSING",
    )
    _assert(
        "ruff_scope_policy:project_exclusion_policy" in inputs,
        "RUNTIME_RUFF_SCOPE_POLICY_EVIDENCE_MISSING",
    )
    print("RUNTIME_RUFF_AVAILABLE: PASS")
    print("RUNTIME_RUFF_READ_ONLY_PROJECT_SCAN: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--patch-zip", default="")
    parser.add_argument(
        "--require-runtime-ruff",
        action="store_true",
        help="Require a real read-only Ruff project scan for local validation.",
    )
    args = parser.parse_args()

    project_root = Path(args.project_root).expanduser().resolve()
    _assert(project_root.is_dir(), "PROJECT_ROOT_INVALID")
    transient_root = project_root.parent / (
        project_root.name + "_delete_after_daily_work"
    )
    workspace = transient_root / (FEATURE_ID + "_validator")
    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.mkdir(parents=True, exist_ok=True)
    try:
        _validate_source(project_root)
        _validate_catalog_and_cli(project_root)
        _validate_read_only_execution(project_root, workspace)
        _validate_unavailable(project_root, workspace)
        if args.require_runtime_ruff:
            _validate_runtime_ruff(project_root)
        if args.patch_zip:
            _validate_patch_zip(Path(args.patch_zip).expanduser().resolve())
        print("VALIDATION OK: " + FEATURE_ID)
        return 0
    finally:
        shutil.rmtree(workspace, ignore_errors=True)


if __name__ == "__main__":
    try:
        exit_status = main()
    except Exception as exc:
        print("VALIDATION FAILED: " + str(exc))
        exit_status = 1
    raise SystemExit(exit_status)
