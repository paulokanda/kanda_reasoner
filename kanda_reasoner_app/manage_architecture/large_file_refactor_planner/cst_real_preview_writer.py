# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/cst_real_preview_writer.py
"""Real moved-code preview writer for the Workbench, preview-only."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
from pathlib import Path
from typing import Any

from .cst_docstring_inserter import (
    DocstringInsertionResult,
    insert_missing_docstrings_for_preview_blocks,
)
from .cst_facade_global_import_inserter import (
    FacadeGlobalImportInsertionReport,
    insert_facade_global_dependency_imports,
)
from .cst_preview_rendering import render_preview_facade, render_preview_helper
from .facade_consumer_compatibility import (
    FacadeConsumerCompatibilityReport,
    build_facade_consumer_compatibility_report,
)
from .helper_import_synthesizer import (
    HelperImportSynthesisReport,
    synthesize_helper_imports,
)
from .cst_symbol_source_extractor import (
    SourceExtractionResult,
    extract_source_blocks,
    libcst_available as is_libcst_available,
)
from .cst_transform_fidelity import (
    CstTransformFidelityReport,
    build_cst_transform_fidelity_report,
)
from .models import SCHEMA_VERSION, RefactorPlan
from .preview_writer import resolve_preview_root
from .workbench_project_support_paths import preview_root_blockers
from .workbench_dependency_readiness import WorkbenchDependencyReadinessResult
from .workbench_plan_intake import WorkbenchPlanIntakeResult

__all__ = [
    "REAL_PREVIEW_FEATURE_ID",
    "RealPreviewFile",
    "RealPreviewWriteResult",
    "build_and_write_real_preview",
]

REAL_PREVIEW_FEATURE_ID = "architecture-review-large-file-refactor-real-preview-v1"
_PROTECTED_PARTS = {
    ".project_reference",
    "_project_reference",
    "project_freeze_after_update",
    "project_error_memory",
    "project_freeze_ledger",
    "show_project_to_ai",
    "_show_project_to_ai",
}


@dataclass(frozen=True)
class RealPreviewFile:
    """One generated real moved-code preview file."""

    relative_path: str
    role: str
    symbols: list[str]
    content_hash: str
    physical_lines: int

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready file record."""
        return asdict(self)


