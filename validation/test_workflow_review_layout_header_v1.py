from __future__ import annotations

import base64
import py_compile
import zipfile
from pathlib import Path

FEATURE_ID = "workflow-review-layout-header-v1"
ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / "kanda_reasoner_app" / "backend_payloads" / "payload_w.py"
LAZY_TABS = ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "lazy_tabs.py"
PATCH_ZIP = ROOT.parent / "kanda_workflow_review_layout_header_v1_patch.zip"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def decode_payload_w() -> str:
    namespace: dict[str, object] = {}
    exec(PAYLOAD.read_text(encoding="utf-8"), namespace)
    parts = namespace.get("PAYLOAD_PARTS_W")
    require(isinstance(parts, tuple), "PAYLOAD_PARTS_W must be a tuple")
    return "".join(base64.b64decode(part).decode("utf-8") for part in parts)


def test_payload_compiles() -> None:
    py_compile.compile(str(PAYLOAD), doraise=True)
    py_compile.compile(str(LAZY_TABS), doraise=True)
    decoded = decode_payload_w()
    temp_decoded = ROOT / "validation" / "_decoded_payload_w_check_tmp.py"
    temp_decoded.write_text(decoded, encoding="utf-8")
    try:
        py_compile.compile(str(temp_decoded), doraise=True)
    finally:
        try:
            temp_decoded.unlink()
        except OSError:
            pass


def test_workflow_project_root_moves_to_host() -> None:
    decoded = decode_payload_w()
    require(
        "self._root_path_label = QLabel(\"Project Root:\")" in decoded,
        "Workflow Review must define a Project Root host label",
    )
    require(
        "def move_project_root_controls_to_layout" in decoded,
        "Workflow Review must expose project-root host move hook",
    )
    require(
        "self._root_combo.setMaximumWidth(360)" in decoded,
        "Workflow Review project-root combo must be compact for host row",
    )
    require(
        "destination_layout.insertWidget(insert_index + 2, self._root_combo, 0)" in decoded,
        "Workflow Review project-root combo must be inserted into host row",
    )
    require(
        "form.addRow(\"Project root\"" not in decoded,
        "old Workflow Review Project root form row must not be restored",
    )


def test_workflow_run_options_are_toolbar_left() -> None:
    decoded = decode_payload_w()
    require(
        "workflow_review_run_options_toolbar_widget" in decoded,
        "Workflow Review run options toolbar widget missing",
    )
    require(
        "toolbar.addWidget(self._run_options_toolbar_widget)" in decoded,
        "Workflow Review run options must be added to Main toolbar",
    )
    require(
        decoded.index("toolbar.addWidget(self._run_options_toolbar_widget)")
        < decoded.index("run_action = QAction(\"> Run\", self)"),
        "Workflow Review run options must appear left of Run action",
    )
    require(
        "run_options_toolbar_layout.addWidget(self._mode_combo)" in decoded,
        "Mode dropdown must be in toolbar run-options widget",
    )
    require(
        "run_options_toolbar_layout.addWidget(self._strict_write_checkbox)" in decoded,
        "Require confirm checkbox must be in toolbar run-options widget",
    )
    require(
        "if mode == \"write\" and self._strict_write_checkbox.isChecked():" in decoded,
        "write confirmation gate must remain wired to checkbox",
    )


def test_worker_script_group_removed_from_host_and_body() -> None:
    decoded = decode_payload_w()
    lazy = LAZY_TABS.read_text(encoding="utf-8")
    require(
        "form.addRow(self._script_row_label" not in decoded,
        "old Workflow Review worker script form row must not be restored",
    )
    require(
        "host_label = QLabel(\"Worker Script:\")" not in decoded,
        "Workflow Review must not create host Worker Script label",
    )
    require(
        "def _move_tab2_worker_script_selector_to_status_row" not in lazy,
        "Lazy tab must not move Workflow Review worker script selector",
    )
    require(
        "_move_tab2_project_root_controls_to_status_row" in lazy,
        "Lazy tab must move Workflow Review Project Root controls instead",
    )
    require(
        "Worker script: manage_workflows.py" not in lazy,
        "Workflow Review source hover must not expose removed worker-script group text",
    )


def test_architecture_frozen_layout_preserved() -> None:
    lazy = LAZY_TABS.read_text(encoding="utf-8")
    require(
        "_move_tab1_project_root_controls_to_status_row" in lazy,
        "Architecture Review project-root host relocation must remain",
    )
    require(
        "border: 1px solid black; padding: 2px 6px;" in lazy,
        "Python executable/source header black frames must remain",
    )
    require(
        "_move_error_memory_project_root_controls_to_status_row" in lazy,
        "Error Memory project-root host relocation must remain",
    )


def test_zip_contract() -> None:
    require(PATCH_ZIP.exists(), "patch ZIP missing beside project root")
    with zipfile.ZipFile(PATCH_ZIP) as archive:
        names = set(archive.namelist())
    required = {
        "kanda_reasoner_app/backend_payloads/payload_w.py",
        "kanda_reasoner_app/reasoner_tools_gui_shell/lazy_tabs.py",
        "validation/test_workflow_review_layout_header_v1.py",
        "KANDA_FREEZE_HINT.json",
    }
    require(required.issubset(names), "patch ZIP missing required files")
    require(
        "kanda_reasoner_app/manage_architecture/manage_architecture_gui.py" not in names,
        "patch must not overwrite frozen Architecture Review source",
    )


def main() -> int:
    test_payload_compiles()
    test_workflow_project_root_moves_to_host()
    test_workflow_run_options_are_toolbar_left()
    test_worker_script_group_removed_from_host_and_body()
    test_architecture_frozen_layout_preserved()
    test_zip_contract()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
