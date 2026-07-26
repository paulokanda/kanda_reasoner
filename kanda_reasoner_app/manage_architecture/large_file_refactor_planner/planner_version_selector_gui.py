# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_version_selector_gui.py
"""Compact exclusive version selector for Large File Refactor Planner actions."""

from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QMetaObject, Slot
from PySide6.QtWidgets import (
    QButtonGroup,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QWidget,
)

from .docstring_formatting import format_docstring_proposals
from .planner_version_state import (
    PLANNER_VERSION_HEURISTIC,
    PLANNER_VERSION_LOCAL_AI,
    PLANNER_VERSION_WEB_AI,
    get_selected_planner_version_bundle,
    planner_version_available,
    persist_planner_version_preference,
    select_planner_version,
    selected_planner_version,
)
from .split_formatting import format_split_plan

__all__ = [
    "build_planner_version_selector",
    "refresh_planner_version_selector",
    "render_selected_planner_version",
]

_VERSION_LABELS = (
    (PLANNER_VERSION_HEURISTIC, "Heuristic"),
    (PLANNER_VERSION_LOCAL_AI, "Local AI"),
    (PLANNER_VERSION_WEB_AI, "Imported Web AI"),
)


class _PlannerVersionSelectorWidget(QWidget):
    """Auto-connected selector host with bounded callbacks and no worker ownership."""

    def __init__(
        self,
        window: object,
        refresh_callback: Callable[[object], None],
        web_ai_import_callback: Callable[[object], None] | None,
        cancel_callback: Callable[[object], bool] | None,
    ) -> None:
        super().__init__()
        self._planner_window = window
        self._refresh_callback = refresh_callback
        self._web_ai_import_callback = web_ai_import_callback
        self._cancel_callback = cancel_callback

    @Slot(bool)
    def on_plannerVersionHeuristicRadio_toggled(self, checked: bool) -> None:
        self._select(PLANNER_VERSION_HEURISTIC, checked)

    @Slot(bool)
    def on_plannerVersionLocalAiRadio_toggled(self, checked: bool) -> None:
        self._select(PLANNER_VERSION_LOCAL_AI, checked)

    @Slot(bool)
    def on_plannerVersionImportedWebAiRadio_toggled(self, checked: bool) -> None:
        self._select(PLANNER_VERSION_WEB_AI, checked)

    @Slot()
    def on_largeFilePlannerVersionSelectionCancelButton_clicked(self) -> None:
        if self._cancel_callback is not None:
            self._cancel_callback(self._planner_window)

    def _select(self, version_name: str, checked: bool) -> None:
        _on_selected(
            self._planner_window,
            version_name,
            checked,
            self._refresh_callback,
            self._web_ai_import_callback,
        )


def build_planner_version_selector(
    window: object,
    *,
    refresh_callback: Callable[[object], None],
    web_ai_import_callback: Callable[[object], None] | None = None,
    cancel_callback: Callable[[object], bool] | None = None,
) -> QWidget:
    """Build exclusive route radios plus a bounded work-cancel action."""

    widget = _PlannerVersionSelectorWidget(
        window,
        refresh_callback,
        web_ai_import_callback,
        cancel_callback,
    )
    row = QHBoxLayout(widget)
    row.setContentsMargins(0, 0, 0, 0)
    row.setSpacing(12)
    row.addWidget(QLabel("Use Version"))
    group = QButtonGroup(widget)
    group.setExclusive(True)
    radios: dict[str, QRadioButton] = {}
    for version_name, label in _VERSION_LABELS:
        radio = QRadioButton(label)
        radio.setObjectName(_radio_object_name(version_name))
        group.addButton(radio)
        radios[version_name] = radio
        row.addWidget(radio)
    cancel_button = QPushButton("Cancel")
    cancel_button.setObjectName("largeFilePlannerVersionSelectionCancelButton")
    cancel_button.setToolTip(
        "Cancel active split-plan generation or Local AI review without changing "
        "the selected version."
    )
    cancel_button.setEnabled(False)
    row.addWidget(cancel_button)
    window._large_file_refactor_version_button_group = group
    window._large_file_refactor_version_radios = radios
    window._large_file_refactor_cancel_button = cancel_button
    QMetaObject.connectSlotsByName(widget)
    selected = selected_planner_version(window)
    if selected == PLANNER_VERSION_LOCAL_AI:
        radios[PLANNER_VERSION_LOCAL_AI].setChecked(True)
    else:
        radios[selected].setChecked(True)
    row.addStretch(1)
    refresh_planner_version_selector(window)
    return widget


