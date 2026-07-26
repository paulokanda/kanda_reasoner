# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/main_workbench_web_ai_package.py
"""Atomic, deduplicated Web AI packages from sealed Main Workbench evidence."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import shutil
from typing import Any
import uuid
import zipfile

from .external_ai_candidate_exchange_contract import (
    CandidateSetIdentity,
    ExchangeIdentity,
    build_candidate_set_identity,
    build_exchange_identity,
)
from .external_ai_exchange_workspace import external_ai_exchange_workspace_root
from .main_workbench_state_store import (
    MainWorkbenchTerminalSeal,
    terminal_seal_is_current,
    terminal_seal_matches_evidence,
)
from .main_workbench_web_ai_prompt import build_main_workbench_web_ai_task
from .main_workbench_web_ai_package_io import (
    build_package_manifest,
    candidate_hashes,
    collect_project_context,
    canonical_hash,
    copy_baseline_target,
    copy_candidate_family,
    copy_project_context,
    hash_file,
    json_ready,
    preview_identity_hash,
    project_context_identity,
    sanitize_project_paths,
    verify_package_manifest,
    verify_package_zip,
    write_json,
    write_package_zip,
)
from .workbench_project_support_paths import exchange_root_blockers

__all__ = [
    "MAIN_WORKBENCH_WEB_AI_PACKAGE_FEATURE_ID",
    "MainWorkbenchWebAIPackageRequest",
    "MainWorkbenchWebAIPackageResult",
    "build_or_reuse_main_workbench_web_ai_package",
    "capture_main_workbench_web_ai_package_request",
]

MAIN_WORKBENCH_WEB_AI_PACKAGE_FEATURE_ID = (
    "main-workbench-complete-refactor-web-ai-package-v1"
)
_SCHEMA_VERSION = "1.0"


@dataclass(frozen=True)
class MainWorkbenchWebAIPackageRequest:
    """Immutable non-GUI evidence captured before background package work."""

    active_project_root: str
    terminal_seal: MainWorkbenchTerminalSeal
    snapshot: Any
    preview: Any
    structural: Any
    aqr_context: Any
    aqr_outcome: Any


@dataclass(frozen=True)
class MainWorkbenchWebAIPackageResult:
    """Describe one published or reused complete refactor exchange package."""

    feature_id: str
    exchange_id: str
    workspace_root: str
    exchange_root: str
    zip_path: str
    prompt_path: str
    manifest_path: str
    package_content_hash: str
    candidate_identity: CandidateSetIdentity
    exchange_identity: ExchangeIdentity
    candidate_files: tuple[str, ...]
    zip_sha256: str
    reused: bool


def capture_main_workbench_web_ai_package_request(
    *,
    window: object,
    active_project_root: str | Path,
    terminal_seal: MainWorkbenchTerminalSeal,
) -> MainWorkbenchWebAIPackageRequest:
    """Capture current card evidence on the GUI thread before background work."""
    project_root = Path(active_project_root).expanduser().resolve(strict=True)
    if not terminal_seal_is_current(window, terminal_seal):
        raise ValueError("MAIN_WORKBENCH_TERMINAL_SEAL_STALE")
    request = MainWorkbenchWebAIPackageRequest(
        active_project_root=str(project_root),
        terminal_seal=terminal_seal,
        snapshot=getattr(
            window,
            "_large_file_refactor_workbench_plan_snapshot",
            None,
        ),
        preview=getattr(
            window,
            "_large_file_refactor_workbench_real_preview",
            None,
        ),
        structural=getattr(
            window,
            "_large_file_refactor_workbench_structural_validation",
            None,
        ),
        aqr_context=getattr(
            window,
            "_large_file_refactor_workbench_aqr_context",
            None,
        ),
        aqr_outcome=getattr(
            window,
            "_large_file_refactor_workbench_advanced_quality_review",
            None,
        ),
    )
    _validate_request(request)
    return request


def build_or_reuse_main_workbench_web_ai_package(
    request: MainWorkbenchWebAIPackageRequest,
) -> MainWorkbenchWebAIPackageResult:
    """Build or reuse one package without reading Qt objects in the worker."""
    project_root = Path(request.active_project_root).resolve(strict=True)
    terminal_seal = request.terminal_seal
    snapshot = request.snapshot
    preview = request.preview
    structural = request.structural
    aqr_context = request.aqr_context
    aqr_outcome = request.aqr_outcome
    _validate_request(request)
    preview_root = Path(preview.preview_root).expanduser().resolve(strict=True)
    verified_candidate_hashes = candidate_hashes(preview_root, preview)
    project_context = collect_project_context(project_root)
    project_context_hash = project_context_identity(project_context)
    identity_source = _analysis_identity(
        snapshot=snapshot,
        preview=preview,
        aqr_context=aqr_context,
        project_root=project_root,
    )
    candidate_identity = build_candidate_set_identity(
        project_card_identity=str(identity_source["project_card_identity"]),
        target_relative_path=str(identity_source["target_relative_path"]),
        baseline_hash=str(identity_source["baseline_hash"]),
        preview_hash=str(identity_source["preview_hash"]),
        plan_hash=str(identity_source["plan_hash"]),
        candidate_file_hashes=verified_candidate_hashes,
    )
    content_payload = _package_content_payload(
        terminal_seal=terminal_seal,
        candidate_identity=candidate_identity,
        structural=structural,
        aqr_outcome=aqr_outcome,
        project_context_hash=project_context_hash,
    )
    package_content_hash = canonical_hash(content_payload)
    card_root = external_ai_exchange_workspace_root(
        project_root,
        candidate_identity.project_card_identity,
        candidate_identity.target_relative_path,
    ).resolve(strict=False)
    _require_exchange_root(project_root, card_root)
    card_root.mkdir(parents=True, exist_ok=True)
    existing = _find_reusable_package(
        card_root=card_root,
        package_content_hash=package_content_hash,
        candidate_identity=candidate_identity,
    )
    if existing is not None:
        return existing
    generation = _next_exchange_generation(card_root)
    exchange_id = f"EXCH-{generation:04d}"
    exchange_identity = build_exchange_identity(
        exchange_id=exchange_id,
        candidate_identity=candidate_identity,
        exchange_generation=generation,
    )
    final_root = (card_root / exchange_id).resolve(strict=False)
    final_zip = card_root / f"{exchange_id}__candidates_to_ai.zip"
    partial_root = card_root / (
        "." + exchange_id + ".partial-" + uuid.uuid4().hex[:12]
    )
    partial_zip = card_root / (
        "." + exchange_id + ".partial-" + uuid.uuid4().hex[:12] + ".zip"
    )
    _require_exchange_root(project_root, final_root)
    _require_exchange_root(project_root, partial_root)
    if final_root.exists() or final_zip.exists():
        raise FileExistsError("MAIN_WORKBENCH_EXCHANGE_GENERATION_COLLISION")
    published_root = False
    published_zip = False
    try:
        partial_root.mkdir(parents=True, exist_ok=False)
        copied = copy_candidate_family(preview_root, preview, partial_root)
        copied_context = copy_project_context(project_context, partial_root)
        copy_baseline_target(
            project_root,
            candidate_identity.target_relative_path,
            partial_root,
        )
        _write_context(
            destination=partial_root,
            project_root=project_root,
            snapshot=snapshot,
            preview=preview,
            structural=structural,
            aqr_outcome=aqr_outcome,
            terminal_seal=terminal_seal,
        )
        write_json(
            partial_root / "lineage" / "CANDIDATE_SET_IDENTITY.json",
            candidate_identity.to_dict(),
        )
        write_json(
            partial_root / "lineage" / "EXCHANGE_IDENTITY.json",
            exchange_identity.to_dict(),
        )
        prompt_path = partial_root / "EXTERNAL_AI_TASK.md"
        prompt_path.write_text(
            build_main_workbench_web_ai_task(
                candidate_identity=candidate_identity,
                exchange_identity=exchange_identity,
                candidate_files=copied,
                terminal_status=terminal_seal.terminal_status,
                blockers=terminal_seal.blockers,
            ),
            encoding="utf-8",
            newline="\n",
        )
        manifest_path = partial_root / "EXCHANGE_MANIFEST.json"
        manifest = build_package_manifest(
            root=partial_root,
            schema_version=_SCHEMA_VERSION,
            feature_id=MAIN_WORKBENCH_WEB_AI_PACKAGE_FEATURE_ID,
            package_content_hash=package_content_hash,
            candidate_identity_hash=candidate_identity.identity_hash,
            exchange_identity_hash=exchange_identity.identity_hash,
        )
        write_json(manifest_path, manifest)
        verify_package_manifest(partial_root, manifest)
        write_package_zip(partial_root, partial_zip)
        verify_package_zip(partial_root, partial_zip)
        if not terminal_seal_matches_evidence(
            seal=terminal_seal,
            active_project_root=project_root,
            snapshot=snapshot,
            preview=preview,
            structural=structural,
            aqr=aqr_outcome,
        ):
            raise ValueError("MAIN_WORKBENCH_SOURCE_CHANGED_DURING_PACKAGE_BUILD")
        current_context_hash = project_context_identity(
            collect_project_context(project_root)
        )
        if current_context_hash != project_context_hash:
            raise ValueError("MAIN_WORKBENCH_PROJECT_CONTEXT_CHANGED_DURING_BUILD")
        if not copied_context:
            raise ValueError("MAIN_WORKBENCH_PROJECT_CONTEXT_EMPTY")
        partial_root.replace(final_root)
        published_root = True
        partial_zip.replace(final_zip)
        published_zip = True
        return MainWorkbenchWebAIPackageResult(
            feature_id=MAIN_WORKBENCH_WEB_AI_PACKAGE_FEATURE_ID,
            exchange_id=exchange_id,
            workspace_root=str(card_root),
            exchange_root=str(final_root),
            zip_path=str(final_zip),
            prompt_path=str(final_root / "EXTERNAL_AI_TASK.md"),
            manifest_path=str(final_root / "EXCHANGE_MANIFEST.json"),
            package_content_hash=package_content_hash,
            candidate_identity=candidate_identity,
            exchange_identity=exchange_identity,
            candidate_files=tuple(copied),
            zip_sha256=hash_file(final_zip),
            reused=False,
        )
    except Exception:
        shutil.rmtree(partial_root, ignore_errors=True)
        partial_zip.unlink(missing_ok=True)
        if published_zip:
            final_zip.unlink(missing_ok=True)
        if published_root:
            shutil.rmtree(final_root, ignore_errors=True)
        raise


def _validate_request(request: MainWorkbenchWebAIPackageRequest) -> None:
    """Fail closed when captured evidence no longer matches its terminal seal."""
    if not terminal_seal_matches_evidence(
        seal=request.terminal_seal,
        active_project_root=request.active_project_root,
        snapshot=request.snapshot,
        preview=request.preview,
        structural=request.structural,
        aqr=request.aqr_outcome,
    ):
        raise ValueError("MAIN_WORKBENCH_TERMINAL_SEAL_STALE")
    _validate_state(
        snapshot=request.snapshot,
        preview=request.preview,
        terminal_seal=request.terminal_seal,
    )


def _validate_state(*, snapshot: Any, preview: Any, terminal_seal: MainWorkbenchTerminalSeal) -> None:
    if snapshot is None or not bool(snapshot.integrity_valid()):
        raise ValueError("MAIN_WORKBENCH_PLAN_SNAPSHOT_INVALID")
    if preview is None or str(getattr(preview, "status", "")) != "real_preview_written":
        raise ValueError("MAIN_WORKBENCH_PREVIEW_NOT_READY")
    if tuple(getattr(preview, "blockers", ()) or ()):
        raise ValueError("MAIN_WORKBENCH_PREVIEW_BLOCKED")
    if terminal_seal.terminal_status not in {
        "READY_FOR_WEB_AI",
        "WEB_AI_REQUIRED_WITH_BLOCKERS",
    }:
        raise ValueError("MAIN_WORKBENCH_TERMINAL_STATUS_NOT_PACKAGEABLE")


def _analysis_identity(
    *,
    snapshot: Any,
    preview: Any,
    aqr_context: Any,
    project_root: Path,
) -> dict[str, str]:
    if aqr_context is not None:
        identity = aqr_context.request.analysis_identity
        if str(identity.project_card_identity) != str(snapshot.snapshot_hash):
            raise ValueError("MAIN_WORKBENCH_AQR_CARD_IDENTITY_MISMATCH")
        return {
            "project_card_identity": str(identity.project_card_identity),
            "target_relative_path": str(identity.target_relative_path),
            "baseline_hash": str(identity.baseline_hash),
            "preview_hash": str(identity.preview_hash),
            "plan_hash": str(identity.refactor_plan_hash),
        }
    target = Path(str(snapshot.target_file)).resolve()
    try:
        target_relative = target.relative_to(project_root).as_posix()
    except ValueError as error:
        raise ValueError("MAIN_WORKBENCH_TARGET_OUTSIDE_ACTIVE_PROJECT") from error
    return {
        "project_card_identity": str(snapshot.snapshot_hash),
        "target_relative_path": target_relative,
        "baseline_hash": str(snapshot.source_content_hash),
        "preview_hash": preview_identity_hash(preview),
        "plan_hash": canonical_hash(json.loads(snapshot.plan_json)),
    }



def _write_context(
    *,
    destination: Path,
    project_root: Path,
    snapshot: Any,
    preview: Any,
    structural: Any,
    aqr_outcome: Any,
    terminal_seal: MainWorkbenchTerminalSeal,
) -> None:
    context = destination / "context"
    write_json(context / "workbench_plan.json", json.loads(snapshot.plan_json))
    write_json(context / "module_analysis.json", json.loads(snapshot.analysis_json))
    write_json(context / "preview_manifest.json", sanitize_project_paths(json_ready(preview), project_root))
    write_json(context / "structural_validation.json", sanitize_project_paths(json_ready(structural), project_root))
    write_json(context / "advanced_quality_review.json", sanitize_project_paths(json_ready(aqr_outcome), project_root))
    write_json(context / "main_workbench_terminal_seal.json", terminal_seal.to_dict())
    write_json(
        context / "ownership_model.json",
        {
            "tool_role": "reusable_card_machine",
            "active_project_role": "card_owner",
            "selected_module_role": "inserted_card",
            "preview_role": "project_owned_candidate_evidence",
            "canonical_source_mutated": False,
        },
    )


def _package_content_payload(
    *,
    terminal_seal: MainWorkbenchTerminalSeal,
    candidate_identity: CandidateSetIdentity,
    structural: Any,
    aqr_outcome: Any,
    project_context_hash: str,
) -> dict[str, Any]:
    return {
        "schema_version": _SCHEMA_VERSION,
        "feature_id": MAIN_WORKBENCH_WEB_AI_PACKAGE_FEATURE_ID,
        "terminal_status": terminal_seal.terminal_status,
        "candidate_identity_hash": candidate_identity.identity_hash,
        "structural_hash": canonical_hash(json_ready(structural)),
        "aqr_hash": canonical_hash(json_ready(aqr_outcome)),
        "blocker_hash": terminal_seal.blocker_hash,
        "project_context_hash": project_context_hash,
        "prompt_schema": "main_workbench_complete_refactor_v1",
    }


def _find_reusable_package(
    *,
    card_root: Path,
    package_content_hash: str,
    candidate_identity: CandidateSetIdentity,
) -> MainWorkbenchWebAIPackageResult | None:
    for root in sorted(card_root.glob("EXCH-*"), reverse=True):
        if not root.is_dir():
            continue
        manifest_path = root / "EXCHANGE_MANIFEST.json"
        if not manifest_path.is_file():
            continue
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError):
            continue
        if str(manifest.get("package_content_hash", "")) != package_content_hash:
            continue
        if str(manifest.get("candidate_identity_hash", "")) != candidate_identity.identity_hash:
            continue
        exchange_payload = json.loads(
            (root / "lineage" / "EXCHANGE_IDENTITY.json").read_text(encoding="utf-8-sig")
        )
        exchange_identity = ExchangeIdentity(**exchange_payload)
        zip_path = card_root / f"{exchange_identity.exchange_id}__candidates_to_ai.zip"
        if not zip_path.is_file():
            continue
        try:
            verify_package_manifest(root, manifest)
            verify_package_zip(root, zip_path)
        except (OSError, TypeError, ValueError, zipfile.BadZipFile):
            continue
        candidate_members = {
            str(item.get("relative_path") or ""): str(item.get("sha256") or "")
            for item in tuple(manifest.get("candidate_files") or ())
            if isinstance(item, dict)
        }
        if canonical_hash(candidate_members) != candidate_identity.candidate_set_hash:
            continue
        if exchange_identity.identity_hash != str(
            manifest.get("exchange_identity_hash") or ""
        ):
            continue
        if exchange_identity.candidate_identity_hash != candidate_identity.identity_hash:
            continue
        candidates = tuple(
            item["relative_path"]
            for item in manifest.get("candidate_files", [])
            if isinstance(item, dict) and item.get("relative_path")
        )
        return MainWorkbenchWebAIPackageResult(
            feature_id=MAIN_WORKBENCH_WEB_AI_PACKAGE_FEATURE_ID,
            exchange_id=exchange_identity.exchange_id,
            workspace_root=str(card_root),
            exchange_root=str(root),
            zip_path=str(zip_path),
            prompt_path=str(root / "EXTERNAL_AI_TASK.md"),
            manifest_path=str(manifest_path),
            package_content_hash=package_content_hash,
            candidate_identity=candidate_identity,
            exchange_identity=exchange_identity,
            candidate_files=candidates,
            zip_sha256=hash_file(zip_path),
            reused=True,
        )
    return None

def _next_exchange_generation(card_root: Path) -> int:
    values = []
    for path in card_root.glob("EXCH-*"):
        suffix = path.name[5:]
        if path.is_dir() and suffix.isdigit():
            values.append(int(suffix))
    return max(values, default=0) + 1


def _require_exchange_root(project_root: Path, candidate: Path) -> None:
    blockers = exchange_root_blockers(project_root, candidate)
    if blockers:
        raise ValueError("MAIN_WORKBENCH_EXCHANGE_OWNERSHIP_BLOCKED:" + "|".join(blockers))
