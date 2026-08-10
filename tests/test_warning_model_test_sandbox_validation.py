from __future__ import annotations

from pathlib import Path
import subprocess
import tempfile
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

from kanda_reasoner_app.manage_architecture.warning_model_test_generation_contract import (
    ACTION_CREATE_FOCUSED_TEST,
    ModelTestMutationProposal,
)
from kanda_reasoner_app.manage_architecture.warning_model_test_sandbox_validation import (
    validate_mutation_proposals,
)


def _write(root: Path, relative: str, text: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _fixture(root: Path) -> ModelTestMutationProposal:
    _write(root, "pkg/__init__.py", "")
    _write(root, "pkg/service.py", "def double(value: int) -> int:\n    return value * 2\n")
    _write(
        root,
        "kanda_reasoner_app/manage_architecture/manage_architecture.py",
        "# fake CLI path for injected runner\n",
    )
    code = (
        "from pkg.service import double\n\n"
        "def test_double_contract():\n"
        "    assert double(4) == 8\n"
    )
    return ModelTestMutationProposal(
        source_path="pkg/service.py",
        module_name="pkg.service",
        action=ACTION_CREATE_FOCUSED_TEST,
        target_test_path="tests/test_service.py",
        generated_test_code=code,
        rendered_test_text=code,
        test_sha256_before="",
        confidence=0.95,
        reason="deterministic public function contract",
        model_name="qwen2.5-coder:14b",
    )


def test_disposable_copy_runs_targeted_pytest_then_accepts_fresh_audit_gap_removal() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "project"
        root.mkdir()
        proposal = _fixture(root)
        calls: list[list[str]] = []

        def fake_runner(args, **kwargs):
            del kwargs
            calls.append([str(item) for item in args])
            if "pytest" in args:
                return subprocess.CompletedProcess(args, 0, stdout="1 passed\n", stderr="")
            return subprocess.CompletedProcess(
                args,
                1,
                stdout="ARCHITECTURE VALIDATION SUMMARY\nTotal issues: 0\n",
                stderr="",
            )

        report = validate_mutation_proposals(
            root,
            (proposal,),
            runner=fake_runner,
        )
        assert len(calls) == 2
        assert any("pytest" in call for call in calls)
        assert report.outcomes[0].accepted is True
        sandbox = Path(report.sandbox_root)
        assert sandbox != root
        assert (sandbox / "tests/test_service.py").is_file()
        assert not (root / "tests/test_service.py").exists()


def test_fresh_audit_that_still_reports_source_rejects_mutation() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "project"
        root.mkdir()
        proposal = _fixture(root)

        def fake_runner(args, **kwargs):
            del kwargs
            if "pytest" in args:
                return subprocess.CompletedProcess(args, 0, stdout="1 passed\n", stderr="")
            output = (
                "WARNING TEST_PROTECTION_GAP pkg/service.py :: still unprotected\n"
                "ARCHITECTURE VALIDATION SUMMARY\nTotal issues: 1\n"
            )
            return subprocess.CompletedProcess(args, 1, stdout=output, stderr="")

        report = validate_mutation_proposals(
            root,
            (proposal,),
            runner=fake_runner,
        )
        assert report.outcomes[0].accepted is False
        assert "remained" in report.outcomes[0].reason


def test_target_path_collision_fails_closed_before_acceptance() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "project"
        root.mkdir()
        first = _fixture(root)
        second = ModelTestMutationProposal(
            source_path="pkg/other_service.py",
            module_name="pkg.other_service",
            action=first.action,
            target_test_path=first.target_test_path,
            generated_test_code=first.generated_test_code,
            rendered_test_text=first.rendered_test_text,
            test_sha256_before="",
            confidence=0.93,
            reason="collision fixture",
            model_name=first.model_name,
        )

        def fake_runner(args, **kwargs):
            del kwargs
            return subprocess.CompletedProcess(
                args,
                1,
                stdout="ARCHITECTURE VALIDATION SUMMARY\nTotal issues: 0\n",
                stderr="",
            )

        report = validate_mutation_proposals(
            root,
            (first, second),
            runner=fake_runner,
        )
        assert all(not item.accepted for item in report.outcomes)
        assert all("collision" in item.reason.lower() for item in report.outcomes)


def main() -> int:
    tests = [
        test_disposable_copy_runs_targeted_pytest_then_accepts_fresh_audit_gap_removal,
        test_fresh_audit_that_still_reports_source_rejects_mutation,
        test_target_path_collision_fails_closed_before_acceptance,
    ]
    for test in tests:
        test()
        print(test.__name__ + ": PASS")
    print("WARNING_MODEL_RESOLVER_V2_SANDBOX_VALIDATION_TESTS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
