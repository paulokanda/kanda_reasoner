"""Validate Main Workbench orchestration and complete Web AI packaging."""

from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
import hashlib
import importlib
import json
from pathlib import Path
import shutil
import tempfile
from types import SimpleNamespace
import zipfile

FEATURE_ID = "main-workbench-complete-web-ai-orchestration-v1"
PLANNER_DIR = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
)
TOUCHED_FILES = (
    PLANNER_DIR / "gui_shell.py",
    PLANNER_DIR / "workbench_gui.py",
    PLANNER_DIR / "advanced_quality_review_gui.py",
    PLANNER_DIR / "planner_status_projection.py",
    PLANNER_DIR / "main_workbench_state_store.py",
    PLANNER_DIR / "main_workbench_pipeline_models.py",
    PLANNER_DIR / "main_workbench_stage_adapters.py",
    PLANNER_DIR / "main_workbench_stage_worker.py",
    PLANNER_DIR / "main_workbench_pipeline.py",
    PLANNER_DIR / "main_workbench_gui.py",
    PLANNER_DIR / "main_workbench_web_ai_prompt.py",
    PLANNER_DIR / "main_workbench_web_ai_package.py",
    PLANNER_DIR / "main_workbench_web_ai_package_io.py",
    Path("tools/validate_main_workbench_complete_web_ai_orchestration_v1.py"),
    Path("tools/validate_planner_workbench_blocked_plan_correction_ownership_v3.py"),
    Path("tools/validate_large_file_refactor_workbench_gui_progression_v1.py"),
)


@dataclass(frozen=True)
class _PreviewFile:
    relative_path: str
    content_hash: str


@dataclass(frozen=True)
class _Preview:
    status: str
    preview_root: str
    files: tuple[_PreviewFile, ...]
    blockers: tuple[str, ...] = ()


class _Snapshot:
    def __init__(self, target: Path, source_hash: str) -> None:
        self.target_file = str(target)
        self.source_content_hash = source_hash
        self.snapshot_hash = "a" * 64
        self.plan_json = json.dumps(
            {"planned_modules": [{"path": "sample.py"}]},
            sort_keys=True,
        )
        self.analysis_json = json.dumps(
            {"symbols": ["original", "helper"]},
            sort_keys=True,
        )

    def integrity_valid(self) -> bool:
        return True


class _RootEdit:
    def __init__(self, value: str) -> None:
        self._value = value

    def text(self) -> str:
        return self._value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--require-pyside", action="store_true")
    args = parser.parse_args()
    project_root = Path(args.project_root).expanduser().resolve(strict=True)
    _validate_source_files(project_root)
    _validate_static_contracts(project_root)
    _exercise_terminal_seal_and_package(project_root)
    _validate_pyside_imports(project_root, required=args.require_pyside)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


def _validate_source_files(project_root: Path) -> None:
    for relative in TOUCHED_FILES:
        path = project_root / relative
        if not path.is_file():
            raise AssertionError("TOUCHED_FILE_MISSING:" + relative.as_posix())
        data = path.read_bytes()
        if data.startswith(b"\xef\xbb\xbf"):
            raise AssertionError("UTF8_BOM_FORBIDDEN:" + relative.as_posix())
        if any(value > 127 for value in data):
            raise AssertionError("NON_ASCII_SOURCE:" + relative.as_posix())
        text = data.decode("utf-8")
        lines = len(text.splitlines())
        if not 101 <= lines <= 499:
            raise AssertionError(
                "TOUCHED_MODULE_LINE_LAW:" + relative.as_posix() + ":" + str(lines)
            )
        compile(text, str(path), "exec")
        ast.parse(text, filename=str(path))
    print("TOUCHED_PYTHON_MODULES_101_499: PASS")
    print("TOUCHED_PYTHON_COMPILE_AND_AST: PASS")
    print("SOURCE_ASCII_UTF8_NO_BOM: PASS")


