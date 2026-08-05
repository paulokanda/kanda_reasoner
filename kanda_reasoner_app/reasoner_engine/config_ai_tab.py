# project-path: kanda_reasoner_app/reasoner_engine/config_ai_tab.py
"""Composite Config AI tab for gateway, direct API, and local settings."""

from __future__ import annotations

from PySide6.QtWidgets import QTabWidget, QVBoxLayout, QWidget

from kanda_reasoner_app.local_ai_configuration import (
    LocalAIConfigurationController,
    application_local_ai_configuration,
)
from kanda_reasoner_app.reasoner_engine.config_direct_web_ai_tab import (
    ConfigDirectWebAITab,
)
from kanda_reasoner_app.reasoner_engine.config_local_ai_tab import ConfigLocalAITab
from kanda_reasoner_app.reasoner_engine.config_web_ai_tab import ConfigWebAITab
from kanda_reasoner_app.web_ai_configuration import application_web_ai_configuration

__all__ = ["ConfigAITab"]


class ConfigAITab(QWidget):
    """Host the canonical gateway, direct API, and local AI configuration."""

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        local_controller: LocalAIConfigurationController | None = None,
        external_controller: object | None = None,
    ) -> None:
        super().__init__(parent)
        del external_controller
        self._local_controller = local_controller or application_local_ai_configuration()
        self._web_controller = application_web_ai_configuration()
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        self.subtabs = QTabWidget()
        self.web_ai_tab = ConfigWebAITab()
        self.direct_web_ai_tab = ConfigDirectWebAITab(
            controller=self._web_controller
        )
        self.external_ai_tab = self.direct_web_ai_tab
        self.local_ai_tab = ConfigLocalAITab(controller=self._local_controller)
        self.subtabs.addTab(self.web_ai_tab, "Config Web AI")
        self.subtabs.addTab(self.direct_web_ai_tab, "Direct API Providers")
        self.subtabs.addTab(self.local_ai_tab, "Config Local AI")
        root.addWidget(self.subtabs)
        self._local_controller.open_configuration_requested.connect(
            lambda: self.subtabs.setCurrentWidget(self.local_ai_tab)
        )
        self._web_controller.open_configuration_requested.connect(
            self._open_selected_web_configuration
        )
        if self._local_controller.consume_open_target() == "local":
            self.subtabs.setCurrentWidget(self.local_ai_tab)

    def _open_selected_web_configuration(self) -> None:
        """Open the gateway or direct API subtab for the selected provider."""
        if self._web_controller.profile().provider_class == "direct":
            self.subtabs.setCurrentWidget(self.direct_web_ai_tab)
        else:
            self.subtabs.setCurrentWidget(self.web_ai_tab)
