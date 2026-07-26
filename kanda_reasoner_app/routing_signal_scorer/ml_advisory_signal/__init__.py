# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/__init__.py
"""Phase 1a ML advisory signal boundary contracts.

This package is intentionally non-runtime and non-authoritative. It
exposes only data contracts, null/mock advisors, and boundary guards.
"""

from .advisor_interface import AdvisorProtocol
from .boundary_guard import assert_phase1a_environment_allowed
from .fixture_catalog_contract import (
    OfflineFixtureCatalog,
    OfflineFixtureCatalogEntry,
    OfflineFixtureIntent,
    catalog_fixtures,
)
from .contract import (
    AdvisoryFlag,
    AdvisoryGroupObservation,
    AdvisoryInput,
    AdvisoryOutput,
    AdvisoryReasonCode,
    BoundaryStatus,
    build_abstain_output,
)
from .mock_advisor import MockAdvisor
from .null_advisor import NullAdvisor
from .offline_evaluation_contract import (
    OfflineEvaluationFixture,
    OfflineEvaluationResult,
    OfflineEvaluationStatus,
    OfflineEvaluationSummary,
)
from .offline_evaluation_harness import run_offline_evaluation
from .offline_fixture_catalog import build_phase3_synthetic_fixture_catalog
from .output_firewall import validate_advisory_output

from .advisor_comparison_contract import (
    OfflineAdvisorComparisonParticipant,
    OfflineAdvisorComparisonReport,
    OfflineAdvisorComparisonStatus,
    compare_offline_advisor_summaries,
)
from .offline_advisor_comparison import run_phase4_null_vs_mock_offline_comparison

from .real_adapter_boundary_contract import (
    RealAdapterBoundaryDecision,
    RealAdapterBoundaryStatus,
    RealAdapterDescriptor,
    evaluate_real_adapter_boundary,
)
from .offline_real_adapter_boundary import build_phase5_offline_real_adapter_boundary_probe

from .real_adapter_candidate_contract import (
    RealAdapterCandidateDecision,
    RealAdapterCandidateDescriptor,
    RealAdapterCandidateStatus,
    evaluate_real_adapter_candidate,
)
from .offline_real_adapter_candidate import build_phase5_offline_candidate_probe

from .guarded_runtime_display_contract import (
    GuardedRuntimeAdvisoryDisplayDecision,
    GuardedRuntimeAdvisoryDisplayPolicy,
    GuardedRuntimeAdvisoryDisplayStatus,
    evaluate_guarded_runtime_display_contract,
)
from .offline_guarded_runtime_display import build_phase6_guarded_display_contract_probe

from .guarded_runtime_display import (
    GuardedRuntimeAdvisoryDisplayPayload,
    GuardedRuntimeAdvisoryDisplaySurfacePolicy,
    build_guarded_runtime_advisory_display_payload,
    build_phase6_guarded_runtime_display_payload_probe,
)