def _validate_static_contracts(project_root: Path) -> None:
    gui = _read(project_root, PLANNER_DIR / "main_workbench_gui.py")
    shell = _read(project_root, PLANNER_DIR / "gui_shell.py")
    pipeline = _read(project_root, PLANNER_DIR / "main_workbench_pipeline.py")
    workbench = _read(project_root, PLANNER_DIR / "workbench_gui.py")
    aqr = _read(project_root, PLANNER_DIR / "advanced_quality_review_gui.py")
    package = _read(project_root, PLANNER_DIR / "main_workbench_web_ai_package.py")
    prompt = _read(project_root, PLANNER_DIR / "main_workbench_web_ai_prompt.py")
    required_gui = (
        'QPushButton("Main Workbench")',
        'QPushButton("Send Complete Project to Web AI")',
        "build_main_workbench_controls(window)",
    )
    for token in required_gui:
        if token not in gui + shell:
            raise AssertionError("PLAN_ACTION_CONTROL_MISSING:" + token)
    print("PLAN_ACTIONS_TWO_BUTTON_NORMAL_MODE: PASS")
    adapters = _read(
        project_root,
        PLANNER_DIR / "main_workbench_stage_adapters.py",
    )
    stage_contracts = (
        ("run_workbench_plan_intake_stage", pipeline, workbench),
        ("build_workbench_dependency_readiness", adapters, adapters),
        ("build_and_write_real_preview", adapters, adapters),
        ("validate_real_preview_structure", adapters, adapters),
        ("start_advanced_quality_review_for_window", pipeline, aqr),
    )
    for token, caller_source, owner_source in stage_contracts:
        if token not in caller_source or token not in owner_source:
            raise AssertionError("EXISTING_STAGE_ADAPTER_MISSING:" + token)
    print("EXISTING_WORKBENCH_STAGE_ENGINES_REUSED: PASS")
    worker = _read(
        project_root,
        PLANNER_DIR / "main_workbench_stage_worker.py",
    )
    for token in (
        "QThread",
        "generation",
        "result_ready",
        "failure",
        "settlement_relay.settle",
        "Qt.ConnectionType.QueuedConnection",
    ):
        if token not in worker:
            raise AssertionError("BACKGROUND_STAGE_WORKER_CONTRACT_MISSING:" + token)
    if "MainWorkbenchPackageController" not in gui:
        raise AssertionError("BACKGROUND_PACKAGE_WORKER_CONTROLLER_MISSING")
    if "execute=build_or_reuse_main_workbench_web_ai_package" not in gui:
        raise AssertionError("BACKGROUND_PACKAGE_WORKER_EXECUTION_MISSING")
    print("GENERATION_TAGGED_QTHREAD_STAGE_WORKER: PASS")
    print("GENERATION_TAGGED_QTHREAD_PACKAGE_WORKER: PASS")
    tree = ast.parse(pipeline)
    forbidden_calls = {
        "build_and_write_source_apply_payload",
        "prepare_preflight_backup",
        "apply_refactor_transaction",
        "refactor_large_module",
    }
    observed_calls = {
        _call_name(node.func)
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
    }
    blocked = sorted(forbidden_calls.intersection(observed_calls))
    if blocked:
        raise AssertionError("CANONICAL_SOURCE_APPLY_CALL_PRESENT:" + ",".join(blocked))
    print("MAIN_WORKBENCH_CANONICAL_SOURCE_MUTATION_DISABLED: PASS")
    pipeline_models = _read(
        project_root,
        PLANNER_DIR / "main_workbench_pipeline_models.py",
    )
    for token in (
        "STALE_AFTER_EXTERNAL_SOURCE_MUTATION",
        "READY_FOR_WEB_AI",
        "WEB_AI_REQUIRED_WITH_BLOCKERS",
        "CANCELLED",
    ):
        if token not in pipeline_models:
            raise AssertionError("PIPELINE_TERMINAL_STATE_MISSING:" + token)
    print("PIPELINE_TERMINAL_STATE_CONTRACT: PASS")
    for token in (
        ".partial-",
        "partial_root.replace(final_root)",
        "partial_zip.replace(final_zip)",
        "capture_main_workbench_web_ai_package_request",
        "verify_package_manifest",
    ):
        if token not in package:
            raise AssertionError("ATOMIC_PACKAGE_CONTRACT_MISSING:" + token)
    print("ATOMIC_PACKAGE_PUBLICATION_CONTRACT: PASS")
    if "The next AI has no prior knowledge" not in prompt:
        raise AssertionError("SELF_CONTAINED_WEB_AI_CONTEXT_MISSING")
    if "project_source folder contains the bounded Python project tree" not in prompt:
        raise AssertionError("BOUNDED_PROJECT_CONTEXT_INSTRUCTION_MISSING")
    if "KANDA Reasoner Tool is the reusable card machine" not in prompt:
        raise AssertionError("TOOL_PROJECT_OWNERSHIP_CONTEXT_MISSING")
    print("SELF_CONTAINED_WEB_AI_HANDOFF_CONTEXT: PASS")


