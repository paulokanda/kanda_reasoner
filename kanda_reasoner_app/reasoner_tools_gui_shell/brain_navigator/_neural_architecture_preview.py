"""Internal isolated WebView preview for the Neural Architecture brain asset.

This module creates an explicit manual-preview QWebEngineView for the extracted
Brain Navigator visual asset. It is not wired into the visible first tab and it
never switches tabs directly. Importing this module is safe without PySide6
because Qt classes are loaded only by the preview factory.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from importlib import import_module
from typing import Any

from ._web_bridge import (
    BrainWebBridgeBundle,
    BrainWebBridgeConfig,
    build_brain_web_channel_bootstrap_script,
    create_brain_web_bridge,
)
from .assets.brain_visual_template import build_neural_architecture_asset_preview_html

RegionCallback = Callable[[str], object]

NEURAL_ARCHITECTURE_PREVIEW_TITLE = "Neural Architecture Preview"

__all__: list[str] = []


@dataclass(frozen=True)
class NeuralArchitecturePreviewConfig:
    """Configuration for the isolated Neural Architecture preview.

    Attributes:
        on_region_hovered: Optional adapter called when the preview bridge
            receives a hover event.
        on_region_clicked: Optional adapter called when the preview bridge
            receives a click event.
        object_name: Object name registered in the QWebChannel.
        window_title: Title used by the manual preview wrapper widget.
    """

    on_region_hovered: RegionCallback | None = None
    on_region_clicked: RegionCallback | None = None
    object_name: str = "bridge"
    window_title: str = NEURAL_ARCHITECTURE_PREVIEW_TITLE


@dataclass(frozen=True)
class NeuralArchitecturePreviewSummary:
    """Describe the isolated Neural Architecture preview sub-box boundary."""

    box_id: str
    contract_version: str
    responsibility: str
    owner_paths: tuple[str, ...]
    public_functions: tuple[str, ...]
    allowed_dependencies: tuple[str, ...]
    forbidden_dependencies: tuple[str, ...]
    implementation_state: str
    visual_integration_state: str


@dataclass(frozen=True)
class NeuralArchitecturePreviewBundle:
    """Created preview objects returned by the factory.

    Attributes:
        widget: QWidget wrapper containing the QWebEngineView.
        web_view: QWebEngineView instance.
        bridge_bundle: BrainWebBridgeBundle attached to the web page.
        html: Local HTML loaded into the web view.
    """

    widget: object
    web_view: object
    bridge_bundle: BrainWebBridgeBundle
    html: str


def _qt_widgets_attr(name: str) -> Any:
    """Return a PySide6.QtWidgets attribute through a lazy import."""

    return getattr(import_module("PySide6.QtWidgets"), name)


def _qt_web_engine_widgets_attr(name: str) -> Any:
    """Return a PySide6.QtWebEngineWidgets attribute through a lazy import."""

    return getattr(import_module("PySide6.QtWebEngineWidgets"), name)


def build_neural_architecture_preview_html(
    *,
    object_name: str = "bridge",
) -> str:
    """Build HTML for the isolated Neural Architecture WebView preview.

    The returned page uses the extracted visual asset and injects the same
    QWebChannel bridge bootstrap used by future in-tab integration.

    Args:
        object_name: QWebChannel object name used by the bridge bootstrap.

    Returns:
        Complete HTML document for QWebEngineView.setHtml.
    """

    html = build_neural_architecture_asset_preview_html()
    bootstrap_script = build_brain_web_channel_bootstrap_script(object_name)
    insertion = (
        "\n// Bridge bootstrap for isolated manual preview.\n"
        + bootstrap_script
        + "\n"
    )
    script_marker = "<script>\n"
    if script_marker in html:
        return html.replace(script_marker, script_marker + insertion, 1)
    return html.replace("</body>", f"<script>{insertion}</script></body>")


def create_neural_architecture_preview(
    config: NeuralArchitecturePreviewConfig | None = None,
) -> NeuralArchitecturePreviewBundle:
    """Create the isolated Neural Architecture preview widget.

    This factory is intentionally separate from the visible Brain Navigator tab.
    It creates a QWebEngineView, attaches the Brain Web Bridge, loads the
    extracted asset preview HTML, and returns all created objects for manual
    visual testing.

    Args:
        config: Optional preview configuration.

    Returns:
        Bundle containing the wrapper widget, web view, bridge, and HTML.
    """

    preview_config = config or NeuralArchitecturePreviewConfig()
    html = build_neural_architecture_preview_html(
        object_name=preview_config.object_name,
    )

    QWidget = _qt_widgets_attr("QWidget")
    QVBoxLayout = _qt_widgets_attr("QVBoxLayout")
    QWebEngineView = _qt_web_engine_widgets_attr("QWebEngineView")

    widget = QWidget()
    widget.setObjectName("neuralArchitecturePreviewWidget")
    widget.setWindowTitle(preview_config.window_title)

    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)

    web_view = QWebEngineView()
    web_view.setObjectName("neuralArchitecturePreviewView")
    layout.addWidget(web_view)

    bridge_bundle = create_brain_web_bridge(
        BrainWebBridgeConfig(
            object_name=preview_config.object_name,
            on_region_hovered=preview_config.on_region_hovered,
            on_region_clicked=preview_config.on_region_clicked,
        )
    )
    bridge_bundle.connect_to_page(web_view.page())
    # Keep strong references on Qt-owned objects so the QObject bridge and
    # QWebChannel survive after the factory returns. This is required for
    # runtime Open module button clicks to reach Python reliably.
    setattr(widget, "_brain_navigator_bridge_bundle", bridge_bundle)
    setattr(web_view, "_brain_navigator_bridge_bundle", bridge_bundle)
    web_view.setHtml(html)

    return NeuralArchitecturePreviewBundle(
        widget=widget,
        web_view=web_view,
        bridge_bundle=bridge_bundle,
        html=html,
    )


def get_neural_architecture_preview_summary() -> NeuralArchitecturePreviewSummary:
    """Return Box Architecture metadata for the isolated preview sub-box."""

    return NeuralArchitecturePreviewSummary(
        box_id="neural_architecture_preview",
        contract_version="0.1",
        responsibility=(
            "Create an explicit manual-preview QWebEngineView for the extracted "
            "Neural Architecture brain asset without replacing the visible "
            "Brain Navigator fallback tab."
        ),
        owner_paths=(
            "kanda_reasoner_app/reasoner_tools_gui_shell/brain_navigator/_neural_architecture_preview.py",
        ),
        public_functions=(
            "build_neural_architecture_preview_html",
            "create_neural_architecture_preview",
            "get_neural_architecture_preview_summary",
        ),
        allowed_dependencies=(
            "brain_navigator.assets.brain_visual_template",
            "brain_navigator._web_bridge",
            "PySide6.QtWebEngineWidgets.lazy_factory_only",
        ),
        forbidden_dependencies=(
            "main_window",
            "tool_specs",
            "tab_navigation_controller",
            "direct_tab_index_switching",
            "other_tab_internals",
        ),
        implementation_state="isolated_neural_architecture_webview_preview",
        visual_integration_state="manual_preview_only_not_default_visible_tab",
    )
