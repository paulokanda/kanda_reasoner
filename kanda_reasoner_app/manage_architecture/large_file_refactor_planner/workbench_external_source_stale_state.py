# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_external_source_stale_state.py
"""Detect and invalidate Workbench transactions after external source mutation."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .models import SCHEMA_VERSION
from .workbench_execution_basis import execution_basis_is_fresh

__all__ = [
    "WORKBENCH_EXTERNAL_SOURCE_STALE_FEATURE_ID",
    "STALE_AFTER_EXTERNAL_SOURCE_MUTATION",
    "EXTERNAL_SOURCE_STALE_MESSAGE",
    "WorkbenchExternalSourceStaleState",
    "detect_external_source_stale_state",
    "invalidate_external_source_stale_transaction",
    "sync_external_source_stale_state_from_window",
]

WORKBENCH_EXTERNAL_SOURCE_STALE_FEATURE_ID = (
    "architecture-review-large-file-refactor-external-source-stale-state-v1"
)
STALE_AFTER_EXTERNAL_SOURCE_MUTATION = "STALE_AFTER_EXTERNAL_SOURCE_MUTATION"
EXTERNAL_SOURCE_STALE_MESSAGE = (
    "The project source changed outside this Workbench transaction. "
    "Reload the card and create a fresh pipeline."
)

# Once the Workbench mutation lane owns source mutation, drift against the
# pre-apply basis is expected and must not be reclassified as external drift.
_WORKBENCH_OWNED_OR_RETIRED_STATES = {
    "LANE_RESERVED",
    "EXECUTING",
    "VALIDATING",
    "RECOVERY_PENDING",
    "ROLLBACK_PENDING",
    "COMPLETED_VALIDATED",
    "COMPLETED_WITH_BEHAVIOR_RISK_ACCEPTED",
    "ROLLBACK_VERIFIED",
    "ABANDONED",
}


@dataclass(frozen=True)
class WorkbenchExternalSourceStaleState:
    """Read-only classification and optional invalidation outcome."""

    schema_version: str
    feature_id: str
    status: str
    stale: bool
    invalidated: bool
    transaction_id: str
    transaction_state: str
    lane_state: str
    message: str
    blockers: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready state record."""
        data = asdict(self)
        data["blockers"] = list(self.blockers)
        return data


def detect_external_source_stale_state(
    *,
    execution_basis: Any,
    transaction_bundle: Any = None,
) -> WorkbenchExternalSourceStaleState:
    """Classify pre-apply external source drift without changing source."""
    transaction = getattr(transaction_bundle, "transaction", None)
    authoritative = _authoritative_transaction_state(transaction_bundle)

    if authoritative.transaction_state == STALE_AFTER_EXTERNAL_SOURCE_MUTATION:
        return _state(
            status=STALE_AFTER_EXTERNAL_SOURCE_MUTATION,
            stale=True,
            invalidated=True,
            transaction=transaction,
            transaction_state=authoritative.transaction_state,
            lane_state=authoritative.lane_state,
            blockers=authoritative.blockers,
        )

    if authoritative.transaction_state in _WORKBENCH_OWNED_OR_RETIRED_STATES:
        return _state(
            status="WORKBENCH_TRANSACTION_OWNS_OR_RETIRES_SOURCE_CHANGE",
            stale=False,
            transaction=transaction,
            transaction_state=authoritative.transaction_state,
            lane_state=authoritative.lane_state,
            blockers=authoritative.blockers,
        )

    if execution_basis is None:
        return _state(
            status="NO_EXECUTION_BASIS",
            stale=False,
            transaction=transaction,
            transaction_state=authoritative.transaction_state,
            lane_state=authoritative.lane_state,
            blockers=authoritative.blockers,
        )

    fresh, basis_blockers = execution_basis_is_fresh(execution_basis)
    if fresh:
        return _state(
            status="EXECUTION_BASIS_FRESH",
            stale=False,
            transaction=transaction,
            transaction_state=authoritative.transaction_state,
            lane_state=authoritative.lane_state,
            blockers=authoritative.blockers,
        )

    blockers = tuple(sorted(set((*authoritative.blockers, *basis_blockers))))
    return _state(
        status=STALE_AFTER_EXTERNAL_SOURCE_MUTATION,
        stale=True,
        transaction=transaction,
        transaction_state=authoritative.transaction_state,
        lane_state=authoritative.lane_state,
        blockers=blockers,
    )