def _exercise_terminal_seal_and_package(project_root: Path) -> None:
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.main_workbench_state_store import (
        build_main_workbench_terminal_seal,
        terminal_seal_is_current,
    )
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.main_workbench_web_ai_package import (
        build_or_reuse_main_workbench_web_ai_package,
        capture_main_workbench_web_ai_package_request,
    )

    test_root = Path(tempfile.mkdtemp(prefix="kanda-main-workbench-validation-"))
    support_root: Path | None = None
    try:
        active_project = test_root / "sample_project"
        target = active_project / "pkg" / "sample.py"
        target.parent.mkdir(parents=True)
        target.write_text("def original():\n    return 1\n", encoding="utf-8")
        baseline = target.read_bytes()
        baseline_hash = _hash_bytes(baseline)
        preview_root = test_root / "preview_support"
        preview_root.mkdir()
        candidate = preview_root / "sample.py"
        candidate.write_text(
            "def original():\n    return 1\n\ndef helper():\n    return 2\n",
            encoding="utf-8",
        )
        preview = _Preview(
            status="real_preview_written",
            preview_root=str(preview_root),
            files=(
                _PreviewFile(
                    relative_path="sample.py",
                    content_hash=_hash_bytes(candidate.read_bytes()),
                ),
            ),
        )
        snapshot = _Snapshot(target, baseline_hash)
        window = SimpleNamespace(
            _root_path_edit=_RootEdit(str(active_project)),
            _large_file_refactor_workbench_plan_snapshot=snapshot,
            _large_file_refactor_workbench_real_preview=preview,
            _large_file_refactor_workbench_structural_validation={"status": "passed"},
            _large_file_refactor_workbench_advanced_quality_review={"decision": "PASS"},
            _large_file_refactor_workbench_aqr_context=None,
        )
        seal = build_main_workbench_terminal_seal(
            window,
            active_project_root=str(active_project),
            generation=1,
            terminal_status="READY_FOR_WEB_AI",
            blockers=(),
        )
        if not terminal_seal_is_current(window, seal):
            raise AssertionError("FRESH_TERMINAL_SEAL_REJECTED")
        request = capture_main_workbench_web_ai_package_request(
            window=window,
            active_project_root=active_project,
            terminal_seal=seal,
        )
        first = build_or_reuse_main_workbench_web_ai_package(request)
        second = build_or_reuse_main_workbench_web_ai_package(request)
        if first.exchange_id != "EXCH-0001" or first.reused:
            raise AssertionError("FIRST_EXCHANGE_GENERATION_INVALID")
        if second.exchange_id != first.exchange_id or not second.reused:
            raise AssertionError("IDENTICAL_PACKAGE_NOT_REUSED")
        rerun_seal = build_main_workbench_terminal_seal(
            window,
            active_project_root=str(active_project),
            generation=2,
            terminal_status="READY_FOR_WEB_AI",
            blockers=(),
        )
        rerun_request = capture_main_workbench_web_ai_package_request(
            window=window,
            active_project_root=active_project,
            terminal_seal=rerun_seal,
        )
        rerun = build_or_reuse_main_workbench_web_ai_package(rerun_request)
        if rerun.exchange_id != first.exchange_id or not rerun.reused:
            raise AssertionError("IDENTICAL_RERUN_CREATED_DUPLICATE_EXCHANGE")
        if target.read_bytes() != baseline:
            raise AssertionError("PACKAGE_BUILD_MUTATED_CANONICAL_SOURCE")
        _assert_zip_contract(Path(first.zip_path))
        support_root = active_project.parent / (active_project.name + "_show_project_to_AI")
        try:
            Path(first.zip_path).resolve().relative_to(support_root.resolve())
        except ValueError as error:
            raise AssertionError("PACKAGE_ESCAPES_PROJECT_SUPPORT") from error
        print("PROJECT_OWNED_TERMINAL_SEAL_CURRENT: PASS")
        print("IDENTICAL_PACKAGE_IDENTITY_REUSED: PASS")
        print("IDENTICAL_PIPELINE_RERUN_REUSES_EXCHANGE: PASS")
        print("COMPLETE_PACKAGE_ZIP_REOPEN: PASS")
        print("ACTIVE_PROJECT_SOURCE_NOT_MUTATED: PASS")
        print("TOOL_PROJECT_LOGICAL_OWNERSHIP_SEPARATION: PASS")
        Path(first.zip_path).write_bytes(b"corrupt zip")
        repaired = build_or_reuse_main_workbench_web_ai_package(rerun_request)
        if repaired.exchange_id != "EXCH-0002" or repaired.reused:
            raise AssertionError("CORRUPT_REUSABLE_PACKAGE_WAS_ACCEPTED")
        print("CORRUPT_REUSABLE_PACKAGE_REJECTED: PASS")
        window._large_file_refactor_workbench_structural_validation = {
            "status": "passed_with_warnings",
            "warnings": ["synthetic changed evidence"],
        }
        if terminal_seal_is_current(window, seal):
            raise AssertionError("CHANGED_EVIDENCE_DID_NOT_INVALIDATE_SEAL")
        changed_seal = build_main_workbench_terminal_seal(
            window,
            active_project_root=str(active_project),
            generation=2,
            terminal_status="READY_FOR_WEB_AI",
            blockers=(),
        )
        changed_request = capture_main_workbench_web_ai_package_request(
            window=window,
            active_project_root=active_project,
            terminal_seal=changed_seal,
        )
        changed = build_or_reuse_main_workbench_web_ai_package(changed_request)
        if changed.exchange_id != "EXCH-0003" or changed.reused:
            raise AssertionError("CHANGED_EVIDENCE_DID_NOT_CREATE_NEW_EXCHANGE")
        print("CHANGED_EVIDENCE_NEW_EXCHANGE_GENERATION: PASS")
        target.write_text("def externally_changed():\n    return 9\n", encoding="utf-8")
        if terminal_seal_is_current(window, changed_seal):
            raise AssertionError("EXTERNAL_SOURCE_MUTATION_NOT_DETECTED")
        print("EXTERNAL_SOURCE_MUTATION_INVALIDATES_SEND: PASS")
    finally:
        shutil.rmtree(test_root, ignore_errors=True)
        if support_root is not None:
            shutil.rmtree(support_root, ignore_errors=True)


