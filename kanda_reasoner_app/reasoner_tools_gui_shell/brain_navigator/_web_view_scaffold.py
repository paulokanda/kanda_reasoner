"""Internal QWebEngine scaffold for Brain Navigator web content.

This module owns the safe, test-page WebView scaffold for the Brain Navigator
box. It is intentionally not wired into the visible first tab yet. Importing the
module is safe without PySide6 or QWebEngine because Qt classes are loaded only
when ``create_brain_web_view_scaffold`` is called.

The scaffold creates a simple local HTML surface with brain-region buttons and
QWebChannel calls. It emits region intent through the Brain Web Bridge only and
never switches tabs directly.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from html import escape
from importlib import import_module
from typing import Any

from kanda_reasoner_app.reasoner_tools_gui_shell.brain_region_mapping.contract import (
    BrainRegionTarget,
    list_brain_region_targets,
)

from ._web_bridge import (
    BrainWebBridgeBundle,
    BrainWebBridgeConfig,
    build_brain_web_channel_bootstrap_script,
    create_brain_web_bridge,
)

RegionCallback = Callable[[str], object]

QWEBCHANNEL_SCRIPT_URL = "qrc:///qtwebchannel/qwebchannel.js"
BRAIN_WEB_VIEW_SCAFFOLD_TITLE = "Brain Navigator WebView Scaffold"

__all__: list[str] = []


@dataclass(frozen=True)
class BrainWebViewScaffoldConfig:
    """Configuration for the safe Brain Navigator WebView scaffold.

    Attributes:
        region_targets: Optional explicit brain-region mapping targets.
        on_region_hovered: Optional adapter called when the WebBridge receives
            a hover event.
        on_region_clicked: Optional adapter called when the WebBridge receives
            a click event.
        object_name: Object name registered in the QWebChannel.
    """

    region_targets: tuple[BrainRegionTarget, ...] | None = None
    on_region_hovered: RegionCallback | None = None
    on_region_clicked: RegionCallback | None = None
    object_name: str = "bridge"


@dataclass(frozen=True)
class BrainWebViewScaffoldSummary:
    """Describe the Brain WebView scaffold sub-box boundary."""

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
class BrainWebViewScaffoldBundle:
    """Created WebView scaffold objects returned by the factory.

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


def _target_rows(region_targets: Sequence[BrainRegionTarget]) -> str:
    """Render HTML rows for the scaffold's region buttons."""

    rows: list[str] = []
    for target in region_targets:
        region_id = escape(target.region_id, quote=True)
        region_name = escape(target.region_name, quote=True)
        tab_label = escape(target.target_tab_label, quote=True)
        tooltip = escape(target.tooltip_text, quote=True)
        rows.append(
            "<button class=\"region-card\" "
            f"data-region-id=\"{region_id}\" "
            f"title=\"{tooltip}\" "
            f"onmouseenter=\"notifyRegionHovered('{region_id}')\" "
            f"onclick=\"notifyRegionClicked('{region_id}')\">"
            f"<span class=\"region-name\">{region_name}</span>"
            f"<span class=\"target-name\">{tab_label}</span>"
            "</button>"
        )
    return "\n".join(rows)


