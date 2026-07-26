# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/preview_writer.py
"""Governed project-support Preview writer for the large-file planner."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

from .workbench_project_support_paths import (
    preview_root_blockers,
    resolve_workbench_preview_root,
)

from .models import (
    FEATURE_ID,
    SCHEMA_VERSION,
    DocstringProposal,
    LLMArbitrationResult,
    PreviewBundle,
    PreviewFileDraft,
    PreviewValidationResult,
    PreviewWriteResult,
    RefactorPlan,
)

__all__ = [
    "build_preview_bundle",
    "validate_preview_bundle",
    "write_preview_files",
    "resolve_preview_root",
]

_SKELETON_MODE = "preview_only_no_write_skeleton"
_GOVERNED_MODE = "governed_preview_project_support_only"
_CHECKED_RULES = [
    "no_project_source_write",
    "project_support_preview_root_only",
    "public_api_preserved",
    "source_hash_carried_forward",
    "validation_blockers_carried_forward",
    "libcst_parse_gate_or_safe_fallback",
]


def build_preview_bundle(
    plan: RefactorPlan,
    *,
    preview_root: str = "",
    docstring_proposals: list[DocstringProposal] | None = None,
    llm_result: LLMArbitrationResult | None = None,
    governed_write: bool = False,
) -> PreviewBundle:
    """Build a preview bundle from an existing split plan."""
    proposals = docstring_proposals or []
    files = [
        _draft_from_module(
            module.filename,
            module.role,
            module.symbols,
            module.estimated_lines,
            write_enabled=governed_write,
        )
        for module in plan.proposed_modules
    ]
    risks = list(plan.risks)
    if proposals:
        risks.append("DOCSTRING_PROPOSALS_REVIEW_REQUIRED")
    if llm_result is not None and llm_result.fallback_used:
        risks.append("LLM_FALLBACK_USED")
    blockers = list(plan.validation_blockers)
    if sorted(plan.public_api_before) != sorted(plan.public_api_after_expected):
        blockers.append("PUBLIC_API_MISMATCH")
    if governed_write and not preview_root:
        blockers.append("MISSING_PREVIEW_ROOT")
    write_mode = _GOVERNED_MODE if governed_write else _SKELETON_MODE
    status = "blocked" if blockers else "preview_write_ready" if governed_write else "preview_skeleton_ready"
    return PreviewBundle(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        target_file=plan.target_file,
        source_content_hash=plan.source_content_hash,
        preview_root=preview_root,
        write_mode=write_mode,
        libcst_available=_libcst_available(),
        public_api_before=list(plan.public_api_before),
        public_api_after_expected=list(plan.public_api_after_expected),
        files=files,
        validation_blockers=blockers,
        risk_flags=risks,
        status=status,
    )


def validate_preview_bundle(bundle: PreviewBundle) -> PreviewValidationResult:
    """Validate preview bundle safety without touching the filesystem."""
    blockers = list(bundle.validation_blockers)
    warnings = list(bundle.risk_flags)
    if bundle.write_mode not in {_SKELETON_MODE, _GOVERNED_MODE}:
        blockers.append("UNSAFE_WRITE_MODE")
    if sorted(bundle.public_api_before) != sorted(bundle.public_api_after_expected):
        blockers.append("PUBLIC_API_MISMATCH")
    if not bundle.source_content_hash:
        blockers.append("MISSING_SOURCE_HASH")
    if bundle.write_mode == _SKELETON_MODE and any(item.write_enabled for item in bundle.files):
        blockers.append("SKELETON_PREVIEW_FILE_WRITE_ENABLED")
    if bundle.write_mode == _GOVERNED_MODE and not all(item.write_enabled for item in bundle.files):
        blockers.append("GOVERNED_PREVIEW_FILE_WRITE_DISABLED")
    if bundle.write_mode == _GOVERNED_MODE and not bundle.preview_root:
        blockers.append("MISSING_PREVIEW_ROOT")
    if not bundle.libcst_available:
        warnings.append("LIBCST_NOT_AVAILABLE_SAFE_TEMPLATE_PREVIEW_ONLY")
    status = "passed" if not blockers else "blocked"
    return PreviewValidationResult(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        status=status,
        checked_rules=list(_CHECKED_RULES),
        blockers=blockers,
        warnings=warnings,
    )


def write_preview_files(bundle: PreviewBundle, active_project_root: str = "") -> PreviewWriteResult:
    """Write governed Preview artifacts under the selected project support root."""
    if not active_project_root:
        raise RuntimeError("Preview file writing is disabled unless an active project root is supplied.")
    blockers = _write_blockers(bundle, active_project_root)
    if blockers:
        return PreviewWriteResult(
            schema_version=SCHEMA_VERSION,
            feature_id=FEATURE_ID,
            status="blocked",
            preview_root=bundle.preview_root,
            written_files=[],
            blockers=blockers,
        )
    preview_root = Path(bundle.preview_root).resolve()
    preview_root.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    for draft in bundle.files:
        destination = preview_root / _safe_relative_path(draft.relative_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(_preview_file_text(bundle, draft), encoding="utf-8")
        written.append(str(destination))
    manifest = preview_root / "PREVIEW_MANIFEST.json"
    manifest.write_text(json.dumps(bundle.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    written.append(str(manifest))
    proof = preview_root / "NO_SOURCE_WRITE_PROOF.txt"
    proof.write_text(_proof_text(bundle, active_project_root), encoding="utf-8")
    written.append(str(proof))
    return PreviewWriteResult(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        status="written",
        preview_root=str(preview_root),
        written_files=written,
        warnings=list(bundle.risk_flags),
    )


def resolve_preview_root(active_project_root: str, daily_root: str = "") -> str:
    """Return the governed project-support Preview root without creating it."""
    if daily_root:
        raise ValueError("DAILY_WORK_PREVIEW_ROOT_FORBIDDEN")
    return str(resolve_workbench_preview_root(active_project_root))


def _write_blockers(bundle: PreviewBundle, active_project_root: str) -> list[str]:
    """Return blockers that prevent preview artifact writes."""
    blockers = list(bundle.validation_blockers)
    project_root = Path(active_project_root).resolve()
    if bundle.write_mode != _GOVERNED_MODE:
        blockers.append("WRITE_MODE_NOT_GOVERNED")
    if any(not item.write_enabled for item in bundle.files):
        blockers.append("DRAFT_WRITE_NOT_ENABLED")
    if not bundle.preview_root:
        blockers.append("MISSING_PREVIEW_ROOT")
        return sorted(set(blockers))
    preview_root = Path(bundle.preview_root).resolve()
    blockers.extend(preview_root_blockers(project_root, preview_root))
    for draft in bundle.files:
        try:
            _safe_relative_path(draft.relative_path)
        except ValueError as exc:
            blockers.append(str(exc))
    return sorted(set(blockers))


def _draft_from_module(
    filename: str,
    role: str,
    symbols: list[str],
    estimated_lines: int,
    *,
    write_enabled: bool,
) -> PreviewFileDraft:
    """Build one preview file draft from a proposed module."""
    seed = "\n".join([filename, role, *symbols, str(estimated_lines), str(write_enabled)])
    return PreviewFileDraft(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        relative_path=filename,
        source_role=role,
        planned_symbols=list(symbols),
        content_hash=hashlib.sha256(seed.encode("utf-8")).hexdigest(),
        estimated_lines=int(estimated_lines),
        write_enabled=write_enabled,
    )


def _preview_file_text(bundle: PreviewBundle, draft: PreviewFileDraft) -> str:
    """Return deterministic preview-only Python text for one draft."""
    exports = [name for name in draft.planned_symbols if name.isidentifier()]
    lines = [
        '"""Preview-only module draft generated by KANDA Reasoner."""',
        "# This file is a governed project-support Preview artifact.",
        "# It is not source of truth and must not be copied manually into source.",
        f"# Target source: {bundle.target_file}",
        f"# Source hash: {bundle.source_content_hash}",
        f"# Draft role: {draft.source_role}",
        "",
        "__all__ = " + repr(exports),
        "",
    ]
    for name in exports:
        lines.append(f"# Planned symbol: {name}")
    if not exports:
        lines.append("# No direct public symbols planned for this preview draft.")
    return "\n".join(lines).rstrip() + "\n"


def _proof_text(bundle: PreviewBundle, active_project_root: str) -> str:
    """Return a human-readable no-source-write proof record."""
    return "\n".join(
        [
            "KANDA governed preview generation proof",
            f"active_project_root={Path(active_project_root).resolve()}",
            f"preview_root={Path(bundle.preview_root).resolve()}",
            "project_source_modified=false",
            "preview_scope=project_support_only",
            f"feature_id={FEATURE_ID}",
            "",
        ]
    )


def _safe_relative_path(relative_path: str) -> Path:
    """Return a safe relative path or raise for unsafe path text."""
    cleaned = str(relative_path or "").replace("\\", "/").strip()
    path = Path(cleaned)
    if not cleaned or path.is_absolute() or ".." in path.parts:
        raise ValueError("UNSAFE_PREVIEW_RELATIVE_PATH")
    return path



def _libcst_available() -> bool:
    """Return whether LibCST is importable without importing it."""
    return importlib.util.find_spec("libcst") is not None