def _assert_zip_contract(path: Path) -> None:
    required = {
        "EXTERNAL_AI_TASK.md",
        "EXCHANGE_MANIFEST.json",
        "lineage/CANDIDATE_SET_IDENTITY.json",
        "lineage/EXCHANGE_IDENTITY.json",
        "context/main_workbench_terminal_seal.json",
        "context/ownership_model.json",
        "project_source/pkg/sample.py",
    }
    with zipfile.ZipFile(path) as archive:
        members = {item.filename for item in archive.infolist() if not item.is_dir()}
        if not required.issubset(members):
            missing = sorted(required.difference(members))
            raise AssertionError("PACKAGE_MEMBER_MISSING:" + ",".join(missing))
        if not any(name.startswith("candidate_family/") for name in members):
            raise AssertionError("CANDIDATE_FAMILY_MISSING")
        manifest = json.loads(archive.read("EXCHANGE_MANIFEST.json").decode("utf-8"))
        if not manifest.get("candidate_files"):
            raise AssertionError("CANDIDATE_MANIFEST_EMPTY")


def _validate_pyside_imports(project_root: Path, *, required: bool) -> None:
    try:
        importlib.import_module("PySide6")
    except ModuleNotFoundError:
        if required:
            raise AssertionError("REAL_PYSIDE6_GUI_IMPORT_SMOKE_UNAVAILABLE")
        print("REAL_PYSIDE6_GUI_IMPORT_SMOKE: SKIP_UNAVAILABLE")
        return
    modules = (
        "kanda_reasoner_app.manage_architecture.large_file_refactor_planner.main_workbench_pipeline_models",
        "kanda_reasoner_app.manage_architecture.large_file_refactor_planner.main_workbench_stage_adapters",
        "kanda_reasoner_app.manage_architecture.large_file_refactor_planner.main_workbench_stage_worker",
        "kanda_reasoner_app.manage_architecture.large_file_refactor_planner.main_workbench_pipeline",
        "kanda_reasoner_app.manage_architecture.large_file_refactor_planner.main_workbench_gui",
        "kanda_reasoner_app.manage_architecture.large_file_refactor_planner.gui_shell",
    )
    for name in modules:
        importlib.import_module(name)
    print("REAL_PYSIDE6_GUI_IMPORT_SMOKE: PASS")


def _read(project_root: Path, relative: Path) -> str:
    return (project_root / relative).read_text(encoding="utf-8")


def _call_name(node: ast.expr) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return ""


def _hash_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
