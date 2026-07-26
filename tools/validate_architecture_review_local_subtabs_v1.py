# project-path: tools/validate_architecture_review_local_subtabs_v1.py
"""Validate the Audit Project and Architecture Review tab hierarchy."""
from __future__ import annotations

__all__: list[str] = []

import ast
import json
import py_compile
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAX_CODE_LINES = 500

MAIN_GUI_REL = (
    "kanda_reasoner_app/manage_architecture/manage_architecture_gui.py"
)
TOOL_SPECS_REL = (
    "kanda_reasoner_app/reasoner_tools_gui_shell/tool_specs.py"
)
SUBTABS_REL = (
    "kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py"
)
MODE_UI_REL = (
    "kanda_reasoner_app/manage_architecture/architecture_review_mode_ui.py"
)
AUDIT_ACTIONS_REL = (
    "kanda_reasoner_app/manage_architecture/architecture_audit_actions_gui.py"
)
SPLIT_AUDIT_REL = (
    "kanda_reasoner_app/manage_architecture/large_module_split_audit_gui.py"
)
HELP_CATALOG_REL = (
    "kanda_reasoner_app/reasoner_tools_gui_help/tab1_architecture.json"
)
HELP_SOURCE_REL = (
    "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/source/"
    "architecture_review.md"
)
HELP_RENDERED_REL = (
    "kanda_reasoner_app/reasoner_tools_gui_shell/help_docs/rendered/"
    "architecture_review.html"
)
TOUCHED_SOURCE_FILES = [
    MAIN_GUI_REL,
    TOOL_SPECS_REL,
    SUBTABS_REL,
    MODE_UI_REL,
    AUDIT_ACTIONS_REL,
    SPLIT_AUDIT_REL,
]

REQUIRED_SUBTAB_FRAGMENTS = [
    "_audit_project_subtab_widget",
    "audit_project_subtab_widget",
    "_architecture_review_page",
    "_architecture_review_subtab_stack",
    "architecture_review_child_tab_widget",
    "_AUDIT_PROJECT_ARCHITECTURE_TAB_LABEL",
    "_AUDIT_PROJECT_ENGINEERING_SAFETY_TAB_LABEL",
    "_AUDIT_PROJECT_WORKFLOW_REVIEW_TAB_LABEL",
    "_engineering_safety_page",
    "_workflow_review_page",
    "create_embedded_workflow_review",
    "create_engineering_safety_panel",
    "_ARCHITECTURE_REVIEW_CHILD_TAB_LABELS",
    '"Architecture Review"',
    '"Engineering Safety"',
    '"Workflow Review"',
    '"Check Update Architecture"',
    '"Large Module AST Split Audit"',
    '"Large File Refactor Planner"',
    '"Large File Refactor WorkBench"',
    "QTabWidget",
    "currentChanged.connect",
    "Validate Project",
    "bind_mode_action_button",
]

FORBIDDEN_LEGACY_SUBTAB_FRAGMENTS = [
    "_architecture_review_general_ear",
    "_architecture_review_split_ear",
    "_ACTIVE_EAR_STYLE",
    "_INACTIVE_EAR_STYLE",
    '"Check & Update Architecture"',
]

REQUIRED_MODE_LABEL_FRAGMENTS = [
    '"validate": "Validate Project"',
    '"diff": "Preview Changes"',
    '"scan": "Scan Project"',
    '"write": "Write Architecture Files"',
]

REQUIRED_SPLIT_OUTPUT_FRAGMENTS = [
    "_large_module_split_output.clear()",
    "_large_module_split_output.appendPlainText(result.markdown)",
    "_last_large_module_split_handoff",
]


def _read_project_text(relative_path: str) -> str:
    """Read a project file as UTF-8 text."""
    path = PROJECT_ROOT / relative_path
    if not path.is_file():
        raise AssertionError(f"Missing expected file: {relative_path}")
    return path.read_text(encoding="utf-8")


def _line_count(text: str) -> int:
    """Return the physical line count for source text."""
    return len(text.splitlines())


def _validate_py_compile(relative_path: str) -> None:
    """Compile one Python source file without importing GUI dependencies."""
    py_compile.compile(str(PROJECT_ROOT / relative_path), doraise=True)


def _validate_line_counts() -> None:
    """Ensure touched code modules stay within the active size canon."""
    for relative_path in TOUCHED_SOURCE_FILES:
        count = _line_count(_read_project_text(relative_path))
        if count > MAX_CODE_LINES:
            raise AssertionError(
                f"{relative_path} has {count} lines; "
                f"maximum is {MAX_CODE_LINES}"
            )


def _validate_main_facade() -> None:
    """Ensure the main GUI module remains a facade over helper modules."""
    text = _read_project_text(MAIN_GUI_REL)
    for fragment in [
        "ArchitectureAuditActionsMixin",
        "LargeModuleSplitAuditGuiMixin",
        "build_architecture_review_ui(self, install_tab1_ai_review_controls)",
        "ArchitectureManagerWindow",
    ]:
        if fragment not in text:
            raise AssertionError(f"Main GUI missing fragment: {fragment}")

    tree = ast.parse(text)
    class_names = [
        node.name
        for node in tree.body
        if isinstance(node, ast.ClassDef)
    ]
    if "ArchitectureManagerWindow" not in class_names:
        raise AssertionError("ArchitectureManagerWindow class was not found")


