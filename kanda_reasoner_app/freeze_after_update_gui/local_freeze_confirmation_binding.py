# project-path: kanda_reasoner_app/freeze_after_update_gui/local_freeze_confirmation_binding.py
"""Bind a human freeze confirmation to the exact reviewed form and project."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Callable, Mapping

__all__ = [
    "FreezeActionStateController",
    "apply_freeze_form_inputs",
    "bind_freeze_confirmation_invalidation",
    "build_freeze_confirmation_binding",
    "collect_freeze_form_inputs",
    "freeze_confirmation_binding_matches",
    "render_freeze_findings",
]


class FreezeActionStateController:
    """Own confirm/ignore button state for one local-freeze dialog."""

    def __init__(
        self,
        *,
        confirm_button: Any,
        ignore_button: Any,
        confirm_enabled_style: str,
        ignore_enabled_style: str,
        disabled_style: str,
    ) -> None:
        self._confirm_button = confirm_button
        self._ignore_button = ignore_button
        self._confirm_enabled_style = confirm_enabled_style
        self._ignore_enabled_style = ignore_enabled_style
        self._disabled_style = disabled_style

    def set_state(
        self,
        can_confirm: bool,
        can_ignore: bool,
        reason: str = "",
    ) -> None:
        """Project one validated state to both freeze action buttons."""

        self._confirm_button.setEnabled(can_confirm)
        self._ignore_button.setEnabled(can_ignore)
        if can_confirm:
            self._confirm_button.setStyleSheet(self._confirm_enabled_style)
            self._confirm_button.setToolTip(
                "Write this validated local freeze entry and close the form "
                "immediately."
            )
        else:
            self._confirm_button.setStyleSheet(self._disabled_style)
            self._confirm_button.setToolTip(
                reason
                or "Preview and validate a writable freeze entry before "
                "confirming."
            )
        if can_ignore:
            self._ignore_button.setStyleSheet(self._ignore_enabled_style)
            self._ignore_button.setToolTip(
                "Discard this current writable freeze draft and mark the "
                "current freeze hint as ignored/used. No freeze entry is "
                "written."
            )
        else:
            self._ignore_button.setStyleSheet(self._disabled_style)
            self._ignore_button.setToolTip(
                reason or "No current writable freeze draft is available to ignore."
            )

    def disable(self, reason: str = "") -> None:
        """Disable confirmation and ignore actions with one shared reason."""

        self.set_state(False, False, reason)


def render_freeze_findings(result: Mapping[str, Any]) -> str:
    """Render validation findings before the read-only Markdown preview."""

    lines: list[str] = []
    errors = result.get("errors") or []
    warnings = result.get("warnings") or []
    if errors:
        lines.append("ERRORS:")
        lines.extend(f"- {item}" for item in errors)
        lines.append("")
    if warnings:
        lines.append("WARNINGS:")
        lines.extend(f"- {item}" for item in warnings)
        lines.append("")
    return "\n".join(lines)


_FORM_FIELDS = (
    "feature_title",
    "primary_box",
    "box_type",
    "validated_files",
    "generated_files",
    "protected_paths",
    "do_not_regress_rules",
    "validation_evidence_summary",
    "known_warnings",
    "planned_next_step",
    "notes",
)


def _resolved_root_text(project_root: str | Path) -> str:
    """Return a stable selected-project identity for confirmation binding."""

    return str(Path(project_root).expanduser().resolve(strict=False))


def _canonical_inputs(inputs: Mapping[str, Any]) -> dict[str, str]:
    """Return exact form text under the fixed local-freeze field inventory."""

    return {field: str(inputs.get(field, "")) for field in _FORM_FIELDS}


def _inputs_digest(inputs: Mapping[str, Any]) -> str:
    """Return a deterministic digest of the exact reviewed freeze form."""

    payload = json.dumps(
        _canonical_inputs(inputs),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def build_freeze_confirmation_binding(
    project_root: str | Path,
    inputs: Mapping[str, Any],
) -> dict[str, str]:
    """Bind confirmation to one selected project and one exact form snapshot."""

    return {
        "schema_version": "1.0",
        "selected_project_root": _resolved_root_text(project_root),
        "form_sha256": _inputs_digest(inputs),
    }


def freeze_confirmation_binding_matches(
    binding: Mapping[str, Any] | None,
    project_root: str | Path,
    inputs: Mapping[str, Any],
) -> tuple[bool, str]:
    """Return whether the current project and form still match the preview."""

    if not isinstance(binding, Mapping):
        return False, "No current confirmation binding is available."
    if str(binding.get("schema_version") or "") != "1.0":
        return False, "The confirmation binding schema is invalid."
    if str(binding.get("selected_project_root") or "") != _resolved_root_text(
        project_root
    ):
        return False, "The selected project changed after Preview."
    if str(binding.get("form_sha256") or "") != _inputs_digest(inputs):
        return False, "The freeze form changed after Preview."
    return True, ""


def collect_freeze_form_inputs(widgets: Any) -> dict[str, str]:
    """Read the exact freeze form values from the dialog widgets."""

    return {
        "feature_title": widgets.feature_title_edit.text().strip(),
        "primary_box": widgets.primary_box_edit.text().strip(),
        "box_type": widgets.box_type_edit.text().strip() or "Module Box",
        "validated_files": widgets.validated_files_edit.toPlainText(),
        "generated_files": widgets.generated_files_edit.toPlainText(),
        "protected_paths": widgets.protected_paths_edit.toPlainText(),
        "do_not_regress_rules": widgets.do_not_regress_edit.toPlainText(),
        "validation_evidence_summary": (
            widgets.validation_evidence_edit.toPlainText()
        ),
        "known_warnings": widgets.known_warnings_edit.toPlainText().strip(),
        "planned_next_step": (
            widgets.planned_next_step_edit.toPlainText().strip()
        ),
        "notes": widgets.notes_edit.toPlainText().strip(),
    }


def apply_freeze_form_inputs(widgets: Any, inputs: Mapping[str, Any]) -> None:
    """Apply one input mapping to the local-freeze dialog widgets."""

    widgets.feature_title_edit.setText(str(inputs.get("feature_title", "")))
    widgets.primary_box_edit.setText(str(inputs.get("primary_box", "")))
    widgets.box_type_edit.setText(
        str(inputs.get("box_type", "Module Box") or "Module Box")
    )
    widgets.validated_files_edit.setPlainText(
        str(inputs.get("validated_files", ""))
    )
    widgets.generated_files_edit.setPlainText(
        str(inputs.get("generated_files", ""))
    )
    widgets.protected_paths_edit.setPlainText(
        str(inputs.get("protected_paths", ""))
    )
    widgets.do_not_regress_edit.setPlainText(
        str(inputs.get("do_not_regress_rules", ""))
    )
    widgets.validation_evidence_edit.setPlainText(
        str(inputs.get("validation_evidence_summary", ""))
    )
    widgets.known_warnings_edit.setPlainText(
        str(inputs.get("known_warnings", ""))
    )
    widgets.planned_next_step_edit.setPlainText(
        str(inputs.get("planned_next_step", ""))
    )
    widgets.notes_edit.setPlainText(str(inputs.get("notes", "")))


def bind_freeze_confirmation_invalidation(
    widgets: Any,
    project_root_edit: Any,
    callback: Callable[..., None],
) -> int:
    """Invalidate a confirmation whenever reviewed form or target text changes."""

    editors = (
        widgets.feature_title_edit,
        widgets.primary_box_edit,
        widgets.box_type_edit,
        widgets.validated_files_edit,
        widgets.generated_files_edit,
        widgets.protected_paths_edit,
        widgets.do_not_regress_edit,
        widgets.validation_evidence_edit,
        widgets.known_warnings_edit,
        widgets.planned_next_step_edit,
        widgets.notes_edit,
        project_root_edit,
    )
    for editor in editors:
        editor.textChanged.connect(callback)
    return len(editors)
