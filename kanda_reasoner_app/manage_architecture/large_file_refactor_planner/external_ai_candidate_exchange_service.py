"""Build lineage-bound outbound candidate exchanges for external AI review."""
from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
import hashlib
import json
from pathlib import Path
import shutil
from typing import Any
import zipfile

from .external_ai_candidate_exchange_contract import (
    CandidateSetIdentity,
    ExchangeIdentity,
    build_candidate_set_identity,
    build_exchange_identity,
)
from .external_ai_candidate_exchange_prompt import build_external_ai_candidate_review_task
from .external_ai_exchange_workspace import external_ai_exchange_workspace_root
from .workbench_project_support_paths import (
    ai_refactoring_card_exchange_root,
    exchange_root_blockers,
)

__all__ = [
    "EXTERNAL_AI_CANDIDATE_EXCHANGE_OUTBOUND_FEATURE_ID",
    "ExternalAICandidateExchangeResult",
    "clean_external_ai_exchange_folder",
    "create_external_ai_candidate_exchange",
]

EXTERNAL_AI_CANDIDATE_EXCHANGE_OUTBOUND_FEATURE_ID = (
    "external-ai-candidate-exchange-outbound-v1"
)
_EXCHANGE_SCHEMA_VERSION = "1.0"
_CONTEXT_DIR = "context"
_CANDIDATE_DIR = "candidate_family"
_BASELINE_DIR = "baseline_target"
_LINEAGE_DIR = "lineage"
_BUNDLE_MANIFEST = Path(
    "workbench/_bundle_temp/BUNDLE_MANIFEST_EXTERNAL_AI_CANDIDATE_EXCHANGE.txt"
)


@dataclass(frozen=True)
class ExternalAICandidateExchangeResult:
    """Describe one complete outbound exchange package and its lineage."""

    feature_id: str
    exchange_id: str
    workspace_root: str
    exchange_root: str
    zip_path: str
    prompt_path: str
    manifest_path: str
    candidate_identity: CandidateSetIdentity
    exchange_identity: ExchangeIdentity
    candidate_files: tuple[str, ...]
    package_file_count: int
    zip_sha256: str


