# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/advanced_import_rewrite_support.py
"""Advanced no-write import rewrite support evidence for the Workbench."""
from __future__ import annotations

import ast
from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
from typing import Any

from .models import ImportMigrationPreview, ImportMigrationRecord, SCHEMA_VERSION

__all__ = [
    "ADVANCED_IMPORT_REWRITE_SUPPORT_FEATURE_ID",
    "AdvancedImportRewriteSupportResult",
    "build_advanced_import_rewrite_support",
    "write_advanced_import_rewrite_support",
]

ADVANCED_IMPORT_REWRITE_SUPPORT_FEATURE_ID = (
    "architecture-review-large-file-refactor-advanced-import-rewrite-support-v1"
)
_ADVANCED_SUPPORT_MANIFEST = "ADVANCED_IMPORT_REWRITE_SUPPORT.json"
_BLOCKED_FLAGS = {
    "STAR_IMPORT_RISK",
    "RELATIVE_IMPORT_RISK",
    "DYNAMIC_IMPORT_RISK",
    "STRING_REFERENCE_RISK",
    "PATCH_TARGET_RISK",
    "IMPORTER_SYNTAX_RISK",
}
_PROTECTED_PARTS = {
    ".project_reference",
    "_project_reference",
    "project_error_memory",
    "project_freeze_after_update",
    "project_freeze_ledger",
    "show_project_to_AI",
    "_show_project_to_AI",
}


