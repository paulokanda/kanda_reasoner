# project-path: kanda_reasoner_app/reasoner_context_collector/collector_output.py
"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from .collector_config import CollectorConfig


def build_collector_info(root: Path) -> dict:
    """Build a collector info.
    
    Parameters
    ----------
    root : Path
        The root path.
    
    Returns
    -------
    dict
        The mapped values.
    """
    
    return {
        "collector_version": "1.8",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "root_path": str(root),
    }


def build_collection_config(config: CollectorConfig) -> dict:
    """Build a collection config.
    
    Parameters
    ----------
    config : CollectorConfig
        The configuration data.
    
    Returns
    -------
    dict
        The mapped values.
    """
    
    return {
        "excluded_dirs": config.excluded_dirs,
        "include_tests": config.include_tests,
        "include_vendor_code": config.include_vendor_code,
        "max_snippet_lines": config.max_snippet_lines,
        "max_docstring_length": config.max_docstring_length,
        "enable_edit_ready_source_index": config.enable_edit_ready_source_index,
        "include_full_source_in_file_index": config.include_full_source_in_file_index,
        "max_anchor_context_lines": config.max_anchor_context_lines,
        "max_source_excerpt_lines": config.max_source_excerpt_lines,
        "max_full_source_chars": config.max_full_source_chars,
        "enable_packaging_metadata": config.enable_packaging_metadata,
        "enable_documentation_intent": config.enable_documentation_intent,
        "max_packaging_dependencies": config.max_packaging_dependencies,
        "max_doc_evidence_snippets": config.max_doc_evidence_snippets,
        "max_doc_excerpt_chars": config.max_doc_excerpt_chars,
        "documentation_glob_patterns": list(config.documentation_glob_patterns),
        "packaging_file_patterns": list(config.packaging_file_patterns),
    }


def build_collector_scope() -> dict:
    """Build a collector scope.
    
    Returns
    -------
    dict
        The mapped values.
    """
    
    return {
        "domain_scope": "kanda_reasoner_app",
        "runtime_scope": "generic_reusable",
        "is_project_agnostic": True,
        "runtime_scenario_filter_mode": "canonical_domain_only",
    }


def build_limitations_section(
    *,
    files_corpus: dict[str, Any] | None = None,
    local_symbol_index: dict[str, Any] | None = None,
    packaging_metadata: dict[str, Any] | None = None,
    documentation_intent: dict[str, Any] | None = None,
    parse_errors: list[dict[str, Any]] | None = None,
    runtime_trace_present: bool = False,
    runtime_scenario_present: bool = False,
) -> dict[str, Any]:
    """Build a limitations section.
    
    Parameters
    ----------
    files_corpus : dict[str, Any] | None, optional
        The optional files corpus value.
    local_symbol_index : dict[str, Any] | None, optional
        The optional local symbol index value.
    packaging_metadata : dict[str, Any] | None, optional
        The optional packaging metadata value.
    documentation_intent : dict[str, Any] | None, optional
        The optional documentation intent value.
    parse_errors : list[dict[str, Any]] | None, optional
        The optional parse errors value.
    runtime_trace_present : bool, optional
        The optional runtime trace present value.
    runtime_scenario_present : bool, optional
        The optional runtime scenario present value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    files_corpus = files_corpus if isinstance(files_corpus, dict) else {}
    local_symbol_index = (
        local_symbol_index if isinstance(local_symbol_index, dict) else {}
    )
    packaging_metadata = (
        packaging_metadata if isinstance(packaging_metadata, dict) else {}
    )
    documentation_intent = (
        documentation_intent if isinstance(documentation_intent, dict) else {}
    )
    parse_errors = parse_errors if isinstance(parse_errors, list) else []

    packaging_warnings = list(packaging_metadata.get("packaging_parse_warnings", []))
    packaging_confidence = str(
        packaging_metadata.get("packaging_confidence", "unknown")
    ).strip() or "unknown"
    documentation_warnings = list(
        documentation_intent.get("documentation_parse_warnings", [])
    )
    documentation_confidence = str(
        documentation_intent.get("project_purpose_summary_confidence", "unknown")
    ).strip() or "unknown"

    missing_files = list(files_corpus.get("missing_from_files_corpus", []))
    duplicate_files = list(files_corpus.get("duplicate_files", []))
    unexpected_files = list(files_corpus.get("unexpected_in_files_corpus", []))

    static_analysis_blind_spots = [
        "Dynamic imports and reflection may hide real call targets.",
        "Runtime-only signal connections and state transitions are incomplete without runtime traces.",
        "Generated files, vendor bundles, and mis-decoded packaging docs can lower confidence in summaries.",
        "Test intent and runtime behavior cannot be inferred completely from static analysis alone.",
    ]

    return {
        "files_corpus": {
            "walked_python_file_count": int(files_corpus.get("walked_python_file_count", 0)),
            "emitted_file_count": int(files_corpus.get("emitted_file_count", 0)),
            "parse_error_file_count": int(files_corpus.get("parse_error_file_count", 0)),
            "matches_expected_after_parse_errors": bool(
                files_corpus.get("matches_expected_after_parse_errors", False)
            ),
            "missing_from_files_corpus": missing_files,
            "unexpected_in_files_corpus": unexpected_files,
            "duplicate_files": duplicate_files,
        },
        "local_symbol_index": {
            "mismatch_count": int(local_symbol_index.get("mismatch_count", 0)),
            "mismatch_examples": list(local_symbol_index.get("mismatch_examples", [])),
        },
        "packaging_metadata": {
            "confidence": packaging_confidence,
            "warning_count": len(packaging_warnings),
            "warnings": packaging_warnings,
        },
        "documentation_intent": {
            "confidence": documentation_confidence,
            "warning_count": len(documentation_warnings),
            "warnings": documentation_warnings,
        },
        "parse_failures": {
            "count": len(parse_errors),
            "files": [str(item.get("file", "")).strip() for item in parse_errors if str(item.get("file", "")).strip()],
        },
        "runtime_evidence": {
            "runtime_trace_present": bool(runtime_trace_present),
            "runtime_scenario_present": bool(runtime_scenario_present),
            "runtime_evidence_absent": not bool(runtime_trace_present or runtime_scenario_present),
        },
        "static_analysis_blind_spots": static_analysis_blind_spots,
    }
