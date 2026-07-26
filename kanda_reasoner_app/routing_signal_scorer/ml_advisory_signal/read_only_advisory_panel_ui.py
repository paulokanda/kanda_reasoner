# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/read_only_advisory_panel_ui.py
"""Phase 8 read-only advisory panel UI implementation.

Renderer-neutral view-model builder only. This module may transform a Phase 7
read-only advisory surface envelope into a bounded in-memory panel view model.
It does not render UI, activate a runtime panel, mutate screens, wire runtime
telemetry surfaces, call the router, call an advisor, execute adapters, call
providers, persist data, influence routes, or grant ML route authority.
"""

from __future__ import annotations


__all__ = [
    'build_phase8_read_only_advisory_panel_ui_probe',
    'build_read_only_advisory_panel_view_model',
    'ReadOnlyAdvisoryPanelSection',
    'ReadOnlyAdvisoryPanelUIPolicy',
    'ReadOnlyAdvisoryPanelUIState',
    'ReadOnlyAdvisoryPanelViewModel',
    'ReadOnlyPanelRenderMode',
    'ReadOnlyPanelSectionKind',
]
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple

from ._read_only_advisory_panel_ui_invariants import (
    validate_panel_section,
    validate_ui_policy,
    validate_view_model,
)
from ._read_only_advisory_panel_ui_status import build_section_specs

from .read_only_advisory_surface_wiring import (
    ReadOnlyAdvisorySurfaceWiringEnvelope,
    ReadOnlySurfaceAttachmentState,
    build_phase7_read_only_surface_wiring_probe,
)
from .guarded_runtime_display import GuardedRuntimeAdvisoryDisplayPayload


FEATURE_ID = "rss_ml_adv_phase8_read_only_advisory_panel_ui_implementation_v1"
SOURCE_REVIEW_FEATURE_ID = (
    "rss_ml_adv_phase8_read_only_advisory_panel_ui_contract_result_review_gate_v1"
)


class ReadOnlyPanelRenderMode(str, Enum):
    """Renderer-neutral panel states."""

    VIEW_MODEL_READY = "VIEW_MODEL_READY"
    DISABLED_NOOP = "DISABLED_NOOP"
    FAIL_OPEN_NO_SURFACE = "FAIL_OPEN_NO_SURFACE"


class ReadOnlyPanelSectionKind(str, Enum):
    """Allowed bounded section kinds for the read-only panel model."""

    ADVISORY_ROLE_LABEL = "advisory_role_label"
    CANONICAL_ROUTE_UNCHANGED_LABEL = "canonical_route_unchanged_label"
    NO_ROUTE_AUTHORITY_LABEL = "no_route_authority_label"
    ADVISORY_STATUS = "advisory_status"
    BOUNDARY_STATUS = "boundary_status"
    CONFIDENCE_BAND = "confidence_band"
    CONFIDENCE_NOT_CORRECTNESS_LABEL = "confidence_not_correctness_label"
    REASON_CODES_BOUNDED = "reason_codes_bounded"
    GUARDRAIL_STATE = "guardrail_state"
    DISABLED_NOOP_STATE = "disabled_noop_state"
    NON_TRAINING_FEEDBACK_SLOT = "non_training_feedback_slot"


class ReadOnlyAdvisoryPanelUIState(str, Enum):
    """High-level panel view-model state."""

    READY_READ_ONLY = "READY_READ_ONLY"
    DISABLED_NOOP = "DISABLED_NOOP"
    FAIL_OPEN_NO_SURFACE = "FAIL_OPEN_NO_SURFACE"


