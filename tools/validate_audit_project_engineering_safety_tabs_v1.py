# project-path: tools/validate_audit_project_engineering_safety_tabs_v1.py
"""Validate nested Engineering Safety tabs and Full Audit behavior."""

from __future__ import annotations

import argparse
import builtins
import importlib
import py_compile
import symtable
import sys
from pathlib import Path

__all__: list[str] = []

FEATURE_ID = "audit-project-engineering-safety-full-pontual-audit-v1r6"
MAX_PHYSICAL_LINES = 500
PANEL_REL = Path("reasoner_tools_gui_engineering_safety_panel.py")
FULL_AUDIT_REL = Path("_reasoner_tools_gui_engineering_safety_full_audit.py")
SONAR_REL = Path("_reasoner_tools_gui_engineering_safety_sonar.py")
CATALOG_REL = Path("_reasoner_tools_gui_engineering_safety_panel_catalog.py")
SUBTABS_REL = Path(
    "kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py"
)
TOOL_SPECS_REL = Path(
    "kanda_reasoner_app/reasoner_tools_gui_shell/tool_specs.py"
)
BRAIN_MAPPING_REL = Path(
    "kanda_reasoner_app/reasoner_tools_gui_shell/brain_region_mapping/"
    "_mapping_data.py"
)
HELP_SOURCE_REL = Path(
    "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/source/"
    "engineering_safety.md"
)
HELP_RENDERED_REL = Path(
    "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/rendered/"
    "engineering_safety.html"
)
HELP_JSON_REL = Path(
    "kanda_reasoner_app/reasoner_tools_gui_help/engineering_safety.json"
)


def _require(condition: bool, message: str) -> None:
    """Raise an assertion when a validation condition is false."""
    if not condition:
        raise AssertionError(message)


def _read(root: Path, relative: Path) -> str:
    """Read one current project source as strict UTF-8."""
    path = root / relative
    _require(path.is_file(), "Missing expected source: " + str(relative))
    return path.read_text(encoding="utf-8", errors="strict")


