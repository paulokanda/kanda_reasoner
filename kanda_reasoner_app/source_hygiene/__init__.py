# project-path: kanda_reasoner_app/source_hygiene/__init__.py
"""Source hygiene tools for Kanda Reasoner."""

from .bom_fixer import (
    BomFixResult,
    fix_project_utf8_bom,
    remove_utf8_bom_from_file,
    validate_text_file_after_bom_fix,
)
from .bom_scanner import (
    DEFAULT_BOM_SCAN_SUFFIXES,
    UTF8_BOM_BYTES,
    iter_bom_scan_files,
    scan_file_for_bom,
    scan_project_for_bom,
)
from .report_writer import default_source_hygiene_report_dir, write_source_hygiene_report
from .ruff_quality import (
    RUFF_QUALITY_FEATURE_ID,
    build_ruff_quality_report,
)
from .schemas import (
    DEFAULT_REPORT_TYPE,
    VALID_CONFIDENCE,
    VALID_REPORT_TYPES,
    VALID_SEVERITIES,
    SourceHygieneFinding,
    SourceHygieneReport,
    SourceHygieneWriteResult,
    make_report_id,
    normalize_confidence,
    normalize_report_type,
    normalize_severity,
    utc_timestamp,
)
from .shadow_audit import (
    ShadowAuditFileSummary,
    audit_project_for_shadow_conflicts,
    audit_python_file_for_shadow_conflicts,
    iter_shadow_audit_files,
)
from .shadow_fixer import (
    FacadeFixResult,
    apply_safe_package_marker_fix,
    build_safe_facade_fix_plan,
    iter_empty_init_files,
    plan_safe_package_marker_fix,
)
from .shadow_planner import (
    ShadowCorrectionPlanItem,
    build_shadow_conflict_plan,
    classify_shadow_finding,
    finding_to_plan_item,
)

__all__ = [
    "BomFixResult",
    "DEFAULT_BOM_SCAN_SUFFIXES",
    "DEFAULT_REPORT_TYPE",
    "FacadeFixResult",
    "RUFF_QUALITY_FEATURE_ID",
    "ShadowAuditFileSummary",
    "ShadowCorrectionPlanItem",
    "SourceHygieneFinding",
    "SourceHygieneReport",
    "SourceHygieneWriteResult",
    "UTF8_BOM_BYTES",
    "VALID_CONFIDENCE",
    "VALID_REPORT_TYPES",
    "VALID_SEVERITIES",
    "apply_safe_package_marker_fix",
    "audit_project_for_shadow_conflicts",
    "audit_python_file_for_shadow_conflicts",
    "build_safe_facade_fix_plan",
    "build_shadow_conflict_plan",
    "build_ruff_quality_report",
    "classify_shadow_finding",
    "default_source_hygiene_report_dir",
    "finding_to_plan_item",
    "fix_project_utf8_bom",
    "iter_bom_scan_files",
    "iter_empty_init_files",
    "iter_shadow_audit_files",
    "make_report_id",
    "normalize_confidence",
    "normalize_report_type",
    "normalize_severity",
    "plan_safe_package_marker_fix",
    "remove_utf8_bom_from_file",
    "scan_file_for_bom",
    "scan_project_for_bom",
    "utc_timestamp",
    "validate_text_file_after_bom_fix",
    "write_source_hygiene_report",
]
