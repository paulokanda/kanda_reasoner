"""Validate and persist optional external AI return candidate generations."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
from typing import Any
import zipfile

from .external_ai_candidate_exchange_contract import (
    AIResponseIdentity,
    ai_response_identity_blockers,
    build_ai_response_identity,
    build_candidate_set_identity,
)
from .workbench_project_support_paths import exchange_root_blockers

__all__ = [
    "EXTERNAL_AI_RETURN_OPTIONAL_IMPORT_FEATURE_ID",
    "ExternalAIReturnGenerationResult",
    "ai_return_import_readiness_blockers",
    "build_optional_ai_return_instructions",
    "import_external_ai_candidate_answer",
]

EXTERNAL_AI_RETURN_OPTIONAL_IMPORT_FEATURE_ID = (
    "external-ai-return-contract-optional-candidate-import-v1"
)
_RETURN_SCHEMA_VERSION = "1.0"
_MANIFEST_NAME = "AI_RETURN_MANIFEST.json"
_IDENTITY_NAME = "lineage/AI_RESPONSE_IDENTITY.json"
_CANDIDATE_PREFIX = "candidate_family/"
_MAX_ARCHIVE_ENTRIES = 512
_MAX_MEMBER_BYTES = 64 * 1024 * 1024
_MAX_TOTAL_BYTES = 256 * 1024 * 1024


@dataclass(frozen=True)
class ExternalAIReturnGenerationResult:
    """Describe one validated return package persisted as a new candidate generation."""

    feature_id: str
    exchange_id: str
    return_id: str
    return_root: str
    manifest_path: str
    receipt_path: str
    response_identity: AIResponseIdentity
    candidate_files: tuple[str, ...]
    candidate_set_hash: str
    source_zip_sha256: str


def ai_return_import_readiness_blockers(
    *,
    exchange_result: Any,
    aqr_context: Any,
) -> tuple[str, ...]:
    """Return blockers for exposing optional Import AI Answer controls."""
    blockers: list[str] = []
    if exchange_result is None:
        blockers.append("AI_RETURN_ACTIVE_EXCHANGE_MISSING")
        return tuple(blockers)
    exchange_root = Path(str(getattr(exchange_result, "exchange_root", "") or ""))
    if not exchange_root.is_dir():
        blockers.append("AI_RETURN_ACTIVE_EXCHANGE_ROOT_MISSING")
    candidate_files = tuple(getattr(exchange_result, "candidate_files", ()) or ())
    if not candidate_files:
        blockers.append("AI_RETURN_ACTIVE_CANDIDATE_FAMILY_EMPTY")
    if aqr_context is None or getattr(aqr_context, "request", None) is None:
        blockers.append("AI_RETURN_ACTIVE_AQR_CONTEXT_MISSING")
        return tuple(blockers)
    identity = getattr(aqr_context.request, "analysis_identity", None)
    exchange_identity = getattr(exchange_result, "exchange_identity", None)
    if identity is None or exchange_identity is None:
        blockers.append("AI_RETURN_ACTIVE_LINEAGE_MISSING")
        return tuple(blockers)
    if exchange_identity.project_card_identity != identity.project_card_identity:
        blockers.append("AI_RETURN_ACTIVE_CARD_MISMATCH")
    if exchange_identity.target_relative_path != identity.target_relative_path:
        blockers.append("AI_RETURN_ACTIVE_TARGET_MISMATCH")
    if exchange_identity.source_preview_hash != identity.preview_hash:
        blockers.append("AI_RETURN_ACTIVE_PREVIEW_STALE")
    return tuple(sorted(set(blockers)))


def build_optional_ai_return_instructions(exchange_result: Any) -> str:
    """Return optional advanced import instructions while preserving patch ZIP default."""
    exchange = exchange_result.exchange_identity
    candidates = tuple(sorted(str(item) for item in exchange_result.candidate_files))
    candidate_lines = "\n".join("- " + item for item in candidates)
    return "\n".join(
        [
            "",
            "## Optional advanced AI return package",
            "",
            "The default and preferred return route remains one complete cumulative ",
            "governed KANDA patch ZIP. Use this optional return contract only when the ",
            "human explicitly chooses Import AI Answer in the Workbench.",
            "",
            "An optional importable answer ZIP must contain only:",
            "- AI_RETURN_MANIFEST.json",
            "- lineage/AI_RESPONSE_IDENTITY.json",
            "- candidate_family/<the complete original candidate family>",
            "",
            "The imported answer becomes a new Project Support candidate generation. ",
            "It does not replace Preview, write canonical Project source, prepare a ",
            "transaction, acknowledge warnings, or confirm human review.",
            "",
            "Required source lineage:",
            "exchange_id: " + exchange.exchange_id,
            "project_card_identity: " + exchange.project_card_identity,
            "target_relative_path: " + exchange.target_relative_path,
            "source_preview_hash: " + exchange.source_preview_hash,
            "source_candidate_set_hash: " + exchange.source_candidate_set_hash,
            "source_exchange_identity_hash: " + exchange.identity_hash,
            "",
            "Required candidate paths:",
            candidate_lines,
            "",
            "The return manifest must declare return_kind=candidate_generation, ",
            "schema_version=1.0, return_schema_version=1.0, the source exchange ",
            "identity hash, the response identity hash, and exact SHA-256/size entries ",
            "for every returned candidate file.",
        ]
    )


def import_external_ai_candidate_answer(
    *,
    active_project_root: str | Path,
    exchange_result: Any,
    answer_zip_path: str | Path,
    active_project_card_identity: str,
    active_target_relative_path: str,
    active_preview_hash: str,
) -> ExternalAIReturnGenerationResult:
    """Validate one optional AI answer ZIP and persist a new candidate generation."""
    project_root = Path(active_project_root).expanduser().resolve(strict=True)
    source_zip = Path(answer_zip_path).expanduser().resolve(strict=True)
    if not source_zip.is_file() or source_zip.suffix.lower() != ".zip":
        raise ValueError("AI_RETURN_ZIP_INVALID")

    exchange_root = Path(exchange_result.exchange_root).expanduser().resolve(strict=False)
    blockers = exchange_root_blockers(project_root, exchange_root)
    if blockers:
        raise ValueError("AI_RETURN_EXCHANGE_OWNERSHIP_BLOCKED:" + "|".join(blockers))
    exchange_identity = exchange_result.exchange_identity
    if exchange_root.name != exchange_identity.exchange_id:
        raise ValueError("AI_RETURN_EXCHANGE_ROOT_ID_MISMATCH")

    expected_candidates = tuple(sorted(str(item) for item in exchange_result.candidate_files))
    if not expected_candidates:
        raise ValueError("AI_RETURN_EXPECTED_CANDIDATE_FAMILY_EMPTY")

    with zipfile.ZipFile(source_zip, "r") as archive:
        members = _validated_archive_members(archive, expected_candidates)
        manifest = _load_json_member(archive, _MANIFEST_NAME)
        supplied_identity = _load_response_identity(archive)
        candidate_bytes, candidate_hashes = _load_candidate_family(
            archive,
            expected_candidates,
        )

    return_identity = build_candidate_set_identity(
        project_card_identity=exchange_result.candidate_identity.project_card_identity,
        target_relative_path=exchange_result.candidate_identity.target_relative_path,
        baseline_hash=exchange_result.candidate_identity.baseline_hash,
        preview_hash=exchange_result.candidate_identity.preview_hash,
        plan_hash=exchange_result.candidate_identity.plan_hash,
        candidate_file_hashes=candidate_hashes,
    )
    expected_response = build_ai_response_identity(
        exchange_identity=exchange_identity,
        return_candidate_set_hash=return_identity.candidate_set_hash,
        return_schema_version=_RETURN_SCHEMA_VERSION,
    )
    _validate_manifest(
        manifest=manifest,
        members=members,
        expected_candidates=expected_candidates,
        candidate_bytes=candidate_bytes,
        candidate_hashes=candidate_hashes,
        exchange_identity_hash=exchange_identity.identity_hash,
        expected_response=expected_response,
    )
    if supplied_identity != expected_response:
        raise ValueError("AI_RETURN_RESPONSE_IDENTITY_MISMATCH")
    blockers = ai_response_identity_blockers(
        exchange_identity,
        supplied_identity,
        active_project_card_identity=active_project_card_identity,
        active_target_relative_path=active_target_relative_path,
        active_preview_hash=active_preview_hash,
    )
    if blockers:
        raise ValueError("AI_RETURN_LINEAGE_BLOCKED:" + "|".join(blockers))

    returns_root = exchange_root / "returns"
    blockers = exchange_root_blockers(project_root, returns_root)
    if blockers:
        raise ValueError("AI_RETURN_ROOT_OWNERSHIP_BLOCKED:" + "|".join(blockers))
    returns_root.mkdir(parents=True, exist_ok=True)
    generation = _next_return_generation(returns_root)
    return_id = f"RETURN-{generation:04d}"
    return_root = returns_root / return_id
    if return_root.exists():
        raise FileExistsError("AI_RETURN_GENERATION_ALREADY_EXISTS:" + return_id)
    return_root.mkdir(parents=True, exist_ok=False)

    try:
        for relative, data in sorted(candidate_bytes.items()):
            destination = return_root / _CANDIDATE_PREFIX / _safe_relative(relative)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
        identity_path = return_root / _IDENTITY_NAME
        _write_json(identity_path, expected_response.to_dict())
        manifest_path = return_root / _MANIFEST_NAME
        _write_json(manifest_path, manifest)
        receipt_path = return_root / "IMPORT_RECEIPT.json"
        receipt = {
            "schema_version": _RETURN_SCHEMA_VERSION,
            "feature_id": EXTERNAL_AI_RETURN_OPTIONAL_IMPORT_FEATURE_ID,
            "exchange_id": exchange_identity.exchange_id,
            "return_id": return_id,
            "response_identity_hash": expected_response.identity_hash,
            "return_candidate_set_hash": return_identity.candidate_set_hash,
            "source_zip_sha256": _hash_file(source_zip),
            "candidate_file_count": len(expected_candidates),
            "import_mode": "new_candidate_generation_only",
            "canonical_source_mutated": False,
            "preview_replaced": False,
            "transaction_prepared": False,
            "human_authorization_changed": False,
        }
        _write_json(receipt_path, receipt)
    except Exception:
        shutil.rmtree(return_root, ignore_errors=True)
        raise

    return ExternalAIReturnGenerationResult(
        feature_id=EXTERNAL_AI_RETURN_OPTIONAL_IMPORT_FEATURE_ID,
        exchange_id=exchange_identity.exchange_id,
        return_id=return_id,
        return_root=str(return_root),
        manifest_path=str(manifest_path),
        receipt_path=str(receipt_path),
        response_identity=expected_response,
        candidate_files=expected_candidates,
        candidate_set_hash=return_identity.candidate_set_hash,
        source_zip_sha256=_hash_file(source_zip),
    )


def _validated_archive_members(
    archive: zipfile.ZipFile,
    expected_candidates: tuple[str, ...],
) -> tuple[str, ...]:
    infos = archive.infolist()
    if not infos or len(infos) > _MAX_ARCHIVE_ENTRIES:
        raise ValueError("AI_RETURN_ARCHIVE_ENTRY_COUNT_INVALID")
    names: list[str] = []
    total_size = 0
    for info in infos:
        if info.is_dir():
            continue
        if info.flag_bits & 0x1:
            raise ValueError("AI_RETURN_ENCRYPTED_MEMBER_FORBIDDEN")
        if _zipinfo_is_symlink(info):
            raise ValueError("AI_RETURN_SYMLINK_MEMBER_FORBIDDEN")
        name = _safe_archive_name(info.filename)
        if name in names:
            raise ValueError("AI_RETURN_DUPLICATE_ARCHIVE_MEMBER:" + name)
        if info.file_size > _MAX_MEMBER_BYTES:
            raise ValueError("AI_RETURN_MEMBER_TOO_LARGE:" + name)
        total_size += info.file_size
        if total_size > _MAX_TOTAL_BYTES:
            raise ValueError("AI_RETURN_ARCHIVE_TOO_LARGE")
        names.append(name)
    expected = {_MANIFEST_NAME, _IDENTITY_NAME}
    expected.update(_CANDIDATE_PREFIX + item for item in expected_candidates)
    if set(names) != expected:
        missing = sorted(expected.difference(names))
        extra = sorted(set(names).difference(expected))
        raise ValueError(
            "AI_RETURN_ARCHIVE_CONTENT_MISMATCH:missing="
            + ",".join(missing)
            + ";extra="
            + ",".join(extra)
        )
    return tuple(sorted(names))


def _load_candidate_family(
    archive: zipfile.ZipFile,
    expected_candidates: tuple[str, ...],
) -> tuple[dict[str, bytes], dict[str, str]]:
    payloads: dict[str, bytes] = {}
    hashes: dict[str, str] = {}
    for relative in expected_candidates:
        name = _CANDIDATE_PREFIX + relative
        data = archive.read(name)
        payloads[relative] = data
        hashes[relative] = hashlib.sha256(data).hexdigest()
    return payloads, hashes


def _load_response_identity(archive: zipfile.ZipFile) -> AIResponseIdentity:
    payload = _load_json_member(archive, _IDENTITY_NAME)
    required = {
        "schema_version",
        "exchange_id",
        "project_card_identity",
        "target_relative_path",
        "source_preview_hash",
        "source_candidate_set_hash",
        "return_candidate_set_hash",
        "return_schema_version",
    }
    if set(payload) != required:
        raise ValueError("AI_RETURN_IDENTITY_SCHEMA_INVALID")
    return AIResponseIdentity(**{key: str(payload[key]) for key in sorted(required)})


def _validate_manifest(
    *,
    manifest: dict[str, Any],
    members: tuple[str, ...],
    expected_candidates: tuple[str, ...],
    candidate_bytes: dict[str, bytes],
    candidate_hashes: dict[str, str],
    exchange_identity_hash: str,
    expected_response: AIResponseIdentity,
) -> None:
    required = {
        "schema_version",
        "return_schema_version",
        "return_kind",
        "exchange_id",
        "source_exchange_identity_hash",
        "response_identity_hash",
        "candidate_files",
    }
    if set(manifest) != required:
        raise ValueError("AI_RETURN_MANIFEST_SCHEMA_INVALID")
    if manifest["schema_version"] != _RETURN_SCHEMA_VERSION:
        raise ValueError("AI_RETURN_MANIFEST_SCHEMA_VERSION_UNSUPPORTED")
    if manifest["return_schema_version"] != _RETURN_SCHEMA_VERSION:
        raise ValueError("AI_RETURN_SCHEMA_VERSION_UNSUPPORTED")
    if manifest["return_kind"] != "candidate_generation":
        raise ValueError("AI_RETURN_KIND_INVALID")
    if manifest["exchange_id"] != expected_response.exchange_id:
        raise ValueError("AI_RETURN_MANIFEST_EXCHANGE_MISMATCH")
    if manifest["source_exchange_identity_hash"] != exchange_identity_hash:
        raise ValueError("AI_RETURN_SOURCE_EXCHANGE_IDENTITY_HASH_MISMATCH")
    if manifest["response_identity_hash"] != expected_response.identity_hash:
        raise ValueError("AI_RETURN_RESPONSE_IDENTITY_HASH_MISMATCH")
    entries = manifest["candidate_files"]
    if not isinstance(entries, list) or len(entries) != len(expected_candidates):
        raise ValueError("AI_RETURN_MANIFEST_CANDIDATE_LIST_INVALID")
    observed: dict[str, tuple[str, int]] = {}
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {
            "relative_path",
            "sha256",
            "size_bytes",
        }:
            raise ValueError("AI_RETURN_MANIFEST_CANDIDATE_ENTRY_INVALID")
        relative = _safe_relative(str(entry["relative_path"])).as_posix()
        if relative in observed:
            raise ValueError("AI_RETURN_MANIFEST_CANDIDATE_DUPLICATE:" + relative)
        observed[relative] = (str(entry["sha256"]), int(entry["size_bytes"]))
    if tuple(sorted(observed)) != expected_candidates:
        raise ValueError("AI_RETURN_MANIFEST_CANDIDATE_PATHS_MISMATCH")
    for relative in expected_candidates:
        expected = (candidate_hashes[relative], len(candidate_bytes[relative]))
        if observed[relative] != expected:
            raise ValueError("AI_RETURN_MANIFEST_CANDIDATE_HASH_OR_SIZE_MISMATCH:" + relative)
    if len(members) != len(expected_candidates) + 2:
        raise ValueError("AI_RETURN_MANIFEST_MEMBER_COUNT_MISMATCH")


def _load_json_member(archive: zipfile.ZipFile, name: str) -> dict[str, Any]:
    try:
        data = archive.read(name)
    except KeyError as error:
        raise ValueError("AI_RETURN_REQUIRED_MEMBER_MISSING:" + name) from error
    try:
        payload = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("AI_RETURN_JSON_INVALID:" + name) from error
    if not isinstance(payload, dict):
        raise ValueError("AI_RETURN_JSON_OBJECT_REQUIRED:" + name)
    return payload


def _next_return_generation(returns_root: Path) -> int:
    generations: list[int] = []
    for path in returns_root.iterdir():
        if not path.is_dir() or not path.name.startswith("RETURN-"):
            continue
        suffix = path.name[7:]
        if suffix.isdigit():
            generations.append(int(suffix))
    return max(generations, default=0) + 1


def _safe_archive_name(value: str) -> str:
    text = str(value or "").replace("\\", "/").strip("/")
    path = PurePosixPath(text)
    if not text or path.is_absolute() or ".." in path.parts:
        raise ValueError("AI_RETURN_ARCHIVE_PATH_INVALID")
    if ":" in path.parts[0]:
        raise ValueError("AI_RETURN_ARCHIVE_DRIVE_PATH_FORBIDDEN")
    return path.as_posix()


def _safe_relative(value: str) -> Path:
    text = str(value or "").replace("\\", "/").strip()
    path = PurePosixPath(text)
    if not text or path.is_absolute() or ".." in path.parts:
        raise ValueError("AI_RETURN_RELATIVE_PATH_INVALID")
    return Path(*path.parts)


def _zipinfo_is_symlink(info: zipfile.ZipInfo) -> bool:
    mode = (info.external_attr >> 16) & 0o170000
    return mode == 0o120000


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    path.write_text(text, encoding="utf-8", newline="\n")


def _hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
