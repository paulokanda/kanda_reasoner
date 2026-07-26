# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/external_ai_candidate_exchange_contract.py
"""Immutable lineage contracts for external AI candidate exchange."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import PurePosixPath
from typing import Mapping

__all__ = [
    "EXTERNAL_AI_CANDIDATE_EXCHANGE_FOUNDATION_FEATURE_ID",
    "AIResponseIdentity",
    "CandidateSetIdentity",
    "ExchangeIdentity",
    "ai_response_identity_blockers",
    "build_ai_response_identity",
    "build_candidate_set_identity",
    "build_exchange_identity",
]

EXTERNAL_AI_CANDIDATE_EXCHANGE_FOUNDATION_FEATURE_ID = (
    "external-ai-candidate-exchange-foundation-v1"
)


@dataclass(frozen=True)
class CandidateSetIdentity:
    """Bind a complete candidate family to one card and Preview generation."""

    schema_version: str
    project_card_identity: str
    target_relative_path: str
    baseline_hash: str
    preview_hash: str
    plan_hash: str
    candidate_set_hash: str
    candidate_file_count: int

    def to_dict(self) -> dict[str, str | int]:
        """Return a JSON-ready identity payload."""
        return asdict(self)

    @property
    def identity_hash(self) -> str:
        """Return canonical SHA-256 for this candidate identity."""
        return _canonical_hash(self.to_dict())


@dataclass(frozen=True)
class ExchangeIdentity:
    """Bind one outbound AI exchange to its exact source candidate set."""

    schema_version: str
    exchange_id: str
    project_card_identity: str
    target_relative_path: str
    source_preview_hash: str
    source_candidate_set_hash: str
    candidate_identity_hash: str
    exchange_generation: int

    def to_dict(self) -> dict[str, str | int]:
        """Return a JSON-ready identity payload."""
        return asdict(self)

    @property
    def identity_hash(self) -> str:
        """Return canonical SHA-256 for this exchange identity."""
        return _canonical_hash(self.to_dict())


@dataclass(frozen=True)
class AIResponseIdentity:
    """Describe one AI return package before any candidate import is allowed."""

    schema_version: str
    exchange_id: str
    project_card_identity: str
    target_relative_path: str
    source_preview_hash: str
    source_candidate_set_hash: str
    return_candidate_set_hash: str
    return_schema_version: str

    def to_dict(self) -> dict[str, str]:
        """Return a JSON-ready identity payload."""
        return asdict(self)

    @property
    def identity_hash(self) -> str:
        """Return canonical SHA-256 for the response identity."""
        return _canonical_hash(self.to_dict())


def build_candidate_set_identity(
    *,
    project_card_identity: str,
    target_relative_path: str,
    baseline_hash: str,
    preview_hash: str,
    plan_hash: str,
    candidate_file_hashes: Mapping[str, str],
    schema_version: str = "1.0",
) -> CandidateSetIdentity:
    """Build one immutable identity from the complete candidate family."""
    normalized_files = _normalize_candidate_hashes(candidate_file_hashes)
    if not normalized_files:
        raise ValueError("CANDIDATE_SET_EMPTY")
    candidate_set_hash = _canonical_hash(normalized_files)
    values = {
        "schema_version": schema_version,
        "project_card_identity": project_card_identity,
        "target_relative_path": _normalize_relative_path(target_relative_path),
        "baseline_hash": baseline_hash,
        "preview_hash": preview_hash,
        "plan_hash": plan_hash,
        "candidate_set_hash": candidate_set_hash,
    }
    _require_nonempty(values, "CANDIDATE_SET_IDENTITY_FIELDS_EMPTY")
    return CandidateSetIdentity(
        schema_version=str(schema_version).strip(),
        project_card_identity=str(project_card_identity).strip(),
        target_relative_path=str(values["target_relative_path"]),
        baseline_hash=str(baseline_hash).strip(),
        preview_hash=str(preview_hash).strip(),
        plan_hash=str(plan_hash).strip(),
        candidate_set_hash=candidate_set_hash,
        candidate_file_count=len(normalized_files),
    )


def build_exchange_identity(
    *,
    exchange_id: str,
    candidate_identity: CandidateSetIdentity,
    exchange_generation: int,
    schema_version: str = "1.0",
) -> ExchangeIdentity:
    """Bind one outbound exchange to a complete candidate-set identity."""
    safe_exchange_id = _normalize_identifier(exchange_id, "EXCHANGE_ID_INVALID")
    if int(exchange_generation) < 1:
        raise ValueError("EXCHANGE_GENERATION_INVALID")
    return ExchangeIdentity(
        schema_version=str(schema_version).strip(),
        exchange_id=safe_exchange_id,
        project_card_identity=candidate_identity.project_card_identity,
        target_relative_path=candidate_identity.target_relative_path,
        source_preview_hash=candidate_identity.preview_hash,
        source_candidate_set_hash=candidate_identity.candidate_set_hash,
        candidate_identity_hash=candidate_identity.identity_hash,
        exchange_generation=int(exchange_generation),
    )


def build_ai_response_identity(
    *,
    exchange_identity: ExchangeIdentity,
    return_candidate_set_hash: str,
    return_schema_version: str,
    schema_version: str = "1.0",
) -> AIResponseIdentity:
    """Build one response identity bound to the originating exchange."""
    values = {
        "schema_version": schema_version,
        "exchange_id": exchange_identity.exchange_id,
        "project_card_identity": exchange_identity.project_card_identity,
        "target_relative_path": exchange_identity.target_relative_path,
        "source_preview_hash": exchange_identity.source_preview_hash,
        "source_candidate_set_hash": exchange_identity.source_candidate_set_hash,
        "return_candidate_set_hash": return_candidate_set_hash,
        "return_schema_version": return_schema_version,
    }
    _require_nonempty(values, "AI_RESPONSE_IDENTITY_FIELDS_EMPTY")
    return AIResponseIdentity(
        **{key: str(value).strip() for key, value in values.items()}
    )


def ai_response_identity_blockers(
    exchange_identity: ExchangeIdentity,
    response_identity: AIResponseIdentity,
    *,
    active_project_card_identity: str,
    active_target_relative_path: str,
    active_preview_hash: str,
) -> tuple[str, ...]:
    """Return fail-closed blockers before a returned candidate can be attached."""
    blockers: list[str] = []
    active_target = _normalize_relative_path(active_target_relative_path)
    if response_identity.exchange_id != exchange_identity.exchange_id:
        blockers.append("AI_RESPONSE_EXCHANGE_ID_MISMATCH")
    if response_identity.project_card_identity != exchange_identity.project_card_identity:
        blockers.append("AI_RESPONSE_PROJECT_CARD_MISMATCH")
    if response_identity.target_relative_path != exchange_identity.target_relative_path:
        blockers.append("AI_RESPONSE_TARGET_MISMATCH")
    if response_identity.source_preview_hash != exchange_identity.source_preview_hash:
        blockers.append("AI_RESPONSE_SOURCE_PREVIEW_MISMATCH")
    if (
        response_identity.source_candidate_set_hash
        != exchange_identity.source_candidate_set_hash
    ):
        blockers.append("AI_RESPONSE_SOURCE_CANDIDATE_SET_MISMATCH")
    if response_identity.project_card_identity != str(active_project_card_identity).strip():
        blockers.append("AI_RESPONSE_NOT_FOR_ACTIVE_CARD")
    if response_identity.target_relative_path != active_target:
        blockers.append("AI_RESPONSE_NOT_FOR_ACTIVE_TARGET")
    if response_identity.source_preview_hash != str(active_preview_hash).strip():
        blockers.append("AI_RESPONSE_SOURCE_PREVIEW_STALE")
    if not response_identity.return_candidate_set_hash.strip():
        blockers.append("AI_RESPONSE_RETURN_CANDIDATE_SET_HASH_EMPTY")
    return tuple(sorted(set(blockers)))


def _normalize_candidate_hashes(values: Mapping[str, str]) -> dict[str, str]:
    """Return sorted relative-path hashes and reject ambiguous candidate entries."""
    normalized: dict[str, str] = {}
    for raw_path, raw_hash in values.items():
        path = _normalize_relative_path(raw_path)
        file_hash = str(raw_hash or "").strip()
        if not file_hash:
            raise ValueError("CANDIDATE_FILE_HASH_EMPTY:" + path)
        if path in normalized:
            raise ValueError("CANDIDATE_FILE_PATH_DUPLICATE:" + path)
        normalized[path] = file_hash
    return dict(sorted(normalized.items()))


def _normalize_relative_path(value: str) -> str:
    """Return one safe POSIX relative path for package lineage."""
    text = str(value or "").replace("\\", "/").strip()
    path = PurePosixPath(text)
    if not text or path.is_absolute() or ".." in path.parts:
        raise ValueError("RELATIVE_PATH_INVALID")
    return path.as_posix()


def _normalize_identifier(value: str, marker: str) -> str:
    """Return a filesystem-safe stable identifier without changing ownership."""
    text = str(value or "").strip()
    if not text:
        raise ValueError(marker)
    cleaned = "".join(
        character if character.isalnum() or character in {"-", "_"} else "_"
        for character in text
    ).strip("_-.")
    if not cleaned:
        raise ValueError(marker)
    return cleaned[:96]


def _require_nonempty(values: Mapping[str, object], marker: str) -> None:
    """Reject incomplete lineage identities before package creation or import."""
    missing = [key for key, value in values.items() if not str(value or "").strip()]
    if missing:
        raise ValueError(marker + ":" + ",".join(sorted(missing)))


def _canonical_hash(payload: Mapping[str, object]) -> str:
    """Return canonical SHA-256 for one JSON-serializable payload."""
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
