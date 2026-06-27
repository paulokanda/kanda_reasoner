r"""
MODULE ORIGIN: kanda_reasoner_app/reasoner_engine\reasoner_retriever.py
MANIFEST: kanda_reasoner_app/reasoner_engine\reasoner_retriever_help.json
HELP FOLDER: kanda_reasoner_app/reasoner_engine\reasoner_retriever_help
PURPOSE: Own file-level retrieval and compact file-evidence formatting for ProjectRetriever.
EXPORTS: retrieve_files, build_compact_file_evidence
DEPENDS ON: query_intents.py, query_text.py, file_context_scoring.py, profile_support.py
REFACTOR DATE: 2026-04-10
"""

# Canonical readable source. Deprecated private base64 source shards are history only.
from __future__ import annotations

import re

from kanda_reasoner_app.reasoner_engine.v10_models import EvidenceItem
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.query_intents import (
    detect_query_intents,
    is_where_is_called_question,
)
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.query_text import (
    file_name_from_path,
    is_allowed_project_path,
    is_auxiliary_ui_path,
    last_part_match_in_query,
    norm_text,
    tokenize_query,
)

__all__ = ["retrieve_files", "build_compact_file_evidence"]


def retrieve_files(retriever, question: str, limit: int) -> list[EvidenceItem]:
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
    scored: list[EvidenceItem] = []

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

    candidate_paths = set(retriever.idx.files_by_path.keys())

    if is_runtime_question:
        candidate_paths.update(retriever.idx.runtime_events_by_file.keys())

    # runtime_signal_connections are collector-internal probe signals.
    # Do not add their source files to candidate_paths - they are not
    # EEG project files and would inject empty-content noise into evidence.

    for path in sorted(candidate_paths):
        if not is_allowed_project_path(path):
            continue

        file_record = retriever.idx.files_by_path.get(path, {})
        if not isinstance(file_record, dict):
            file_record = {}

        module_name = file_record.get(
            "module_name",
            path[:-3].replace("\\", ".").replace("/", ".")
            if path.endswith(".py")
            else path,
        )
        docstring = file_record.get("docstring", "")
        strings = " ".join(file_record.get("strings", []))
        comments = " ".join(file_record.get("comments", []))
        entry_markers = " ".join(file_record.get("entry_markers", []))
        ui_hits = " ".join(file_record.get("ui_keyword_hits", []))
        eeg_hits = " ".join(file_record.get("eeg_keyword_hits", []))
        semantic_hints = " ".join(file_record.get("semantic_hints", []))
        roles = retriever.idx.semantic_roles.get(path, {}).get("roles", [])

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

        score = 0
        reasons: list[str] = []

        if reset_runtime_query:
            asks_amplitude_map = (
                "amplitude map" in q
                or "amplitude-map" in q
                or "amp map" in q
                or "topomap" in q
            )

            amplitude_map_side_file = (
                "eeg_amplitude_map_initializer.py" in normalized_path
                or "/amplitude_map/" in normalized_path
                or "amplitude_map" in base_name
            )

            core_reset_runtime_file = (
                normalized_path.startswith("shell/viewer/eeg_visualizer_core.py")
                or normalized_path.startswith("core/snapshot/eeg_pipeline_reset.py")
                or normalized_path.startswith("core/snapshot/eeg_session_snapshot.py")
            )

            if (
                amplitude_map_side_file
                and not asks_amplitude_map
                and not core_reset_runtime_file
            ):
                score -= 220
                reasons.append("reset-runtime-amplitude-map-file-penalty")

        if normalized_path in q:
            score += 120
            reasons.append("exact-path-match")

        if base_name and base_name in q:
            score += 80
            reasons.append("exact-filename-match")

        for file_name in question_file_names:
            if base_name == file_name.lower():
                score += 80
                reasons.append("question-filename-match")

        for token in tokens:
            if token in haystack:
                score += 3
                reasons.append("token:" + token)

        if intents["packaging_metadata"] and path in packaging_files:
            score += 220
            reasons.append("packaging-file-boost")

        if intents["documentation_intent"] and path in documentation_files:
            score += 220
            reasons.append("documentation-file-boost")

        for class_name in class_names:
            class_name_norm = norm_text(class_name)
            if class_name_norm and class_name_norm in q:
                score += 180
                reasons.append("exact-class-match")

            class_tail = class_name_norm.split(".")[-1]
            if class_tail and class_tail in q:
                score += 100
                reasons.append("exact-class-tail-match")

        for called_symbol in called_symbols:
            called_symbol_norm = norm_text(called_symbol)
            if called_symbol_norm and called_symbol_norm in q:
                score += 20
                reasons.append("exact-called-symbol-match")

        if exact_reference_query:
            import_blob = " ".join(file_record.get("imports", []))
            import_blob_low = norm_text(import_blob)
            full_source = norm_text(file_record.get("full_source", ""))

            for target in exact_symbol_targets:
                if not target:
                    continue

                token_hit = target in haystack
                import_hit = target in import_blob_low
                call_hit = full_source and f"{target}(" in full_source

                if token_hit:
                    score += 120
                    reasons.append("exact-reference-token-match:" + target)

                if import_hit:
                    score += 180
                    reasons.append("exact-reference-import-boost:" + target)

                if call_hit:
                    score += 360
                    reasons.append("exact-reference-callsite-boost:" + target)

                if full_source and f"import {target}" in full_source:
                    score += 120
                    reasons.append("exact-reference-import-line-boost:" + target)

                if full_source and "from " in full_source and target in full_source:
                    score += 80
                    reasons.append("exact-reference-from-import-boost:" + target)

                if import_hit and call_hit:
                    score += 320
                    reasons.append("exact-reference-import-plus-call-boost:" + target)

                timeline_target_match = (
                    "timeline" in target
                    or any(
                        term in target
                        for term in retriever._profile_alias_terms(
                            "timeline_symbol_terms"
                        )
                    )
                )

                if timeline_target_match:
                    if any(
                        owner_path in normalized_path
                        for owner_path in retriever._profile_owner_paths(
                            "timeline_owner_paths"
                        )
                    ):
                        score += 180
                        reasons.append("timeline-exact-caller-owner-path-boost")

        if wants_call_site:
            if "build_and_show" in haystack:
                score += 120
                reasons.append("call-site-build-and-show-boost")

            if any(term in normalized_path for term in ["main_window_builder", "viewer"]):
                score += 80
                reasons.append("call-site-main-window-path-boost")

            navbar_callsite_match = asks_for_navbar_builder and (
                retriever._text_has_profile_alias(haystack, "navbar_builder_terms")
            )

            notebook_callsite_match = asks_for_notebook_builder and (
                retriever._text_has_profile_alias(haystack, "notebook_builder_terms")
            )

            if navbar_callsite_match:
                score += 180
                reasons.append("call-site-navbar-builder-boost")

            if notebook_callsite_match:
                score += 180
                reasons.append("call-site-notebook-builder-boost")

            if (
                asks_for_navbar_builder
                and asks_for_notebook_builder
                and "build_and_show" in haystack
                and navbar_callsite_match
                and notebook_callsite_match
            ):
                score += 260
                reasons.append("call-site-combined-builder-chain-boost")

            if any(
                term in haystack
                for term in retriever._profile_alias_terms("builder_callsite_markers")
            ):
                score += 140
                reasons.append("call-site-builder-marker-family-boost")

        if intents["explicit_call_chain"] and "retriever.v.main_window.show" in haystack:
            score += 220
            reasons.append("exact-call-chain-match")

        if intents["main_window_show"]:
            if "retriever.v.main_window.show" in haystack:
                score += 260
                reasons.append("main-window-show-call-boost")

            if "build_and_show" in haystack:
                score += 180
                reasons.append("main-window-show-build-and-show-boost")

            if any(term in normalized_path for term in ["main_window", "viewer", "launcher"]):
                score += 50
                reasons.append("main-window-show-path-boost")

            if any(
                term in normalized_path
                for term in ["migration_", "legacy_import", "auditor", "scanner"]
            ):
                score -= 180
                reasons.append("main-window-show-non-ui-penalty")

        if intents["qtimer_showmaximized"]:
            if (
                "qtimer.singleshot" in haystack
                and "retriever.v.main_window.showmaximized" in haystack
            ):
                score += 320
                reasons.append("qtimer-showmaximized-exact-call-boost")

            if "showmaximized" in haystack and "qtimer.singleshot" not in haystack:
                score -= 180
                reasons.append("direct-showmaximized-without-qtimer-penalty")

            if any(term in normalized_path for term in ["main_window", "viewer", "launcher"]):
                score += 40
                reasons.append("qtimer-showmaximized-path-boost")

        if intents["where_is"]:
            if any(name in q for name in class_names):
                score += 220
                reasons.append("where-is-class-definition-boost")

            if any(name in q for name in function_names):
                score += 160
                reasons.append("where-is-function-definition-boost")

            if last_part_match_in_query(function_names, q):
                score += 60
                reasons.append("where-is-function-tail-boost")

            if last_part_match_in_query(class_names, q):
                score += 80
                reasons.append("where-is-class-tail-boost")

        if intents["which_calls"]:
            if called_symbols:
                score += 20
                reasons.append("which-calls-has-call-graph")

            if any(token in " ".join(called_symbols) for token in tokens):
                score += 120
                reasons.append("which-calls-called-symbol-boost")

            if not called_symbols:
                score -= 40
                reasons.append("which-calls-no-calls-penalty")

        if intents["explain_chain"]:
            if path in entry_files:
                score += 80
                reasons.append("explain-chain-entry-file-boost")

            if any(
                term in normalized_path
                for term in ["main", "builder", "launcher", "interface_manager", "viewer"]
            ):
                score += 50
                reasons.append("explain-chain-orchestrator-path-boost")

            orchestration_terms = [
                "qapplication",
                "build_and_show",
                "create_main_window",
                "create_main_widget",
                "addtab",
                "setcentralwidget",
                "show(",
                "showmaximized",
            ]
            if any(term in haystack for term in orchestration_terms):
                score += 60
                reasons.append("explain-chain-orchestration-boost")

            chain_key = None
            if "startup" in q:
                chain_key = "startup_chain"
            elif "timeline" in q or retriever._question_has_profile_alias(q, "timeline"):
                chain_key = "timeline_chain"
            elif "topomap" in q or "amplitude" in q:
                chain_key = "topomap_chain"
            elif reset_cleanup_query:
                chain_key = "reset_chain"

            if chain_key:
                chain_steps = retriever.idx.execution_chains.get(chain_key, [])
                chain_files = {
                    str(step.get("file", "")).strip()
                    for step in chain_steps
                    if isinstance(step, dict) and str(step.get("file", "")).strip()
                }
                if path in chain_files:
                    score += 180
                    reasons.append("named-chain-step-boost")

            if any(
                marker in normalized_path
                for marker in [
                    "common/templates/tables",
                    "core/snapshot",
                ]
            ):
                score -= 120
                reasons.append("topomap-implementation-non-owner-penalty")

        if (
            retriever._question_has_profile_alias(q, "topomap_explanation")
            or intents["topomap_explanation"]
        ):
            topomap_implementation_query = any(
                term in q
                for term in [
                    "implement",
                    "implements",
                    "implemented",
                    "implementation",
                    "creating",
                    "updating",
                    "participate in creating",
                    "participate in updating",
                    "modules participate",
                    "which code implements",
                    "which modules participate",
                ]
            )

            if "topomap" in haystack or retriever._text_has_profile_alias(haystack, "topomap"):
                score += 220
                reasons.append("topomap-explanation-core-boost")

            if "amplitude_map" in haystack or any(
                term in haystack
                for term in retriever._profile_alias_terms("topomap_symbol_terms")
            ):
                score += 140
                reasons.append("topomap-explanation-amplitude-map-boost")

            if any(
                marker in haystack
                for marker in [
                    "render",
                    "renderer",
                    "draw",
                    "plot",
                    "topography",
                    "topographic",
                ]
            ) or any(
                term in haystack
                for term in retriever._profile_alias_terms("topomap_symbol_terms")
            ):
                score += 120
                reasons.append("topomap-explanation-render-boost")

            if any(
                owner_path in normalized_path
                for owner_path in retriever._profile_owner_paths("topomap_owner_paths")
            ):
                score += 80
                reasons.append("topomap-explanation-path-boost")

            if topomap_implementation_query:
                owner_path_hit = any(
                    owner_path in normalized_path
                    for owner_path in retriever._profile_owner_paths("topomap_owner_paths")
                )

                symbol_family_hit = any(
                    term in haystack
                    for term in retriever._profile_alias_terms("topomap_symbol_terms")
                )

                core_symbol_hit = (
                    "eegamplitudemap" in haystack or "toporenderer" in haystack
                )

                if owner_path_hit:
                    score += 300
                    reasons.append("topomap-implementation-owner-path-boost")

                if symbol_family_hit:
                    score += 220
                    reasons.append("topomap-implementation-symbol-family-boost")

                if core_symbol_hit:
                    score += 260
                    reasons.append("topomap-implementation-core-symbol-boost")

                if owner_path_hit and symbol_family_hit:
                    score += 220
                    reasons.append("topomap-implementation-owner-plus-symbol-boost")

                if owner_path_hit and core_symbol_hit:
                    score += 240
                    reasons.append("topomap-implementation-owner-plus-core-boost")

                if any(
                    marker in normalized_path
                    for marker in [
                        "common/templates/tables",
                        "core/snapshot",
                        "migration_",
                        "legacy_import",
                        "auditor",
                        "scanner",
                    ]
                ):
                    score -= 220
                    reasons.append("topomap-implementation-non-owner-penalty")

                if (
                    "label_renderer" in normalized_path
                    and "topomap_renderer" not in normalized_path
                ):
                    score -= 80
                    reasons.append("topomap-implementation-adjacent-renderer-penalty")

        if reset_cleanup_query:
            if any(
                owner_path in normalized_path
                for owner_path in retriever._profile_owner_paths("reset_cleanup_owner_paths")
            ):
                score += 160
                reasons.append("reset-cleanup-owner-path-boost")

            if any(
                term in haystack
                for term in retriever._profile_alias_terms("reset_cleanup_symbol_terms")
            ):
                score += 140
                reasons.append("reset-cleanup-symbol-family-boost")

            if retriever._text_has_profile_alias(haystack, "reset_cleanup"):
                score += 80
                reasons.append("reset-cleanup-alias-boost")

        if intents["explicit_call_chain"]:
            if any(
                term in normalized_path
                for term in ["migration_", "legacy_import", "auditor", "scanner"]
            ):
                score -= 160
                reasons.append("non-ui-callchain-penalty")

            if any(term in normalized_path for term in ["main_window", "viewer", "launcher"]):
                score += 40
                reasons.append("ui-callchain-path-boost")

        if path in entry_files and any(
            key in q for key in ["start", "startup", "main", "launch", "open", "show"]
        ):
            score += 14
            reasons.append("entry-file")

        if "topomap" in q and (
            "topomap" in haystack
            or "amplitude_map" in haystack
            or retriever._text_has_profile_alias(haystack, "topomap")
            or any(
                term in haystack
                for term in retriever._profile_alias_terms("topomap_symbol_terms")
            )
        ):
            score += 12
            reasons.append("topomap-related")

        if "timeline" in q and "timeline" in haystack:
            score += 12
            reasons.append("timeline-related")

        if retriever._question_has_profile_alias(q, "timeline"):
            if any(
                owner_path in normalized_path
                for owner_path in retriever._profile_owner_paths("timeline_owner_paths")
            ):
                score += 80
                reasons.append("timeline-owner-path-boost")

            if any(
                term in haystack
                for term in retriever._profile_alias_terms("timeline_symbol_terms")
            ):
                score += 120
                reasons.append("timeline-symbol-family-boost")

        if "splash" in q and "splash" in haystack:
            score += 12
            reasons.append("splash-related")

        if "tab" in q and ("tab" in haystack or "notebook" in haystack or "addtab" in haystack):
            score += 12
            reasons.append("tab-related")

        if reset_cleanup_query and (
            "reset" in haystack
            or "snapshot" in haystack
            or "cleanup" in haystack
            or "close" in haystack
            or retriever._text_has_profile_alias(haystack, "reset_cleanup")
            or any(
                term in haystack
                for term in retriever._profile_alias_terms("reset_cleanup_symbol_terms")
            )
        ):
            score += 12
            reasons.append("reset-related")

        if "responsibility" in q and (
            "manager" in haystack or "builder" in haystack or "controller" in haystack
        ):
            score += 10
            reasons.append("responsibility-related")

        if "uncertainty" in q and (
            "warning" in haystack or "try" in haystack or "exception" in haystack
        ):
            score += 8
            reasons.append("uncertainty-related")

        for sub in retriever.idx.subsystems:
            sub_name = str(sub.get("name", "")).strip().lower()
            if not sub_name:
                continue

            if sub_name in q:
                sub_files = sub.get("files", [])
                if isinstance(sub_files, list) and path in sub_files:
                    score += 60
                    reasons.append("subsystem-member-boost:" + sub_name)
                break

        if intents["startup"]:
            if any(marker in haystack for marker in startup_orchestration_markers):
                score += 50
                reasons.append("startup-chain-boost")

            if path in entry_files and (
                startup_orchestrator_path_hit or startup_orchestration_content_hit
            ):
                score += 30
                reasons.append("startup-entry-boost")

            if any(
                term in normalized_path
                for term in ["main_window", "interface_manager", "builder", "launcher", "main", "runner"]
            ):
                score += 20
                reasons.append("startup-path-boost")

            startup_chain_steps = retriever.idx.execution_chains.get("startup_chain", [])
            startup_chain_files = {
                str(step.get("file", "")).strip()
                for step in startup_chain_steps
                if isinstance(step, dict) and str(step.get("file", "")).strip()
            }
            if path in startup_chain_files and (
                startup_orchestrator_path_hit or startup_orchestration_content_hit
            ):
                score += 180
                reasons.append("startup-named-chain-step-boost")

            if "eegmainwindowbuilder" in q and "eegmainwindowbuilder" in haystack:
                score += 160
                reasons.append("startup-main-window-builder-boost")

            if is_auxiliary_ui_path(path):
                score -= 20
                reasons.append("startup-auxiliary-penalty")

            if any(
                term in normalized_path
                for term in ["migration_", "legacy_import", "auditor", "scanner"]
            ):
                score -= 180
                reasons.append("startup-non-ui-penalty")

            if "check_runtime_trace_schema.py" in normalized_path:
                score -= 120
                reasons.append("startup-schema-validator-penalty")

            if startup_leaf_ui_path_hit and not startup_orchestrator_path_hit:
                score -= 200
                reasons.append("startup-leaf-ui-penalty")

            if (
                "/common/utils/" in normalized_path
                or normalized_path.startswith("common/utils/")
            ):
                score -= 90
                reasons.append("startup-common-utils-penalty")

        if explanation_heavy:
            if path in entry_files:
                score += 40
                reasons.append("explanation-entry-file-boost")

            if any(
                term in normalized_path
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

            if called_symbols:
                score += 24
                reasons.append("explanation-has-calls-boost")

            if function_names:
                score += 12
                reasons.append("explanation-has-functions-boost")

            if class_names:
                score += 10
                reasons.append("explanation-has-classes-boost")

            if advanced_ctx["ui_actions"]:
                score += 24
                reasons.append("explanation-ui-actions-boost")

            if advanced_ctx["boundaries"]:
                score += 22
                reasons.append("explanation-boundary-boost")

            if advanced_ctx["runtime"] and is_runtime_question:
                score += 34
                reasons.append("explanation-runtime-boost")

            if runtime_anchors:
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
            if any(marker in haystack for marker in explanatory_markers):
                score += 26
                reasons.append("explanation-orchestration-marker-boost")

            if is_auxiliary_ui_path(path) and "help" not in q:
                score -= 25
                reasons.append("explanation-auxiliary-penalty")

        score += retriever._score_advanced_file_context(q, path, tokens, reasons)

        runtime_signal_score, runtime_signal_paths = retriever._score_runtime_signal_matches(
            q,
            reasons,
        )
        if path in runtime_signal_paths:
            score += runtime_signal_score
            reasons.append("runtime-signal-path-boost")

        if is_runtime_question:
            runtime_blob = advanced_ctx["runtime"]

            if runtime_blob:
                score += 80
                reasons.append("runtime-heavy-question-runtime-boost")

            if (
                "runtime_runner_probe_apply_button" in q
                and "runtime_runner_probe_apply_button" in runtime_blob
            ):
                score += 220
                reasons.append("exact-runtime-probe-apply-button-boost")

            if "apply button" in q and (
                "probe apply button clicked" in runtime_blob
                or "on_apply_clicked" in runtime_blob
            ):
                score += 180
                reasons.append("apply-click-runtime-boost")

            if "signal connections" in q and retriever.idx.runtime_events_by_file.get(path):
                score += 120
                reasons.append("runtime-signal-connections-file-boost")

            if "check_runtime_trace_schema.py" in normalized_path:
                score -= 120
                reasons.append("runtime-schema-validator-penalty")

            if "/tooltips/" in normalized_path or "tooltip" in normalized_path:
                score -= 80
                reasons.append("runtime-tooltip-noise-penalty")

            if (
                normalized_path.endswith("/runtime_runner.py")
                or normalized_path == "runtime_runner.py"
                or "/project_reasoner_v10_runtime_collector/" in normalized_path
                or "/runtime_collector/" in normalized_path
            ):
                score += 220
                reasons.append("runtime-collector-path-boost")

            if "runtime probe signal connections" in q and "signal_connection" in runtime_blob:
                score += 180
                reasons.append("runtime-probe-signal-connections-boost")

            if (
                "probe button signal-slot connections" in q
                and "runtime_runner_probe_apply_button" in runtime_blob
            ):
                score += 240
                reasons.append("probe-button-signal-slot-runtime-boost")

            if "on_apply_clicked" in q and "on_apply_clicked" in runtime_blob:
                score += 260
                reasons.append("exact-on-apply-clicked-runtime-boost")

            qt_signal_map = getattr(retriever.idx, "qt_signal_map", [])
            if isinstance(qt_signal_map, list):
                best_signal_score = 0
                for sig_record in qt_signal_map:
                    if not isinstance(sig_record, dict):
                        continue
                    sig_file = str(sig_record.get("source_file", "")).strip()
                    if sig_file != path:
                        continue
                    sig_name = str(sig_record.get("signal_name", "")).lower()
                    target = str(sig_record.get("target", "")).lower()
                    src_sym = str(sig_record.get("source_symbol", "")).lower()
                    combined = sig_name + " " + target + " " + src_sym
                    matched_tokens = [tok for tok in tokens if tok in combined]
                    if not matched_tokens:
                        continue
                    record_score = 120 + (80 if len(matched_tokens) >= 2 else 0)
                    if record_score > best_signal_score:
                        best_signal_score = record_score
                if best_signal_score > 0:
                    score += best_signal_score
                    reasons.append("qt-signal-map-boost")

        if intents.get("uncertainty", False):
            hotspot_count = len(retriever.idx.hotspots_by_file.get(path, []))
            if hotspot_count:
                hotspot_boost = min(120, hotspot_count * 12)
                score += hotspot_boost
                reasons.append(f"uncertainty-hotspot-boost:{hotspot_boost}")

        if score <= 0:
            continue

        detail = retriever._build_compact_file_evidence(path, reasons)
        scored.append(
            EvidenceItem(
                evidence_id="",
                score=score,
                path=path,
                module_name=module_name,
                reason=", ".join(sorted(set(reasons))),
                detail=detail,
            )
        )

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


def build_compact_file_evidence(retriever, path: str, reasons: list[str]) -> str:
    file_record = retriever.idx.files_by_path.get(path, {})
    if not isinstance(file_record, dict):
        file_record = {}

    roles = retriever.idx.semantic_roles.get(path, {}).get("roles", [])
    advanced_ctx = retriever._collect_file_context_blobs(path)
    runtime_anchors, runtime_previews = retriever._get_runtime_anchor_summary(
        path,
        limit=12,
    )

    lines: list[str] = []
    lines.append("Path: " + path)

    module_name = file_record.get(
        "module_name",
        path[:-3].replace("\\", ".").replace("/", ".")
        if path.endswith(".py")
        else path,
    )

    lines.append("Module: " + str(module_name))
    lines.append("Reasons: " + ", ".join(sorted(set(reasons))))

    if roles:
        lines.append("Roles: " + ", ".join(roles))

    entry_markers = file_record.get("entry_markers", [])
    if entry_markers:
        lines.append("Entry markers: " + "; ".join(entry_markers[:6]))

    top_functions: list[str] = []
    for fn in file_record.get("functions", [])[:8]:
        top_functions.append(fn.get("qualname", "") + "@" + str(fn.get("lineno", "")))
    if top_functions:
        lines.append("Functions: " + " | ".join(top_functions))

    top_classes: list[str] = []
    for cls in file_record.get("classes", [])[:6]:
        class_text = cls.get("name", "") + "@" + str(cls.get("lineno", ""))
        methods = cls.get("methods", [])[:4]
        if methods:
            class_text += " methods=" + ",".join([m.get("name", "") for m in methods])
        top_classes.append(class_text)
    if top_classes:
        lines.append("Classes: " + " | ".join(top_classes))

    imports_out = sorted(retriever.idx.import_graph_out.get(path, []))
    if imports_out:
        lines.append("Imports out: " + " | ".join(imports_out[:8]))

    calls_out = sorted(retriever.idx.call_graph_out.get(path, []))
    if calls_out:
        lines.append("Calls out: " + " | ".join(calls_out[:10]))

    docstring = str(file_record.get("docstring", "")).strip()
    if docstring:
        docstring = re.sub(r"\s+", " ", docstring)
        lines.append("Docstring: " + docstring[:500])

    widget_count = len(retriever.idx.widgets_by_file.get(path, []))
    ui_action_count = len(retriever.idx.ui_actions_by_file.get(path, []))
    boundary_count = len(retriever.idx.boundaries_by_file.get(path, []))
    runtime_event_count = len(retriever.idx.runtime_events_by_file.get(path, []))
    hotspot_count = len(retriever.idx.hotspots_by_file.get(path, []))

    lines.append(
        "Advanced context: "
        + f"widgets={widget_count}, "
        + f"ui_actions={ui_action_count}, "
        + f"boundaries={boundary_count}, "
        + f"runtime_events={runtime_event_count}, "
        + f"hotspots={hotspot_count}"
    )

    if advanced_ctx["widgets"]:
        lines.append("Widget context: " + advanced_ctx["widgets"][:350])

    if advanced_ctx["ui_actions"]:
        lines.append("UI action context: " + advanced_ctx["ui_actions"][:350])

    if advanced_ctx["boundaries"]:
        lines.append("Boundary context: " + advanced_ctx["boundaries"][:250])

    if runtime_anchors:
        lines.append("Runtime anchors: " + " | ".join(runtime_anchors))

    if runtime_previews:
        lines.append("Runtime preview: " + " | ".join(runtime_previews[:4]))

    if advanced_ctx["runtime"]:
        lines.append("Runtime context: " + advanced_ctx["runtime"][:800])

    if advanced_ctx["hotspots"]:
        lines.append("Hotspot context: " + advanced_ctx["hotspots"][:250])

    qt_signal_map = getattr(retriever.idx, "qt_signal_map", [])
    if isinstance(qt_signal_map, list):
        sig_lines: list[str] = []
        for sig_record in qt_signal_map:
            if not isinstance(sig_record, dict):
                continue
            if str(sig_record.get("source_file", "")).strip() != path:
                continue
            sig_name = str(sig_record.get("signal_name", "")).strip()
            target = str(sig_record.get("target", "")).strip()
            src_sym = str(sig_record.get("source_symbol", "")).strip()
            if sig_name or target:
                sig_lines.append(
                    sig_name
                    + (" -> " + target if target else "")
                    + (" [" + src_sym + "]" if src_sym else "")
                )
        if sig_lines:
            lines.append("Qt signals: " + " | ".join(sig_lines[:12]))

    return "\n".join(lines)





