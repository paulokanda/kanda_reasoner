# project-path: kanda_reasoner_app/reasoner_context_bundle/routing_manifest_builder.py
"""Build task-to-evidence routes for AI project handoff."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from .handoff_boundary_contract import build_handoff_trust_envelope
from .json_writer import write_json_atomic
from .output_paths import bundle_artifact_paths
from .path_normalization import artifact_logical_posix_path
from .project_context import resolve_project_context
from .schema_models import ProjectContext
from .source_tree_exporter_shared import SOURCE_ARCHIVE_MANIFEST_SUFFIX

__all__ = [
    "build_routing_manifest_payload",
    "write_routing_manifest_json",
]

SCHEMA_VERSION = 1
BUNDLE_KIND = "routing_manifest"
GENERATOR_NAME = "reasoner_context_bundle.routing_manifest_builder"
GENERATOR_VERSION = "1.3.0"


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


def _route(
    task_type: str,
    description: str,
    source_archive_hints: list[str],
    source_search: list[str],
    validation_hint: list[str],
    additional_route_read_artifacts: list[str] | None = None,
) -> dict[str, Any]:
    """Support route behavior.
    
    Parameters
    ----------
    task_type : str
        The task type value.
    description : str
        The description value.
    source_archive_hints : list[str]
        The source archive hints value.
    source_search : list[str]
        The source search value.
    validation_hint : list[str]
        The validation hint value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    route_read_artifacts = [
        "bundle_manifest_json",
        "file_manifest_json",
        "patch_safety_routes_json",
    ]
    for artifact_name in additional_route_read_artifacts or []:
        if artifact_name not in route_read_artifacts:
            route_read_artifacts.append(artifact_name)

    return {
        "task_type": task_type,
        "description": description,
        "always_read_artifacts": [
            "ai_briefing_json",
            "routing_manifest_json",
        ],
        "route_read_artifacts": route_read_artifacts,
        "source_archive_hints": source_archive_hints,
        "source_search_hints": source_search,
        "must_inspect_exact_source_before_editing": True,
        "forbidden_generated_paths": [
            "show_project_to_AI/**",
            "*_show_project_to_AI/**",
        ],
        "validation_hints": validation_hint,
        "fallback": (
            "If this route is incomplete, search file_manifest and source_archive_manifest, "
            "then inspect exact source files before editing."
        ),
    }


