# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_source_mutation_primitives.py
"""Canonical exact-byte mutation primitives shared by Workbench apply paths."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import ast
import hashlib
import os
from pathlib import Path
from typing import Any, Iterable

from .models import SCHEMA_VERSION
from .workbench_source_payload_builder import SourceApplyPayloadReadinessResult

__all__ = [
    "SOURCE_MUTATION_PRIMITIVES_FEATURE_ID",
    "SourceMutationOperation",
    "build_source_mutation_operations",
    "apply_source_mutation_operation",
    "verify_source_mutation_operation",
    "current_file_hash",
]

SOURCE_MUTATION_PRIMITIVES_FEATURE_ID = (
    "architecture-review-large-file-refactor-source-mutation-primitives-v1"
)
_PROTECTED_PARTS = {
    ".project_reference",
    "_project_reference",
    "project_freeze_after_update",
    "project_error_memory",
    "project_freeze_ledger",
    "show_project_to_AI",
    "_show_project_to_AI",
}


@dataclass(frozen=True)
class SourceMutationOperation:
    """One exact-byte physical operation owned by the canonical apply primitive."""

    schema_version: str
    feature_id: str
    sequence_no: int
    operation_type: str
    relative_path: str
    payload_path: str
    destination_path: str
    payload_hash: str
    precondition_hash: str
    destination_existed: bool
    byte_size: int

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready operation description."""
        return asdict(self)


def build_source_mutation_operations(
    *,
    source_payload: SourceApplyPayloadReadinessResult,
    active_project_root: str | Path,
) -> tuple[tuple[SourceMutationOperation, ...], tuple[str, ...]]:
    """Build deterministic exact-byte operations without mutating project source."""
    root = Path(active_project_root).resolve()
    blockers: list[str] = []
    if source_payload.status != "source_apply_payload_ready":
        blockers.append("SOURCE_APPLY_PAYLOAD_NOT_READY")
    if source_payload.import_rewrite_enabled:
        blockers.append("IMPORT_REWRITE_MUST_REMAIN_DISABLED")
    target = Path(source_payload.target_file).resolve()
    target_dir = target.parent
    seen: set[Path] = set()
    operations: list[SourceMutationOperation] = []
    sorted_files = sorted(
        source_payload.files,
        key=lambda item: str(Path(item.destination_path).resolve()).casefold(),
    )
    for sequence_no, file_record in enumerate(sorted_files, start=1):
        payload_path = Path(file_record.payload_path).resolve()
        destination = Path(file_record.destination_path).resolve()
        if destination in seen:
            blockers.append("DUPLICATE_DESTINATION:" + str(destination))
            continue
        seen.add(destination)
        blockers.extend(
            _destination_blockers(
                destination=destination,
                target_dir=target_dir,
                project_root=root,
            )
        )
        if not payload_path.is_file():
            blockers.append("SOURCE_PAYLOAD_FILE_MISSING:" + str(payload_path))
            continue
        raw = payload_path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != file_record.content_hash:
            blockers.append("SOURCE_PAYLOAD_HASH_MISMATCH:" + str(payload_path))
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            blockers.append("SOURCE_PAYLOAD_NOT_UTF8:" + str(payload_path))
            continue
        if "KANDA PREVIEW ARTIFACT" in text:
            blockers.append("PREVIEW_WATERMARK_IN_SOURCE_PAYLOAD:" + str(payload_path))
        try:
            compile(text, str(destination), "exec")
            ast.parse(text)
        except SyntaxError:
            blockers.append("SOURCE_PAYLOAD_SYNTAX_INVALID:" + str(payload_path))
        existed = destination.is_file()
        precondition_hash = current_file_hash(destination) if existed else ""
        operation_type = "REPLACE_FILE" if existed else "CREATE_FILE"
        operations.append(
            SourceMutationOperation(
                schema_version=SCHEMA_VERSION,
                feature_id=SOURCE_MUTATION_PRIMITIVES_FEATURE_ID,
                sequence_no=sequence_no,
                operation_type=operation_type,
                relative_path=str(file_record.relative_path),
                payload_path=str(payload_path),
                destination_path=str(destination),
                payload_hash=digest,
                precondition_hash=precondition_hash,
                destination_existed=existed,
                byte_size=len(raw),
            )
        )
    if not operations:
        blockers.append("NO_SOURCE_MUTATION_OPERATIONS")
    return tuple(operations), tuple(sorted(set(blockers)))


