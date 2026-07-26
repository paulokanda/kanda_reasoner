# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_sealed_payload.py
"""Exact immutable payload sealing for Preview, Shadow Apply, and later real apply."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path
from typing import Any

from .cst_real_preview_writer import RealPreviewWriteResult
from .models import SCHEMA_VERSION
from .module_size_policy import check_resulting_module_size
from .workbench_execution_contract import WorkbenchExecutionContract
from .workbench_source_payload_builder import SourceApplyPayloadReadinessResult
from .workbench_transformation_recipe import TransformationRecipe

__all__ = [
    "SEALED_PAYLOAD_FEATURE_ID",
    "SealedPayloadFile",
    "WorkbenchSealedPayload",
    "build_and_write_sealed_payload",
    "verify_sealed_payload",
]

SEALED_PAYLOAD_FEATURE_ID = (
    "architecture-review-large-file-refactor-workbench-sealed-exact-payload-v1"
)
_MANIFEST_NAME = "WORKBENCH_SEALED_PAYLOAD.json"


@dataclass(frozen=True)
class SealedPayloadFile:
    """One exact byte artifact covered by the Workbench payload seal."""

    relative_path: str
    payload_path: str
    destination_path: str
    content_hash: str
    byte_size: int
    physical_lines: int
    role: str
    symbols: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["symbols"] = list(self.symbols)
        return data


@dataclass(frozen=True)
class WorkbenchSealedPayload:
    """Immutable artifact manifest that is the only downstream byte truth."""

    schema_version: str
    feature_id: str
    payload_id: str
    contract_hash: str
    recipe_hash: str
    source_content_hash: str
    payload_root: str
    manifest_path: str
    transform_backend: str
    files: tuple[SealedPayloadFile, ...]
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]
    payload_hash: str
    source_mutation_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["files"] = [item.to_dict() for item in self.files]
        data["blockers"] = list(self.blockers)
        data["warnings"] = list(self.warnings)
        return data

    def integrity_valid(self) -> bool:
        valid, _ = verify_sealed_payload(self)
        return valid


def build_and_write_sealed_payload(
    *,
    contract: WorkbenchExecutionContract,
    recipe: TransformationRecipe,
    preview: RealPreviewWriteResult,
    source_payload: SourceApplyPayloadReadinessResult,
) -> WorkbenchSealedPayload:
    """Seal the exact already-generated payload bytes without transforming them again."""
    blockers: list[str] = []
    if not contract.integrity_valid():
        blockers.append("EXECUTION_CONTRACT_HASH_MISMATCH")
    if not recipe.integrity_valid():
        blockers.append("TRANSFORMATION_RECIPE_HASH_MISMATCH")
    if recipe.contract_hash != contract.contract_hash:
        blockers.append("RECIPE_CONTRACT_HASH_MISMATCH")
    if source_payload.status != "source_apply_payload_ready":
        blockers.append("SOURCE_PAYLOAD_NOT_READY")
    if source_payload.source_mutation_enabled or source_payload.apply_enabled:
        blockers.append("SOURCE_PAYLOAD_MUTATION_AUTHORITY_PRESENT")
    if preview.extraction_backend != "libcst_position_provider":
        blockers.append("LIBCST_EXTRACTION_BACKEND_REQUIRED")
    fidelity_backend = str(preview.cst_transform_fidelity.get("transform_backend", ""))
    if fidelity_backend != "libcst_transform_partition":
        blockers.append("LIBCST_TRANSFORM_FIDELITY_REQUIRED")

    payload_root = Path(source_payload.payload_root).resolve()
    manifest_path = payload_root / _MANIFEST_NAME
    files: list[SealedPayloadFile] = []
    preview_by_name = {item.relative_path: item for item in preview.files}
    expected_destinations = {str(Path(path).resolve()) for path in contract.exact_target_files}

    for item in source_payload.files:
        payload_path = Path(item.payload_path).resolve()
        destination = str(Path(item.destination_path).resolve())
        preview_item = preview_by_name.get(item.relative_path)
        if preview_item is None:
            blockers.append(f"SEALED_FILE_MISSING_PREVIEW_RECORD:{item.relative_path}")
            continue
        if not payload_path.is_file():
            blockers.append(f"SEALED_PAYLOAD_FILE_MISSING:{item.relative_path}")
            continue
        raw = payload_path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != item.content_hash:
            blockers.append(f"SEALED_PAYLOAD_HASH_MISMATCH:{item.relative_path}")
        text = raw.decode("utf-8")
        size = check_resulting_module_size(text, relative_path=item.relative_path)
        blockers.extend(size.blockers)
        if destination not in expected_destinations:
            blockers.append(f"SEALED_DESTINATION_NOT_IN_CONTRACT:{item.relative_path}")
        files.append(
            SealedPayloadFile(
                relative_path=item.relative_path,
                payload_path=str(payload_path),
                destination_path=destination,
                content_hash=digest,
                byte_size=len(raw),
                physical_lines=len(text.splitlines()),
                role=item.role,
                symbols=tuple(item.symbols),
            )
        )

    sealed_destinations = {item.destination_path for item in files}
    missing_destinations = expected_destinations - sealed_destinations
    for path in sorted(missing_destinations, key=str.casefold):
        blockers.append(f"CONTRACT_DESTINATION_MISSING_FROM_SEAL:{path}")

    unique_blockers = tuple(sorted(set(blockers)))
    file_fingerprint = "|".join(
        f"{item.relative_path}:{item.content_hash}:{item.destination_path}"
        for item in sorted(files, key=lambda record: record.relative_path.casefold())
    )
    payload_id = "payload-" + hashlib.sha256(
        f"{contract.contract_hash}|{recipe.recipe_hash}|{file_fingerprint}".encode("utf-8")
    ).hexdigest()[:20]
    provisional = WorkbenchSealedPayload(
        schema_version=SCHEMA_VERSION,
        feature_id=SEALED_PAYLOAD_FEATURE_ID,
        payload_id=payload_id,
        contract_hash=contract.contract_hash,
        recipe_hash=recipe.recipe_hash,
        source_content_hash=recipe.source_content_hash,
        payload_root=str(payload_root),
        manifest_path=str(manifest_path),
        transform_backend="libcst_position_extraction_and_deterministic_render",
        files=tuple(sorted(files, key=lambda record: record.relative_path.casefold())),
        blockers=unique_blockers,
        warnings=(
            "SEALED_PAYLOAD_BYTES_ARE_DOWNSTREAM_EXECUTION_TRUTH",
            "NO_FORMATTER_LINTER_OR_AI_MUTATION_ALLOWED_AFTER_SEAL",
            "SOURCE_MUTATION_REMAINS_DISABLED",
        ),
        payload_hash="",
        source_mutation_enabled=False,
    )
    sealed = WorkbenchSealedPayload(
        **{**provisional.__dict__, "payload_hash": _payload_hash(provisional)}
    )
    payload_root.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(sealed.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return sealed


def verify_sealed_payload(payload: WorkbenchSealedPayload) -> tuple[bool, tuple[str, ...]]:
    """Re-read every sealed artifact and prove exact hash and manifest integrity."""
    blockers: list[str] = list(payload.blockers)
    if not payload.payload_hash or payload.payload_hash != _payload_hash(payload):
        blockers.append("SEALED_PAYLOAD_MANIFEST_HASH_MISMATCH")
    for item in payload.files:
        path = Path(item.payload_path).resolve()
        if not path.is_file():
            blockers.append(f"SEALED_PAYLOAD_FILE_MISSING:{item.relative_path}")
            continue
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != item.content_hash:
            blockers.append(f"SEALED_PAYLOAD_FILE_HASH_CHANGED:{item.relative_path}")
        if len(raw) != item.byte_size:
            blockers.append(f"SEALED_PAYLOAD_FILE_SIZE_CHANGED:{item.relative_path}")
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            blockers.append(f"SEALED_PAYLOAD_NOT_UTF8:{item.relative_path}")
            continue
        if len(text.splitlines()) != item.physical_lines:
            blockers.append(f"SEALED_PAYLOAD_LINE_COUNT_CHANGED:{item.relative_path}")
        blockers.extend(check_resulting_module_size(text, relative_path=item.relative_path).blockers)
    unique = tuple(sorted(set(blockers)))
    return not unique, unique


def _payload_hash(payload: WorkbenchSealedPayload) -> str:
    body = {
        "schema_version": payload.schema_version,
        "feature_id": payload.feature_id,
        "payload_id": payload.payload_id,
        "contract_hash": payload.contract_hash,
        "recipe_hash": payload.recipe_hash,
        "source_content_hash": payload.source_content_hash,
        "payload_root": payload.payload_root,
        "transform_backend": payload.transform_backend,
        "files": [item.to_dict() for item in payload.files],
        "blockers": list(payload.blockers),
        "warnings": list(payload.warnings),
        "source_mutation_enabled": payload.source_mutation_enabled,
    }
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