def invalidate_external_source_stale_transaction(
    *,
    execution_basis: Any,
    transaction_bundle: Any,
) -> WorkbenchExternalSourceStaleState:
    """Invalidate one safely cancellable prepared transaction after drift."""
    detected = detect_external_source_stale_state(
        execution_basis=execution_basis,
        transaction_bundle=transaction_bundle,
    )
    if not detected.stale or detected.invalidated:
        return detected

    transaction = getattr(transaction_bundle, "transaction", None)
    if transaction is None:
        return detected

    transaction_store = getattr(transaction_bundle, "transaction_store", None)
    mutation_lane_store = getattr(transaction_bundle, "mutation_lane_store", None)
    if transaction_store is None or mutation_lane_store is None:
        return _with_blocker(detected, "STALE_INVALIDATION_STORE_MISSING")

    record = transaction_store.get_transaction(transaction.transaction_id)
    if record is None:
        return _with_blocker(
            detected,
            "STALE_INVALIDATION_TRANSACTION_RECORD_MISSING",
        )

    record_state = str(record.get("state", "")).upper()
    if record_state != "PREPARED":
        return _with_blocker(
            detected,
            "EXTERNAL_SOURCE_MUTATION_ACTIVE_TRANSACTION_REQUIRES_RECOVERY:"
            + record_state,
        )

    request = mutation_lane_store.get_request(transaction.mutation_request_id)
    if request is None:
        return _with_blocker(
            detected,
            "STALE_INVALIDATION_MUTATION_REQUEST_MISSING",
        )

    request_state = str(request.get("state", "")).upper()
    if request_state == "QUEUED":
        mutation_lane_store.transition(
            transaction.mutation_request_id,
            "CANCELLED",
            reason=STALE_AFTER_EXTERNAL_SOURCE_MUTATION,
        )
    elif request_state != "CANCELLED":
        return _with_blocker(
            detected,
            "STALE_INVALIDATION_MUTATION_REQUEST_NOT_QUEUED:" + request_state,
        )

    transaction_store.transition_transaction(
        transaction.transaction_id,
        STALE_AFTER_EXTERNAL_SOURCE_MUTATION,
        recovery_state="NONE",
        rollback_state="NOT_REQUIRED",
    )
    transaction_store.store_artifact(
        transaction.transaction_id,
        "EXTERNAL_SOURCE_STALE_INVALIDATION",
        {
            "schema_version": SCHEMA_VERSION,
            "feature_id": WORKBENCH_EXTERNAL_SOURCE_STALE_FEATURE_ID,
            "status": STALE_AFTER_EXTERNAL_SOURCE_MUTATION,
            "message": EXTERNAL_SOURCE_STALE_MESSAGE,
            "basis_blockers": list(detected.blockers),
        },
    )
    return _replace_state(
        detected,
        invalidated=True,
        transaction_state=STALE_AFTER_EXTERNAL_SOURCE_MUTATION,
        lane_state="CANCELLED",
    )


