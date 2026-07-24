# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/brain_navigator/assets/brain_visual_floating_window.py
"""Floating Remember Box data for the Neural Architecture brain visual.

This module is data-only. It defines the professional floating explanation
window payload shown when a Neural Architecture pulse marker is clicked. It does
not import GUI modules, tab widgets, the main window, or tab navigation logic.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json

__all__ = [
    "BrainFloatingRememberWindow",
    "BrainFloatingRememberWindowLayerSummary",
    "build_neural_architecture_floating_window_data_js",
    "get_neural_architecture_floating_window_summary",
    "list_neural_architecture_floating_windows",
]


@dataclass(frozen=True)
class BrainFloatingRememberWindow:
    """Describe one click-open floating Remember Box payload.

    Attributes:
        region_id: Stable brain-region identifier used by marker events.
        region_name: Human-readable neuroanatomical label.
        target_tab_label: Human-visible target module label.
        analogy_title: Short professional analogy title.
        purpose_text: Explanation of what the mapped module is for.
        action_state: Explicit state of the module-opening action.
        action_label: Text shown on the controlled action button.
    """

    region_id: str
    region_name: str
    target_tab_label: str
    analogy_title: str
    purpose_text: str
    action_state: str
    action_label: str


@dataclass(frozen=True)
class BrainFloatingRememberWindowLayerSummary:
    """Describe the floating Remember Box layer boundary."""

    box_id: str
    contract_version: str
    responsibility: str
    owner_paths: tuple[str, ...]
    window_count: int
    region_ids: tuple[str, ...]
    interaction_events: tuple[str, ...]
    implementation_state: str
    visual_integration_state: str


_FLOATING_WINDOWS: tuple[BrainFloatingRememberWindow, ...] = (
    BrainFloatingRememberWindow(
        "frontal_lobe",
        "Frontal lobe",
        "Audit Project",
        "Executive planning and architecture",
        "Opens the governed workspace for architecture, workflow, and engineering-safety review.",
        "Ready to open through the injected Tab Navigation Controller callback.",
        "Open module",
    ),
    BrainFloatingRememberWindow(
        "broca_area",
        "Broca Area (language area)",
        "Local AI",
        "Language production and clear answers",
        "Broca Area supports expressive language, like Local AI turns project context into clear explanations, answers, and implementation guidance.",
        "Ready to open through the injected Tab Navigation Controller callback.",
        "Open module",
    ),
    BrainFloatingRememberWindow(
        "parietal_lobe",
        "Parietal lobe",
        "Audit Project",
        "Integration and workflow coordination",
        "Opens Audit Project, where Workflow Review checks how tasks connect, execute, and remain consistent.",
        "Ready to open through the injected Tab Navigation Controller callback.",
        "Open module",
    ),
    BrainFloatingRememberWindow(
        "brainstem_midbrain",
        "Brainstem / Midbrain region",
        "Audit Project",
        "Survival layer and safety control",
        "Opens Audit Project, where Engineering Safety protects against unsafe architecture, private reach-in, and brittle shortcuts.",
        "Ready to open through the injected Tab Navigation Controller callback.",
        "Open module",
    ),
    BrainFloatingRememberWindow(
        "cerebellar_folia",
        "Cerebellar folia",
        "Docstring Assistant",
        "Fine detail and precision documentation",
        "Works at the detailed level of modules, classes, and functions to improve documentation clarity.",
        "Ready to open through the injected Tab Navigation Controller callback.",
        "Open module",
    ),
    BrainFloatingRememberWindow(
        "occipital_lobe",
        "Occipital lobe",
        "Show Project to AI",
        "Seeing the whole project",
        "Helps visualize the project layout, source organization, and structural relationships.",
        "Ready to open through the injected Tab Navigation Controller callback.",
        "Open module",
    ),
    BrainFloatingRememberWindow(
        "visual_association_cortex",
        "Visual association cortex",
        "Project Structure 3D",
        "Spatial integration and structural mapping",
        "Opens a read-only 3D map for exploring Project packages, modules, "
        "and relationships without changing source or architecture.",
        "Ready to open through the injected Tab Navigation Controller callback.",
        "Open module",
    ),
    BrainFloatingRememberWindow(
        "central_sulcus",
        "Central sulcus",
        "Web AI",
        "Boundary between project context and web reasoning",
        "Uses the active Project handoff while preserving the governed boundary between local source authority and external Web AI advice.",
        "Ready to open through the injected Tab Navigation Controller callback.",
        "Open module",
    ),
    BrainFloatingRememberWindow(
        "cerebellum",
        "Cerebellum",
        "Config AI",
        "Calibration and coordinated settings",
        "Centralizes gateway, model, endpoint, and credential settings so the AI tabs use one coordinated configuration owner.",
        "Ready to open through the injected Tab Navigation Controller callback.",
        "Open module",
    ),
    BrainFloatingRememberWindow(
        "temporal_lobe",
        "Temporal lobe",
        "Local AI",
        "Meaning, memory, and language",
        "Interprets project context and answers questions about code, structure, and implementation intent.",
        "Ready to open through the injected Tab Navigation Controller callback.",
        "Open module",
    ),
    BrainFloatingRememberWindow(
        "temporal_lobe_error_memory",
        "Temporal lobe Error Memory node",
        "Error Memory",
        "Failure memory and learned prevention",
        "Keeps project-specific lessons from failures so repeated mistakes can be recognized, corrected, and prevented.",
        "Ready to open through the injected Tab Navigation Controller callback.",
        "Open module",
    ),
    BrainFloatingRememberWindow(
        "hippocampus",
        "Hippocampus",
        "Freeze Feature After Update",
        "Memory consolidation and protected recall",
        "Stores validated project changes as durable project-local freeze memory so future AI work can recall and respect what is already protected.",
        "Ready to open through the injected Tab Navigation Controller callback.",
        "Open module",
    ),
    BrainFloatingRememberWindow(
        "lateral_sulcus",
        "Lateral sulcus / Sylvian fissure",
        "Exclusion Rules",
        "Functional boundary and separation rules",
        "Defines what should stay excluded from analysis, packaging, or AI context loading.",
        "Ready to open through the injected Tab Navigation Controller callback.",
        "Open module",
    ),
    BrainFloatingRememberWindow(
        "longitudinal_fissure",
        "Longitudinal fissure",
        "Prompt Library",
        "Central organization of knowledge",
        "Organizes reusable prompt knowledge into a structured system for future developer assistance.",
        "Ready to open through the injected Tab Navigation Controller callback.",
        "Open module",
    ),
)


def list_neural_architecture_floating_windows() -> tuple[BrainFloatingRememberWindow, ...]:
    """Return the floating Remember Box payloads in canonical marker order."""

    return _FLOATING_WINDOWS


def build_neural_architecture_floating_window_data_js() -> str:
    """Return JavaScript payload data for floating Remember Box windows."""

    payload = json.dumps(
        [asdict(window) for window in _FLOATING_WINDOWS],
        ensure_ascii=True,
        sort_keys=True,
    )
    return f"const NEURAL_ARCHITECTURE_FLOATING_WINDOWS = {payload};"


def get_neural_architecture_floating_window_summary() -> BrainFloatingRememberWindowLayerSummary:
    """Return the floating Remember Box layer summary."""

    windows = list_neural_architecture_floating_windows()
    return BrainFloatingRememberWindowLayerSummary(
        box_id="neural_architecture_floating_remember_window_layer",
        contract_version="0.2",
        responsibility=(
            "Define click-open floating Fancy Index payloads and visual behavior "
            "for Neural Architecture markers. The WebView emits intent only; "
            "Python opens modules through an injected stable-tab callback."
        ),
        owner_paths=(
            "kanda_reasoner_app/reasoner_tools_gui_shell/brain_navigator/assets/brain_visual_floating_window.py",
        ),
        window_count=len(windows),
        region_ids=tuple(window.region_id for window in windows),
        interaction_events=(
            "marker_left_click_opens_floating_fancy_index(region_id)",
            "open_module_button_emits_region_clicked(region_id)",
            "click_outside_or_escape_closes_floating_window",
        ),
        implementation_state="floating_fancy_index_with_controlled_open_module_action",
        visual_integration_state="visible_neural_architecture_with_fancy_index_open_module_action",
    )
