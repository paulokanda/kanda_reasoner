# project-path: tests/test_engineering_diagnostics_wave2u.py
"""Focused contracts for Wave 2U governed Patch Preview."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
import zipfile

from kanda_reasoner_app.engineering_diagnostics import (
    BOM_PRODUCER_ID,
    RUFF_PRODUCER_ID,
    DiagnosticFindingRecord,
    DiagnosticRemediationIntent,
    DiagnosticRunRecord,
    DiagnosticValidationPlan,
)
from kanda_reasoner_app.engineering_diagnostics_patch_preview import (
    build_governed_patch_preview_plan,
    create_governed_patch_preview,
    patch_preview_approval_token,
)
from kanda_reasoner_app.engineering_diagnostics_patch_preview.storage import (
    resolve_patch_preview_paths,
)


def _run(producer_id: str) -> DiagnosticRunRecord:
    return DiagnosticRunRecord(
        run_id="run-" + producer_id,
        attempt_id="attempt-1",
        project_id="project-1",
        project_root_fingerprint="a" * 64,
        producer_id=producer_id,
        producer_version="1.0",
        scan_identity="b" * 64,
        source_fingerprint="c" * 64,
        scope_fingerprint="d" * 64,
        configuration_fingerprint="e" * 64,
        operation_generation=1,
        completion_status="COMPLETED",
        finding_count=1,
        content_digest="f" * 64,
        started_at_utc="2026-08-06T00:00:00Z",
        completed_at_utc="2026-08-06T00:00:01Z",
        provenance={},
    )


def _finding(code: str, path: str = "sample.py") -> DiagnosticFindingRecord:
    return DiagnosticFindingRecord(
        run_id="run",
        issue_fingerprint="1" * 64,
        evidence_digest="2" * 64,
        code=code,
        relative_path=path,
        message="mechanical issue",
        severity="warning",
        confidence="high",
        semantic_key="semantic",
        symbol_id="",
        location_key="line:1",
        category="source_hygiene",
        line=1,
        evidence={
            "fix_available": True,
            "fix_applicability": "safe",
            "fix_message": "Apply exact safe edit.",
        },
        suggested_action="Apply exact safe edit.",
    )


def _intent(finding: DiagnosticFindingRecord, *, frozen: str = "UNFROZEN") -> DiagnosticRemediationIntent:
    return DiagnosticRemediationIntent(
        intent_id="remediation-" + "3" * 64,
        target_issue_fingerprint=finding.issue_fingerprint,
        action_class="SAFE_MECHANICAL_FIX_AVAILABLE",
        likely_correction="Apply exact safe edit.",
        reason="Deterministic safe correction.",
        canonical_owner="sample.py",
        expected_affected_files=(finding.relative_path,),
        frozen_path_impact=frozen,
        governing_freeze_ids=() if frozen == "UNFROZEN" else ("freeze-1",),
        required_governed_wave="",
        fix_applicability="EXACT_FILE",
        mechanical_safety="SAFE_MECHANICAL" if frozen == "UNFROZEN" else "BLOCKED_BY_FREEZE",
        semantic_review_requirement="NOT_REQUIRED",
        validation_plan=DiagnosticValidationPlan(
            focused_tests=("focused",),
            validation_commands=("validate",),
            rollback_expectation="restore exact bytes",
            evidence_required=("evidence",),
        ),
        uncertainty="low",
        primary_trust_source="KANDA_RULE_TEMPLATE",
        rule_template_id="kanda.remediation.test.v1",
        deterministic_evidence=("evidence",),
        project_governance_rules=("governance",),
    )


class EngineeringDiagnosticsWave2UTests(unittest.TestCase):
    """Prove exact-source, isolation, rollback, and human-gate contracts."""

    def _project(self, payload: bytes) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        unique_name = "sample_project_" + Path(temporary.name).name.lower().replace("-", "_")
        root = Path(temporary.name) / unique_name
        root.mkdir()
        (root / "sample.py").write_bytes(payload)
        paths = resolve_patch_preview_paths(root)
        self.addCleanup(shutil.rmtree, paths.support_root, True)
        self.addCleanup(shutil.rmtree, paths.daily_work_root, True)
        return temporary, root

    def test_approval_token_is_issue_bound(self) -> None:
        self.assertEqual(patch_preview_approval_token("a" * 64), "PREVIEW " + "a" * 12)

    def test_plan_requires_patch_prepared_lifecycle(self) -> None:
        temporary, root = self._project(b"\xef\xbb\xbfprint('x')\n")
        self.addCleanup(temporary.cleanup)
        finding = _finding("BOM")
        with self.assertRaisesRegex(ValueError, "PATCH_PREVIEW_REQUIRES_PATCH_PREPARED"):
            build_governed_patch_preview_plan(
                root, _run(BOM_PRODUCER_ID), finding, _intent(finding),
                decision_state="FIX_PLANNED", owner_status="READY",
                approval_token=patch_preview_approval_token(finding.issue_fingerprint),
            )

    def test_frozen_path_is_hard_blocked(self) -> None:
        temporary, root = self._project(b"\xef\xbb\xbfprint('x')\n")
        self.addCleanup(temporary.cleanup)
        finding = _finding("BOM")
        base = _intent(finding)
        intent = SimpleNamespace(**base.__dict__) if hasattr(base, "__dict__") else SimpleNamespace(
            target_issue_fingerprint=base.target_issue_fingerprint,
            action_class=base.action_class,
            mechanical_safety=base.mechanical_safety,
            semantic_review_requirement=base.semantic_review_requirement,
            frozen_path_impact="FROZEN",
            governing_freeze_ids=("freeze-1",),
            expected_affected_files=base.expected_affected_files,
            intent_id=base.intent_id,
        )
        with self.assertRaisesRegex(ValueError, "PATCH_PREVIEW_FROZEN_PATH_HARD_BLOCK"):
            build_governed_patch_preview_plan(
                root, _run(BOM_PRODUCER_ID), finding, intent,
                decision_state="PATCH_PREPARED", owner_status="READY",
                approval_token=patch_preview_approval_token(finding.issue_fingerprint),
            )

    def test_wrong_confirmation_token_is_rejected(self) -> None:
        temporary, root = self._project(b"\xef\xbb\xbfprint('x')\n")
        self.addCleanup(temporary.cleanup)
        finding = _finding("BOM")
        with self.assertRaisesRegex(ValueError, "EXACT_HUMAN_CONFIRMATION"):
            build_governed_patch_preview_plan(
                root, _run(BOM_PRODUCER_ID), finding, _intent(finding),
                decision_state="PATCH_PREPARED", owner_status="READY",
                approval_token="PREVIEW wrong",
            )

    def test_unsupported_ruff_rule_is_rejected(self) -> None:
        temporary, root = self._project(b"print('x')\n")
        self.addCleanup(temporary.cleanup)
        finding = _finding("F841")
        with self.assertRaisesRegex(ValueError, "CORRECTION_KIND_NOT_ELIGIBLE"):
            build_governed_patch_preview_plan(
                root, _run(RUFF_PRODUCER_ID), finding, _intent(finding),
                decision_state="PATCH_PREPARED", owner_status="READY",
                approval_token=patch_preview_approval_token(finding.issue_fingerprint),
            )

    def test_bom_preview_has_exact_diff_and_rollback_zip(self) -> None:
        original = b"\xef\xbb\xbfprint('x')\n"
        temporary, root = self._project(original)
        self.addCleanup(temporary.cleanup)
        finding = _finding("BOM")
        record = create_governed_patch_preview(
            root, _run(BOM_PRODUCER_ID), finding, _intent(finding),
            decision_state="PATCH_PREPARED", owner_status="READY",
            approval_token=patch_preview_approval_token(finding.issue_fingerprint),
        )
        self.assertEqual((root / "sample.py").read_bytes(), original)
        self.assertEqual(record.status, "PREVIEW_READY_FOR_GOVERNED_VALIDATION")
        self.assertIn("-\ufeffprint('x')", Path(record.diff_path).read_text(encoding="utf-8"))
        with zipfile.ZipFile(record.proposal_zip_path) as archive:
            self.assertEqual(
                set(archive.namelist()),
                {"PATCH_PREVIEW.diff", "PATCH_PREVIEW_MANIFEST.json", "VALIDATION_PLAN.txt", "proposed/sample.py"},
            )
            self.assertEqual(archive.read("proposed/sample.py"), b"print('x')\n")
        with zipfile.ZipFile(record.rollback_zip_path) as archive:
            self.assertEqual(
                set(archive.namelist()),
                {"ROLLBACK_MANIFEST.json", "original/sample.py"},
            )
            self.assertEqual(archive.read("original/sample.py"), original)

    def test_repeated_preview_attempts_receive_unique_ids(self) -> None:
        temporary, root = self._project(b"\xef\xbb\xbfprint('x')\n")
        self.addCleanup(temporary.cleanup)
        finding = _finding("BOM")
        kwargs = {
            "decision_state": "PATCH_PREPARED",
            "owner_status": "READY",
            "approval_token": patch_preview_approval_token(finding.issue_fingerprint),
        }
        first = create_governed_patch_preview(
            root, _run(BOM_PRODUCER_ID), finding, _intent(finding), **kwargs
        )
        second = create_governed_patch_preview(
            root, _run(BOM_PRODUCER_ID), finding, _intent(finding), **kwargs
        )
        self.assertNotEqual(first.preview_id, second.preview_id)
        self.assertTrue(Path(first.preview_root).is_dir())
        self.assertTrue(Path(second.preview_root).is_dir())
        self.assertIn("PATCH_PREVIEW_UNIQUE_ATTEMPT_ID: PASS", second.validation_markers)

    def test_preview_manifest_is_non_installable(self) -> None:
        temporary, root = self._project(b"\xef\xbb\xbfprint('x')\n")
        self.addCleanup(temporary.cleanup)
        finding = _finding("BOM")
        record = create_governed_patch_preview(
            root, _run(BOM_PRODUCER_ID), finding, _intent(finding),
            decision_state="PATCH_PREPARED", owner_status="READY",
            approval_token=patch_preview_approval_token(finding.issue_fingerprint),
        )
        manifest = json.loads(Path(record.manifest_path).read_text())
        self.assertFalse(manifest["plan"]["installable"])
        self.assertFalse(manifest["plan"]["source_mutation_allowed"])
        self.assertIn("Validate Project", Path(record.preview_root, "VALIDATION_PLAN.txt").read_text())

    def test_active_source_change_during_preview_fails_closed(self) -> None:
        original = b"\xef\xbb\xbfprint('x')\n"
        temporary, root = self._project(original)
        self.addCleanup(temporary.cleanup)
        finding = _finding("BOM")
        def mutate(path: Path) -> None:
            path.write_text("print('changed')\n", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "ACTIVE_SOURCE_CHANGED"):
            create_governed_patch_preview(
                root, _run(BOM_PRODUCER_ID), finding, _intent(finding),
                decision_state="PATCH_PREPARED", owner_status="READY",
                approval_token=patch_preview_approval_token(finding.issue_fingerprint),
                after_source_read=mutate,
            )
        support = root.parent / "sample_project_show_project_to_AI" / "engineering_diagnostics_patch_preview" / "previews"
        self.assertFalse(support.exists() and any(support.iterdir()))

    def test_ruff_preview_scopes_fix_to_one_rule_and_one_file(self) -> None:
        original = b"import os\nprint('x')\n"
        temporary, root = self._project(original)
        self.addCleanup(temporary.cleanup)
        finding = _finding("F401")
        commands: list[tuple[str, ...]] = []
        def runner(command, _cwd):
            command = tuple(command)
            commands.append(command)
            path = Path(command[-1])
            if "--fix-only" in command:
                path.write_text("print('x')\n", encoding="utf-8")
            return 0, "", ""
        record = create_governed_patch_preview(
            root, _run(RUFF_PRODUCER_ID), finding, _intent(finding),
            decision_state="PATCH_PREPARED", owner_status="READY",
            approval_token=patch_preview_approval_token(finding.issue_fingerprint),
            command_runner=runner,
        )
        self.assertEqual((root / "sample.py").read_bytes(), original)
        self.assertEqual(len(commands), 2)
        self.assertTrue(all(command[command.index("--select") + 1] == "F401" for command in commands))
        self.assertTrue(all(command[-1].endswith("sample.py") for command in commands))
        self.assertIn("PATCH_PREVIEW_GLOBAL_RUFF_FIX_EXECUTED: NO", record.validation_markers)

    def test_disposable_workspace_is_removed(self) -> None:
        temporary, root = self._project(b"\xef\xbb\xbfprint('x')\n")
        self.addCleanup(temporary.cleanup)
        finding = _finding("BOM")
        record = create_governed_patch_preview(
            root, _run(BOM_PRODUCER_ID), finding, _intent(finding),
            decision_state="PATCH_PREPARED", owner_status="READY",
            approval_token=patch_preview_approval_token(finding.issue_fingerprint),
        )
        workspace = root.parent / "sample_project_delete_after_daily_work" / "engineering_diagnostics_patch_preview" / "workspaces" / record.preview_id
        self.assertFalse(workspace.exists())


if __name__ == "__main__":
    unittest.main()
