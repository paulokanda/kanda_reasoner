# project-path: kanda_reasoner_app/reasoner_engine/project_profile_help/built_in_profiles.py
"""Support V10 project reasoning and evidence handling."""

from __future__ import annotations

from .profile_types import ProjectProfile


GENERIC_FEATURE_FLAGS = {
    "use_profile_path_boosts": False,
    "use_profile_symbol_boosts": False,
    "use_profile_question_aliases": False,
    "use_profile_chain_aliases": False,
}

GENERIC_PROJECT_PROFILE = ProjectProfile(
    name="generic",
    description="Generic project profile with no project-specific ranking terms.",
    domain_scope="generic",
    path_priority_terms=(),
    path_penalty_terms=(),
    owner_path_boosts={},
    symbol_priority_terms=(),
    symbol_penalty_terms=(),
    symbol_boosts={},
    question_aliases={},
    chain_aliases={},
    feature_flags=dict(GENERIC_FEATURE_FLAGS),
    notes=(
        "Default fallback profile.",
        "Must work for any selected project.",
        "Contains no EEG-specific assumptions.",
    ),
)

GENERIC_PYTHON_PROJECT_PROFILE = ProjectProfile(
    name="generic_python",
    description=(
        "Passive generic Python profile placeholder for ordinary Python projects. "
        "It introduces a canonical Python-family profile name without changing "
        "retrieval behavior yet."
    ),
    domain_scope="python",
    path_priority_terms=(),
    path_penalty_terms=(),
    owner_path_boosts={},
    symbol_priority_terms=(),
    symbol_penalty_terms=(),
    symbol_boosts={},
    question_aliases={},
    chain_aliases={},
    feature_flags=dict(GENERIC_FEATURE_FLAGS),
    notes=(
        "Passive placeholder for step 27.",
        "Keeps current behavior unchanged.",
        "Will be enriched in later profile steps.",
    ),
)

ARCHITECTURE_HEAVY_PYTHON_PROJECT_PROFILE = ProjectProfile(
    name="architecture_heavy_python",
    description=(
        "Passive profile placeholder for layered or architecture-heavy Python projects. "
        "It introduces a canonical profile name for service-controller-repository or "
        "multi-boundary codebases without changing retrieval behavior yet."
    ),
    domain_scope="python",
    path_priority_terms=(),
    path_penalty_terms=(),
    owner_path_boosts={},
    symbol_priority_terms=(),
    symbol_penalty_terms=(),
    symbol_boosts={},
    question_aliases={},
    chain_aliases={},
    feature_flags=dict(GENERIC_FEATURE_FLAGS),
    notes=(
        "Passive placeholder for step 27.",
        "Represents layered Python repositories with strong architectural boundaries.",
        "Will be enriched in later steps without changing the schema contract.",
    ),
)

QT_PYTHON_PROJECT_PROFILE = ProjectProfile(
    name="qt_python",
    description=(
        "Passive profile placeholder for Qt-oriented Python projects. "
        "It introduces a canonical profile name for PySide and PyQt codebases "
        "without changing retrieval behavior yet."
    ),
    domain_scope="python_qt",
    path_priority_terms=(),
    path_penalty_terms=(),
    owner_path_boosts={},
    symbol_priority_terms=(),
    symbol_penalty_terms=(),
    symbol_boosts={},
    question_aliases={},
    chain_aliases={},
    feature_flags=dict(GENERIC_FEATURE_FLAGS),
    notes=(
        "Passive placeholder for step 27.",
        "Represents PySide or PyQt application families.",
        "Will be enriched in later steps without changing current behavior.",
    ),
)

