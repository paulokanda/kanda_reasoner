"""Internal Qt WebChannel bridge for the Brain Navigator box.

This module isolates the future QWebChannel and QObject wiring for the
rotating brain view. Importing the module is safe without PySide6 because Qt
classes are loaded only when ``create_brain_web_bridge`` is called.

The bridge emits brain-region intent only. It does not switch tabs, import the
main window, inspect the tab registry, or mutate other GUI boxes.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from importlib import import_module
from typing import Any, Final

BRAIN_WEB_BRIDGE_OBJECT_NAME: Final[str] = "bridge"
UNKNOWN_BRAIN_REGION_ID: Final[str] = "unknown_region"


__all__: list[str] = []

RegionCallback = Callable[[str], object]


@dataclass(frozen=True)
class BrainWebBridgeConfig:
    """Configuration used when creating the Qt WebChannel bridge.

    Attributes:
        object_name: Name registered into the QWebChannel object map.
        on_region_hovered: Optional adapter called after a hover signal emits.
        on_region_clicked: Optional adapter called after a click signal emits.
    """

    object_name: str = BRAIN_WEB_BRIDGE_OBJECT_NAME
    on_region_hovered: RegionCallback | None = None
    on_region_clicked: RegionCallback | None = None


@dataclass(frozen=True)
class BrainWebBridgeBundle:
    """Created Qt bridge objects returned by the bridge factory.

    Attributes:
        bridge: QObject instance exposed to JavaScript.
        channel: QWebChannel instance containing the registered bridge.
        object_name: Name used by JavaScript to retrieve the bridge object.
    """

    bridge: object
    channel: object
    object_name: str

    def connect_to_page(self, page: object) -> None:
        """Attach the QWebChannel to a QWebEnginePage-like object.

        Args:
            page: Object exposing ``setWebChannel(channel)``.

        Raises:
            AttributeError: If the page object does not expose setWebChannel.
        """

        page.setWebChannel(self.channel)


@dataclass(frozen=True)
class BrainWebBridgeSummary:
    """Describe the Brain Web Bridge sub-box boundary."""

    box_id: str
    contract_version: str
    responsibility: str
    owner_paths: tuple[str, ...]
    public_functions: tuple[str, ...]
    emitted_signals: tuple[str, ...]
    javascript_slots: tuple[str, ...]
    forbidden_dependencies: tuple[str, ...]
    implementation_state: str


def normalize_brain_region_id(region_id: object) -> str:
    """Normalize a JavaScript region identifier into a safe string.

    Args:
        region_id: Raw value received from JavaScript.

    Returns:
        Stripped string value, or ``unknown_region`` when empty.
    """

    normalized = str(region_id or "").strip()
    if not normalized:
        return UNKNOWN_BRAIN_REGION_ID
    return normalized


def build_brain_web_channel_bootstrap_script(
    object_name: str = BRAIN_WEB_BRIDGE_OBJECT_NAME,
) -> str:
    """Return the JavaScript bootstrap snippet for QWebChannel registration.

    Args:
        object_name: Registered channel object name.

    Returns:
        JavaScript snippet that assigns ``window.brainNavigatorBridge``.
    """

    safe_object_name = str(object_name or BRAIN_WEB_BRIDGE_OBJECT_NAME).strip()
    if not safe_object_name:
        safe_object_name = BRAIN_WEB_BRIDGE_OBJECT_NAME

    return (
        "let brainNavigatorBridge = null;\n"
        "try {\n"
        "    if (typeof QWebChannel !== 'undefined' "
        "&& typeof qt !== 'undefined') {\n"
        "        new QWebChannel(qt.webChannelTransport, function(channel) {\n"
        f"            brainNavigatorBridge = channel.objects.{safe_object_name};\n"
        "            window.brainNavigatorBridge = brainNavigatorBridge;\n"
        "        });\n"
        "    }\n"
        "} catch (err) {\n"
        "    console.warn('Brain Navigator bridge unavailable:', err);\n"
        "}\n"
    )


def _qt_core_attr(name: str) -> Any:
    """Return a PySide6.QtCore attribute through a lazy import."""

    return getattr(import_module("PySide6.QtCore"), name)


def _qt_web_channel_attr(name: str) -> Any:
    """Return a PySide6.QtWebChannel attribute through a lazy import."""

    return getattr(import_module("PySide6.QtWebChannel"), name)


def create_brain_web_bridge(
    config: BrainWebBridgeConfig | None = None,
) -> BrainWebBridgeBundle:
    """Create a QWebChannel bridge for Brain Navigator web content.

    The returned bridge exposes these JavaScript-callable slots:

    ``onRegionHovered(region_id)``
    ``onRegionClicked(region_id)``
    ``onBrainClicked()`` for legacy no-region demo pages

    Args:
        config: Optional bridge configuration and callbacks.

    Returns:
        BrainWebBridgeBundle containing the QObject bridge and QWebChannel.
    """

    bridge_config = config or BrainWebBridgeConfig()
    object_name = normalize_brain_region_id(bridge_config.object_name)
    if object_name == UNKNOWN_BRAIN_REGION_ID:
        object_name = BRAIN_WEB_BRIDGE_OBJECT_NAME

    QObject = _qt_core_attr("QObject")
    Signal = _qt_core_attr("Signal")
    Slot = _qt_core_attr("Slot")
    QWebChannel = _qt_web_channel_attr("QWebChannel")

    class BrainWebBridge(QObject):  # type: ignore[misc, valid-type]
        """QObject exposed to JavaScript through QWebChannel."""

        regionHovered = Signal(str)
        regionClicked = Signal(str)

        def __init__(self) -> None:
            """Create the Qt bridge object."""

            super().__init__()

        @Slot(str)
        def onRegionHovered(self, region_id: str) -> None:
            """Emit a brain-region hover intent from JavaScript."""

            normalized_region_id = normalize_brain_region_id(region_id)
            self.regionHovered.emit(normalized_region_id)
            if bridge_config.on_region_hovered is not None:
                bridge_config.on_region_hovered(normalized_region_id)

        @Slot(str)
        def onRegionClicked(self, region_id: str) -> None:
            """Emit a brain-region click intent from JavaScript."""

            normalized_region_id = normalize_brain_region_id(region_id)
            self.regionClicked.emit(normalized_region_id)
            if bridge_config.on_region_clicked is not None:
                bridge_config.on_region_clicked(normalized_region_id)

        @Slot()
        def onBrainClicked(self) -> None:
            """Handle legacy demo clicks that do not provide a region ID."""

            self.onRegionClicked(UNKNOWN_BRAIN_REGION_ID)

    bridge = BrainWebBridge()
    channel = QWebChannel()
    channel.registerObject(object_name, bridge)

    return BrainWebBridgeBundle(
        bridge=bridge,
        channel=channel,
        object_name=object_name,
    )


def get_brain_web_bridge_summary() -> BrainWebBridgeSummary:
    """Return Box Architecture metadata for the Brain Web Bridge sub-box."""

    return BrainWebBridgeSummary(
        box_id="brain_web_bridge",
        contract_version="0.1",
        responsibility=(
            "Expose a QWebChannel QObject bridge that converts JavaScript "
            "hover and click calls into brain-region intent signals."
        ),
        owner_paths=(
            "kanda_reasoner_app/reasoner_tools_gui_shell/brain_navigator/_web_bridge.py",
        ),
        public_functions=(
            "create_brain_web_bridge",
            "build_brain_web_channel_bootstrap_script",
            "normalize_brain_region_id",
            "get_brain_web_bridge_summary",
        ),
        emitted_signals=(
            "regionHovered(region_id)",
            "regionClicked(region_id)",
        ),
        javascript_slots=(
            "onRegionHovered(region_id)",
            "onRegionClicked(region_id)",
            "onBrainClicked()",
        ),
        forbidden_dependencies=(
            "main_window",
            "tool_specs",
            "tab_navigation_controller",
            "direct_tab_index_switching",
            "other_tab_internals",
        ),
        implementation_state="qt_web_channel_bridge_scaffold",
    )