def _validate_static_contract(root: Path) -> None:
    """Validate hierarchy, cancellation, sonar, root ownership, and limits."""
    expected = {
        PANEL_REL: (
            "project_root_provider: Callable[[], object] | None = None",
            "panel.engineering_safety_project_root_provider = project_root_provider",
            "Return the project root selected by the shared Audit Project header.",
            "_install_complete_engineering_review",
            "get_engineering_safety_panel_catalog",
            "run_engineering_safety_panel_command",
            'audit_tabs.addTab(pontual_audit_page, "Pontual Audit")',
        ),
        FULL_AUDIT_REL: (
            'audit_tabs.insertTab(0, full_page, "Full Audit")',
            'QPushButton("Complete Enginneering Review")',
            'QPushButton("Cancel Review")',
            "create_engineering_safety_sonar",
            "cancel_event = Event()",
            "cancel_event.is_set",
            "Cancellation is cooperative",
            'f"Cancelled: {\'YES\' if cancelled else \'NO\'}"',
        ),
        SONAR_REL: (
            "def create_engineering_safety_sonar",
            "GreenSonarActivityMonitor",
            'title="Engineering Safety Full Audit"',
            'setObjectName("engineeringSafetyFullAuditSonarMonitor")',
            "def start(self) -> None:",
            "def stop(self) -> None:",
            "self._monitor.start(",
            "self._monitor.set_idle()",
            "Engineering review running",
        ),
        SUBTABS_REL: (
            '_AUDIT_PROJECT_ENGINEERING_SAFETY_TAB_LABEL = "Engineering Safety"',
            '"reasoner_tools_gui_engineering_safety_panel"',
            '"create_engineering_safety_panel"',
            "project_root_provider=lambda: window._root_path_edit.text().strip()",
        ),
    }
    for relative, fragments in expected.items():
        text = _read(root, relative)
        compile(text, str(root / relative), "exec")
        for fragment in fragments:
            _require(
                fragment in text,
                str(relative) + " missing contract fragment: " + fragment,
            )
        _require(
            len(text.splitlines()) <= MAX_PHYSICAL_LINES,
            str(relative) + " exceeds 500 physical lines.",
        )

    panel_text = _read(root, PANEL_REL)
    forbidden_panel_fragments = (
        'QLabel("Project Root:")',
        'QLineEdit(str(resolve_active_project_root()))',
        'QPushButton("Browse...")',
        "engineering_safety_project_root_edit",
        "move_project_root_controls_to_layout",
        "QFileDialog.getExistingDirectory",
    )
    for fragment in forbidden_panel_fragments:
        _require(
            fragment not in panel_text,
            "Duplicate Engineering Safety root control remains: " + fragment,
        )

    sonar_text = _read(root, SONAR_REL)
    for forbidden in (
        "QPainter",
        "QPen",
        "QRadialGradient",
        "QTimer",
        "paintEvent",
        "drawEllipse",
        "drawLine",
    ):
        _require(
            forbidden not in sonar_text,
            "Engineering Safety still owns duplicate radar drawing code: "
            + forbidden,
        )
    full_audit_text = _read(root, FULL_AUDIT_REL)
    _require(
        "layout.addWidget(sonar)" not in full_audit_text,
        "Canonical floating sonar was incorrectly inserted into the page layout.",
    )
    _require(
        "monitor.widget().setObjectName" not in sonar_text,
        "Engineering Safety overrides the canonical sonar panel object name.",
    )
    _require(
        "cancel_event.set()\n        sonar.stop()" in full_audit_text,
        "Cancel Review does not stop sonar immediately.",
    )
    print("ENGINEERING_SAFETY_CANONICAL_GREEN_SONAR_TEMPLATE: PASS")
    print("ENGINEERING_SAFETY_CANONICAL_SONAR_BACKGROUND_CONTRACT: PASS")
    print("ENGINEERING_SAFETY_CANCEL_STOPS_SONAR_IMMEDIATELY_CONTRACT: PASS")

    tool_specs = _read(root, TOOL_SPECS_REL)
    _require(
        'step_title="Engineering Safety"' not in tool_specs,
        "Engineering Safety remains a top-level shell ToolSpec.",
    )
    mapping = _read(root, BRAIN_MAPPING_REL)
    brainstem_start = mapping.find('"region_id": "brainstem_midbrain"')
    brainstem_end = mapping.find("    },", brainstem_start)
    brainstem = mapping[brainstem_start:brainstem_end]
    _require(brainstem_start >= 0, "Brainstem mapping was not found.")
    _require(
        '"target_tab_id": "architecture_review"' in brainstem,
        "Brainstem mapping still targets the removed top-level tab.",
    )
    help_source = _read(root, HELP_SOURCE_REL)
    help_rendered = _read(root, HELP_RENDERED_REL)
    help_json = _read(root, HELP_JSON_REL)
    help_fragments = (
        "Cancel Review",
        "cooperative cancellation",
        "immediately",
        "gradient background",
        "sonar",
        "shared Audit Project header",
    )
    for fragment in help_fragments:
        _require(fragment in help_source, "Help source missing: " + fragment)
        _require(fragment in help_rendered, "Rendered help missing: " + fragment)
    _require(
        "does not create a second Project Root field" in help_source,
        "Help source does not explain duplicate root removal.",
    )
    _require(
        "does not duplicate the Project Root field" in help_rendered,
        "Rendered help does not explain duplicate root removal.",
    )
    for fragment in ("Cancel Review", "sonar", "single Project Root selector"):
        _require(fragment in help_json, "Help JSON missing: " + fragment)

    print("ENGINEERING_SAFETY_DUPLICATE_ROOT_CONTROLS_REMOVED: PASS")
    print("SHARED_PROJECT_ROOT_PROVIDER_CONTRACT: PASS")
    print("ENGINEERING_SAFETY_SONAR_STATIC_CONTRACT: PASS")
    print("ENGINEERING_SAFETY_HELP_ALIGNMENT: PASS")


def _validate_panel_name_bindings(root: Path) -> None:
    """Reject unresolved global names in the public panel factory."""
    text = _read(root, PANEL_REL)
    table = symtable.symtable(text, str(root / PANEL_REL), "exec")
    module_names = set(table.get_identifiers())
    builtin_names = set(dir(builtins))
    target = next(
        (
            child
            for child in table.get_children()
            if child.get_name() == "create_engineering_safety_panel"
        ),
        None,
    )
    _require(target is not None, "Public panel factory was not found.")

    unresolved: set[str] = set()
    pending = [target]
    while pending:
        scope = pending.pop()
        pending.extend(scope.get_children())
        for symbol in scope.get_symbols():
            if not symbol.is_referenced() or not symbol.is_global():
                continue
            if symbol.get_name() in module_names or symbol.get_name() in builtin_names:
                continue
            unresolved.add(symbol.get_name())

    _require(
        not unresolved,
        "Public panel factory has unresolved name bindings: "
        + ", ".join(sorted(unresolved)),
    )
    _require(
        "puntual_audit_page" not in text and "puntual_audit_layout" not in text,
        "Legacy inconsistent puntual variable spelling remains.",
    )
    print("ENGINEERING_SAFETY_PANEL_NAME_BINDINGS: PASS")


