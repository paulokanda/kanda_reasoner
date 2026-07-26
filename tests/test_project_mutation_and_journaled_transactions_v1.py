"""Behavior tests for project mutation and journaled transaction boundaries."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest import mock

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import kanda_reasoner_app.engineering_safety.project_mutation_lane as mutation_lane
import kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_completion_apply_bridge as completion_bridge
import kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_journaled_apply_executor as journaled_apply
import kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_refactor_transaction as refactor_transaction
import kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_source_mutation_primitives as mutation_primitives
import kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_transaction_rollback as transaction_rollback
import kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_transaction_store as transaction_store
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_journaled_apply_models import (
    JournaledApplyResult,
)


class ProjectMutationAndJournaledTransactionTests(unittest.TestCase):
    """Exercise real queue, apply, persistence, finalization, and rollback behavior."""

    def _new_stores(
        self,
        root: Path,
    ) -> tuple[
        transaction_store.WorkbenchTransactionStore,
        mutation_lane.ProjectMutationLaneStore,
    ]:
        tx_root = root / "support" / "transactions"
        return (
            transaction_store.WorkbenchTransactionStore(tx_root),
            mutation_lane.ProjectMutationLaneStore(
                tx_root.parent / "project_mutation_lane.sqlite3"
            ),
        )

    def _queue_request(
        self,
        *,
        root: Path,
        lane: mutation_lane.ProjectMutationLaneStore,
        request_id: str,
        transaction_id: str,
        target: Path,
    ) -> mutation_lane.MutationRequest:
        request = mutation_lane.build_mutation_request(
            request_id=request_id,
            project_root=root,
            owner_box="tests/mutation",
            operation_family="TEST_MUTATION",
            transaction_id=transaction_id,
            mutation_paths=[target],
            basis_paths=[target],
        )
        lane.port("tests/mutation").submit(request)
        return request

    def _create_transaction(
        self,
        *,
        store: transaction_store.WorkbenchTransactionStore,
        transaction_id: str,
        request: mutation_lane.MutationRequest,
    ) -> Path:
        return store.create_transaction(
            transaction_id=transaction_id,
            contract_hash="contract-hash",
            snapshot_hash="snapshot-hash",
            baseline_hash="baseline-hash",
            physical_project_id=request.physical_project_id,
            project_root=request.project_root,
            owner_box=request.owner_box,
            mutation_request_id=request.request_id,
        )

    def test_project_mutation_lane_serializes_owner_and_transitions(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "project"
            root.mkdir()
            target = root / "module.py"
            target.write_text("VALUE = 1\n", encoding="utf-8")
            _store, lane = self._new_stores(root)
            request = self._queue_request(
                root=root,
                lane=lane,
                request_id="request-1",
                transaction_id="tx-1",
                target=target,
            )

            self.assertTrue(request.integrity_valid())
            reserved = lane.reserve_next(request.physical_project_id)
            self.assertIsNotNone(reserved)
            self.assertEqual(reserved["state"], "RESERVED")
            self.assertIsNotNone(lane.active_owner(request.physical_project_id))

            lane.transition(request.request_id, "EXECUTING")
            lane.transition(request.request_id, "VALIDATING")
            completed = lane.transition(request.request_id, "COMPLETED")
            self.assertEqual(completed["state"], "COMPLETED")
            self.assertIsNone(lane.active_owner(request.physical_project_id))

            with self.assertRaisesRegex(ValueError, "OWNER_BOX_MISMATCH"):
                lane.port("tests/other").submit(request)

    def test_exact_source_mutation_and_transaction_store_round_trip(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "project"
            root.mkdir()
            target = root / "module.py"
            payload = root / "payload.py"
            target.write_bytes(b"VALUE = 1\n")
            payload.write_bytes(b"VALUE = 2\n")
            old_hash = mutation_primitives.current_file_hash(target)
            new_hash = mutation_primitives.current_file_hash(payload)
            operation = mutation_primitives.SourceMutationOperation(
                schema_version="1.0",
                feature_id=mutation_primitives.SOURCE_MUTATION_PRIMITIVES_FEATURE_ID,
                sequence_no=1,
                operation_type="REPLACE_FILE",
                relative_path="module.py",
                payload_path=str(payload),
                destination_path=str(target),
                payload_hash=new_hash,
                precondition_hash=old_hash,
                destination_existed=True,
                byte_size=payload.stat().st_size,
            )

            resulting_hash = mutation_primitives.apply_source_mutation_operation(
                operation,
                operation_id="tx-op-0001",
            )
            self.assertEqual(resulting_hash, new_hash)
            self.assertEqual(target.read_bytes(), payload.read_bytes())
            self.assertEqual(
                mutation_primitives.verify_source_mutation_operation(operation),
                (True, ""),
            )

            store, lane = self._new_stores(root)
            request = self._queue_request(
                root=root,
                lane=lane,
                request_id="request-store",
                transaction_id="tx-store",
                target=target,
            )
            tx_root = self._create_transaction(
                store=store,
                transaction_id="tx-store",
                request=request,
            )
            digest = store.store_artifact(
                "tx-store",
                "TEST_ARTIFACT",
                {"value": 2},
            )
            self.assertEqual(len(digest), 64)
            self.assertEqual(
                store.load_artifact("tx-store", "TEST_ARTIFACT"),
                {"value": 2},
            )
            self.assertTrue(tx_root.is_dir())

    def test_refactor_transaction_reserves_the_exact_queued_request(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "project"
            root.mkdir()
            target = root / "module.py"
            target.write_text("VALUE = 1\n", encoding="utf-8")
            store, lane = self._new_stores(root)
            request = self._queue_request(
                root=root,
                lane=lane,
                request_id="request-reserve",
                transaction_id="tx-reserve",
                target=target,
            )
            tx_root = self._create_transaction(
                store=store,
                transaction_id="tx-reserve",
                request=request,
            )
            transaction = refactor_transaction.WorkbenchRefactorTransaction(
                schema_version="1.0",
                feature_id="test",
                transaction_id="tx-reserve",
                contract_hash="contract-hash",
                snapshot_hash="snapshot-hash",
                baseline_hash="baseline-hash",
                execution_basis_hash="basis-hash",
                project_root=str(root.resolve()),
                physical_project_id=request.physical_project_id,
                durable_transaction_root=str(tx_root),
                mutation_request_id=request.request_id,
                lane_state="QUEUED",
                transaction_state="PREPARED",
            )

            reserved = refactor_transaction.reserve_workbench_project_lane(
                transaction=transaction,
                transaction_store=store,
                mutation_lane_store=lane,
            )
            self.assertEqual(reserved.lane_state, "RESERVED")
            self.assertEqual(reserved.transaction_state, "LANE_RESERVED")
            self.assertEqual(store.get_transaction("tx-reserve")["state"], "LANE_RESERVED")

    def test_journaled_apply_blocks_before_mutation_and_finalizes_validated_result(self) -> None:
        blocked_transaction = SimpleNamespace(
            transaction_id="tx-blocked",
            durable_transaction_root="support/tx-blocked",
            lane_state="QUEUED",
            transaction_state="PREPARED",
        )
        source_payload = SimpleNamespace(
            target_file="module.py",
            source_content_hash="before",
            preview_root="preview",
        )
        with mock.patch.object(
            journaled_apply,
            "entry_blockers",
            return_value=("BLOCKED_BY_TEST",),
        ):
            blocked = journaled_apply.execute_journaled_refactor_apply(
                transaction=blocked_transaction,
                authorization=SimpleNamespace(),
                execution_basis=SimpleNamespace(),
                sealed_payload=SimpleNamespace(),
                source_payload=source_payload,
                preflight_backup=SimpleNamespace(),
                transaction_store=mock.Mock(),
                mutation_lane_store=mock.Mock(),
            )
        self.assertEqual(blocked.status, "blocked")
        self.assertIn("BLOCKED_BY_TEST", blocked.blockers)

        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "project"
            root.mkdir()
            target = root / "module.py"
            target.write_text("VALUE = 1\n", encoding="utf-8")
            store, lane = self._new_stores(root)
            request = self._queue_request(
                root=root,
                lane=lane,
                request_id="request-finalize",
                transaction_id="tx-finalize",
                target=target,
            )
            self._create_transaction(
                store=store,
                transaction_id="tx-finalize",
                request=request,
            )
            lane.reserve_next(request.physical_project_id)
            lane.transition(request.request_id, "EXECUTING")
            lane.transition(request.request_id, "VALIDATING")
            store.transition_transaction("tx-finalize", "VALIDATING")
            result = JournaledApplyResult(
                schema_version="1.0",
                feature_id="test",
                status="applied",
                transaction_id="tx-finalize",
                target_file=str(target),
                source_content_hash_before="before",
                source_content_hash_after="after",
                preview_root="preview",
                rollback_manifest_path="rollback.json",
                execution_manifest_path="execution.json",
                source_mutation_enabled=True,
                import_rewrite_enabled=False,
                lane_state="VALIDATING",
                transaction_state="VALIDATING",
            )
            terminal = journaled_apply.finalize_journaled_refactor_transaction(
                result=result,
                structural_pass=True,
                behavior_status="BEHAVIOR_VALIDATED_PASS",
                behavior_risk_accepted=False,
                transaction_store=store,
                mutation_lane_store=lane,
            )
            self.assertEqual(terminal, "COMPLETED_VALIDATED")
            self.assertEqual(
                store.get_transaction("tx-finalize")["state"],
                "COMPLETED_VALIDATED",
            )
            self.assertEqual(
                lane.get_request(request.request_id)["state"],
                "COMPLETED",
            )

    def test_journaled_rollback_restores_backup_and_closes_lane(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "project"
            root.mkdir()
            target = root / "module.py"
            payload = root / "payload.py"
            backup = root / "backup.py"
            original = b"VALUE = 1\n"
            changed = b"VALUE = 2\n"
            target.write_bytes(original)
            payload.write_bytes(changed)
            backup.write_bytes(original)
            original_hash = hashlib.sha256(original).hexdigest()
            changed_hash = hashlib.sha256(changed).hexdigest()
            operation = mutation_primitives.SourceMutationOperation(
                schema_version="1.0",
                feature_id=mutation_primitives.SOURCE_MUTATION_PRIMITIVES_FEATURE_ID,
                sequence_no=1,
                operation_type="REPLACE_FILE",
                relative_path="module.py",
                payload_path=str(payload),
                destination_path=str(target),
                payload_hash=changed_hash,
                precondition_hash=original_hash,
                destination_existed=True,
                byte_size=len(changed),
            )
            mutation_primitives.apply_source_mutation_operation(
                operation,
                operation_id="tx-rollback-op-0001",
            )

            store, lane = self._new_stores(root)
            request = self._queue_request(
                root=root,
                lane=lane,
                request_id="request-rollback",
                transaction_id="tx-rollback",
                target=target,
            )
            self._create_transaction(
                store=store,
                transaction_id="tx-rollback",
                request=request,
            )
            lane.reserve_next(request.physical_project_id)
            lane.transition(request.request_id, "EXECUTING")
            operation_id = store.register_operation(
                transaction_id="tx-rollback",
                sequence_no=1,
                operation_type="REPLACE_FILE",
                target_path=str(target),
                precondition_hash=original_hash,
                payload_hash=changed_hash,
                backup_path=str(backup),
            )
            store.record_operation_intent(operation_id)
            store.record_operation_applied(operation_id)
            store.record_operation_verified(operation_id)

            with mock.patch.object(
                transaction_rollback,
                "load_persisted_operation_plan",
                return_value=((operation,), {}),
            ):
                result = transaction_rollback.rollback_journaled_refactor_transaction(
                    transaction_id="tx-rollback",
                    transaction_store=store,
                    mutation_lane_store=lane,
                )

            self.assertEqual(result.status, "rollback_verified")
            self.assertEqual(target.read_bytes(), original)
            self.assertEqual(store.get_transaction("tx-rollback")["state"], "ROLLBACK_VERIFIED")
            self.assertEqual(lane.get_request(request.request_id)["state"], "ROLLED_BACK")

    def test_completion_bridge_keeps_confirmation_gate_and_delegates_rollback(self) -> None:
        blocked_bundle = SimpleNamespace(
            gate=SimpleNamespace(enabled=False, blockers=("HUMAN_REVIEW_REQUIRED",)),
        )
        with self.assertRaisesRegex(RuntimeError, "GATE_BLOCKED"):
            completion_bridge.execute_completion_transaction(
                evidence=None,
                transaction_bundle=blocked_bundle,
                preflight=None,
                source_payload=None,
                executor_proof_available=False,
            )

        sentinel = object()
        bundle = SimpleNamespace(
            transaction=SimpleNamespace(transaction_id="tx-delegate"),
            transaction_store=object(),
            mutation_lane_store=object(),
        )
        with mock.patch.object(
            completion_bridge,
            "rollback_journaled_refactor_transaction",
            return_value=sentinel,
        ) as rollback:
            result = completion_bridge.rollback_completion_transaction(bundle)
        self.assertIs(result, sentinel)
        rollback.assert_called_once_with(
            transaction_id="tx-delegate",
            transaction_store=bundle.transaction_store,
            mutation_lane_store=bundle.mutation_lane_store,
        )


if __name__ == "__main__":
    unittest.main()
