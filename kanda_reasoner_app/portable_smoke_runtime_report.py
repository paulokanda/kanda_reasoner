# project-path: kanda_reasoner_app/portable_smoke_runtime_report.py
"""Fail-closed runtime evidence for interactive Portable GUI smoke tests."""

from __future__ import annotations

import hashlib
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

__all__ = [
    "PORTABLE_SMOKE_REPORT_PATH_ENV",
    "PORTABLE_SMOKE_REPORT_ROOT_ENV",
    "PORTABLE_SMOKE_REPORT_TOKEN_ENV",
    "record_portable_smoke_event",
]

PORTABLE_SMOKE_REPORT_PATH_ENV = "KANDA_PORTABLE_SMOKE_RUNTIME_REPORT"
PORTABLE_SMOKE_REPORT_ROOT_ENV = "KANDA_PORTABLE_SMOKE_RUNTIME_REPORT_ROOT"
PORTABLE_SMOKE_REPORT_TOKEN_ENV = "KANDA_PORTABLE_SMOKE_RUNTIME_REPORT_TOKEN"
SCHEMA_VERSION = "1.0"


def _normalized_absolute_path(text: str) -> Path | None:
    raw = str(text or "").strip()
    if not raw:
        return None
    path = Path(raw).expanduser()
    if not path.is_absolute():
        return None
    return path.resolve(strict=False)


def _bounded_report_path() -> tuple[Path, str] | None:
    report = _normalized_absolute_path(
        os.environ.get(PORTABLE_SMOKE_REPORT_PATH_ENV, "")
    )
    root = _normalized_absolute_path(
        os.environ.get(PORTABLE_SMOKE_REPORT_ROOT_ENV, "")
    )
    token = os.environ.get(PORTABLE_SMOKE_REPORT_TOKEN_ENV, "").strip()
    if report is None and root is None and not token:
        return None
    if report is None or root is None or not token:
        return None
    try:
        report.relative_to(root)
    except ValueError:
        return None
    if report.is_symlink() or root.is_symlink():
        return None
    root.mkdir(parents=True, exist_ok=True)
    return report, hashlib.sha256(token.encode("utf-8")).hexdigest()


def _read_existing(path: Path, token_sha256: str) -> dict[str, Any]:
    if not path.is_file():
        return {
            "schema_version": SCHEMA_VERSION,
            "token_sha256": token_sha256,
            "events": [],
        }
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return {
            "schema_version": SCHEMA_VERSION,
            "token_sha256": token_sha256,
            "events": [],
        }
    if not isinstance(payload, dict):
        return {
            "schema_version": SCHEMA_VERSION,
            "token_sha256": token_sha256,
            "events": [],
        }
    if payload.get("token_sha256") != token_sha256:
        return {
            "schema_version": SCHEMA_VERSION,
            "token_sha256": token_sha256,
            "events": [],
        }
    events = payload.get("events")
    if not isinstance(events, list):
        payload["events"] = []
    return payload


def record_portable_smoke_event(
    *,
    status: str,
    kind: str,
    source: str,
    message: str = "",
) -> None:
    """Append one bounded smoke event when runtime reporting is enabled."""
    resolved = _bounded_report_path()
    if resolved is None:
        return
    path, token_sha256 = resolved
    normalized_status = str(status or "").strip().upper()
    if normalized_status not in {"PASS", "FAIL"}:
        normalized_status = "FAIL"
    payload = _read_existing(path, token_sha256)
    events = payload.setdefault("events", [])
    events.append(
        {
            "status": normalized_status,
            "kind": str(kind or "").strip(),
            "source": str(source or "").strip(),
            "message": str(message or "").strip()[:12000],
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
        }
    )
    temporary = path.with_name(path.name + ".tmp-" + uuid.uuid4().hex)
    temporary.parent.mkdir(parents=True, exist_ok=True)
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    os.replace(temporary, path)