@dataclass(frozen=True)
class RealPreviewWriteResult:
    """Preview-only real moved-code generation result."""

    schema_version: str
    feature_id: str
    status: str
    target_file: str
    source_content_hash: str
    preview_root: str
    libcst_available: bool
    extraction_backend: str = "ast_source_span_fallback"
    docstring_insertion_enabled: bool = True
    docstring_insertions: list[dict[str, str]] = field(default_factory=list)
    helper_import_synthesis_enabled: bool = True
    helper_import_synthesis: dict[str, Any] = field(default_factory=dict)
    facade_global_import_insertion: dict[str, Any] = field(default_factory=dict)
    facade_consumer_compatibility: dict[str, Any] = field(default_factory=dict)
    cst_transform_fidelity_enabled: bool = True
    cst_transform_fidelity: dict[str, Any] = field(default_factory=dict)
    files: list[RealPreviewFile] = field(default_factory=list)
    written_files: list[str] = field(default_factory=list)
    source_mutation_enabled: bool = False
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready preview result."""
        data = asdict(self)
        data["files"] = [item.to_dict() for item in self.files]
        return data


def build_and_write_real_preview(
    *,
    plan: RefactorPlan | None,
    intake: WorkbenchPlanIntakeResult | None,
    dependency_readiness: WorkbenchDependencyReadinessResult | None,
    active_project_root: str,
    preview_root: str = "",
) -> RealPreviewWriteResult:
    """Generate moved-code Preview files under selected project support only."""
    blockers = _entry_blockers(plan, intake, dependency_readiness)
    if plan is None or intake is None:
        return _blocked("", "", preview_root, blockers)
    target = Path(plan.target_file).resolve()
    current_hash = _hash_file(target)
    if current_hash != plan.source_content_hash:
        blockers.append("STALE_SOURCE")
    root = Path(active_project_root).resolve()
    final_preview_root = preview_root or resolve_preview_root(str(root))
    blockers.extend(_preview_root_blockers(root, final_preview_root))
    if blockers:
        return _blocked(str(target), plan.source_content_hash, final_preview_root, blockers)
    consumer_compatibility = build_facade_consumer_compatibility_report(
        active_project_root=root,
        target_file=target,
        moved_symbols=_helper_symbol_map(plan),
    )
    if consumer_compatibility.blockers:
        return _blocked(
            str(target),
            plan.source_content_hash,
            final_preview_root,
            list(consumer_compatibility.blockers),
            warnings=list(consumer_compatibility.warnings),
            facade_consumer_compatibility=consumer_compatibility,
        )
    generated, extraction, docstrings, facade_globals, helper_imports, fidelity = _generate_files(
        plan,
        target,
        dependency_readiness,
        set(consumer_compatibility.imported_moved_symbols),
    )
    if extraction.blockers or docstrings.blockers or facade_globals.blockers or fidelity.blockers:
        return _blocked(
            str(target),
            plan.source_content_hash,
            final_preview_root,
            [
                *extraction.blockers,
                *docstrings.blockers,
                *facade_globals.blockers,
                *fidelity.blockers,
            ],
            extraction_backend=extraction.extraction_backend,
            warnings=[
                *extraction.warnings,
                *docstrings.warnings,
                *facade_globals.warnings,
                *consumer_compatibility.warnings,
                *fidelity.warnings,
            ],
            facade_consumer_compatibility=consumer_compatibility,
        )
    write_blockers = _write_files(Path(final_preview_root).resolve(), generated, root)
    if write_blockers:
        return _blocked(
            str(target),
            plan.source_content_hash,
            final_preview_root,
            write_blockers,
            extraction_backend=extraction.extraction_backend,
            warnings=[
                *extraction.warnings,
                *consumer_compatibility.warnings,
            ],
            facade_consumer_compatibility=consumer_compatibility,
        )
    manifest = Path(final_preview_root).resolve() / "REAL_PREVIEW_MANIFEST.json"
    result = RealPreviewWriteResult(
        schema_version=SCHEMA_VERSION,
        feature_id=REAL_PREVIEW_FEATURE_ID,
        status="real_preview_written",
        target_file=str(target),
        source_content_hash=plan.source_content_hash,
        preview_root=str(Path(final_preview_root).resolve()),
        libcst_available=is_libcst_available(),
        extraction_backend=extraction.extraction_backend,
        docstring_insertion_enabled=True,
        docstring_insertions=[item.to_dict() for item in docstrings.insertions],
        helper_import_synthesis_enabled=True,
        helper_import_synthesis=helper_imports.to_dict(),
        facade_global_import_insertion=facade_globals.to_dict(),
        facade_consumer_compatibility=consumer_compatibility.to_dict(),
        cst_transform_fidelity_enabled=True,
        cst_transform_fidelity=fidelity.to_dict(),
        files=generated,
        written_files=[str(Path(final_preview_root).resolve() / item.relative_path) for item in generated],
        warnings=_stable_warnings(
            extraction,
            [
                *docstrings.warnings,
                *facade_globals.warnings,
                *consumer_compatibility.warnings,
                *helper_imports.warnings,
                *fidelity.warnings,
            ],
        ),
    )
    manifest.write_text(json.dumps(result.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    return RealPreviewWriteResult(
        schema_version=result.schema_version,
        feature_id=result.feature_id,
        status=result.status,
        target_file=result.target_file,
        source_content_hash=result.source_content_hash,
        preview_root=result.preview_root,
        libcst_available=result.libcst_available,
        extraction_backend=result.extraction_backend,
        docstring_insertion_enabled=result.docstring_insertion_enabled,
        docstring_insertions=list(result.docstring_insertions),
        helper_import_synthesis_enabled=result.helper_import_synthesis_enabled,
        helper_import_synthesis=dict(result.helper_import_synthesis),
        facade_global_import_insertion=dict(result.facade_global_import_insertion),
        facade_consumer_compatibility=dict(result.facade_consumer_compatibility),
        cst_transform_fidelity_enabled=result.cst_transform_fidelity_enabled,
        cst_transform_fidelity=dict(result.cst_transform_fidelity),
        files=list(result.files),
        written_files=[*result.written_files, str(manifest)],
        source_mutation_enabled=False,
        blockers=list(result.blockers),
        warnings=list(result.warnings),
    )


def _generate_files(
    plan: RefactorPlan,
    target: Path,
    dependency_readiness: WorkbenchDependencyReadinessResult | None,
    compatibility_import_names: set[str],
) -> tuple[
    list[RealPreviewFile],
    SourceExtractionResult,
    DocstringInsertionResult,
    FacadeGlobalImportInsertionReport,
    HelperImportSynthesisReport,
    CstTransformFidelityReport,
]:
    """Render facade and helpers from extracted top-level source blocks."""
    helper_for_symbol = _helper_symbol_map(plan)
    source_text = target.read_text(encoding="utf-8", errors="replace")
    extraction = extract_source_blocks(target, set(helper_for_symbol))
    fidelity = build_cst_transform_fidelity_report(source_text, set(helper_for_symbol))
    docstrings = insert_missing_docstrings_for_preview_blocks(extraction.symbol_blocks)
    facade_globals = insert_facade_global_dependency_imports(
        plan=plan,
        readiness=dependency_readiness,
        blocks=docstrings.blocks,
    )
    symbol_blocks = facade_globals.blocks
    helper_imports = synthesize_helper_imports(
        plan=plan,
        readiness=dependency_readiness,
        import_blocks=extraction.import_blocks,
    )
    files: list[RealPreviewFile] = []
    for module in plan.proposed_modules:
        if module.role == "public_facade":
            content = render_preview_facade(
                plan,
                module.filename,
                extraction.import_blocks,
                extraction.retained_facade_blocks,
                helper_for_symbol,
                extraction.extraction_backend,
                compatibility_import_names=compatibility_import_names,
            )
        else:
            content = render_preview_helper(
                plan,
                module.filename,
                module.role,
                module.symbols,
                helper_imports.imports_for_module(module.filename),
                symbol_blocks,
                extraction.extraction_backend,
            )
        files.append(_preview_file(module.filename, module.role, module.symbols, content))
        _cache_content(module.filename, content)
    return files, extraction, docstrings, facade_globals, helper_imports, fidelity


def _helper_symbol_map(plan: RefactorPlan) -> dict[str, str]:
    """Return symbol-to-helper mapping for non-facade modules."""
    mapping: dict[str, str] = {}
    for module in plan.proposed_modules:
        if module.role == "public_facade":
            continue
        for symbol in module.symbols:
            mapping[symbol] = module.filename
    return mapping


def _preview_file(filename: str, role: str, symbols: list[str], content: str) -> RealPreviewFile:
    """Build a preview file record and cache its content for writing."""
    return RealPreviewFile(
        relative_path=filename,
        role=role,
        symbols=list(symbols),
        content_hash=hashlib.sha256(content.encode("utf-8")).hexdigest(),
        physical_lines=len(content.splitlines()),
    )


_CONTENT_CACHE: dict[str, str] = {}


def _cache_content(filename: str, content: str) -> None:
    """Store rendered preview text until write step."""
    _CONTENT_CACHE[filename] = content


def _write_files(preview_root: Path, files: list[RealPreviewFile], project_root: Path) -> list[str]:
    """Write preview files after no-leak destination checks."""
    blockers: list[str] = []
    preview_root.mkdir(parents=True, exist_ok=True)
    for item in files:
        try:
            target = preview_root / _safe_relative(item.relative_path)
        except ValueError as exc:
            blockers.append(str(exc))
            continue
        blockers.extend(_destination_blockers(target, preview_root, project_root))
        if blockers:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(_CONTENT_CACHE[item.relative_path].encode("utf-8"))
    return sorted(set(blockers))


def _entry_blockers(
    plan: RefactorPlan | None,
    intake: WorkbenchPlanIntakeResult | None,
    readiness: WorkbenchDependencyReadinessResult | None,
) -> list[str]:
    """Return high-level blockers before preview generation."""
    blockers: list[str] = []
    if plan is None:
        blockers.append("PLANNER_PLAN_MISSING")
    if intake is None or not intake.ready_for_real_preview:
        blockers.append("WORKBENCH_INTAKE_NOT_READY")
    if readiness is None or not readiness.ready_for_real_preview_writer:
        blockers.append("DEPENDENCY_READINESS_NOT_READY")
    if plan is not None and plan.status == "blocked":
        blockers.append("PLANNER_PLAN_BLOCKED")
    return blockers


def _preview_root_blockers(project_root: Path, preview_root: str) -> list[str]:
    """Return blockers for Preview roots outside selected project support."""
    return preview_root_blockers(project_root, preview_root)


def _destination_blockers(target: Path, preview_root: Path, project_root: Path) -> list[str]:
    """Return blockers for one preview destination."""
    resolved = target.resolve()
    blockers: list[str] = []
    if not _is_relative_to(resolved, preview_root):
        blockers.append("PREVIEW_DESTINATION_OUTSIDE_PREVIEW_ROOT")
    if _is_relative_to(resolved, project_root):
        blockers.append("PREVIEW_DESTINATION_INSIDE_PROJECT_SOURCE")
    if {part.lower() for part in resolved.parts} & _PROTECTED_PARTS:
        blockers.append("PREVIEW_DESTINATION_INSIDE_PROTECTED_ROOT")
    return blockers


def _safe_relative(text: str) -> Path:
    """Return a safe relative file path for a generated preview file."""
    path = Path(str(text or "").replace("\\", "/"))
    if not str(text).strip() or path.is_absolute() or ".." in path.parts:
        raise ValueError("UNSAFE_REAL_PREVIEW_RELATIVE_PATH")
    return path


def _blocked(
    target: str,
    source_hash: str,
    preview_root: str,
    blockers: list[str],
    *,
    extraction_backend: str = "blocked",
    warnings: list[str] | None = None,
    facade_consumer_compatibility: FacadeConsumerCompatibilityReport | None = None,
) -> RealPreviewWriteResult:
    """Return a blocked real-preview result."""
    return RealPreviewWriteResult(
        schema_version=SCHEMA_VERSION,
        feature_id=REAL_PREVIEW_FEATURE_ID,
        status="blocked",
        target_file=target,
        source_content_hash=source_hash,
        preview_root=preview_root,
        libcst_available=is_libcst_available(),
        extraction_backend=extraction_backend,
        facade_consumer_compatibility=(
            facade_consumer_compatibility.to_dict()
            if facade_consumer_compatibility is not None
            else {}
        ),
        blockers=sorted(set(blockers)),
        warnings=_stable_warnings(None, warnings or []),
    )


def _stable_warnings(extraction: SourceExtractionResult | None, extra: list[str] | None = None) -> list[str]:
    """Return stable warnings for this preview-only train."""
    warnings = [
        "REAL_PREVIEW_IS_PROJECT_SUPPORT_STATE_NOT_SOURCE_TRUTH",
        "SOURCE_MUTATION_DISABLED",
        "IMPORT_MIGRATION_APPLY_DISABLED",
        "CST_FIDELITY_METADATA_ENABLED",
        "HELPER_IMPORT_SYNTHESIS_METADATA_ENABLED",
        "STRONGER_CST_TRANSFORM_FIDELITY_ENABLED",
    ]
    if not is_libcst_available():
        warnings.append("LIBCST_NOT_AVAILABLE_SOURCE_SPAN_FALLBACK_USED")
    if extraction is not None:
        warnings.extend(extraction.warnings)
    warnings.extend(extra or [])
    return sorted(set(warnings))


def _hash_file(path: Path) -> str:
    """Return SHA-256 for a file or empty string."""
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return ""


def _is_relative_to(path: Path, base: Path) -> bool:
    """Return whether path is contained by base after resolution."""
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False
