# project-path: kanda_reasoner_app/engineering_diagnostics_gui/lifecycle_ui.py
"""Human-controlled lifecycle actions for Engineering Diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping

from kanda_reasoner_app.engineering_diagnostics import DiagnosticLifecycleTarget

from .models import DiagnosticFindingView

__all__ = ["LifecycleActionBinding", "create_lifecycle_controls", "bind_lifecycle_actions"]

_ACTION_LABELS = (
    ("Confirm issue", "CONFIRM"),
    ("Suppress with reason", "SUPPRESS"),
    ("Accept risk", "ACCEPT_RISK"),
    ("Mark false positive", "MARK_FALSE_POSITIVE"),
    ("Defer to governed wave", "DEFER"),
    ("Reopen", "REOPEN"),
)


@dataclass(frozen=True, slots=True)
class LifecycleActionBinding:
    """Bound controls that can be disabled during collector activity."""

    controls: tuple[object, ...]

    def set_enabled(self, enabled: bool) -> None:
        for control in self.controls:
            control.setEnabled(bool(enabled))


def create_lifecycle_controls(layout, combo_box_type, push_button_type, label_type):
    """Create one compact action selector without importing Qt at module import."""
    action_combo = combo_box_type()
    for label, action in _ACTION_LABELS:
        action_combo.addItem(label, action)
    apply_button = push_button_type("Apply Decision")
    layout.addWidget(label_type("Lifecycle"))
    layout.addWidget(action_combo)
    layout.addWidget(apply_button)
    return {"action": action_combo, "apply": apply_button}


def _prompt(input_dialog, panel, title: str, label: str, *, required: bool) -> str | None:
    value, accepted = input_dialog.getText(panel, title, label)
    if not accepted:
        return None
    text = str(value or "").strip()
    if required and not text:
        return None
    return text


def _select_target(
    input_dialog,
    panel,
    selected: DiagnosticFindingView,
) -> DiagnosticLifecycleTarget | None:
    targets: list[tuple[str, DiagnosticLifecycleTarget]] = [
        (
            "Issue | " + selected.record.code + " | " + selected.record.issue_fingerprint[:12],
            DiagnosticLifecycleTarget(
                "ISSUE",
                selected.record.issue_fingerprint,
                selected.record.code + " | " + selected.record.relative_path,
                (selected.record.issue_fingerprint,),
            ),
        )
    ]
    for group in selected.groups:
        targets.append(
            (
                "Group | " + group.label + " | " + group.group_id[:12],
                DiagnosticLifecycleTarget(
                    "GROUP",
                    group.group_id,
                    group.label,
                    group.member_issue_fingerprints,
                ),
            )
        )
    labels = tuple(label for label, _target in targets)
    choice, accepted = input_dialog.getItem(
        panel,
        "Lifecycle decision target",
        "Apply this decision to:",
        labels,
        0,
        False,
    )
    if not accepted:
        return None
    return targets[labels.index(str(choice))][1]


def bind_lifecycle_actions(
    *,
    panel,
    controller,
    controls: Mapping[str, object],
    input_dialog,
    message_box,
    current_project_root: Callable[[], str],
    current_run_id: Callable[[], str],
    table,
    model,
    render_run: Callable[[str], None],
    show_error: Callable[[str, BaseException], None],
    status_label,
) -> LifecycleActionBinding:
    """Bind persistent decisions to the existing Store mutation owner."""

    def selected_view() -> DiagnosticFindingView | None:
        indexes = table.selectionModel().selectedRows()
        return model.row_view(indexes[0].row()) if indexes else None

    def apply_decision() -> None:
        selected = selected_view()
        run_id = current_run_id()
        if selected is None or not run_id:
            status_label.setText("Select a finding and completed run first.")
            return
        target = _select_target(input_dialog, panel, selected)
        if target is None:
            return
        action = str(controls["action"].currentData() or "").strip().upper()
        author = _prompt(
            input_dialog,
            panel,
            "Lifecycle decision",
            "Author:",
            required=True,
        )
        if author is None:
            return
        reason_code = _prompt(
            input_dialog,
            panel,
            "Lifecycle decision",
            "Reason code (UPPER_SNAKE_CASE):",
            required=True,
        )
        if reason_code is None:
            return
        rationale = _prompt(
            input_dialog,
            panel,
            "Lifecycle decision",
            "Rationale:",
            required=True,
        )
        if rationale is None:
            return
        revisit = _prompt(
            input_dialog,
            panel,
            "Lifecycle decision",
            "Revisit condition:",
            required=True,
        )
        if revisit is None:
            return
        expiration = _prompt(
            input_dialog,
            panel,
            "Lifecycle decision",
            "Expiration timestamp (optional):",
            required=False,
        )
        if expiration is None:
            return
        ticket = _prompt(
            input_dialog,
            panel,
            "Lifecycle decision",
            "Related ticket (optional):",
            required=False,
        )
        if ticket is None:
            return
        wave = _prompt(
            input_dialog,
            panel,
            "Lifecycle decision",
            "Related governed wave"
            + (" (required):" if action == "DEFER" else " (optional):"),
            required=action == "DEFER",
        )
        if wave is None:
            return
        explicit = False
        if action == "ACCEPT_RISK":
            confirmation = message_box.question(
                panel,
                "Explicit accepted-risk confirmation",
                "Accept this diagnostic risk explicitly and persist the decision?",
                message_box.Yes | message_box.No,
                message_box.No,
            )
            if confirmation != message_box.Yes:
                return
            explicit = True
        try:
            controller.record_lifecycle_decision(
                current_project_root(),
                run_id,
                target,
                action=action,
                reason_code=reason_code,
                rationale=rationale,
                author=author,
                expected_generation=selected.decision_generation
                if target.target_kind == "ISSUE"
                else selected.group_decision_generation(target.target_id),
                expires_at_utc=expiration,
                revisit_condition=revisit,
                related_ticket=ticket,
                related_wave=wave,
                explicit_confirmation=explicit,
            )
        except Exception as exc:  # noqa: BLE001
            show_error("Lifecycle decision failed", exc)
            return
        status_label.setText("Lifecycle decision persisted; findings retained.")
        render_run(run_id)

    controls["apply"].clicked.connect(apply_decision)
    return LifecycleActionBinding(tuple(controls.values()))