def create_external_ai_candidate_exchange(
    *,
    active_project_root: str | Path,
    plan_snapshot: Any,
    preview_result: Any,
    aqr_context: Any,
    aqr_outcome: Any,
    completion_evidence: Any,
) -> ExternalAICandidateExchangeResult:
    """Create one complete context ZIP under the selected Project support root."""
    project_root = Path(active_project_root).expanduser().resolve(strict=True)
    _validate_required_state(
        plan_snapshot=plan_snapshot,
        preview_result=preview_result,
        aqr_context=aqr_context,
        aqr_outcome=aqr_outcome,
        completion_evidence=completion_evidence,
    )
    identity = aqr_context.request.analysis_identity
    if aqr_outcome.analysis_identity_hash != identity.identity_hash:
        raise ValueError("AI_EXCHANGE_AQR_IDENTITY_MISMATCH")
    if identity.project_card_identity != plan_snapshot.snapshot_hash:
        raise ValueError("AI_EXCHANGE_CARD_IDENTITY_MISMATCH")

    preview_root = Path(preview_result.preview_root).expanduser().resolve(strict=True)
    candidate_hashes = _candidate_hashes(preview_root, preview_result)
    candidate_identity = build_candidate_set_identity(
        project_card_identity=identity.project_card_identity,
        target_relative_path=identity.target_relative_path,
        baseline_hash=identity.baseline_hash,
        preview_hash=identity.preview_hash,
        plan_hash=identity.refactor_plan_hash,
        candidate_file_hashes=candidate_hashes,
    )

    card_root = external_ai_exchange_workspace_root(
        project_root,
        identity.project_card_identity,
        identity.target_relative_path,
    ).resolve(strict=False)
    blockers = exchange_root_blockers(project_root, card_root)
    if blockers:
        raise ValueError("AI_EXCHANGE_OWNERSHIP_BLOCKED:" + "|".join(blockers))
    card_root.mkdir(parents=True, exist_ok=True)
    generation = _next_exchange_generation(card_root)
    exchange_id = f"EXCH-{generation:04d}"
    exchange_identity = build_exchange_identity(
        exchange_id=exchange_id,
        candidate_identity=candidate_identity,
        exchange_generation=generation,
    )
    exchange_root = (card_root / exchange_id).resolve(strict=False)
    blockers = exchange_root_blockers(project_root, exchange_root)
    if blockers:
        raise ValueError("AI_EXCHANGE_OWNERSHIP_BLOCKED:" + "|".join(blockers))
    if exchange_root.exists():
        raise FileExistsError("AI_EXCHANGE_ID_ALREADY_EXISTS:" + exchange_id)
    exchange_root.mkdir(parents=True, exist_ok=False)

    try:
        copied_candidates = _copy_candidate_family(
            preview_root,
            preview_result,
            exchange_root / _CANDIDATE_DIR,
        )
        _copy_baseline_target(
            project_root,
            identity.target_relative_path,
            exchange_root / _BASELINE_DIR,
        )
        _write_context_files(
            exchange_root=exchange_root,
            project_root=project_root,
            plan_snapshot=plan_snapshot,
            preview_result=preview_result,
            aqr_outcome=aqr_outcome,
            completion_evidence=completion_evidence,
        )
        _write_json(
            exchange_root / _LINEAGE_DIR / "CANDIDATE_SET_IDENTITY.json",
            candidate_identity.to_dict(),
        )
        _write_json(
            exchange_root / _LINEAGE_DIR / "EXCHANGE_IDENTITY.json",
            exchange_identity.to_dict(),
        )
        prompt_path = exchange_root / "EXTERNAL_AI_TASK.md"
        prompt_path.write_text(
            build_external_ai_candidate_review_task(
                candidate_identity=candidate_identity,
                exchange_identity=exchange_identity,
                candidate_files=copied_candidates,
            ),
            encoding="utf-8",
            newline="\n",
        )
        _write_bundle_manifest(exchange_root, exchange_identity)
        manifest_path = exchange_root / "EXCHANGE_MANIFEST.json"
        manifest = _build_exchange_manifest(
            exchange_root=exchange_root,
            candidate_identity=candidate_identity,
            exchange_identity=exchange_identity,
        )
        _write_json(manifest_path, manifest)
        zip_path = card_root / f"{exchange_id}__candidates_to_ai.zip"
        _write_exchange_zip(exchange_root, zip_path)
        return ExternalAICandidateExchangeResult(
            feature_id=EXTERNAL_AI_CANDIDATE_EXCHANGE_OUTBOUND_FEATURE_ID,
            exchange_id=exchange_id,
            workspace_root=str(card_root),
            exchange_root=str(exchange_root),
            zip_path=str(zip_path),
            prompt_path=str(prompt_path),
            manifest_path=str(manifest_path),
            candidate_identity=candidate_identity,
            exchange_identity=exchange_identity,
            candidate_files=tuple(copied_candidates),
            package_file_count=len(manifest["files"]),
            zip_sha256=_hash_file(zip_path),
        )
    except Exception:
        shutil.rmtree(exchange_root, ignore_errors=True)
        raise


def clean_external_ai_exchange_folder(
    *,
    active_project_root: str | Path,
    exchange_root: str | Path,
) -> tuple[str, ...]:
    """Delete contents of one active exchange folder after descendant checks."""
    project_root = Path(active_project_root).expanduser().resolve(strict=True)
    root = Path(exchange_root).expanduser().resolve(strict=False)
    blockers = exchange_root_blockers(project_root, root)
    if blockers:
        raise ValueError("AI_EXCHANGE_CLEAN_OWNERSHIP_BLOCKED:" + "|".join(blockers))
    card_root = ai_refactoring_card_exchange_root(
        project_root,
        _card_identity_from_exchange_root(project_root, root),
    ).resolve(strict=False)
    try:
        root.relative_to(card_root)
    except ValueError as error:
        raise ValueError("AI_EXCHANGE_CLEAN_NOT_CARD_DESCENDANT") from error
    if root == card_root:
        raise ValueError("AI_EXCHANGE_CLEAN_CARD_ROOT_FORBIDDEN")
    if not root.is_dir():
        return ()
    removed: list[str] = []
    for child in sorted(root.iterdir(), key=lambda item: item.name.lower()):
        try:
            child.resolve(strict=False).relative_to(root.resolve(strict=False))
        except ValueError as error:
            raise ValueError("AI_EXCHANGE_CLEAN_CHILD_ESCAPES_ROOT") from error
        removed.append(child.name)
        if child.is_dir() and not child.is_symlink():
            shutil.rmtree(child)
        else:
            child.unlink()
    return tuple(removed)