def _validate_shell_title_contract() -> None:
    """Require the new visible title while preserving the stable tab ID."""
    text = _read_project_text(TOOL_SPECS_REL)
    architecture_spec_start = text.find('step_title="Audit Project"')
    if architecture_spec_start == -1:
        raise AssertionError("Audit Project ToolSpec title is missing")
    architecture_spec_end = text.find("    ToolSpec(", architecture_spec_start + 1)
    architecture_spec = text[architecture_spec_start:architecture_spec_end]
    if 'tab_id="architecture_review"' not in architecture_spec:
        raise AssertionError("Stable architecture_review tab ID changed")
    if 'step_title="Architecture Review"' in architecture_spec:
        raise AssertionError("Legacy top-level Architecture Review title remains")
    if 'step_title="Engineering Safety"' in text:
        raise AssertionError("Engineering Safety remains a top-level shell tab")
    workflow_start = text.find('step_title="Workflow Review"')
    workflow_end = text.find("    ToolSpec(", workflow_start + 1)
    workflow_spec = text[workflow_start:workflow_end]
    if 'visible_in_shell=False' not in workflow_spec:
        raise AssertionError("Workflow Review remains a top-level shell tab")


def _validate_subtab_layout_contract() -> None:
    """Ensure the requested three-level tab hierarchy is present."""
    text = _read_project_text(SUBTABS_REL)
    for fragment in REQUIRED_SUBTAB_FRAGMENTS:
        if fragment not in text:
            raise AssertionError(f"Subtab layout missing fragment: {fragment}")
    for fragment in FORBIDDEN_LEGACY_SUBTAB_FRAGMENTS:
        if fragment in text:
            raise AssertionError(
                f"Legacy subtab implementation remains: {fragment}"
            )
    if "architecture_review_local_title_label" in text:
        raise AssertionError(
            "Duplicate local Architecture Review title label remains"
        )
    if 'QLabel("Architecture Review")' in text:
        raise AssertionError(
            "Duplicate local Architecture Review label remains"
        )


def _validate_mode_label_contract() -> None:
    """Ensure every technical mode has one beginner-facing action label."""
    text = _read_project_text(MODE_UI_REL)
    for fragment in REQUIRED_MODE_LABEL_FRAGMENTS:
        if fragment not in text:
            raise AssertionError(
                f"Mode action label mapping missing fragment: {fragment}"
            )


def _validate_help_hierarchy_contract() -> None:
    """Keep fallback and rich help aligned with the nested visible labels."""
    catalog = json.loads(_read_project_text(HELP_CATALOG_REL))
    if catalog.get("tab") != "Audit Project > Architecture Review":
        raise AssertionError("Fallback help tab identity is stale")

    source = _read_project_text(HELP_SOURCE_REL)
    rendered = _read_project_text(HELP_RENDERED_REL)
    for fragment in (
        "Audit Project",
        "Architecture Review",
        "Check Update Architecture",
        "Engineering Safety",
        "Workflow Review",
    ):
        if fragment not in source:
            raise AssertionError(
                f"Rich help source missing hierarchy fragment: {fragment}"
            )
        if fragment not in rendered:
            raise AssertionError(
                f"Rendered help missing hierarchy fragment: {fragment}"
            )


def _validate_project_output_created_before_clear_binding() -> None:
    """Ensure Clear Audit Results is connected after _output exists."""
    text = _read_project_text(SUBTABS_REL)
    create_index = text.find("window._output = QPlainTextEdit()")
    clear_index = text.find(
        "clear_button.clicked.connect(window._output.clear)"
    )
    if create_index == -1:
        raise AssertionError(
            "Project Audit Results output widget is not created"
        )
    if clear_index == -1:
        raise AssertionError("Clear Audit Results binding was not found")
    if create_index > clear_index:
        raise AssertionError(
            "Clear Audit Results is bound before window._output is created"
        )


def _validate_split_audit_output_isolated() -> None:
    """Ensure AST split audit writes only to its own output window."""
    text = _read_project_text(SPLIT_AUDIT_REL)
    for fragment in REQUIRED_SPLIT_OUTPUT_FRAGMENTS:
        if fragment not in text:
            raise AssertionError(f"Split output missing fragment: {fragment}")

    function_start = text.find("def run_large_module_split_audit_from_gui")
    if function_start == -1:
        raise AssertionError(
            "run_large_module_split_audit_from_gui was not found"
        )
    function_end = text.find(
        "\n    def copy_large_module_target_path",
        function_start,
    )
    function_text = text[function_start:function_end]
    if "self._output.clear()" in function_text:
        raise AssertionError(
            "AST split audit must not clear Project Audit Results"
        )
    if "self._output.appendPlainText" in function_text:
        raise AssertionError(
            "AST split audit must not write into Project Audit Results"
        )


def main() -> int:
    """Run focused validation for Architecture Review local subtabs."""
    for relative_path in [
        *TOUCHED_SOURCE_FILES,
        "tools/validate_architecture_review_local_subtabs_v1.py",
    ]:
        _validate_py_compile(relative_path)
    _validate_line_counts()
    _validate_main_facade()
    _validate_shell_title_contract()
    _validate_subtab_layout_contract()
    _validate_mode_label_contract()
    _validate_help_hierarchy_contract()
    _validate_project_output_created_before_clear_binding()
    _validate_split_audit_output_isolated()
    print("VALIDATION OK: architecture-review-local-subtabs-v1")
    print(
        "VALIDATION OK: "
        "architecture-review-local-subtabs-v1-runtime-repair-v1"
    )
    print("VALIDATION OK: architecture-review-subtab-style-repair-v1")
    print("VALIDATION OK: architecture-review-subtab-height-compact-v1")
    print(
        "VALIDATION OK: "
        "audit-project-architecture-review-three-level-tabs-v1"
    )
    print(
        "VALIDATION OK: "
        "audit-project-architecture-review-three-level-tabs-v1r2"
    )
    print(
        "VALIDATION OK: "
        "audit-project-engineering-safety-full-pontual-audit-v1"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
