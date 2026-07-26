r"""Startup and explanation-heavy scoring helpers for file retrieval."""
from __future__ import annotations

from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_context import (
    CandidateFileContext,
    RetrievalQueryContext,
)
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.query_text import (
    is_auxiliary_ui_path,
)

__all__ = [
    'apply_startup_scoring',
    'apply_explanation_heavy_scoring',
]



def apply_startup_scoring(
    retriever,
    query: RetrievalQueryContext,
    candidate: CandidateFileContext,
    score: int,
    reasons: list[str],
) -> int:
    if any(marker in candidate.haystack for marker in candidate.startup_orchestration_markers):
        score += 50
        reasons.append("startup-chain-boost")

    if candidate.path in query.entry_files and (
        candidate.startup_orchestrator_path_hit
        or candidate.startup_orchestration_content_hit
    ):
        score += 30
        reasons.append("startup-entry-boost")

    if any(
        term in candidate.normalized_path
        for term in [
            "main_window",
            "interface_manager",
            "builder",
            "launcher",
            "main",
            "runner",
        ]
    ):
        score += 20
        reasons.append("startup-path-boost")

    startup_chain_steps = retriever.idx.execution_chains.get("startup_chain", [])
    startup_chain_files = {
        str(step.get("file", "")).strip()
        for step in startup_chain_steps
        if isinstance(step, dict) and str(step.get("file", "")).strip()
    }
    if candidate.path in startup_chain_files and (
        candidate.startup_orchestrator_path_hit
        or candidate.startup_orchestration_content_hit
    ):
        score += 180
        reasons.append("startup-named-chain-step-boost")

    if "eegmainwindowbuilder" in query.q and "eegmainwindowbuilder" in candidate.haystack:
        score += 160
        reasons.append("startup-main-window-builder-boost")

    if is_auxiliary_ui_path(candidate.path):
        score -= 20
        reasons.append("startup-auxiliary-penalty")

    if any(
        term in candidate.normalized_path
        for term in ["migration_", "legacy_import", "auditor", "scanner"]
    ):
        score -= 180
        reasons.append("startup-non-ui-penalty")

    if "check_runtime_trace_schema.py" in candidate.normalized_path:
        score -= 120
        reasons.append("startup-schema-validator-penalty")

    if candidate.startup_leaf_ui_path_hit and not candidate.startup_orchestrator_path_hit:
        score -= 200
        reasons.append("startup-leaf-ui-penalty")

    if (
        "/common/utils/" in candidate.normalized_path
        or candidate.normalized_path.startswith("common/utils/")
    ):
        score -= 90
        reasons.append("startup-common-utils-penalty")

    return score


def apply_explanation_heavy_scoring(
    query: RetrievalQueryContext,
    candidate: CandidateFileContext,
    score: int,
    reasons: list[str],
) -> int:
    if candidate.path in query.entry_files:
        score += 40
        reasons.append("explanation-entry-file-boost")

    if any(
        term in candidate.normalized_path
        for term in [
            "main",
            "builder",
            "launcher",
            "initializer",
            "manager",
            "controller",
            "service",
            "runner",
            "viewer",
            "interface_manager",
        ]
    ):
        score += 45
        reasons.append("explanation-path-role-boost")

    if candidate.called_symbols:
        score += 24
        reasons.append("explanation-has-calls-boost")

    if candidate.function_names:
        score += 12
        reasons.append("explanation-has-functions-boost")

    if candidate.class_names:
        score += 10
        reasons.append("explanation-has-classes-boost")

    if candidate.advanced_ctx["ui_actions"]:
        score += 24
        reasons.append("explanation-ui-actions-boost")

    if candidate.advanced_ctx["boundaries"]:
        score += 22
        reasons.append("explanation-boundary-boost")

    if candidate.advanced_ctx["runtime"] and query.is_runtime_question:
        score += 34
        reasons.append("explanation-runtime-boost")

    if candidate.runtime_anchors:
        score += 12
        reasons.append("explanation-runtime-anchors-boost")

    explanatory_markers = [
        "build",
        "initialize",
        "init",
        "connect",
        "load",
        "show",
        "render",
        "plot",
        "draw",
        "update",
        "refresh",
        "attach",
        "create",
        "signal",
        "slot",
        "handler",
    ]
    if any(marker in candidate.haystack for marker in explanatory_markers):
        score += 26
        reasons.append("explanation-orchestration-marker-boost")

    if is_auxiliary_ui_path(candidate.path) and "help" not in query.q:
        score -= 25
        reasons.append("explanation-auxiliary-penalty")

    return score