def build_brain_web_view_scaffold_html(
    region_targets: Sequence[BrainRegionTarget] | None = None,
    *,
    object_name: str = "bridge",
) -> str:
    """Build the local HTML used by the WebView scaffold.

    Args:
        region_targets: Optional explicit mapping targets.
        object_name: QWebChannel object name used by the bridge bootstrap.

    Returns:
        Complete HTML document for QWebEngineView.setHtml.
    """

    targets = tuple(region_targets or list_brain_region_targets())
    rows = _target_rows(targets)
    bootstrap_script = build_brain_web_channel_bootstrap_script(object_name)
    escaped_title = escape(BRAIN_WEB_VIEW_SCAFFOLD_TITLE)

    return f"""<!doctype html>
<html lang=\"en\">
<head>
<meta charset=\"utf-8\">
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
<title>{escaped_title}</title>
<script src=\"{QWEBCHANNEL_SCRIPT_URL}\"></script>
<style>
html, body {{
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    background: #05070d;
    color: #f5f7fb;
    font-family: Arial, Helvetica, sans-serif;
}}
.shell {{
    box-sizing: border-box;
    min-height: 100%;
    padding: 24px;
    display: grid;
    grid-template-columns: minmax(280px, 1fr) minmax(260px, 0.75fr);
    gap: 18px;
}}
.stage {{
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 18px;
    background: radial-gradient(circle at center, #223765 0%, #101827 44%, #070a12 100%);
    min-height: 420px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}
.brain-placeholder {{
    width: min(430px, 82%);
    aspect-ratio: 1.22;
    border-radius: 48% 52% 46% 54%;
    border: 2px solid rgba(255, 172, 64, 0.9);
    box-shadow: 0 0 34px rgba(255, 153, 51, 0.34), inset 0 0 42px rgba(48, 102, 190, 0.55);
    animation: brainSpin 18s linear infinite;
    position: relative;
}}
.brain-placeholder::before,
.brain-placeholder::after {{
    content: \"\";
    position: absolute;
    inset: 16% 22%;
    border: 1px solid rgba(255, 255, 255, 0.22);
    border-radius: 45% 55% 50% 50%;
}}
.brain-placeholder::after {{
    inset: 24% 32%;
    border-color: rgba(255, 172, 64, 0.35);
}}
@keyframes brainSpin {{
    0% {{ transform: rotateY(0deg) rotateZ(-2deg); }}
    50% {{ transform: rotateY(180deg) rotateZ(2deg); }}
    100% {{ transform: rotateY(360deg) rotateZ(-2deg); }}
}}
.panel {{
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 18px;
    background: rgba(9, 13, 23, 0.88);
    padding: 18px;
}}
h1 {{
    margin: 0 0 8px;
    color: #ffad42;
    font-size: 22px;
}}
p {{
    margin: 0 0 16px;
    color: #c9d3e8;
    line-height: 1.45;
}}
.region-grid {{
    display: grid;
    gap: 8px;
}}
.region-card {{
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 12px;
    background: rgba(35, 53, 88, 0.72);
    color: #ffffff;
    padding: 10px 12px;
    text-align: left;
    cursor: pointer;
}}
.region-card:hover {{
    border-color: rgba(255, 172, 64, 0.95);
    background: rgba(71, 92, 140, 0.86);
}}
.region-name {{
    display: block;
    font-weight: 700;
}}
.target-name {{
    display: block;
    color: #b8c7e6;
    font-size: 12px;
    margin-top: 3px;
}}
.status {{
    margin-top: 14px;
    color: #ffcf8a;
    font-weight: 700;
}}
</style>
</head>
<body>
<div class=\"shell\">
    <section class=\"stage\" aria-label=\"Brain preview scaffold\">
        <div class=\"brain-placeholder\" role=\"img\" aria-label=\"Rotating brain placeholder\"></div>
    </section>
    <aside class=\"panel\">
        <h1>{escaped_title}</h1>
        <p>This safe local WebView test surface validates QWebChannel bridge wiring before the real rotating brain replaces the fallback index.</p>
        <div class=\"region-grid\">
{rows}
        </div>
        <div id=\"status\" class=\"status\">Bridge status: initializing</div>
    </aside>
</div>
<script>
{bootstrap_script}
function setStatus(text) {{
    const statusNode = document.getElementById('status');
    if (statusNode) {{
        statusNode.textContent = text;
    }}
}}
function notifyRegionHovered(regionId) {{
    if (window.brainNavigatorBridge && window.brainNavigatorBridge.onRegionHovered) {{
        window.brainNavigatorBridge.onRegionHovered(regionId);
        setStatus('Hovered: ' + regionId);
    }} else {{
        setStatus('Bridge not ready for hover: ' + regionId);
    }}
}}
function notifyRegionClicked(regionId) {{
    if (window.brainNavigatorBridge && window.brainNavigatorBridge.onRegionClicked) {{
        window.brainNavigatorBridge.onRegionClicked(regionId);
        setStatus('Clicked: ' + regionId);
    }} else {{
        setStatus('Bridge not ready for click: ' + regionId);
    }}
}}
window.addEventListener('load', function() {{
    setTimeout(function() {{
        if (window.brainNavigatorBridge) {{
            setStatus('Bridge status: ready');
        }} else {{
            setStatus('Bridge status: waiting');
        }}
    }}, 300);
}});
</script>
</body>
</html>
"""


def create_brain_web_view_scaffold(
    config: BrainWebViewScaffoldConfig | None = None,
) -> BrainWebViewScaffoldBundle:
    """Create the QWebEngineView scaffold without replacing the fallback tab.

    Args:
        config: Optional scaffold configuration.

    Returns:
        Bundle containing the wrapper widget, web view, bridge, and HTML.
    """

    scaffold_config = config or BrainWebViewScaffoldConfig()
    region_targets = tuple(scaffold_config.region_targets or list_brain_region_targets())
    html = build_brain_web_view_scaffold_html(
        region_targets,
        object_name=scaffold_config.object_name,
    )

    QWidget = _qt_widgets_attr("QWidget")
    QVBoxLayout = _qt_widgets_attr("QVBoxLayout")
    QWebEngineView = _qt_web_engine_widgets_attr("QWebEngineView")

    widget = QWidget()
    widget.setObjectName("brainWebViewScaffoldWidget")
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)

    web_view = QWebEngineView()
    web_view.setObjectName("brainWebViewScaffoldView")
    layout.addWidget(web_view)

    bridge_bundle = create_brain_web_bridge(
        BrainWebBridgeConfig(
            object_name=scaffold_config.object_name,
            on_region_hovered=scaffold_config.on_region_hovered,
            on_region_clicked=scaffold_config.on_region_clicked,
        )
    )
    bridge_bundle.connect_to_page(web_view.page())
    web_view.setHtml(html)

    return BrainWebViewScaffoldBundle(
        widget=widget,
        web_view=web_view,
        bridge_bundle=bridge_bundle,
        html=html,
    )


def get_brain_web_view_scaffold_summary() -> BrainWebViewScaffoldSummary:
    """Return Box Architecture metadata for the WebView scaffold sub-box."""

    return BrainWebViewScaffoldSummary(
        box_id="brain_web_view_scaffold",
        contract_version="0.1",
        responsibility=(
            "Create a safe local QWebEngineView test surface that attaches the "
            "Brain Web Bridge and emits brain-region intent only."
        ),
        owner_paths=(
            "kanda_reasoner_app/reasoner_tools_gui_shell/brain_navigator/_web_view_scaffold.py",
        ),
        public_functions=(
            "build_brain_web_view_scaffold_html",
            "create_brain_web_view_scaffold",
            "get_brain_web_view_scaffold_summary",
        ),
        allowed_dependencies=(
            "brain_region_mapping.contract",
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
        implementation_state="qwebengine_scaffold_dry_run",
        visual_integration_state="not_wired_into_visible_brain_tab_yet",
    )
