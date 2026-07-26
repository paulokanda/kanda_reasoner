"""Smoke tests for Batch 15 non-GUI public contract coverage."""

from __future__ import annotations

import kanda_prompt_workspace.prompt_tools.audit_startup_candidates_runner as audit_runner
import kanda_reasoner_app.error_memory.intake_form_builder as intake_form_builder
import kanda_reasoner_app.error_memory.intake_json_parser as intake_json_parser
import kanda_reasoner_app.reasoner_context_bundle.source_tree_exporter_writer as source_tree_exporter_writer
import kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_models as review_models
import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_context as file_retrieval_context
import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_scoring_exact as file_retrieval_scoring_exact
import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_scoring_explain as file_retrieval_scoring_explain
import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_scoring_runtime as file_retrieval_scoring_runtime
import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_scoring_semantic as file_retrieval_scoring_semantic


def test_batch15_non_gui_public_contracts_are_importable() -> None:
    """Verify selected non-GUI public modules remain directly importable."""

    modules = (
        audit_runner,
        intake_form_builder,
        intake_json_parser,
        source_tree_exporter_writer,
        review_models,
        file_retrieval_context,
        file_retrieval_scoring_exact,
        file_retrieval_scoring_explain,
        file_retrieval_scoring_runtime,
        file_retrieval_scoring_semantic,
    )
    for module in modules:
        assert module.__name__
