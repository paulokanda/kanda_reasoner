"""Structured-text bridge into the existing external AI return ZIP validator."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
from typing import Any
import zipfile

from .external_ai_candidate_exchange_contract import (
    build_ai_response_identity,
    build_candidate_set_identity,
)
from .external_ai_candidate_return_intake import (
    ExternalAIReturnGenerationResult,
    import_external_ai_candidate_answer,
)
from .workbench_project_support_paths import daily_work_root

__all__ = [
    "KANDA_AI_CANDIDATE_RETURN_BEGIN",
    "KANDA_AI_CANDIDATE_RETURN_END",
    "import_external_ai_candidate_answer_text",
]

KANDA_AI_CANDIDATE_RETURN_BEGIN = "KANDA_AI_CANDIDATE_RETURN_BEGIN"
KANDA_AI_CANDIDATE_RETURN_END = "KANDA_AI_CANDIDATE_RETURN_END"
_SCHEMA_VERSION = "1.0"
_MAX_MEMBER_BYTES = 64 * 1024 * 1024
_MAX_TOTAL_BYTES = 256 * 1024 * 1024


def import_external_ai_candidate_answer_text(
    *,
    active_project_root: str | Path,
    exchange_result: Any,
    answer_text: str,
    active_project_card_identity: str,
    active_target_relative_path: str,
    active_preview_hash: str,
) -> ExternalAIReturnGenerationResult:
    """Convert bounded structured text to transient ZIP and reuse canonical intake."""
    project_root = Path(active_project_root).expanduser().resolve(strict=True)
    payload = _parse_structured_answer(answer_text)
    candidates = _validate_payload(payload, exchange_result)
    staging_root = (
        daily_work_root(project_root)
        / "ai_candidate_text_return_staging"
        / exchange_result.exchange_identity.exchange_id
    )
    if staging_root.exists():
        shutil.rmtree(staging_root)
    staging_root.mkdir(parents=True, exist_ok=False)
    zip_path = staging_root / "structured_ai_answer.zip"
    try:
        _write_transient_return_zip(zip_path, exchange_result, candidates)
        return import_external_ai_candidate_answer(
            active_project_root=project_root,
            exchange_result=exchange_result,
            answer_zip_path=zip_path,
            active_project_card_identity=active_project_card_identity,
            active_target_relative_path=active_target_relative_path,
            active_preview_hash=active_preview_hash,
        )
    finally:
        shutil.rmtree(staging_root, ignore_errors=True)


def _parse_structured_answer(text: str) -> dict[str, Any]:
    value = str(text or "").strip()
    begin = value.find(KANDA_AI_CANDIDATE_RETURN_BEGIN)
    end = value.find(KANDA_AI_CANDIDATE_RETURN_END)
    if begin < 0 or end < 0 or end <= begin:
        raise ValueError("AI_RETURN_TEXT_MARKERS_MISSING_OR_INVALID")
    before = value[:begin].strip()
    after = value[end + len(KANDA_AI_CANDIDATE_RETURN_END):].strip()
    if before or after:
        raise ValueError("AI_RETURN_TEXT_EXTRA_CONTENT_OUTSIDE_MARKERS")
    body = value[begin + len(KANDA_AI_CANDIDATE_RETURN_BEGIN):end].strip()
    try:
        payload = json.loads(body)
    except json.JSONDecodeError as error:
        raise ValueError("AI_RETURN_TEXT_JSON_INVALID") from error
    if not isinstance(payload, dict):
        raise ValueError("AI_RETURN_TEXT_JSON_OBJECT_REQUIRED")
    return payload


def _validate_payload(payload: dict[str, Any], exchange_result: Any) -> dict[str, bytes]:
    if set(payload) != {"schema_version", "return_kind", "source_lineage", "candidate_family"}:
        raise ValueError("AI_RETURN_TEXT_SCHEMA_INVALID")
    if payload["schema_version"] != _SCHEMA_VERSION:
        raise ValueError("AI_RETURN_TEXT_SCHEMA_VERSION_UNSUPPORTED")
    if payload["return_kind"] != "candidate_generation_text":
        raise ValueError("AI_RETURN_TEXT_KIND_INVALID")
    lineage = payload["source_lineage"]
    if not isinstance(lineage, dict):
        raise ValueError("AI_RETURN_TEXT_LINEAGE_OBJECT_REQUIRED")
    exchange = exchange_result.exchange_identity
    expected_lineage = {
        "exchange_id": exchange.exchange_id,
        "project_card_identity": exchange.project_card_identity,
        "target_relative_path": exchange.target_relative_path,
        "source_preview_hash": exchange.source_preview_hash,
        "source_candidate_set_hash": exchange.source_candidate_set_hash,
        "source_exchange_identity_hash": exchange.identity_hash,
    }
    if lineage != expected_lineage:
        raise ValueError("AI_RETURN_TEXT_LINEAGE_MISMATCH")
    family = payload["candidate_family"]
    if not isinstance(family, list):
        raise ValueError("AI_RETURN_TEXT_CANDIDATE_FAMILY_LIST_REQUIRED")
    expected_paths = tuple(sorted(str(item) for item in exchange_result.candidate_files))
    candidates: dict[str, bytes] = {}
    total = 0
    for entry in family:
        if not isinstance(entry, dict) or set(entry) != {"relative_path", "content_utf8"}:
            raise ValueError("AI_RETURN_TEXT_CANDIDATE_ENTRY_INVALID")
        relative = _safe_relative(str(entry["relative_path"]))
        if relative in candidates:
            raise ValueError("AI_RETURN_TEXT_CANDIDATE_DUPLICATE:" + relative)
        content = entry["content_utf8"]
        if not isinstance(content, str):
            raise ValueError("AI_RETURN_TEXT_CONTENT_STRING_REQUIRED:" + relative)
        data = content.encode("utf-8")
        if len(data) > _MAX_MEMBER_BYTES:
            raise ValueError("AI_RETURN_TEXT_MEMBER_TOO_LARGE:" + relative)
        total += len(data)
        if total > _MAX_TOTAL_BYTES:
            raise ValueError("AI_RETURN_TEXT_TOTAL_TOO_LARGE")
        candidates[relative] = data
    if tuple(sorted(candidates)) != expected_paths:
        raise ValueError("AI_RETURN_TEXT_CANDIDATE_PATHS_MISMATCH")
    return candidates


def _write_transient_return_zip(
    zip_path: Path,
    exchange_result: Any,
    candidates: dict[str, bytes],
) -> None:
    hashes = {name: hashlib.sha256(data).hexdigest() for name, data in candidates.items()}
    source_identity = exchange_result.candidate_identity
    return_identity = build_candidate_set_identity(
        project_card_identity=source_identity.project_card_identity,
        target_relative_path=source_identity.target_relative_path,
        baseline_hash=source_identity.baseline_hash,
        preview_hash=source_identity.preview_hash,
        plan_hash=source_identity.plan_hash,
        candidate_file_hashes=hashes,
    )
    response_identity = build_ai_response_identity(
        exchange_identity=exchange_result.exchange_identity,
        return_candidate_set_hash=return_identity.candidate_set_hash,
        return_schema_version=_SCHEMA_VERSION,
    )
    manifest = {
        "schema_version": _SCHEMA_VERSION,
        "return_schema_version": _SCHEMA_VERSION,
        "return_kind": "candidate_generation",
        "exchange_id": exchange_result.exchange_identity.exchange_id,
        "source_exchange_identity_hash": exchange_result.exchange_identity.identity_hash,
        "response_identity_hash": response_identity.identity_hash,
        "candidate_files": [
            {
                "relative_path": name,
                "sha256": hashes[name],
                "size_bytes": len(candidates[name]),
            }
            for name in sorted(candidates)
        ],
    }
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            "AI_RETURN_MANIFEST.json",
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        )
        archive.writestr(
            "lineage/AI_RESPONSE_IDENTITY.json",
            json.dumps(response_identity.to_dict(), indent=2, sort_keys=True) + "\n",
        )
        for name in sorted(candidates):
            archive.writestr("candidate_family/" + name, candidates[name])


def _safe_relative(value: str) -> str:
    text = str(value or "").replace("\\", "/").strip()
    path = PurePosixPath(text)
    if not text or path.is_absolute() or ".." in path.parts:
        raise ValueError("AI_RETURN_TEXT_RELATIVE_PATH_INVALID")
    if ":" in path.parts[0]:
        raise ValueError("AI_RETURN_TEXT_DRIVE_PATH_FORBIDDEN")
    return path.as_posix()
