# project-path: kanda_reasoner_app/reasoner_engine/project_web_ai_apply_receipts.py
"""Store durable Project Web AI terminal receipts and handoff freshness."""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping

__all__ = [
    "ProjectWebAIApplyReceipt",
    "ProjectWebAIApplyReceiptError",
    "apply_preview_caption",
    "assert_project_web_ai_handoff_fresh",
    "receipt_allows_retry_after_shadow_delete",
    "receipt_matches_fresh_project_context",
    "prepare_receipt_root",
    "write_apply_receipt",
]

_RECEIPT_FOLDER = "project_validation_evidence/project_web_ai_apply_receipts"
_TERMINAL_SUCCESS = "APPLIED_SOURCE_VERIFIED"
_UNRESOLVED = "UNRESOLVED"


class ProjectWebAIApplyReceiptError(RuntimeError):
    """Raised when durable receipt ownership or freshness is unsafe."""


def apply_preview_caption(receipt: "ProjectWebAIApplyReceipt | None") -> str:
    """Return an honest Preview label for one terminal apply outcome."""
    if receipt is None:
        return "View Shadow Preview"
    return {
        "APPLIED_SOURCE_VERIFIED": "View Applied Preview",
        "PROPOSAL_ONLY": "View Recorded Proposal",
        "ROLLED_BACK": "View Rolled-Back Preview",
        "UNRESOLVED": "View Unresolved Preview",
    }.get(receipt.status, "View Terminal Preview")


def receipt_allows_retry_after_shadow_delete(
    receipt: "ProjectWebAIApplyReceipt | None",
) -> bool:
    """Return whether deleting a rolled-back Preview may reopen the cycle."""
    return bool(receipt is not None and receipt.status == "ROLLED_BACK")


def receipt_matches_fresh_project_context(
    receipt: "ProjectWebAIApplyReceipt | None",
    *,
    project_id: str,
    project_root_fingerprint: str,
) -> bool:
    """Return whether a verified apply belongs to an accepted fresh context."""
    return bool(
        receipt is not None
        and receipt.status == "APPLIED_SOURCE_VERIFIED"
        and receipt.project_id == str(project_id or "")
        and receipt.project_root_fingerprint
        == str(project_root_fingerprint or "")
    )


@dataclass(frozen=True)
class ProjectWebAIApplyReceipt:
    """Describe one terminal Project Web AI review outcome."""

    schema_version: str
    transaction_id: str
    authorization_id: str
    operation_id: str
    status: str
    operation_class: str
    project_id: str
    project_root: str
    project_root_fingerprint: str
    project_epoch: int
    snapshot_id: str
    preview_fingerprint: str
    changed_files: tuple[str, ...]
    source_sha256: tuple[str, ...]
    installed_sha256: tuple[str, ...]
    backup_root: str
    validation_markers: tuple[str, ...]
    started_at_utc: str
    completed_at_utc: str
    error: str
    receipt_path: str = ""

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-safe receipt mapping."""
        payload = asdict(self)
        for key in (
            "changed_files",
            "source_sha256",
            "installed_sha256",
            "validation_markers",
        ):
            payload[key] = list(payload[key])
        return payload


def prepare_receipt_root(support_root: str | Path) -> Path:
    """Create and probe the canonical Project-owned receipt directory."""
    root = Path(support_root).expanduser().resolve(strict=False)
    receipt_root = (root / _RECEIPT_FOLDER).resolve(strict=False)
    try:
        receipt_root.relative_to(root)
    except ValueError as exc:
        raise ProjectWebAIApplyReceiptError("APPLY_RECEIPT_PATH_ESCAPE") from exc
    receipt_root.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        prefix=".kanda_receipt_probe_",
        suffix=".tmp",
        dir=receipt_root,
        delete=False,
    ) as handle:
        probe = Path(handle.name)
        handle.write("probe\n")
        handle.flush()
        os.fsync(handle.fileno())
    probe.unlink(missing_ok=True)
    return receipt_root


def write_apply_receipt(
    support_root: str | Path,
    receipt: ProjectWebAIApplyReceipt,
) -> ProjectWebAIApplyReceipt:
    """Atomically persist one terminal receipt under Project Support."""
    receipt_root = prepare_receipt_root(support_root)
    target = receipt_root / (receipt.transaction_id + ".json")
    if target.exists():
        raise ProjectWebAIApplyReceiptError("APPLY_RECEIPT_ALREADY_EXISTS")
    payload = receipt.to_dict()
    payload["receipt_path"] = str(target)
    temp = receipt_root / ("." + receipt.transaction_id + ".tmp")
    encoded = (
        json.dumps(payload, ensure_ascii=True, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")
    try:
        with temp.open("xb") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, target)
    finally:
        temp.unlink(missing_ok=True)
    return ProjectWebAIApplyReceipt(**{**asdict(receipt), "receipt_path": str(target)})


def assert_project_web_ai_handoff_fresh(
    support_root: str | Path,
    handoff_generated_at_utc: str,
) -> None:
    """Block stale handoff reuse after a successful or unresolved source write."""
    receipt_root = (
        Path(support_root).expanduser().resolve(strict=False) / _RECEIPT_FOLDER
    )
    if not receipt_root.is_dir():
        return
    latest = _latest_authoritative_receipt(receipt_root)
    if latest is None:
        return
    status = str(latest.get("status") or "")
    if status == _UNRESOLVED:
        raise ProjectWebAIApplyReceiptError(
            "PROJECT_WEB_AI_APPLY_OUTCOME_UNRESOLVED:"
            + str(latest.get("transaction_id") or "unknown")
        )
    if status != _TERMINAL_SUCCESS:
        return
    completed = _parse_utc(str(latest.get("completed_at_utc") or ""))
    generated = _parse_utc(handoff_generated_at_utc)
    if completed is None or generated is None or generated <= completed:
        raise ProjectWebAIApplyReceiptError(
            "SHOW_PROJECT_TO_AI_REFRESH_REQUIRED_AFTER_APPLY:"
            + str(latest.get("transaction_id") or "unknown")
        )


def _latest_authoritative_receipt(root: Path) -> Mapping[str, object] | None:
    """Return the newest parsed terminal receipt, ignoring malformed files."""
    records: list[tuple[datetime, Mapping[str, object]]] = []
    for path in root.glob("*.json"):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(payload, dict):
            continue
        completed = _parse_utc(str(payload.get("completed_at_utc") or ""))
        if completed is not None:
            records.append((completed, payload))
    if not records:
        return None
    records.sort(key=lambda item: item[0])
    return records[-1][1]


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
