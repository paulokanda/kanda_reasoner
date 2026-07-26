# project-path: kanda_reasoner_app/source_hygiene/ruff_correction_apply.py
"""Explicit, hash-guarded Ruff correction apply transactions with rollback."""

from __future__ import annotations

from contextlib import contextmanager
import hashlib
import os
from pathlib import Path
from typing import Iterator, Sequence

from .ruff_correction_models import (
    RUFF_CORRECTION_FEATURE_ID,
    RUFF_CORRECTION_SCHEMA_VERSION,
    RuffCorrectionApplyReceipt,
    RuffCorrectionPreviewRecord,
)
from .ruff_correction_discovery import _require_policy_version
from .ruff_correction_errors import RuffCorrectionApplyError
from .ruff_correction_identity import (
    _manifest_identity_payload,
    _preview_payload_digest,
)
from .ruff_correction_storage import (
    atomic_write_bytes,
    atomic_write_json,
    ensure_project_relative_file,
    load_json_object,
    resolve_ruff_correction_paths,
    safe_preview_id,
    sha256_bytes,
    sha256_file,
    utc_now,
)
from .ruff_policy_identity import resolve_ruff_policy_identity
from .ruff_quality_runtime import (
    _DEFAULT_RUFF_TIMEOUT_SECONDS,
    _resolve_ruff_command,
    _run_ruff_process,
)
from .ruff_quality_scope import _build_ruff_quality_scope

__all__ = [
    "apply_ruff_correction_preview",
    "load_ruff_correction_preview",
]


def load_ruff_correction_preview(
    project_root: str | Path,
    preview_id: str,
) -> RuffCorrectionPreviewRecord:
    """Load and validate one durable project-owned preview manifest."""
    paths = resolve_ruff_correction_paths(project_root)
    safe_id = safe_preview_id(preview_id)
    preview_root = paths.preview_root(safe_id)
    manifest_path = preview_root / "preview_manifest.json"
    record = RuffCorrectionPreviewRecord.from_dict(load_json_object(manifest_path))
    _validate_preview_record(record, paths.project_root, preview_root)
    return record


def apply_ruff_correction_preview(
    project_root: str | Path,
    preview_id: str,
    *,
    confirm_token: str,
    ruff_argv_prefix: Sequence[str] | None = None,
    timeout_seconds: float = _DEFAULT_RUFF_TIMEOUT_SECONDS,
) -> RuffCorrectionApplyReceipt:
    """Apply one reviewed preview after exact confirmation and stale checks."""
    paths = resolve_ruff_correction_paths(project_root)
    root = paths.project_root
    safe_id = safe_preview_id(preview_id)
    preview_root = paths.preview_root(safe_id)
    record = load_ruff_correction_preview(root, safe_id)

    if record.status != "PREVIEW_READY" or not record.files:
        raise RuffCorrectionApplyError("RUFF_CORRECTION_PREVIEW_NOT_APPLYABLE")
    if str(confirm_token or "") != record.confirm_token:
        raise RuffCorrectionApplyError("RUFF_CORRECTION_CONFIRMATION_TOKEN_MISMATCH")
    if float(timeout_seconds) <= 0:
        raise RuffCorrectionApplyError("RUFF_CORRECTION_TIMEOUT_NOT_POSITIVE")

    receipt_path = paths.receipts_root / (safe_id + ".json")
    if receipt_path.exists():
        raise RuffCorrectionApplyError("RUFF_CORRECTION_PREVIEW_ALREADY_RECEIPTED")

    policy = resolve_ruff_policy_identity(root)
    if policy.identity_token != record.policy_identity_token:
        raise RuffCorrectionApplyError("RUFF_CORRECTION_POLICY_IDENTITY_STALE")
    if policy.config_sha256 != record.policy_config_sha256:
        raise RuffCorrectionApplyError("RUFF_CORRECTION_POLICY_HASH_STALE")

    identity = _resolve_ruff_command(
        ruff_argv_prefix,
        timeout_seconds=timeout_seconds,
    )
    _require_policy_version(identity.version, policy.required_version)
    if identity.version != record.ruff_version:
        raise RuffCorrectionApplyError("RUFF_CORRECTION_RUFF_VERSION_STALE")

    payload_root = preview_root / "payload"
    source_before = _validate_source_and_payload(root, payload_root, record)
    transaction_id = _transaction_id(safe_id, record.manifest_identity_sha256)
    backup_root = paths.backups_root / transaction_id
    changed_paths = tuple(item.relative_path for item in record.files)
    cache_before = (root / ".ruff_cache").exists()

    with _exclusive_preview_lock(paths.locks_root, safe_id, transaction_id):
        try:
            _write_backups(backup_root, source_before)
            _apply_payload(root, payload_root, record)
            validation_markers = _validate_applied_files(
                root,
                record,
                identity.argv_prefix,
                timeout_seconds,
            )
            if not cache_before and (root / ".ruff_cache").exists():
                raise RuffCorrectionApplyError("RUFF_CORRECTION_PROJECT_CACHE_LEAK")
        except Exception as exc:
            rollback_markers = _rollback_from_backups(
                root,
                backup_root,
                source_before,
            )
            receipt = _write_receipt(
                receipt_path=receipt_path,
                receipt_id=transaction_id,
                preview_id=safe_id,
                status="ROLLED_BACK",
                project_root=root,
                backup_root=backup_root,
                changed_files=changed_paths,
                validation_markers=rollback_markers,
                error=str(exc),
                metadata={
                    "ruff_version": identity.version,
                    "manifest_identity_sha256": record.manifest_identity_sha256,
                },
            )
            raise RuffCorrectionApplyError(
                "RUFF_CORRECTION_APPLY_ROLLED_BACK:"
                + receipt.receipt_path
                + ":"
                + str(exc)
            ) from exc

        return _write_receipt(
            receipt_path=receipt_path,
            receipt_id=transaction_id,
            preview_id=safe_id,
            status="APPLIED",
            project_root=root,
            backup_root=backup_root,
            changed_files=changed_paths,
            validation_markers=validation_markers,
            error="",
            metadata={
                "ruff_version": identity.version,
                "ruff_command_source": identity.source,
                "policy_identity_token": policy.identity_token,
                "manifest_identity_sha256": record.manifest_identity_sha256,
            },
        )


