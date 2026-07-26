# project-path: tools/validate_engineering_safety_ruff_policy_identity_v2.py
"""Validate canonical Ruff policy identity without changing frozen Phase 1."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

__all__ = [
    "main",
]

FEATURE_ID = "engineering-safety-ruff-policy-identity-v2"
EXPECTED_RUFF_VERSION = "ruff 0.15.21"
EXPECTED_REQUIRED_VERSION = "==0.15.21"
EXPECTED_TARGET_VERSION = "py310"
EXPECTED_LINE_LENGTH = 88
EXPECTED_POLICY_TEXT = """required-version = \"==0.15.21\"
target-version = \"py310\"
line-length = 88
indent-width = 4
force-exclude = true
respect-gitignore = true
preview = false
fix = false
unsafe-fixes = false
show-fixes = true
src = [\".\"]

[lint]
extend-select = [\"E501\"]
preview = false

[format]
quote-style = \"double\"
indent-style = \"space\"
skip-magic-trailing-comma = false
line-ending = \"auto\"
docstring-code-format = false
preview = false
"""
FROZEN_V1R2_HASHES = {
    "_reasoner_tools_gui_engineering_safety_panel_commands.py": (
        "d80ea8ffd9f8c78d1c42e1ef30772afe7ca5cfaeda051a3aef0d61c045698b92"
    ),
    "reasoner_tools_gui_engineering_safety_panel.py": (
        "4e692e40532c553b577786ec88fd244f19a3bb48f4137649299d60f094fde803"
    ),
    "kanda_reasoner_app/safety_suite_cli/commands.py": (
        "4ad824f42a148f9bf14651e521d848882c606746bde856df4cafbd186a5cf4d4"
    ),
    "kanda_reasoner_app/safety_suite_cli/commands_actions_private.py": (
        "30124df6e7c139ff6ec7865490771c44916ada58f2cc3379dbc01a03469e2d5c"
    ),
    "kanda_reasoner_app/safety_suite_cli/commands_catalog_private.py": (
        "e8317c0f94cf0d48c8656011f719b1841b7ae88a07f72a1df6a9326a6f5244f4"
    ),
    "kanda_reasoner_app/safety_suite_cli/commands_parsers_private.py": (
        "e13c0fa9071f6a84835c34065e937a8897ead75ec94f2f05ec7b32c5a169d29e"
    ),
    "kanda_reasoner_app/source_hygiene/__init__.py": (
        "3289158296bb108d117d5013362306fa6d8c615e1579d34b5236630a2ffa4b28"
    ),
    "kanda_reasoner_app/source_hygiene/ruff_quality.py": (
        "7a2318f5f2f44508695a2f7d9ce602670af64f5360147a6c850aa4bdce5ceca7"
    ),
    "kanda_reasoner_app/source_hygiene/ruff_quality_runtime.py": (
        "2f7ac19a402c2094467d89b0bdd012146ec332c41a87a1b79bfa3b170c4d612a"
    ),
    "kanda_reasoner_app/source_hygiene/ruff_quality_scope.py": (
        "aac05f694bd7f65397ee8d53d2d3883aace37005058d1b2e16d8d3b30b490b3a"
    ),
    "kanda_reasoner_app/source_hygiene/schemas.py": (
        "31bfc47a146eac742f08d831ea4ef9490c66742fa769f0592a4154fce4a4097d"
    ),
    "tools/validate_engineering_safety_source_hygiene_ruff_quality_v1.py": (
        "b782d29787be0d959a8a446bf73797bc3297e139950c8ed4d684c1f8e5bd1661"
    ),
}
NEW_SOURCE_PATHS = (
    "kanda_reasoner_app/source_hygiene/ruff_policy_identity.py",
    "tools/validate_engineering_safety_ruff_policy_identity_v2.py",
)
FORBIDDEN_MUTATION_ARGUMENTS = (
    "--fix",
    "--fix-only",
    "--unsafe-fixes",
)


def main() -> int:
    """Run all focused Phase 2 policy validation gates."""
    args = _parse_args()
    project_root = Path(args.project_root).expanduser().resolve()
    patch_zip = Path(args.patch_zip).expanduser().resolve()
    _require_directory(project_root, "PROJECT_ROOT")
    _require_file(patch_zip, "PATCH_ZIP")

    sys.path.insert(0, str(project_root))
    from kanda_reasoner_app.source_hygiene.ruff_policy_identity import (
        resolve_ruff_policy_identity,
    )

    _validate_policy_bytes(project_root)
    print("RUFF_POLICY_CANONICAL_FILE: PASS")

    identity = resolve_ruff_policy_identity(project_root)
    _assert(identity.config_relative_path == "ruff.toml", "CONFIG_PATH")
    _assert(identity.required_version == EXPECTED_REQUIRED_VERSION, "REQUIRED_VERSION")
    _assert(identity.target_version == EXPECTED_TARGET_VERSION, "TARGET_VERSION")
    _assert(identity.line_length == EXPECTED_LINE_LENGTH, "LINE_LENGTH")
    _assert(not identity.competing_config_paths, "CONFIG_AUTHORITY")
    print("RUFF_POLICY_CONFIG_IDENTITY: PASS")
    print("RUFF_POLICY_CONFIG_SHA256: " + identity.config_sha256)

    _validate_frozen_phase1(project_root)
    print("FROZEN_PHASE1_V1R2_BYTE_IDENTITY: PASS")

    _validate_python_sources(project_root)
    print("PYTHON_COMPILE: PASS")
    print("MODULE_SIZE_LAW_BELOW_500: PASS")

    _validate_no_mutation_defaults(project_root)
    print("RUFF_POLICY_READ_ONLY_DEFAULTS: PASS")

    ruff_prefix = _resolve_ruff_prefix(args.ruff_executable)
    version = _run(
        (*ruff_prefix, "--version"),
        cwd=project_root,
        accepted_returncodes=(0,),
    ).strip()
    _assert(version.splitlines()[0].strip() == EXPECTED_RUFF_VERSION, "RUFF_VERSION")
    print("RUNTIME_RUFF_REQUIRED_VERSION: PASS")

    _validate_frozen_phase1_runtime(project_root, ruff_prefix)
    print("FROZEN_PHASE1_RUNTIME_POLICY_COMPATIBILITY: PASS")

    _validate_real_ruff(project_root, ruff_prefix)
    print("RUNTIME_RUFF_POLICY_DISCOVERY: PASS")
    print("RUNTIME_RUFF_READ_ONLY_POLICY_SCAN: PASS")

    _validate_patch_zip(patch_zip)
    print("PATCH_ZIP_CONTRACT: PASS")
    print("ZIP CONTRACT: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--patch-zip", required=True)
    parser.add_argument("--ruff-executable", default="")
    return parser.parse_args()


def _validate_policy_bytes(project_root: Path) -> None:
    path = project_root / "ruff.toml"
    _require_file(path, "RUFF_POLICY")
    text = path.read_text(encoding="utf-8", errors="strict")
    _assert(text == EXPECTED_POLICY_TEXT, "RUFF_POLICY_BYTES")
    _assert(not text.startswith("\ufeff"), "RUFF_POLICY_BOM")


def _validate_frozen_phase1(project_root: Path) -> None:
    for relative, expected_hash in FROZEN_V1R2_HASHES.items():
        path = project_root / relative
        _require_file(path, "FROZEN_PHASE1_FILE")
        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        _assert(actual_hash == expected_hash, "FROZEN_PHASE1_HASH:" + relative)


def _validate_python_sources(project_root: Path) -> None:
    for relative in NEW_SOURCE_PATHS:
        path = project_root / relative
        _require_file(path, "NEW_SOURCE")
        text = path.read_text(encoding="utf-8", errors="strict")
        _assert(not text.startswith("\ufeff"), "SOURCE_BOM:" + relative)
        ast.parse(text, filename=str(path))
        line_count = len(text.splitlines())
        _assert(line_count < 500, "MODULE_SIZE:" + relative)
        _assert(text.isascii(), "SOURCE_ASCII:" + relative)


def _validate_no_mutation_defaults(project_root: Path) -> None:
    text = (project_root / "ruff.toml").read_text(encoding="utf-8")
    _assert("fix = false" in text, "FIX_FALSE")
    _assert("unsafe-fixes = false" in text, "UNSAFE_FIXES_FALSE")
    source = (
        project_root / "kanda_reasoner_app/source_hygiene/ruff_policy_identity.py"
    ).read_text(encoding="utf-8")
    for argument in FORBIDDEN_MUTATION_ARGUMENTS:
        _assert(argument not in source, "FORBIDDEN_ARGUMENT:" + argument)


def _resolve_ruff_prefix(explicit: str) -> tuple[str, ...]:
    if explicit.strip():
        return (explicit.strip(),)
    return (sys.executable, "-m", "ruff")


def _validate_frozen_phase1_runtime(
    project_root: Path,
    ruff_prefix: tuple[str, ...],
) -> None:
    """Prove the frozen Phase 1 scanner consumes the new policy read-only."""
    from kanda_reasoner_app.source_hygiene.ruff_quality import (
        build_ruff_quality_report,
    )

    before = _python_hashes(project_root)
    report = build_ruff_quality_report(
        project_root,
        ruff_argv_prefix=ruff_prefix,
    )
    after = _python_hashes(project_root)
    _assert(before == after, "FROZEN_PHASE1_SOURCE_MUTATION")
    blocker_codes = {
        "RUFF_QUALITY_BLOCKED",
        "RUFF_LINT_EXECUTION_FAILED",
        "RUFF_FORMAT_EXECUTION_FAILED",
    }
    actual_codes = {finding.code for finding in report.findings}
    _assert(not blocker_codes.intersection(actual_codes), "FROZEN_PHASE1_BLOCKER")
    _assert(
        "ruff_version:" + EXPECTED_RUFF_VERSION in report.input_sources,
        "FROZEN_PHASE1_VERSION_EVIDENCE",
    )
    _assert(
        "ruff_scope_policy:project_exclusion_policy" in report.input_sources,
        "FROZEN_PHASE1_SCOPE_EVIDENCE",
    )
    _assert(not (project_root / ".ruff_cache").exists(), "PROJECT_RUFF_CACHE_LEAK")


def _python_hashes(project_root: Path) -> dict[str, str]:
    """Return hashes for all Python files, including excluded reference files."""
    output: dict[str, str] = {}
    for path in sorted(project_root.rglob("*.py")):
        if not path.is_file():
            continue
        relative = path.relative_to(project_root).as_posix()
        output[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return output


def _validate_real_ruff(
    project_root: Path,
    ruff_prefix: tuple[str, ...],
) -> None:
    policy = project_root / "ruff.toml"
    with tempfile.TemporaryDirectory(prefix="kanda_ruff_policy_v2_") as temp_dir:
        root = Path(temp_dir)
        good = root / "good.py"
        long_line = root / "long_line.py"
        good.write_text("value = 1\n", encoding="utf-8")
        long_line.write_text(
            'message = "' + ("x" * 100) + '"\n',
            encoding="utf-8",
        )
        before = {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in (good, long_line)
        }
        check_output = _run(
            (
                *ruff_prefix,
                "check",
                "--config",
                str(policy),
                "--no-cache",
                "--output-format",
                "json",
                str(root),
            ),
            cwd=project_root,
            accepted_returncodes=(1,),
        )
        payload = json.loads(check_output)
        _assert(isinstance(payload, list), "RUFF_JSON_PAYLOAD")
        _assert(any(item.get("code") == "E501" for item in payload), "E501_POLICY")

        format_output = _run(
            (
                *ruff_prefix,
                "format",
                "--config",
                str(policy),
                "--check",
                "--no-cache",
                str(root),
            ),
            cwd=project_root,
            accepted_returncodes=(0, 1),
        )
        _assert("error:" not in format_output.casefold(), "FORMAT_CONFIG_PARSE")

        after = {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in (good, long_line)
        }
        _assert(before == after, "RUFF_RUNTIME_MUTATION")
        _assert(not (root / ".ruff_cache").exists(), "RUFF_CACHE_LEAK")


def _validate_patch_zip(patch_zip: Path) -> None:
    expected = {
        "KANDA_FREEZE_HINT.json",
        "ruff.toml",
        "kanda_reasoner_app/source_hygiene/ruff_policy_identity.py",
        "tools/validate_engineering_safety_ruff_policy_identity_v2.py",
    }
    with zipfile.ZipFile(patch_zip, "r") as archive:
        names = set(archive.namelist())
        _assert(names == expected, "PATCH_ZIP_CONTENTS")
        hint = json.loads(archive.read("KANDA_FREEZE_HINT.json"))
    _assert(hint.get("feature_id") == FEATURE_ID, "FREEZE_HINT_FEATURE_ID")
    _assert(hint.get("root_freeze_hint", True), "FREEZE_HINT_ROOT")


def _run(
    argv: tuple[str, ...],
    *,
    cwd: Path,
    accepted_returncodes: tuple[int, ...],
) -> str:
    completed = subprocess.run(
        argv,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    output = (completed.stdout or "") + (completed.stderr or "")
    if completed.returncode not in accepted_returncodes:
        raise AssertionError(
            "COMMAND_FAILED:"
            + str(completed.returncode)
            + ":"
            + " ".join(argv)
            + ":"
            + " ".join(output.split())[:1200]
        )
    return output


def _require_directory(path: Path, label: str) -> None:
    _assert(path.exists() and path.is_dir(), label + "_NOT_DIRECTORY")


def _require_file(path: Path, label: str) -> None:
    _assert(path.exists() and path.is_file(), label + "_NOT_FILE:" + str(path))


def _assert(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print("VALIDATION FAILED: " + str(error))
        raise SystemExit(1)
