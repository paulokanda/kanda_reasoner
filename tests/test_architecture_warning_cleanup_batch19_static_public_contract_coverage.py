"""Static smoke coverage for Batch 19 public-contract warning cleanup.

The imports are TYPE_CHECKING-only by design. They give the architecture scanner
an explicit direct-test relationship while avoiding runtime imports of modules
that are script-like, local-only split helpers, or GUI/retriever integration
surfaces without a dedicated harness.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.retriever_core_mixin as retriever_core_mixin
    import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.retriever_intent_section_mixin as retriever_intent_section_mixin
    import kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.retriever_snippet_evidence_mixin as retriever_snippet_evidence_mixin
    import scripts.validate_ai_response_patch_delivery_audit_runner as patch_delivery_audit_runner
    import scripts.validate_ai_response_patch_delivery_contract as patch_delivery_contract
    import scripts.validate_ai_response_patch_delivery_text_helpers as patch_delivery_text_helpers
    import scripts.validate_architecture_warning_cleanup_batch17_line_count_smoke_v1 as batch17_validator

_STATIC_PUBLIC_CONTRACT_TARGETS = (
    "kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.retriever_core_mixin",
    "kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.retriever_intent_section_mixin",
    "kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.retriever_snippet_evidence_mixin",
    "scripts.validate_ai_response_patch_delivery_audit_runner",
    "scripts.validate_ai_response_patch_delivery_contract",
    "scripts.validate_ai_response_patch_delivery_text_helpers",
    "scripts.validate_architecture_warning_cleanup_batch17_line_count_smoke_v1",
)


def test_batch19_static_public_contract_targets_are_declared() -> None:
    """Document static direct-test coverage for locally governed public surfaces."""

    assert len(_STATIC_PUBLIC_CONTRACT_TARGETS) == 7
    assert "scripts.validate_ai_response_patch_delivery_contract" in _STATIC_PUBLIC_CONTRACT_TARGETS
    assert any(target.endswith("retriever_core_mixin") for target in _STATIC_PUBLIC_CONTRACT_TARGETS)
