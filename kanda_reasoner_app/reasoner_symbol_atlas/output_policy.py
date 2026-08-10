# project-path: kanda_reasoner_app/reasoner_symbol_atlas/output_policy.py
"""Output policy helpers for Project Symbol Atlas reports.

The Project Symbol Atlas uses complete JSON as the canonical project evidence.
Live scans may add context, but archived reference folders, snippets, backups,
workbench scratch files, and migrated test archives must not become active edit
or test recommendations.
"""

from __future__ import annotations

import re
from typing import Iterable, List, Optional, Sequence

from .reference_folder_policy import (
    build_reasoner_symbol_atlas_reference_path_markers,
)

INACTIVE_PATH_MARKERS = (
    *build_reasoner_symbol_atlas_reference_path_markers(),
    "tests_archive/",
    "tests_archive\\",
    "remaining_misplaced_tests/",
    "remaining_misplaced_tests\\",
    "root_tests/_migrated_architecture/",
    "root_tests\\_migrated_architecture\\",
    "snippets/",
    "snippets\\",
    "workbench/_bundle_temp/",
    "workbench\\_bundle_temp\\",
    "deprecated/",
    "deprecated\\",
    "older_deprecated/",
    "older_deprecated\\",
    "oldies_deprecated/",
    "oldies_deprecated\\",
    "backup/",
    "backup\\",
    "backups/",
    "backups\\",
    "scratch/",
    "scratch\\",
    "_tmp_",
)

LOW_VALUE_TEST_MARKERS = (
    "/__init__.py",
    "\\__init__.py",
    "/fixtures/",
    "\\fixtures\\",
    "/benchmark_corpus/",
    "\\benchmark_corpus\\",
)

IMPORTANT_TEST_TERMS = (
    "reasoner_symbol_atlas",
    "engineering_safety",
    "reasoner_tools_gui_engineering_safety_panel",
    "_reasoner_tools_gui_engineering_safety_panel_commands",
    "gui003_engineering_safety_panel_actions",
    "gui004",
    "pa020",
    "pa021",
    "pa021b2",
    "pa023",
    "manage_architecture",
    "manage_workflows",
    "py_compile reasoner_tools_gui_engineering_safety_panel.py",
)

MAX_RELATED_FILES = 30
MAX_TESTS_TO_RUN = 18

__all__ = [
    "IMPORTANT_TEST_TERMS",
    "INACTIVE_PATH_MARKERS",
    "LOW_VALUE_TEST_MARKERS",
    "MAX_RELATED_FILES",
    "MAX_TESTS_TO_RUN",
    "is_active_atlas_path",
    "is_active_owner_candidate",
    "is_active_project_source_path",
    "is_active_test_command",
    "normalize_atlas_path",
    "sanitize_atlas_markdown_text",
]


def normalize_atlas_path(value: str) -> str:
    """Return a normalized path-like string for policy checks."""
    return value.strip().strip("`\"'").replace("\\", "/")


def is_active_atlas_path(value: str) -> bool:
    """Return True when a path can be used as active project evidence."""
    normalized = normalize_atlas_path(value).lower()
    if not normalized:
        return False
    inactive_markers = [marker.lower().replace("\\", "/") for marker in INACTIVE_PATH_MARKERS]
    if any(marker in normalized for marker in inactive_markers):
        return False
    return True


def is_active_project_source_path(value: str) -> bool:
    """Return True when a path is active implementation source, not tests."""
    normalized = normalize_atlas_path(value).lower()
    if not is_active_atlas_path(normalized):
        return False
    return not (normalized.startswith("tests/") or "/tests/" in normalized)


def is_active_owner_candidate(
    value: str,
    owner_role: str = "",
    is_test_file: bool = False,
) -> bool:
    """Return True when a record may compete for active canonical ownership."""
    normalized = normalize_atlas_path(value).lower().strip("/")
    if not normalized or not is_active_project_source_path(normalized):
        return False
    if is_test_file:
        return False
    role = str(owner_role or "").strip().lower()
    if role in {"generated_or_stale", "test_only"}:
        return False
    parts = tuple(part for part in normalized.split("/") if part)
    if any(part in {"fixtures", "generated", "_generated", "workbench"} for part in parts):
        return False
    name = parts[-1] if parts else ""
    if name.startswith("test_") or name.endswith("_test.py"):
        return False
    return True


def is_active_test_command(value: str) -> bool:
    """Return True when a test command should remain in GUI recommendations."""
    normalized = normalize_atlas_path(value).lower()
    inactive_markers = [marker.lower().replace("\\", "/") for marker in INACTIVE_PATH_MARKERS]
    low_value_markers = [marker.lower().replace("\\", "/") for marker in LOW_VALUE_TEST_MARKERS]
    if not normalized:
        return False
    if any(marker in normalized for marker in inactive_markers):
        return False
    if any(marker in normalized for marker in low_value_markers):
        return False
    if "python " not in normalized:
        return False
    if "python tests/" in normalized or "python ./tests/" in normalized:
        return False
    return True


