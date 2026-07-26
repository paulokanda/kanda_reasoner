# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/models.py
"""Data contracts for the Architecture Review Large File Refactor Planner."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from ._model_payload_support import (
    _blocked_candidate,
    _module_analysis_payload,
    _plain_payload,
    _refactor_plan_payload,
)

from ._preview_delivery_models import (
    _ImportMigrationPreview,
    _ImportMigrationRecord,
    _PreviewArtifactValidationResult,
    _PreviewBundle,
    _PreviewFileDraft,
    _PreviewValidationResult,
    _PreviewWriteResult,
    _ProjectPatchPayloadResult,
)

PreviewFileDraft = _PreviewFileDraft
PreviewBundle = _PreviewBundle
PreviewValidationResult = _PreviewValidationResult
PreviewWriteResult = _PreviewWriteResult
ImportMigrationRecord = _ImportMigrationRecord
ImportMigrationPreview = _ImportMigrationPreview
PreviewArtifactValidationResult = _PreviewArtifactValidationResult
ProjectPatchPayloadResult = _ProjectPatchPayloadResult

for _public_name, _public_model in (
    ("PreviewFileDraft", PreviewFileDraft),
    ("PreviewBundle", PreviewBundle),
    ("PreviewValidationResult", PreviewValidationResult),
    ("PreviewWriteResult", PreviewWriteResult),
    ("ImportMigrationRecord", ImportMigrationRecord),
    ("ImportMigrationPreview", ImportMigrationPreview),
    ("PreviewArtifactValidationResult", PreviewArtifactValidationResult),
    ("ProjectPatchPayloadResult", ProjectPatchPayloadResult),
):
    _public_model.__name__ = _public_name
    _public_model.__qualname__ = _public_name
    _public_model.__module__ = __name__

del _public_model
del _public_name

__all__ = [
    "DocstringProposal",
    "FEATURE_ID",
    "IDEAL_PHYSICAL_LINES",
    "ImportMigrationPreview",
    "ImportMigrationRecord",
    "ImportRecord",
    "LLMArbitrationRequest",
    "LLMArbitrationResult",
    "LargeFileCandidate",
    "MAX_PHYSICAL_LINES",
    "MIN_HELPER_PHYSICAL_LINES",
    "ModuleAnalysisReport",
    "PATCH_ALLOWED_STATE",
    "PlannerSettings",
    "PlannerState",
    "PreviewArtifactValidationResult",
    "PreviewBundle",
    "PreviewFileDraft",
    "PreviewValidationResult",
    "PreviewWriteResult",
    "ProjectPatchPayloadResult",
    "ProposedModule",
    "RefactorPlan",
    "RefactorSymbol",
    "SCHEMA_VERSION",
    "SourceSnapshot",
]

FEATURE_ID = "architecture-review-large-file-refactor-planner-v1"
SCHEMA_VERSION = "1.0"
IDEAL_PHYSICAL_LINES = 400
MAX_PHYSICAL_LINES = 499
MIN_HELPER_PHYSICAL_LINES = 101


class PlannerState(str, Enum):
    """Allowed state machine values for the planner workflow."""

    IDLE = "IDLE"
    CANDIDATE_SELECTED = "CANDIDATE_SELECTED"
    ANALYZING = "ANALYZING"
    ANALYZED = "ANALYZED"
    PLAN_READY = "PLAN_READY"
    LLM_REVIEW_READY = "LLM_REVIEW_READY"
    DOCSTRING_READY = "DOCSTRING_READY"
    PREVIEW_GENERATING = "PREVIEW_GENERATING"
    PREVIEW_READY = "PREVIEW_READY"
    VALIDATING = "VALIDATING"
    VALIDATION_PASSED = "VALIDATION_PASSED"
    VALIDATION_FAILED = "VALIDATION_FAILED"
    PATCH_READY = "PATCH_READY"
    BLOCKED = "BLOCKED"
    STALE_SOURCE = "STALE_SOURCE"
    CANCELLED = "CANCELLED"


PATCH_ALLOWED_STATE = PlannerState.VALIDATION_PASSED


@dataclass(frozen=True)
class PlannerSettings:
    """User-visible settings for the first planner train car."""

    ideal_physical_lines: int = IDEAL_PHYSICAL_LINES
    maximum_physical_lines: int = MAX_PHYSICAL_LINES
    minimum_helper_physical_lines: int = MIN_HELPER_PHYSICAL_LINES
    preserve_public_facade: bool = True
    generate_missing_docstrings: bool = True
    rewrite_project_imports: bool = False
    import_migration_preview: bool = True
    use_local_llm: bool = False
    preview_only: bool = True
    create_patch_only_after_validation: bool = True

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready settings dictionary."""
        return _plain_payload(self)


@dataclass(frozen=True)
class SourceSnapshot:
    """Stable source fingerprint used by preview and patch staleness gates."""

    schema_version: str
    feature_id: str
    source_path: str
    source_size: int
    source_mtime_ns: int
    source_content_hash: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready source snapshot dictionary."""
        return _plain_payload(self)


@dataclass(frozen=True)
class LargeFileCandidate:
    """Candidate Python file for safe large-module planning."""

    schema_version: str
    path: str
    relative_path: str
    line_count_physical: int
    public_symbol_count: int = 0
    class_count: int = 0
    function_count: int = 0
    missing_docstring_count: int = 0
    external_importer_count: int = 0
    risk_flags: list[str] = field(default_factory=list)
    source_box: str = "active_project_source"
    is_eligible: bool = True
    blocked_reason: str = ""
    suggested_action: str = "Analyze"

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready candidate dictionary."""
        return _plain_payload(self)

    @classmethod
    def blocked(
        cls,
        *,
        path: Path,
        root: Path,
        line_count: int,
        reason: str,
        suggested_action: str,
    ) -> "LargeFileCandidate":
        """Build a blocked candidate while preserving path evidence."""
        return _blocked_candidate(
            cls, SCHEMA_VERSION, path, root, line_count, reason, suggested_action
        )


