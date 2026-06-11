"""Fallback Brain Navigator index widget.

This module owns the first visible Brain Navigator fallback UI. It deliberately
uses normal Qt widgets only and does not import the web engine or the future 3D
brain bridge. The widget presents the brain-to-tool mapping as an index and
updates a Remember Box style card before requesting tab navigation through an
injected callback.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from importlib import import_module
from typing import Any

from kanda_reasoner_app.reasoner_tools_gui_shell.brain_region_mapping.contract import (
    BrainRegionTarget,
    list_brain_region_targets,
)
from kanda_reasoner_app.reasoner_tools_gui_shell.remember_box.contract import (
    RememberBoxState,
    build_remember_box_state,
    create_empty_remember_box_state,
)

OpenTabById = Callable[[str], object]


def _qt_widgets_attr(name: str) -> Any:
    """Return a PySide6.QtWidgets attribute through a lazy import."""

    return getattr(import_module("PySide6.QtWidgets"), name)


def _qt_core_attr(name: str) -> Any:
    """Return a PySide6.QtCore attribute through a lazy import."""

    return getattr(import_module("PySide6.QtCore"), name)


@dataclass(frozen=True)
class BrainNavigatorFallbackConfig:
    """Configuration for the fallback Brain Navigator index.

    Attributes:
        open_tab_by_id: Optional callback that opens a target tab by stable ID.
        region_targets: Optional explicit target list for tests or alternate maps.
    """

    open_tab_by_id: OpenTabById | None = None
    region_targets: tuple[BrainRegionTarget, ...] | None = None


class BrainNavigatorFallbackWidget(_qt_widgets_attr("QWidget")):
    """First-tab fallback index for the Brain Navigator box.

    The widget keeps visible behavior inside the Brain Navigator box while using
    only public contracts from mapping and Remember Box. It never reaches into
    MainWindow, tab internals, or QTabWidget indexes.
    """

    def __init__(self, config: BrainNavigatorFallbackConfig | None = None) -> None:
        """Create the fallback index widget.

        Args:
            config: Optional fallback widget configuration.
        """

        super().__init__()
        self._config = config or BrainNavigatorFallbackConfig()
        self._open_tab_by_id = self._config.open_tab_by_id
        self._region_targets = tuple(
            self._config.region_targets or list_brain_region_targets()
        )
        self._selected_state = create_empty_remember_box_state()
        self._selected_target_tab_id = ""

        self._title_label = _qt_widgets_attr("QLabel")("Brain Navigator")
        self._subtitle_label = _qt_widgets_attr("QLabel")(
            "Safe fallback index. The 3D rotating brain will be connected in a later box patch."
        )
        self._region_label = _qt_widgets_attr("QLabel")()
        self._target_label = _qt_widgets_attr("QLabel")()
        self._analogy_title_label = _qt_widgets_attr("QLabel")()
        self._analogy_text_label = _qt_widgets_attr("QLabel")()
        self._status_label = _qt_widgets_attr("QLabel")()
        self._open_button = _qt_widgets_attr("QPushButton")("Open tool")
        self._button_by_region_id: dict[str, object] = {}

        self._build_ui()
        self._apply_state(self._selected_state)

    def _build_ui(self) -> None:
        """Build the fallback index layout."""

        QFrame = _qt_widgets_attr("QFrame")
        QGridLayout = _qt_widgets_attr("QGridLayout")
        QHBoxLayout = _qt_widgets_attr("QHBoxLayout")
        QPushButton = _qt_widgets_attr("QPushButton")
        QVBoxLayout = _qt_widgets_attr("QVBoxLayout")
        Qt = _qt_core_attr("Qt")

        root = QVBoxLayout(self)
        root.setContentsMargins(14, 14, 14, 14)
        root.setSpacing(12)

        self._title_label.setObjectName("brainNavigatorTitle")
        self._title_label.setAlignment(Qt.AlignCenter)
        self._title_label.setStyleSheet(
            "font-size: 20px; font-weight: 700; color: #1f4ea3;"
        )
        root.addWidget(self._title_label)

        self._subtitle_label.setObjectName("brainNavigatorSubtitle")
        self._subtitle_label.setWordWrap(True)
        self._subtitle_label.setAlignment(Qt.AlignCenter)
        self._subtitle_label.setStyleSheet("color: #555555; font-weight: 600;")
        root.addWidget(self._subtitle_label)

        content = QHBoxLayout()
        content.setSpacing(14)
        root.addLayout(content, 1)

        index_frame = QFrame()
        index_frame.setObjectName("brainNavigatorIndexFrame")
        index_frame.setFrameShape(QFrame.StyledPanel)
        index_layout = QVBoxLayout(index_frame)
        index_layout.setContentsMargins(12, 12, 12, 12)
        index_layout.setSpacing(8)

        index_title = _qt_widgets_attr("QLabel")("Brain structures as app modules")
        index_title.setStyleSheet("font-weight: 700;")
        index_layout.addWidget(index_title)

        grid = QGridLayout()
        grid.setSpacing(6)
        index_layout.addLayout(grid)

        for index, target in enumerate(self._region_targets):
            button = QPushButton(f"{target.region_name} -> {target.target_tab_label}")
            button.setObjectName(f"brainRegionButton_{target.region_id}")
            button.setToolTip(target.tooltip_text)
            button.clicked.connect(
                lambda _checked=False, region_id=target.region_id: self.select_region(region_id)
            )
            self._button_by_region_id[target.region_id] = button
            grid.addWidget(button, index // 2, index % 2)

        content.addWidget(index_frame, 2)

        card_frame = QFrame()
        card_frame.setObjectName("brainNavigatorRememberFrame")
        card_frame.setFrameShape(QFrame.StyledPanel)
        card_layout = QVBoxLayout(card_frame)
        card_layout.setContentsMargins(12, 12, 12, 12)
        card_layout.setSpacing(8)

        card_title = _qt_widgets_attr("QLabel")("Remember Box")
        card_title.setStyleSheet("font-weight: 700; color: #d46b08;")
        card_layout.addWidget(card_title)

        for label in (
            self._region_label,
            self._target_label,
            self._analogy_title_label,
            self._analogy_text_label,
            self._status_label,
        ):
            label.setWordWrap(True)
            card_layout.addWidget(label)

        self._open_button.setObjectName("brainNavigatorOpenToolButton")
        self._open_button.clicked.connect(self.open_selected_target)
        card_layout.addWidget(self._open_button)
        card_layout.addStretch(1)

        content.addWidget(card_frame, 1)

    def select_region(self, region_id: str) -> RememberBoxState:
        """Select a brain region and update the Remember Box card.

        Args:
            region_id: Brain region identifier from the mapping contract.

        Returns:
            The new RememberBoxState displayed by the widget.
        """

        target = next(
            (item for item in self._region_targets if item.region_id == region_id),
            None,
        )
        state = build_remember_box_state(target)
        self._apply_state(state)
        return state

    def open_selected_target(self) -> object | None:
        """Request opening the currently selected target tab.

        Returns:
            Whatever the injected ``open_tab_by_id`` callback returns, or None
            when no target/callback is available.
        """

        if not self._selected_state.can_open_target:
            return None
        if self._open_tab_by_id is None:
            return None
        return self._open_tab_by_id(self._selected_state.target_tab_id)

    def _apply_state(self, state: RememberBoxState) -> None:
        """Render a RememberBoxState into the fallback card."""

        self._selected_state = state
        self._selected_target_tab_id = state.target_tab_id
        self._region_label.setText(f"Brain structure: {state.region_name}")
        self._target_label.setText(f"Mapped tab: {state.target_tab_label}")
        self._analogy_title_label.setText(f"Analogy: {state.analogy_title}")
        self._analogy_text_label.setText(state.analogy_text)
        self._status_label.setText(f"Status: {state.status}")
        self._open_button.setText(state.action_label)
        self._open_button.setEnabled(state.can_open_target and self._open_tab_by_id is not None)

    def current_remember_state(self) -> RememberBoxState:
        """Return the currently displayed RememberBoxState."""

        return self._selected_state


def create_brain_navigator_fallback_widget(
    *,
    open_tab_by_id: OpenTabById | None = None,
    region_targets: tuple[BrainRegionTarget, ...] | None = None,
) -> object:
    """Create the visible fallback Brain Navigator widget.

    Args:
        open_tab_by_id: Optional stable tab-id navigation callback.
        region_targets: Optional explicit mapping targets.

    Returns:
        A QWidget instance without importing the web engine or brain mesh assets.
    """

    return BrainNavigatorFallbackWidget(
        BrainNavigatorFallbackConfig(
            open_tab_by_id=open_tab_by_id,
            region_targets=region_targets,
        )
    )