def _validate_preview_record(
    record: RuffCorrectionPreviewRecord,
    root: Path,
    preview_root: Path,
) -> None:
    """Validate preview ownership, schema, paths, and immutable identity."""
    if record.schema_version != RUFF_CORRECTION_SCHEMA_VERSION:
        raise RuffCorrectionApplyError("RUFF_CORRECTION_SCHEMA_MISMATCH")
    if record.feature_id != RUFF_CORRECTION_FEATURE_ID:
        raise RuffCorrectionApplyError("RUFF_CORRECTION_FEATURE_ID_MISMATCH")
    if safe_preview_id(record.preview_id) != preview_root.name:
        raise RuffCorrectionApplyError("RUFF_CORRECTION_PREVIEW_ID_MISMATCH")
    if Path(record.project_root).expanduser().resolve() != root:
        raise RuffCorrectionApplyError("RUFF_CORRECTION_PROJECT_ROOT_MISMATCH")

    expected_manifest = (preview_root / "preview_manifest.json").resolve()
    expected_diff = (preview_root / "preview.diff").resolve()
    expected_payload = (preview_root / "payload").resolve()
    if Path(record.manifest_path).resolve() != expected_manifest:
        raise RuffCorrectionApplyError("RUFF_CORRECTION_MANIFEST_PATH_MISMATCH")
    if Path(record.diff_path).resolve() != expected_diff:
        raise RuffCorrectionApplyError("RUFF_CORRECTION_DIFF_PATH_MISMATCH")
    if Path(record.payload_root).resolve() != expected_payload:
        raise RuffCorrectionApplyError("RUFF_CORRECTION_PAYLOAD_PATH_MISMATCH")
    if record.changed_file_count != len(record.files):
        raise RuffCorrectionApplyError("RUFF_CORRECTION_CHANGED_COUNT_MISMATCH")

    core = _manifest_identity_payload(
        preview_id=record.preview_id,
        project_root=root,
        ruff_version=record.ruff_version,
        policy_token=record.policy_identity_token,
        policy_sha256=record.policy_config_sha256,
        source_snapshot=record.source_snapshot_sha256,
        preview_payload_digest=record.preview_payload_sha256,
        scope_paths=record.scope_paths,
        files=record.files,
    )
    from .ruff_correction_storage import canonical_json_bytes

    expected_identity = sha256_bytes(canonical_json_bytes(core))
    if expected_identity != record.manifest_identity_sha256:
        raise RuffCorrectionApplyError("RUFF_CORRECTION_MANIFEST_IDENTITY_MISMATCH")
    expected_token = "APPLY_RUFF_CORRECTION_" + record.preview_id.upper()
    if record.status == "PREVIEW_READY" and record.confirm_token != expected_token:
        raise RuffCorrectionApplyError("RUFF_CORRECTION_CONFIRM_TOKEN_INVALID")


