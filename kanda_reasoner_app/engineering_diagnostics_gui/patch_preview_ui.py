# project-path: kanda_reasoner_app/engineering_diagnostics_gui/patch_preview_ui.py
"""Qt binding for reviewed Wave 2U governed Patch Preview creation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from kanda_reasoner_app.engineering_diagnostics_patch_preview import (
    create_governed_patch_preview,
    patch_preview_approval_token,
    render_governed_patch_preview,
)

__all__ = ["bind_patch_preview_action", "create_patch_preview_button"]


def create_patch_preview_button(toolbar, push_button_type):
    """Create the separate governed Patch Preview entry control."""
    button = push_button_type("Create Patch Preview")
    button.setObjectName("engineeringDiagnosticsPatchPreviewButton")
    button.setToolTip(
        "Create a non-installable exact diff and rollback bundle from one "
        "reviewed safe mechanical remediation intent."
    )
    button.setEnabled(False)
    toolbar.addWidget(button)
    return button


@dataclass(slots=True)
class _PatchPreviewBinding:
    button: object
    table: object
    model: object
    busy: bool = False

    def selected_view(self):
        """Return the selected immutable finding view when available."""
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            return None
        return self.model.row_view(rows[0].row())

    def refresh_enabled(self) -> None:
        """Enable only for a reviewed, ready, safe, unfrozen intent."""
        view = self.selected_view()
        intent = view.remediation_intent if view is not None else None
        eligible = bool(
            view is not None
            and intent is not None
            and view.decision_state == "PATCH_PREPARED"
            and view.owner_status == "READY"
            and view.frozen_status == "UNFROZEN"
            and intent.action_class == "SAFE_MECHANICAL_FIX_AVAILABLE"
            and intent.mechanical_safety == "SAFE_MECHANICAL"
            and len(intent.expected_affected_files) == 1
        )
        self.button.setEnabled(not self.busy and eligible)

    def set_enabled(self, enabled: bool) -> None:
        """Combine parent busy state with deterministic eligibility."""
        self.busy = not bool(enabled)
        self.refresh_enabled()


def bind_patch_preview_action(
    *,
    panel,
    button,
    table,
    model,
    detail,
    status_label,
    controller,
    current_project_root: Callable[[], str],
    current_run_id: Callable[[], str],
    input_dialog,
    message_box,
):
    """Bind a human-confirmed proposal action without any source apply lane."""
    binding = _PatchPreviewBinding(button, table, model)

    def create_preview() -> None:
        view = binding.selected_view()
        if view is None or view.remediation_intent is None:
            status_label.setText("Select one eligible remediation intent first.")
            return
        token = patch_preview_approval_token(view.record.issue_fingerprint)
        approved = message_box.question(
            panel,
            "Create governed Patch Preview",
            "Create an isolated, non-installable proposal for the selected issue? "
            "Project source will not be modified.",
            message_box.Yes | message_box.No,
            message_box.No,
        )
        if approved != message_box.Yes:
            return
        typed, accepted = input_dialog.getText(
            panel,
            "Exact Patch Preview confirmation",
            "Type the exact token:\n" + token,
        )
        if not accepted:
            return
        run_id = current_run_id()
        try:
            run_view = controller.load_run_view(current_project_root(), run_id)
            record = create_governed_patch_preview(
                current_project_root(),
                run_view.run,
                view.record,
                view.remediation_intent,
                decision_state=view.decision_state,
                owner_status=view.owner_status,
                approval_token=str(typed),
            )
        except Exception as exc:  # noqa: BLE001
            status_label.setText("Patch Preview blocked: " + str(exc))
            return
        detail.setPlainText(render_governed_patch_preview(record))
        status_label.setText(
            "Patch Preview ready for governed validation: " + record.preview_id
        )

    button.clicked.connect(create_preview)
    table.selectionModel().selectionChanged.connect(
        lambda _selected, _deselected: binding.refresh_enabled()
    )
    binding.refresh_enabled()
    panel.engineering_diagnostics_patch_preview_button = button
    panel.refresh_engineering_diagnostics_patch_preview = binding.refresh_enabled
    return binding
