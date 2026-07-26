from __future__ import annotations

from pathlib import Path
import subprocess
import tempfile

from kanda_reasoner_app.manage_architecture.warning_model_live_audit import (
    FreshTestProtectionAudit,
    apply_and_verify_model_plan,
    run_fresh_test_protection_audit,
)
from kanda_reasoner_app.manage_architecture.warning_model_test_apply import (
    ModelTestProtectionApplyResult,
    apply_validated_model_test_changes,
)
from kanda_reasoner_app.manage_architecture.warning_test_protection_gap_resolver import (
    ACTION_LINK_EXISTING_TEST,
    TestProtectionGapDecision,
)


def _decision(test_sha: str) -> TestProtectionGapDecision:
    return TestProtectionGapDecision(
        source_path="pkg/source.py",
        module_name="pkg.source",
        action=ACTION_LINK_EXISTING_TEST,
        reason="test",
        source_public_symbols=("run",),
        candidate_test_path="tests/test_source.py",
        candidate_score=20,
        candidate_reasons=("references_source_public_symbol",),
        test_sha256_before=test_sha,
    )


def test_fresh_audit_uses_subprocess_output_not_gui_text() -> None:
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        cli = root / "kanda_reasoner_app/manage_architecture/manage_architecture.py"
        cli.parent.mkdir(parents=True)
        cli.write_text("# fixture\n", encoding="utf-8")
        output = """WARNING TEST_PROTECTION_GAP pkg/source.py :: gap\nARCHITECTURE VALIDATION SUMMARY\n"""

        def runner(*args, **kwargs):
            return subprocess.CompletedProcess(args=args[0], returncode=1, stdout=output, stderr="")

        result = run_fresh_test_protection_audit(root, runner=runner)
        assert result.source_paths == frozenset({"pkg/source.py"})
        assert len(result.findings) == 1


def test_noop_link_is_not_reported_as_applied() -> None:
    import hashlib

    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        test_path = root / "tests/test_source.py"
        test_path.parent.mkdir(parents=True)
        original = "from typing import TYPE_CHECKING\nif TYPE_CHECKING:\n    import pkg.source as _test_protection_source\n"
        test_path.write_text(original, encoding="utf-8")
        digest = hashlib.sha256(original.encode("utf-8")).hexdigest()
        result = apply_validated_model_test_changes(root, (_decision(digest),), ())
        assert result.linked_count == 0
        assert result.applied_count == 0
        assert result.changed_files == ()


def test_apply_verify_compares_fresh_before_and_after_paths() -> None:
    class Plan:
        project_root = "/tmp/project"
        decisions = (
            type("Decision", (), {"source_path": "pkg/source.py", "action": "link_existing_test"})(),
        )

    audits = iter(
        (
            FreshTestProtectionAudit("before", (), frozenset({"pkg/source.py", "pkg/hidden.py"}), 1),
            FreshTestProtectionAudit("after", (), frozenset({"pkg/hidden.py", "pkg/new.py"}), 1),
        )
    )

    def audit_func(root):
        return next(audits)

    def apply_func(plan):
        return ModelTestProtectionApplyResult(1, 0, ("tests/test_source.py",), "/backup")

    result = apply_and_verify_model_plan(Plan(), audit_func=audit_func, apply_func=apply_func)
    assert result.resolved_source_paths == ("pkg/source.py",)
    assert result.still_present_source_paths == ()
    assert result.newly_surfaced_paths == ("pkg/new.py",)


def test_stale_plan_blocks_before_write() -> None:
    class Plan:
        project_root = "/tmp/project"
        decisions = (
            type("Decision", (), {"source_path": "pkg/source.py", "action": "link_existing_test"})(),
        )

    called = {"apply": False}

    def audit_func(root):
        return FreshTestProtectionAudit("before", (), frozenset(), 1)

    def apply_func(plan):
        called["apply"] = True
        raise AssertionError("must not apply")

    try:
        apply_and_verify_model_plan(Plan(), audit_func=audit_func, apply_func=apply_func)
    except RuntimeError as exc:
        assert "MODEL PLAN STALE" in str(exc)
    else:
        raise AssertionError("stale plan must fail")
    assert called["apply"] is False


if __name__ == "__main__":
    test_fresh_audit_uses_subprocess_output_not_gui_text()
    test_noop_link_is_not_reported_as_applied()
    test_apply_verify_compares_fresh_before_and_after_paths()
    test_stale_plan_blocks_before_write()
    print("WARNING_MODEL_STATE_REFRESH_VERIFIED_APPLY_DIRECT_TESTS: PASS")
