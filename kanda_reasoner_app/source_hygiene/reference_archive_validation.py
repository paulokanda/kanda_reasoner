"""Validate local metadata and the explicit KANDA reference archive."""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import Callable

from kanda_reasoner_app.project_exclusion_policy import (
    DEFAULT_PROJECT_EXCLUDED_FOLDERS,
)
from kanda_reasoner_app.reasoner_context_bundle import (
    source_tree_exporter_inventory as _source_inventory,
)
from kanda_reasoner_app.reasoner_context_bundle.source_tree_exporter_shared import (
    _ALWAYS_EXCLUDED_DIRS,
)
from kanda_reasoner_app.source_hygiene.tool_archive_policy import (
    ToolArchivePolicyError,
    ToolPathClassification,
    classify_tool_source_path,
)

Gate = Callable[[str, bool, str], None]

_LOCAL_METADATA_NAMES = {".ai", ".idea", ".vscode", ".novelide"}
_SOURCE_SUFFIXES = {
    ".py",
    ".pyi",
    ".spec",
    ".ps1",
    ".sh",
    ".bash",
    ".bat",
    ".cmd",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".mjs",
    ".cjs",
    ".rs",
    ".go",
    ".java",
    ".kt",
    ".kts",
    ".c",
    ".cc",
    ".cpp",
    ".h",
    ".hpp",
    ".cs",
    ".swift",
    ".rb",
    ".php",
}


def copy_hygiene_contract(source_root: Path, target_root: Path) -> None:
    """Copy the immutable source-hygiene contract into one test Tool root."""
    source = source_root / "kanda_reasoner_app" / "source_hygiene"
    target = target_root / "kanda_reasoner_app" / "source_hygiene"
    target.mkdir(parents=True, exist_ok=True)
    for relative in (
        "TOOL_SOURCE_CLASSIFICATION.json",
        "SYNTHETIC_FIXTURE_MANIFEST.json",
        "fixtures/static_context_smoke_minimal.json",
    ):
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / relative, destination)


def validate_local_development_metadata_classification(
    project_root: Path,
    gate: Gate,
) -> None:
    """Preserve bounded metadata acceptance and source-bearing rejection."""
    with tempfile.TemporaryDirectory(prefix="kanda_hidden_metadata_") as raw:
        fixture_root = Path(raw)
        copy_hygiene_contract(project_root, fixture_root)
        for name in _LOCAL_METADATA_NAMES:
            folder = fixture_root / name
            folder.mkdir()
            (folder / "workspace.json").write_text("{}", encoding="utf-8")
        decisions = {
            name: classify_tool_source_path(fixture_root, Path(name))
            for name in sorted(_LOCAL_METADATA_NAMES)
        }
        safe = all(
            item.classification
            is ToolPathClassification.GENERATED_TOOL_EVIDENCE
            and not item.include_in_tool_archive
            for item in decisions.values()
        )
        for name, relative in (
            (".github", "workflows/check.yml"),
            (".hidden_source", "module.py"),
        ):
            path = fixture_root / name / relative
            path.parent.mkdir(parents=True)
            path.write_text("pass", encoding="utf-8")
            try:
                classify_tool_source_path(fixture_root, Path(name))
            except ToolArchivePolicyError:
                continue
            raise AssertionError("HIDDEN_SOURCE_DIRECTORY_FAIL_CLOSED:" + name)
        try:
            classify_tool_source_path(fixture_root, Path("mystery_source"))
        except ToolArchivePolicyError:
            unknown_rejected = True
        else:
            unknown_rejected = False
    gate("TOOL_LOCAL_AI_METADATA_CLASSIFIED", safe and ".ai" in decisions, "")
    gate("TOOL_LOCAL_DEVELOPMENT_METADATA_CLASSIFIED", safe, "")
    gate("TOOL_ROOT_HIDDEN_METADATA_POLICY", safe and unknown_rejected, "")


def _live_reference_counts(reference_root: Path) -> tuple[int, int]:
    files = 0
    source_bearing = 0
    for candidate in reference_root.rglob("*"):
        if candidate.is_symlink():
            raise AssertionError(
                "PROJECT_REFERENCE_REPARSE_POINT_PRESENT:" + str(candidate)
            )
        if not candidate.is_file():
            continue
        files += 1
        if candidate.suffix.casefold() in _SOURCE_SUFFIXES:
            source_bearing += 1
    return files, source_bearing


def validate_project_reference_archive_policy(
    project_root: Path,
    gate: Gate,
) -> None:
    """Validate the established noncanonical .project_reference owner."""
    reference_root = project_root / ".project_reference"
    gate(
        "PROJECT_REFERENCE_LIVE_REFERENCE_ARCHIVE_PRESENT",
        reference_root.is_dir() and not reference_root.is_symlink(),
        str(reference_root),
    )
    decision = classify_tool_source_path(project_root, Path(".project_reference"))
    explicit = (
        decision.classification
        is ToolPathClassification.GENERATED_TOOL_EVIDENCE
        and not decision.include_in_tool_archive
        and decision.matched_rule == "path_prefix:.project_reference"
    )
    gate("PROJECT_REFERENCE_EXPLICIT_CLASSIFICATION", explicit, decision.matched_rule)
    file_count, source_count = _live_reference_counts(reference_root)
    gate(
        "PROJECT_REFERENCE_SOURCE_BEARING_CONTENT_NONCANONICAL",
        file_count > 0 and source_count > 0,
        f"files={file_count};source_bearing={source_count}",
    )
    gate(
        "PROJECT_REFERENCE_PROJECT_POLICY_EXCLUSION_PRESERVED",
        ".project_reference" in DEFAULT_PROJECT_EXCLUDED_FOLDERS,
        "",
    )
    gate(
        "PROJECT_REFERENCE_SOURCE_ARCHIVE_EXCLUSION_PRESERVED",
        ".project_reference" in _ALWAYS_EXCLUDED_DIRS,
        "",
    )

    with tempfile.TemporaryDirectory(prefix="kanda_reference_archive_") as raw:
        fixture_root = Path(raw) / "tool"
        output_root = Path(raw) / "output"
        (fixture_root / "kanda_reasoner_app").mkdir(parents=True)
        (fixture_root / "reasoner_tools_gui.py").write_text(
            "# fixture\n", encoding="utf-8"
        )
        (fixture_root / "KandaReasonerWindows.spec").write_text(
            "# fixture\n", encoding="utf-8"
        )
        (fixture_root / "kanda_reasoner_app" / "__init__.py").write_text(
            "# fixture\n", encoding="utf-8"
        )
        reference_file = fixture_root / ".project_reference" / "CANNON" / "old.py"
        reference_file.parent.mkdir(parents=True)
        reference_file.write_text("VALUE = 1\n", encoding="utf-8")
        copy_hygiene_contract(project_root, fixture_root)
        inventory = _source_inventory.gather_source_archive_inventory(
            fixture_root,
            output_root,
        )
        included = {str(item["path"]) for item in inventory["included_files"]}
        excluded = {str(item["path"]) for item in inventory["excluded_paths"]}
        preserved = (
            ".project_reference" in excluded
            and not any(path.startswith(".project_reference/") for path in included)
        )
    gate("PROJECT_REFERENCE_ARCHIVE_INCLUDED_FILE_COUNT_ZERO", preserved, "")
