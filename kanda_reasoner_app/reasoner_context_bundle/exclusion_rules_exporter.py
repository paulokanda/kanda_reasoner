"""Export active project exclusion rules as a companion JSON artifact."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from .exclusion_engine import decide_path_exclusion
from .exclusion_provider import load_bundle_exclusion_rules
from .json_writer import write_json_atomic
from .output_paths import bundle_artifact_paths
from .project_context import resolve_project_context
from .schema_models import ExclusionRules, ProjectContext

__all__ = [
    "build_exclusion_rules_payload",
    "write_exclusion_rules_json",
]

SCHEMA_VERSION = 1
BUNDLE_KIND = "exclusion_rules"
GENERATOR_NAME = "reasoner_context_bundle.exclusion_rules_exporter"
GENERATOR_VERSION = "1.0.0"

_SAMPLE_PATHS = (
    "<PRODUCT_PACKAGE>/example.py",
    "project_analysis_evidence/json_complete/example.json",
    "_project" + "_reference/example.md",
    "tests/test_example.py",
    "temp/example.py",
    "example.log",
)


def _context(project: str | Path | ProjectContext) -> ProjectContext:
    if isinstance(project, ProjectContext):
        return project
    return resolve_project_context(project)


def _rules_dict(rules: ExclusionRules) -> dict[str, list[str]]:
    return {
        "folders": list(rules.folders),
        "files": list(rules.files),
        "extensions": list(rules.extensions),
    }


def _decision_examples(context: ProjectContext, rules: ExclusionRules) -> list[dict[str, Any]]:
    examples: list[dict[str, Any]] = []
    for rel_path in _SAMPLE_PATHS:
        decision = decide_path_exclusion(rel_path, context, rules)
        examples.append(decision.as_dict())
    return examples


def build_exclusion_rules_payload(
    project: str | Path | ProjectContext,
) -> dict[str, Any]:
    """Return the JSON payload for active project exclusion rules."""
    context = _context(project)
    rules = load_bundle_exclusion_rules(context)
    return {
        "schema_version": SCHEMA_VERSION,
        "bundle_kind": BUNDLE_KIND,
        "generator": {
            "name": GENERATOR_NAME,
            "version": GENERATOR_VERSION,
        },
        "generated_at_utc": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "project": {
            "project_slug": context.project_slug,
            "project_root_marker": "<PROJECT_ROOT>",
            "evidence_root_relative": "project_analysis_evidence",
            "json_complete_relative": "project_analysis_evidence/json_complete",
        },
        "source": {
            "kind": "central_project_exclusion_policy",
            "function": rules.source,
            "contract": "read_only_adapter",
        },
        "rules": _rules_dict(rules),
        "normalization": {
            "case_sensitive": False,
            "path_separator": "/",
            "windows_backslash_supported": True,
            "trailing_slash_equivalent": True,
        },
        "decision_examples": _decision_examples(context, rules),
    }


def write_exclusion_rules_json(project: str | Path | ProjectContext) -> Path:
    """Write <project_slug>__exclusion_rules.json for one project."""
    context = _context(project)
    paths = bundle_artifact_paths(context)
    payload = build_exclusion_rules_payload(context)
    return write_json_atomic(paths.exclusion_rules_json, payload)
