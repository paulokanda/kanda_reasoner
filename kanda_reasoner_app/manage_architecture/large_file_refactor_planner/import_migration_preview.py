# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/import_migration_preview.py
"""Read-only import migration preview for planned module splits."""
from __future__ import annotations

from pathlib import Path

from .models import (
    FEATURE_ID,
    SCHEMA_VERSION,
    ImportMigrationPreview,
    ImportMigrationRecord,
    RefactorPlan,
)

__all__ = ["build_import_migration_preview", "discover_project_importers"]

_SKIP_DIR_NAMES = {
    ".git",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".venv",
    "venv",
    "env",
    "build",
    "dist",
}
_PROTECTED_PARTS = {
    "project_error_memory",
    "project_freeze_after_update",
    "large_file_refactor_preview",
}


def build_import_migration_preview(
    plan: RefactorPlan,
    *,
    active_project_root: str = "",
    importer_paths: list[str] | None = None,
    max_files: int = 200,
) -> ImportMigrationPreview:
    """Build a read-only preview of import updates without writing files."""
    blockers = []
    warnings = ["IMPORT_MIGRATION_PREVIEW_ONLY_NO_REWRITE"]
    target = Path(plan.target_file)
    source_stem = target.stem
    candidates = list(importer_paths or [])
    if active_project_root and importer_paths is None:
        candidates = discover_project_importers(active_project_root, source_stem, max_files=max_files)
    if not candidates:
        warnings.append("NO_PROJECT_IMPORTERS_FOUND_OR_SCAN_NOT_REQUESTED")
    if plan.import_migration.get("rewrite_project_imports") is True:
        blockers.append("IMPORT_REWRITE_ENABLED_NOT_ALLOWED_IN_PREVIEW")
    records = []
    for importer in sorted(set(candidates)):
        records.extend(_records_for_importer(plan, importer, source_stem))
    status = "blocked" if blockers else "preview_only"
    return ImportMigrationPreview(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        target_file=plan.target_file,
        source_content_hash=plan.source_content_hash,
        rewrite_enabled=False,
        records=records,
        blockers=sorted(set(blockers)),
        warnings=sorted(set(warnings)),
        status=status,
    )


def discover_project_importers(active_project_root: str, module_stem: str, *, max_files: int = 200) -> list[str]:
    """Return Python files that textually import the selected module stem."""
    project_root = Path(active_project_root).resolve()
    if not project_root.exists():
        return []
    matches: list[str] = []
    needles = (f"import {module_stem}", f"from {module_stem} import")
    for path in _iter_project_python_files(project_root, max_files):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if any(needle in text for needle in needles):
            matches.append(str(path))
    return matches


def _records_for_importer(
    plan: RefactorPlan,
    importer_file: str,
    source_stem: str,
) -> list[ImportMigrationRecord]:
    """Return preview records for one importing file."""
    helpers = [module.filename for module in plan.proposed_modules if module.role != "public_facade"]
    facade = next((module.filename for module in plan.proposed_modules if module.role == "public_facade"), Path(plan.target_file).name)
    suggested = _suggested_comment(source_stem, facade, helpers)
    return [
        ImportMigrationRecord(
            schema_version=SCHEMA_VERSION,
            feature_id=FEATURE_ID,
            importer_file=importer_file,
            original_import=f"import/from {source_stem}",
            suggested_import=suggested,
            action="review_only_no_rewrite",
            reason="Original facade remains public API owner; helper imports require future governed preview approval.",
            status="preview_only",
            blockers=[],
            risk_flags=["IMPORT_MIGRATION_NOT_APPLIED"],
        )
    ]


def _suggested_comment(source_stem: str, facade_filename: str, helpers: list[str]) -> str:
    """Return deterministic human-readable import migration guidance."""
    helper_text = ", ".join(sorted(helpers)) if helpers else "<none>"
    return (
        f"Keep public imports pointed at facade {facade_filename}; "
        f"review helper candidates for {source_stem}: {helper_text}."
    )


def _iter_project_python_files(project_root: Path, max_files: int):
    """Yield bounded project Python files while skipping protected roots."""
    seen = 0
    for path in project_root.rglob("*.py"):
        parts = set(path.parts)
        if parts & _PROTECTED_PARTS:
            continue
        if any(part in _SKIP_DIR_NAMES for part in path.parts):
            continue
        seen += 1
        if seen > max_files:
            break
        yield path