def _validate_complete_audit_runtime(root: Path) -> None:
    """Prove normal and cancelled review result semantics."""
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    panel = importlib.import_module("reasoner_tools_gui_engineering_safety_panel")
    full_audit = importlib.import_module(
        "_reasoner_tools_gui_engineering_safety_full_audit"
    )
    catalog = panel.get_engineering_safety_panel_catalog()
    calls: list[str] = []

    class Result:
        def __init__(self, command_name: str) -> None:
            self.status_code = 1 if command_name == "crash-triage" else 0
            self.stdout = "result for " + command_name
            self.stderr = "controlled failure" if self.status_code else ""

    def runner(command_name: str, project_root: str) -> object:
        _require(project_root == str(root), "Full audit changed project identity.")
        calls.append(command_name)
        return Result(command_name)

    report = full_audit.run_complete_engineering_review(
        catalog,
        str(root),
        runner,
    )
    expected_calls = [
        item.command_name
        for item in catalog
        if item.command_name != "ruff-correction-dialog"
    ]
    _require(calls == expected_calls, "Complete audit changed catalog order.")
    for item in catalog:
        _require(item.label in report, "Report omitted catalog item: " + item.label)
    _require(
        "Outcome: MANUAL REVIEW REQUIRED" in report,
        "Interactive Ruff correction safety disposition is missing.",
    )
    _require(
        "Engineering Safety - Crash Triage" in report
        and "Outcome: FAIL" in report,
        "Controlled failure result was not retained.",
    )
    _require("Cancelled: NO" in report, "Normal review was misclassified.")
    _require(
        report.rstrip().endswith("Total catalog items: " + str(len(catalog))),
        "Complete audit summary is missing or truncated.",
    )

    cancel_state = {"requested": False}
    cancel_calls: list[str] = []

    def cancelling_runner(command_name: str, project_root: str) -> object:
        _require(project_root == str(root), "Cancelled audit changed project identity.")
        cancel_calls.append(command_name)
        cancel_state["requested"] = True
        return Result(command_name)

    cancelled_report = full_audit.run_complete_engineering_review(
        catalog,
        str(root),
        cancelling_runner,
        lambda: cancel_state["requested"],
    )
    _require(cancel_calls == [catalog[0].command_name], "Cancellation ran extra items.")
    _require("Overall: CANCELLED" in cancelled_report, "Cancellation status missing.")
    _require("Cancelled: YES" in cancelled_report, "Cancellation summary missing.")
    _require("Stopped before item 02/" in cancelled_report, "Stop boundary missing.")
    _require(
        "The active command, if any, was allowed to settle safely."
        in cancelled_report,
        "Cooperative settlement message is missing.",
    )

    exception_calls: list[str] = []

    def exception_runner(command_name: str, project_root: str) -> object:
        _require(project_root == str(root), "Exception audit changed project identity.")
        exception_calls.append(command_name)
        if len(exception_calls) == 1:
            raise RuntimeError("controlled command boundary failure")
        return Result(command_name)

    exception_report = full_audit.run_complete_engineering_review(
        catalog,
        str(root),
        exception_runner,
    )
    _require(
        exception_calls == expected_calls,
        "Explicit command exception stopped later catalog items.",
    )
    _require(
        "RuntimeError: controlled command boundary failure" in exception_report,
        "Command exception was not surfaced in the complete audit report.",
    )
    _require(
        "Outcome: FAIL" in exception_report
        and "Status: 1" in exception_report
        and "Overall: ATTENTION REQUIRED" in exception_report,
        "Command exception did not produce an explicit typed failure outcome.",
    )

    print("FULL_AUDIT_CATALOG_ORDER: PASS")
    print("FULL_AUDIT_CONTINUES_AFTER_FAILURE: PASS")
    print("FULL_AUDIT_EXCEPTION_BOUNDARY_RESULT: PASS")
    print("FULL_AUDIT_INTERACTIVE_ACTION_NOT_AUTO_APPLIED: PASS")
    print("FULL_AUDIT_DISCRIMINATED_LOG: PASS")
    print("FULL_AUDIT_CANCEL_BETWEEN_ITEMS: PASS")
    print("FULL_AUDIT_CANCELLED_SUMMARY: PASS")


def validate(project_root: Path) -> None:
    """Run focused Engineering Safety nested-tab validation."""
    root = project_root.expanduser().resolve()
    _require(root.is_dir(), "Project root is not a directory: " + str(root))
    for relative in (
        PANEL_REL,
        FULL_AUDIT_REL,
        SONAR_REL,
        CATALOG_REL,
        SUBTABS_REL,
        TOOL_SPECS_REL,
        BRAIN_MAPPING_REL,
    ):
        py_compile.compile(str(root / relative), doraise=True)
    _validate_static_contract(root)
    _validate_panel_name_bindings(root)
    _validate_complete_audit_runtime(root)
    print("ENGINEERING_SAFETY_TOP_LEVEL_REMOVED: PASS")
    print("AUDIT_PROJECT_ENGINEERING_SAFETY_SIBLING: PASS")
    print("ENGINEERING_SAFETY_FULL_PONTUAL_ORDER: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()
    try:
        validate(Path(args.project_root))
    except Exception as exc:
        print("VALIDATION FAIL: " + FEATURE_ID + " - " + str(exc))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