def _validate_source_and_payload(
    root: Path,
    payload_root: Path,
    record: RuffCorrectionPreviewRecord,
) -> dict[str, bytes]:
    """Prove active source freshness and preview payload integrity."""
    source_before: dict[str, bytes] = {}
    seen: set[str] = set()
    for item in record.files:
        if item.relative_path in seen:
            raise RuffCorrectionApplyError("RUFF_CORRECTION_DUPLICATE_FILE_RECORD")
        seen.add(item.relative_path)
        source_path, relative = ensure_project_relative_file(root, item.relative_path)
        source_bytes = source_path.read_bytes()
        if sha256_bytes(source_bytes) != item.source_sha256:
            raise RuffCorrectionApplyError("RUFF_CORRECTION_SOURCE_STALE:" + relative)
        payload_path = (payload_root / relative).resolve()
        try:
            payload_path.relative_to(payload_root.resolve())
        except ValueError as exc:
            raise RuffCorrectionApplyError(
                "RUFF_CORRECTION_PAYLOAD_OUTSIDE_PREVIEW"
            ) from exc
        if not payload_path.is_file():
            raise RuffCorrectionApplyError(
                "RUFF_CORRECTION_PAYLOAD_FILE_MISSING:" + relative
            )
        if sha256_file(payload_path) != item.preview_sha256:
            raise RuffCorrectionApplyError(
                "RUFF_CORRECTION_PAYLOAD_HASH_MISMATCH:" + relative
            )
        source_before[relative] = source_bytes
    if _preview_payload_digest(record.files) != record.preview_payload_sha256:
        raise RuffCorrectionApplyError("RUFF_CORRECTION_PAYLOAD_IDENTITY_MISMATCH")
    return source_before


def _write_backups(backup_root: Path, source_before: dict[str, bytes]) -> None:
    """Write durable project-owned backups before active source mutation."""
    if backup_root.exists():
        raise RuffCorrectionApplyError("RUFF_CORRECTION_BACKUP_ROOT_EXISTS")
    for relative, payload in source_before.items():
        atomic_write_bytes(backup_root / relative, payload)


def _apply_payload(
    root: Path,
    payload_root: Path,
    record: RuffCorrectionPreviewRecord,
) -> None:
    """Atomically install reviewed payload bytes into active project source."""
    for item in record.files:
        target, relative = ensure_project_relative_file(root, item.relative_path)
        payload = (payload_root / relative).read_bytes()
        atomic_write_bytes(target, payload)
        if sha256_file(target) != item.preview_sha256:
            raise RuffCorrectionApplyError(
                "RUFF_CORRECTION_ATOMIC_WRITE_HASH_MISMATCH:" + relative
            )


def _validate_applied_files(
    root: Path,
    record: RuffCorrectionPreviewRecord,
    argv_prefix: Sequence[str],
    timeout_seconds: float,
) -> tuple[str, ...]:
    """Validate exact payload hashes, syntax, Ruff execution, and formatting."""
    changed_files: list[Path] = []
    for item in record.files:
        path, relative = ensure_project_relative_file(root, item.relative_path)
        payload = path.read_bytes()
        if sha256_bytes(payload) != item.preview_sha256:
            raise RuffCorrectionApplyError(
                "RUFF_CORRECTION_POST_APPLY_HASH_FAILED:" + relative
            )
        try:
            text = payload.decode("utf-8")
            compile(text, relative, "exec")
        except (UnicodeDecodeError, SyntaxError) as exc:
            raise RuffCorrectionApplyError(
                "RUFF_CORRECTION_POST_APPLY_SYNTAX_FAILED:" + relative
            ) from exc
        changed_files.append(path)

    scope = _build_ruff_quality_scope(root)
    lint = _run_ruff_process(
        (
            *argv_prefix,
            *scope.global_argv,
            "check",
            "--output-format",
            "json",
            "--exit-zero",
            "--no-cache",
            "--no-preview",
            "--color",
            "never",
            *scope.command_argv,
            *(str(path) for path in changed_files),
        ),
        cwd=root,
        timeout_seconds=timeout_seconds,
    )
    if lint.returncode != 0:
        raise RuffCorrectionApplyError(
            "RUFF_CORRECTION_POST_APPLY_LINT_EXECUTION_FAILED:"
            + _bounded_text(lint.stderr or lint.stdout)
        )
    formatting = _run_ruff_process(
        (
            *argv_prefix,
            *scope.global_argv,
            "format",
            "--check",
            "--no-cache",
            "--no-preview",
            "--color",
            "never",
            *scope.command_argv,
            *(str(path) for path in changed_files),
        ),
        cwd=root,
        timeout_seconds=timeout_seconds,
    )
    if formatting.returncode != 0:
        raise RuffCorrectionApplyError(
            "RUFF_CORRECTION_POST_APPLY_FORMAT_CHECK_FAILED:"
            + _bounded_text(formatting.stderr or formatting.stdout)
        )
    return (
        "ACTIVE_SOURCE_PREVIEW_HASH_MATCH: PASS",
        "ACTIVE_SOURCE_PYTHON_COMPILE: PASS",
        "ACTIVE_SOURCE_RUFF_EXECUTION: PASS",
        "ACTIVE_SOURCE_RUFF_FORMAT_CHECK: PASS",
    )


