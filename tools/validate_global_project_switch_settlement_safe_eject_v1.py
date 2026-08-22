# project-path: tools/validate_global_project_switch_settlement_safe_eject_v1.py
"""Validate global Project settlement, safe eject, and re-selection."""

from __future__ import annotations

import argparse
import ast
import os
import sys
import tempfile
from pathlib import Path

FEATURE_ID = "global-project-switch-settlement-safe-eject-v1"

TOUCHED_FILES = (
    "kanda_reasoner_app/reasoner_tools_gui_shell/main_window.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/project_scope_sync.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/main_window_help/window_project_root.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/main_window_help/window_tool_patches.py",
    "tools/validate_shell_active_project_sync_v1.py",
    "tools/validate_global_project_switch_settlement_safe_eject_v1.py",
)


def require(condition: bool, message: str) -> None:
    """Raise one deterministic validation failure."""
    if not condition:
        raise AssertionError(message)


def read_source(project_root: Path, relative_path: str) -> str:
    """Read one required UTF-8 source file."""
    path = project_root / relative_path
    require(path.is_file(), "missing source file: " + relative_path)
    return path.read_text(encoding="utf-8")


def function_text(source_text: str, function_name: str) -> str:
    """Return one top-level or class method source segment."""
    tree = ast.parse(source_text)
    lines = source_text.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name == function_name and node.end_lineno is not None:
                return "\n".join(lines[node.lineno - 1 : node.end_lineno])
    raise AssertionError("function not found: " + function_name)


def validate_static(project_root: Path) -> None:
    """Validate exact source ownership, contracts, and module-size gates."""
    sources = {
        relative: read_source(project_root, relative)
        for relative in TOUCHED_FILES
    }
    for relative, text in sources.items():
        ast.parse(text, filename=relative)
        line_count = len(text.splitlines())
        require(
            100 < line_count < 500,
            relative + " must remain strictly within 101-499 physical lines",
        )
    print("TOUCHED_SOURCE_MODULES_STRICTLY_101_TO_499: PASS")

    main = sources[TOUCHED_FILES[0]]
    scope = sources[TOUCHED_FILES[1]]
    roots = sources[TOUCHED_FILES[2]]
    patches = sources[TOUCHED_FILES[3]]

    require(
        'QPushButton("Select Active Project", central)' in main
        and 'QPushButton("Eject Active Project", central)' in main
        and "self._refresh_active_project_controls()" in main,
        "shell-level Project controls are missing",
    )
    print("GLOBAL_PROJECT_CONTROLS_PRESENT: PASS")

    require(
        "def project_eject_block(" in scope
        and "def request_project_scope_settlement(" in scope
        and 'getattr(widget, "request_project_scope_settlement", None)' in scope,
        "public Project-scope settlement facade is missing",
    )
    print("PUBLIC_PROJECT_SCOPE_LIFECYCLE_FACADE: PASS")

    require(
        'tab_id == "project_web_ai"' in scope
        and 'getattr(widget, "stop_request", None)' in scope
        and "waiting_for_worker" in scope
        and 'getattr(widget, "_chat_thread", None) is not None' in scope,
        "Project Web AI settlement ownership is incomplete",
    )
    print("PROJECT_WEB_AI_SETTLEMENT_GUARD: PASS")

    eject_text = function_text(roots, "_perform_project_eject")
    require(
        "clear_current_selection()" in eject_text
        and "self._project_switch_ticket += 1" in eject_text
        and "self.current_project_root = None" in eject_text
        and "self._set_loaded_project_scopes_enabled(False)" in eject_text,
        "safe eject does not clear authority and disable Project scope",
    )
    forbidden_delete_tokens = (
        ".unlink(",
        "rmtree(",
        "Remove-Item",
        "project_freeze_ledger",
    )
    require(
        not any(token in eject_text for token in forbidden_delete_tokens),
        "safe eject contains a durable delete or wrong-store operation",
    )
    print("SAFE_EJECT_AUTHORITY_CLEAR_WITHOUT_DURABLE_DELETE: PASS")

    require(
        "_apply_project_widget_enabled_state(spec.tab_id, widget)" in patches
        and "_set_loaded_project_scopes_enabled(True)" in patches,
        "lazy Project tabs do not follow selected/ejected availability",
    )
    print("LAZY_PROJECT_TAB_AVAILABILITY_SYNC: PASS")



