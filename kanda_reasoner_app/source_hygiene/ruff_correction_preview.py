# project-path: kanda_reasoner_app/source_hygiene/ruff_correction_preview.py
"""Create reviewed Ruff correction previews in disposable and support roots."""

from __future__ import annotations

from pathlib import Path
import shutil
from typing import Sequence

from .ruff_correction_discovery import (
    _apply_safe_corrections_to_shadow,
    _copy_candidates_to_shadow,
    _decode_utf8,
    _format_candidate_paths,
    _load_source_payloads,
    _require_policy_version,
    _resolve_scope_targets,
    _safe_lint_candidate_counts,
)
from .ruff_correction_errors import RuffCorrectionPreviewError
from .ruff_correction_identity import (
    _manifest_identity_payload,
    _new_preview_id,
    _preview_payload_digest,
    _preview_readme,
    _preview_seed,
    _snapshot_digest,
    _unified_diff,
    _verify_active_source_unchanged,
)
from .ruff_correction_models import (
    RuffCorrectionFileRecord,
    RuffCorrectionPreviewRecord,
)
from .ruff_correction_storage import (
    atomic_write_json,
    atomic_write_text,
    canonical_json_bytes,
    copy_file,
    resolve_ruff_correction_paths,
    sha256_bytes,
    utc_now,
)
from .ruff_policy_identity import resolve_ruff_policy_identity
from .ruff_quality_runtime import (
    _DEFAULT_RUFF_TIMEOUT_SECONDS,
    _resolve_ruff_command,
    _run_ruff_process,
)
from .ruff_quality_scope import _build_ruff_quality_scope

__all__ = ["create_ruff_correction_preview"]

_DEFAULT_MAX_FILES = 100


def create_ruff_correction_preview(
    project_root: str | Path,
    *,
    scope_paths: Sequence[str | Path] | None = None,
    max_files: int = _DEFAULT_MAX_FILES,
    ruff_argv_prefix: Sequence[str] | None = None,
    timeout_seconds: float = _DEFAULT_RUFF_TIMEOUT_SECONDS,
) -> RuffCorrectionPreviewRecord:
    """Create a read-only active-source preview using a disposable shadow copy."""
    paths = resolve_ruff_correction_paths(project_root)
    root = paths.project_root
    if int(max_files) <= 0:
        raise RuffCorrectionPreviewError("RUFF_CORRECTION_MAX_FILES_NOT_POSITIVE")
    if float(timeout_seconds) <= 0:
        raise RuffCorrectionPreviewError("RUFF_CORRECTION_TIMEOUT_NOT_POSITIVE")

    policy = resolve_ruff_policy_identity(root)
    identity = _resolve_ruff_command(
        ruff_argv_prefix,
        timeout_seconds=timeout_seconds,
    )
    _require_policy_version(identity.version, policy.required_version)
    targets, scope_display = _resolve_scope_targets(root, scope_paths)
    scope = _build_ruff_quality_scope(root)
    cache_before = (root / ".ruff_cache").exists()

    lint_result = _run_ruff_process(
        (
            *identity.argv_prefix,
            *scope.global_argv,
            "check",
            "--output-format",
            "json",
            "--exit-zero",
            "--no-cache",
            "--color",
            "never",
            *scope.command_argv,
            *(str(item) for item in targets),
        ),
        cwd=root,
        timeout_seconds=timeout_seconds,
    )
    if lint_result.returncode != 0:
        raise RuffCorrectionPreviewError(
            "RUFF_CORRECTION_LINT_DISCOVERY_FAILED:"
            + _bounded_text(lint_result.stderr or lint_result.stdout)
        )

    format_result = _run_ruff_process(
        (
            *identity.argv_prefix,
            *scope.global_argv,
            "format",
            "--check",
            "--no-cache",
            "--color",
            "never",
            *scope.command_argv,
            *(str(item) for item in targets),
        ),
        cwd=root,
        timeout_seconds=timeout_seconds,
    )
    if format_result.returncode not in (0, 1):
        raise RuffCorrectionPreviewError(
            "RUFF_CORRECTION_FORMAT_DISCOVERY_FAILED:"
            + _bounded_text(format_result.stderr or format_result.stdout)
        )

    safe_lint_counts = _safe_lint_candidate_counts(lint_result.stdout, root)
    format_candidates = _format_candidate_paths(format_result.stdout, root)
    candidate_relatives = tuple(
        sorted(set(safe_lint_counts) | set(format_candidates), key=str.casefold)
    )
    if len(candidate_relatives) > int(max_files):
        raise RuffCorrectionPreviewError(
            "RUFF_CORRECTION_CANDIDATE_LIMIT_EXCEEDED:"
            + str(len(candidate_relatives))
            + ":"
            + str(max_files)
        )

    source_payloads = _load_source_payloads(root, candidate_relatives)
    source_snapshot = _snapshot_digest(source_payloads)
    preview_seed = _preview_seed(
        project_root=root,
        policy_token=policy.identity_token,
        ruff_version=identity.version,
        source_snapshot=source_snapshot,
        scope_paths=scope_display,
    )
    preview_id = _new_preview_id(preview_seed)
    preview_root = paths.preview_root(preview_id)
    payload_root = preview_root / "payload"
    manifest_path = preview_root / "preview_manifest.json"
    diff_path = preview_root / "preview.diff"
    shadow_root = paths.shadow_root(preview_id)
    if preview_root.exists() or shadow_root.exists():
        raise RuffCorrectionPreviewError("RUFF_CORRECTION_PREVIEW_ID_COLLISION")

    preview_root.mkdir(parents=True, exist_ok=False)
    try:
        changed_records, combined_diff = _build_shadow_preview(
            root=root,
            shadow_root=shadow_root,
            payload_root=payload_root,
            config_relative_path=policy.config_relative_path,
            candidate_relatives=candidate_relatives,
            source_payloads=source_payloads,
            safe_lint_counts=safe_lint_counts,
            format_candidates=format_candidates,
            ruff_argv_prefix=identity.argv_prefix,
            timeout_seconds=timeout_seconds,
        )
        _verify_active_source_unchanged(root, source_payloads)
        if not cache_before and (root / ".ruff_cache").exists():
            raise RuffCorrectionPreviewError("RUFF_CORRECTION_PROJECT_CACHE_LEAK")

        preview_payload_digest = _preview_payload_digest(changed_records)
        status = "PREVIEW_READY" if changed_records else "NO_CHANGES"
        core_identity = _manifest_identity_payload(
            preview_id=preview_id,
            project_root=root,
            ruff_version=identity.version,
            policy_token=policy.identity_token,
            policy_sha256=policy.config_sha256,
            source_snapshot=source_snapshot,
            preview_payload_digest=preview_payload_digest,
            scope_paths=scope_display,
            files=changed_records,
        )
        manifest_identity = sha256_bytes(canonical_json_bytes(core_identity))
        confirm_token = (
            "APPLY_RUFF_CORRECTION_" + preview_id.upper() if changed_records else ""
        )
        record = RuffCorrectionPreviewRecord(
            preview_id=preview_id,
            status=status,
            project_root=str(root),
            created_at_utc=utc_now(),
            ruff_version=identity.version,
            ruff_command_source=identity.source,
            policy_identity_token=policy.identity_token,
            policy_config_sha256=policy.config_sha256,
            scope_paths=scope_display,
            candidate_file_count=len(candidate_relatives),
            changed_file_count=len(changed_records),
            source_snapshot_sha256=source_snapshot,
            preview_payload_sha256=preview_payload_digest,
            manifest_identity_sha256=manifest_identity,
            confirm_token=confirm_token,
            preview_root=str(preview_root),
            manifest_path=str(manifest_path),
            diff_path=str(diff_path),
            payload_root=str(payload_root),
            files=tuple(changed_records),
            warnings=_preview_warnings(),
        )
        atomic_write_text(
            diff_path,
            combined_diff or "No Ruff-safe correction changes were found.\n",
        )
        atomic_write_json(manifest_path, record.to_dict())
        atomic_write_text(preview_root / "README.txt", _preview_readme(record))
        return record
    except Exception:
        if preview_root.exists():
            shutil.rmtree(preview_root, ignore_errors=True)
        raise


