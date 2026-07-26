# project-path: tools/validate_engineering_safety_ruff_correction_gui_v3b.py
"""Focused validation for the Phase 3B Ruff correction GUI adapter."""

from __future__ import annotations

import argparse
import ast
from dataclasses import fields
import hashlib
import json
import os
from pathlib import Path, PureWindowsPath
import subprocess
import sys
import tempfile
from types import SimpleNamespace
from typing import Any, Sequence
from zipfile import ZipFile

__all__ = [
    "main",
]

FEATURE_ID = "engineering-safety-ruff-correction-gui-v3b"
EXPECTED_PATCH_FILES = {
    "KANDA_FREEZE_HINT.json",
    "KANDA_ERROR_LESSON_JSON_phase3b_validator_windows_path_separator_v1.txt",
    "tools/validate_engineering_safety_ruff_correction_gui_v3b.py",
}
TOUCHED_PYTHON_FILES = tuple(
    sorted(path for path in EXPECTED_PATCH_FILES if path.endswith(".py"))
)
PHASE3B_PRODUCT_HASHES = {
    "_reasoner_tools_gui_engineering_safety_panel_catalog.py": (
        "5015f39815b3800673d75ea45a76ed33e444ddfb8b8b0565b2ba246fa06ca22a"
    ),
    "_reasoner_tools_gui_ruff_correction_dialog.py": (
        "1dd0040c7b5904415a3347521359a9ffbbeeecc48f0df70cc8a1f34f68168f86"
    ),
    "reasoner_tools_gui_engineering_safety_panel.py": (
        "ef2f896a8e94d24a28e8dfac61af48b5541e54815a787420969211e59776cf09"
    ),
}
EXPECTED_PUBLIC_EXPORTS = [
    "ENGINEERING_SAFETY_PANEL_CATALOG",
    "EngineeringSafetyPanelTool",
    "build_engineering_safety_panel_cli_args",
    "build_engineering_safety_panel_command",
    "create_engineering_safety_panel",
    "get_engineering_safety_panel_catalog",
    "run_engineering_safety_panel_cli_command",
]
BASELINE_CATALOG = (
    ("Source Hygiene", "Scan BOM", "bom-scan"),
    ("Source Hygiene", "Ruff Quality", "ruff-quality"),
    ("Source Hygiene", "Shadow Audit", "shadow-audit"),
    ("Source Hygiene", "Plan Shadow Fix", "shadow-plan"),
    ("Source Hygiene", "Facade Fix Plan", "facade-fix-plan"),
    ("Engineering Safety", "Risk Change Radar", "risk-radar"),
    ("Engineering Safety", "Crash Triage", "crash-triage"),
    ("Engineering Safety", "Refactor Playbook", "refactor-playbook"),
    ("Governance Automation", "Release Notes", "release-notes"),
    ("Governance Automation", "Push Plan", "push-plan"),
    ("Stack Compatibility", "Stack Brief", "stack-brief"),
    ("Draft Reliability", "API Contract", "api-contract"),
    ("Draft Reliability", "Property Test", "property-test"),
    ("Project Symbol Atlas", "Atlas Report", "atlas-report"),
    ("Project Symbol Atlas", "Evidence Freshness", "evidence-freshness"),
    ("Project Symbol Atlas", "Find Symbol", "find-symbol"),
    ("Project Symbol Atlas", "Find Owner", "find-owner"),
    ("Project Symbol Atlas", "Facade Owner", "facade-owner"),
    ("Project Symbol Atlas", "Main and Helpers", "main-helpers"),
    ("Project Symbol Atlas", "Related Files", "related-files"),
    ("Project Symbol Atlas", "Pre-Patch Gate", "pre-patch-gate"),
    ("Utilities", "List Tools", "list-tools"),
)
NEW_CATALOG_ENTRY = (
    "Source Hygiene",
    "Ruff Corrections",
    "ruff-correction-dialog",
)
FROZEN_UNTOUCHED_HASHES = {
    "_reasoner_tools_gui_engineering_safety_panel_commands.py": (
        "d80ea8ffd9f8c78d1c42e1ef30772afe7ca5cfaeda051a3aef0d61c045698b92"
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
    "ruff.toml": ("52172a11111cedc04a0942130358ecb65ffa34ee98be833ef6c50cbc01bc0746"),
    "kanda_reasoner_app/source_hygiene/ruff_policy_identity.py": (
        "6ecde4874c74888fd19314cf12eeda9556469db97ba0fc1ae818323e15533fcf"
    ),
    "kanda_reasoner_app/source_hygiene/ruff_correction_apply.py": (
        "8c5555a39d7ebce82d5a2871d13c3a5c14b6b75e6fd04996f381b57728102d79"
    ),
    "kanda_reasoner_app/source_hygiene/ruff_correction_cli.py": (
        "525240b49730ee862b57be85e2b1649b14c40f92a14b918991a8215b57d4803c"
    ),
    "kanda_reasoner_app/source_hygiene/ruff_correction_discovery.py": (
        "f2e3bdaaa2aa419554b03347f95b3b1e217032f61efd934ae40e175e161831f4"
    ),
    "kanda_reasoner_app/source_hygiene/ruff_correction_errors.py": (
        "00bb463b417304075e4fb79195fa063d113112d8383377f736b87bbf3379ad64"
    ),
    "kanda_reasoner_app/source_hygiene/ruff_correction_identity.py": (
        "9702600a026967209ce8a9a148cc54f5771becb4f55880e05286d47ebec66b33"
    ),
    "kanda_reasoner_app/source_hygiene/ruff_correction_models.py": (
        "4a1edb6feaeb6a91ca87b3972edad002451367904ceef144d1d67a410043e56f"
    ),
    "kanda_reasoner_app/source_hygiene/ruff_correction_preview.py": (
        "3a43dd6bde617758c6bb3b6c0899eac9a2ac423aad6c2c2127897534ad7d3448"
    ),
    "kanda_reasoner_app/source_hygiene/ruff_correction_storage.py": (
        "d4bb6b1a5679d59e966ab32392a4a130f505fba72037d8238bf7d838fd3c6c88"
    ),
}


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _validate_patch_zip(path: Path) -> None:
    _assert(path.is_file(), "PATCH_ZIP_MISSING")
    with ZipFile(path) as archive:
        members = archive.namelist()
        names = set(members)
        _assert(len(members) == len(names), "PATCH_ZIP_DUPLICATE_MEMBER")
        _assert(names == EXPECTED_PATCH_FILES, "PATCH_ZIP_FILE_SET_MISMATCH")
        hint = json.loads(archive.read("KANDA_FREEZE_HINT.json"))
    _assert(hint.get("feature_id") == FEATURE_ID, "FREEZE_HINT_FEATURE_ID_MISMATCH")
    _assert(
        hint.get("freeze_readiness") == "requires_local_validation",
        "FREEZE_HINT_READINESS_MISMATCH",
    )
    _assert(
        hint.get("local_validation_status") == "not_run",
        "FREEZE_HINT_LOCAL_STATUS_MISMATCH",
    )
    _assert(
        "User-local" in str(hint.get("validation_evidence_summary") or ""),
        "FREEZE_HINT_LOCAL_VALIDATION_WARNING_MISSING",
    )
    print("PATCH_MEMBER_SCOPE_VALIDATOR_REPAIR_ONLY: PASS")


def _validate_source(project_root: Path) -> None:
    for relative in TOUCHED_PYTHON_FILES:
        path = project_root / relative
        _assert(path.is_file(), "TOUCHED_FILE_MISSING:" + relative)
        text = path.read_text(encoding="utf-8", errors="strict")
        compile(text, str(path), "exec")
        line_count = len(text.splitlines())
        _assert(line_count < 500, "MODULE_SIZE_LIMIT_EXCEEDED:" + relative)
        _assert(text.isascii(), "NON_ASCII_SOURCE:" + relative)
    print("PYTHON_COMPILE: PASS")
    print("MODULE_SIZE_LAW_BELOW_500: PASS")
    print("ASCII_PYTHON_SOURCE: PASS")


def _validate_frozen_identity(project_root: Path) -> None:
    for relative, expected in FROZEN_UNTOUCHED_HASHES.items():
        path = project_root / relative
        _assert(path.is_file(), "FROZEN_FILE_MISSING:" + relative)
        _assert(_sha256(path) == expected, "FROZEN_FILE_CHANGED:" + relative)
    print("FROZEN_PHASE2_PHASE3A_BYTE_IDENTITY: PASS")
    print("PHASE1_UNTOUCHED_ADAPTER_IDENTITY: PASS")


def _validate_phase3b_product_identity(project_root: Path) -> None:
    for relative, expected in PHASE3B_PRODUCT_HASHES.items():
        path = project_root / relative
        _assert(path.is_file(), "PHASE3B_PRODUCT_FILE_MISSING:" + relative)
        _assert(_sha256(path) == expected, "PHASE3B_PRODUCT_FILE_CHANGED:" + relative)
    print("PHASE3B_PRODUCT_BYTE_IDENTITY: PASS")


def _normalize_windows_path_contract(value: object) -> str:
    """Normalize one drive-qualified path for separator-insensitive comparison."""
    return str(PureWindowsPath(str(value).strip())).casefold()


def _catalog_tuple(item: Any) -> tuple[str, str, str]:
    return (item.section, item.label, item.command_name)


def _validate_panel_contract(project_root: Path) -> None:
    sys.path.insert(0, str(project_root))
    try:
        import reasoner_tools_gui_engineering_safety_panel as panel

        _assert(
            panel.__all__ == EXPECTED_PUBLIC_EXPORTS, "PANEL_PUBLIC_EXPORTS_CHANGED"
        )
        field_names = tuple(
            item.name for item in fields(panel.EngineeringSafetyPanelTool)
        )
        _assert(
            field_names == ("section", "label", "command_name", "description"),
            "PANEL_TOOL_FIELDS_CHANGED",
        )
        _assert(
            panel.EngineeringSafetyPanelTool.__module__ == panel.__name__,
            "PANEL_TOOL_PUBLIC_OWNER_CHANGED",
        )
        catalog = tuple(
            _catalog_tuple(item)
            for item in panel.get_engineering_safety_panel_catalog()
        )
        _assert(len(catalog) == len(BASELINE_CATALOG) + 1, "PANEL_CATALOG_COUNT")
        _assert(catalog[2] == NEW_CATALOG_ENTRY, "RUFF_CORRECTION_GUI_ENTRY_POSITION")
        without_new = tuple(item for item in catalog if item[2] != NEW_CATALOG_ENTRY[2])
        _assert(without_new == BASELINE_CATALOG, "EXISTING_PANEL_CATALOG_CHANGED")
        fixture_root = "E:/fixture_project"
        args = list(
            panel.build_engineering_safety_panel_cli_args(
                "ruff-quality",
                fixture_root,
            )
        )
        _assert(
            len(args) == 3 and args[:2] == ["ruff-quality", "--root"],
            "EXISTING_PANEL_COMMAND_SHAPE_CHANGED",
        )
        _assert(
            _normalize_windows_path_contract(args[2])
            == _normalize_windows_path_contract(fixture_root),
            "EXISTING_PANEL_COMMAND_ROOT_CHANGED",
        )
        _assert(
            _normalize_windows_path_contract("E:/fixture_project")
            == _normalize_windows_path_contract(r"E:\fixture_project"),
            "WINDOWS_PATH_SEPARATOR_NORMALIZATION_REGRESSION",
        )
    finally:
        if sys.path and sys.path[0] == str(project_root):
            sys.path.pop(0)
        for name in (
            "reasoner_tools_gui_engineering_safety_panel",
            "_reasoner_tools_gui_engineering_safety_panel_catalog",
        ):
            sys.modules.pop(name, None)
    print("GUI_CATALOG_EXTRACTION_PUBLIC_CONTRACT: PASS")
    print("GUI_EXISTING_COMMAND_ARGS_PRESERVED: PASS")
    print("GUI_WINDOWS_PATH_SEPARATOR_COMPATIBILITY: PASS")
    print("RUFF_CORRECTION_GUI_ENTRY: PASS")


def _validate_lazy_import_and_gates(project_root: Path) -> None:
    panel_path = project_root / "reasoner_tools_gui_engineering_safety_panel.py"
    dialog_path = project_root / "_reasoner_tools_gui_ruff_correction_dialog.py"
    panel_source = panel_path.read_text(encoding="utf-8")
    dialog_source = dialog_path.read_text(encoding="utf-8")
    tree = ast.parse(dialog_source)
    top_imports: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            top_imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            top_imports.append(node.module)
    _assert(
        not any(name.startswith("PySide6") for name in top_imports),
        "PYSIDE6_IMPORTED_AT_MODULE_IMPORT",
    )
    required_fragments = (
        'command_name == "ruff-correction-dialog"',
        "create_ruff_correction_dialog",
        "create_ruff_correction_preview",
        "load_ruff_correction_preview",
        "apply_ruff_correction_preview",
        "QMessageBox.question",
        "token != str(record.confirm_token)",
        "root_edit.setReadOnly(True)",
        "ThreadPoolExecutor(max_workers=1)",
        "QTimer.singleShot",
    )
    combined = panel_source + "\n" + dialog_source
    for fragment in required_fragments:
        _assert(fragment in combined, "GUI_REQUIRED_FRAGMENT_MISSING:" + fragment)
    forbidden = (
        "pip install",
        "--unsafe-fixes",
        "--fix-only",
        "write_text(",
        "write_bytes(",
    )
    _assert(
        not any(item in dialog_source for item in forbidden),
        "GUI_FORBIDDEN_MUTATION_OR_INSTALL",
    )
    print("RUFF_CORRECTION_GUI_LAZY_PYSIDE6: PASS")
    print("RUFF_CORRECTION_GUI_REVIEW_APPLY_GATES: PASS")
    print("RUFF_CORRECTION_GUI_NO_AUTO_INSTALL: PASS")


def _validate_dialog_support(project_root: Path, ruff_executable: str) -> None:
    sys.path.insert(0, str(project_root))
    try:
        import _reasoner_tools_gui_ruff_correction_dialog as support

        _assert(
            support._split_scope_paths("a.py; b\na.py") == ("a.py", "b"),
            "GUI_SCOPE_NORMALIZATION",
        )
        resolved = support._resolve_exact_ruff_executable(
            project_root,
            candidates=(ruff_executable,),
        )
        _assert(
            Path(resolved).resolve() == Path(ruff_executable).resolve(),
            "GUI_EXACT_RUFF_RESOLUTION",
        )
        with tempfile.TemporaryDirectory(prefix="kanda_gui_preview_") as temp_dir:
            diff_path = Path(temp_dir) / "preview.diff"
            diff_path.write_text(
                "--- a.py\n+++ a.py\n",
                encoding="utf-8",
                newline="\n",
            )
            record = SimpleNamespace(
                diff_path=str(diff_path),
                to_dict=lambda: {
                    "preview_id": "preview-test",
                    "status": "PREVIEW_READY",
                },
            )
            rendered = support._preview_text(record)
            _assert("EXACT DIFF" in rendered, "GUI_EXACT_DIFF_HEADING")
            _assert("preview-test" in rendered, "GUI_PREVIEW_MANIFEST_MISSING")
    finally:
        if sys.path and sys.path[0] == str(project_root):
            sys.path.pop(0)
        sys.modules.pop("_reasoner_tools_gui_ruff_correction_dialog", None)
    print("RUFF_CORRECTION_GUI_PINNED_RUFF_RESOLUTION: PASS")
    print("RUFF_CORRECTION_GUI_EXACT_DIFF_RENDERING: PASS")


def _run_ruff(project_root: Path, ruff_executable: str) -> None:
    files = [str(project_root / relative) for relative in TOUCHED_PYTHON_FILES]
    lint = subprocess.run(
        [
            ruff_executable,
            "check",
            "--no-cache",
            "--output-format",
            "concise",
            *files,
        ],
        cwd=project_root,
        capture_output=True,
        text=True,
        check=False,
    )
    _assert(
        lint.returncode == 0,
        "TOUCHED_MODULE_RUFF_LINT:" + lint.stdout + lint.stderr,
    )
    formatting = subprocess.run(
        [ruff_executable, "format", "--check", "--no-cache", *files],
        cwd=project_root,
        capture_output=True,
        text=True,
        check=False,
    )
    _assert(
        formatting.returncode == 0,
        "TOUCHED_MODULE_RUFF_FORMAT:" + formatting.stdout + formatting.stderr,
    )
    print("TOUCHED_MODULE_RUFF_LINT: PASS")
    print("TOUCHED_MODULE_RUFF_FORMAT_CHECK: PASS")


def _validate_pyside6_smoke(project_root: Path, required: bool) -> None:
    try:
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
        from PySide6.QtWidgets import (
            QApplication,
            QLineEdit,
            QPlainTextEdit,
            QPushButton,
        )
    except ImportError:
        if required:
            raise AssertionError("PYSIDE6_REQUIRED_BUT_UNAVAILABLE")
        print("PYSIDE6_RUNTIME_SMOKE: NOT_EXECUTED")
        return

    before = {
        relative: _sha256(project_root / relative)
        for relative in FROZEN_UNTOUCHED_HASHES
    }
    sys.path.insert(0, str(project_root))
    try:
        from _reasoner_tools_gui_ruff_correction_dialog import (
            create_ruff_correction_dialog,
        )

        app = QApplication.instance() or QApplication([])
        dialog = create_ruff_correction_dialog(None, project_root)
        _assert(
            dialog.objectName() == "engineeringSafetyRuffCorrectionDialog",
            "GUI_DIALOG_OBJECT_NAME",
        )
        root_edit = dialog.findChild(QLineEdit, "ruffCorrectionProjectRoot")
        output = dialog.findChild(QPlainTextEdit, "ruffCorrectionOutput")
        apply_button = dialog.findChild(
            QPushButton,
            "ruffCorrectionApplyPreview",
        )
        _assert(
            root_edit is not None and root_edit.isReadOnly(),
            "GUI_ROOT_WIDGET_CONTRACT",
        )
        _assert(
            output is not None and output.isReadOnly(),
            "GUI_OUTPUT_WIDGET_CONTRACT",
        )
        _assert(
            apply_button is not None and not apply_button.isEnabled(),
            "GUI_APPLY_DEFAULT_DISABLED",
        )
        dialog.close()
        app.processEvents()
    finally:
        if sys.path and sys.path[0] == str(project_root):
            sys.path.pop(0)
        sys.modules.pop("_reasoner_tools_gui_ruff_correction_dialog", None)
    after = {
        relative: _sha256(project_root / relative)
        for relative in FROZEN_UNTOUCHED_HASHES
    }
    _assert(before == after, "GUI_SMOKE_MUTATED_FROZEN_SOURCE")
    print("PYSIDE6_RUNTIME_SMOKE: PASS")
    print("GUI_SMOKE_ACTIVE_SOURCE_UNCHANGED: PASS")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--patch-zip", required=True)
    parser.add_argument("--ruff-executable", required=True)
    parser.add_argument("--require-pyside6", action="store_true")
    args = parser.parse_args(list(argv) if argv is not None else None)

    project_root = Path(args.project_root).expanduser().resolve()
    patch_zip = Path(args.patch_zip).expanduser().resolve()
    ruff_executable = str(Path(args.ruff_executable).expanduser().resolve())

    _validate_patch_zip(patch_zip)
    _validate_frozen_identity(project_root)
    _validate_phase3b_product_identity(project_root)
    _validate_source(project_root)
    _validate_panel_contract(project_root)
    _validate_lazy_import_and_gates(project_root)
    _validate_dialog_support(project_root, ruff_executable)
    _run_ruff(project_root, ruff_executable)
    _validate_pyside6_smoke(project_root, bool(args.require_pyside6))
    print("PATCH_ZIP_CONTRACT: PASS")
    print("ZIP CONTRACT: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