@dataclass(frozen=True)
class RefactorSymbol:
    """Top-level symbol evidence collected by the AST analyzer."""

    schema_version: str
    name: str
    kind: str
    visibility: str
    start_line: int
    end_line: int
    physical_lines: int
    decorators: list[str] = field(default_factory=list)
    signature: str = ""
    return_annotation: str = ""
    has_docstring: bool = False
    docstring_text: str = ""
    docstring_provenance: str = "existing"
    references: list[str] = field(default_factory=list)
    imports_used: list[str] = field(default_factory=list)
    globals_used: list[str] = field(default_factory=list)
    external_importers: list[str] = field(default_factory=list)
    atomic_cluster_id: str = ""
    risk_flags: list[str] = field(default_factory=list)
    assigned_module: str = ""
    content_hash: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready symbol dictionary."""
        return _plain_payload(self)


@dataclass(frozen=True)
class ImportRecord:
    """Import statement evidence for one selected module."""

    schema_version: str
    original_module: str
    imported_name: str
    alias: str = ""
    is_relative: bool = False
    relative_level: int = 0
    is_star: bool = False
    line_span: tuple[int, int] = (0, 0)
    used_by_symbols: list[str] = field(default_factory=list)
    risk_flags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready import dictionary."""
        return _plain_payload(self)


@dataclass(frozen=True)
class ModuleAnalysisReport:
    """Read-only AST evidence for the currently selected target module."""

    schema_version: str
    feature_id: str
    target_file: str
    source_content_hash: str
    line_count_physical: int
    module_docstring_present: bool
    module_docstring_preview: str
    all_names: list[str]
    public_api_symbols: list[str]
    imports: list[ImportRecord]
    symbols: list[RefactorSymbol]
    constants: list[str]
    assignments: list[str]
    global_statements: list[str]
    nonlocal_statements: list[str]
    module_level_calls: list[str]
    if_main_present: bool
    nested_symbol_count: int
    missing_docstring_count: int
    risk_flags: list[str] = field(default_factory=list)
    analysis_errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready analysis report dictionary."""
        return _module_analysis_payload(self)


@dataclass(frozen=True)
class ProposedModule:
    """Planned output module placeholder for later train cars."""

    schema_version: str
    filename: str
    role: str
    symbols: list[str]
    estimated_lines: int
    preview_physical_lines: int = 0
    imports: list[str] = field(default_factory=list)
    exports: list[str] = field(default_factory=list)
    docstrings_generated: list[str] = field(default_factory=list)
    risk_flags: list[str] = field(default_factory=list)
    status: str = "not_generated"
    line_limit_justification: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready proposed module dictionary."""
        return _plain_payload(self)


@dataclass(frozen=True)
class DocstringProposal:
    """Reviewable docstring proposal generated from static evidence only."""

    schema_version: str
    feature_id: str
    target_file: str
    target_kind: str
    target_name: str
    proposed_docstring: str
    provenance: str
    confidence: str
    risk_flags: list[str] = field(default_factory=list)
    reason: str = ""
    status: str = "proposed"

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready docstring proposal dictionary."""
        return _plain_payload(self)


@dataclass(frozen=True)
class LLMArbitrationRequest:
    """Bounded JSON-only request contract for local LLM arbitration."""

    schema_version: str
    feature_id: str
    target_file: str
    purpose: str
    symbol_name: str
    symbol_line_span: tuple[int, int]
    candidate_modules: list[str]
    model_name: str
    temperature: float
    settings_hash: str
    prompt_version: str
    file_content_hash: str
    symbol_body_hash: str
    candidate_module_list_hash: str
    cache_key: str
    local_llm_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready LLM arbitration request."""
        return _plain_payload(self)


@dataclass(frozen=True)
class LLMArbitrationResult:
    """Validated result or deterministic fallback for local LLM arbitration."""

    schema_version: str
    feature_id: str
    status: str
    selected_module: str = ""
    confidence: str = "none"
    rationale: str = ""
    warnings: list[str] = field(default_factory=list)
    raw_response_used: bool = False
    fallback_used: bool = True

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready LLM arbitration result."""
        return _plain_payload(self)


@dataclass(frozen=True)
class RefactorPlan:
    """Deterministic split-plan contract generated before preview writing."""

    schema_version: str
    feature_id: str
    target_file: str
    source_content_hash: str
    settings: dict[str, Any]
    public_api_before: list[str]
    public_api_after_expected: list[str]
    symbols: list[RefactorSymbol]
    atomic_clusters: list[str]
    proposed_modules: list[ProposedModule]
    import_migration: dict[str, Any]
    docstring_proposals: list[DocstringProposal]
    risks: list[str]
    validation_blockers: list[str]
    status: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready refactor plan dictionary."""
        return _refactor_plan_payload(self)