def _build_shadow_preview(
    *,
    root: Path,
    shadow_root: Path,
    payload_root: Path,
    config_relative_path: str,
    candidate_relatives: Sequence[str],
    source_payloads: dict[str, bytes],
    safe_lint_counts: dict[str, int],
    format_candidates: set[str],
    ruff_argv_prefix: Sequence[str],
    timeout_seconds: float,
) -> tuple[list[RuffCorrectionFileRecord], str]:
    """Apply safe corrections to a shadow tree and build exact preview records."""
    records: list[RuffCorrectionFileRecord] = []
    diff_parts: list[str] = []
    try:
        shadow_root.mkdir(parents=True, exist_ok=False)
        copy_file(root / config_relative_path, shadow_root / "ruff.toml")
        shadow_files = _copy_candidates_to_shadow(
            root,
            shadow_root,
            candidate_relatives,
        )
        if shadow_files:
            _apply_safe_corrections_to_shadow(
                ruff_argv_prefix,
                shadow_root,
                shadow_files,
                timeout_seconds,
            )
        for relative in candidate_relatives:
            source_bytes = source_payloads[relative]
            shadow_file = shadow_root / relative
            preview_bytes = shadow_file.read_bytes()
            if preview_bytes == source_bytes:
                continue
            source_text = _decode_utf8(source_bytes, relative, "source")
            preview_text = _decode_utf8(preview_bytes, relative, "preview")
            diff_text = _unified_diff(relative, source_text, preview_text)
            if not diff_text:
                raise RuffCorrectionPreviewError(
                    "RUFF_CORRECTION_CHANGED_FILE_DIFF_EMPTY:" + relative
                )
            copy_file(shadow_file, payload_root / relative)
            diff_parts.append(diff_text.rstrip("\n"))
            records.append(
                RuffCorrectionFileRecord(
                    relative_path=relative,
                    source_sha256=sha256_bytes(source_bytes),
                    preview_sha256=sha256_bytes(preview_bytes),
                    source_size_bytes=len(source_bytes),
                    preview_size_bytes=len(preview_bytes),
                    safe_lint_finding_count=safe_lint_counts.get(relative, 0),
                    format_required=relative in format_candidates,
                    diff_sha256=sha256_bytes(diff_text.encode("utf-8")),
                )
            )
    finally:
        if shadow_root.exists():
            shutil.rmtree(shadow_root, ignore_errors=True)
    combined = "\n".join(diff_parts)
    return records, combined + ("\n" if combined else "")


def _preview_warnings() -> tuple[str, ...]:
    """Return stable human-review warnings for every preview."""
    return (
        "Only Ruff safe lint fixes and Ruff formatting were applied to the "
        "disposable shadow copy.",
        "Active project source was not modified while creating this preview.",
        "Apply requires the exact preview ID and confirmation token.",
        "A stale source hash or changed Ruff policy blocks apply.",
    )


def _bounded_text(value: object, limit: int = 1200) -> str:
    """Return one bounded single-line diagnostic string."""
    compact = " ".join(str(value or "").split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."