__all__ = [
    "build_read_only_advisory_surface_wiring_envelope",
    "build_phase7_read_only_surface_wiring_probe",
    "ReadOnlySurfaceAttachmentState",
    "ReadOnlyAdvisorySurfaceWiringPolicy",
    "ReadOnlyAdvisorySurfaceWiringEnvelope",
    "CanonicalDispatchSnapshot",
    "AdvisorProtocol",
    "AdvisoryFlag",
    "AdvisoryGroupObservation",
    "AdvisoryInput",
    "AdvisoryOutput",
    "AdvisoryReasonCode",
    "BoundaryStatus",
    "MockAdvisor",
    "OfflineFixtureCatalog",
    "OfflineFixtureCatalogEntry",
    "OfflineFixtureIntent",
    "build_phase3_synthetic_fixture_catalog",
    "catalog_fixtures",
    "NullAdvisor",
    "OfflineEvaluationFixture",
    "OfflineEvaluationResult",
    "OfflineEvaluationStatus",
    "OfflineEvaluationSummary",
    "assert_phase1a_environment_allowed",
    "build_abstain_output",
    "run_offline_evaluation",
    "OfflineAdvisorComparisonParticipant",
    "OfflineAdvisorComparisonReport",
    "OfflineAdvisorComparisonStatus",
    "compare_offline_advisor_summaries",
    "run_phase4_null_vs_mock_offline_comparison",
    "RealAdapterBoundaryDecision",
    "RealAdapterBoundaryStatus",
    "RealAdapterDescriptor",
    "evaluate_real_adapter_boundary",
    "build_phase5_offline_real_adapter_boundary_probe",
    "RealAdapterCandidateDecision",
    "RealAdapterCandidateDescriptor",
    "RealAdapterCandidateStatus",
    "evaluate_real_adapter_candidate",
    "build_phase5_offline_candidate_probe",
    "GuardedRuntimeAdvisoryDisplayDecision",
    "GuardedRuntimeAdvisoryDisplayPolicy",
    "GuardedRuntimeAdvisoryDisplayStatus",
    "evaluate_guarded_runtime_display_contract",
    "build_phase6_guarded_display_contract_probe",
    "build_phase6_guarded_runtime_display_payload_probe",
    "build_guarded_runtime_advisory_display_payload",
    "GuardedRuntimeAdvisoryDisplaySurfacePolicy",
    "GuardedRuntimeAdvisoryDisplayPayload",
    "validate_advisory_output",
    "WebBookInformedAdvisorySurfaceGain",
    "WebBookInformedSurfaceWiringAudit",
    "WebBookInformedSurfaceWiringContract",
    "WebBookInformedSurfaceWiringDecision",
    "build_phase7_web_book_informed_surface_wiring_contract",
    "evaluate_phase7_web_book_advisory_surface_wiring_request",
    "GuardedAdvisorySurfaceWiringContract",
    "GuardedAdvisorySurfaceWiringDecision",
    "GuardedAdvisorySurfaceWiringPolicy",
    "SurfaceVisibilityMode",
    "build_phase7_guarded_advisory_surface_wiring_contract",
    "evaluate_phase7_guarded_advisory_surface_wiring_request",
    "ReadOnlyAdvisoryPanelUIContractDecision",
    "ReadOnlyAdvisoryPanelUIContractPolicy",
    "ReadOnlyPanelContractStatus",
    "ReadOnlyPanelVisibilityMode",
    "build_phase8_read_only_advisory_panel_ui_contract",
    "evaluate_phase8_read_only_advisory_panel_ui_request",
    "DEFAULT_ALLOWED_SECTION_KINDS",
    "ReadOnlyAdvisoryPanelSection",
    "ReadOnlyAdvisoryPanelUIState",
    "ReadOnlyAdvisoryPanelUIPolicy",
    "ReadOnlyAdvisoryPanelViewModel",
    "ReadOnlyPanelRenderMode",
    "ReadOnlyPanelSectionKind",
    "build_phase8_read_only_advisory_panel_ui_probe",
    "build_read_only_advisory_panel_view_model",
    "ReadOnlyAdvisoryPanelRuntimeActivationDecision",
    "ReadOnlyAdvisoryPanelRuntimeActivationPolicy",
    "ReadOnlyPanelRuntimeActivationMode",
    "ReadOnlyPanelRuntimeActivationStatus",
    "build_phase9_read_only_advisory_panel_runtime_activation_contract",
    "build_phase9_read_only_panel_runtime_activation_contract_probe",
    "evaluate_phase9_read_only_advisory_panel_runtime_activation_request",
    "ReadOnlyAdvisoryPanelRuntimeActivationEnvelope",
    "ReadOnlyAdvisoryPanelRuntimeActivationPolicy",
    "ReadOnlyAdvisoryPanelRuntimeActivationEnvelopePolicy",
    "ReadOnlyPanelRuntimeActivationEnvelopeState",
    "build_phase9_read_only_panel_runtime_activation_implementation_probe",
    "build_read_only_advisory_panel_runtime_activation_envelope",
]


