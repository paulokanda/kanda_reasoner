from __future__ import annotations

import json
from pathlib import Path
import tempfile
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

from kanda_reasoner_app.manage_architecture.warning_heuristic_resolver import WarningFinding
from kanda_reasoner_app.manage_architecture.warning_model_test_protection_resolver import (
    apply_model_test_protection_plan,
    build_model_test_protection_plan,
)
from kanda_reasoner_app.manage_architecture.warning_model_test_protection_context import ModelResolverError


def _write(root: Path, relative: str, text: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _fixture(root: Path) -> WarningFinding:
    _write(root, "pkg/__init__.py", "")
    _write(
        root,
        "pkg/feature_alpha_controller.py",
        '__all__ = ["run_alpha"]\n\ndef run_alpha(value: int) -> int:\n    return value + 1\n',
    )
    _write(
        root,
        "pkg/feature_alpha_helper.py",
        'def run_alpha(value: int) -> int:\n    return value + 1\n',
    )
    _write(
        root,
        "validation/test_alpha_flow.py",
        'import pkg.feature_alpha_helper as helper\n\ndef test_alpha_flow():\n    assert getattr(helper, "run_alpha")(1) == 2\n',
    )
    return WarningFinding(
        code="TEST_PROTECTION_GAP",
        path="pkg/feature_alpha_controller.py",
        message="Important active module has no direct test module import.",
    )


def test_selected_top_model_is_used_exactly_and_model_link_can_apply() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        finding = _fixture(root)
        calls: list[str] = []

        def fake_chat(messages, *, model_selection, temperature, max_tokens):
            calls.append(model_selection)
            payload = {
                "decisions": [
                    {
                        "source_path": "pkg/feature_alpha_controller.py",
                        "action": "link_existing_test",
                        "candidate_test_path": "validation/test_alpha_flow.py",
                        "confidence": 0.96,
                        "reason": "The existing alpha flow test exercises the same alpha behavior through the sibling helper surface.",
                        "evidence_symbols": ["run_alpha"],
                    }
                ]
            }
            return json.dumps(payload), model_selection

        plan = build_model_test_protection_plan(
            root,
            [finding],
            model_selection="qwen3-coder:30b",
            chat_callable=fake_chat,
            model_lister=lambda: ["qwen3-coder:30b", "other-model:7b"],
        )
        assert calls == ["qwen3-coder:30b"]
        assert plan.model_name == "qwen3-coder:30b"
        assert plan.heuristic_safe_count == 0
        assert plan.model_safe_count == 1
        assert plan.web_ai_count == 0

        result = apply_model_test_protection_plan(plan)
        assert result.applied_count == 1
        assert result.changed_files == ("validation/test_alpha_flow.py",)
        updated = (root / "validation/test_alpha_flow.py").read_text(encoding="utf-8")
        assert "if TYPE_CHECKING:" in updated
        assert "import pkg.feature_alpha_controller as _test_protection_feature_alpha_controller" in updated
        assert Path(result.backup_root).is_dir()


def test_unavailable_selected_model_fails_closed_without_chat() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        finding = _fixture(root)
        called = False

        def fake_chat(*args, **kwargs):
            nonlocal called
            called = True
            raise AssertionError("chat must not run")

        try:
            build_model_test_protection_plan(
                root,
                [finding],
                model_selection="missing-model:99b",
                chat_callable=fake_chat,
                model_lister=lambda: ["qwen3-coder:30b"],
            )
        except ModelResolverError as exc:
            assert "not available" in str(exc)
        else:
            raise AssertionError("missing selected model must fail closed")
        assert called is False


def test_ai_cannot_invent_candidate_test_path() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        finding = _fixture(root)

        def fake_chat(messages, *, model_selection, temperature, max_tokens):
            payload = {
                "decisions": [
                    {
                        "source_path": "pkg/feature_alpha_controller.py",
                        "action": "link_existing_test",
                        "candidate_test_path": "validation/test_invented.py",
                        "confidence": 0.99,
                        "reason": "invented",
                        "evidence_symbols": ["run_alpha"],
                    }
                ]
            }
            return json.dumps(payload), model_selection

        plan = build_model_test_protection_plan(
            root,
            [finding],
            model_selection="qwen3-coder:30b",
            chat_callable=fake_chat,
            model_lister=lambda: ["qwen3-coder:30b"],
        )
        assert plan.model_safe_count == 0
        assert plan.web_ai_count == 1


def test_invalid_json_retries_once_then_accepts_valid_contract() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        finding = _fixture(root)
        calls = 0

        def fake_chat(messages, *, model_selection, temperature, max_tokens):
            nonlocal calls
            calls += 1
            if calls == 1:
                return "not json", model_selection
            payload = {
                "decisions": [
                    {
                        "source_path": "pkg/feature_alpha_controller.py",
                        "action": "web_ai",
                        "candidate_test_path": "",
                        "confidence": 0.40,
                        "reason": "The relationship is ambiguous.",
                        "evidence_symbols": [],
                    }
                ]
            }
            return json.dumps(payload), model_selection

        plan = build_model_test_protection_plan(
            root,
            [finding],
            model_selection="qwen3-coder:30b",
            chat_callable=fake_chat,
            model_lister=lambda: ["qwen3-coder:30b"],
        )
        assert calls == 2
        assert plan.model_safe_count == 0
        assert plan.web_ai_count == 1


def test_auto_top_selector_uses_first_dynamic_ollama_model() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        finding = _fixture(root)
        used: list[str] = []

        def fake_chat(messages, *, model_selection, temperature, max_tokens):
            used.append(model_selection)
            payload = {
                "decisions": [
                    {
                        "source_path": "pkg/feature_alpha_controller.py",
                        "action": "web_ai",
                        "candidate_test_path": "",
                        "confidence": 0.2,
                        "reason": "ambiguous",
                        "evidence_symbols": [],
                    }
                ]
            }
            return json.dumps(payload), model_selection

        plan = build_model_test_protection_plan(
            root,
            [finding],
            model_selection="Auto (first available Ollama model)",
            chat_callable=fake_chat,
            model_lister=lambda: ["model-a:14b", "model-b:32b"],
        )
        assert used == ["model-a:14b"]
        assert plan.model_name == "model-a:14b"



def test_canonical_adapter_chat_exact_never_falls_back_to_other_model() -> None:
    from kanda_reasoner_app.manage_architecture.ai_review.adapter import (
        Tab1AIReviewAdapter,
    )

    calls: list[str] = []

    class Registry:
        def list_models(self):
            return ["model-a:14b", "model-b:32b"]

    class AI:
        def chat(self, messages, *, model, temperature, max_tokens, use_cache):
            calls.append(model)
            return "ok"

    adapter = Tab1AIReviewAdapter(
        registry_factory=Registry,
        ai_factory=AI,
    )
    text, used = adapter.chat_exact(
        [{"role": "user", "content": "test"}],
        model_name="model-b:32b",
        temperature=0.0,
        max_tokens=50,
    )
    assert text == "ok"
    assert used == "model-b:32b"
    assert calls == ["model-b:32b"]

    try:
        adapter.chat_exact(
            [{"role": "user", "content": "test"}],
            model_name="missing:99b",
            temperature=0.0,
            max_tokens=50,
        )
    except RuntimeError as exc:
        assert "not available" in str(exc)
    else:
        raise AssertionError("chat_exact must fail closed for unavailable selection")
    assert calls == ["model-b:32b"]


def main() -> int:
    tests = [
        test_selected_top_model_is_used_exactly_and_model_link_can_apply,
        test_unavailable_selected_model_fails_closed_without_chat,
        test_ai_cannot_invent_candidate_test_path,
        test_invalid_json_retries_once_then_accepts_valid_contract,
        test_auto_top_selector_uses_first_dynamic_ollama_model,
        test_canonical_adapter_chat_exact_never_falls_back_to_other_model,
    ]
    for test in tests:
        test()
        print(test.__name__ + ": PASS")
    print("WARNING_MODEL_RESOLVER_TEST_PROTECTION_FOCUSED_TESTS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
