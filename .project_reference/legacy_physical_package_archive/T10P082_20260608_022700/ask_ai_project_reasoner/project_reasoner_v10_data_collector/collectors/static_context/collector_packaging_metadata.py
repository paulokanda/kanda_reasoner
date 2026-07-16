"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from kanda_reasoner_app.reasoner_context_collector.collector_config import CollectorConfig

from ...parsers import parse_packaging_metadata


def _empty_packaging_metadata(enabled: bool) -> dict[str, Any]:
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
