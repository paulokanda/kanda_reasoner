"""Smoke coverage for Batch 18 public ownership repair."""

from __future__ import annotations

import importlib


def test_batch18_patch_delivery_facade_owns_public_validator_symbols() -> None:
    """The facade remains the only public owner of patch-delivery validator symbols."""

    facade = importlib.import_module("scripts.validate_ai_response_patch_delivery")
    assert facade.__all__ == [
        "ResponseValidationError",
        "validate_response_text",
        "validate_zip_member_names",
    ]
    assert isinstance(facade.ResponseValidationError, type)
    assert callable(facade.validate_response_text)
    assert callable(facade.validate_zip_member_names)


def test_batch18_patch_delivery_helpers_are_implementation_only() -> None:
    """Helper modules must not claim duplicate public ownership via __all__."""

    helper_names = [
        "scripts.validate_ai_response_patch_delivery_contract",
        "scripts.validate_ai_response_patch_delivery_audit_runner",
        "scripts.validate_ai_response_patch_delivery_text_helpers",
    ]
    for module_name in helper_names:
        module = importlib.import_module(module_name)
        assert getattr(module, "__all__") == []


def test_batch18_new_retriever_mixins_keep_public_class_contracts() -> None:
    """Batch 17 retriever mixin modules have direct public-contract coverage."""

    expected = {
        "kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.retriever_core_mixin": "ProjectRetrieverCoreMixin",
        "kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.retriever_intent_section_mixin": "ProjectRetrieverIntentSectionMixin",
        "kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.retriever_snippet_evidence_mixin": "ProjectRetrieverSnippetEvidenceMixin",
    }
    for module_name, symbol_name in expected.items():
        module = importlib.import_module(module_name)
        assert module.__all__ == [symbol_name]
        assert isinstance(getattr(module, symbol_name), type)


def test_batch18_batch17_validator_has_direct_smoke_coverage() -> None:
    """Batch 17 validator is directly imported through its narrow public contract."""

    validator = importlib.import_module("scripts.validate_architecture_warning_cleanup_batch17_line_count_smoke_v1")
    assert validator.__all__ == ["main"]
    assert callable(validator.main)