DEFAULT_ALLOWED_SECTION_KINDS: Tuple[ReadOnlyPanelSectionKind, ...] = (
    ReadOnlyPanelSectionKind.ADVISORY_ROLE_LABEL,
    ReadOnlyPanelSectionKind.CANONICAL_ROUTE_UNCHANGED_LABEL,
    ReadOnlyPanelSectionKind.NO_ROUTE_AUTHORITY_LABEL,
    ReadOnlyPanelSectionKind.ADVISORY_STATUS,
    ReadOnlyPanelSectionKind.BOUNDARY_STATUS,
    ReadOnlyPanelSectionKind.CONFIDENCE_BAND,
    ReadOnlyPanelSectionKind.CONFIDENCE_NOT_CORRECTNESS_LABEL,
    ReadOnlyPanelSectionKind.REASON_CODES_BOUNDED,
    ReadOnlyPanelSectionKind.GUARDRAIL_STATE,
    ReadOnlyPanelSectionKind.DISABLED_NOOP_STATE,
    ReadOnlyPanelSectionKind.NON_TRAINING_FEEDBACK_SLOT,
)


@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelUIPolicy:
    """Policy for safe renderer-neutral panel view-model construction."""

    panel_id: str
    panel_label: str
    source_review_feature_id: str
    allowed_section_kinds: Tuple[ReadOnlyPanelSectionKind, ...] = DEFAULT_ALLOWED_SECTION_KINDS
    enabled: bool = True
    max_sections: int = 11
    read_only: bool = True
    telemetry_only: bool = True
    renderer_neutral: bool = True
    in_memory_only: bool = True
    bounded: bool = True
    fail_open: bool = True
    removable_noop: bool = True
    route_invariant: bool = True
    final_selection_invisible: bool = True
    non_authoritative: bool = True
    consumes_phase7_surface_envelope_only: bool = True
    section_values_are_bounded_status_only: bool = True
    require_advisory_role_label: bool = True
    require_canonical_route_unchanged_label: bool = True
    require_no_route_authority_label: bool = True
    require_confidence_not_correctness_label: bool = True
    non_training_feedback_only: bool = True
    route_override_button_enabled: bool = False
    use_ml_route_button_enabled: bool = False
    best_route_claim_enabled: bool = False
    prompt_ranking_enabled: bool = False
    free_text_route_advice_enabled: bool = False
    free_text_explanations_enabled: bool = False
    runtime_panel_activation_enabled: bool = False
    runtime_ui_mutation_enabled: bool = False
    runtime_telemetry_surface_wired: bool = False
    route_influence_enabled: bool = False
    route_authority_enabled: bool = False
    router_calls_enabled: bool = False
    advisor_calls_enabled: bool = False
    adapter_execution_enabled: bool = False
    provider_calls_enabled: bool = False
    persistence_enabled: bool = False
    prompt_loading_enabled: bool = False
    prompt_registry_mutation_enabled: bool = False
    prompt_library_read_enabled: bool = False
    freeze_memory_read_enabled: bool = False
    freeze_memory_write_enabled: bool = False
    router_canon_read_enabled: bool = False
    runtime_shadow_mode_enabled: bool = False
    training_enabled: bool = False
    calibration_enabled: bool = False
    model_improvement_enabled: bool = False
    runtime_pilot_behavior_enabled: bool = False
    runtime_copilot_decision_behavior_enabled: bool = False

    def __post_init__(self) -> None:
        """Validate the immutable UI policy contract."""
        validate_ui_policy(
            self,
            source_review_feature_id=SOURCE_REVIEW_FEATURE_ID,
            section_kind_type=ReadOnlyPanelSectionKind,
        )


@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelSection:
    """Single bounded renderer-neutral panel section."""

    kind: ReadOnlyPanelSectionKind
    label: str
    value: str
    severity: str = "info"
    read_only: bool = True
    action_enabled: bool = False
    route_authority_enabled: bool = False
    route_influence_enabled: bool = False
    free_text_route_advice: bool = False

    def __post_init__(self) -> None:
        """Validate one immutable bounded panel section."""
        validate_panel_section(
            self,
            section_kind_type=ReadOnlyPanelSectionKind,
        )


