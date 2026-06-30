# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/brain_navigator/contract.py
"""Public contract for the Brain Navigator box.

This module keeps import-time side effects low and avoids static PySide6,
QWebEngine, tab registry, and main-window imports. The visible fallback index
widget is created lazily through the public contract so tests can import this
module without GUI dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass


__all__ = [
    "BRAIN_NAVIGATOR_BOX_ID",
    "BRAIN_NAVIGATOR_TAB_ID",
    "BRAIN_NAVIGATOR_TAB_LABEL",
    "BrainNavigatorContractSummary",
    "build_brain_web_channel_bootstrap_script",
    "build_neural_architecture_asset_preview_html",
    "build_neural_architecture_marker_data_js",
    "list_neural_architecture_floating_windows",
    "get_neural_architecture_floating_window_summary",
    "build_neural_architecture_floating_window_data_js",
    "get_neural_architecture_pulse_marker_summary",
    "list_neural_architecture_pulse_markers",
    "get_neural_architecture_preview_summary",
    "create_visible_neural_architecture_brain_tab",
    "get_visible_neural_architecture_tab_summary",
    "open_mapped_tab_by_region_id",
    "create_neural_architecture_preview",
    "build_neural_architecture_preview_html",
    "build_brain_web_view_scaffold_html",
    "create_brain_navigator_tab",
    "create_brain_web_bridge",
    "create_brain_web_view_scaffold",
    "get_brain_navigator_contract_summary",
    "get_brain_navigator_freeze_snapshot",
    "get_neural_architecture_visual_spec",
    "get_brain_mesh_data_summary",
    "get_brain_mesh_data_js",
    "get_brain_web_bridge_summary",
    "get_brain_web_view_scaffold_summary",
    "normalize_brain_region_id",
]

BRAIN_NAVIGATOR_BOX_ID = "brain_navigator"
BRAIN_NAVIGATOR_TAB_ID = "brain_navigator"
BRAIN_NAVIGATOR_TAB_LABEL = "Brain Navigator"


@dataclass(frozen=True)
class BrainNavigatorContractSummary:
    """Describe the public boundary of the Brain Navigator scaffold.

    Attributes:
        box_id: Stable Box Architecture identifier for this feature box.
        tab_id: Stable tab identifier planned for registry integration.
        tab_label: Human-visible tab label planned for the first tab.
        responsibility: Single responsibility statement for the box.
        owner_paths: Project-relative paths owned by this box.
        public_outputs: Event names that the future GUI implementation may emit.
        forbidden_dependencies: Boxes or modules this box must not reach into.
        implementation_state: Current scaffold state.
    """

    box_id: str
    tab_id: str
    tab_label: str
    responsibility: str
    owner_paths: tuple[str, ...]
    public_outputs: tuple[str, ...]
    forbidden_dependencies: tuple[str, ...]
    implementation_state: str


def get_brain_navigator_contract_summary() -> BrainNavigatorContractSummary:
    """Return the Brain Navigator scaffold contract summary.

    Returns:
        Immutable summary of the box boundary that focused tests and future
        registry wiring can inspect without importing GUI internals.
    """

    return BrainNavigatorContractSummary(
        box_id=BRAIN_NAVIGATOR_BOX_ID,
        tab_id=BRAIN_NAVIGATOR_TAB_ID,
        tab_label=BRAIN_NAVIGATOR_TAB_LABEL,
        responsibility=(
            "Own the first-tab interactive brain homepage and emit user intent "
            "when a brain region is hovered or clicked."
        ),
        owner_paths=(
            "kanda_reasoner_app/reasoner_tools_gui_shell/brain_navigator/",
        ),
        public_outputs=(
            "brain_region_hovered(region_id)",
            "brain_region_clicked(region_id)",
        ),
        forbidden_dependencies=(
            "main_window",
            "tool_specs",
            "engineering_safety",
            "prompt_library",
            "workflow_review",
            "architecture_review",
            "other_tab_internals",
        ),
        implementation_state="visible_neural_architecture_brain_with_fancy_index_open_module_action",
    )



def get_brain_navigator_freeze_snapshot() -> object:
    """Return the final Brain Navigator freeze snapshot lazily."""

    from ._freeze_snapshot import (
        get_brain_navigator_freeze_snapshot as _get_snapshot,
    )

    return _get_snapshot()


def create_brain_web_bridge(*args: object, **kwargs: object) -> object:
    """Create the internal Qt WebChannel bridge lazily.

    The bridge object emits brain-region hover and click intent. It does not
    navigate tabs directly and does not import MainWindow or tab internals.

    Args:
        *args: Forwarded to the bridge factory.
        **kwargs: Forwarded to the bridge factory.

    Returns:
        BrainWebBridgeBundle-like object containing the QObject bridge and
        QWebChannel.
    """

    from ._web_bridge import create_brain_web_bridge as _create_bridge

    return _create_bridge(*args, **kwargs)


def build_brain_web_channel_bootstrap_script(*args: object, **kwargs: object) -> str:
    """Build the JavaScript QWebChannel bootstrap snippet lazily.

    Args:
        *args: Forwarded to the bridge script builder.
        **kwargs: Forwarded to the bridge script builder.

    Returns:
        JavaScript bridge bootstrap text.
    """

    from ._web_bridge import build_brain_web_channel_bootstrap_script as _build_script

    return _build_script(*args, **kwargs)


def normalize_brain_region_id(*args: object, **kwargs: object) -> str:
    """Normalize a JavaScript brain-region ID lazily through the bridge box."""

    from ._web_bridge import normalize_brain_region_id as _normalize

    return _normalize(*args, **kwargs)


def get_brain_web_bridge_summary() -> object:
    """Return the Brain Web Bridge sub-box summary lazily."""

    from ._web_bridge import get_brain_web_bridge_summary as _get_summary

    return _get_summary()


def build_brain_web_view_scaffold_html(*args: object, **kwargs: object) -> str:
    """Build the safe local Brain WebView scaffold HTML lazily."""

    from ._web_view_scaffold import (
        build_brain_web_view_scaffold_html as _build_html,
    )

    return _build_html(*args, **kwargs)


def create_brain_web_view_scaffold(*args: object, **kwargs: object) -> object:
    """Create the internal Brain WebView scaffold lazily.

    The scaffold is not wired into the visible first tab by this patch. It
    creates a QWebEngineView test surface and attaches the Brain Web Bridge.
    """

    from ._web_view_scaffold import create_brain_web_view_scaffold as _create

    return _create(*args, **kwargs)


def get_brain_web_view_scaffold_summary() -> object:
    """Return the Brain WebView scaffold sub-box summary lazily."""

    from ._web_view_scaffold import (
        get_brain_web_view_scaffold_summary as _get_summary,
    )

    return _get_summary()



def get_brain_mesh_data_summary() -> object:
    """Return the extracted brain mesh data summary lazily."""

    from .assets.brain_mesh_data import get_brain_mesh_data_summary as _get_summary

    return _get_summary()


def get_brain_mesh_data_js() -> str:
    """Return the extracted inert brain mesh JavaScript lazily."""

    from .assets.brain_mesh_data import get_brain_mesh_data_js as _get_js

    return _get_js()


def get_neural_architecture_visual_spec() -> object:
    """Return the frozen Neural Architecture visual requirements lazily."""

    from .assets.brain_visual_spec import (
        get_neural_architecture_visual_spec as _get_spec,
    )

    return _get_spec()


def build_neural_architecture_asset_preview_html() -> str:
    """Build inert Neural Architecture asset preview HTML lazily.

    The preview is not wired into the visible first tab by Patch 8.
    """

    from .assets.brain_visual_template import (
        build_neural_architecture_asset_preview_html as _build_html,
    )

    return _build_html()



def list_neural_architecture_pulse_markers() -> object:
    """Return the responsive pulse marker anchors lazily."""

    from .assets.brain_visual_markers import (
        list_neural_architecture_pulse_markers as _list_markers,
    )

    return _list_markers()


def build_neural_architecture_marker_data_js() -> str:
    """Build JavaScript pulse marker data lazily."""

    from .assets.brain_visual_markers import (
        build_neural_architecture_marker_data_js as _build_marker_js,
    )

    return _build_marker_js()


def get_neural_architecture_pulse_marker_summary() -> object:
    """Return the pulse marker layer summary lazily."""

    from .assets.brain_visual_markers import (
        get_neural_architecture_pulse_marker_summary as _get_summary,
    )

    return _get_summary()


def list_neural_architecture_floating_windows() -> object:
    """Return the floating Remember Box payloads lazily."""

    from .assets.brain_visual_floating_window import (
        list_neural_architecture_floating_windows as _list_windows,
    )

    return _list_windows()


def build_neural_architecture_floating_window_data_js() -> str:
    """Build JavaScript floating Remember Box data lazily."""

    from .assets.brain_visual_floating_window import (
        build_neural_architecture_floating_window_data_js as _build_window_js,
    )

    return _build_window_js()


def get_neural_architecture_floating_window_summary() -> object:
    """Return the floating Remember Box layer summary lazily."""

    from .assets.brain_visual_floating_window import (
        get_neural_architecture_floating_window_summary as _get_summary,
    )

    return _get_summary()



def build_neural_architecture_preview_html(*args: object, **kwargs: object) -> str:
    """Build the isolated Neural Architecture preview HTML lazily."""

    from ._neural_architecture_preview import (
        build_neural_architecture_preview_html as _build_html,
    )

    return _build_html(*args, **kwargs)


def create_neural_architecture_preview(*args: object, **kwargs: object) -> object:
    """Create the isolated Neural Architecture WebView preview lazily.

    The preview is not wired into the visible first tab by Patch 9.
    """

    from ._neural_architecture_preview import (
        create_neural_architecture_preview as _create_preview,
    )

    return _create_preview(*args, **kwargs)


def get_neural_architecture_preview_summary() -> object:
    """Return the isolated Neural Architecture preview summary lazily."""

    from ._neural_architecture_preview import (
        get_neural_architecture_preview_summary as _get_summary,
    )

    return _get_summary()



def create_visible_neural_architecture_brain_tab(*args: object, **kwargs: object) -> object:
    """Create the visible Neural Architecture brain tab lazily."""

    from ._visible_neural_architecture_tab import (
        create_visible_neural_architecture_brain_tab as _create_visible,
    )

    return _create_visible(*args, **kwargs)


def open_mapped_tab_by_region_id(*args: object, **kwargs: object) -> object:
    """Resolve a brain region and request stable-tab navigation lazily."""

    from ._visible_neural_architecture_tab import (
        open_mapped_tab_by_region_id as _open_mapped_tab,
    )

    return _open_mapped_tab(*args, **kwargs)


def get_visible_neural_architecture_tab_summary() -> object:
    """Return the visible Neural Architecture tab summary lazily."""

    from ._visible_neural_architecture_tab import (
        get_visible_neural_architecture_tab_summary as _get_summary,
    )

    return _get_summary()

def create_brain_navigator_tab(*args: object, **kwargs: object) -> object:
    """Create the visible Brain Navigator tab widget.

    The default visible tab is now the Neural Architecture WebView. The safe
    fallback index is still available and is used only when the WebView or brain
    visual cannot be created.

    Args:
        *args: Forwarded to the visible brain tab factory.
        **kwargs: Forwarded to the visible brain tab factory.

    Returns:
        QWidget-like visible Neural Architecture brain tab, or the fallback
        index widget if WebEngine creation fails.
    """

    from ._visible_neural_architecture_tab import (
        create_visible_neural_architecture_brain_tab as _create_visible_tab,
    )

    return _create_visible_tab(*args, **kwargs)