def build_routing_manifest_payload(project: str | Path | ProjectContext) -> dict[str, Any]:
    """Build routing rules that tell AI what to load for common tasks."""
    context = _context(project)
    paths = bundle_artifact_paths(context)
    source_archive_manifest = context.json_complete_dir / (
        context.project_slug + SOURCE_ARCHIVE_MANIFEST_SUFFIX
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "bundle_kind": BUNDLE_KIND,
        "generator": {
            "name": GENERATOR_NAME,
            "version": GENERATOR_VERSION,
        },
        "generated_at_utc": _utc_now(),
        "handoff_trust": build_handoff_trust_envelope(context),
        "project": {
            "project_slug": context.project_slug,
            "active_project_id": context.active_project_id,
            "active_project_root_fingerprint": (
                context.active_project_root_fingerprint
            ),
            "project_root_marker": "<PROJECT_ROOT>",
            "evidence_root_relative": "show_project_to_AI",
            "json_complete_relative": "show_project_to_AI/second_prompt_files",
        },
        "artifact_paths": {
            "ai_briefing_json": artifact_logical_posix_path(paths.ai_briefing_json, context),
            "routing_manifest_json": artifact_logical_posix_path(paths.routing_manifest_json, context),
            "bundle_manifest_json": artifact_logical_posix_path(paths.bundle_manifest_json, context),
            "file_manifest_json": artifact_logical_posix_path(paths.file_manifest_json, context),
            "patch_safety_routes_json": artifact_logical_posix_path(paths.patch_safety_routes_json, context),
            "exclusion_rules_json": artifact_logical_posix_path(paths.exclusion_rules_json, context),
            "validation_state_json": artifact_logical_posix_path(paths.validation_state_json, context),
            "source_archive_manifest_json": artifact_logical_posix_path(
                source_archive_manifest,
                context,
            ),
        },
        "loading_policy": {
            "always_read": ["ai_briefing_json", "routing_manifest_json"],
            "read_for_routing": ["bundle_manifest_json", "file_manifest_json"],
            "read_for_subsystem_edit": ["patch_safety_routes_json", "file_manifest_json", "source_archive_manifest_json"],
            "read_for_exclusion_audit": [
                "exclusion_rules_json",
                "file_manifest_json",
                "source_archive_manifest_json",
            ],
            "read_for_handoff_validation": [
                "validation_state_json",
                "bundle_manifest_json",
                "source_archive_manifest_json",
            ],
            "read_for_debugging": ["runtime_trace_summary", "warning_index"],
            "read_only_on_request": ["runtime_trace_raw", "large full indexes"],
        },
        "task_routes": {
            "general_project_understanding": _route(
                "general_project_understanding",
                "Understand project architecture without editing.",
                ["collector_info", "collector_scope", "module_summary_index", "entry_points_detail", "limitations", "warning_index"],
                ["entry points", "README", "main modules"],
                ["No validation required unless changing files."],
            ),
            "gui_tab_change": _route(
                "gui_tab_change",
                "Change a GUI tab, button, callback, or visible workflow.",
                ["widget_registry", "widget_summary", "ui_action_index", "widget_ui_action_bridge", "boundary_index"],
                ["tab registration", "button callback", "QWidget", "QPushButton", "clicked.connect"],
                ["py_compile touched files", "launch GUI smoke check when available"],
            ),
            "project_structure_map_update": _route(
                "project_structure_map_update",
                "Update Project Structure Map / Run Collector / evidence-generation behavior.",
                ["entry_points_detail", "call_edges", "persistence_io_index", "change_impact_index", "web_ai_file_responsibility_index"],
                ["CollectorRunnerWindow", "Run Collector", "run_collector", "bundle_orchestrator", "output_paths"],
                ["py_compile changed files", "run context bundle CLI", "verify dynamic output path"],
                [
                    "exclusion_rules_json",
                    "source_archive_manifest_json",
                    "validation_state_json",
                ],
            ),
            "exclusion_policy_audit": _route(
                "exclusion_policy_audit",
                "Audit project exclusion rules, omitted paths, and archive completeness.",
                [
                    "collector_scope",
                    "persistence_io_index",
                    "web_ai_file_responsibility_index",
                    "limitations",
                ],
                [
                    "exclusion rules",
                    "excluded paths",
                    "missing file",
                    "source archive manifest",
                ],
                [
                    "verify exclusion rule normalization",
                    "verify source archive manifest coverage",
                    "confirm excluded paths are intentional",
                ],
                [
                    "exclusion_rules_json",
                    "source_archive_manifest_json",
                    "validation_state_json",
                ],
            ),
            "runtime_bug_debugging": _route(
                "runtime_bug_debugging",
                "Debug runtime errors or child-process failures.",
                ["runtime_trace_summary", "runtime_scenario_index", "runtime_call_stack_index", "warning_index"],
                ["traceback", "QProcess", "runtime runner", "collector child"],
                ["reproduce failing command", "py_compile touched files"],
            ),
            "patch_delivery_update": _route(
                "patch_delivery_update",
                "Update patch generation, install, or validation delivery behavior.",
                ["persistence_io_index", "boundary_index", "change_impact_index", "web_ai_test_protection_index"],
                ["patch", "install", "validation", "KANDA_FREEZE_HINT"],
                ["patch contract validation", "py_compile touched files"],
            ),
            "freeze_workflow_update": _route(
                "freeze_workflow_update",
                "Update freeze-after-write, freeze memory, or confirmation-gate logic.",
                ["boundary_index", "persistence_io_index", "change_impact_index", "warning_index"],
                ["freeze", "Confirm and Write", "frozen_features_memory", "freeze_hint_intake"],
                ["freeze workflow validation", "py_compile touched files"],
            ),
        },
        "fallback_route": {
            "read": [
                "ai_briefing_json",
                "routing_manifest_json",
                "file_manifest_json",
                "source_archive_manifest_json",
            ],
            "then": "Search exact source files by symbol or task term before editing.",
        },
    }


def write_routing_manifest_json(project: str | Path | ProjectContext) -> Path:
    """Write <project_slug>__routing_manifest.json for one project."""
    context = _context(project)
    paths = bundle_artifact_paths(context)
    payload = build_routing_manifest_payload(context)
    return write_json_atomic(paths.routing_manifest_json, payload)
