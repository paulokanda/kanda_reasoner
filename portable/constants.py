"""Constants for the KANDA Reasoner Portable builder."""

from __future__ import annotations

from pathlib import Path


__all__ = [
    "BUILDER_VERSION",
    "PORTABLE_HARDENING_FEATURES",
    "PORTABLE_HARDENING_STAGE",
    "BUILDER_MEMBER_FEATURE_ID",
    "EXTERNAL_CONTROL_FEATURE_ID",
    "PRODUCTION_PORTABLE_ENABLED",
    "PROJECT_FOLDER_NAME",
    "SPEC_NAME",
    "FINAL_ZIP_NAME",
    "EXPECTED_PYTHON",
    "EXPECTED_PYINSTALLER",
    "MAX_ARCHIVE_PATH_BYTES",
    "FIRST_SMOKE_CONFIRMATION",
    "SMOKE_CONFIRMATION",
    "NON_RUNTIME_LONG_PATH_DOCS",
    "FORBIDDEN_GENERATED_FOLDER_NAMES",
    "FORBIDDEN_GENERATED_PATH_SEQUENCES",
    "RUNTIME_PACKAGE_PATH_SEQUENCES",
    "FORBIDDEN_GENERATED_FILE_MARKERS",
    "PORTABLE_ARCHIVE_SUFFIX",
    "NON_RUNTIME_CACHE_FOLDER_NAMES",
    "NON_RUNTIME_DEBRIS_FILE_NAMES",
    "NON_RUNTIME_BACKUP_MARKERS",
    "NON_RUNTIME_BACKUP_SUFFIXES",
    "PROJECT_SNAPSHOT_IGNORES",
    "VENV_PYTHON_RELATIVE",
]

FEATURE_ID = "kanda-reasoner-portable-timestamped-publication-name-v1r32"
BUILDER_VERSION = "v1r32"
PORTABLE_HARDENING_FEATURES = (
    "registry-boundary-gate",
    "packaged-gui-smoke-isolation",
    "governed-root-exact-rollback",
    "runtime-path-hash-allowlist",
    "exact-builder-member-governance",
    "external-build-control-hash-binding",
    "self-host-venv-build-interpreter",
    "production-portable-authorization",
    "spec-audit-policy-reconciliation",
    "posix-zip-member-writer",
    "packaged-gui-runtime-report-preservation",
    "pyinstaller-submodule-import-preflight",
    "selected-owner-fire-shield-isolation",
    "packaged-worker-reentry-dispatch",
    "clean-start-gui-regression-reset",
    "tool-project-decoupled-portable-build",
    "timestamped-publication-name",
)
PORTABLE_HARDENING_STAGE = (
    "registry-boundary-plus-smoke-isolation-plus-"
    "governed-root-rollback-plus-runtime-path-hash-allowlist-plus-"
    "exact-builder-member-governance-plus-"
    "external-build-control-hash-binding-plus-"
    "self-host-venv-build-interpreter-plus-"
    "production-portable-authorization-plus-"
    "spec-audit-policy-reconciliation-plus-"
    "posix-zip-member-writer-plus-"
    "packaged-gui-runtime-report-preservation-plus-"
    "pyinstaller-submodule-import-preflight-plus-"
    "selected-owner-fire-shield-isolation-plus-"
    "packaged-worker-reentry-dispatch-plus-"
    "clean-start-gui-regression-reset-plus-"
    "tool-project-decoupled-portable-build-plus-"
    "timestamped-publication-name"
)
BUILDER_MEMBER_FEATURE_ID = (
    "kanda-reasoner-portable-exact-builder-member-governance-v1"
)
EXTERNAL_CONTROL_FEATURE_ID = (
    "kanda-reasoner-portable-external-build-control-hash-binding-v1r2"
)
EXTERNAL_CONTROL_MANIFEST_NAME = "PORTABLE_EXTERNAL_BUILD_CONTROLS.json"
PRODUCTION_PORTABLE_ENABLED = True
PROJECT_FOLDER_NAME = "kanda_reasoner"
PRODUCT_NAME = "KandaReasoner"
SPEC_NAME = "KandaReasonerWindows.spec"
FINAL_ZIP_NAME = f"{PRODUCT_NAME}-Windows-Portable.zip"
EXPECTED_PYTHON = (3, 12)
EXPECTED_PYINSTALLER = "6.21.0"
VENV_PYTHON_RELATIVE = Path(".venv") / "Scripts" / "python.exe"
MAX_ARCHIVE_PATH_BYTES = 259
FIRST_SMOKE_CONFIRMATION = "FIRST PASS CLOSED"
SMOKE_CONFIRMATION = "PORTABLE TESTS PASS CLOSED"

NON_RUNTIME_LONG_PATH_DOCS = (
    Path("_internal")
    / "kanda_reasoner_app"
    / "routing_signal_scorer"
    / "mlrt_non_runtime_candidate_reliability"
)

FORBIDDEN_GENERATED_FOLDER_NAMES = {
    "first_prompt_files",
    "second_prompt_files",
}

FORBIDDEN_GENERATED_PATH_SEQUENCES = (
    (
        "project_freeze_after_update",
        "freeze_hint_intake",
    ),
)

RUNTIME_PACKAGE_PATH_SEQUENCES = (
    (
        "kanda_reasoner_app",
        "freeze_hint_intake",
    ),
)

FORBIDDEN_GENERATED_FILE_MARKERS = (
    "__ai_handoff_upload",
    "__ai_handoff_all_in_one",
    "__source_archive_part",
    "__png_assets_part",
    "__error_memory_full",
)

PORTABLE_ARCHIVE_SUFFIX = "-windows-portable.zip"

NON_RUNTIME_CACHE_FOLDER_NAMES = {
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
}

NON_RUNTIME_DEBRIS_FILE_NAMES = {
    ".ds_store",
    "desktop.ini",
    "thumbs.db",
}

NON_RUNTIME_BACKUP_MARKERS = (
    ".bak_",
    ".backup_",
    ".orig_",
    ".rej_",
)

NON_RUNTIME_BACKUP_SUFFIXES = (
    ".bak",
    ".backup",
    ".orig",
    ".rej",
    "~",
)

PROJECT_SNAPSHOT_IGNORES = {
    ".git",
    ".idea",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
}
