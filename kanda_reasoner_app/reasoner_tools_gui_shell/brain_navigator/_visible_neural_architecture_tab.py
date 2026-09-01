# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/brain_navigator/_visible_neural_architecture_tab.py
"""Visible Neural Architecture tab factory for Brain Navigator.

This module promotes the isolated Neural Architecture WebView preview into the
visible Brain Navigator tab while preserving the safe fallback index if WebEngine
or the brain renderer cannot be created. It does not switch tabs, import
MainWindow, or inspect tab internals. PySide-dependent factories are imported
only inside the creation path.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

OpenTabById = Callable[[str], object]
CanOpenTabId = Callable[[str], bool]

__all__: list[str] = []


@dataclass(frozen=True)
class VisibleNeuralArchitectureTabSummary:
    """Describe the visible Neural Architecture tab integration boundary."""

    box_id: str
    contract_version: str
    responsibility: str
    owner_paths: tuple[str, ...]
    public_functions: tuple[str, ...]
    visual_integration_state: str
    fallback_behavior: str
    forbidden_dependencies: tuple[str, ...]


def open_mapped_tab_by_region_id(
    region_id: str,
    open_tab_by_id: OpenTabById | None,
    can_open_tab_id: CanOpenTabId | None = None,
) -> object | None:
    """Resolve a brain region and request stable-tab navigation.

    The WebView emits only the region identifier. This adapter uses the public
    Brain Region Mapping contract and the injected tab-opening callback. It does
    not inspect tab widgets, registry internals, or numeric indexes.
    """

    if open_tab_by_id is None:
        return None

    from ..brain_region_mapping.contract import resolve_brain_region

    target = resolve_brain_region(region_id)
    if not target.is_known or not target.target_tab_id:
        return None
    if can_open_tab_id is not None and not can_open_tab_id(target.target_tab_id):
        return None
    return open_tab_by_id(target.target_tab_id)


def create_visible_neural_architecture_brain_tab(
    *,
    open_tab_by_id: OpenTabById | None = None,
    can_open_tab_id: CanOpenTabId | None = None,
) -> object:
    """Create the visible Brain Navigator tab as the Neural Architecture brain.

    Args:
        open_tab_by_id: Reserved injected navigation callback. It is passed only
            to the fallback widget if the WebView cannot be created. Direct tab
            opening from the brain visual is performed only after the user clicks
            the explicit Open module button inside the floating Fancy Index.

    Returns:
        QWidget containing the Neural Architecture WebView, or the safe fallback
        index widget if WebEngine/visual creation fails.
    """

    try:
        from ._neural_architecture_preview import (
            NeuralArchitecturePreviewConfig,
            create_neural_architecture_preview,
        )

        bundle = create_neural_architecture_preview(
            NeuralArchitecturePreviewConfig(
                window_title="Brain Navigator",
                on_region_clicked=lambda region_id: open_mapped_tab_by_region_id(
                    region_id,
                    open_tab_by_id,
                    can_open_tab_id,
                ),
            )
        )
        bundle.widget.setObjectName("visibleNeuralArchitectureBrainTab")
        from ._fallback_index_widget import create_brain_navigator_fallback_widget

        fallback_widget = create_brain_navigator_fallback_widget(
            open_tab_by_id=open_tab_by_id,
            can_open_tab_id=can_open_tab_id,
        )
        fallback_widget.hide()
        layout = bundle.widget.layout()
        if layout is None:
            raise RuntimeError("Brain Navigator preview layout is unavailable")
        layout.addWidget(fallback_widget)

        def _show_fallback(*_args: object) -> None:
            try:
                bundle.web_view.hide()
                fallback_widget.show()
            except RuntimeError:
                return

        def _show_preview_if_healthy(load_ok: bool) -> None:
            if not load_ok:
                _show_fallback()
                return

            def _renderer_ready(value: object) -> None:
                if bool(value):
                    try:
                        fallback_widget.hide()
                        bundle.web_view.show()
                    except RuntimeError:
                        return
                else:
                    _show_fallback()

            try:
                bundle.web_view.page().runJavaScript(
                    "typeof THREE !== 'undefined'",
                    _renderer_ready,
                )
            except (AttributeError, RuntimeError):
                _show_fallback()

        load_finished = getattr(bundle.web_view, "loadFinished", None)
        if load_finished is not None and hasattr(load_finished, "connect"):
            load_finished.connect(_show_preview_if_healthy)
        page = bundle.web_view.page()
        render_terminated = getattr(page, "renderProcessTerminated", None)
        if render_terminated is not None and hasattr(render_terminated, "connect"):
            render_terminated.connect(_show_fallback)

        # Keep the preview bundle and fallback alive for the lifetime of the tab.
        # QWebChannel does not reliably preserve the Python QObject bridge if
        # the only strong reference is the local factory variable.
        setattr(bundle.widget, "_brain_navigator_preview_bundle", bundle)
        setattr(bundle.widget, "_brain_navigator_fallback_widget", fallback_widget)
        setattr(bundle.widget, "_brain_navigator_open_tab_by_id", open_tab_by_id)
        setattr(bundle.widget, "_brain_navigator_can_open_tab_id", can_open_tab_id)
        return bundle.widget
    except Exception:
        from ._fallback_index_widget import create_brain_navigator_fallback_widget

        return create_brain_navigator_fallback_widget(
            open_tab_by_id=open_tab_by_id,
            can_open_tab_id=can_open_tab_id,
        )


def get_visible_neural_architecture_tab_summary() -> VisibleNeuralArchitectureTabSummary:
    """Return Box Architecture metadata for the visible brain integration."""

    return VisibleNeuralArchitectureTabSummary(
        box_id="visible_neural_architecture_brain_tab",
        contract_version="0.2",
        responsibility=(
            "Create the visible Brain Navigator tab using the Neural Architecture "
            "WebView by default, with fallback index only if WebEngine creation fails. "
            "Open module actions are routed through the injected stable-tab callback."
        ),
        owner_paths=(
            "kanda_reasoner_app/reasoner_tools_gui_shell/brain_navigator/_visible_neural_architecture_tab.py",
        ),
        public_functions=(
            "create_visible_neural_architecture_brain_tab",
            "open_mapped_tab_by_region_id",
            "get_visible_neural_architecture_tab_summary",
        ),
        visual_integration_state="visible_default_neural_architecture_with_fancy_index_open_module_action",
        fallback_behavior="fallback_index_only_when_webengine_or_brain_visual_creation_fails",
        forbidden_dependencies=(
            "main_window",
            "tool_specs",
            "tab_navigation_controller",
            "direct_tab_index_switching",
            "other_tab_internals",
        ),
    )
