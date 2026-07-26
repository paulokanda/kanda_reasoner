# project-path: kanda_reasoner_app/reasoner_engine/config_ai_tab.py
"""Composite Config AI tab with preserved Web AI and global Local AI settings."""

from __future__ import annotations

from PySide6.QtWidgets import QTabWidget, QVBoxLayout, QWidget

from kanda_reasoner_app.local_ai_configuration import (
    LocalAIConfigurationController,
    application_local_ai_configuration,
)
from kanda_reasoner_app.reasoner_engine.config_local_ai_tab import ConfigLocalAITab
from kanda_reasoner_app.reasoner_engine.config_web_ai_tab import ConfigWebAITab
from kanda_reasoner_app.web_ai_configuration import application_web_ai_configuration

__all__ = ["ConfigAITab"]


class ConfigAITab(QWidget):
    """Host the unchanged Web AI configuration and one global Local AI owner."""

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        local_controller: LocalAIConfigurationController | None = None,
    ) -> None:
        super().__init__(parent)
        self._local_controller = local_controller or application_local_ai_configuration()
        self._web_controller = application_web_ai_configuration()
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        self.subtabs = QTabWidget()
        self.web_ai_tab = ConfigWebAITab()
        self.local_ai_tab = ConfigLocalAITab(controller=self._local_controller)
        self.subtabs.addTab(self.web_ai_tab, "Config Web AI")
        self.subtabs.addTab(self.local_ai_tab, "Config Local AI")
        root.addWidget(self.subtabs)
        self._local_controller.open_configuration_requested.connect(
            lambda: self.subtabs.setCurrentWidget(self.local_ai_tab)
        )
        self._web_controller.open_configuration_requested.connect(
            lambda: self.subtabs.setCurrentWidget(self.web_ai_tab)
        )
        if self._local_controller.consume_open_target() == "local":
            self.subtabs.setCurrentWidget(self.local_ai_tab)