@dataclass(frozen=True)
class ReadOnlyAdvisoryPanelViewModel:
    """Renderer-neutral, immutable read-only advisory panel view model."""

    feature_id: str
    panel_id: str
    panel_label: str
    state: ReadOnlyAdvisoryPanelUIState
    render_mode: ReadOnlyPanelRenderMode
    source_surface_id: Optional[str]
    source_surface_label: Optional[str]
    source_attachment_state: Optional[ReadOnlySurfaceAttachmentState]
    canonical_result_id: Optional[str]
    canonical_dispatch_label: Optional[str]
    final_selection_hash: Optional[str]
    sections: Tuple[ReadOnlyAdvisoryPanelSection, ...]
    failure_state_codes: Tuple[str, ...]
    non_training_feedback_slot_enabled: bool
    read_only: bool = True
    telemetry_only: bool = True
    renderer_neutral: bool = True
    in_memory_only: bool = True
    bounded: bool = True
    fail_open: bool = True
    removable_noop: bool = True
    route_invariant: bool = True
    final_selection_invisible: bool = True
    non_authoritative: bool = True
    runtime_panel_activation_enabled: bool = False
    runtime_ui_mutation_enabled: bool = False
    runtime_telemetry_surface_wired: bool = False
    route_influence_enabled: bool = False
    route_authority_enabled: bool = False
    route_override_button_enabled: bool = False
    use_ml_route_button_enabled: bool = False
    prompt_ranking_enabled: bool = False
    free_text_route_advice_enabled: bool = False
    free_text_explanations_enabled: bool = False
    runtime_copilot_decision_behavior_enabled: bool = False

    def __post_init__(self) -> None:
        """Validate the immutable renderer-neutral view model."""
        validate_view_model(
            self,
            feature_id=FEATURE_ID,
            state_type=ReadOnlyAdvisoryPanelUIState,
            render_mode_type=ReadOnlyPanelRenderMode,
            attachment_state_type=ReadOnlySurfaceAttachmentState,
            section_type=ReadOnlyAdvisoryPanelSection,
        )


def build_read_only_advisory_panel_view_model(
    policy: ReadOnlyAdvisoryPanelUIPolicy,
    surface_envelope: object | None,
) -> ReadOnlyAdvisoryPanelViewModel:
    """Build a renderer-neutral read-only advisory panel view model.

    The function only consumes an already-built Phase 7 surface envelope. It
    fails open if the envelope is missing or invalid and never calls router,
    advisor, adapters, providers, persistence, or UI APIs.
    """

    if not isinstance(policy, ReadOnlyAdvisoryPanelUIPolicy):
        raise TypeError("policy must be ReadOnlyAdvisoryPanelUIPolicy")
    if not policy.enabled:
        return _build_noop_view_model(policy, ReadOnlyAdvisoryPanelUIState.DISABLED_NOOP, ReadOnlyPanelRenderMode.DISABLED_NOOP, ("disabled_noop",))
    if not isinstance(surface_envelope, ReadOnlyAdvisorySurfaceWiringEnvelope):
        return _build_noop_view_model(policy, ReadOnlyAdvisoryPanelUIState.FAIL_OPEN_NO_SURFACE, ReadOnlyPanelRenderMode.FAIL_OPEN_NO_SURFACE, ("missing_or_invalid_surface_envelope",))

    sections = _build_sections(policy, surface_envelope)
    return ReadOnlyAdvisoryPanelViewModel(
        feature_id=FEATURE_ID,
        panel_id=policy.panel_id,
        panel_label=policy.panel_label,
        state=ReadOnlyAdvisoryPanelUIState.READY_READ_ONLY,
        render_mode=ReadOnlyPanelRenderMode.VIEW_MODEL_READY,
        source_surface_id=surface_envelope.surface_id,
        source_surface_label=surface_envelope.surface_label,
        source_attachment_state=surface_envelope.attachment_state,
        canonical_result_id=surface_envelope.canonical_snapshot_after.canonical_result_id,
        canonical_dispatch_label=surface_envelope.canonical_snapshot_after.canonical_dispatch_label,
        final_selection_hash=surface_envelope.canonical_snapshot_after.final_selection_hash,
        sections=sections[: policy.max_sections],
        failure_state_codes=surface_envelope.failure_state_codes,
        non_training_feedback_slot_enabled=surface_envelope.non_training_feedback_slot_enabled,
    )


