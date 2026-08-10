# project-path: kanda_reasoner_app/engineering_diagnostics_patch_preview/preview.py
"""Create exact, isolated, non-installable governed patch preview bundles."""

from __future__ import annotations

import difflib
import hashlib
import json
from pathlib import Path
import shutil
from typing import Callable, Sequence
import uuid
import zipfile

from kanda_reasoner_app.engineering_diagnostics import (
    DiagnosticFindingRecord,
    DiagnosticRemediationIntent,
    DiagnosticRunRecord,
)

from .models import (
    PATCH_PREVIEW_FEATURE_ID,
    GovernedPatchPreviewFile,
    GovernedPatchPreviewRecord,
)
from .policy import build_governed_patch_preview_plan
from .storage import (
    atomic_write_bytes,
    atomic_write_json,
    atomic_write_text,
    resolve_patch_preview_paths,
    governed_preview_sha256_bytes,
    governed_preview_sha256_file,
    utc_now,
)
from .transformations import CommandRunner, build_isolated_proposed_bytes

__all__ = ["create_governed_patch_preview", "render_governed_patch_preview"]


def _preview_id(issue: str, original_sha256: str) -> str:
    attempt_nonce = uuid.uuid4().hex
    seed = hashlib.sha256(
        (PATCH_PREVIEW_FEATURE_ID + "|" + issue + "|" + original_sha256 + "|" + attempt_nonce).encode(
            "utf-8"
        )
    ).hexdigest()
    return "patch-preview-" + seed[:24]


def _diff(relative: str, before: bytes, after: bytes) -> str:
    try:
        before_text = before.decode("utf-8")
        after_text = after.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError("PATCH_PREVIEW_UTF8_SOURCE_REQUIRED") from exc
    return "".join(
        difflib.unified_diff(
            before_text.splitlines(keepends=True),
            after_text.splitlines(keepends=True),
            fromfile="a/" + relative,
            tofile="b/" + relative,
            lineterm="\n",
        )
    )


