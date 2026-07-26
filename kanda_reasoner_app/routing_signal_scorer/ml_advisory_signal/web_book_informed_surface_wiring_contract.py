# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/web_book_informed_surface_wiring_contract.py
"""Web-and-book-informed Phase 7 advisory surface wiring research contract.

Contract only. It adds no runtime wiring, no UI panel, no provider calls, no
adapter execution, no route authority, and no router prompt logic changes.
"""

from __future__ import annotations


__all__ = [
    'build_phase7_web_book_informed_surface_wiring_contract',
    'evaluate_phase7_web_book_advisory_surface_wiring_request',
    'WebBookInformedAdvisorySurfaceGain',
    'WebBookInformedSurfaceWiringAudit',
    'WebBookInformedSurfaceWiringContract',
    'WebBookInformedSurfaceWiringDecision',
]
from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class WebBookInformedAdvisorySurfaceGain:
    """A source-backed gain accepted into the project logic flux."""

    code: str
    source_family: str
    logic_gain: str
    future_gate: str
    allowed_now: bool


@dataclass(frozen=True)
class WebBookInformedSurfaceWiringAudit:
    """External-source audit summary without adding runtime dependencies."""

    web_sources: Tuple[str, ...]
    book_sources: Tuple[str, ...]
    rejected_or_deferred: Tuple[str, ...]


@dataclass(frozen=True)
class WebBookInformedSurfaceWiringContract:
    """Research-to-logic contract for future advisory-surface wiring."""

    feature_id: str
    reviewed_feature_id: str
    audit: WebBookInformedSurfaceWiringAudit
    gains: Tuple[WebBookInformedAdvisorySurfaceGain, ...]
    automatic_use_rule: str
    visible_panel_rule: str
    route_effect_rule: str
    direct_route_authority_allowed: bool
    runtime_panel_wired: bool
    provider_calls_allowed: bool
    router_final_selection_modified: bool
    persistence_allowed: bool
    critical_boundary_error_budget: int

    def gain_codes(self) -> Tuple[str, ...]:
        """Support gain codes behavior.
        
        Returns
        -------
        Tuple[str, ...]
            The tuple result.
        """
        
        return tuple(gain.code for gain in self.gains)

    def source_counts(self) -> Tuple[int, int]:
        """Support source counts behavior.
        
        Returns
        -------
        Tuple[int, int]
            The tuple result.
        """
        
        return (len(self.audit.web_sources), len(self.audit.book_sources))


@dataclass(frozen=True)
class WebBookInformedSurfaceWiringDecision:
    """Decision for a proposed next-step wiring request."""

    may_auto_use_after_router: bool
    may_show_visible_panel: bool
    may_affect_route_choice: bool
    required_next_contract: str
    reason: str


FEATURE_ID = "rss_ml_adv_phase7_web_book_informed_advisory_surface_wiring_research_flux_v1"
REVIEWED_FEATURE_ID = "rss_ml_adv_phase6_guarded_runtime_advisory_display_completion_handoff_v1"

WEB_SOURCES = (
    "NIST AI Risk Management Framework and Generative AI Profile",
    "OWASP Top 10 for LLM and GenAI Applications",
    "Google People + AI Guidebook",
    "Microsoft HAX Toolkit Guidelines for Human-AI Interaction",
    "OpenAI Evals and Guardrails documentation",
    "UK NCSC prompt injection confused-deputy guidance",
    "Anthropic effective-agents guardrail/evals design notes",
)

BOOK_SOURCES = (
    "AI Engineering: Building Applications with Foundation Models - Chip Huyen",
    "Designing Large Language Model Applications - Suhas Pai",
    "Designing Machine Learning Systems - Chip Huyen",
    "Reliable Machine Learning - Cathy Chen, Niall Richard Murphy, Kranti Parisa, Todd Underwood, D. Sculley",
    "Human-Centered AI - Ben Shneiderman",
)


