# project-path: kanda_reasoner_app/reasoner_context_bundle/patch_safety_routes_builder.py
"""Build conservative patch-safety routes for AI-assisted edits."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from kanda_reasoner_app.project_artifact_staging import (
    build_project_artifact_staging_contract,
)

from .json_writer import write_json_atomic
from .output_paths import bundle_artifact_paths
from .path_normalization import artifact_logical_posix_path
from .project_context import resolve_project_context
from .schema_models import ProjectContext

__all__ = [
    "build_patch_safety_routes_payload",
    "write_patch_safety_routes_json",
]

SCHEMA_VERSION = 1
BUNDLE_KIND = "patch_safety_routes"
GENERATOR_NAME = "reasoner_context_bundle.patch_safety_routes_builder"
GENERATOR_VERSION = "1.2.0"


def _utc_now() -> str:
    """Support utc now behavior.
    
    Returns
    -------
    str
        The string result.
    """
    
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _context(project: str | Path | ProjectContext) -> ProjectContext:
    """Support context behavior.
    
    Parameters
    ----------
    project : str | Path | ProjectContext
        The project value.
    
    Returns
    -------
    ProjectContext
        The project context result.
    """
    
    if isinstance(project, ProjectContext):
        return project
    return resolve_project_context(project)


def _safety_route(
    subsystem: str,
    description: str,
    source_hints: list[str],
    validation: list[str],
    freeze_required: bool,
) -> dict[str, Any]:
    """Support safety route behavior.
    
    Parameters
    ----------
    subsystem : str
        The subsystem value.
    description : str
        The description value.
    source_hints : list[str]
        The source hints value.
    validation : list[str]
        The validation value.
    freeze_required : bool
        The freeze required value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    return {
        "subsystem": subsystem,
        "description": description,
        "risk_level": "governed" if freeze_required else "standard",
        "must_read_source_hints": source_hints,
        "must_inspect_exact_source_before_editing": True,
        "allowed_edit_policy": "Edit only exact source files required for the task.",
        "forbidden_generated_paths": [
            "show_project_to_AI/**",
            "*_show_project_to_AI/**",
            "__pycache__/**",
            "*.pyc",
        ],
        "required_validation": validation,
        "freeze_required": freeze_required,
        "notes": [
            "JSON artifacts are evidence and routing aids, not edit authority.",
            "Generated files must not be modified as source code.",
        ],
    }


def build_patch_safety_routes_payload(project: str | Path | ProjectContext) -> dict[str, Any]:
    """Build decision-ready patch-safety routes for a selected project."""
    context = _context(project)
    paths = bundle_artifact_paths(context)
    return {
        "schema_version": SCHEMA_VERSION,
        "bundle_kind": BUNDLE_KIND,
        "generator": {
            "name": GENERATOR_NAME,
            "version": GENERATOR_VERSION,
        },
        "generated_at_utc": _utc_now(),
        "artifact_staging": build_project_artifact_staging_contract(context.root),
        "project": {
            "project_slug": context.project_slug,
            "project_root_marker": "<PROJECT_ROOT>",
            "evidence_root_relative": "show_project_to_AI",
            "json_complete_relative": "show_project_to_AI/second_prompt_files",
        },
        "source_truth_policy": {
            "source_files_are_truth": True,
            "inspect_exact_source_before_editing": True,
            "json_summaries_do_not_authorize_patches": True,
        },
        "related_artifacts": {
            "routing_manifest_json": artifact_logical_posix_path(paths.routing_manifest_json, context),
            "bundle_manifest_json": artifact_logical_posix_path(paths.bundle_manifest_json, context),
            "validation_state_json": artifact_logical_posix_path(paths.validation_state_json, context),
        },
        "subsystems": {
            "project_structure_map": _safety_route(
                "project_structure_map",
                "Collector tab, Run Collector, dynamic evidence paths, lightweight map JSON, source archive manifest, and companion bundle generation.",
                ["CollectorRunnerWindow", "_run_collector", "_start_collector_process", "bundle_orchestrator", "output_paths"],
                ["py_compile changed files", "run reasoner_context_bundle CLI on a sample project", "verify dynamic show_project_to_AI output path"],
                True,
            ),
            "gui_shell": _safety_route(
                "gui_shell",
                "PySide GUI tabs, buttons, callbacks, and embedded tool windows.",
                ["QTabWidget", "QPushButton", "clicked.connect", "tool_specs"],
                ["py_compile changed files", "manual GUI smoke check"],
                False,
            ),
            "patch_delivery": _safety_route(
                "patch_delivery",
                "Patch ZIP contract, install instructions, validation delivery, and release hygiene.",
                ["patch", "install", "validation", "KANDA_FREEZE_HINT"],
                ["patch contract validation", "py_compile changed files"],
                True,
            ),
            "freeze_workflow": _safety_route(
                "freeze_workflow",
                "Freeze memory, preview, confirm-and-write, and startup freeze-context refresh.",
                ["freeze", "Confirm and Write", "frozen_features_memory", "freeze_hint_intake"],
                ["freeze workflow validation", "py_compile changed files"],
                True,
            ),
        },
    }


def write_patch_safety_routes_json(project: str | Path | ProjectContext) -> Path:
    """Write <project_slug>__patch_safety_routes.json for one project."""
    context = _context(project)
    paths = bundle_artifact_paths(context)
    payload = build_patch_safety_routes_payload(context)
    return write_json_atomic(paths.patch_safety_routes_json, payload)
