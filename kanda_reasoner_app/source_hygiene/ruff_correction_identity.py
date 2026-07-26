# project-path: kanda_reasoner_app/source_hygiene/ruff_correction_identity.py
"""Diff and identity helpers for Ruff correction previews."""

from __future__ import annotations

import difflib
import hashlib
import time
from pathlib import Path
from typing import Any, Sequence

from .ruff_correction_models import (
    RUFF_CORRECTION_FEATURE_ID,
    RuffCorrectionFileRecord,
    RuffCorrectionPreviewRecord,
)
from .ruff_correction_storage import canonical_json_bytes, sha256_bytes, utc_now

__all__: list[str] = []


def _unified_diff(relative: str, before: str, after: str) -> str:
    """Return one exact unified diff for review."""
    lines = difflib.unified_diff(
        before.splitlines(keepends=True),
        after.splitlines(keepends=True),
        fromfile="a/" + relative,
        tofile="b/" + relative,
        lineterm="\n",
    )
    return "".join(lines)


def _snapshot_digest(payloads: dict[str, bytes]) -> str:
    """Hash the ordered active-source snapshot."""
    digest = hashlib.sha256()
    for relative in sorted(payloads, key=str.casefold):
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(sha256_bytes(payloads[relative]).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def _preview_payload_digest(records: Sequence[RuffCorrectionFileRecord]) -> str:
    """Hash the ordered corrected payload identity."""
    digest = hashlib.sha256()
    for record in sorted(records, key=lambda item: item.relative_path.casefold()):
        digest.update(record.relative_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(record.preview_sha256.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def _preview_seed(
    *,
    project_root: Path,
    policy_token: str,
    ruff_version: str,
    source_snapshot: str,
    scope_paths: Sequence[str],
) -> str:
    """Return a digest seed for preview identity."""
    payload = {
        "feature_id": RUFF_CORRECTION_FEATURE_ID,
        "project_root": str(project_root),
        "policy_token": policy_token,
        "ruff_version": ruff_version,
        "source_snapshot": source_snapshot,
        "scope_paths": list(scope_paths),
        "created_at_utc": utc_now(),
        "created_at_time_ns": time.time_ns(),
    }
    return sha256_bytes(canonical_json_bytes(payload))


def _new_preview_id(seed: str) -> str:
    """Build a collision-resistant readable preview identifier."""
    stamp = utc_now().replace("-", "").replace(":", "")
    stamp = stamp.replace("T", "t").replace("Z", "z")
    return "ruff3a-" + stamp + "-" + seed[:12]


def _manifest_identity_payload(
    *,
    preview_id: str,
    project_root: Path,
    ruff_version: str,
    policy_token: str,
    policy_sha256: str,
    source_snapshot: str,
    preview_payload_digest: str,
    scope_paths: Sequence[str],
    files: Sequence[RuffCorrectionFileRecord],
) -> dict[str, Any]:
    """Return the immutable fields protected by manifest identity."""
    return {
        "feature_id": RUFF_CORRECTION_FEATURE_ID,
        "preview_id": preview_id,
        "project_root": str(project_root),
        "ruff_version": ruff_version,
        "policy_identity_token": policy_token,
        "policy_config_sha256": policy_sha256,
        "source_snapshot_sha256": source_snapshot,
        "preview_payload_sha256": preview_payload_digest,
        "scope_paths": list(scope_paths),
        "files": [item.to_dict() for item in files],
    }


def _verify_active_source_unchanged(
    root: Path,
    original_payloads: dict[str, bytes],
) -> None:
    """Prove preview generation did not mutate active source."""
    for relative, expected in original_payloads.items():
        current = (root / relative).read_bytes()
        if current != expected:
            from .ruff_correction_errors import RuffCorrectionPreviewError

            raise RuffCorrectionPreviewError(
                "RUFF_CORRECTION_ACTIVE_SOURCE_MUTATED_DURING_PREVIEW:" + relative
            )


def _preview_readme(record: RuffCorrectionPreviewRecord) -> str:
    """Return plain-text human review instructions."""
    lines = [
        "Ruff Correction Preview",
        "",
        "Preview ID: " + record.preview_id,
        "Status: " + record.status,
        "Changed files: " + str(record.changed_file_count),
        "Diff: " + record.diff_path,
        "Manifest: " + record.manifest_path,
    ]
    if record.confirm_token:
        lines.extend(
            [
                "",
                "Apply is blocked unless the exact confirmation token is provided:",
                record.confirm_token,
            ]
        )
    lines.extend(
        [
            "",
            "This preview did not modify active project source.",
            "Review the exact diff before any apply transaction.",
        ]
    )
    return "\n".join(lines) + "\n"
