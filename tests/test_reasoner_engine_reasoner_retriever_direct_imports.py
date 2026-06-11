"""Direct architecture protection for canonical reasoner_retriever modules."""

import unittest

import kanda_reasoner_app.reasoner_engine.reasoner_retriever as reasoner_retriever
import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.bundle_merge as bundle_merge
import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_context_scoring as file_context_scoring
import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval as file_retrieval
import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.live_source_fallback as live_source_fallback
import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.profile_support as profile_support
import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.query_text as query_text
import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.section_retrieval as section_retrieval
import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.snippet_retrieval as snippet_retrieval
import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.symbol_retrieval as symbol_retrieval
import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_help.file_retrieval_impl_private_impl as file_retrieval_impl_private_impl
import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_help.file_retrieval_source_part_1_private_impl as file_retrieval_source_part_1_private_impl
import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_help.file_retrieval_source_part_2_private_impl as file_retrieval_source_part_2_private_impl
import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_help.file_retrieval_source_part_3_private_impl as file_retrieval_source_part_3_private_impl
import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.retriever_consensus_private_impl as retriever_consensus_private_impl
import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.retriever_routing_private_impl as retriever_routing_private_impl
import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.snippet_retrieval_help.snippet_retrieval_part_1_private_impl as snippet_retrieval_part_1_private_impl
import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.snippet_retrieval_help.snippet_retrieval_part_2_private_impl as snippet_retrieval_part_2_private_impl
import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.snippet_retrieval_help.snippet_retrieval_part_3_private_impl as snippet_retrieval_part_3_private_impl
import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.symbol_retrieval_support_private_impl as symbol_retrieval_support_private_impl


class ReasonerEngineReasonerRetrieverDirectImportTests(unittest.TestCase):
    """Keep migrated retriever modules visible to the architecture scanner."""

    def test_public_retriever_modules_are_directly_importable(self):
        modules = [
            reasoner_retriever,
            bundle_merge,
            file_context_scoring,
            file_retrieval,
            live_source_fallback,
            profile_support,
            query_text,
            section_retrieval,
            snippet_retrieval,
            symbol_retrieval,
        ]
        for module in modules:
            self.assertTrue(getattr(module, "__name__", ""))

    def test_private_retriever_parts_are_directly_importable(self):
        modules = [
            file_retrieval_impl_private_impl,
            file_retrieval_source_part_1_private_impl,
            file_retrieval_source_part_2_private_impl,
            file_retrieval_source_part_3_private_impl,
            retriever_consensus_private_impl,
            retriever_routing_private_impl,
            snippet_retrieval_part_1_private_impl,
            snippet_retrieval_part_2_private_impl,
            snippet_retrieval_part_3_private_impl,
            symbol_retrieval_support_private_impl,
        ]
        for module in modules:
            self.assertTrue(getattr(module, "__name__", ""))

    def test_public_contract_functions_are_present(self):
        self.assertTrue(hasattr(bundle_merge, "merge_retrieval_bundles"))
        self.assertTrue(hasattr(file_retrieval, "retrieve_files"))
        self.assertTrue(hasattr(live_source_fallback, "find_live_source_candidates"))
        self.assertTrue(hasattr(query_text, "norm_text"))
        self.assertTrue(hasattr(section_retrieval, "retrieve_packaging_metadata"))
        self.assertTrue(hasattr(snippet_retrieval, "retrieve_snippets"))
        self.assertTrue(hasattr(symbol_retrieval, "retrieve_symbols"))


if __name__ == "__main__":
    unittest.main()