def _rollback_from_backups(
    root: Path,
    backup_root: Path,
    source_before: dict[str, bytes],
) -> tuple[str, ...]:
    """Restore all changed files and verify exact baseline hashes."""
    for relative, expected in source_before.items():
        backup = backup_root / relative
        if not backup.is_file():
            raise RuffCorrectionApplyError(
                "RUFF_CORRECTION_ROLLBACK_BACKUP_MISSING:" + relative
            )
        target, _ = ensure_project_relative_file(root, relative)
        atomic_write_bytes(target, backup.read_bytes())
        if target.read_bytes() != expected:
            raise RuffCorrectionApplyError(
                "RUFF_CORRECTION_ROLLBACK_HASH_FAILED:" + relative
            )
    return (
        "RUFF_CORRECTION_ROLLBACK_COMPLETED: PASS",
        "RUFF_CORRECTION_BASELINE_HASH_RESTORED: PASS",
    )


def _write_receipt(
    *,
    receipt_path: Path,
    receipt_id: str,
    preview_id: str,
    status: str,
    project_root: Path,
    backup_root: Path,
    changed_files: Sequence[str],
    validation_markers: Sequence[str],
    error: str,
    metadata: dict[str, object],
) -> RuffCorrectionApplyReceipt:
    """Write one durable project-owned transaction receipt."""
    receipt = RuffCorrectionApplyReceipt(
        receipt_id=receipt_id,
        preview_id=preview_id,
        status=status,
        project_root=str(project_root),
        created_at_utc=utc_now(),
        backup_root=str(backup_root),
        receipt_path=str(receipt_path),
        changed_files=tuple(changed_files),
        validation_markers=tuple(validation_markers),
        error=error,
        metadata=dict(metadata),
    )
    atomic_write_json(receipt_path, receipt.to_dict())
    return receipt


@contextmanager
def _exclusive_preview_lock(
    locks_root: Path,
    preview_id: str,
    transaction_id: str,
) -> Iterator[None]:
    """Hold an explicit project-owned lock for one apply transaction."""
    locks_root.mkdir(parents=True, exist_ok=True)
    lock_path = locks_root / (preview_id + ".lock")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    try:
        descriptor = os.open(lock_path, flags, 0o600)
    except FileExistsError as exc:
        raise RuffCorrectionApplyError(
            "RUFF_CORRECTION_APPLY_LOCK_EXISTS:" + str(lock_path)
        ) from exc
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write("transaction_id=" + transaction_id + "\n")
            handle.write("created_at_utc=" + utc_now() + "\n")
        yield
    finally:
        try:
            lock_path.unlink()
        except OSError:
            pass


def _transaction_id(preview_id: str, manifest_identity: str) -> str:
    """Return a readable transaction identifier."""
    digest = hashlib.sha256(
        (preview_id + "\0" + manifest_identity + "\0" + utc_now()).encode("utf-8")
    ).hexdigest()
    stamp = utc_now().replace("-", "").replace(":", "")
    stamp = stamp.replace("T", "t").replace("Z", "z")
    return "ruff3a-apply-" + stamp + "-" + digest[:12]


def _bounded_text(value: object, limit: int = 1200) -> str:
    """Return one bounded single-line diagnostic string."""
    compact = " ".join(str(value or "").split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."
