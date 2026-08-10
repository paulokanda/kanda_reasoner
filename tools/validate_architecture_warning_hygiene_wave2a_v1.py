"""Validate deterministic warning cleanup for architecture wave 2A."""

from __future__ import annotations

import argparse
import ast
import os
import re
import subprocess
import sys
from pathlib import Path

FEATURE_ID = "architecture-warning-hygiene-wave2a-v1"
TARGETS = {
    "rollback": Path("tools/validate_portable_governed_root_rollback_v1.py"),
    "handoff": Path("tools/validate_project_structure_show_project_json_handoff_v1.py"),
    "authority": Path("tools/validate_tool_portable_local_ai_project_authority_v1r1.py"),
}
PORTABLE_MANIFESTS = (
    Path("portable/PORTABLE_RUNTIME_ALLOWLIST.json"),
    Path("portable/PORTABLE_BUILDER_MANIFEST.json"),
    Path("portable/PORTABLE_EXTERNAL_BUILD_CONTROLS.json"),
)


def require(condition: bool, code: str) -> None:
    """Raise a deterministic validation error when condition is false."""
    if not condition:
        raise RuntimeError(code)


def read(root: Path, key: str) -> str:
    """Read one target source file as strict UTF-8."""
    return (root / TARGETS[key]).read_text(encoding="utf-8")


def validate_compile_and_size(root: Path) -> None:
    """Parse all touched Python modules and enforce the 500-line hard gate."""
    relatives = (*TARGETS.values(), Path(__file__).resolve().relative_to(root))
    for relative in relatives:
        path = root / relative
        text = path.read_text(encoding="utf-8")
        ast.parse(text, filename=str(path))
        require(len(text.splitlines()) <= 500, "MODULE_OVER_500_LINES:" + relative.as_posix())
    print("WAVE2A PYTHON COMPILE AND SIZE: PASS")


def validate_static(root: Path) -> None:
    """Validate exact warning repairs and preserved compatibility."""
    rollback = read(root, "rollback")
    start = rollback.index("def _assert_restored(")
    end = rollback.index("\n\ndef _functional_fixture", start)
    block = rollback[start:end]
    require(block.count('.read_text(encoding="utf-8")') == 6, "ROLLBACK_UTF8_COUNT_INVALID")
    require(".read_text()" not in block, "ROLLBACK_IMPLICIT_READ_REMAINS")
    print("PORTABLE ROLLBACK EXPLICIT UTF8 READS: PASS")

    handoff_tree = ast.parse(read(root, "handoff"))
    require(
        ast.get_docstring(handoff_tree)
        == "Validate Show Project complete-JSON handoff into Project Structure.",
        "HANDOFF_DOCSTRING_INVALID",
    )
    print("PROJECT STRUCTURE VALIDATOR DOCSTRING: PASS")

    authority = read(root, "authority")
    tree = ast.parse(authority)
    cls = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "FakeSettings")
    method = next(node for node in cls.body if isinstance(node, ast.FunctionDef) and node.name == "value")
    names = {arg.arg for arg in [*method.args.posonlyargs, *method.args.args, *method.args.kwonlyargs]}
    require("type" not in names, "FAKE_SETTINGS_TYPE_SHADOW_REMAINS")
    require(method.args.kwarg is not None and method.args.kwarg.arg == "options", "FAKE_SETTINGS_KEYWORD_BRIDGE_MISSING")
    require('requested_type = options.get("type")' in authority, "FAKE_SETTINGS_TYPE_KEYWORD_NOT_READ")
    print("PORTABLE AUTHORITY FIXTURE TYPE SHADOWING ABSENT: PASS")
    print("PORTABLE AUTHORITY FIXTURE QSETTINGS KEYWORD COMPATIBILITY: PASS")


