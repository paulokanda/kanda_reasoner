"""Public-contract regression tests for three Tool lazy-tab owner repairs."""

from __future__ import annotations

import unittest


class ToolLazyTabOwnerRepairTests(unittest.TestCase):
    def test_journaled_authorization_uses_public_model_contract(self) -> None:
        from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import (
            build_journaled_apply_authorization,
        )

        authorization = build_journaled_apply_authorization(
            transaction_id="tx-test",
            contract_hash="c" * 64,
            payload_hash="p" * 64,
            semantic_reviewed=True,
            warnings_acknowledged=True,
            transaction_summary_confirmed=True,
            executor_proof_available=True,
        )
        self.assertTrue(authorization.integrity_valid())

    def test_widget_registry_uses_direct_canonical_owners(self) -> None:
        from kanda_reasoner_app.reasoner_context_collector.collector_widget_registry import (
            build_widget_registry,
        )

        source = """
from PySide6.QtWidgets import QPushButton, QVBoxLayout
layout = QVBoxLayout()
button = QPushButton('Run')
button.setToolTip('Execute')
layout.addWidget(button)
"""
        result = build_widget_registry(
            [{"path": "sample.py", "source": source}]
        )
        records = list(result.values())
        self.assertTrue(records)
        self.assertTrue(
            any(record.get("display_text") == "Run" for record in records)
        )
        self.assertTrue(
            any(record.get("tooltip_text") == "Execute" for record in records)
        )
        self.assertTrue(any(record.get("layout_records") for record in records))

    def test_prompt_snapshot_is_owned_by_models_contract(self) -> None:
        from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_models import (
            PromptSnapshot,
        )
        from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_session_capture import (
            build_ml_advisory_prompt_context_snapshot,
        )

        snapshot = PromptSnapshot.from_mapping(
            {
                "prompt_id": "p1",
                "prompt_name": "Prompt",
                "prompt_path": "prompts/p1.md",
                "prompt_hash": "h",
                "prompt_summary": "summary",
            }
        )
        self.assertEqual(snapshot.prompt_id, "p1")
        advisory = build_ml_advisory_prompt_context_snapshot(question="question")
        self.assertIsInstance(advisory, PromptSnapshot)


if __name__ == "__main__":
    unittest.main()
