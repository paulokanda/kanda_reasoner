# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_web_ai_import_artifact.py
"""External inbox contract for installed Web AI Planner version responses."""

from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.project_support_boundary import (
    assert_no_forbidden_nested_support_root,
)

__all__ = [
    "WEB_AI_IMPORT_DIRECTORY_NAME",
    "WEB_AI_IMPORT_FILENAME",
    "build_web_ai_import_contract",
    "read_installed_web_ai_response",
    "stage_validated_web_ai_response",
    "web_ai_import_artifact_path",
]

WEB_AI_IMPORT_DIRECTORY_NAME = "project_large_file_refactor_planner_web_ai_import"
WEB_AI_IMPORT_FILENAME = "pending_imported_web_ai_plan.txt"


def web_ai_import_artifact_path(project_root: str | Path) -> Path:
    """Return the external pending Web AI import artifact path for a project."""

    show_project_root = assert_no_forbidden_nested_support_root(project_root)
    return show_project_root / WEB_AI_IMPORT_DIRECTORY_NAME / WEB_AI_IMPORT_FILENAME


def read_installed_web_ai_response(project_root: str | Path) -> str:
    """Read one externally installed marker-wrapped Web AI response artifact."""

    artifact = web_ai_import_artifact_path(project_root)
    if not artifact.is_file():
        raise FileNotFoundError(
            "Installed Web AI Planner version artifact was not found: " + str(artifact)
        )
    return artifact.read_text(encoding="utf-8", errors="strict")


def stage_validated_web_ai_response(
    project_root: str | Path,
    raw_text: str,
) -> Path:
    """Stage one already-validated pasted response in the external import inbox."""

    if not isinstance(raw_text, str) or not raw_text.strip():
        raise ValueError("Validated Web AI response text cannot be empty.")
    artifact = web_ai_import_artifact_path(project_root)
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(raw_text, encoding="utf-8", newline="")
    installed = artifact.read_text(encoding="utf-8", errors="strict")
    if installed != raw_text:
        raise OSError("Installed Web AI response does not match staged text exactly.")
    return artifact


def build_web_ai_import_contract(project_root: str | Path) -> dict[str, object]:
    """Return the installer contract included in the Web AI clipboard package."""

    root = Path(project_root).expanduser().resolve(strict=False)
    relative_destination = str(
        Path(f"{root.name}_show_project_to_AI")
        / WEB_AI_IMPORT_DIRECTORY_NAME
        / WEB_AI_IMPORT_FILENAME
    )
    return {
        "artifact_kind": "kanda_large_file_refactor_planner_imported_web_ai_version",
        "destination_relative_to_drive_root": relative_destination,
        "payload_filename": WEB_AI_IMPORT_FILENAME,
        "required_bundle_files": [
            "INSTALL.ps1",
            "VALIDATE.ps1",
            "FREEZE.ps1",
            "KANDA_FREEZE_HINT.json",
            "bundle_manifest.json",
            WEB_AI_IMPORT_FILENAME,
        ],
        "installer_requirements": [
            "Create a governed ZIP containing install, validate, freeze-evidence, freeze-hint, manifest, and payload files.",
            "INSTALL.ps1 must accept -ProjectRoot and derive drive root with [System.IO.Path]::GetPathRoot($ProjectRoot).",
            "The installer must write only the pending imported Web AI plan artifact to the external destination contract.",
            "Do not modify KANDA Python source, Workbench state, selected-project source, freeze memory, or Error Memory Lessons.",
            "The installed payload must contain exactly one marker-wrapped KANDA_WEB_AI_PLANNING_RESPONSE block.",
            "PowerShell literal marker counts must use explicit whole-string logic such as Regex.Matches with Regex.Escape, not String.Split(markerString).",
            "The installer must verify that the installed payload equals the packaged payload exactly.",
        ],
        "validation_requirements": [
            "Validate exactly one begin marker and exactly one end marker.",
            "Validate JSON parsing, schema_version, exchange_feature_id, source_content_hash, base_plan_hash, action-list types, and complete architecture_answers.",
            "Validate that the installed artifact equals the packaged payload exactly.",
            "Fail closed before freeze evidence when any identity or marker contract fails.",
        ],
        "freeze_evidence_requirements": [
            "FREEZE.ps1 reruns or consumes fresh validation evidence and merges evidence only.",
            "Do not write canonical frozen feature memory directly.",
            "After evidence merge, use Freeze Feature After Update -> Preview -> Confirm and Write.",
            "Keep imported-plan freeze evidence separate from later Workbench source-implementation freeze evidence.",
        ],
        "receive_workflow": [
            "Install the returned ZIP locally as the canonical default path.",
            "Open Large File Refactor Planner.",
            "Select Imported Web AI Version to load the installed artifact, or paste the exact marker-wrapped response directly into Panel 4: Proposed split plan.",
            "Pasted text is validated, staged through the same external pending artifact boundary, read back, and revalidated before review.",
            "Review the imported plan, then load it as Imported Web AI Version.",
        ],
    }