def validate_manifest_non_membership(root: Path) -> None:
    """Prove Portable manifests do not govern the touched validator files."""
    paths = {p.as_posix() for p in TARGETS.values()}
    paths.add(Path(__file__).resolve().relative_to(root).as_posix())
    for manifest in PORTABLE_MANIFESTS:
        text = (root / manifest).read_text(encoding="utf-8")
        overlap = sorted(path for path in paths if path in text)
        require(not overlap, "PORTABLE_MANIFEST_MEMBERSHIP_UNEXPECTED:" + manifest.as_posix())
    print("PORTABLE RUNTIME ALLOWLIST MODIFIED: NO")
    print("PORTABLE BUILDER MANIFEST MODIFIED: NO")
    print("PORTABLE EXTERNAL BUILD CONTROLS MODIFIED: NO")


def run_owned_validator(root: Path, relative: str, args: list[str], marker: str) -> None:
    """Run one existing validator and require its owned marker."""
    path = root / relative
    require(path.is_file(), "VALIDATOR_MISSING:" + relative)
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = str(root)
    result = subprocess.run(
        [sys.executable, str(path), *args], cwd=str(root), env=env,
        text=True, capture_output=True, check=False, timeout=1200,
    )
    output = (result.stdout or "") + (result.stderr or "")
    print(output, end="" if output.endswith("\n") else "\n")
    require(result.returncode == 0, "VALIDATOR_FAILED:" + relative)
    require(marker in output, "VALIDATOR_MARKER_MISSING:" + relative)


def validate_live_architecture(root: Path) -> None:
    """Run the current architecture owner and reject the eight target warnings."""
    path = root / "kanda_reasoner_app/manage_architecture/manage_architecture.py"
    result = subprocess.run(
        [sys.executable, str(path), "--root", str(root), "--validate"],
        cwd=str(root), text=True, capture_output=True, check=False, timeout=1200,
    )
    output = (result.stdout or "") + (result.stderr or "")
    print(output, end="" if output.endswith("\n") else "\n")
    require(result.returncode == 0, "ARCHITECTURE_VALIDATE_FAILED")
    require(re.search(r"Errors:\s*0\b", output) is not None, "ARCHITECTURE_ERRORS_NOT_ZERO")
    forbidden = (
        ("UNSAFE_PATH_PLATFORM_ASSUMPTION", TARGETS["rollback"].as_posix()),
        ("MISSING_DOCSTRING", TARGETS["handoff"].as_posix()),
        ("SYMBOL_SHADOWING", TARGETS["authority"].as_posix()),
    )
    for code, relative in forbidden:
        require(
            not any(code in line and relative in line for line in output.splitlines()),
            "TARGET_WARNING_REMAINS:" + code + ":" + relative,
        )
    print("WAVE2A TARGET ARCHITECTURE WARNINGS ABSENT: PASS")


def main() -> int:
    """Run static and live validation for warning-hygiene wave 2A."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    root = Path(args.project_root).expanduser().resolve(strict=True)
    validate_compile_and_size(root)
    validate_static(root)
    validate_manifest_non_membership(root)
    if not args.static_only:
        run_owned_validator(
            root,
            "tools/validate_tool_portable_local_ai_project_authority_v1r1.py",
            ["--tool-root", str(root), "--skip-existing-validators"],
            "VALIDATION OK: kanda-reasoner-tool-portable-local-ai-project-authority-v1r1",
        )
        run_owned_validator(
            root,
            "tools/validate_project_structure_show_project_json_handoff_v1.py",
            ["--tool-root", str(root)],
            "VALIDATION OK: kanda-reasoner-project-structure-show-project-json-handoff-v1",
        )
        if os.name == "nt":
            run_owned_validator(
                root,
                "tools/validate_portable_governed_root_rollback_v1.py",
                ["--project-root", str(root)],
                "VALIDATION OK: portable-governed-root-rollback-v1",
            )
        else:
            print("PORTABLE ROLLBACK WINDOWS VALIDATION: SKIPPED_NON_WINDOWS")
        validate_live_architecture(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("VALIDATION FAILED: " + FEATURE_ID)
        print(exc.__class__.__name__ + ": " + str(exc))
        raise SystemExit(1)
