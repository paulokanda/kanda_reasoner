# project-path: kanda_reasoner_app/reasoner_context_collector/collectors/static_context/collector_packaging_metadata.py
"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from kanda_reasoner_app.reasoner_context_collector.collector_config import CollectorConfig

from ...parsers import parse_packaging_metadata


def _empty_packaging_metadata(enabled: bool) -> dict[str, Any]:
    """Support empty packaging metadata behavior.
    
    Parameters
    ----------
    enabled : bool
        The enabled value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    return {
        "enabled": enabled,
        "project_name": "",
        "declared_version": "",
        "build_backend": "",
        "package_manager_signals": [],
        "declared_dependencies": [],
        "declared_optional_dependencies": {},
        "declared_entrypoints": [],
        "declared_tooling": {},
        "packaging_files_found": [],
        "packaging_evidence": [],
        "packaging_parse_warnings": [],
        "packaging_confidence": "unknown",
    }


def collect_packaging_metadata(
    project_root: Path,
    config: CollectorConfig,
) -> dict[str, Any]:
    """Support collect packaging metadata behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    config : CollectorConfig
        The configuration data.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    if not config.enable_packaging_metadata:
        return _empty_packaging_metadata(enabled=False)

    parsed = parse_packaging_metadata(
        project_root=Path(project_root).expanduser().resolve(),
        file_patterns=config.packaging_file_patterns,
        max_dependencies=config.max_packaging_dependencies,
    )

    payload = _empty_packaging_metadata(enabled=True)
    payload.update(parsed)
    payload["enabled"] = True
    return payload
