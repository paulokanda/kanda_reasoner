# project-path: kanda_reasoner_app/manage_architecture/warning_model_test_protection_resolver.py
"""Orchestrate semantic Local AI escalation and sandbox-validated test changes."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
import json
from pathlib import Path

from kanda_reasoner_app.manage_architecture.ai_review.adapter import Tab1AIReviewAdapter
from kanda_reasoner_app.manage_architecture.warning_heuristic_resolver import WarningFinding
from kanda_reasoner_app.manage_architecture.warning_model_test_apply import (
    ModelTestProtectionApplyResult,
    apply_validated_model_test_changes,
)
from kanda_reasoner_app.manage_architecture.warning_model_test_generation_contract import (
    ACTION_CREATE_FOCUSED_TEST,
    ACTION_EXTEND_EXISTING_TEST,
    ACTION_MODEL_TEST_CHANGE,
    ModelTestMutationProposal,
    build_mutation_proposal,
)
from kanda_reasoner_app.manage_architecture.warning_model_test_protection_context import (
    ModelResolverError,
    ModelTestSourceContext,
    build_model_source_context,
    build_model_test_messages,
    decision_from_model_payload,
    iter_test_files,
    parse_model_test_response,
    resolve_selected_model,
)
from kanda_reasoner_app.manage_architecture.warning_model_test_sandbox_validation import (
    SandboxValidationReport,
    validate_mutation_proposals,
)
from kanda_reasoner_app.manage_architecture.warning_test_protection_gap_resolver import (
    ACTION_ALREADY_PROTECTED,
    ACTION_LINK_EXISTING_TEST,
    ACTION_WEB_AI,
    TestProtectionGapDecision,
    TestProtectionGapPlan,
    build_test_protection_gap_plan,
)

__all__ = [
    "ModelTestProtectionPlan",
    "apply_model_test_protection_plan",
    "build_model_test_protection_plan",
]

_BATCH_SIZE = 2
ProgressCallback = Callable[[int, int, int, int, str, str], None]
ChatCallable = Callable[..., tuple[str, str]]
ModelLister = Callable[[], list[str]]
SandboxValidator = Callable[..., SandboxValidationReport]


def list_available_models() -> list[str]:
    """Return current models from the same registry as the top selector."""
    return Tab1AIReviewAdapter().list_models()


def chat_selected_model(
    messages: list[dict[str, str]],
    *,
    model_selection: str,
    temperature: float,
    max_tokens: int,
) -> tuple[str, str]:
    """Run raw chat with the already-resolved exact model selection."""
    try:
        return Tab1AIReviewAdapter().chat_exact(
            messages,
            model_name=model_selection,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    except Exception as exc:
        raise ModelResolverError(str(exc)) from exc


@dataclass(frozen=True, slots=True)
class ModelTestProtectionPlan:
    """Combined heuristic, semantic-link, and sandbox-validated test-change plan."""

    project_root: str
    model_name: str
    decisions: tuple[TestProtectionGapDecision, ...]
    mutations: tuple[ModelTestMutationProposal, ...]
    sandbox_root: str
    heuristic_safe_count: int
    model_safe_count: int
    model_test_change_count: int
    already_protected_count: int
    web_ai_count: int

    @property
    def safe_link_count(self) -> int:
        return self.heuristic_safe_count + self.model_safe_count

    @property
    def safe_change_count(self) -> int:
        return self.safe_link_count + self.model_test_change_count



def _call_batch(
    contexts: tuple[ModelTestSourceContext, ...],
    *,
    model_name: str,
    chat_callable: ChatCallable,
) -> dict[str, dict[str, object]]:
    expected = {item.source_path for item in contexts}
    messages = build_model_test_messages(contexts)
    errors: list[str] = []
    for attempt in range(2):
        request_messages = list(messages)
        if errors:
            request_messages.append(
                {
                    "role": "user",
                    "content": (
                        "Previous response validation failed: "
                        + errors[-1]
                        + ". Return the exact JSON contract only."
                    ),
                }
            )
        try:
            response_text, used_model = chat_callable(
                request_messages,
                model_selection=model_name,
                temperature=0.02,
                max_tokens=6000,
            )
            if str(used_model or "").strip() != model_name:
                raise ModelResolverError(
                    "model-assisted runtime used a different model than selected: "
                    + str(used_model)
                )
            return parse_model_test_response(response_text, expected)
        except (ValueError, json.JSONDecodeError, ModelResolverError) as exc:
            errors.append(type(exc).__name__ + ": " + str(exc))
            if attempt == 1:
                raise ModelResolverError(
                    "model-assisted batch response invalid after one retry. "
                    + " | ".join(errors)
                ) from exc
    raise AssertionError("unreachable")


def _progress_counts(
    plan: TestProtectionGapPlan,
    final_by_source: dict[str, TestProtectionGapDecision],
) -> tuple[int, int, int]:
    complete = [
        final_by_source.get(item.source_path)
        for item in plan.decisions
        if final_by_source.get(item.source_path) is not None
    ]
    done = sum(1 for item in complete if item.action != ACTION_WEB_AI)
    web_ai = sum(1 for item in complete if item.action == ACTION_WEB_AI)
    return len(complete), done, web_ai


def _emit_pending_progress(
    callback: ProgressCallback | None,
    heuristic_plan: TestProtectionGapPlan,
    final_by_source: dict[str, TestProtectionGapDecision],
    source_path: str,
    action: str,
) -> None:
    if callback is None:
        return
    complete_count, done, web_ai = _progress_counts(heuristic_plan, final_by_source)
    callback(
        len(heuristic_plan.decisions),
        len(heuristic_plan.decisions) - complete_count,
        done,
        web_ai,
        source_path,
        action,
    )


def _web_ai_decision(
    context: ModelTestSourceContext,
    *,
    reason: str,
    candidate_test_path: str = "",
    score: int = 0,
) -> TestProtectionGapDecision:
    return TestProtectionGapDecision(
        source_path=context.source_path,
        module_name=context.module_name,
        action=ACTION_WEB_AI,
        candidate_test_path=candidate_test_path,
        candidate_score=score,
        candidate_reasons=("model_reviewed", "sandbox_fail_closed"),
        source_public_symbols=context.public_symbols,
        test_sha256_before="",
        reason=reason,
    )


def _pending_mutation_decision(
    context: ModelTestSourceContext,
    proposal: ModelTestMutationProposal,
) -> TestProtectionGapDecision:
    return TestProtectionGapDecision(
        source_path=context.source_path,
        module_name=context.module_name,
        action=ACTION_MODEL_TEST_CHANGE,
        candidate_test_path=proposal.target_test_path,
        candidate_score=int(round(proposal.confidence * 100)),
        candidate_reasons=("model_generated_behavioral_test", "sandbox_validation_pending"),
        source_public_symbols=context.public_symbols,
        test_sha256_before=proposal.test_sha256_before,
        reason=proposal.reason,
    )


def _accepted_mutation_decision(
    context: ModelTestSourceContext,
    proposal: ModelTestMutationProposal,
    validation_reason: str,
) -> TestProtectionGapDecision:
    return TestProtectionGapDecision(
        source_path=context.source_path,
        module_name=context.module_name,
        action=ACTION_MODEL_TEST_CHANGE,
        candidate_test_path=proposal.target_test_path,
        candidate_score=int(round(proposal.confidence * 100)),
        candidate_reasons=(
            "model_generated_behavioral_test",
            "sandbox_targeted_pytest_pass",
            "sandbox_architecture_gap_removed",
        ),
        source_public_symbols=context.public_symbols,
        test_sha256_before=proposal.test_sha256_before,
        reason=proposal.reason + " Validation: " + validation_reason,
    )


def _sandbox_progress_adapter(
    callback: ProgressCallback | None,
    heuristic_plan: TestProtectionGapPlan,
    final_by_source: dict[str, TestProtectionGapDecision],
) -> ProgressCallback | None:
    if callback is None:
        return None

    def adapted(
        _total: int,
        _to_go: int,
        _done: int,
        _web_ai: int,
        source_path: str,
        action: str,
    ) -> None:
        _emit_pending_progress(
            callback,
            heuristic_plan,
            final_by_source,
            source_path,
            action,
        )

    return adapted


def build_model_test_protection_plan(
    project_root: str | Path,
    findings: Iterable[WarningFinding],
    *,
    model_selection: str,
    chat_callable: ChatCallable = chat_selected_model,
    model_lister: ModelLister = list_available_models,
    sandbox_validator: SandboxValidator = validate_mutation_proposals,
    progress_callback: ProgressCallback | None = None,
) -> ModelTestProtectionPlan:
    """Escalate heuristic gaps to semantic linking or sandbox-validated real tests."""
    root = Path(project_root).expanduser().resolve()
    heuristic_plan = build_test_protection_gap_plan(root, tuple(findings))
    model_name = resolve_selected_model(model_selection, model_lister=model_lister)
    test_files = iter_test_files(root)
    final_by_source: dict[str, TestProtectionGapDecision] = {}
    unresolved: list[TestProtectionGapDecision] = []
    contexts_by_source: dict[str, ModelTestSourceContext] = {}
    for decision in heuristic_plan.decisions:
        if decision.action == ACTION_WEB_AI:
            unresolved.append(decision)
        else:
            final_by_source[decision.source_path] = decision
    contexts: list[ModelTestSourceContext] = []
    for decision in unresolved:
        context = build_model_source_context(root, decision, test_files)
        if context is None:
            final_by_source[decision.source_path] = decision
            continue
        contexts.append(context)
        contexts_by_source[context.source_path] = context

    provisional_mutations: list[ModelTestMutationProposal] = []
    for index in range(0, len(contexts), _BATCH_SIZE):
        batch = tuple(contexts[index : index + _BATCH_SIZE])
        for context in batch:
            _emit_pending_progress(
                progress_callback,
                heuristic_plan,
                final_by_source,
                context.source_path,
                "local_ai_reviewing",
            )
        try:
            payloads = _call_batch(batch, model_name=model_name, chat_callable=chat_callable)
        except ModelResolverError as exc:
            payloads = {
                context.source_path: {
                    "action": ACTION_WEB_AI,
                    "candidate_test_path": "",
                    "confidence": 0.0,
                    "reason": str(exc),
                }
                for context in batch
            }
        for context in batch:
            payload = payloads[context.source_path]
            action = str(payload.get("action", "")).strip()
            if action in {ACTION_EXTEND_EXISTING_TEST, ACTION_CREATE_FOCUSED_TEST}:
                try:
                    proposal = build_mutation_proposal(root, context, payload, model_name)
                except Exception as exc:
                    final_by_source[context.source_path] = _web_ai_decision(
                        context,
                        reason="Local AI test proposal rejected: " + type(exc).__name__ + ": " + str(exc),
                    )
                else:
                    provisional_mutations.append(proposal)
                    final_by_source[context.source_path] = _pending_mutation_decision(context, proposal)
            else:
                final_by_source[context.source_path] = decision_from_model_payload(
                    context,
                    payload,
                    model_name,
                )
            _emit_pending_progress(
                progress_callback,
                heuristic_plan,
                final_by_source,
                context.source_path,
                final_by_source[context.source_path].action,
            )

    accepted_mutations: list[ModelTestMutationProposal] = []
    sandbox_root = ""
    if provisional_mutations:
        report = sandbox_validator(
            root,
            tuple(provisional_mutations),
            progress_callback=_sandbox_progress_adapter(
                progress_callback,
                heuristic_plan,
                final_by_source,
            ),
        )
        sandbox_root = report.sandbox_root
        outcomes = report.outcome_by_source()
        for proposal in provisional_mutations:
            context = contexts_by_source[proposal.source_path]
            outcome = outcomes.get(proposal.source_path)
            if outcome is not None and outcome.accepted:
                accepted_mutations.append(proposal)
                final_by_source[proposal.source_path] = _accepted_mutation_decision(
                    context,
                    proposal,
                    outcome.reason,
                )
            else:
                final_by_source[proposal.source_path] = _web_ai_decision(
                    context,
                    reason=(
                        outcome.reason
                        if outcome is not None
                        else "Disposable-project validation returned no outcome for the proposal."
                    ),
                    candidate_test_path=proposal.target_test_path,
                    score=int(round(proposal.confidence * 100)),
                )
            _emit_pending_progress(
                progress_callback,
                heuristic_plan,
                final_by_source,
                proposal.source_path,
                final_by_source[proposal.source_path].action,
            )

    ordered = tuple(final_by_source[item.source_path] for item in heuristic_plan.decisions)
    heuristic_safe = sum(
        1 for item in heuristic_plan.decisions if item.action == ACTION_LINK_EXISTING_TEST
    )
    model_safe = sum(
        1
        for item in ordered
        if item.action == ACTION_LINK_EXISTING_TEST
        and "model_semantic_review" in item.candidate_reasons
    )
    model_test_changes = sum(1 for item in ordered if item.action == ACTION_MODEL_TEST_CHANGE)
    already = sum(1 for item in ordered if item.action == ACTION_ALREADY_PROTECTED)
    web_ai = sum(1 for item in ordered if item.action == ACTION_WEB_AI)
    return ModelTestProtectionPlan(
        project_root=str(root),
        model_name=model_name,
        decisions=ordered,
        mutations=tuple(accepted_mutations),
        sandbox_root=sandbox_root,
        heuristic_safe_count=heuristic_safe,
        model_safe_count=model_safe,
        model_test_change_count=model_test_changes,
        already_protected_count=already,
        web_ai_count=web_ai,
    )


def apply_model_test_protection_plan(
    plan: ModelTestProtectionPlan,
) -> ModelTestProtectionApplyResult:
    """Apply confirmed links and sandbox-validated test changes through one guarded writer."""
    return apply_validated_model_test_changes(
        plan.project_root,
        plan.decisions,
        plan.mutations,
    )