EEG_PROJECT_PROFILE = ProjectProfile(
    name="eeg_kernel_ai_neural_data_analysis",
    description=(
        "Optional profile placeholder for the EEG project. "
        "It preserves current project-specific vocabulary so those terms can "
        "be migrated out of the generic retriever core in later steps."
    ),
    domain_scope="eeg",
    path_priority_terms=(
        "shell/viewer",
        "shell/navbar",
        "shell/notebook",
        "shell/timeline",
        "plugins/eeg_traces",
        "plugins/amplitude_map",
        "core/snapshot",
    ),
    path_penalty_terms=(),
    owner_path_boosts={
        "shell/viewer": 0,
        "shell/navbar": 0,
        "shell/notebook": 0,
        "shell/timeline": 0,
        "plugins/eeg_traces": 0,
        "plugins/amplitude_map": 0,
        "core/snapshot": 0,
    },
    symbol_priority_terms=(
        "NotebookBuilder",
        "NavBarBuilder",
        "build_top",
        "build_upper",
        "attach_timeline_to_tab",
        "TimelineManager",
        "time_clicked",
        "window_moved",
        "on_timeline_clicked",
        "on_window_moved",
        "EEGMainWindowBuilder",
        "build_and_show",
        "EEGAmplitudeMap",
        "TopoRenderer",
        "plot_topomap",
        "mne.viz.plot_topomap",
        "amplitude_map",
        "reset_to_initial_eeg_state",
        "unload_content",
        "cleanup",
        "snapshot",
        "close",
    ),
    symbol_penalty_terms=(),
    symbol_boosts={
        "NotebookBuilder": 0,
        "NavBarBuilder": 0,
        "attach_timeline_to_tab": 0,
        "TimelineManager": 0,
        "EEGAmplitudeMap": 0,
        "TopoRenderer": 0,
    },
    question_aliases={
        "timeline": (
            "timeline chain",
            "timeline wiring",
            "timeline attachment",
            "timeline manager",
            "timeline widget",
            "attach_timeline_to_tab",
            "time_clicked",
            "window_moved",
            "on_timeline_clicked",
            "on_window_moved",
        ),
        "timeline_symbol_terms": (
            "attach_timeline_to_tab",
            "timelinemanager",
            "time_clicked",
            "window_moved",
            "on_timeline_clicked",
            "on_window_moved",
        ),
        "timeline_owner_paths": (
            "plugins/eeg_traces",
            "shell/timeline",
        ),
        "top_navigation": (
            "top navigation",
            "upper navigation",
            "superior tab",
            "top tab",
            "navbar",
            "navigation bars",
            "notebook tabs",
        ),
        "navbar_builder_terms": (
            "navbarbuilder",
            "nav bar builder",
            "build_top",
            "build_upper",
        ),
        "notebook_builder_terms": (
            "notebookbuilder",
            "notebook builder",
            "notebook tabs",
            "nb_builder.build",
            "addtab",
            "currentchanged.connect",
        ),
        "builder_callsite_markers": (
            "build_and_show",
            "build_top",
            "build_upper",
            "notebookbuilder",
            "nb_builder.build",
            "addtab",
            "currentchanged.connect",
        ),
        "topomap": (
            "topomap",
            "amplitude map",
            "topographic map",
            "topography",
            "toporenderer",
            "topomap renderer",
            "amplitude renderer",
            "mne.viz.plot_topomap",
            "viz.plot_topomap",
        ),
        "topomap_explanation": (
            "topomap explanation",
            "explain topomap",
            "explain amplitude map",
            "how topomap works",
            "how amplitude map works",
            "topomap rendering",
            "amplitude map rendering",
            "topographic rendering",
        ),
        "topomap_implementation": (
            "topomap implementation",
            "implement topomap",
            "implements topomap",
            "implemented topomap",
            "which code implements topomap",
            "which modules implement topomap",
            "which modules participate in topomap",
            "amplitude map implementation",
            "implement amplitude map",
            "which code implements amplitude map",
        ),
        "topomap_symbol_terms": (
            "toporenderer",
            "eegamplitudemap",
            "plot_topomap",
            "mne.viz.plot_topomap",
            "viz.plot_topomap",
            "amplitude_map",
        ),
        "topomap_owner_paths": (
            "plugins/amplitude_map",
            "renderer/topomap",
            "shell/viewer",
        ),
        "reset_cleanup": (
            "reset chain",
            "cleanup chain",
            "snapshot reset",
            "close cleanup",
            "reset / cleanup",
            "reset cleanup",
            "session snapshot",
            "pipeline reset",
            "reset flow",
            "cleanup flow",
        ),
        "reset_cleanup_symbol_terms": (
            "reset_to_initial_eeg_state",
            "unload_content",
            "cleanup_resources",
            "cleanup",
            "snapshot",
            "close",
        ),
        "reset_cleanup_owner_paths": (
            "core/snapshot",
            "shell/viewer",
            "plugins/amplitude_map",
        ),
    },
    chain_aliases={
        "startup_chain": (
            "startup chain",
            "main window startup",
            "launch chain",
        ),
        "timeline_chain": (
            "timeline chain",
            "timeline wiring chain",
            "timeline attachment chain",
        ),
        "topomap_chain": (
            "topomap chain",
            "amplitude map chain",
        ),
        "reset_chain": (
            "reset chain",
            "cleanup chain",
        ),
    },
    feature_flags={
        "use_profile_path_boosts": False,
        "use_profile_symbol_boosts": False,
        "use_profile_question_aliases": True,
        "use_profile_chain_aliases": False,
    },
    notes=(
        "Placeholder only in this step.",
        "Current boost values are intentionally zero to avoid behavior change.",
        "Later steps may migrate EEG-specific retriever heuristics into this profile.",
    ),
)

__all__ = [
    "GENERIC_PROJECT_PROFILE",
    "GENERIC_PYTHON_PROJECT_PROFILE",
    "ARCHITECTURE_HEAVY_PYTHON_PROJECT_PROFILE",
    "QT_PYTHON_PROJECT_PROFILE",
    "EEG_PROJECT_PROFILE",
]
