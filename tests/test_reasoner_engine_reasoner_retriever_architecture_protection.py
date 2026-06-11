"""Direct architecture-protection imports for reasoner_retriever."""

from __future__ import annotations

import unittest

from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help import bundle_merge
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help import file_context_scoring
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help import file_retrieval
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help import live_source_fallback
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help import profile_support
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help import query_text
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help import section_retrieval
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help import snippet_retrieval
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help import symbol_retrieval
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help import retriever_consensus_private_impl
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help import retriever_routing_private_impl
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help import symbol_retrieval_support_private_impl
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_help import file_retrieval_impl_private_impl
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_help import file_retrieval_source_part_1_private_impl
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_help import file_retrieval_source_part_2_private_impl
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_help import file_retrieval_source_part_3_private_impl
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.snippet_retrieval_help import snippet_retrieval_part_1_private_impl
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.snippet_retrieval_help import snippet_retrieval_part_2_private_impl
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.snippet_retrieval_help import snippet_retrieval_part_3_private_impl


class ReasonerEngineReasonerRetrieverArchitectureProtectionTests(unittest.TestCase):
    """Keep migrated retriever modules visible to architecture validation."""

    def test_public_retriever_helper_contracts_are_directly_importable(self) -> None:
        modules = [
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
            with self.subTest(module=module.__name__):
                self.assertTrue(hasattr(module, "__all__"), module.__name__)

    def test_private_retriever_parts_are_directly_importable(self) -> None:
        modules = [
            retriever_consensus_private_impl,
            retriever_routing_private_impl,
            symbol_retrieval_support_private_impl,
            file_retrieval_impl_private_impl,
            file_retrieval_source_part_1_private_impl,
            file_retrieval_source_part_2_private_impl,
            file_retrieval_source_part_3_private_impl,
            snippet_retrieval_part_1_private_impl,
            snippet_retrieval_part_2_private_impl,
            snippet_retrieval_part_3_private_impl,
        ]

        for module in modules:
            with self.subTest(module=module.__name__):
                self.assertIsNotNone(module)

    def test_query_text_basic_helpers_match_current_contract(self) -> None:
        self.assertEqual(query_text.norm_text("  Hello  WORLD  "), "hello  world")
        self.assertEqual(query_text.file_name_from_path("a/b/c.py"), "c.py")


if __name__ == "__main__":
    unittest.main()
