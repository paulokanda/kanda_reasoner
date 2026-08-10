# project-path: kanda_reasoner_app/engineering_diagnostics_gui/grouping_ui.py
"""Human-confirmed manual grouping controls without import-time Qt coupling."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping

from .models import DiagnosticFindingView

__all__ = [
    "GroupingActionBinding",
    "bind_grouping_actions",
    "create_group_filter",
    "create_grouping_buttons",
]


@dataclass(slots=True)
class GroupingActionBinding:
    """Bound manual grouping controls for one Engineering Diagnostics panel."""

    buttons: tuple[object, ...]

    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable every manual grouping action."""
        for button in self.buttons:
            button.setEnabled(bool(enabled))


def create_grouping_buttons(toolbar, button_type) -> Mapping[str, object]:
    """Create compact manual grouping action buttons."""
    buttons = {
        "create": button_type("New Group"),
        "move": button_type("Move to Group"),
        "ungroup": button_type("Ungroup"),
        "review": button_type("Mark Group Reviewed"),
    }
    for button in buttons.values():
        toolbar.addWidget(button)
    return buttons


def create_group_filter(selection_row, combo_type, label_type):
    """Create the transient grouping filter."""
    combo = combo_type()
    combo.addItems(("all", "manual", "deterministic", "ungrouped"))
    selection_row.addWidget(label_type("Group"))
    selection_row.addWidget(combo)
    return combo


def _prompt_text(input_dialog, panel, title: str, label: str) -> str | None:
    value, accepted = input_dialog.getText(panel, title, label)
    text = str(value or "").strip()
    return text if accepted and text else None


def _audit_fields(input_dialog, panel, action: str) -> tuple[str, str] | None:
    author = _prompt_text(
        input_dialog,
        panel,
        action,
        "Author for the persistent decision history:",
    )
    if author is None:
        return None
    reason = _prompt_text(
        input_dialog,
        panel,
        action,
        "Reason for this manual grouping decision:",
    )
    if reason is None:
        return None
    return author, reason


def bind_grouping_actions(
    *,
    panel,
    controller,
    buttons: Mapping[str, object],
    input_dialog,
    message_box,
    current_project_root: Callable[[], str],
    current_run_id: Callable[[], str],
    table,
    model,
    render_run: Callable[[str], None],
    show_error: Callable[[str, BaseException], None],
    status_label,
) -> GroupingActionBinding:
    """Bind explicit human grouping actions to the sole store mutation owner."""

    def selected_view() -> DiagnosticFindingView | None:
        indexes = table.selectionModel().selectedRows()
        return model.row_view(indexes[0].row()) if indexes else None

    def current_run_view():
        run_id = current_run_id()
        if not run_id:
            status_label.setText("Select a completed run first.")
            return None
        return controller.load_run_view(current_project_root(), run_id)

    def create_group() -> None:
        run_view = current_run_view()
        if run_view is None:
            return
        label = _prompt_text(
            input_dialog,
            panel,
            "Create diagnostic group",
            "Manual diagnostic group label:",
        )
        if label is None:
            return
        audit = _audit_fields(input_dialog, panel, "Create diagnostic group")
        if audit is None:
            return
        author, reason = audit
        try:
            controller.create_manual_group(
                current_project_root(),
                run_view.run.run_id,
                label=label,
                author=author,
                reason=reason,
                expected_generation=run_view.grouping_generation,
            )
        except Exception as exc:  # noqa: BLE001
            show_error("Manual group creation failed", exc)
            return
        status_label.setText("Manual diagnostic group created.")
        render_run(run_view.run.run_id)

    def move_to_group() -> None:
        selected = selected_view()
        run_view = current_run_view()
        if selected is None or run_view is None:
            status_label.setText("Select a finding and completed run first.")
            return
        manual_groups = tuple(
            group for group in run_view.groups if group.kind == "MANUAL"
        )
        if not manual_groups:
            status_label.setText("Create a manual group first.")
            return
        labels = tuple(group.label + " | " + group.group_id[:12] for group in manual_groups)
        choice, accepted = input_dialog.getItem(
            panel,
            "Move finding to group",
            "Manual diagnostic group:",
            labels,
            0,
            False,
        )
        if not accepted:
            return
        index = labels.index(str(choice))
        audit = _audit_fields(input_dialog, panel, "Move finding to group")
        if audit is None:
            return
        author, reason = audit
        try:
            controller.assign_issue_to_manual_group(
                current_project_root(),
                run_view.run.run_id,
                selected.record.issue_fingerprint,
                manual_groups[index].group_id,
                author=author,
                reason=reason,
                expected_generation=run_view.grouping_generation,
            )
        except Exception as exc:  # noqa: BLE001
            show_error("Manual grouping failed", exc)
            return
        status_label.setText("Finding moved to manual diagnostic group.")
        render_run(run_view.run.run_id)

    def ungroup() -> None:
        selected = selected_view()
        run_view = current_run_view()
        if selected is None or run_view is None or selected.manual_group is None:
            status_label.setText("Select a finding with a manual group assignment.")
            return
        confirmation = message_box.question(
            panel,
            "Ungroup finding",
            "Remove the selected manual group assignment?",
            message_box.Yes | message_box.No,
            message_box.No,
        )
        if confirmation != message_box.Yes:
            return
        audit = _audit_fields(input_dialog, panel, "Ungroup finding")
        if audit is None:
            return
        author, reason = audit
        try:
            controller.ungroup_manual_issue(
                current_project_root(),
                run_view.run.run_id,
                selected.record.issue_fingerprint,
                author=author,
                reason=reason,
                expected_generation=run_view.grouping_generation,
            )
        except Exception as exc:  # noqa: BLE001
            show_error("Ungrouping failed", exc)
            return
        status_label.setText("Manual group assignment removed; history retained.")
        render_run(run_view.run.run_id)

    def mark_reviewed() -> None:
        selected = selected_view()
        run_view = current_run_view()
        if selected is None or run_view is None or selected.manual_group is None:
            status_label.setText("Select a finding assigned to a manual group.")
            return
        audit = _audit_fields(input_dialog, panel, "Mark diagnostic group reviewed")
        if audit is None:
            return
        author, reason = audit
        try:
            controller.mark_manual_group_reviewed(
                current_project_root(),
                run_view.run.run_id,
                selected.manual_group.group_id,
                author=author,
                reason=reason,
                expected_generation=run_view.grouping_generation,
            )
        except Exception as exc:  # noqa: BLE001
            show_error("Group review update failed", exc)
            return
        status_label.setText("Manual diagnostic group marked reviewed.")
        render_run(run_view.run.run_id)

    buttons["create"].clicked.connect(create_group)
    buttons["move"].clicked.connect(move_to_group)
    buttons["ungroup"].clicked.connect(ungroup)
    buttons["review"].clicked.connect(mark_reviewed)
    return GroupingActionBinding(tuple(buttons.values()))