def _validate_required_state(
    *,
    plan_snapshot: Any,
    preview_result: Any,
    aqr_context: Any,
    aqr_outcome: Any,
    completion_evidence: Any,
) -> None:
    if plan_snapshot is None or not plan_snapshot.integrity_valid():
        raise ValueError("AI_EXCHANGE_PLAN_SNAPSHOT_INVALID")
    if preview_result is None or preview_result.status != "real_preview_written":
        raise ValueError("AI_EXCHANGE_PREVIEW_NOT_READY")
    if preview_result.blockers:
        raise ValueError("AI_EXCHANGE_PREVIEW_BLOCKED")
    if aqr_context is None or aqr_outcome is None:
        raise ValueError("AI_EXCHANGE_AQR_EVIDENCE_MISSING")
    if completion_evidence is None:
        raise ValueError("AI_EXCHANGE_COMPLETION_EVIDENCE_MISSING")


def _candidate_hashes(preview_root: Path, preview_result: Any) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for item in tuple(preview_result.files or ()):
        relative = _safe_relative(item.relative_path)
        source = (preview_root / relative).resolve(strict=True)
        _require_descendant(source, preview_root, "AI_EXCHANGE_CANDIDATE_ESCAPES_PREVIEW")
        observed = _hash_file(source)
        if observed != str(item.content_hash):
            raise ValueError("AI_EXCHANGE_CANDIDATE_HASH_MISMATCH:" + relative.as_posix())
        hashes[relative.as_posix()] = observed
    if not hashes:
        raise ValueError("AI_EXCHANGE_CANDIDATE_FAMILY_EMPTY")
    return dict(sorted(hashes.items()))


def _copy_candidate_family(
    preview_root: Path,
    preview_result: Any,
    destination_root: Path,
) -> list[str]:
    copied: list[str] = []
    for item in sorted(preview_result.files, key=lambda value: value.relative_path):
        relative = _safe_relative(item.relative_path)
        source = (preview_root / relative).resolve(strict=True)
        _require_descendant(source, preview_root, "AI_EXCHANGE_CANDIDATE_ESCAPES_PREVIEW")
        destination = destination_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())
        copied.append(relative.as_posix())
    return copied


def _copy_baseline_target(
    project_root: Path,
    target_relative_path: str,
    destination_root: Path,
) -> None:
    relative = _safe_relative(target_relative_path)
    source = (project_root / relative).resolve(strict=True)
    _require_descendant(source, project_root, "AI_EXCHANGE_BASELINE_TARGET_ESCAPES_PROJECT")
    destination = destination_root / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(source.read_bytes())


def _write_context_files(
    *,
    exchange_root: Path,
    project_root: Path,
    plan_snapshot: Any,
    preview_result: Any,
    aqr_outcome: Any,
    completion_evidence: Any,
) -> None:
    context_root = exchange_root / _CONTEXT_DIR
    _write_json(
        context_root / "workbench_plan.json",
        _sanitize_project_paths(json.loads(plan_snapshot.plan_json), project_root),
    )
    _write_json(
        context_root / "module_analysis.json",
        _sanitize_project_paths(json.loads(plan_snapshot.analysis_json), project_root),
    )
    _write_json(
        context_root / "preview_manifest.json",
        _sanitize_project_paths(_json_ready(preview_result), project_root),
    )
    _write_json(
        context_root / "advanced_quality_review.json",
        aqr_outcome.cross_check_report.to_dict(),
    )
    semantic = _json_ready(completion_evidence.semantic_review)
    text_diff = _bounded_text_diff(completion_evidence.text_diff)
    _write_json(
        context_root / "completion_review.json",
        _sanitize_project_paths({
            "semantic_review": semantic,
            "text_diff": text_diff,
            "shadow_validation_status": str(completion_evidence.shadow_validation.status),
            "contract_id": str(completion_evidence.contract.contract_id),
            "sealed_payload_hash": str(completion_evidence.sealed_payload.payload_hash),
        }, project_root),
    )


def _bounded_text_diff(report: Any, limit: int = 1200) -> dict[str, Any]:
    rows = []
    for row in tuple(getattr(report, "rows", ()) or ())[:limit]:
        rows.append(_json_ready(row))
    return {
        "status": str(getattr(report, "status", "unknown")),
        "rows": rows,
        "rows_truncated": len(tuple(getattr(report, "rows", ()) or ())) > limit,
        "warnings": [str(item) for item in tuple(getattr(report, "warnings", ()) or ())],
    }