def apply_source_mutation_operation(
    operation: SourceMutationOperation,
    *,
    operation_id: str,
) -> str:
    """Apply one exact-byte operation after immediate precondition verification."""
    payload_path = Path(operation.payload_path).resolve()
    destination = Path(operation.destination_path).resolve()
    raw = payload_path.read_bytes()
    payload_hash = hashlib.sha256(raw).hexdigest()
    if payload_hash != operation.payload_hash:
        raise RuntimeError("OPERATION_PAYLOAD_HASH_MISMATCH:" + str(destination))
    _verify_precondition(operation, destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp = destination.with_name(
        "." + destination.name + "." + _safe_operation_fragment(operation_id) + ".kanda_tmp"
    )
    if temp.exists():
        temp.unlink()
    try:
        with temp.open("xb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        if current_file_hash(temp) != operation.payload_hash:
            raise RuntimeError("OPERATION_TEMP_HASH_MISMATCH:" + str(destination))
        os.replace(temp, destination)
    finally:
        if temp.exists():
            temp.unlink()
    resulting_hash = current_file_hash(destination)
    if resulting_hash != operation.payload_hash:
        raise RuntimeError("OPERATION_RESULT_HASH_MISMATCH:" + str(destination))
    return resulting_hash


def verify_source_mutation_operation(operation: SourceMutationOperation) -> tuple[bool, str]:
    """Verify one destination matches its exact expected payload hash."""
    destination = Path(operation.destination_path).resolve()
    if not destination.is_file():
        return False, "APPLIED_DESTINATION_MISSING:" + str(destination)
    digest = current_file_hash(destination)
    if digest != operation.payload_hash:
        return False, "APPLIED_DESTINATION_HASH_MISMATCH:" + str(destination)
    return True, ""


def current_file_hash(path: str | Path) -> str:
    """Return SHA-256 for one file, or an empty string when absent."""
    candidate = Path(path)
    if not candidate.is_file():
        return ""
    return hashlib.sha256(candidate.read_bytes()).hexdigest()


def copy_operations_with_payload_root(
    operations: Iterable[SourceMutationOperation],
    *,
    payload_root: str | Path,
) -> tuple[SourceMutationOperation, ...]:
    """Return operations rebound to durable payload copies under payload_root."""
    root = Path(payload_root).resolve()
    rebound: list[SourceMutationOperation] = []
    for operation in operations:
        durable = (root / operation.relative_path).resolve()
        rebound.append(
            SourceMutationOperation(
                **{
                    **operation.__dict__,
                    "payload_path": str(durable),
                }
            )
        )
    return tuple(rebound)


def _verify_precondition(operation: SourceMutationOperation, destination: Path) -> None:
    """Raise when the live destination no longer matches operation preconditions."""
    current = current_file_hash(destination)
    if operation.operation_type == "CREATE_FILE":
        if destination.exists():
            raise RuntimeError("CREATE_DESTINATION_ALREADY_EXISTS:" + str(destination))
        return
    if operation.operation_type == "REPLACE_FILE":
        if not destination.is_file():
            raise RuntimeError("REPLACE_DESTINATION_MISSING:" + str(destination))
        if current != operation.precondition_hash:
            raise RuntimeError("REPLACE_PRECONDITION_HASH_MISMATCH:" + str(destination))
        return
    raise RuntimeError("UNSUPPORTED_MUTATION_OPERATION_TYPE:" + operation.operation_type)


def _destination_blockers(
    *,
    destination: Path,
    target_dir: Path,
    project_root: Path,
) -> list[str]:
    """Return containment blockers for one destination."""
    blockers: list[str] = []
    if not _is_relative_to(destination, project_root):
        blockers.append("DESTINATION_OUTSIDE_PROJECT_ROOT:" + str(destination))
    if destination.parent != target_dir:
        blockers.append("DESTINATION_NOT_IN_TARGET_DIRECTORY:" + str(destination))
    if destination.suffix != ".py":
        blockers.append("DESTINATION_NOT_PYTHON:" + str(destination))
    if _protected_parts(destination):
        blockers.append("DESTINATION_IN_PROTECTED_ROOT:" + str(destination))
    return blockers


def _protected_parts(path: Path) -> tuple[str, ...]:
    """Return protected path components present after resolution."""
    lowered = {part.casefold() for part in path.resolve().parts}
    return tuple(sorted(lowered & {part.casefold() for part in _PROTECTED_PARTS}))


def _safe_operation_fragment(operation_id: str) -> str:
    """Return a filesystem-safe bounded fragment for a temporary filename."""
    digest = hashlib.sha256(operation_id.encode("utf-8")).hexdigest()[:16]
    return digest


def _is_relative_to(path: Path, root: Path) -> bool:
    """Return whether one resolved path is contained by another."""
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False
