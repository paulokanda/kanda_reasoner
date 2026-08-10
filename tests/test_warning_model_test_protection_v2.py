from __future__ import annotations

import json
from pathlib import Path
import tempfile
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kanda_reasoner_app.manage_architecture.warning_model_test_sandbox_validation import (
        SandboxValidationReport,
    )

from kanda_reasoner_app.manage_architecture.warning_heuristic_resolver import WarningFinding
from kanda_reasoner_app.manage_architecture.warning_model_test_generation_contract import (
    ACTION_CREATE_FOCUSED_TEST,
    build_mutation_proposal,
)
from kanda_reasoner_app.manage_architecture.warning_model_test_protection_context import (
    build_model_source_context,
    iter_test_files,
)
from kanda_reasoner_app.manage_architecture.warning_model_test_protection_resolver import (
    apply_model_test_protection_plan,
    build_model_test_protection_plan,
)
from kanda_reasoner_app.manage_architecture.warning_model_test_sandbox_validation import (
    SandboxMutationOutcome,
    SandboxValidationReport,
)
from kanda_reasoner_app.manage_architecture.warning_test_protection_gap_resolver import (
    ACTION_WEB_AI,
    TestProtectionGapDecision,
)


def _write(root: Path, relative: str, text: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _finding() -> WarningFinding:
    return WarningFinding(
        code="TEST_PROTECTION_GAP",
        path="pkg/calculator_service.py",
        message="Important active module has no direct test module import.",
    )


def _fixture(root: Path) -> None:
    _write(root, "pkg/__init__.py", "")
    _write(
        root,
        "pkg/calculator_service.py",
        '__all__ = ["add"]\n\n'
        'def _private_noise(value: int) -> int:\n'
        '    return value * 100\n\n'
        'def add(left: int, right: int) -> int:\n'
        '    if left < 0 and right < 0:\n'
        '        raise ValueError("both values cannot be negative")\n'
        '    return left + right\n',
    )
    _write(
        root,
        "pkg/calculator_helper.py",
        "def add(left: int, right: int) -> int:\n    return left + right\n",
    )
    _write(
        root,
        "validation/test_calculator_flow.py",
        "import pkg.calculator_helper as helper\n\n"
        "def test_calculator_flow():\n"
        "    assert helper.add(2, 3) == 5\n",
    )


def _create_payload() -> dict[str, object]:
    return {
        "source_path": "pkg/calculator_service.py",
        "action": ACTION_CREATE_FOCUSED_TEST,
        "candidate_test_path": "",
        "target_test_path": "tests/test_calculator_service.py",
        "confidence": 0.95,
        "reason": "The public add contract has deterministic success and error behavior.",
        "evidence_symbols": ["add"],
        "test_code": (
            "from pkg.calculator_service import add\n\n"
            "def test_add_contract():\n"
            "    assert add(2, 3) == 5\n"
        ),
    }


def test_semantic_context_uses_ast_selected_public_body_and_richer_candidate_evidence() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _fixture(root)
        source = root / "pkg/calculator_service.py"
        padded = '# noise\n' * 400 + source.read_text(encoding="utf-8")
        source.write_text(padded, encoding="utf-8")
        decision = TestProtectionGapDecision(
            source_path="pkg/calculator_service.py",
            module_name="pkg.calculator_service",
            action=ACTION_WEB_AI,
            candidate_test_path="",
            candidate_score=0,
            candidate_reasons=(),
            source_public_symbols=("add",),
            test_sha256_before="",
            reason="gap",
        )
        context = build_model_source_context(root, decision, iter_test_files(root))
        assert context is not None
        assert "def add" in context.source_excerpt
        assert "return left + right" in context.source_excerpt
        assert context.suggested_new_test_path == "tests/test_calculator_service.py"
        assert context.candidates
        candidate = context.candidates[0]
        assert "test_calculator_flow" in candidate.test_functions
        assert candidate.assertion_symbols


def test_create_focused_test_can_be_sandbox_accepted_and_applied_after_confirmation_layer() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _fixture(root)
        chat_calls: list[str] = []

        def fake_chat(messages, *, model_selection, temperature, max_tokens):
            del messages, temperature, max_tokens
            chat_calls.append(model_selection)
            return json.dumps({"decisions": [_create_payload()]}), model_selection

        def fake_sandbox(project_root, proposals, *, progress_callback=None):
            assert Path(project_root) == root
            assert len(proposals) == 1
            proposal = proposals[0]
            assert proposal.target_test_path == "tests/test_calculator_service.py"
            if progress_callback is not None:
                progress_callback(1, 0, 1, 0, proposal.target_test_path, "sandbox_audit")
            return SandboxValidationReport(
                sandbox_root=str(root.parent / "disposable"),
                outcomes=(
                    SandboxMutationOutcome(
                        source_path=proposal.source_path,
                        target_test_path=proposal.target_test_path,
                        accepted=True,
                        reason="Targeted pytest passed and gap disappeared.",
                    ),
                ),
                targeted_pytest_return_codes=((proposal.target_test_path, 0),),
                audit_return_code=1,
            )

        plan = build_model_test_protection_plan(
            root,
            [_finding()],
            model_selection="qwen2.5-coder:14b",
            chat_callable=fake_chat,
            model_lister=lambda: ["qwen2.5-coder:14b"],
            sandbox_validator=fake_sandbox,
        )
        assert chat_calls == ["qwen2.5-coder:14b"]
        assert plan.model_test_change_count == 1
        assert plan.safe_change_count == 1
        assert plan.web_ai_count == 0
        assert len(plan.mutations) == 1
        result = apply_model_test_protection_plan(plan)
        assert result.mutated_test_count == 1
        assert result.linked_count == 0
        created = root / "tests/test_calculator_service.py"
        assert created.is_file()
        assert "assert add(2, 3) == 5" in created.read_text(encoding="utf-8")


def test_sandbox_rejection_keeps_test_change_in_web_ai_lane() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _fixture(root)

        def fake_chat(messages, *, model_selection, temperature, max_tokens):
            del messages, temperature, max_tokens
            return json.dumps({"decisions": [_create_payload()]}), model_selection

        def reject_sandbox(project_root, proposals, *, progress_callback=None):
            del project_root, progress_callback
            proposal = proposals[0]
            return SandboxValidationReport(
                sandbox_root="sandbox",
                outcomes=(
                    SandboxMutationOutcome(
                        source_path=proposal.source_path,
                        target_test_path=proposal.target_test_path,
                        accepted=False,
                        reason="Targeted pytest failed.",
                    ),
                ),
                targeted_pytest_return_codes=((proposal.target_test_path, 1),),
                audit_return_code=1,
            )

        plan = build_model_test_protection_plan(
            root,
            [_finding()],
            model_selection="qwen2.5-coder:14b",
            chat_callable=fake_chat,
            model_lister=lambda: ["qwen2.5-coder:14b"],
            sandbox_validator=reject_sandbox,
        )
        assert plan.model_test_change_count == 0
        assert plan.web_ai_count == 1
        assert plan.mutations == ()
        assert "Targeted pytest failed" in plan.decisions[0].reason


def test_generation_contract_rejects_import_only_and_assert_true_silencers() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _fixture(root)
        decision = TestProtectionGapDecision(
            source_path="pkg/calculator_service.py",
            module_name="pkg.calculator_service",
            action=ACTION_WEB_AI,
            candidate_test_path="",
            candidate_score=0,
            candidate_reasons=(),
            source_public_symbols=("add",),
            test_sha256_before="",
            reason="gap",
        )
        context = build_model_source_context(root, decision, iter_test_files(root))
        assert context is not None
        payload = _create_payload()
        payload["test_code"] = (
            "from pkg.calculator_service import add\n\n"
            "def test_fake_smoke():\n"
            "    assert True\n"
        )
        try:
            build_mutation_proposal(root, context, payload, "qwen2.5-coder:14b")
        except ValueError as exc:
            assert "assertion" in str(exc).lower()
        else:
            raise AssertionError("assert True warning silencer must be rejected")


def test_progress_emits_review_phase_before_blocking_model_call() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _fixture(root)
        events: list[tuple[str, str]] = []

        def fake_chat(messages, *, model_selection, temperature, max_tokens):
            del messages, temperature, max_tokens
            assert events and events[-1][1] == "local_ai_reviewing"
            payload = _create_payload()
            payload["action"] = "web_ai"
            payload["target_test_path"] = ""
            payload["test_code"] = ""
            return json.dumps({"decisions": [payload]}), model_selection

        def progress(total, to_go, done, web_ai, source_path, action):
            del total, to_go, done, web_ai
            events.append((source_path, action))

        plan = build_model_test_protection_plan(
            root,
            [_finding()],
            model_selection="qwen2.5-coder:14b",
            chat_callable=fake_chat,
            model_lister=lambda: ["qwen2.5-coder:14b"],
            progress_callback=progress,
        )
        assert plan.web_ai_count == 1
        assert any(action == "local_ai_reviewing" for _, action in events)


def main() -> int:
    tests = [
        test_semantic_context_uses_ast_selected_public_body_and_richer_candidate_evidence,
        test_create_focused_test_can_be_sandbox_accepted_and_applied_after_confirmation_layer,
        test_sandbox_rejection_keeps_test_change_in_web_ai_lane,
        test_generation_contract_rejects_import_only_and_assert_true_silencers,
        test_progress_emits_review_phase_before_blocking_model_call,
    ]
    for test in tests:
        test()
        print(test.__name__ + ": PASS")
    print("WARNING_MODEL_RESOLVER_V2_SEMANTIC_AND_GENERATION_TESTS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
