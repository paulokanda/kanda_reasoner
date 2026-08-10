# project-path: tests/test_project_web_ai_persistence_contracts.py
"""Functional regression protection for Project Web AI persistence owners."""

from __future__ import annotations

import hashlib
import json
import stat
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

import kanda_reasoner_app.reasoner_engine.project_web_ai_apply_receipts as apply_receipts
import kanda_reasoner_app.reasoner_engine.project_web_ai_shadow as project_shadow
import kanda_reasoner_app.reasoner_engine.project_web_ai_write_storage as write_storage
from kanda_reasoner_app.reasoner_engine.project_web_ai_apply_contracts import (
    ProjectWebAIApplyAuthorization,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_change_contracts import (
    ProjectWebAIChangeOperation,
    ProjectWebAIChangeProposal,
    ProjectWebAIChangeTarget,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_source_reader import (
    ExactProjectSourceFile,
)
from kanda_reasoner_app.web_ai_provider_contracts import ProjectWebAIRequestIdentity


def _request_identity(support_root: Path) -> ProjectWebAIRequestIdentity:
    return ProjectWebAIRequestIdentity(
        request_id="request-1",
        session_id="session-1",
        project_id="project-1",
        project_slug="fixture",
        project_root_fingerprint="f" * 64,
        support_root=str(support_root),
        snapshot_id="snapshot-1",
        context_hash="c" * 64,
        gateway_id="gateway-1",
        model_id="model-1",
        privacy_approval_id="privacy-1",
        created_at_utc="2026-08-04T00:00:00+00:00",
        project_epoch=7,
        evidence_context_hash="e" * 64,
    )


def _receipt(
    status: str,
    transaction_id: str,
    completed_at_utc: str,
) -> apply_receipts.ProjectWebAIApplyReceipt:
    return apply_receipts.ProjectWebAIApplyReceipt(
        schema_version="1.0",
        transaction_id=transaction_id,
        authorization_id="authorization-" + transaction_id,
        operation_id="operation-1",
        status=status,
        operation_class="REPLACE_EXISTING_FILES",
        project_id="project-1",
        project_root="C:/fixture",
        project_root_fingerprint="f" * 64,
        project_epoch=7,
        snapshot_id="snapshot-1",
        preview_fingerprint="p" * 64,
        changed_files=("sample.py",),
        source_sha256=("1" * 64,),
        installed_sha256=("2" * 64,),
        backup_root="C:/fixture_daily/backups",
        validation_markers=("PASS",),
        started_at_utc="2026-08-04T00:00:00+00:00",
        completed_at_utc=completed_at_utc,
        error="",
    )


def _authorization() -> ProjectWebAIApplyAuthorization:
    return ProjectWebAIApplyAuthorization(
        authorization_id="authorization-1",
        transaction_id="transaction-1",
        operation_id="operation-1",
        project_id="project-1",
        project_root_fingerprint="f" * 64,
        project_epoch=7,
        snapshot_id="snapshot-1",
        preview_fingerprint="p" * 64,
        target_paths=("sample.py",),
        source_sha256=("1" * 64,),
        proposed_sha256=("2" * 64,),
        authorized_at_utc="2026-08-04T00:00:00+00:00",
    )


class ProjectWebAIPersistenceContractTests(unittest.TestCase):
    """Exercise real receipt, Shadow, and write-storage filesystem boundaries."""

    def test_apply_receipt_persistence_and_freshness_contract(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kanda_receipts_") as temp:
            support_root = Path(temp) / "support"
            support_root.mkdir()

            self.assertEqual(
                apply_receipts.apply_preview_caption(None),
                "View Shadow Preview",
            )
            success = _receipt(
                "APPLIED_SOURCE_VERIFIED",
                "transaction-success",
                "2026-08-04T00:00:01+00:00",
            )
            rollback = _receipt(
                "ROLLED_BACK",
                "transaction-rollback",
                "2026-08-04T00:00:02+00:00",
            )
            self.assertEqual(
                apply_receipts.apply_preview_caption(success),
                "View Applied Preview",
            )
            self.assertTrue(
                apply_receipts.receipt_allows_retry_after_shadow_delete(rollback)
            )
            self.assertFalse(
                apply_receipts.receipt_allows_retry_after_shadow_delete(success)
            )
            self.assertTrue(
                apply_receipts.receipt_matches_fresh_project_context(
                    success,
                    project_id="project-1",
                    project_root_fingerprint="f" * 64,
                )
            )
            self.assertFalse(
                apply_receipts.receipt_matches_fresh_project_context(
                    success,
                    project_id="project-2",
                    project_root_fingerprint="f" * 64,
                )
            )

            receipt_root = apply_receipts.prepare_receipt_root(support_root)
            self.assertTrue(receipt_root.is_dir())
            stored = apply_receipts.write_apply_receipt(support_root, success)
            stored_path = Path(stored.receipt_path)
            self.assertTrue(stored_path.is_file())
            payload = json.loads(stored_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["transaction_id"], success.transaction_id)
            self.assertEqual(payload["status"], "APPLIED_SOURCE_VERIFIED")

            with self.assertRaisesRegex(
                apply_receipts.ProjectWebAIApplyReceiptError,
                "APPLY_RECEIPT_ALREADY_EXISTS",
            ):
                apply_receipts.write_apply_receipt(support_root, success)

            with self.assertRaisesRegex(
                apply_receipts.ProjectWebAIApplyReceiptError,
                "SHOW_PROJECT_TO_AI_REFRESH_REQUIRED_AFTER_APPLY",
            ):
                apply_receipts.assert_project_web_ai_handoff_fresh(
                    support_root,
                    "2026-08-04T00:00:01+00:00",
                )
            apply_receipts.assert_project_web_ai_handoff_fresh(
                support_root,
                "2026-08-04T00:00:03+00:00",
            )

            unresolved = _receipt(
                "UNRESOLVED",
                "transaction-unresolved",
                "2026-08-04T00:00:04+00:00",
            )
            apply_receipts.write_apply_receipt(support_root, unresolved)
            with self.assertRaisesRegex(
                apply_receipts.ProjectWebAIApplyReceiptError,
                "PROJECT_WEB_AI_APPLY_OUTCOME_UNRESOLVED",
            ):
                apply_receipts.assert_project_web_ai_handoff_fresh(
                    support_root,
                    "2026-08-04T00:00:05+00:00",
                )

    def test_shadow_preview_build_delete_and_source_immutability(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kanda_shadow_") as temp:
            root = Path(temp)
            project_root = root / "project"
            daily_root = root / "daily"
            support_root = root / "support"
            project_root.mkdir()
            daily_root.mkdir()
            support_root.mkdir()
            source_path = project_root / "sample.py"
            original = b"value = 1\n"
            source_path.write_bytes(original)
            source = ExactProjectSourceFile(
                relative_path="sample.py",
                sha256=hashlib.sha256(original).hexdigest(),
                size_bytes=len(original),
                text=original.decode("utf-8"),
                had_utf8_bom=False,
                newline="\n",
            )
            request = _request_identity(support_root)
            operation = ProjectWebAIChangeOperation(
                operation_id="operation-shadow",
                request_identity=request,
                project_root=str(project_root),
                daily_work_root=str(daily_root),
                question="Change the value.",
                advisory_answer="Replace one with two.",
                source_files=(source,),
            )
            target = ProjectWebAIChangeTarget(
                relative_path="sample.py",
                expected_sha256=source.sha256,
                unified_diff=(
                    "--- a/sample.py\n"
                    "+++ b/sample.py\n"
                    "@@ -1 +1 @@\n"
                    "-value = 1\n"
                    "+value = 2\n"
                ),
            )
            proposal = ProjectWebAIChangeProposal(
                operation_id=operation.operation_id,
                project_id=request.project_id,
                project_root_fingerprint=request.project_root_fingerprint,
                project_epoch=request.project_epoch,
                snapshot_id=request.snapshot_id,
                summary="Replace fixture value.",
                targets=(target,),
                affected_public_contracts=(),
                required_validators=(),
                known_risks=(),
            )

            preview = project_shadow.build_shadow_preview(operation, proposal)
            self.assertIsInstance(preview, project_shadow.ProjectWebAIShadowPreview)
            self.assertIsInstance(preview.targets[0], project_shadow.ShadowTargetPreview)
            self.assertEqual(source_path.read_bytes(), original)
            self.assertEqual(
                Path(preview.targets[0].shadow_path).read_bytes(),
                b"value = 2\n",
            )
            self.assertIn("PROJECT_SOURCE_UNCHANGED: PASS", preview.validation_markers)
            operation_root = Path(preview.shadow_root).parent
            self.assertTrue(operation_root.is_dir())
            project_shadow.delete_shadow_preview(preview)
            self.assertFalse(operation_root.exists())
            project_shadow.delete_shadow_preview(None)

            mismatched = replace(proposal, operation_id="other-operation")
            with self.assertRaisesRegex(
                project_shadow.ProjectWebAIShadowError,
                "SHADOW_OPERATION_IDENTITY_MISMATCH",
            ):
                project_shadow.build_shadow_preview(operation, mismatched)

            source_path.write_bytes(b"value = 3\n")
            with self.assertRaisesRegex(
                project_shadow.ProjectWebAIShadowError,
                "STALE_SOURCE_HASH:sample.py",
            ):
                project_shadow.build_shadow_preview(operation, proposal)

    def test_write_storage_real_mutation_and_containment_contract(self) -> None:
        with tempfile.TemporaryDirectory(prefix="kanda_storage_") as temp:
            root = Path(temp)
            project_root = root / "project"
            daily_root = root / "daily"
            support_root = root / "support"
            shadow_root = daily_root / "operation" / "shadow"
            for path in (project_root, daily_root, support_root, shadow_root):
                path.mkdir(parents=True, exist_ok=True)

            source_path = project_root / "sample.py"
            source_path.write_bytes(b"value = 1\n")
            source_mode = stat.S_IMODE(source_path.stat().st_mode)
            self.assertEqual(
                write_storage.contained_project_file(
                    project_root,
                    "sample.py",
                ),
                source_path.resolve(),
            )
            with self.assertRaisesRegex(RuntimeError, "APPLY_UNSAFE_RELATIVE_PATH"):
                write_storage.contained_project_file(project_root, "../escape.py")

            shadow_path = shadow_root / "sample.py"
            shadow_path.write_bytes(b"value = 2\n")
            preview = project_shadow.ProjectWebAIShadowPreview(
                operation_id="operation-storage",
                shadow_root=str(shadow_root),
                summary="fixture",
                targets=(),
                affected_public_contracts=(),
                required_validators=(),
                known_risks=(),
                validation_markers=("PASS",),
            )
            self.assertEqual(
                write_storage.contained_shadow_file(preview, "sample.py"),
                shadow_path.resolve(),
            )
            with self.assertRaisesRegex(
                RuntimeError,
                "APPLY_UNSAFE_SHADOW_RELATIVE_PATH",
            ):
                write_storage.contained_shadow_file(preview, "../escape.py")

            write_storage.require_distinct_apply_roots(
                project_root,
                daily_root,
                support_root,
            )
            with self.assertRaisesRegex(
                RuntimeError,
                "APPLY_ROOT_PROJECT_DAILY_OVERLAP",
            ):
                write_storage.require_distinct_apply_roots(
                    project_root,
                    project_root / "daily",
                    support_root,
                )

            backup_root = daily_root / "backups"
            write_storage.write_source_backups(
                backup_root,
                {"sample.py": b"value = 1\n"},
            )
            self.assertEqual(
                (backup_root / "sample.py").read_bytes(),
                b"value = 1\n",
            )
            with self.assertRaises(FileExistsError):
                write_storage.write_source_backups(
                    backup_root,
                    {"sample.py": b"duplicate\n"},
                )

            write_storage.atomic_replace_source(
                source_path,
                b"value = 2\n",
                source_mode,
                "transaction-1",
            )
            self.assertEqual(source_path.read_bytes(), b"value = 2\n")
            temporary = source_path.with_name(
                ".sample.py.kanda-web-ai-transaction-.tmp"
            )
            self.assertFalse(temporary.exists())

            lock_path = daily_root / "apply.lock"
            with write_storage.exclusive_apply_lock(lock_path, "transaction-1"):
                self.assertEqual(
                    lock_path.read_text(encoding="utf-8"),
                    "transaction-1\n",
                )
                with self.assertRaisesRegex(
                    RuntimeError,
                    "APPLY_OPERATION_ALREADY_LOCKED",
                ):
                    with write_storage.exclusive_apply_lock(
                        lock_path,
                        "transaction-2",
                    ):
                        self.fail("nested lock unexpectedly acquired")
            self.assertFalse(lock_path.exists())

            state_path = daily_root / "state" / "transaction.json"
            authorization = _authorization()
            write_storage.write_transaction_state(
                state_path,
                authorization,
                status="PREPARED",
                error="",
                updated_at_utc="2026-08-04T00:00:00+00:00",
                receipt_path="C:/support/receipt.json",
            )
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(state["transaction_id"], authorization.transaction_id)
            self.assertEqual(state["status"], "PREPARED")
            self.assertEqual(
                write_storage.project_web_ai_sha256_bytes(b"abc"),
                hashlib.sha256(b"abc").hexdigest(),
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
