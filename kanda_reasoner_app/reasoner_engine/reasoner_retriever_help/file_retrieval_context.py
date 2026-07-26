r"""
Cohesive context helpers for file-level ProjectRetriever evidence scoring.

This module exists because the original file_retrieval.py stored query setup,
per-file context extraction, and result reindexing inside one large function.
It keeps those mechanics importable without changing the public contract.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from kanda_reasoner_app.reasoner_engine.v10_models import EvidenceItem
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.query_intents import (
    detect_query_intents,
    is_where_is_called_question,
)
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.query_text import (
    file_name_from_path,
    is_allowed_project_path,
    norm_text,
    tokenize_query,
)

__all__ = [
    'RetrievalQueryContext',
    'CandidateFileContext',
    'build_query_context',
    'candidate_file_paths',
    'collect_symbols',
    'module_name_for_file',
    'build_candidate_context',
    'reindex_file_evidence',
]



@dataclass(slots=True)
class RetrievalQueryContext:
    q: str
    tokens: list[str]
    intents: dict[str, Any]
    which_calls_query: Any
    explanation_heavy: bool
    is_runtime_question: bool
    entry_files: set[str]
    question_file_names: set[str]
    packaging_files: set[str]
    documentation_files: set[str]
    exact_reference_query: bool
    exact_symbol_targets: list[str]
    wants_call_site: bool
    wants_definition: bool
    asks_for_navbar_builder: bool
    asks_for_notebook_builder: bool
    reset_cleanup_query: bool
    reset_runtime_query: bool


@dataclass(slots=True)
class CandidateFileContext:
    path: str
    file_record: dict[str, Any]
    module_name: Any
    docstring: Any
    function_names: list[str]
    class_names: list[str]
    called_symbols: list[str]
    roles: list[str]
    advanced_ctx: dict[str, str]
    runtime_anchors: list[str]
    runtime_previews: list[str]
    haystack: str
    normalized_path: str
    base_name: str
    startup_orchestration_markers: list[str]
    startup_orchestration_content_hit: bool
    startup_orchestrator_path_hit: bool
    startup_leaf_ui_path_hit: bool


def build_query_context(retriever, question: str) -> RetrievalQueryContext:
    q = norm_text(question)
    tokens = tokenize_query(q)
    intents = detect_query_intents(q)
    which_calls_query = intents["which_calls"]

    explanation_heavy = (
        intents["explanatory"]
        or intents["code_localized_explanation"]
        or intents["explain_chain"]
    )
    is_runtime_question = intents["runtime_heavy"]

    entry_files = {
        path
        for path in retriever.idx.project_summary.get("entry_files", [])
        if is_allowed_project_path(path)
    }
    question_file_names = set(re.findall(r"[a-zA-Z0-9_\-]+\.py", q))

    packaging_files = {
        path
        for path in retriever.idx.packaging_metadata.get("packaging_files_found", [])
        if is_allowed_project_path(path)
    }

    documentation_files = {
        path
        for path in retriever.idx.documentation_intent.get(
            "documentation_files_found", []
        )
        if is_allowed_project_path(path)
    }

    exact_reference_query = is_where_is_called_question(q)
    exact_symbol_targets = [
        token for token in tokens if "_" in token or "." in token or len(token) >= 10
    ]

    wants_call_site = (
        "call site" in q
        or "called" in q
        or "constructs" in q
        or "startup chain" in q
        or retriever._question_has_profile_alias(q, "top_navigation")
    )

    wants_definition = (
        "files define" in q
        or "which files define" in q
        or "defined by" in q
        or "where is defined" in q
        or "definition" in q
    )

    asks_for_navbar_builder = retriever._question_has_profile_alias(
        q,
        "navbar_builder_terms",
    )

    asks_for_notebook_builder = retriever._question_has_profile_alias(
        q,
        "notebook_builder_terms",
    )

    reset_cleanup_query = (
        "reset" in q
        or "cleanup" in q
        or "snapshot" in q
        or "close" in q
        or retriever._question_has_profile_alias(q, "reset_cleanup")
    )

    reset_runtime_query = is_runtime_question and (
        "reset" in q
        or "close" in q
        or "disconnect" in q
        or "timer" in q
        or "signal" in q
    )

    return RetrievalQueryContext(
        q=q,
        tokens=tokens,
        intents=intents,
        which_calls_query=which_calls_query,
        explanation_heavy=explanation_heavy,
        is_runtime_question=is_runtime_question,
        entry_files=entry_files,
        question_file_names=question_file_names,
        packaging_files=packaging_files,
        documentation_files=documentation_files,
        exact_reference_query=exact_reference_query,
        exact_symbol_targets=exact_symbol_targets,
        wants_call_site=wants_call_site,
        wants_definition=wants_definition,
        asks_for_navbar_builder=asks_for_navbar_builder,
        asks_for_notebook_builder=asks_for_notebook_builder,
        reset_cleanup_query=reset_cleanup_query,
        reset_runtime_query=reset_runtime_query,
    )


def candidate_file_paths(retriever, ctx: RetrievalQueryContext) -> set[str]:
    candidate_paths = set(retriever.idx.files_by_path.keys())
    if ctx.is_runtime_question:
        candidate_paths.update(retriever.idx.runtime_events_by_file.keys())
    return candidate_paths


def collect_symbols(file_record: dict[str, Any]) -> tuple[list[str], list[str], list[str]]:
    function_names: list[str] = []
    class_names: list[str] = []
    called_symbols: list[str] = []

    for fn in file_record.get("functions", []):
        function_names.append(fn.get("qualname", ""))
        function_names.append(fn.get("name", ""))
        for call in fn.get("calls", []):
            called_symbols.append(call.get("call_name", ""))

    for cls in file_record.get("classes", []):
        class_names.append(cls.get("name", ""))
        for method in cls.get("methods", []):
            function_names.append(method.get("qualname", ""))
            function_names.append(method.get("name", ""))
            for call in method.get("calls", []):
                called_symbols.append(call.get("call_name", ""))

    return function_names, class_names, called_symbols


def module_name_for_file(path: str, file_record: dict[str, Any]) -> Any:
    return file_record.get(
        "module_name",
        path[:-3].replace("\\", ".").replace("/", ".")
        if path.endswith(".py")
        else path,
    )


def build_candidate_context(retriever, path: str) -> CandidateFileContext:
    file_record = retriever.idx.files_by_path.get(path, {})
    if not isinstance(file_record, dict):
        file_record = {}

    module_name = module_name_for_file(path, file_record)
    docstring = file_record.get("docstring", "")
    strings = " ".join(file_record.get("strings", []))
    comments = " ".join(file_record.get("comments", []))
    entry_markers = " ".join(file_record.get("entry_markers", []))
    ui_hits = " ".join(file_record.get("ui_keyword_hits", []))
    eeg_hits = " ".join(file_record.get("eeg_keyword_hits", []))
    semantic_hints = " ".join(file_record.get("semantic_hints", []))
    roles = retriever.idx.semantic_roles.get(path, {}).get("roles", [])

    function_names, class_names, called_symbols = collect_symbols(file_record)
    advanced_ctx = retriever._collect_file_context_blobs(path)
    runtime_anchors, runtime_previews = retriever._get_runtime_anchor_summary(
        path,
        limit=12,
    )

    haystack = " ".join(
        [
            norm_text(path),
            norm_text(module_name),
            norm_text(docstring),
            norm_text(strings),
            norm_text(comments),
            norm_text(entry_markers),
            norm_text(ui_hits),
            norm_text(eeg_hits),
            norm_text(semantic_hints),
            norm_text(" ".join(function_names)),
            norm_text(" ".join(class_names)),
            norm_text(" ".join(called_symbols)),
            norm_text(" ".join(roles)),
            advanced_ctx["widgets"],
            advanced_ctx["ui_actions"],
            advanced_ctx["boundaries"],
            advanced_ctx["runtime"],
            advanced_ctx["hotspots"],
            norm_text(" ".join(runtime_anchors)),
            norm_text(" ".join(runtime_previews)),
        ]
    )

    normalized_path = path.replace("\\", "/").lower()
    base_name = file_name_from_path(path)
    startup_orchestration_markers = [
        "qapplication",
        "def main",
        "main(",
        "build_application",
        "run_app",
        "app.exec",
        "build_and_show",
        "create_main_window",
        "create_main_widget",
        "setcentralwidget",
        "show(",
        "showmaximized",
        'if __name__ == "__main__"',
        "if __name__ == '__main__'",
    ]
    startup_orchestration_content_hit = any(
        marker in haystack for marker in startup_orchestration_markers
    )
    startup_orchestrator_path_hit = (
        normalized_path in {"shell/kanda_main.py", "shell/kanda_runner.py"}
        or any(
            term in normalized_path
            for term in [
                "main_window",
                "interface_manager",
                "launcher",
                "runner",
                "kanda_main",
                "kanda_runner",
            ]
        )
    )
    startup_leaf_ui_path_hit = any(
        marker in normalized_path
        for marker in [
            "common/templates/tooltips/",
            "common/utils/",
            "plugins/filter_panel/",
            "combobox_template.py",
            "hover_card_widget.py",
            "tooltip",
        ]
    )

    return CandidateFileContext(
        path=path,
        file_record=file_record,
        module_name=module_name,
        docstring=docstring,
        function_names=function_names,
        class_names=class_names,
        called_symbols=called_symbols,
        roles=roles,
        advanced_ctx=advanced_ctx,
        runtime_anchors=runtime_anchors,
        runtime_previews=runtime_previews,
        haystack=haystack,
        normalized_path=normalized_path,
        base_name=base_name,
        startup_orchestration_markers=startup_orchestration_markers,
        startup_orchestration_content_hit=startup_orchestration_content_hit,
        startup_orchestrator_path_hit=startup_orchestrator_path_hit,
        startup_leaf_ui_path_hit=startup_leaf_ui_path_hit,
    )


def reindex_file_evidence(scored: list[EvidenceItem], limit: int) -> list[EvidenceItem]:
    scored.sort(key=lambda item: (-item.score, item.path))
    scored = scored[:limit]

    reindexed: list[EvidenceItem] = []
    for idx, item in enumerate(scored, start=1):
        reindexed.append(
            EvidenceItem(
                evidence_id="F" + str(idx).zfill(2),
                score=item.score,
                path=item.path,
                module_name=item.module_name,
                reason=item.reason,
                detail=item.detail,
            )
        )
    return reindexed
