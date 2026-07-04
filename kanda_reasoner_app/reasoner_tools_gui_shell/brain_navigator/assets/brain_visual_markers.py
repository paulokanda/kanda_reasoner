# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/brain_navigator/assets/brain_visual_markers.py
"""Pulse marker contract for the Neural Architecture brain visual.

This module is data-only. It defines pulsing marker anchors for the visible
Neural Architecture brain. Marker positions include a fallback screen anchor and
an anatomical 3D anchor. The 3D anchor is snapped to the rendered mesh at runtime
so markers rotate with the brain instead of floating as fixed 2D overlays.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json

__all__ = [
    "BrainPulseMarker",
    "BrainPulseMarkerLayerSummary",
    "build_neural_architecture_marker_data_js",
    "get_neural_architecture_pulse_marker_summary",
    "list_neural_architecture_pulse_markers",
]


@dataclass(frozen=True)
class BrainPulseMarker:
    """Describe one visible pulsing marker on the brain preview.

    Attributes:
        region_id: Stable brain-region identifier emitted to the bridge.
        region_name: Human-readable neuroanatomical label.
        x_percent: Horizontal fallback marker anchor for no-Three.js fallback.
        y_percent: Vertical fallback marker anchor for no-Three.js fallback.
        anchor_x: Normalized right-left anatomical side coordinate.
        anchor_y: Normalized superior-inferior anatomical coordinate.
        anchor_z: Normalized anterior-posterior anatomical coordinate.
        surface_cloud: Mesh cloud used for surface snapping.
        preferred_side: Optional hemisphere side used when snapping to surface.
        anchor_lift: Small radial lift so DOM markers sit just above the mesh.
        default_state: Default visual behavior.
        hover_state: Hover visual behavior.
    """

    region_id: str
    region_name: str
    x_percent: float
    y_percent: float
    anchor_x: float
    anchor_y: float
    anchor_z: float
    surface_cloud: str = "telencephalon"
    preferred_side: int = 1
    anchor_lift: float = 1.026
    default_state: str = "dark_blue_slow_pulsing_circle"
    hover_state: str = "live_red_fast_pulsing_circle"


@dataclass(frozen=True)
class BrainPulseMarkerLayerSummary:
    """Describe the marker layer boundary."""

    box_id: str
    contract_version: str
    responsibility: str
    owner_paths: tuple[str, ...]
    marker_count: int
    region_ids: tuple[str, ...]
    interaction_events: tuple[str, ...]
    implementation_state: str
    visual_integration_state: str


# Model coordinate convention for the uploaded male_brain.glb visual:
# x = right-left hemisphere side, y = superior-inferior, z = anterior-posterior.
# This corrects the previous screen-percentage mistake where x was treated as
# the anterior-posterior axis. The anchors below are based on the original mesh
# landmark guide curves and are snapped to the rendered surface at runtime.
_PULSE_MARKERS: tuple[BrainPulseMarker, ...] = (
    # Frontal marker refined to a frontopolar position at the most anterior tip.
    # Frontal lobe moved anteriorly. The anterior depth offset equals the
    # original frontal-lobe to lateral-sulcus anterior-posterior distance:
    # 0.54 - 0.18 = 0.36, therefore 0.54 + 0.36 = 0.90.
    BrainPulseMarker("frontal_lobe", "Frontal lobe", 79.0, 40.0, 0.70, 0.24, 0.90),
    # Broca Area keeps the former frontal-lobe marker position.
    BrainPulseMarker("broca_area", "Broca Area (language area)", 68.0, 40.0, 0.70, 0.24, 0.54),
    # Parietal marker lowered from the crown into a more central superior cerebrum position.
    BrainPulseMarker("parietal_lobe", "Parietal lobe", 54.0, 42.0, 0.34, 0.26, -0.10),
    # Brainstem remains centered but is lowered into the middle of the trunk-like structure.
    BrainPulseMarker(
        "brainstem_midbrain",
        "Brainstem / Midbrain region",
        50.0,
        64.0,
        0.00,
        -0.36,
        -0.04,
        surface_cloud="midbrain",
        preferred_side=0,
        anchor_lift=1.018,
    ),
    # Cerebellar folia lowered so the marker sits clearly within the cerebellar mass.
    BrainPulseMarker(
        "cerebellar_folia",
        "Cerebellar folia",
        43.0,
        70.0,
        0.34,
        -0.44,
        -0.60,
        surface_cloud="cerebellum",
        anchor_lift=1.020,
    ),
    # Occipital marker lowered on the posterior cerebrum, above the cerebellum.
    BrainPulseMarker("occipital_lobe", "Occipital lobe", 39.0, 49.0, 0.28, -0.02, -0.60),
    BrainPulseMarker("central_sulcus", "Central sulcus", 56.0, 35.0, 0.34, 0.34, 0.12),
    # Cerebellum marker moved to the midline vermis area between the two hemispheric lobules.
    BrainPulseMarker(
        "cerebellum",
        "Cerebellum",
        42.0,
        68.0,
        0.00,
        -0.40,
        -0.62,
        surface_cloud="cerebellum",
        preferred_side=0,
        anchor_lift=1.020,
    ),
    # Temporal lobe marker moved below the lateral sulcus. The fallback
    # vertical distance from lateral sulcus to temporal lobe matches the
    # distance from frontal lobe to lateral sulcus: 46.5 - 40.0 = 6.5,
    # therefore 46.5 + 6.5 = 53.0.
    BrainPulseMarker("temporal_lobe", "Temporal lobe", 66.0, 53.0, 0.86, -0.30, 0.24),
    # Error Memory gets a second temporal-lobe marker. It is offset lower and
    # slightly posterior so both temporal-lobe circles remain selectable.
    BrainPulseMarker(
        "temporal_lobe_error_memory",
        "Temporal lobe Error Memory node",
        63.0,
        57.0,
        0.74,
        -0.36,
        0.12,
    ),
    # Hippocampus keeps the former temporal-lobe marker position.
    BrainPulseMarker("hippocampus", "Hippocampus", 58.0, 52.5, 0.54, -0.18, 0.06),
    BrainPulseMarker(
        "lateral_sulcus",
        "Lateral sulcus / Sylvian fissure",
        57.0,
        46.5,
        0.66,
        -0.03,
        0.18,
    ),
    BrainPulseMarker(
        "longitudinal_fissure",
        "Longitudinal fissure",
        51.0,
        22.0,
        0.00,
        0.62,
        0.08,
        preferred_side=0,
    ),
)


def list_neural_architecture_pulse_markers() -> tuple[BrainPulseMarker, ...]:
    """Return the canonical marker anchors for the brain preview."""

    return _PULSE_MARKERS


def build_neural_architecture_marker_data_js() -> str:
    """Return JavaScript marker data used by the preview template."""

    marker_dicts = [asdict(marker) for marker in _PULSE_MARKERS]
    payload = json.dumps(marker_dicts, ensure_ascii=True, sort_keys=True)
    return f"const NEURAL_ARCHITECTURE_PULSE_MARKERS = {payload};"


def get_neural_architecture_pulse_marker_summary() -> BrainPulseMarkerLayerSummary:
    """Return the pulse marker layer summary."""

    markers = list_neural_architecture_pulse_markers()
    return BrainPulseMarkerLayerSummary(
        box_id="neural_architecture_pulse_marker_layer",
        contract_version="0.2",
        responsibility=(
            "Define mesh-anchored pulsing markers for the visible Neural "
            "Architecture brain. Anchors are snapped to mesh surfaces and "
            "projected every frame so they rotate with the model."
        ),
        owner_paths=(
            "kanda_reasoner_app/reasoner_tools_gui_shell/brain_navigator/assets/brain_visual_markers.py",
        ),
        marker_count=len(markers),
        region_ids=tuple(marker.region_id for marker in markers),
        interaction_events=(
            "onRegionHovered(region_id)",
            "onRegionClicked(region_id)",
        ),
        implementation_state="mesh_anchored_pulse_marker_layer",
        visual_integration_state="visible_default_neural_architecture_tab",
    )