def refresh_planner_version_selector(window: object) -> None:
    """Keep every version source selectable and show availability separately."""

    try:
        radios = window._large_file_refactor_version_radios
    except AttributeError:
        radios = {}
    selected = selected_planner_version(window)
    for version_name, _label in _VERSION_LABELS:
        radio = radios.get(version_name)
        if radio is None:
            continue
        radio.setEnabled(True)
        availability = (
            "available" if planner_version_available(window, version_name)
            else "not generated/imported yet"
        )
        radio.setToolTip(_version_tooltip(version_name, availability))
        if version_name == selected and not radio.isChecked():
            radio.blockSignals(True)
            radio.setChecked(True)
            radio.blockSignals(False)
    cancel_button = getattr(window, "_large_file_refactor_cancel_button", None)
    if cancel_button is not None:
        running = bool(
            getattr(window, "_large_file_refactor_split_plan_running", False)
            or getattr(window, "_large_file_refactor_ai_review_running", False)
        )
        cancel_button.setEnabled(running)


def render_selected_planner_version(window: object) -> None:
    """Render the selected isolated plan bundle into the Proposed Split Plan panel."""

    version_name = selected_planner_version(window)
    bundle = get_selected_planner_version_bundle(window)
    label = dict(_VERSION_LABELS).get(version_name, version_name)
    if bundle is None:
        window._large_file_refactor_plan_output.setPlainText(
            "ACTIVE PLANNER VERSION: " + label + "\n\n" + _missing_version_message(version_name)
        )
        return
    text = "ACTIVE PLANNER VERSION: " + label + "\n\n" + format_split_plan(bundle.plan)
    if bundle.docstring_proposals:
        text += "\n\n" + format_docstring_proposals(list(bundle.docstring_proposals))
    window._large_file_refactor_plan_output.setPlainText(text)


def _on_selected(
    window: object,
    version_name: str,
    checked: bool,
    refresh_callback: Callable[[object], None],
    web_ai_import_callback: Callable[[object], None] | None,
) -> None:
    """Select one version source and render its isolated planning state."""

    if not checked:
        return
    select_planner_version(window, version_name)
    persist_planner_version_preference(window, version_name)
    render_selected_planner_version(window)
    refresh_callback(window)
    if (
        version_name == PLANNER_VERSION_WEB_AI
        and not planner_version_available(window, version_name)
        and _analysis_is_available(window)
        and web_ai_import_callback is not None
    ):
        web_ai_import_callback(window)



def _radio_object_name(version_name: str) -> str:
    """Return the fixed object name used by Qt auto-connect."""

    if version_name == PLANNER_VERSION_HEURISTIC:
        return "plannerVersionHeuristicRadio"
    if version_name == PLANNER_VERSION_LOCAL_AI:
        return "plannerVersionLocalAiRadio"
    if version_name == PLANNER_VERSION_WEB_AI:
        return "plannerVersionImportedWebAiRadio"
    raise ValueError("Unknown Planner version: " + version_name)


def _analysis_is_available(window: object) -> bool:
    """Check Planner analysis availability without dynamic attribute lookup."""

    try:
        return window._large_file_refactor_last_analysis is not None
    except AttributeError:
        return False


def _version_tooltip(version_name: str, availability: str) -> str:
    if version_name == PLANNER_VERSION_WEB_AI:
        return (
            "Select the version imported from an external Web AI installer. "
            "State: " + availability
        )
    return "Select this local split-generation route. Version state: " + availability


def _missing_version_message(version_name: str) -> str:
    if version_name == PLANNER_VERSION_WEB_AI:
        return (
            "No Imported Web AI Version is loaded. Generate Heuristic or Local AI "
            "planning, copy Comprehensive Planning for Web AI, then either install "
            "the returned ZIP and select Imported Web AI Version, or paste the "
            "marker-wrapped response directly into Panel 4: Proposed split plan."
        )
    label = dict(_VERSION_LABELS).get(version_name, version_name)
    return label + " version has not been generated yet. Click Generate Split Plan."
