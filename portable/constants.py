"""Constants for the KANDA Reasoner Portable builder."""

from __future__ import annotations

from pathlib import Path


PROJECT_FOLDER_NAME = "kanda_reasoner"
PRODUCT_NAME = "KandaReasoner"
SPEC_NAME = "KandaReasonerWindows.spec"
FINAL_ZIP_NAME = f"{PRODUCT_NAME}-Windows-Portable.zip"
EXPECTED_PYTHON = (3, 12)
EXPECTED_PYINSTALLER = "6.21.0"
MAX_ARCHIVE_PATH_BYTES = 259

NON_RUNTIME_LONG_PATH_DOCS = (
    Path("_internal")
    / "kanda_reasoner_app"
    / "routing_signal_scorer"
    / "mlrt_non_runtime_candidate_reliability"
)

FORBIDDEN_GENERATED_TOKENS = (
    "first_prompt_files",
    "second_prompt_files",
    "__ai_handoff_upload",
    "__ai_handoff_all_in_one",
    "__source_archive_part",
    "__png_assets_part",
    "__error_memory_full",
    "project_freeze_after_update/freeze_hint_intake",
    "-windows-portable.zip",
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