@dataclass(frozen=True)
class AdvancedImportRewriteSupportResult:
    """No-write advanced import rewrite support evidence."""

    schema_version: str
    feature_id: str
    status: str
    target_file: str
    source_content_hash: str
    preview_root: str
    manifest_path: str
    rewrite_enabled: bool = False
    apply_enabled: bool = False
    alias_supported_count: int = 0
    multi_name_supported_count: int = 0
    future_safe_rewrite_count: int = 0
    manual_review_count: int = 0
    records: list[dict[str, Any]] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return JSON-ready result evidence."""
        return asdict(self)


def build_advanced_import_rewrite_support(
    import_preview: ImportMigrationPreview,
    *,
    active_project_root: str,
    preview_root: str = "",
) -> AdvancedImportRewriteSupportResult:
    """Build advanced read-only support records for future import rewrite trains."""
    project_root = Path(active_project_root).resolve()
    preview_path = Path(preview_root).resolve() if preview_root else Path("").resolve()
    manifest_path = preview_path / _ADVANCED_SUPPORT_MANIFEST if preview_root else Path("")
    records = [_advanced_record(record, project_root) for record in import_preview.records]
    blockers = _support_blockers(import_preview, project_root, preview_path, manifest_path, bool(preview_root))
    alias_count = sum(1 for item in records if item["alias_preserved"] or item["alias_detected"])
    multi_count = sum(1 for item in records if item["import_kind"] == "from_import_multi")
    future_safe_count = sum(1 for item in records if item["status"] == "future_safe_rewrite_supported")
    manual_count = sum(1 for item in records if item["status"] == "manual_review_required")
    warnings = _support_warnings(import_preview, records)
    status = "advanced_import_rewrite_support_ready" if not blockers else "blocked"
    return AdvancedImportRewriteSupportResult(
        schema_version=SCHEMA_VERSION,
        feature_id=ADVANCED_IMPORT_REWRITE_SUPPORT_FEATURE_ID,
        status=status,
        target_file=import_preview.target_file,
        source_content_hash=import_preview.source_content_hash,
        preview_root=str(preview_path) if preview_root else "",
        manifest_path=str(manifest_path) if preview_root else "",
        rewrite_enabled=False,
        apply_enabled=False,
        alias_supported_count=alias_count,
        multi_name_supported_count=multi_count,
        future_safe_rewrite_count=future_safe_count,
        manual_review_count=manual_count,
        records=records,
        blockers=sorted(set(blockers)),
        warnings=sorted(set(warnings)),
    )


def write_advanced_import_rewrite_support(result: AdvancedImportRewriteSupportResult) -> None:
    """Write advanced support evidence to the preview root without source mutation."""
    if not result.manifest_path or not result.preview_root:
        raise RuntimeError("Advanced import rewrite support manifest path is required.")
    manifest = Path(result.manifest_path).resolve()
    preview_root = Path(result.preview_root).resolve()
    if not _is_relative_to(manifest, preview_root):
        raise RuntimeError("Advanced import rewrite support manifest must stay inside preview root.")
    preview_root.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _advanced_record(record: ImportMigrationRecord, project_root: Path) -> dict[str, Any]:
    """Return one advanced support record without mutating importers."""
    original_info = _parse_import_statement(record.original_import)
    suggested_info = _parse_import_statement(record.suggested_import)
    flags = sorted(set(record.risk_flags))
    manual = bool(record.blockers) or bool(set(flags) & _BLOCKED_FLAGS)
    action = record.action
    status = "manual_review_required" if manual else "facade_owned_no_rewrite_supported"
    alias_preserved = _aliases_preserved(original_info, suggested_info)
    blockers: list[str] = []
    if action == "rewrite_import":
        if manual:
            status = "manual_review_required"
        elif not suggested_info["parseable"]:
            status = "manual_review_required"
            blockers.append("SUGGESTED_IMPORT_NOT_PARSEABLE")
        elif not alias_preserved:
            status = "manual_review_required"
            blockers.append("ALIAS_NOT_PRESERVED")
        else:
            status = "future_safe_rewrite_supported"
    importer = Path(record.importer_file).resolve()
    if not _is_relative_to(importer, project_root):
        status = "manual_review_required"
        blockers.append("IMPORTER_OUTSIDE_PROJECT")
    return {
        "importer_file": str(importer),
        "importer_relative": _safe_relative(importer, project_root),
        "original_import": record.original_import,
        "suggested_import": record.suggested_import,
        "action": action,
        "status": status,
        "import_kind": original_info["kind"],
        "alias_detected": bool(original_info["aliases"]),
        "alias_names": original_info["aliases"],
        "alias_preserved": alias_preserved,
        "imported_names": original_info["names"],
        "manual_review_reason": _manual_review_reason(flags, blockers, status),
        "risk_flags": flags,
        "blockers": blockers,
    }


def _parse_import_statement(text: str) -> dict[str, Any]:
    """Parse one compact import statement and return alias/name metadata."""
    result = {"parseable": False, "kind": "not_import", "aliases": [], "names": []}
    candidate = text.split(";", 1)[0].strip()
    if not candidate.startswith(("import ", "from ")):
        return result
    try:
        module = ast.parse(candidate)
    except SyntaxError:
        return result
    if len(module.body) != 1:
        return result
    node = module.body[0]
    if isinstance(node, ast.Import):
        result["parseable"] = True
        result["kind"] = "direct_import_multi" if len(node.names) > 1 else "direct_import"
        result["aliases"] = sorted(alias.asname for alias in node.names if alias.asname)
        result["names"] = sorted(alias.name for alias in node.names)
        return result
    if isinstance(node, ast.ImportFrom):
        if any(alias.name == "*" for alias in node.names):
            result["kind"] = "from_import_star"
        else:
            result["kind"] = "from_import_multi" if len(node.names) > 1 else "from_import"
        result["parseable"] = True
        result["aliases"] = sorted(alias.asname for alias in node.names if alias.asname)
        result["names"] = sorted(alias.name for alias in node.names)
    return result


def _aliases_preserved(original: dict[str, Any], suggested: dict[str, Any]) -> bool:
    """Return whether suggested import keeps all aliases from original."""
    original_aliases = set(original.get("aliases", []))
    if not original_aliases:
        return True
    if not suggested.get("parseable"):
        return False
    return original_aliases <= set(suggested.get("aliases", []))


def _support_blockers(
    import_preview: ImportMigrationPreview,
    project_root: Path,
    preview_root: Path,
    manifest_path: Path,
    has_preview_root: bool,
) -> list[str]:
    """Return shielding and preview blockers for advanced support evidence."""
    blockers = list(import_preview.blockers)
    if import_preview.rewrite_enabled is not False:
        blockers.append("IMPORT_PREVIEW_REWRITE_ENABLED_UNEXPECTEDLY")
    if has_preview_root:
        if _is_relative_to(preview_root, project_root):
            blockers.append("PREVIEW_ROOT_INSIDE_PROJECT_SOURCE")
        if not _is_relative_to(manifest_path, preview_root):
            blockers.append("ADVANCED_MANIFEST_OUTSIDE_PREVIEW_ROOT")
        lowered = {part.lower() for part in manifest_path.parts}
        for forbidden in _PROTECTED_PARTS:
            if forbidden.lower() in lowered:
                blockers.append(f"ADVANCED_MANIFEST_INSIDE_PROTECTED_{forbidden.upper()}")
    return blockers


def _support_warnings(
    import_preview: ImportMigrationPreview,
    records: list[dict[str, Any]],
) -> list[str]:
    """Return top-level warnings for advanced support evidence."""
    warnings = [
        "ADVANCED_IMPORT_REWRITE_SUPPORT_ONLY",
        "APPLY_NOT_ENABLED_BY_THIS_TRAIN",
        "STAR_RELATIVE_DYNAMIC_STRING_PATCH_REMAIN_MANUAL_REVIEW",
    ]
    warnings.extend(import_preview.warnings)
    if any(item["alias_detected"] for item in records):
        warnings.append("ALIAS_IMPORT_SUPPORT_EVIDENCE_PRESENT")
    if any(item["import_kind"] == "from_import_multi" for item in records):
        warnings.append("MULTI_NAME_FROM_IMPORT_SUPPORT_EVIDENCE_PRESENT")
    if any(item["status"] == "future_safe_rewrite_supported" for item in records):
        warnings.append("FUTURE_SAFE_REWRITE_SUPPORT_EVIDENCE_PRESENT")
    return warnings


def _manual_review_reason(flags: list[str], blockers: list[str], status: str) -> str:
    """Return a concise reason for manual or supported status."""
    if status != "manual_review_required":
        return "Advanced support evidence only; no source rewrite is enabled by this train."
    if blockers:
        return "; ".join(blockers)
    risky = sorted(set(flags) & _BLOCKED_FLAGS)
    return "Manual review required for risky import reference: " + ", ".join(risky or flags or ["unknown"])


def _is_relative_to(path: Path, root: Path) -> bool:
    """Return whether path is under root without requiring Python 3.9 behavior."""
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _safe_relative(path: Path, root: Path) -> str:
    """Return project-relative path when possible."""
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)
