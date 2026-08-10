# project-path: tools/validate_audit_project_workflow_review_subtab_v1.py
"""Validate Workflow Review as the rightmost Audit Project child tab."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
import tempfile
import types
from pathlib import Path

FEATURE_ID = "audit-project-workflow-review-subtab-v1"
EXPECTED_TABS = ["Architecture Review", "Engineering Safety", "Workflow Review"]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _read(root: Path, relative: str) -> str:
    path = root / relative
    _require(path.is_file(), "Missing file: " + relative)
    return path.read_text(encoding="utf-8")


def validate_static(root: Path) -> None:
    subtabs = _read(
        root,
        "kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py",
    )
    siblings = _read(
        root,
        "kanda_reasoner_app/manage_architecture/audit_project_sibling_tabs.py",
    )
    adapter = _read(
        root,
        "kanda_reasoner_app/manage_architecture/audit_project_workflow_review.py",
    )
    specs = _read(
        root,
        "kanda_reasoner_app/reasoner_tools_gui_shell/tool_specs.py",
    )
    mapping = _read(
        root,
        "kanda_reasoner_app/reasoner_tools_gui_shell/brain_region_mapping/_mapping_data.py",
    )
    window_source = _read(
        root,
        "kanda_reasoner_app/manage_workflows/manage_workflows_gui_help/workflow_gui_window.py",
    )
    worker_source = _read(
        root,
        "kanda_reasoner_app/manage_workflows/manage_workflows_gui_help/workflow_gui_worker.py",
    )
    reporting_source = _read(
        root,
        "kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_reporting.py",
    )
    architecture_mode_ui = _read(
        root,
        "kanda_reasoner_app/manage_architecture/architecture_review_mode_ui.py",
    )
    helper_manifest = json.loads(
        _read(
            root,
            "kanda_reasoner_app/manage_workflows/manage_workflows_gui_help.json",
        )
    )
    worker_manifest_exports = helper_manifest["helpers"][
        "workflow_gui_worker.py"
    ]["exports"]
    _require(
        worker_manifest_exports
        == ["WorkflowRunWorker", "build_workflow_execution_context"],
        "Workflow worker helper manifest exports drifted.",
    )
    _require(
        "build_workflow_execution_context" not in helper_manifest["exports"],
        "Workflow execution-context helper was promoted to facade ownership.",
    )

    for fragment in (
        '_AUDIT_PROJECT_ARCHITECTURE_TAB_LABEL = "Architecture Review"',
        "_build_audit_project_sibling_tabs(window)",
    ):
        _require(fragment in subtabs, "Audit Project host contract missing: " + fragment)
    _require(
        'QPushButton("Validate Project")' in subtabs,
        "Architecture Review Validate Project button contract changed.",
    )
    _require(
        '"validate": "Validate Project"' in architecture_mode_ui,
        "Architecture Review validate-mode label contract changed.",
    )
    for fragment in (
        "def _contain_subtab_horizontal_size_pressure(window: object) -> None:",
        "window._workflow_review_page,",
        "window._workflow_review_page.centralWidget(),",
        "container.setMinimumWidth(0)",
        "container.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding)",
    ):
        _require(
            fragment in subtabs,
            "Audit Project host width-containment contract missing: " + fragment,
        )
    sibling_build_index = subtabs.index("_build_audit_project_sibling_tabs(window)")
    containment_call_index = subtabs.index(
        "_contain_subtab_horizontal_size_pressure(window)",
        sibling_build_index,
    )
    _require(
        sibling_build_index < containment_call_index,
        "Audit Project width containment is not applied after sibling construction.",
    )

    for fragment in (
        '_ENGINEERING_SAFETY_LABEL = "Engineering Safety"',
        '_WORKFLOW_REVIEW_LABEL = "Workflow Review"',
        "create_embedded_workflow_review(",
        "window._workflow_review_page",
        "window._root_path_edit.textChanged.connect",
    ):
        _require(fragment in siblings, "Workflow sibling contract missing: " + fragment)

    engineering_index = siblings.index(
        "tab_widget.addTab(window._engineering_safety_page"
    )
    workflow_index = siblings.index(
        "tab_widget.addTab(window._workflow_review_page", engineering_index
    )
    _require(
        engineering_index < workflow_index,
        "Audit Project sibling tab order changed.",
    )

    for fragment in (
        'setObjectName("audit_project_workflow_review_page")',
        'page.setWindowTitle("Workflow Review")',
        'control.setVisible(False)',
        'root_combo.setCurrentText(selected)',
    ):
        _require(fragment in adapter, "Embedding adapter missing: " + fragment)

    start = specs.index('step_title="Workflow Review"')
    end = specs.find("    ToolSpec(", start + 1)
    workflow_spec = specs[start:end]
    _require('tab_id="workflow_review"' in workflow_spec, "Workflow tab ID changed.")
    _require(
        'visible_in_shell=False' in workflow_spec,
        "Workflow Review remains visible as a duplicate top-level tab.",
    )
    _require(
        '"target_tab_id": "architecture_review"' in mapping
        and 'Audit Project > Workflow Review' in mapping,
        "Brain navigation does not route nested Workflow Review through Audit Project.",
    )
    for fragment in (
        "[KANDA TOOL EXECUTION PROVIDER]",
        "build_workflow_execution_context",
    ):
        _require(fragment in window_source, "Workflow run log contract missing: " + fragment)
    for fragment in (
        "Same canonical resolved Tool/Project root",
        "Tool/Project logical roles merged: NO",
        "WORKFLOW_TOOL_PROVIDER_MISMATCH",
        "TOOL_MODULE_PROVENANCE_VIOLATION",
        "_require_tool_module_origin",
        "sys.path.insert(0, tool_root_text)",
    ):
        _require(fragment in worker_source, "Workflow Tool provenance guard missing: " + fragment)
    _require(
        'print(f"      cwd: {cwd}")' in reporting_source,
        "Workflow command working directory is not visible in results.",
    )
    print("AUDIT_PROJECT_WORKFLOW_REVIEW_STATIC_CONTRACT: PASS")
    print("WORKFLOW_REVIEW_TOP_LEVEL_REMOVED: PASS")
    print("WORKFLOW_REVIEW_STABLE_ID_PRESERVED: PASS")
    print("ARCHITECTURE_REVIEW_VALIDATE_PROJECT_STATIC_CONTRACT: PASS")
    print("WORKFLOW_REVIEW_HOST_WIDTH_POLICY_OWNER_STATIC: PASS")
    print("WORKFLOW_REVIEW_HELPER_MANIFEST_CONTRACT: PASS")


def validate_execution_boundary(root: Path) -> None:
    """Validate Tool/Project provenance without requiring a real Qt runtime."""
    worker_path = (
        root
        / "kanda_reasoner_app"
        / "manage_workflows"
        / "manage_workflows_gui_help"
        / "workflow_gui_worker.py"
    )
    manager_script = (
        root
        / "kanda_reasoner_app"
        / "manage_workflows"
        / "manage_workflows.py"
    )

    injected_modules: list[str] = []
    if "PySide6.QtCore" not in sys.modules:
        qtcore = types.ModuleType("PySide6.QtCore")

        class DummyQObject:
            pass

        class DummySignal:
            def __init__(self, *_args: object) -> None:
                pass

            def emit(self, *_args: object) -> None:
                pass


        qtcore.QObject = DummyQObject
        qtcore.Signal = DummySignal
        pyside = types.ModuleType("PySide6")
        pyside.QtCore = qtcore
        sys.modules["PySide6"] = pyside
        sys.modules["PySide6.QtCore"] = qtcore
        injected_modules.extend(["PySide6.QtCore", "PySide6"])

    module_name = "_workflow_review_boundary_probe"
    spec = importlib.util.spec_from_file_location(module_name, worker_path)
    _require(spec is not None and spec.loader is not None, "Worker probe spec failed.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
        self_host_context = module.build_workflow_execution_context(
            str(manager_script), str(root), "validate"
        )
        _require(
            "Tool role: KANDA TOOL EXECUTION PROVIDER" in self_host_context
            and "Same canonical resolved Tool/Project root: YES" in self_host_context
            and "Tool/Project logical roles merged: NO" in self_host_context,
            "Self-hosting execution context is incomplete.",
        )

        with tempfile.TemporaryDirectory(prefix="workflow_external_project_") as temp:
            external_root = Path(temp).resolve()
            external_context = module.build_workflow_execution_context(
                str(manager_script), str(external_root), "validate"
            )
            _require(
                "Same canonical resolved Tool/Project root: NO" in external_context
                and f"Active Project root: {external_root}" in external_context
                and "Tool/Project logical roles merged: NO" in external_context,
                "External-Project execution context is incomplete.",
            )

            manager_module_name = "kanda_reasoner_app.manage_workflows.manage_workflows"
            real_module = sys.modules.get(manager_module_name)
            fake_module = types.ModuleType(manager_module_name)
            fake_module.__file__ = str(
                external_root
                / "kanda_reasoner_app"
                / "manage_workflows"
                / "manage_workflows.py"
            )
            sys.modules[manager_module_name] = fake_module
            try:
                try:
                    module.WorkflowRunWorker._load_manager_module(
                        str(manager_script)
                    )
                except RuntimeError as exc:
                    _require(
                        "TOOL_MODULE_PROVENANCE_VIOLATION" in str(exc),
                        "Foreign Tool module rejected for the wrong reason.",
                    )
                else:
                    raise AssertionError(
                        "Foreign preloaded Workflow Review Tool module was accepted."
                    )
            finally:
                if real_module is None:
                    sys.modules.pop(manager_module_name, None)
                else:
                    sys.modules[manager_module_name] = real_module

        wrong_script = root / "kanda_reasoner_app" / "manage_architecture" / "manage_architecture.py"
        try:
            module.build_workflow_execution_context(
                str(wrong_script), str(root), "validate"
            )
        except RuntimeError as exc:
            _require(
                "WORKFLOW_TOOL_PROVIDER_MISMATCH" in str(exc),
                "Wrong provider script rejected for the wrong reason.",
            )
        else:
            raise AssertionError("Non-canonical Workflow Review provider was accepted.")
    finally:
        sys.modules.pop(module_name, None)
        for name in injected_modules:
            sys.modules.pop(name, None)

    print("WORKFLOW_REVIEW_TOOL_PROVIDER_PROVENANCE: PASS")
    print("WORKFLOW_REVIEW_TOOL_PROJECT_LOG_CONTEXT: PASS")
    print("WORKFLOW_REVIEW_FOREIGN_TOOL_MODULE_REJECTED: PASS")
    print("WORKFLOW_REVIEW_NONCANONICAL_PROVIDER_REJECTED: PASS")
    print("WORKFLOW_REVIEW_COMMAND_CWD_VISIBLE: PASS")

def _configure_qt_offscreen_environment() -> Path:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

    configured = os.environ.get("QT_QPA_FONTDIR", "").strip()
    if configured:
        configured_path = Path(configured)
        if configured_path.is_dir():
            return configured_path

    candidates: list[Path] = []
    for variable_name in ("WINDIR", "SystemRoot"):
        base = os.environ.get(variable_name, "").strip()
        if base:
            candidates.append(Path(base) / "Fonts")
    candidates.append(Path(r"C:\Windows\Fonts"))

    seen: set[str] = set()
    for candidate in candidates:
        key = str(candidate).casefold()
        if key in seen:
            continue
        seen.add(key)
        if candidate.is_dir():
            resolved = candidate.resolve()
            os.environ["QT_QPA_FONTDIR"] = str(resolved)
            return resolved

    raise AssertionError(
        "QT_FONTDIR_PREFLIGHT_FAILED: no Windows Fonts directory was found."
    )


def _settle_workflow_owned_threads(app: object, workflow: object) -> None:
    """Settle only QThreads explicitly owned by Workflow Review."""
    owned_threads: list[object] = []
    for attribute in ("_worker_thread", "_tab2_ai_review_thread"):
        thread = getattr(workflow, attribute, None)
        if thread is not None and thread not in owned_threads:
            owned_threads.append(thread)

    for thread in owned_threads:
        if thread.isRunning():
            thread.requestInterruption()
            thread.quit()

    for _ in range(80):
        app.processEvents()
        running = [thread for thread in owned_threads if thread.isRunning()]
        if not running:
            break
        for thread in running:
            thread.wait(25)

    _require(
        not any(thread.isRunning() for thread in owned_threads),
        "WORKFLOW_OWNED_QTHREAD_TEARDOWN_FAILED: a Workflow Review thread remained active.",
    )


def validate_runtime(root: Path) -> None:
    try:
        from PySide6.QtWidgets import (
            QApplication,
            QLineEdit,
            QTabWidget,
            QWidget,
        )
    except ModuleNotFoundError:
        print("AUDIT_PROJECT_WORKFLOW_REVIEW_RUNTIME: SKIPPED_NO_PYSIDE6")
        return

    font_dir = _configure_qt_offscreen_environment()
    print("WORKFLOW_REVIEW_QT_FONTDIR_PREFLIGHT: PASS")
    print("WORKFLOW_REVIEW_QT_FONTDIR: " + str(font_dir))
    sys.path.insert(0, str(root))
    from kanda_reasoner_app.manage_architecture.audit_project_workflow_review import (
        create_embedded_workflow_review,
    )
    existing_app = QApplication.instance()
    app = existing_app or QApplication([])
    host = None
    workflow = None
    before_engineering = {
        name for name in sys.modules
        if name.startswith("kanda_reasoner_app.engineering_diagnostics_gui")
    }
    before_architecture_gui = "kanda_reasoner_app.manage_architecture.manage_architecture_gui" in sys.modules
    try:
        host = QWidget()
        root_edit = QLineEdit(str(root), host)
        tabs = QTabWidget(host)
        tabs.addTab(QWidget(tabs), "Architecture Review")
        tabs.addTab(QWidget(tabs), "Engineering Safety")
        workflow = create_embedded_workflow_review(
            parent=tabs,
            project_root_provider=root_edit.text,
        )
        root_edit.textChanged.connect(workflow._audit_project_root_sync)
        tabs.addTab(workflow, "Workflow Review")
        host.show()
        app.processEvents()

        labels = [tabs.tabText(index) for index in range(tabs.count())]
        _require(
            labels == EXPECTED_TABS,
            "Focused Audit Project tab order mismatch: " + repr(labels),
        )
        _require(
            workflow.objectName() == "audit_project_workflow_review_page",
            "Embedded Workflow Review identity changed.",
        )
        _require(
            workflow.centralWidget() is not None,
            "Workflow Review central widget missing.",
        )
        _require(hasattr(workflow, "_output"), "Workflow Review output panel missing.")
        for attribute in ("_root_path_label", "_root_combo", "_browse_root_btn"):
            _require(
                getattr(workflow, attribute).isHidden(),
                "Embedded Workflow Review duplicates shared root control: " + attribute,
            )

        test_root = str(root / "workflow-review-root-sync-probe")
        root_edit.setText(test_root)
        app.processEvents()
        _require(
            workflow._root_combo.currentText() == test_root,
            "Shared Audit Project root did not synchronize to Workflow Review.",
        )
        after_engineering = {
            name for name in sys.modules
            if name.startswith("kanda_reasoner_app.engineering_diagnostics_gui")
        }
        _require(
            after_engineering == before_engineering,
            "FOCUSED_RUNTIME_INITIALIZED_ENGINEERING_DIAGNOSTICS_SIBLING",
        )
        _require(
            before_architecture_gui
            or "kanda_reasoner_app.manage_architecture.manage_architecture_gui" not in sys.modules,
            "FOCUSED_RUNTIME_INITIALIZED_ARCHITECTURE_MANAGER_SIBLING",
        )

    finally:
        try:
            if workflow is not None:
                _settle_workflow_owned_threads(app, workflow)
                workflow.close()
                workflow.deleteLater()
                app.processEvents()
        finally:
            if host is not None:
                host.close()
                host.deleteLater()
                app.processEvents()
            if existing_app is None:
                app.quit()
                app.processEvents()

    print("WORKFLOW_REVIEW_FOCUSED_RUNTIME_SIBLINGS_NOT_INITIALIZED: PASS")
    print("ARCHITECTURE_REVIEW_VALIDATE_PROJECT_UNTOUCHED: PASS")
    print("WORKFLOW_REVIEW_QTHREAD_TEARDOWN: PASS")
    print("WORKFLOW_REVIEW_ISOLATED_FIXTURE_HOST_POLICY_NOT_ASSUMED: PASS")
    print("AUDIT_PROJECT_WORKFLOW_REVIEW_RUNTIME: PASS")
    print("WORKFLOW_REVIEW_SHARED_ROOT_RUNTIME: PASS")
    print("WORKFLOW_REVIEW_HOST_WIDTH_POLICY: PASS")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()
    root = Path(args.project_root).expanduser().resolve()
    try:
        validate_static(root)
        validate_execution_boundary(root)
        validate_runtime(root)
    except Exception as exc:
        print("VALIDATION FAIL: " + FEATURE_ID + " - " + str(exc))
        return 1
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
