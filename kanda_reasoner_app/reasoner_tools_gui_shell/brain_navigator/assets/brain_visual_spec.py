"""Visual contract for the Brain Navigator neural architecture asset.

This module is data-only. It freezes the planned title, footer, marker behavior,
and responsive resizing requirements for the future rotating brain view.
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = [
    "BrainVisualSpec",
    "get_neural_architecture_visual_spec",
]

TITLE_LINES = (
    "Neural Architecture",
    "of",
    "Knowledge and Architecture Navigator for Developer Assistance (KANDA)",
)
FOOTER_TEXT = "What is the airspeed velocity of an unladen swallow?"
VISUAL_MODES = (
    "fallback_index",
    "webview_scaffold",
    "neural_architecture_brain",
)
RESPONSIVE_REQUIREMENTS = (
    "fill_available_tab_space",
    "preserve_aspect_ratio",
    "avoid_brain_clipping",
    "update_renderer_size_on_window_resize",
    "update_camera_aspect_on_window_resize",
    "recalculate_projected_marker_positions_on_resize",
    "keep_title_footer_and_floating_window_usable",
    "render_brain_about_30_percent_smaller_for_complete_fit",
    "restore_original_mesh_colors_after_axis_correction",
    "treat_model_x_as_left_right_and_z_as_anterior_posterior",
    "snap_pulse_markers_to_mesh_surface_and_project_each_frame",
)
MARKER_BEHAVIOR = (
    "dark_blue_slow_pulsing_circle_default",
    "ripple_waves_from_each_circle",
    "live_red_fast_pulse_on_hover",
    "hover_label_only_when_pointer_is_over_marker",
    "left_click_emits_region_id_to_bridge",
    "left_click_opens_floating_explanation_window",
    "click_outside_or_escape_closes_floating_window",
)


@dataclass(frozen=True)
class BrainVisualSpec:
    """Describe the future Brain Navigator visual contract.

    Attributes:
        box_id: Stable identifier for the visual asset sub-box.
        title_lines: Exact title lines to render over the brain.
        footer_text: Exact bottom footer text.
        visual_modes: Supported internal visual modes.
        responsive_requirements: Hard responsive layout requirements.
        marker_behavior: Required marker interaction behavior.
        default_mode_after_final_validation: Planned default mode after manual GUI freeze.
        current_integration_state: Current gated integration state.
    """

    box_id: str
    title_lines: tuple[str, ...]
    footer_text: str
    visual_modes: tuple[str, ...]
    responsive_requirements: tuple[str, ...]
    marker_behavior: tuple[str, ...]
    default_mode_after_final_validation: str
    current_integration_state: str


def get_neural_architecture_visual_spec() -> BrainVisualSpec:
    """Return the frozen visual requirements for the future brain view."""

    return BrainVisualSpec(
        box_id="brain_neural_architecture_visual_asset",
        title_lines=TITLE_LINES,
        footer_text=FOOTER_TEXT,
        visual_modes=VISUAL_MODES,
        responsive_requirements=RESPONSIVE_REQUIREMENTS,
        marker_behavior=MARKER_BEHAVIOR,
        default_mode_after_final_validation="neural_architecture_brain",
        current_integration_state="visible_neural_architecture_with_restored_colors_and_mesh_anchored_markers",
    )