from .web_book_informed_surface_wiring_contract import (
    WebBookInformedAdvisorySurfaceGain,
    WebBookInformedSurfaceWiringAudit,
    WebBookInformedSurfaceWiringContract,
    WebBookInformedSurfaceWiringDecision,
    build_phase7_web_book_informed_surface_wiring_contract,
    evaluate_phase7_web_book_advisory_surface_wiring_request,
)


from .guarded_advisory_surface_wiring_contract import (
    GuardedAdvisorySurfaceWiringContract,
    GuardedAdvisorySurfaceWiringDecision,
    GuardedAdvisorySurfaceWiringPolicy,
    SurfaceVisibilityMode,
    build_phase7_guarded_advisory_surface_wiring_contract,
    evaluate_phase7_guarded_advisory_surface_wiring_request,
)

from .read_only_advisory_surface_wiring import (
    CanonicalDispatchSnapshot,
    ReadOnlyAdvisorySurfaceWiringEnvelope,
    ReadOnlyAdvisorySurfaceWiringPolicy,
    ReadOnlySurfaceAttachmentState,
    build_phase7_read_only_surface_wiring_probe,
    build_read_only_advisory_surface_wiring_envelope,
)


from .read_only_advisory_panel_ui_contract import (
    ReadOnlyAdvisoryPanelUIContractDecision,
    ReadOnlyAdvisoryPanelUIContractPolicy,
    ReadOnlyPanelContractStatus,
    ReadOnlyPanelVisibilityMode,
    build_phase8_read_only_advisory_panel_ui_contract,
    evaluate_phase8_read_only_advisory_panel_ui_request,
)


from .read_only_advisory_panel_ui import (
    DEFAULT_ALLOWED_SECTION_KINDS,
    ReadOnlyAdvisoryPanelSection,
    ReadOnlyAdvisoryPanelUIState,
    ReadOnlyAdvisoryPanelUIPolicy,
    ReadOnlyAdvisoryPanelViewModel,
    ReadOnlyPanelRenderMode,
    ReadOnlyPanelSectionKind,
    build_phase8_read_only_advisory_panel_ui_probe,
    build_read_only_advisory_panel_view_model,
)


from .read_only_advisory_panel_runtime_activation_contract import (
    ReadOnlyAdvisoryPanelRuntimeActivationDecision,
    ReadOnlyAdvisoryPanelRuntimeActivationPolicy,
    ReadOnlyPanelRuntimeActivationMode,
    ReadOnlyPanelRuntimeActivationStatus,
    build_phase9_read_only_advisory_panel_runtime_activation_contract,
    build_phase9_read_only_panel_runtime_activation_contract_probe,
    evaluate_phase9_read_only_advisory_panel_runtime_activation_request,
)


from .read_only_advisory_panel_runtime_activation import (
    ReadOnlyAdvisoryPanelRuntimeActivationEnvelope,
    ReadOnlyAdvisoryPanelRuntimeActivationPolicy as ReadOnlyAdvisoryPanelRuntimeActivationEnvelopePolicy,
    ReadOnlyPanelRuntimeActivationEnvelopeState,
    build_phase9_read_only_panel_runtime_activation_implementation_probe,
    build_read_only_advisory_panel_runtime_activation_envelope,
)

from .read_only_advisory_panel_renderer_mount_contract import (
    FORBIDDEN_RENDERER_MOUNT_CAPABILITIES,
    REQUIRED_RENDERER_MOUNT_CONTRACT_LABELS,
    ReadOnlyAdvisoryPanelRendererMountDecision,
    ReadOnlyAdvisoryPanelRendererMountPolicy,
    ReadOnlyPanelRendererMountMode,
    ReadOnlyPanelRendererMountStatus,
    build_phase10_read_only_advisory_panel_renderer_mount_contract,
    build_phase10_read_only_panel_renderer_mount_contract_probe,
    evaluate_phase10_read_only_advisory_panel_renderer_mount_request,
)

from .read_only_advisory_panel_renderer_mount import (
    ReadOnlyAdvisoryPanelRendererMountDescriptor,
    ReadOnlyAdvisoryPanelRendererMountPolicy as ReadOnlyAdvisoryPanelRendererMountImplementationPolicy,
    ReadOnlyAdvisoryPanelRenderedSection,
    ReadOnlyPanelRendererMountImplementationState,
    build_phase10_read_only_panel_renderer_mount_implementation_probe,
    build_read_only_advisory_panel_renderer_mount_descriptor,
)