def build_phase7_web_book_informed_surface_wiring_contract() -> WebBookInformedSurfaceWiringContract:
    """Build accepted source-informed gates before Phase 7 wiring."""

    gains = (
        WebBookInformedAdvisorySurfaceGain(
            code="authority_separation_final_router_invariant",
            source_family="NIST governance + Human-Centered AI",
            logic_gain="Keep the governed deterministic router as final selector while advisory display remains telemetry.",
            future_gate="Future wiring must assert route invariance before and after display payload construction.",
            allowed_now=True,
        ),
        WebBookInformedAdvisorySurfaceGain(
            code="confusable_deputy_privilege_denial",
            source_family="NCSC prompt-injection + OWASP LLM Top 10",
            logic_gain="Treat advisory/model output as an untrusted confusable deputy and deny privileges.",
            future_gate="No advisory output may call tools, read privileged stores, mutate prompts, or write decisions.",
            allowed_now=True,
        ),
        WebBookInformedAdvisorySurfaceGain(
            code="guardrail_adjacency_before_side_effects",
            source_family="OpenAI guardrails + Anthropic agent design",
            logic_gain="Place guard checks next to any side-effect boundary, not only at workflow entry.",
            future_gate="If future UI/router wiring writes state or triggers tools, guard checks must surround that boundary.",
            allowed_now=True,
        ),
        WebBookInformedAdvisorySurfaceGain(
            code="structured_typed_payload_no_free_text_route_advice",
            source_family="OWASP insecure output handling + Designing LLM Applications",
            logic_gain="Expose typed status/reason fields instead of free-form text that downstream code could misinterpret.",
            future_gate="Future panel payload may expose bounded status/reason codes only, not route recommendations.",
            allowed_now=True,
        ),
        WebBookInformedAdvisorySurfaceGain(
            code="explicit_uncertainty_status_role_and_scope_labeling",
            source_family="Google PAIR + Microsoft HAX + Human-Centered AI",
            logic_gain="Reduce overtrust by labeling uncertainty, abstention, blocked status, scope, and non-authoritative role.",
            future_gate="Visible panel must state canonical router unchanged and ML telemetry-only status.",
            allowed_now=True,
        ),
        WebBookInformedAdvisorySurfaceGain(
            code="user_control_disable_noop_and_non_training_feedback",
            source_family="Microsoft HAX + Human-Centered AI",
            logic_gain="Make the surface removable and controllable; feedback must not train or mutate routing.",
            future_gate="Panel wiring must include disable/no-op behavior and non-training feedback slots.",
            allowed_now=True,
        ),
        WebBookInformedAdvisorySurfaceGain(
            code="eval_first_gates_for_code_payload_model_and_ui_changes",
            source_family="OpenAI evals + AI Engineering",
            logic_gain="Treat evals as a product gate for future code, payload, model, and UI changes.",
            future_gate="Every future wiring step must include route-invariance, fail-open, authority-separation, and payload-schema tests.",
            allowed_now=True,
        ),
        WebBookInformedAdvisorySurfaceGain(
            code="slo_error_budget_and_regression_budget_for_advisory_surface",
            source_family="Reliable Machine Learning + SRE practice",
            logic_gain="Use explicit reliability/error budgets for advisory behavior before any activation.",
            future_gate="Future UI wiring must define zero authority-regression budget and bounded display failure behavior.",
            allowed_now=True,
        ),
        WebBookInformedAdvisorySurfaceGain(
            code="monitoring_readiness_without_persistence_or_privileged_reads",
            source_family="Reliable Machine Learning + Designing ML Systems",
            logic_gain="Design monitorable outcomes without adding persistent logs or privileged reads in this phase.",
            future_gate="Any later monitoring must be privacy-bounded, opt-in/explicitly contracted, and non-routing.",
            allowed_now=True,
        ),
        WebBookInformedAdvisorySurfaceGain(
            code="latency_cost_and_availability_budget_before_provider_activation",
            source_family="AI Engineering + LLM application engineering",
            logic_gain="Provider-backed activation requires latency, cost, availability, and fallback budgets first.",
            future_gate="No provider call may be enabled until a separate budgeted adapter contract exists.",
            allowed_now=True,
        ),
        WebBookInformedAdvisorySurfaceGain(
            code="rollback_and_kill_switch_as_first_class_boundary_requirements",
            source_family="Reliable ML + NIST manage function",
            logic_gain="Rollback and kill-switch are design requirements, not afterthoughts.",
            future_gate="Future wiring must have a single no-op path that leaves router output unchanged.",
            allowed_now=True,
        ),
        WebBookInformedAdvisorySurfaceGain(
            code="modular_typed_interface_no_hidden_registry_or_global_state_coupling",
            source_family="Designing ML Systems + Designing LLM Applications",
            logic_gain="Keep a small typed interface and avoid hidden coupling to registries, prompt libraries, or global state.",
            future_gate="Future surface wiring may depend only on explicit router result and already computed advisory payload.",
            allowed_now=True,
        ),
        WebBookInformedAdvisorySurfaceGain(
            code="security_threat_model_for_prompt_injection_output_handling_disclosure_agency_supply_chain_dos",
            source_family="OWASP LLM Top 10 + NCSC",
            logic_gain="Threat-model the advisory surface for prompt injection, insecure output, disclosure, agency, supply-chain, and DoS risks.",
            future_gate="Future surface must not render untrusted instructions as executable commands or leak privileged context.",
            allowed_now=True,
        ),
        WebBookInformedAdvisorySurfaceGain(
            code="route_influence_limited_to_future_deterministic_recheck_request_not_override",
            source_family="Human-Centered AI + AI safety control logic",
            logic_gain="Allow future disagreement to request deterministic re-check only; never direct override.",
            future_gate="Any route influence discussion must be a new high-risk contract and cannot bypass the governed router.",
            allowed_now=True,
        ),
    )

    audit = WebBookInformedSurfaceWiringAudit(
        web_sources=WEB_SOURCES,
        book_sources=BOOK_SOURCES,
        rejected_or_deferred=(
            "direct_ml_route_override",
            "runtime_copilot_decision_authority",
            "provider_backed_runtime_adapter_activation",
            "free_text_route_recommendations",
            "persistent_advisory_logs_or_report_storage",
            "prompt_library_or_router_canon_reads_by_advisory_path",
        ),
    )

    return WebBookInformedSurfaceWiringContract(
        feature_id=FEATURE_ID,
        reviewed_feature_id=REVIEWED_FEATURE_ID,
        audit=audit,
        gains=gains,
        automatic_use_rule=(
            "Allowed only in a future contract after canonical router final selection, "
            "with route result copied unchanged into the response envelope."
        ),
        visible_panel_rule=(
            "Allowed only as read-only telemetry with uncertainty/status/role labels, "
            "disable/no-op policy, typed bounded fields, and no free-text route recommendations."
        ),
        route_effect_rule=(
            "Direct route choice effect is blocked. A later contract may study deterministic re-check requests only, "
            "with the governed router still final."
        ),
        direct_route_authority_allowed=False,
        runtime_panel_wired=False,
        provider_calls_allowed=False,
        router_final_selection_modified=False,
        persistence_allowed=False,
        critical_boundary_error_budget=0,
    )