def sync_external_source_stale_state_from_window(
    window: object,
) -> WorkbenchExternalSourceStaleState:
    """Synchronize stale classification from current Workbench GUI evidence."""
    evidence = getattr(
        window,
        "_large_file_refactor_workbench_completion_evidence",
        None,
    )
    transaction_bundle = getattr(
        window,
        "_large_file_refactor_workbench_completion_transaction",
        None,
    )
    basis = getattr(evidence, "execution_basis", None)

    if transaction_bundle is None:
        result = detect_external_source_stale_state(
            execution_basis=basis,
            transaction_bundle=None,
        )
    else:
        result = invalidate_external_source_stale_transaction(
            execution_basis=basis,
            transaction_bundle=transaction_bundle,
        )

    setattr(
        window,
        "_large_file_refactor_workbench_external_source_stale_state",
        result,
    )
    if result.stale:
        setattr(
            window,
            "_large_file_refactor_workbench_state",
            STALE_AFTER_EXTERNAL_SOURCE_MUTATION,
        )
    return result


@dataclass(frozen=True)
class _AuthoritativeTransactionState:
    transaction_state: str
    lane_state: str
    blockers: tuple[str, ...]


def _authoritative_transaction_state(
    transaction_bundle: Any,
) -> _AuthoritativeTransactionState:
    transaction = getattr(transaction_bundle, "transaction", None)
    if transaction is None:
        return _AuthoritativeTransactionState("", "", ())

    transaction_state = str(
        getattr(transaction, "transaction_state", "") or ""
    ).upper()
    lane_state = str(getattr(transaction, "lane_state", "") or "").upper()
    blockers: list[str] = []

    transaction_store = getattr(transaction_bundle, "transaction_store", None)
    if transaction_store is not None:
        record = transaction_store.get_transaction(transaction.transaction_id)
        if record is None:
            blockers.append("AUTHORITATIVE_TRANSACTION_RECORD_MISSING")
        else:
            transaction_state = str(record.get("state", "") or "").upper()

    lane_store = getattr(transaction_bundle, "mutation_lane_store", None)
    if lane_store is not None:
        request = lane_store.get_request(transaction.mutation_request_id)
        if request is None:
            blockers.append("AUTHORITATIVE_MUTATION_REQUEST_MISSING")
        else:
            lane_state = str(request.get("state", "") or "").upper()

    return _AuthoritativeTransactionState(
        transaction_state=transaction_state,
        lane_state=lane_state,
        blockers=tuple(sorted(set(blockers))),
    )


def _state(
    *,
    status: str,
    stale: bool,
    blockers: tuple[str, ...],
    transaction: Any = None,
    invalidated: bool = False,
    transaction_state: str = "",
    lane_state: str = "",
) -> WorkbenchExternalSourceStaleState:
    return WorkbenchExternalSourceStaleState(
        schema_version=SCHEMA_VERSION,
        feature_id=WORKBENCH_EXTERNAL_SOURCE_STALE_FEATURE_ID,
        status=status,
        stale=stale,
        invalidated=invalidated,
        transaction_id=str(getattr(transaction, "transaction_id", "") or ""),
        transaction_state=(
            transaction_state
            or str(getattr(transaction, "transaction_state", "") or "")
        ),
        lane_state=(
            lane_state or str(getattr(transaction, "lane_state", "") or "")
        ),
        message=EXTERNAL_SOURCE_STALE_MESSAGE if stale else "",
        blockers=blockers,
    )


def _with_blocker(
    state: WorkbenchExternalSourceStaleState,
    blocker: str,
) -> WorkbenchExternalSourceStaleState:
    return WorkbenchExternalSourceStaleState(
        **{
            **state.__dict__,
            "blockers": tuple(sorted(set((*state.blockers, blocker)))),
        }
    )


def _replace_state(
    state: WorkbenchExternalSourceStaleState,
    *,
    invalidated: bool,
    transaction_state: str,
    lane_state: str | None = None,
) -> WorkbenchExternalSourceStaleState:
    return WorkbenchExternalSourceStaleState(
        **{
            **state.__dict__,
            "invalidated": invalidated,
            "transaction_state": transaction_state,
            "lane_state": lane_state if lane_state is not None else state.lane_state,
        }
    )