def _write_zip(path: Path, members: dict[str, bytes]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(members):
            info = zipfile.ZipInfo(name)
            info.date_time = (1980, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o600 << 16
            archive.writestr(info, members[name])
    temporary.replace(path)


def create_governed_patch_preview(
    project_root: str | Path,
    run: DiagnosticRunRecord,
    finding: DiagnosticFindingRecord,
    intent: DiagnosticRemediationIntent,
    *,
    decision_state: str,
    owner_status: str,
    approval_token: str,
    ruff_argv_prefix: Sequence[str] | None = None,
    command_runner: CommandRunner | None = None,
    after_source_read: Callable[[Path], None] | None = None,
) -> GovernedPatchPreviewRecord:
    """Create a durable proposal without modifying active Project source."""
    paths = resolve_patch_preview_paths(project_root)
    plan = build_governed_patch_preview_plan(
        paths.project_root,
        run,
        finding,
        intent,
        decision_state=decision_state,
        owner_status=owner_status,
        approval_token=approval_token,
    )
    source = (paths.project_root / plan.relative_path).resolve(strict=True)
    original = source.read_bytes()
    if governed_preview_sha256_bytes(original) != plan.original_sha256:
        raise RuntimeError("PATCH_PREVIEW_EXACT_SOURCE_PRECONDITION_FAILED")
    if after_source_read is not None:
        after_source_read(source)

    preview_id = _preview_id(plan.issue_fingerprint, plan.original_sha256)
    preview_root = paths.preview_root(preview_id)
    workspace_root = paths.workspace_root(preview_id)
    if preview_root.exists() or workspace_root.exists():
        raise RuntimeError("PATCH_PREVIEW_ID_COLLISION")
    workspace_file = workspace_root / plan.relative_path
    workspace_file.parent.mkdir(parents=True, exist_ok=True)
    workspace_file.write_bytes(original)
    try:
        proposed, markers = build_isolated_proposed_bytes(
            paths.project_root,
            workspace_file,
            plan,
            ruff_argv_prefix=ruff_argv_prefix,
            command_runner=command_runner,
        )
        if proposed == original:
            raise RuntimeError("PATCH_PREVIEW_NO_EXACT_DIFF")
        if governed_preview_sha256_file(source) != plan.original_sha256:
            raise RuntimeError("PATCH_PREVIEW_ACTIVE_SOURCE_CHANGED_DURING_PREVIEW")
        exact_diff = _diff(plan.relative_path, original, proposed)
        if not exact_diff.strip():
            raise RuntimeError("PATCH_PREVIEW_EXACT_DIFF_EMPTY")

        file_record = GovernedPatchPreviewFile(
            relative_path=plan.relative_path,
            original_sha256=plan.original_sha256,
            proposed_sha256=governed_preview_sha256_bytes(proposed),
            original_size_bytes=len(original),
            proposed_size_bytes=len(proposed),
            diff_sha256=governed_preview_sha256_bytes(exact_diff.encode("utf-8")),
        )
        manifest_path = preview_root / "PATCH_PREVIEW_MANIFEST.json"
        diff_path = preview_root / "PATCH_PREVIEW.diff"
        proposal_zip = preview_root / "PATCH_PREVIEW_PROPOSAL.zip"
        rollback_zip = preview_root / "PATCH_PREVIEW_ROLLBACK.zip"
        validation_markers = (
            *markers,
            "PATCH_PREVIEW_ORIGINAL_HASH_CAPTURED: PASS",
            "PATCH_PREVIEW_EXACT_SOURCE_PRECONDITION: PASS",
            "PATCH_PREVIEW_EXACT_DIFF: PASS",
            "PATCH_PREVIEW_ISOLATED_WORKSPACE: PASS",
            "PATCH_PREVIEW_ACTIVE_SOURCE_MUTATED: NO",
            "PATCH_PREVIEW_INSTALLABLE_ARTIFACT: NO",
            "PATCH_PREVIEW_UNIQUE_ATTEMPT_ID: PASS",
        )
        record = GovernedPatchPreviewRecord(
            preview_id=preview_id,
            status="PREVIEW_READY_FOR_GOVERNED_VALIDATION",
            project_root=str(paths.project_root),
            created_at_utc=utc_now(),
            plan=plan,
            file=file_record,
            preview_root=str(preview_root),
            manifest_path=str(manifest_path),
            diff_path=str(diff_path),
            proposal_zip_path=str(proposal_zip),
            rollback_zip_path=str(rollback_zip),
            validation_markers=validation_markers,
            warnings=(
                "This proposal is not an installable patch.",
                "Validate Project and normal governed delivery remain mandatory.",
            ),
        )
        preview_root.mkdir(parents=True, exist_ok=False)
        atomic_write_text(diff_path, exact_diff)
        atomic_write_bytes(preview_root / "original" / plan.relative_path, original)
        atomic_write_bytes(preview_root / "proposed" / plan.relative_path, proposed)
        atomic_write_json(manifest_path, record.to_dict())
        plan_text = "\n".join(
            [
                "Governed Patch Preview Validation Plan",
                "",
                *record.plan.focused_validation,
                "",
                *record.plan.required_project_validation,
                "",
                "Human confirmation does not authorize source mutation.",
            ]
        ) + "\n"
        atomic_write_text(preview_root / "VALIDATION_PLAN.txt", plan_text)
        manifest_bytes = json.dumps(
            record.to_dict(), ensure_ascii=True, sort_keys=True, indent=2
        ).encode("ascii") + b"\n"
        _write_zip(
            proposal_zip,
            {
                "PATCH_PREVIEW_MANIFEST.json": manifest_bytes,
                "PATCH_PREVIEW.diff": exact_diff.encode("utf-8"),
                "VALIDATION_PLAN.txt": plan_text.encode("utf-8"),
                "proposed/" + plan.relative_path: proposed,
            },
        )
        _write_zip(
            rollback_zip,
            {
                "ROLLBACK_MANIFEST.json": json.dumps(
                    {
                        "schema_version": "1.0",
                        "preview_id": preview_id,
                        "relative_path": plan.relative_path,
                        "original_sha256": plan.original_sha256,
                        "source_mutation_authorized": False,
                    },
                    ensure_ascii=True,
                    sort_keys=True,
                    indent=2,
                ).encode("ascii")
                + b"\n",
                "original/" + plan.relative_path: original,
            },
        )
        return record
    except Exception:
        shutil.rmtree(preview_root, ignore_errors=True)
        raise
    finally:
        shutil.rmtree(workspace_root, ignore_errors=True)


def render_governed_patch_preview(record: GovernedPatchPreviewRecord) -> str:
    """Render one compact human-review summary and exact diff."""
    diff = Path(record.diff_path).read_text(encoding="utf-8")
    lines = [
        "Governed Patch Preview",
        "Preview ID: " + record.preview_id,
        "Status: " + record.status,
        "Correction: " + record.plan.correction_kind,
        "Issue: " + record.plan.issue_fingerprint,
        "File: " + record.file.relative_path,
        "Original SHA-256: " + record.file.original_sha256,
        "Proposed SHA-256: " + record.file.proposed_sha256,
        "Proposal ZIP: " + record.proposal_zip_path,
        "Rollback ZIP: " + record.rollback_zip_path,
        "Installable: NO",
        "Source mutation executed: NO",
        "",
        "EXACT DIFF",
        diff,
    ]
    return "\n".join(lines)