def evaluate_phase7_web_book_advisory_surface_wiring_request(
    *,
    auto_use_after_router: bool,
    visible_panel: bool,
    affect_route_choice: bool,
    provider_backed: bool = False,
    persistent_logging: bool = False,
) -> WebBookInformedSurfaceWiringDecision:
    """Classify next wiring scope under the web-and-book-informed contract."""

    if affect_route_choice:
        return WebBookInformedSurfaceWiringDecision(
            may_auto_use_after_router=auto_use_after_router,
            may_show_visible_panel=visible_panel,
            may_affect_route_choice=False,
            required_next_contract="high_risk_route_authority_escalation_boundary_required_but_not_recommended",
            reason="Direct ML route influence violates the authority model; only deterministic re-check request logic may be studied later.",
        )

    if provider_backed:
        return WebBookInformedSurfaceWiringDecision(
            may_auto_use_after_router=False,
            may_show_visible_panel=False,
            may_affect_route_choice=False,
            required_next_contract="provider_budgeted_adapter_boundary_required_before_activation",
            reason="Provider-backed activation needs latency, cost, availability, privacy, and fallback budgets first.",
        )

    if persistent_logging:
        return WebBookInformedSurfaceWiringDecision(
            may_auto_use_after_router=False,
            may_show_visible_panel=False,
            may_affect_route_choice=False,
            required_next_contract="privacy_bounded_monitoring_contract_required_before_persistence",
            reason="Persistent advisory logs are not allowed without a separate privacy-bounded monitoring contract.",
        )

    if auto_use_after_router or visible_panel:
        return WebBookInformedSurfaceWiringDecision(
            may_auto_use_after_router=auto_use_after_router,
            may_show_visible_panel=visible_panel,
            may_affect_route_choice=False,
            required_next_contract="phase_7_guarded_advisory_surface_wiring_contract_v1",
            reason="Automatic use and visible panel are safe to design only as read-only telemetry after canonical router selection, with no route mutation.",
        )

    return WebBookInformedSurfaceWiringDecision(
        may_auto_use_after_router=False,
        may_show_visible_panel=False,
        may_affect_route_choice=False,
        required_next_contract="no_runtime_wiring_requested",
        reason="Research flux only; keep the completed Phase 6 state dormant.",
    )
