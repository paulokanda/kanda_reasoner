# project-path: kanda_reasoner_app/reasoner_engine/project_profile_help/inference.py
"""Support V10 project reasoning and evidence handling."""

from __future__ import annotations

from typing import Any

from .built_in_profiles import (
    ARCHITECTURE_HEAVY_PYTHON_PROJECT_PROFILE,
    EEG_PROJECT_PROFILE,
    GENERIC_PYTHON_PROJECT_PROFILE,
    QT_PYTHON_PROJECT_PROFILE,
)
from .profile_types import ProjectProfile
from .registry import get_project_profile


def infer_project_profile_name_from_metadata(
    project_root: str = "",
    project_summary: dict[str, Any] | None = None,
    packaging_metadata: dict[str, Any] | None = None,
    documentation_intent: dict[str, Any] | None = None,
) -> str:
    """Support infer project profile name from metadata behavior.
    
    Parameters
    ----------
    project_root : str, optional
        The project root path.
    project_summary : dict[str, Any] | None, optional
        The optional project summary value.
    packaging_metadata : dict[str, Any] | None, optional
        The optional packaging metadata value.
    documentation_intent : dict[str, Any] | None, optional
        The optional documentation intent value.
    
    Returns
    -------
    str
        The string result.
    """
    
    summary = project_summary if isinstance(project_summary, dict) else {}
    packaging = packaging_metadata if isinstance(packaging_metadata, dict) else {}
    documentation = (
        documentation_intent if isinstance(documentation_intent, dict) else {}
    )

    root_text = str(
        project_root or summary.get("project_root", "")
    ).replace("\\", "/").lower()

    if "eeg_kernel_ai_neural_data_analysis" in root_text:
        return EEG_PROJECT_PROFILE.name

    qt_signal_terms = (
        "pyside6",
        "pyside2",
        "pyqt6",
        "pyqt5",
        "qapplication",
        "qwidget",
        "signal-slot",
        "signal slot",
        ".ui",
    )

    qt_text_parts: list[str] = []

    for key in ("declared_dependencies", "package_manager_signals"):
        values = packaging.get(key, [])
        if isinstance(values, list):
            qt_text_parts.extend(
                str(value).strip()
                for value in values
                if str(value).strip()
            )

    declared_optional_dependencies = packaging.get(
        "declared_optional_dependencies", {}
    )
    if isinstance(declared_optional_dependencies, dict):
        for group_name, values in declared_optional_dependencies.items():
            qt_text_parts.append(str(group_name).strip())
            if isinstance(values, list):
                qt_text_parts.extend(
                    str(value).strip()
                    for value in values
                    if str(value).strip()
                )

    declared_entrypoints = packaging.get("declared_entrypoints", [])
    if isinstance(declared_entrypoints, list):
        for item in declared_entrypoints:
            if not isinstance(item, dict):
                continue
            qt_text_parts.extend(
                str(item.get(key, "")).strip()
                for key in ("group", "name", "target")
                if str(item.get(key, "")).strip()
            )

    for key in (
        "external_integrations",
        "run_instructions",
        "architecture_terms",
        "named_features",
    ):
        values = documentation.get(key, [])
        if isinstance(values, list):
            qt_text_parts.extend(
                str(value).strip()
                for value in values
                if str(value).strip()
            )

    qt_blob = " ".join(part.lower() for part in qt_text_parts if part)
    if any(term in qt_blob for term in qt_signal_terms):
        return QT_PYTHON_PROJECT_PROFILE.name

    architecture_signal_groups = {
        "service": ("service", "services"),
        "controller": ("controller", "controllers"),
        "repository": ("repository", "repositories"),
        "layered": (
            "layered architecture",
            "application layer",
            "domain layer",
            "infrastructure layer",
        ),
        "use_case": ("use case", "use cases", "use_case", "use-case"),
        "orchestrator": ("orchestrator", "orchestration"),
        "adapter": ("adapter", "adapters"),
        "factory": ("factory", "factories"),
        "plugin": ("plugin registry", "plugin registries"),
        "event_handler": ("event handler", "event-handler"),
    }

    architecture_text_parts: list[str] = []

    project_purpose_summary = documentation.get("project_purpose_summary", "")
    if isinstance(project_purpose_summary, str) and project_purpose_summary.strip():
        architecture_text_parts.append(project_purpose_summary.strip())

    for key in (
        "declared_workflows",
        "architecture_terms",
        "named_features",
        "run_instructions",
        "external_integrations",
    ):
        values = documentation.get(key, [])
        if isinstance(values, list):
            architecture_text_parts.extend(
                str(value).strip()
                for value in values
                if str(value).strip()
            )

    if isinstance(declared_entrypoints, list):
        for item in declared_entrypoints:
            if not isinstance(item, dict):
                continue
            architecture_text_parts.extend(
                str(item.get(key, "")).strip()
                for key in ("group", "name", "target")
                if str(item.get(key, "")).strip()
            )

    architecture_blob = " ".join(
        part.lower() for part in architecture_text_parts if part
    )

    matched_architecture_groups = sum(
        1
        for variants in architecture_signal_groups.values()
        if any(term in architecture_blob for term in variants)
    )

    if matched_architecture_groups >= 3:
        return ARCHITECTURE_HEAVY_PYTHON_PROJECT_PROFILE.name

    return GENERIC_PYTHON_PROJECT_PROFILE.name


def infer_project_profile(
    project_root: str = "",
    project_summary: dict[str, Any] | None = None,
    packaging_metadata: dict[str, Any] | None = None,
    documentation_intent: dict[str, Any] | None = None,
) -> ProjectProfile:
    """Support infer project profile behavior.
    
    Parameters
    ----------
    project_root : str, optional
        The project root path.
    project_summary : dict[str, Any] | None, optional
        The optional project summary value.
    packaging_metadata : dict[str, Any] | None, optional
        The optional packaging metadata value.
    documentation_intent : dict[str, Any] | None, optional
        The optional documentation intent value.
    
    Returns
    -------
    ProjectProfile
        The project profile result.
    """
    
    profile_name = infer_project_profile_name_from_metadata(
        project_root=project_root,
        project_summary=project_summary,
        packaging_metadata=packaging_metadata,
        documentation_intent=documentation_intent,
    )
    return get_project_profile(profile_name)


__all__ = [
    "infer_project_profile_name_from_metadata",
    "infer_project_profile",
]