__all__.extend([
    "ReadOnlyAdvisoryPanelRendererMountDescriptor",
    "ReadOnlyAdvisoryPanelRendererMountImplementationPolicy",
    "ReadOnlyAdvisoryPanelRenderedSection",
    "ReadOnlyPanelRendererMountImplementationState",
    "build_phase10_read_only_panel_renderer_mount_implementation_probe",
    "build_read_only_advisory_panel_renderer_mount_descriptor",
])

from .read_only_advisory_panel_host_binding_contract import (
    FORBIDDEN_HOST_BINDING_CAPABILITIES,
    REQUIRED_HOST_BINDING_CONTRACT_LABELS,
    ReadOnlyAdvisoryPanelHostBindingDecision,
    ReadOnlyAdvisoryPanelHostBindingPolicy,
    ReadOnlyPanelHostBindingMode,
    ReadOnlyPanelHostBindingStatus,
    build_phase11_read_only_advisory_panel_host_binding_contract,
    build_phase11_read_only_panel_host_binding_contract_probe,
    evaluate_phase11_read_only_advisory_panel_host_binding_request,
)

__all__.extend([
    "FORBIDDEN_HOST_BINDING_CAPABILITIES",
    "REQUIRED_HOST_BINDING_CONTRACT_LABELS",
    "ReadOnlyAdvisoryPanelHostBindingDecision",
    "ReadOnlyAdvisoryPanelHostBindingPolicy",
    "ReadOnlyPanelHostBindingMode",
    "ReadOnlyPanelHostBindingStatus",
    "build_phase11_read_only_advisory_panel_host_binding_contract",
    "build_phase11_read_only_panel_host_binding_contract_probe",
    "evaluate_phase11_read_only_advisory_panel_host_binding_request",
])

from .read_only_advisory_panel_host_binding import (
    ReadOnlyAdvisoryPanelHostBindingDescriptor,
    ReadOnlyAdvisoryPanelHostBindingImplementationPolicy,
    ReadOnlyAdvisoryPanelHostBoundSection,
    ReadOnlyPanelHostBindingImplementationState,
    build_phase11_read_only_panel_host_binding_implementation_probe,
    build_read_only_advisory_panel_host_binding_descriptor,
)

__all__.extend([
    "ReadOnlyAdvisoryPanelHostBindingDescriptor",
    "ReadOnlyAdvisoryPanelHostBindingImplementationPolicy",
    "ReadOnlyAdvisoryPanelHostBoundSection",
    "ReadOnlyPanelHostBindingImplementationState",
    "build_phase11_read_only_panel_host_binding_implementation_probe",
    "build_read_only_advisory_panel_host_binding_descriptor",
])


from .read_only_advisory_panel_runtime_app_host_visibility_contract import (
    FORBIDDEN_RUNTIME_APP_HOST_VISIBILITY_CAPABILITIES,
    REQUIRED_RUNTIME_APP_HOST_VISIBILITY_CONTRACT_LABELS,
    ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDecision,
    ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityPolicy,
    ReadOnlyPanelRuntimeAppHostVisibilityMode,
    ReadOnlyPanelRuntimeAppHostVisibilityStatus,
    build_phase12_read_only_advisory_panel_runtime_app_host_visibility_contract,
    build_phase12_read_only_panel_runtime_app_host_visibility_contract_probe,
    evaluate_phase12_read_only_advisory_panel_runtime_app_host_visibility_request,
)

__all__.extend([
    "FORBIDDEN_RUNTIME_APP_HOST_VISIBILITY_CAPABILITIES",
    "REQUIRED_RUNTIME_APP_HOST_VISIBILITY_CONTRACT_LABELS",
    "ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDecision",
    "ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityPolicy",
    "ReadOnlyPanelRuntimeAppHostVisibilityMode",
    "ReadOnlyPanelRuntimeAppHostVisibilityStatus",
    "build_phase12_read_only_advisory_panel_runtime_app_host_visibility_contract",
    "build_phase12_read_only_panel_runtime_app_host_visibility_contract_probe",
    "evaluate_phase12_read_only_advisory_panel_runtime_app_host_visibility_request",
])

