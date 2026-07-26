# project-path: tools/validate_unsafe_path_platform_warning_correction_v1.py
"""Validate the unsafe path and platform warning correction patch."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import ModuleType
from zipfile import ZipFile

FEATURE_ID = "unsafe-path-platform-warning-correction-v1"
TARGET_FILES = (
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "workbench_behavior_gui_bridge.py",
    "kanda_reasoner_app/source_hygiene/ruff_correction_storage.py",
    "tools/validate_advanced_quality_review_ruff_format_comparison_v5b.py",
    "tools/validate_engineering_safety_ruff_correction_workflow_v3a.py",
    "tools/validate_unsafe_path_platform_warning_correction_v1.py",
)
BUNDLE_MANIFEST = (
    "workbench/_bundle_temp/"
    "BUNDLE_MANIFEST_unsafe_path_platform_warning_correction_v1.txt"
)
ROOT_MEMBERS = (
    "FREEZE.ps1",
    "INSTALL.ps1",
    "KANDA_FREEZE_HINT.json",
    "PACKAGE_MANIFEST.json",
    "VALIDATE.ps1",
    BUNDLE_MANIFEST,
)


def main() -> int:
    """Run all focused and architecture-level validation gates."""
    args = _parse_args()
    root = Path(args.project_root).expanduser().resolve(strict=True)
    patch_zip = Path(args.patch_zip).expanduser().resolve(strict=True)
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    _validate_zip_contract(root, patch_zip)
    print("ZIP CONTRACT: PASS")
    _validate_python_sources(root)
    print("PYTHON_COMPILE: PASS")
    print("MODULE_SIZE_LAW_BELOW_500: PASS")
    print("ASCII_SOURCE_ONLY: PASS")
    _validate_source_contracts(root)
    print("EXPLICIT_TEXT_ENCODING: PASS")
    _validate_binary_hash_behavior(root)
    print("BINARY_HASH_STREAMING: PASS")
    _validate_architecture_scan(root)
    print("TARGET_UNSAFE_PATH_PLATFORM_WARNINGS: 0")
    print("ARCHITECTURE_ERROR_COUNT: 0")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--patch-zip", required=True)
    return parser.parse_args()


def _validate_zip_contract(root: Path, patch_zip: Path) -> None:
    if not patch_zip.is_file():
        raise AssertionError("Patch ZIP missing: " + str(patch_zip))

    with ZipFile(patch_zip) as archive:
        members = tuple(
            sorted(
                item.filename.rstrip("/")
                for item in archive.infolist()
                if not item.is_dir()
            )
        )
        expected = tuple(
            sorted(
                (*ROOT_MEMBERS, *("payload/" + item for item in TARGET_FILES))
            )
        )
        _assert(members == expected, "PATCH_MEMBER_SCOPE_INVALID")

        manifest = json.loads(archive.read("PACKAGE_MANIFEST.json"))
        hint = json.loads(archive.read("KANDA_FREEZE_HINT.json"))
        _assert(manifest.get("feature_id") == FEATURE_ID, "MANIFEST_FEATURE_ID")
        _assert(hint.get("feature_id") == FEATURE_ID, "HINT_FEATURE_ID")
        _assert(
            set(hint.get("protected_paths") or ()) == set(TARGET_FILES),
            "HINT_PROTECTED_PATHS",
        )
        _assert(
            hint.get("freeze_readiness") == "validation_pending",
            "HINT_READINESS_MUST_START_PENDING",
        )
        _assert(
            hint.get("requires_user_validation") is True,
            "HINT_LOCAL_VALIDATION_REQUIRED",
        )

        records = manifest.get("files") or []
        _assert(len(records) == len(TARGET_FILES), "MANIFEST_FILE_COUNT")
        by_path = {
            str(record.get("relative_path")): record
            for record in records
            if isinstance(record, dict)
        }
        _assert(set(by_path) == set(TARGET_FILES), "MANIFEST_FILE_SCOPE")

        for relative in TARGET_FILES:
            payload_name = "payload/" + relative
            payload = archive.read(payload_name)
            payload_hash = hashlib.sha256(payload).hexdigest()
            record = by_path[relative]
            _assert(record.get("sha256") == payload_hash, "PAYLOAD_HASH:" + relative)
            installed_hash = _sha256(root / relative)
            _assert(installed_hash == payload_hash, "INSTALLED_HASH:" + relative)

        bundle_text = archive.read(BUNDLE_MANIFEST).decode("utf-8")
        _assert(FEATURE_ID in bundle_text, "BUNDLE_MANIFEST_FEATURE_ID")
        for relative in TARGET_FILES:
            _assert(relative in bundle_text, "BUNDLE_MANIFEST_PATH:" + relative)


def _validate_python_sources(root: Path) -> None:
    for relative in TARGET_FILES:
        path = root / relative
        _assert(path.is_file(), "SOURCE_MISSING:" + relative)
        text = path.read_text(encoding="utf-8", errors="strict")
        _assert(not any(ord(char) > 127 for char in text), "NON_ASCII:" + relative)
        compile(text, relative, "exec")
        line_count = len(text.splitlines())
        _assert(0 < line_count < 500, "MODULE_SIZE:" + relative)


def _validate_source_contracts(root: Path) -> None:
    bridge = _read(root, TARGET_FILES[0])
    _assert("Legacy Compatibility - Optional Behavior Validation" in bridge, "ASCII_LABEL")
    _assert("\u2014" not in bridge, "EM_DASH_REMAINS")

    storage = _read(root, TARGET_FILES[1])
    _assert("import io" in storage, "BINARY_IO_IMPORT")
    _assert('io.FileIO(path, mode="rb")' in storage, "BINARY_FILEIO_CONTRACT")
    _assert('Path(path).open("rb")' not in storage, "BINARY_OPEN_FALSE_POSITIVE")

    for relative in TARGET_FILES[:-1]:
        tree = ast.parse(_read(root, relative), filename=relative)
        missing = _missing_text_encodings(tree)
        _assert(not missing, "TEXT_ENCODING_MISSING:" + relative + ":" + ",".join(missing))


def _missing_text_encodings(tree: ast.AST) -> list[str]:
    findings: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        call_name = _call_name(node.func)
        lower_name = call_name.lower()
        is_text_method = lower_name.endswith(".read_text") or lower_name.endswith(
            ".write_text"
        )
        is_open = lower_name == "open" or lower_name.endswith(".open")
        if not is_text_method and not is_open:
            continue
        if is_open and _call_uses_binary_mode(node):
            continue
        if any(keyword.arg == "encoding" for keyword in node.keywords):
            continue
        findings.append(str(getattr(node, "lineno", "?")) + ":" + call_name)
    return findings


def _call_name(node: ast.AST) -> str:
    parts: list[str] = []
    current: ast.AST | None = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        parts.append(current.id)
    return ".".join(reversed(parts))


def _call_uses_binary_mode(node: ast.Call) -> bool:
    mode: str | None = None
    if len(node.args) >= 2:
        value = node.args[1]
        if isinstance(value, ast.Constant) and isinstance(value.value, str):
            mode = value.value
    for keyword in node.keywords:
        if keyword.arg == "mode":
            value = keyword.value
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                mode = value.value
    return bool(mode and "b" in mode)


def _validate_binary_hash_behavior(root: Path) -> None:
    module = _load_module(root / TARGET_FILES[1])
    payload = bytes(range(256)) * 8193
    expected = hashlib.sha256(payload).hexdigest()
    with tempfile.TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / "payload.bin"
        path.write_bytes(payload)
        observed = module.sha256_file(path)
    _assert(observed == expected, "SHA256_FILE_BEHAVIOR")


def _load_module(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("_warning_fix_storage", path)
    _assert(spec is not None and spec.loader is not None, "MODULE_SPEC")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _validate_architecture_scan(root: Path) -> None:
    command = (
        sys.executable,
        str(root / "kanda_reasoner_app/manage_architecture/manage_architecture.py"),
        "--root",
        str(root),
        "--validate",
    )
    result = subprocess.run(
        command,
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    output = result.stdout + result.stderr
    _assert(result.returncode == 0, "ARCHITECTURE_VALIDATION_FAILED:\n" + output[-4000:])
    _assert("Errors: 0" in output, "ARCHITECTURE_ERRORS_REMAIN")
    for relative in TARGET_FILES[:-1]:
        relevant_lines = [
            line
            for line in output.splitlines()
            if "UNSAFE_PATH_PLATFORM_ASSUMPTION" in line and relative in line
        ]
        _assert(not relevant_lines, "TARGET_WARNING_REMAINS:" + relative)


def _read(root: Path, relative: str) -> str:
    return (root / relative).read_text(encoding="utf-8", errors="strict")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


if __name__ == "__main__":
    raise SystemExit(main())
