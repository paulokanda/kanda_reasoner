"""Validate Workflow Review toolbar help-right layout v1."""

from __future__ import annotations

import py_compile
from pathlib import Path

FEATURE_ID = "workflow-review-toolbar-help-right-v1"
MARKER = "VALIDATION OK: " + FEATURE_ID
ROOT = Path(__file__).resolve().parents[1]

WINDOW = (
    ROOT
    / "kanda_reasoner_app/manage_workflows/manage_workflows_gui_help/workflow_gui_window.py"
)
FACADE = ROOT / "kanda_reasoner_app/manage_workflows/manage_workflows_gui.py"
LAZY_TABS = ROOT / "kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def assert_ascii(path: Path) -> None:
    data = path.read_text(encoding="utf-8")
    require(
        not any(ord(char) > 127 for char in data),
        "non-ASCII character found in " + path.as_posix(),
    )


def assert_compiles() -> None:
    for path in (WINDOW, FACADE, LAZY_TABS):
        py_compile.compile(str(path), doraise=True)
        assert_ascii(path)


def assert_normal_source_still_protected() -> None:
    window = read(WINDOW)
    facade = read(FACADE)
    require("load_payload" not in facade, "facade restored encoded payload loader")
    require("load_payload" not in window, "window restored encoded payload loader")
    require("PAYLOAD_PARTS" not in facade, "facade restored payload parts")
    require("PAYLOAD_PARTS" not in window, "window restored payload parts")
    require(
        "This is the canonical readable source for Workflow Review" in window,
        "canonical readable source note is missing",
    )


def assert_toolbar_layout() -> None:
    window = read(WINDOW)
    require('toolbar = QToolBar("Main")' in window, "Main toolbar is missing")
    require(
        '"workflow_review_mode_action_toolbar_widget"' in window,
        "mode action toolbar widget object name is missing",
    )
    require(
        '"workflow_review_run_options_toolbar_widget"' in window,
        "run options toolbar widget object name is missing",
    )
    require(
        '"workflow_review_mode_help_toolbar_button"' in window,
        "mode help toolbar button object name is missing",
    )
    require(
        "toolbar.addWidget(self._mode_action_toolbar_widget)" in window,
        "mode action cluster is not added to toolbar",
    )
    require(
        "toolbar.addWidget(self._run_options_toolbar_widget)" in window,
        "run options widget is not added to toolbar",
    )
    require(
        "toolbar.addWidget(self._mode_help_toolbar_button)" in window,
        "mode help button is not added directly to toolbar",
    )
    require(
        window.index("toolbar.addWidget(self._mode_action_toolbar_widget)")
        < window.index("toolbar.addWidget(self._run_options_toolbar_widget)")
        < window.index("toolbar.addWidget(self._mode_help_toolbar_button)"),
        "toolbar order must be actions, run options, mode help",
    )
    require(
        "run_options_toolbar_layout.addWidget(self._mode_help_toolbar_button)"
        not in window,
        "mode help button must not be inside the run options widget",
    )
    require(
        'self._run_button = QPushButton("Run Selected Mode")' in window,
        "Run Selected Mode button is missing",
    )
    require(
        "for mode in (\"validate\", \"diff\", \"scan\", \"write\")" in window,
        "validate/diff/scan/write quick buttons are not created together",
    )
    require(
        "mode_action_toolbar_layout.addWidget(btn)" in window,
        "quick mode buttons are not added to the action cluster",
    )
    require(
        "run_options_toolbar_layout.addWidget(self._strict_write_checkbox)"
        in window,
        "Require confirm before write checkbox is not in run options widget",
    )


def assert_old_body_rows_not_restored() -> None:
    window = read(WINDOW)
    require("buttons = QHBoxLayout()" not in window, "old body button row was restored")
    require("layout.addLayout(buttons)" not in window, "old body button row is still added")
    require("help_btn = QPushButton" not in window, "old body help button remains")
    require("script_form = QFormLayout()" not in window, "worker script form was restored")
    require("layout.addLayout(script_form)" not in window, "worker script form is still added")


def assert_behavior_still_connected() -> None:
    window = read(WINDOW)
    require(
        "self._run_button.clicked.connect(self.run_selected_mode)" in window,
        "Run Selected Mode no longer calls run_selected_mode",
    )
    require(
        "btn.clicked.connect(lambda _=False, m=mode: self.run_mode(m))" in window,
        "quick mode buttons no longer call run_mode with their mode",
    )
    require(
        "self._mode_help_toolbar_button.clicked.connect(self.show_mode_help)"
        in window,
        "mode help button no longer calls show_mode_help",
    )
    require(
        "if mode == \"write\" and self._strict_write_checkbox.isChecked():"
        in window,
        "write confirmation gate was changed or removed",
    )


def assert_host_row_rules_still_protected() -> None:
    window = read(WINDOW)
    lazy = read(LAZY_TABS)
    require(
        "move_project_root_controls_to_layout" in window,
        "project root host-row move hook is missing",
    )
    require(
        "Workflow Review no longer shows script controls" in window,
        "worker-script deprecation hook text is missing",
    )
    require(
        "_move_tab2_project_root_controls_to_status_row" in lazy,
        "lazy tabs no longer moves Workflow Review project root controls",
    )
    require(
        "_move_tab2_worker_script_selector_to_status_row" not in lazy,
        "lazy tabs restored Workflow Review worker script relocation",
    )


def _external_show_project_root(project_root: Path) -> Path:
    project_name = project_root.name
    if project_root.drive:
        return Path(project_root.drive + "\\") / (project_name + "_show_project_to_AI")
    return project_root.parent / (project_name + "_show_project_to_AI")


def assert_freeze_hint_staging_contract() -> None:
    hint_path = (
        _external_show_project_root(ROOT)
        / "project_freeze_after_update"
        / "freeze_hint_intake"
        / "workflow-review-toolbar-help-right-v1__KANDA_FREEZE_HINT.json"
    )
    if hint_path.exists():
        data = hint_path.read_text(encoding="utf-8")
        require(MARKER in data, "staged freeze hint is missing validation marker")
        require("STATUS: IN_SYNC" in data, "staged freeze hint is missing sync marker")


def main() -> int:
    assert_compiles()
    assert_normal_source_still_protected()
    assert_toolbar_layout()
    assert_old_body_rows_not_restored()
    assert_behavior_still_connected()
    assert_host_row_rules_still_protected()
    assert_freeze_hint_staging_contract()
    print(MARKER)
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