def validate_architecture(project_root: Path) -> None:
    """Require zero focused architecture warnings and symbol shadowing."""
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from kanda_reasoner_app.manage_architecture import manage_architecture as architecture

    modules = {}
    for relative in TOUCHED_FILES:
        module, warnings = architecture.scan_module(
            project_root,
            project_root / relative,
            set(),
        )
        require(not warnings, relative + " warnings: " + repr(warnings))
        modules[module.module_id] = module
    issues = architecture.detect_symbol_shadowing_issues(project_root, modules)
    require(not issues, "focused symbol shadowing remains: " + repr(issues))
    print("FOCUSED_ARCHITECTURE_WARNINGS_ZERO: PASS")
    print("FOCUSED_SYMBOL_SHADOWING_ZERO: PASS")

def configure_qt_environment() -> None:
    """Configure deterministic offscreen Qt and Windows font preflight."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    if os.name != "nt":
        return
    candidates = []
    windir = os.environ.get("WINDIR", "").strip()
    if windir:
        candidates.append(Path(windir) / "Fonts")
    candidates.append(Path("C:/Windows/Fonts"))
    for candidate in candidates:
        if candidate.is_dir():
            os.environ.setdefault("QT_QPA_FONTDIR", str(candidate))
            print("QT_OFFSCREEN_FONTDIR_PREFLIGHT: PASS")
            return
    raise AssertionError("No Windows font directory was available for Qt")


def validate_real_qt(project_root: Path) -> None:
    """Exercise blocking, settlement, eject, preservation, and re-selection."""
    configure_qt_environment()
    try:
        from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QWidget
    except ImportError:
        print("REAL_QT_SAFE_EJECT: NOT_APPLICABLE")
        return

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry
    from kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_project_root import (
        _WindowProjectRootMixin,
    )
    from kanda_reasoner_app.reasoner_tools_gui_shell.main_window_help.window_tool_patches import (
        _WindowToolPatchesMixin,
    )
    from kanda_reasoner_app.reasoner_tools_gui_shell.project_scope_sync import (
        project_eject_block,
        request_project_scope_settlement,
    )

    app = QApplication.instance() or QApplication([])

    class LifecycleTab(QWidget):
        def __init__(self) -> None:
            super().__init__()
            self.project_root_edit = QLineEdit()
            self.active = True
            self.cancel_requests = 0
            self.applied_roots: list[str] = []

        def project_scope_switch_block_reason(self) -> str:
            return "focused operation is still running" if self.active else ""

        def request_project_scope_settlement(self) -> None:
            self.cancel_requests += 1

        def set_project_root(self, project_root: Path) -> None:
            root_text = str(project_root)
            self.applied_roots.append(root_text)
            self.project_root_edit.setText(root_text)

    class GlobalTab(QWidget):
        pass

    class WebSession:
        transaction_blocks_project_switch = False
        waiting_for_worker = True

    class WebTab(QWidget):
        def __init__(self) -> None:
            super().__init__()
            self._project_session = WebSession()
            self._chat_thread = object()
            self.stop_count = 0

        def stop_request(self) -> None:
            self.stop_count += 1

    class Harness(_WindowProjectRootMixin, _WindowToolPatchesMixin):
        def __init__(self, registry: ProjectSelectionRegistry, boundary) -> None:
            self._project_selection_registry = registry
            self.current_project_boundary = boundary
            self.current_project_root = boundary.active_project_root
            self._loaded_tools_by_tab_id: dict[str, QWidget] = {}
            self._collector_widget = None
            self._daily_refactor_widget = None
            self._is_propagating_project_root = False
            self._project_switch_ticket = 7
            self._project_root_field_names = ("project_root_edit",)
            self._prefs: dict[str, object] = {}
            self.active_project_value = QLabel()
            self.select_project_button = QPushButton()
            self.eject_project_button = QPushButton()
            self.saved_preferences = 0
            self.switch_blocks: list[str] = []

        def _save_prefs(self) -> None:
            self.saved_preferences += 1

        def _show_project_switch_block(self, reason: str) -> None:
            self.switch_blocks.append(reason)

    with tempfile.TemporaryDirectory(prefix="kanda-safe-eject-") as temp_dir:
        temp_root = Path(temp_dir).resolve()
        project_a = temp_root / "project_a"
        project_b = temp_root / "project_b"
        project_a.mkdir()
        project_b.mkdir()
        registry_path = temp_root / "tool_support" / "projects.json"
        registry = ProjectSelectionRegistry(
            tool_source_root=project_root,
            registry_path=registry_path,
        )
        boundary = registry.register_explicit_root(project_a)
        durable_root = boundary.active_project_support_root
        durable_root.mkdir(parents=True, exist_ok=True)
        durable_sentinel = durable_root / "durable-memory-sentinel.txt"
        durable_sentinel.write_text("preserve", encoding="utf-8")

        harness = Harness(registry, boundary)
        lifecycle_tab = LifecycleTab()
        global_tab = GlobalTab()
        harness._loaded_tools_by_tab_id = {
            "architecture_review": lifecycle_tab,
            "config_web_ai": global_tab,
        }
        harness._patch_common_project_root_fields(lifecycle_tab)
        harness._refresh_active_project_controls()

        completed, reason = harness._perform_project_eject()
        require(not completed, "unsettled Project work did not block eject")
        require("focused operation" in reason, "eject block reason was lost")
        require(lifecycle_tab.cancel_requests == 1, "settlement was not requested")
        require(registry.resolve_current_boundary() is not None, "authority cleared early")
        print("COOPERATIVE_SETTLEMENT_REQUEST: PASS")
        print("UNSETTLED_EJECT_REJECTED: PASS")

        lifecycle_tab.active = False
        prior_ticket = harness._project_switch_ticket
        completed, reason = harness._perform_project_eject()
        require(completed and not reason, "settled Project eject failed")
        require(registry.resolve_current_boundary() is None, "registry authority survived eject")
        require(harness.current_project_root is None, "shell Project root survived eject")
        require(harness._project_switch_ticket == prior_ticket + 1, "eject selection ticket mismatch")
        require(not lifecycle_tab.isEnabled(), "Project tab remained enabled after eject")
        require(global_tab.isEnabled(), "global configuration tab was disabled")
        require(not lifecycle_tab.project_root_edit.text(), "Project root field survived eject")
        require(durable_sentinel.read_text(encoding="utf-8") == "preserve", "durable memory changed")
        print("REGISTRY_AUTHORITY_CLEARED: PASS")
        print("PROJECT_SCOPED_WIDGETS_DISABLED_AFTER_EJECT: PASS")
        print("GLOBAL_CONFIGURATION_PRESERVED_AFTER_EJECT: PASS")
        print("DURABLE_PROJECT_MEMORY_PRESERVED: PASS")

        require(
            harness._propagate_project_root(project_b, explicit_selection=True),
            "new Project selection failed after eject",
        )
        require(lifecycle_tab.isEnabled(), "Project tab did not re-enable")
        require(lifecycle_tab.project_root_edit.text() == str(project_b), "new root not applied")
        require(
            registry.resolve_current_boundary().active_project_root == project_b,
            "registry did not bind the new Project",
        )
        print("NEW_SELECTION_REENABLES_PROJECT_SCOPE: PASS")

        web_tab = WebTab()
        block = project_eject_block("project_web_ai", web_tab)
        require(block is not None, "active Web AI worker did not block eject")
        block = request_project_scope_settlement("project_web_ai", web_tab)
        require(web_tab.stop_count == 1, "Web AI public stop facade was not called")
        require(block is not None, "Web AI eject proceeded before settlement")
        web_tab._project_session.waiting_for_worker = False
        web_tab._chat_thread = None
        require(
            project_eject_block("project_web_ai", web_tab) is None,
            "settled Web AI worker still blocked eject",
        )
        print("STALE_WEB_AI_WORKER_BLOCKS_EJECT: PASS")
        print("PUBLIC_WEB_AI_CANCELLATION_FACADE_USED: PASS")

    app.processEvents()
    print("REAL_QT_SAFE_EJECT: PASS")


def main() -> int:
    """Run focused static and real-Qt validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    project_root = Path(args.project_root).expanduser().resolve()
    validate_static(project_root)
    validate_architecture(project_root)
    validate_real_qt(project_root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
