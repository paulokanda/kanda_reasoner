# project-path: tools/validate_free_python_coding_ai_update5_forward_compatibility_v1r1.py
"""Validate the final cumulative validator forward-compatibility correction."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import py_compile
from typing import Any, Sequence

FEATURE_ID = (
    "free-python-coding-ai-final-readiness-forward-compatible-"
    "regression-correction-v1r1"
)

POWERSHELL_FILES = (
    "RUN_INSTALL.ps1",
    "INSTALL.ps1",
    "RUN_VALIDATE.ps1",
    "VALIDATE.ps1",
    "PREPARE_FREEZE.ps1",
    "NATIVE_PROCESS.ps1",
)

REQUIRED_PATH_TOKENS = (
    '$ToolsRoot = Join-Path $ProjectPath "tools"',
    '$Update1Validator = Join-Path $ToolsRoot "validate_free_python_coding_ai_update1_v1.py"',
    '$Update2Validator = Join-Path $ToolsRoot "validate_free_python_coding_ai_update2_v1.py"',
    '$Update3Validator = Join-Path $ToolsRoot "validate_free_python_coding_ai_update3_v1.py"',
    '$Update4Validator = Join-Path $ToolsRoot "validate_free_python_coding_ai_update4_v1.py"',
    '$Update5Validator = Join-Path $ToolsRoot "validate_free_python_coding_ai_update5_v1.py"',
    '$CorrectionValidator = Join-Path $ToolsRoot "validate_free_python_coding_ai_update5_forward_compatibility_v1r1.py"',
    '$ScriptsRoot = Join-Path $ProjectPath "scripts"',
    '$ZipValidator = Join-Path $ScriptsRoot "validate_patch_zip.py"',
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _require(condition: bool, marker: str) -> None:
    if not condition:
        raise AssertionError(marker)
    print(marker + ": PASS")


def _load_manifest(package_root: Path) -> dict[str, Any]:
    data = json.loads((package_root / "INSTALL_MANIFEST.json").read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError("INSTALL_MANIFEST.json root must be an object.")
    return data


def _validate_required_existing(tool_root: Path, package_root: Path) -> None:
    records = _load_manifest(package_root).get("required_existing_files")
    if not isinstance(records, list) or not records:
        raise RuntimeError("required_existing_files must be a non-empty list.")
    for item in records:
        relative = str(item.get("path") or "").replace("\\", "/")
        expected = str(item.get("sha256") or "").lower()
        target = (tool_root / relative).resolve()
        target.relative_to(tool_root)
        _require(target.is_file(), "REQUIRED UPDATE 5 SOURCE PRESENT: " + relative)
        _require(_sha256(target) == expected, "REQUIRED UPDATE 5 SOURCE HASH: " + relative)
    print("ORIGINAL UPDATE 5 SOURCE FINGERPRINT: PASS")


def _assignment_dict(path: Path, name: str) -> dict[str, str]:
    module = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in module.body:
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id == name
        ):
            value = ast.literal_eval(node.value)
            if not isinstance(value, dict):
                raise RuntimeError(name + " must be a dictionary.")
            return {str(k): str(v) for k, v in value.items()}
    raise RuntimeError(name + " was not found in " + str(path))


def _validate_validator_chain(tool_root: Path) -> None:
    paths = {
        "update2": tool_root / "tools/validate_free_python_coding_ai_update2_v1.py",
        "update3": tool_root / "tools/validate_free_python_coding_ai_update3_v1.py",
        "update4": tool_root / "tools/validate_free_python_coding_ai_update4_v1.py",
        "update5": tool_root / "tools/validate_free_python_coding_ai_update5_v1.py",
    }
    for key, path in paths.items():
        _require(path.is_file(), "CUMULATIVE VALIDATOR PRESENT " + key)
        source = path.read_text(encoding="utf-8")
        ast.parse(source, filename=str(path))
        py_compile.compile(str(path), doraise=True)
        _require(len(source.splitlines()) <= 500, "CUMULATIVE VALIDATOR SIZE <=500 " + key)

    update2_hashes = _assignment_dict(paths["update2"], "FROZEN_UPDATE1_HASHES")
    _require(
        "kanda_reasoner_app/reasoner_engine/config_external_ai_tab.py" not in update2_hashes,
        "UPDATE 2 STALE CONFIG HASH COUPLING REMOVED",
    )
    update2_source = paths["update2"].read_text(encoding="utf-8")
    for token in (
        "UPDATE 1 CONFIG EXTERNAL AI FORWARD COMPATIBILITY: PASS",
        "PRIOR-STAGE VALIDATOR FORWARD COMPATIBILITY: PASS",
    ):
        _require(token in update2_source, "UPDATE 2 FORWARD CAPABILITY " + token)

    predecessor_paths = {
        "update3": ("tools/validate_free_python_coding_ai_update2_v1.py",),
        "update4": (
            "tools/validate_free_python_coding_ai_update2_v1.py",
            "tools/validate_free_python_coding_ai_update3_v1.py",
        ),
        "update5": (
            "tools/validate_free_python_coding_ai_update2_v1.py",
            "tools/validate_free_python_coding_ai_update3_v1.py",
            "tools/validate_free_python_coding_ai_update4_v1.py",
        ),
    }
    for key, forbidden in predecessor_paths.items():
        hashes = _assignment_dict(paths[key], "FROZEN_HASHES")
        for relative in forbidden:
            _require(
                relative not in hashes,
                "CUMULATIVE VALIDATOR HASH COUPLING REMOVED " + key + " " + relative,
            )
    for key, token in (
        ("update3", "UPDATE 2 VALIDATOR FORWARD COMPATIBILITY: PASS"),
        ("update4", "UPDATES 2-3 VALIDATOR FORWARD COMPATIBILITY: PASS"),
        ("update5", "PRIOR-STAGE VALIDATORS FORWARD COMPATIBLE: PASS"),
    ):
        _require(token in paths[key].read_text(encoding="utf-8"), "VALIDATOR CAPABILITY TOKEN " + token)
    print("CUMULATIVE VALIDATOR CAPABILITY CHAIN: PASS")


def _invalid_control_offsets(raw: bytes) -> list[int]:
    return [
        index
        for index, value in enumerate(raw)
        if value < 32 and value not in {9, 10, 13}
    ]


def _validate_delivery_scripts(package_root: Path) -> None:
    for name in POWERSHELL_FILES:
        path = package_root / name
        _require(path.is_file(), "POWERSHELL SCRIPT PRESENT: " + name)
        _require(
            not _invalid_control_offsets(path.read_bytes()),
            "POWERSHELL CONTROL CHARACTERS ABSENT: " + name,
        )
    _require(
        bool(_invalid_control_offsets(b"bad" + bytes([11]) + b"path")),
        "POWERSHELL CONTROL CHARACTER FIXTURE REJECTED",
    )
    print("POWERSHELL_CONTROL_CHARACTERS_REJECTED: PASS")

    text = (package_root / "VALIDATE.ps1").read_text(encoding="utf-8")
    for token in REQUIRED_PATH_TOKENS:
        _require(token in text, "VALIDATOR PATH TOKEN " + token)
    lowered = text.casefold()
    _require("toolsvalidate_" not in lowered, "CONCATENATED TOOLSVALIDATE PATH ABSENT")
    _require('"tools\\validate_' not in lowered, "ESCAPE-SENSITIVE TOOLS PATH ABSENT")
    _require('"scripts\\validate_' not in lowered, "ESCAPE-SENSITIVE SCRIPTS PATH ABSENT")
    _require("\\x0b" not in repr((package_root / "VALIDATE.ps1").read_bytes()), "VERTICAL TAB BYTE ABSENT")
    print("VALIDATOR_PATH_COMPONENT_JOIN_CONTRACT: PASS")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool-root", required=True)
    parser.add_argument("--package-root", required=True)
    args = parser.parse_args(argv)
    tool_root = Path(args.tool_root).expanduser().resolve()
    package_root = Path(args.package_root).expanduser().resolve()
    try:
        _require(tool_root.is_dir(), "VALIDATOR TOOL ROOT IMPORT PATH")
        _require(package_root.is_dir(), "VALIDATOR PACKAGE ROOT")
        _validate_required_existing(tool_root, package_root)
        _validate_validator_chain(tool_root)
        _validate_delivery_scripts(package_root)
        py_compile.compile(str(Path(__file__)), doraise=True)
        _require(True, "CORRECTION VALIDATOR PYTHON COMPILE")
    except Exception as exc:
        print("VALIDATION ERROR: " + exc.__class__.__name__ + ": " + str(exc))
        return 1
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