def _has_important_test_term(value: str) -> bool:
    """Support has important test term behavior.
    
    Parameters
    ----------
    value : str
        The input value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    normalized = value.lower().replace("\\", "/")
    terms = [term.lower().replace("\\", "/") for term in IMPORTANT_TEST_TERMS]
    return any(term in normalized for term in terms)


def _extract_value_after(line: str, marker: str) -> Optional[str]:
    """Support extract value after behavior.
    
    Parameters
    ----------
    line : str
        The line value.
    marker : str
        The marker value.
    
    Returns
    -------
    Optional[str]
        The optional result.
    """
    
    if marker not in line:
        return None
    return line.split(marker, 1)[1].strip()


def _extract_target_path(lines: Sequence[str]) -> Optional[str]:
    """Support extract target path behavior.
    
    Parameters
    ----------
    lines : Sequence[str]
        The line values.
    
    Returns
    -------
    Optional[str]
        The optional result.
    """
    
    patterns = (
        r"->\s*([^\s;]+\.py)",
        r"query=([^;\n]+\.py)",
        r"target_path:\s*([^;\n]+\.py)",
        r"target_path=([^;\n]+\.py)",
    )
    for line in lines:
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                candidate = match.group(1).strip().strip("`\"'")
                if is_active_atlas_path(candidate):
                    return candidate
    return None


def _line_path_value(line: str) -> Optional[str]:
    """Support line path value behavior.
    
    Parameters
    ----------
    line : str
        The line value.
    
    Returns
    -------
    Optional[str]
        The optional result.
    """
    
    for marker in (
        "related_file=",
        "helper_path=",
        "main_path=",
        "primary_edit_target=",
        "file_not_to_touch=",
    ):
        value = _extract_value_after(line, marker)
        if value is not None:
            return value
    return None


def _should_drop_path_line(line: str) -> bool:
    """Support should drop path line behavior.
    
    Parameters
    ----------
    line : str
        The line value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    value = _line_path_value(line)
    if value is None:
        return False
    if value.startswith("box:"):
        return False
    return not is_active_atlas_path(value)


def _replace_bad_owner_line(line: str, target_path: Optional[str]) -> str:
    """Support replace bad owner line behavior.
    
    Parameters
    ----------
    line : str
        The line value.
    target_path : Optional[str]
        The target path value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if not target_path:
        return line
    inactive_primary = "primary_edit_target=" in line and _should_drop_path_line(line)
    inactive_main = "main_path=" in line and _should_drop_path_line(line)
    if inactive_primary:
        prefix = line.split("primary_edit_target=", 1)[0]
        return prefix + "primary_edit_target=" + target_path
    if inactive_main:
        prefix = line.split("main_path=", 1)[0]
        return prefix + "main_path=" + target_path
    if "pre_patch_status=wrong_target_file" in line:
        return line.replace("pre_patch_status=wrong_target_file", "pre_patch_status=needs_owner_review")
    return line


def _dedupe_keep_order(lines: Iterable[str]) -> List[str]:
    """Support dedupe keep order behavior.
    
    Parameters
    ----------
    lines : Iterable[str]
        The line values.
    
    Returns
    -------
    List[str]
        The list result.
    """
    
    seen = set()
    result = []
    for line in lines:
        key = line.strip()
        if key in seen:
            continue
        seen.add(key)
        result.append(line)
    return result


def sanitize_atlas_markdown_text(text: str) -> str:
    """Return GUI-friendly Atlas Markdown with active-scope recommendations only."""
    if not text:
        return text

    original_lines = text.splitlines()
    target_path = _extract_target_path(original_lines)
    cleaned: List[str] = []
    related_seen = 0
    tests_seen = 0
    policy_injected = False

    for original_line in original_lines:
        line = _replace_bad_owner_line(original_line, target_path)
        stripped = line.strip()

        if "existing_code_finder_decision (unknown)" in line:
            line = line.replace(
                "existing_code_finder_decision (unknown)",
                "existing_code_finder_decision (decision)",
            )
            stripped = line.strip()

        if (
            ".project_reference" in line or "_project_reference" in line
            or "project_freeze_ledger" in line
            or "tests_archive" in line
            or "remaining_misplaced_tests" in line
        ):
            if any(
                marker in line
                for marker in (
                    "related_file=",
                    "helper_path=",
                    "main_path=",
                    "test_to_run=",
                    "primary_edit_target=",
                )
            ):
                continue

        if stripped.startswith("- related_file="):
            value = stripped.split("related_file=", 1)[1]
            if not is_active_project_source_path(value):
                continue
            related_seen += 1
            if related_seen > MAX_RELATED_FILES:
                continue

        if stripped.startswith("- helper_path="):
            value = stripped.split("helper_path=", 1)[1]
            if not is_active_atlas_path(value):
                continue

        if stripped.startswith("- test_to_run="):
            value = stripped.split("test_to_run=", 1)[1]
            if not is_active_test_command(value):
                continue
            if not _has_important_test_term(value):
                continue
            tests_seen += 1
            if tests_seen > MAX_TESTS_TO_RUN:
                continue

        cleaned.append(line)

        if not policy_injected and line.startswith("## Decision Details"):
            policy_injected = True
            cleaned.append("")
            cleaned.append("- output_policy=json_canonical_active_scope")
            cleaned.append("- inactive_reference_paths_filtered=true")
            if target_path:
                cleaned.append("- active_target_path=" + target_path)

    cleaned = _dedupe_keep_order(cleaned)
    return "\n".join(cleaned).rstrip() + "\n"