def _write_bundle_manifest(
    exchange_root: Path,
    exchange_identity: ExchangeIdentity,
) -> None:
    """Write the auditable safety scope for the source-code exchange ZIP."""
    lines = (
        "BUNDLE TYPE: EXTERNAL_AI_CANDIDATE_EXCHANGE",
        "FEATURE ID: " + EXTERNAL_AI_CANDIDATE_EXCHANGE_OUTBOUND_FEATURE_ID,
        "EXCHANGE ID: " + exchange_identity.exchange_id,
        "SCOPE: candidate family, baseline target, bounded context, lineage, and task prompt",
        "VALIDATION: file hashes are recorded in EXCHANGE_MANIFEST.json",
        "ROLLBACK: remove this outbound exchange folder and ZIP; canonical source is unchanged",
    )
    manifest_path = exchange_root / _BUNDLE_MANIFEST
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _build_exchange_manifest(
    *,
    exchange_root: Path,
    candidate_identity: CandidateSetIdentity,
    exchange_identity: ExchangeIdentity,
) -> dict[str, Any]:
    files = []
    for path in sorted(exchange_root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(exchange_root).as_posix()
        files.append(
            {
                "relative_path": relative,
                "sha256": _hash_file(path),
                "size_bytes": path.stat().st_size,
            }
        )
    return {
        "schema_version": _EXCHANGE_SCHEMA_VERSION,
        "feature_id": EXTERNAL_AI_CANDIDATE_EXCHANGE_OUTBOUND_FEATURE_ID,
        "candidate_identity_hash": candidate_identity.identity_hash,
        "exchange_identity_hash": exchange_identity.identity_hash,
        "files": files,
    }


def _write_exchange_zip(exchange_root: Path, zip_path: Path) -> None:
    if zip_path.exists():
        raise FileExistsError("AI_EXCHANGE_ZIP_ALREADY_EXISTS:" + zip_path.name)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(exchange_root.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(exchange_root).as_posix())


def _next_exchange_generation(card_root: Path) -> int:
    generations = []
    for path in card_root.iterdir():
        if not path.is_dir() or not path.name.startswith("EXCH-"):
            continue
        suffix = path.name[5:]
        if suffix.isdigit():
            generations.append(int(suffix))
    return max(generations, default=0) + 1


def _card_identity_from_exchange_root(project_root: Path, exchange_root: Path) -> str:
    base = ai_refactoring_card_exchange_root(project_root, "placeholder").parent
    try:
        relative = exchange_root.resolve(strict=False).relative_to(base.resolve(strict=False))
    except ValueError as error:
        raise ValueError("AI_EXCHANGE_CLEAN_OUTSIDE_EXCHANGE_ROOT") from error
    if len(relative.parts) < 2:
        raise ValueError("AI_EXCHANGE_CLEAN_PATH_TOO_SHALLOW")
    return relative.parts[0]


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(_json_ready(payload), indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    path.write_text(text, encoding="utf-8", newline="\n")


def _json_ready(value: Any) -> Any:
    if is_dataclass(value):
        return _json_ready(asdict(value))
    if hasattr(value, "value") and isinstance(getattr(value, "value"), (str, int, float, bool)):
        return value.value
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_ready(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)



def _sanitize_project_paths(value: Any, project_root: Path) -> Any:
    """Replace absolute active-Project paths with stable project-relative paths."""
    if isinstance(value, dict):
        return {str(key): _sanitize_project_paths(item, project_root) for key, item in value.items()}
    if isinstance(value, list):
        return [_sanitize_project_paths(item, project_root) for item in value]
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return value
        try:
            path = Path(text).expanduser()
            if path.is_absolute():
                resolved = path.resolve(strict=False)
                relative = resolved.relative_to(project_root.resolve(strict=False))
                return relative.as_posix()
        except (OSError, ValueError):
            return value
    return value

def _safe_relative(value: str) -> Path:
    path = Path(str(value or "").replace("\\", "/"))
    if not str(value or "").strip() or path.is_absolute() or ".." in path.parts:
        raise ValueError("AI_EXCHANGE_RELATIVE_PATH_INVALID")
    return path


def _require_descendant(path: Path, root: Path, marker: str) -> None:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=False))
    except ValueError as error:
        raise ValueError(marker) from error


def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