from .read_only_advisory_panel_runtime_app_host_visibility import (
    ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDescriptor,
    ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityImplementationPolicy,
    ReadOnlyAdvisoryPanelRuntimeVisibleSection,
    ReadOnlyPanelRuntimeAppHostVisibilityImplementationState,
    build_phase12_read_only_panel_runtime_app_host_visibility_implementation_probe,
    build_read_only_advisory_panel_runtime_app_host_visibility_descriptor,
)

__all__.extend([
    "ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityDescriptor",
    "ReadOnlyAdvisoryPanelRuntimeAppHostVisibilityImplementationPolicy",
    "ReadOnlyAdvisoryPanelRuntimeVisibleSection",
    "ReadOnlyPanelRuntimeAppHostVisibilityImplementationState",
    "build_phase12_read_only_panel_runtime_app_host_visibility_implementation_probe",
    "build_read_only_advisory_panel_runtime_app_host_visibility_descriptor",
])

from .read_only_advisory_panel_passive_visibility_activation_contract import (
    FORBIDDEN_PASSIVE_VISIBILITY_ACTIVATION_CAPABILITIES,
    REQUIRED_PASSIVE_VISIBILITY_ACTIVATION_CONTRACT_LABELS,
    ReadOnlyAdvisoryPanelPassiveVisibilityActivationDecision,
    ReadOnlyAdvisoryPanelPassiveVisibilityActivationPolicy,
    ReadOnlyPanelPassiveVisibilityActivationMode,
    ReadOnlyPanelPassiveVisibilityActivationStatus,
    build_phase13_read_only_advisory_panel_passive_visibility_activation_contract,
    build_phase13_read_only_panel_passive_visibility_activation_contract_probe,
    evaluate_phase13_read_only_advisory_panel_passive_visibility_activation_request,
)

__all__.extend([
    "FORBIDDEN_PASSIVE_VISIBILITY_ACTIVATION_CAPABILITIES",
    "REQUIRED_PASSIVE_VISIBILITY_ACTIVATION_CONTRACT_LABELS",
    "ReadOnlyAdvisoryPanelPassiveVisibilityActivationDecision",
    "ReadOnlyAdvisoryPanelPassiveVisibilityActivationPolicy",
    "ReadOnlyPanelPassiveVisibilityActivationMode",
    "ReadOnlyPanelPassiveVisibilityActivationStatus",
    "build_phase13_read_only_advisory_panel_passive_visibility_activation_contract",
    "build_phase13_read_only_panel_passive_visibility_activation_contract_probe",
    "evaluate_phase13_read_only_advisory_panel_passive_visibility_activation_request",
])

from .read_only_advisory_panel_passive_visibility_activation import (
    ReadOnlyAdvisoryPanelPassiveVisibilityActivationDescriptor,
    ReadOnlyAdvisoryPanelPassiveVisibilityActivationImplementationPolicy,
    ReadOnlyAdvisoryPanelPassiveVisibilitySlot,
    ReadOnlyPanelPassiveVisibilityActivationImplementationState,
    build_phase13_read_only_panel_passive_visibility_activation_implementation_probe,
    build_read_only_advisory_panel_passive_visibility_activation_descriptor,
)

__all__.extend([
    "ReadOnlyAdvisoryPanelPassiveVisibilityActivationDescriptor",
    "ReadOnlyAdvisoryPanelPassiveVisibilityActivationImplementationPolicy",
    "ReadOnlyAdvisoryPanelPassiveVisibilitySlot",
    "ReadOnlyPanelPassiveVisibilityActivationImplementationState",
    "build_phase13_read_only_panel_passive_visibility_activation_implementation_probe",
    "build_read_only_advisory_panel_passive_visibility_activation_descriptor",
])
