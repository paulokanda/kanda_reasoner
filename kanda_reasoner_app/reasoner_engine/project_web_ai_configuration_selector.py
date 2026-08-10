# project-path: kanda_reasoner_app/reasoner_engine/project_web_ai_configuration_selector.py
"""Mirror central Web AI provider and model selection inside Project Web AI."""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import QSignalBlocker

from kanda_reasoner_app.web_ai_provider_contracts import (
    ModelDescriptor,
    provider_profiles,
)

__all__ = ["connect", "render"]


def connect(owner: Any) -> None:
    """Connect mirrored selectors to the existing application controller."""
    owner.web_access_combo.currentIndexChanged.connect(
        lambda _index: _access_changed(owner)
    )
    owner.web_provider_combo.currentIndexChanged.connect(
        lambda _index: _provider_changed(owner)
    )
    owner.web_model_combo.currentIndexChanged.connect(
        lambda _index: _model_changed(owner)
    )
    owner.web_refresh_models_button.clicked.connect(
        owner._web_config.refresh_models
    )


def _access_changed(owner: Any) -> None:
    provider_class = str(owner.web_access_combo.currentData() or "")
    profile = owner._web_config.profile()
    if profile.provider_class == provider_class:
        return
    profiles = tuple(provider_profiles(provider_class))
    if profiles:
        owner._web_config.set_gateway_id(profiles[0].gateway_id)


def _provider_changed(owner: Any) -> None:
    provider_id = str(owner.web_provider_combo.currentData() or "")
    if provider_id:
        owner._web_config.set_gateway_id(provider_id)


def _model_changed(owner: Any) -> None:
    model = owner.web_model_combo.currentData()
    owner._web_config.set_selected_model_id(
        model.model_id if isinstance(model, ModelDescriptor) else ""
    )


def render(owner: Any) -> None:
    """Render controller state without creating a second configuration owner."""
    controller = owner._web_config
    profile = controller.profile()

    with QSignalBlocker(owner.web_access_combo):
        index = owner.web_access_combo.findData(profile.provider_class)
        if index >= 0:
            owner.web_access_combo.setCurrentIndex(index)

    profiles = tuple(provider_profiles(profile.provider_class))
    with QSignalBlocker(owner.web_provider_combo):
        owner.web_provider_combo.clear()
        for item in profiles:
            owner.web_provider_combo.addItem(
                item.display_name,
                item.gateway_id,
            )
        index = owner.web_provider_combo.findData(profile.gateway_id)
        owner.web_provider_combo.setCurrentIndex(index)

    selected_id = controller.selected_model_id()
    with QSignalBlocker(owner.web_model_combo):
        owner.web_model_combo.clear()
        for model in controller.visible_models():
            owner.web_model_combo.addItem(
                "[FREE] " + model.display_name + " - " + model.model_id,
                model,
            )
        selected_index = -1
        for index in range(owner.web_model_combo.count()):
            value = owner.web_model_combo.itemData(index)
            if isinstance(value, ModelDescriptor) and value.model_id == selected_id:
                selected_index = index
                break
        owner.web_model_combo.setCurrentIndex(selected_index)

    has_models = owner.web_model_combo.count() > 0
    owner.web_model_combo.setEnabled(has_models)
    owner.web_refresh_models_button.setEnabled(
        controller.catalog_status() != "Loading..."
    )
    owner.open_web_config_button.setText(
        "Open Direct API Configuration"
        if profile.provider_class == "direct"
        else "Open Gateway Configuration"
    )
