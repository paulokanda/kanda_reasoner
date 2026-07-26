# project-path: kanda_reasoner_app/reasoner_engine/project_web_ai_session.py
"""Own disposable Project Web AI state for one selected Project.

This owner tracks the current Project epoch, the selected root awaiting reload,
worker-settlement locks, and the immutable snapshot identity. It owns no chat
content, provider transport, source writes, Project Support persistence, or
Freeze behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from kanda_reasoner_app.web_ai_provider_contracts import (
    ContextSnapshot,
    ProjectWebAIRequestIdentity,
)

__all__ = [
    "ProjectSwitchDecision",
    "ProjectWebAISessionIdentity",
    "ProjectWebAISessionLifecycle",
    "ProjectWebAISessionStateError",
]


class ProjectWebAISessionStateError(RuntimeError):
    """Raised when stale or incompatible Project session state is used."""


@dataclass(frozen=True)
class ProjectSwitchDecision:
    """Describe one current root-switch decision without authorizing writes."""

    project_epoch: int
    requested_root: str
    wait_for_worker: bool
    reload_allowed: bool


@dataclass(frozen=True)
class ProjectWebAISessionIdentity:
    """Bind transient Project Web AI state to one immutable snapshot."""

    project_epoch: int
    project_id: str
    project_slug: str
    project_root: str
    project_root_fingerprint: str
    support_root: str
    daily_work_root: str
    snapshot_id: str
    context_hash: str

    @classmethod
    def from_snapshot(
        cls,
        snapshot: ContextSnapshot,
        project_epoch: int,
    ) -> "ProjectWebAISessionIdentity":
        """Build one session identity from exact current snapshot fields."""
        return cls(
            project_epoch=project_epoch,
            project_id=snapshot.project_id,
            project_slug=snapshot.project_slug,
            project_root=_canonical_root_text(snapshot.project_root),
            project_root_fingerprint=snapshot.project_root_fingerprint,
            support_root=snapshot.support_root,
            daily_work_root=snapshot.daily_work_root,
            snapshot_id=snapshot.snapshot_id,
            context_hash=snapshot.context_hash,
        )

    def accepts_request(
        self,
        request: ProjectWebAIRequestIdentity,
        snapshot: ContextSnapshot,
    ) -> bool:
        """Return whether one request still belongs to this exact session."""
        return bool(
            request.project_epoch == self.project_epoch
            and request.project_id == self.project_id
            and request.project_slug == self.project_slug
            and request.project_root_fingerprint
            == self.project_root_fingerprint
            and request.support_root == self.support_root
            and request.snapshot_id == self.snapshot_id
            and request.context_hash == self.context_hash
            and snapshot.project_id == self.project_id
            and snapshot.project_slug == self.project_slug
            and _canonical_root_text(snapshot.project_root) == self.project_root
            and snapshot.project_root_fingerprint
            == self.project_root_fingerprint
            and snapshot.support_root == self.support_root
            and snapshot.daily_work_root == self.daily_work_root
            and snapshot.snapshot_id == self.snapshot_id
            and snapshot.context_hash == self.context_hash
        )


class ProjectWebAISessionLifecycle:
    """Coordinate one disposable Project-scoped Web AI session."""

    def __init__(self) -> None:
        """Create an empty session with no selected Project authority."""
        self._project_epoch = 0
        self._pending_root = ""
        self._waiting_for_worker = False
        self._identity: ProjectWebAISessionIdentity | None = None
        self._open_transaction_id = ""
        self._unresolved_transaction_id = ""
        self._refresh_required_root = ""
        self._refresh_after_utc = ""

    @property
    def project_epoch(self) -> int:
        """Return the current monotonically increasing Project epoch."""
        return self._project_epoch

    @property
    def identity(self) -> ProjectWebAISessionIdentity | None:
        """Return the current immutable snapshot binding, when available."""
        return self._identity

    @property
    def waiting_for_worker(self) -> bool:
        """Return whether a previous-Project worker still blocks reload."""
        return self._waiting_for_worker

    @property
    def open_transaction_id(self) -> str:
        """Return the current source-write transaction, when open."""
        return self._open_transaction_id

    @property
    def unresolved_transaction_id(self) -> str:
        """Return the unresolved transaction that blocks Project switching."""
        return self._unresolved_transaction_id

    @property
    def transaction_blocks_project_switch(self) -> bool:
        """Return whether apply state currently forbids Project Eject."""
        return bool(self._open_transaction_id or self._unresolved_transaction_id)

    @property
    def pending_root(self) -> str:
        """Return the newest requested root awaiting a current reload."""
        return self._pending_root

    def request_switch(
        self,
        root_text: str,
        *,
        worker_running: bool,
    ) -> ProjectSwitchDecision:
        """Invalidate old authority and register the newest selected root."""
        if self.transaction_blocks_project_switch:
            raise ProjectWebAISessionStateError(
                "PROJECT_SWITCH_BLOCKED_BY_APPLY_TRANSACTION:"
                + (self._open_transaction_id or self._unresolved_transaction_id)
            )
        requested_root = _canonical_root_text(root_text)
        if requested_root != self._refresh_required_root:
            self._refresh_required_root = ""
            self._refresh_after_utc = ""
        self._project_epoch += 1
        self._identity = None
        self._pending_root = requested_root
        self._waiting_for_worker = bool(worker_running)
        return self._decision()

    def worker_settled(self) -> ProjectSwitchDecision:
        """Release the worker lock and permit only the newest pending reload."""
        self._waiting_for_worker = False
        return self._decision()

    def reload_is_current(self, project_epoch: int, root_text: str) -> bool:
        """Return whether one delayed reload still targets current state."""
        return bool(
            project_epoch == self._project_epoch
            and not self._waiting_for_worker
            and self._pending_root
            and _canonical_root_text(root_text) == self._pending_root
        )

    def bind_snapshot(
        self,
        snapshot: ContextSnapshot,
    ) -> ProjectWebAISessionIdentity:
        """Bind the current epoch to one exact selected-Project snapshot."""
        if self._waiting_for_worker:
            raise ProjectWebAISessionStateError(
                "PROJECT_SWITCH_WAITING_FOR_PREVIOUS_WORKER"
            )
        snapshot_root = _canonical_root_text(snapshot.project_root)
        if self._pending_root and snapshot_root != self._pending_root:
            raise ProjectWebAISessionStateError(
                "STALE_PROJECT_SNAPSHOT_ROOT:" + snapshot_root
            )
        if (
            self._refresh_required_root
            and snapshot_root == self._refresh_required_root
            and not _snapshot_is_newer(
                snapshot.generated_at_utc,
                self._refresh_after_utc,
            )
        ):
            raise ProjectWebAISessionStateError(
                "SHOW_PROJECT_TO_AI_REFRESH_REQUIRED_AFTER_SOURCE_MUTATION"
            )
        identity = ProjectWebAISessionIdentity.from_snapshot(
            snapshot,
            self._project_epoch,
        )
        self._identity = identity
        self._pending_root = ""
        return identity

    def begin_write_transaction(self, transaction_id: str) -> None:
        """Open one exact source-write transaction for the current session."""
        clean = str(transaction_id or "").strip()
        if not clean or self._identity is None or self._waiting_for_worker:
            raise ProjectWebAISessionStateError(
                "PROJECT_WEB_AI_WRITE_TRANSACTION_NOT_ADMISSIBLE"
            )
        if self.transaction_blocks_project_switch:
            raise ProjectWebAISessionStateError(
                "PROJECT_WEB_AI_WRITE_TRANSACTION_ALREADY_OPEN"
            )
        self._open_transaction_id = clean

    def finish_write_transaction(self, transaction_id: str, status: str) -> None:
        """Settle one transaction while retaining unresolved fail-closed state."""
        clean = str(transaction_id or "").strip()
        if not clean or clean != self._open_transaction_id:
            if str(status or "") == "UNRESOLVED" and clean:
                self._unresolved_transaction_id = clean
            return
        self._open_transaction_id = ""
        if str(status or "") == "UNRESOLVED":
            self._unresolved_transaction_id = clean
        else:
            self._unresolved_transaction_id = ""

    def mark_source_mutated(self, project_root: str, completed_at_utc: str) -> None:
        """Invalidate the current handoff until a newer collector run exists."""
        self._project_epoch += 1
        self._identity = None
        self._pending_root = ""
        self._refresh_required_root = _canonical_root_text(project_root)
        self._refresh_after_utc = str(completed_at_utc or "").strip()

    def request_is_current(
        self,
        request: ProjectWebAIRequestIdentity,
        snapshot: ContextSnapshot,
    ) -> bool:
        """Reject events from old Projects, epochs, or snapshot generations."""
        identity = self._identity
        return bool(
            identity is not None
            and not self._waiting_for_worker
            and identity.accepts_request(request, snapshot)
        )

    def invalidate_for_disposal(self) -> None:
        """Invalidate all Project-scoped authority before widget disposal."""
        self._project_epoch += 1
        self._identity = None
        self._pending_root = ""
        self._waiting_for_worker = False

    def _decision(self) -> ProjectSwitchDecision:
        """Return the current immutable switch decision."""
        return ProjectSwitchDecision(
            project_epoch=self._project_epoch,
            requested_root=self._pending_root,
            wait_for_worker=self._waiting_for_worker,
            reload_allowed=bool(
                self._pending_root and not self._waiting_for_worker
            ),
        )


def _canonical_root_text(root_text: str) -> str:
    """Return one normalized root string or an empty selection."""
    value = str(root_text or "").strip()
    if not value:
        return ""
    return str(Path(value).expanduser().resolve(strict=False))

def _snapshot_is_newer(generated_at_utc: str, required_after_utc: str) -> bool:
    """Return whether one generated handoff is newer than the source mutation."""
    generated = _parse_utc(generated_at_utc)
    required = _parse_utc(required_after_utc)
    return bool(generated is not None and required is not None and generated > required)


def _parse_utc(value: str) -> datetime | None:
    """Return one timezone-aware ISO timestamp."""
    text = str(value or "").strip()
    if not text:
        return None
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)

