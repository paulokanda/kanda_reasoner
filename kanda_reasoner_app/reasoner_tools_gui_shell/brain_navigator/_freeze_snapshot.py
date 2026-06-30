# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/brain_navigator/_freeze_snapshot.py
"""Final freeze snapshot metadata for the Brain Navigator flow.

This module is intentionally data-only. It records the behavior that was
validated manually after the Neural Architecture brain became the visible first
Brain Navigator tab. It does not create Qt widgets, switch tabs, inspect the tab
registry, or import any other GUI box internals.
"""

from __future__ import annotations

from dataclasses import dataclass

__all__: list[str] = []


@dataclass(frozen=True)
class BrainNavigatorFreezeSnapshot:
    """Describe the frozen Brain Navigator interaction chain.

    Attributes:
        box_id: Stable Brain Navigator box identifier.
        contract_version: Snapshot contract version.
        frozen_flow: Human-readable steps in the frozen GUI flow.
        visual_guarantees: Visual and interaction guarantees kept by the patch.
        navigation_guarantees: Navigation boundary guarantees.
        fallback_behavior: Safe fallback behavior if WebEngine fails.
        owner_paths: Project paths owned by this snapshot.
        focused_tests: Tests that protect the final flow.
        forbidden_dependencies: Dependencies that remain forbidden.
        freeze_state: Current final freeze state.
    """

    box_id: str
    contract_version: str
    frozen_flow: tuple[str, ...]
    visual_guarantees: tuple[str, ...]
    navigation_guarantees: tuple[str, ...]
    fallback_behavior: str
    owner_paths: tuple[str, ...]
    focused_tests: tuple[str, ...]
    forbidden_dependencies: tuple[str, ...]
    freeze_state: str


def get_brain_navigator_freeze_snapshot() -> BrainNavigatorFreezeSnapshot:
    """Return the final Brain Navigator freeze snapshot.

    Returns:
        Immutable metadata for the validated Neural Architecture Brain
        Navigator flow.
    """

    return BrainNavigatorFreezeSnapshot(
        box_id="brain_navigator",
        contract_version="1.0",
        frozen_flow=(
            "normal_app_opens_visible_neural_architecture_brain_tab",
            "brain_mesh_uses_original_colors_and_seventy_percent_fit_scale",
            "pulse_markers_are_mesh_anchored_and_projected_each_frame",
            "marker_click_opens_floating_fancy_index_only",
            "open_module_button_emits_region_intent_through_qwebchannel",
            "python_adapter_resolves_region_with_public_mapping_contract",
            "mapped_tab_opens_through_injected_stable_tab_callback",
        ),
        visual_guarantees=(
            "title_footer_and_floating_index_remain_html_overlays",
            "markers_spin_with_the_brain_mesh",
            "floating_index_closes_on_outside_click_or_escape",
            "safe_fallback_index_remains_available_on_webengine_failure",
        ),
        navigation_guarantees=(
            "webview_never_uses_numeric_tab_indexes",
            "brain_navigator_never_imports_main_window_or_tool_specs",
            "open_module_uses_injected_open_tab_by_id_callback",
            "qwebchannel_bridge_bundle_is_kept_alive_on_qt_widgets",
        ),
        fallback_behavior=(
            "The Neural Architecture WebView is the default Brain Navigator tab; "
            "the Qt fallback index is created only when WebEngine or visual "
            "creation fails."
        ),
        owner_paths=(
            "kanda_reasoner_app/reasoner_tools_gui_shell/brain_navigator/",
        ),
        focused_tests=(
            "tests/test_brain_navigator_final_freeze_snapshot.py",
            "tests/test_brain_navigator_open_module_bridge_lifetime.py",
            "tests/test_brain_navigator_open_module_button_delivery.py",
            "tests/test_brain_navigator_fancy_index_open_module_action.py",
            "tests/test_brain_navigator_mesh_anchor_marker_refinement.py",
        ),
        forbidden_dependencies=(
            "main_window",
            "tool_specs",
            "direct_tab_index_switching",
            "other_tab_internals",
        ),
        freeze_state="final_brain_navigator_interaction_chain_frozen",
    )
