# project-path: kanda_reasoner_app/templates/_green_sonar_panel.py
"""Floating panel widget for the green sonar activity monitor."""

from __future__ import annotations

from typing import Any

from ._green_sonar_runtime import (
    ERROR,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
    Qt,
    QColor,
    SONAR_BG,
    SONAR_BG_2,
    SONAR_BORDER,
    SONAR_MUTED,
    SONAR_TEXT,
    SUCCESS,
    WARNING,
    _PANEL_HEIGHT,
    _PANEL_WIDTH,
)
from ._green_sonar_scope import _SonarScope

class _SonarPanel(QFrame):
    """Shadowed floating process card anchored by GreenSonarActivityMonitor."""

    def __init__(self, parent: Any = None) -> None:
        """Build the panel layout."""

        super().__init__(parent)
        self.setObjectName("greenSonarActivityPanel")
        self.setFixedSize(_PANEL_WIDTH, _PANEL_HEIGHT)
        self.setAttribute(Qt.WA_StyledBackground, True)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 10)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.setGraphicsEffect(shadow)
        root = QHBoxLayout(self)
        root.setContentsMargins(14, 12, 14, 12)
        root.setSpacing(12)
        self.scope = _SonarScope(self)
        root.addWidget(self.scope, 0, Qt.AlignVCenter)
        text_box = QWidget(self)
        text_layout = QVBoxLayout(text_box)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(3)
        self.title_label = QLabel("Processing", self)
        self.title_label.setObjectName("greenSonarTitle")
        self.status_label = QLabel("Running", self)
        self.status_label.setObjectName("greenSonarStatus")
        self.detail_labels = [QLabel("", self) for _ in range(3)]
        for label in self.detail_labels:
            label.setObjectName("greenSonarDetail")
            label.setWordWrap(True)
        text_layout.addWidget(self.title_label)
        text_layout.addWidget(self.status_label)
        for label in self.detail_labels:
            text_layout.addWidget(label)
        text_layout.addStretch(1)
        root.addWidget(text_box, 1)
        self._apply_style("running")
        self.hide()

    def set_content(self, title: str, status: str, details: tuple[str, str, str], state: str) -> None:
        """Update panel text and visual state."""

        self.title_label.setText(str(title or "Processing"))
        self.status_label.setText(str(status or "Running"))
        for index, label in enumerate(self.detail_labels):
            label.setText(str(details[index] if index < len(details) else ""))
        self.scope.set_state(state)
        self._apply_style(state)

    def _apply_style(self, state: str) -> None:
        """Apply state-dependent panel styling."""

        accent = ERROR if state == "error" else SUCCESS if state == "success" else WARNING if state == "warning" else SONAR_BORDER
        self.setStyleSheet(
            "QFrame#greenSonarActivityPanel {"
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 " + SONAR_BG_2 + ", stop:1 " + SONAR_BG + ");"
            "border: 1px solid " + accent + ";"
            "border-radius: 16px;"
            "}"
            "QLabel#greenSonarTitle {color: " + SONAR_TEXT + "; font-family: Segoe UI; font-size: 11pt; font-weight: 700;}"
            "QLabel#greenSonarStatus {color: " + accent + "; font-family: Segoe UI; font-size: 9pt; font-weight: 700; padding-bottom: 4px;}"
            "QLabel#greenSonarDetail {color: " + SONAR_MUTED + "; font-family: Segoe UI; font-size: 8.5pt;}"
        )
