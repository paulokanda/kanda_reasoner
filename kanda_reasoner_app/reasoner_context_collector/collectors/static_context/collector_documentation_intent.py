"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ...collector_config import CollectorConfig
from ...parsers import parse_documentation_intent


def _empty_documentation_intent(enabled: bool) -> dict[str, Any]:
    return {
        "enabled": enabled,
        "project_purpose_summary": "",
        "declared_workflows": [],
        "architecture_terms": [],
        "run_instructions": [],
        "named_features": [],
        "external_integrations": [],
        "documentation_files_found": [],
        "documentation_evidence": [],
    }


def collect_documentation_intent(
    project_root: Path,
    config: CollectorConfig,
) -> dict[str, Any]:
    if not config.enable_documentation_intent:
        return _empty_documentation_intent(enabled=False)

    parsed = parse_documentation_intent(
        project_root=Path(project_root).expanduser().resolve(),
        glob_patterns=config.documentation_glob_patterns,
        max_evidence_snippets=config.max_doc_evidence_snippets,
        max_excerpt_chars=config.max_doc_excerpt_chars,
    )

    payload = _empty_documentation_intent(enabled=True)
    payload.update(parsed)
    payload["enabled"] = True
    return payload