def build_phase8_read_only_advisory_panel_ui_probe() -> ReadOnlyAdvisoryPanelViewModel:
    """Build a safe in-memory panel view-model probe for validation tests."""

    policy = ReadOnlyAdvisoryPanelUIPolicy(
        panel_id="phase8_read_only_advisory_panel_view_model",
        panel_label="phase8_read_only_advisory_panel_ui_v1",
        source_review_feature_id=SOURCE_REVIEW_FEATURE_ID,
    )
    surface = build_phase7_read_only_surface_wiring_probe()
    return build_read_only_advisory_panel_view_model(policy, surface)


def _build_sections(
    policy: ReadOnlyAdvisoryPanelUIPolicy,
    surface: ReadOnlyAdvisorySurfaceWiringEnvelope,
) -> Tuple[ReadOnlyAdvisoryPanelSection, ...]:
    """Build bounded sections from pure status projection specifications."""
    specs = build_section_specs(
        surface,
        kinds=ReadOnlyPanelSectionKind,
        attached_read_only_state=ReadOnlySurfaceAttachmentState.ATTACHED_READ_ONLY,
        disabled_noop_state_value=ReadOnlySurfaceAttachmentState.DISABLED_NOOP,
    )
    sections = []
    allowed = set(policy.allowed_section_kinds)
    for kind, label, value, severity_value in specs:
        if kind not in allowed:
            continue
        sections.append(
            ReadOnlyAdvisoryPanelSection(
                kind=kind,
                label=label,
                value=value,
                severity=severity_value,
            )
        )
    return tuple(sections)

def _build_noop_view_model(
    policy: ReadOnlyAdvisoryPanelUIPolicy,
    state: ReadOnlyAdvisoryPanelUIState,
    render_mode: ReadOnlyPanelRenderMode,
    failure_codes: Tuple[str, ...],
) -> ReadOnlyAdvisoryPanelViewModel:
    """Support build noop view model behavior.
    
    Parameters
    ----------
    policy : ReadOnlyAdvisoryPanelUIPolicy
        The policy value.
    state : ReadOnlyAdvisoryPanelUIState
        The state value.
    render_mode : ReadOnlyPanelRenderMode
        The render mode value.
    failure_codes : Tuple[str, ...]
        The failure codes value.
    
    Returns
    -------
    ReadOnlyAdvisoryPanelViewModel
        The read only advisory panel view model result.
    """
    
    sections = (
        ReadOnlyAdvisoryPanelSection(
            kind=ReadOnlyPanelSectionKind.ADVISORY_ROLE_LABEL,
            label="Advisory role",
            value="Telemetry unavailable; governed router remains final selector.",
        ),
        ReadOnlyAdvisoryPanelSection(
            kind=ReadOnlyPanelSectionKind.CANONICAL_ROUTE_UNCHANGED_LABEL,
            label="Canonical route",
            value="Unchanged.",
        ),
        ReadOnlyAdvisoryPanelSection(
            kind=ReadOnlyPanelSectionKind.NO_ROUTE_AUTHORITY_LABEL,
            label="Route authority",
            value="No ML route authority.",
        ),
    )
    return ReadOnlyAdvisoryPanelViewModel(
        feature_id=FEATURE_ID,
        panel_id=policy.panel_id,
        panel_label=policy.panel_label,
        state=state,
        render_mode=render_mode,
        source_surface_id=None,
        source_surface_label=None,
        source_attachment_state=None,
        canonical_result_id=None,
        canonical_dispatch_label=None,
        final_selection_hash=None,
        sections=sections[: policy.max_sections],
        failure_state_codes=failure_codes,
        non_training_feedback_slot_enabled=False,
    )


