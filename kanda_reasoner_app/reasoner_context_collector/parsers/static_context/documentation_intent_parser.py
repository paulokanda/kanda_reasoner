# project-path: kanda_reasoner_app/reasoner_context_collector/parsers/static_context/documentation_intent_parser.py
"""Public facade for documentation intent parsing."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ._documentation_intent_extractors import (
    _extract_architecture_terms,
    _extract_external_integrations,
    _extract_first_meaningful_paragraph,
    _extract_heading_lines,
    _extract_named_features,
    _extract_run_instructions,
)
from ._documentation_intent_result_helpers import (
    _dedupe_keep_order,
    _merge_list_field,
    _new_result,
    _append_evidence,
    _append_warning,
)
from ._documentation_intent_scan_helpers import (
    _doc_rank,
    _discover_doc_files,
    _extract_best_purpose_summary,
    _looks_like_cache_or_generated_doc,
    _looks_like_vendor_or_font_doc,
    _normalize_rel_path,
    _read_text_best_effort,
)

DEFAULT_DOCUMENTATION_GLOB_PATTERNS: tuple[str, ...] = (
    "README*",
    "docs/**/*.md",
    "docs/**/*.rst",
    "**/*ADR*.md",
    "**/*architecture*.md",
    "mkdocs.yml",
    "conf.py",
)

__all__ = [
    "DEFAULT_DOCUMENTATION_GLOB_PATTERNS",
    "parse_documentation_intent",
]


def parse_documentation_intent(
    project_root: Path,
    glob_patterns: tuple[str, ...] = DEFAULT_DOCUMENTATION_GLOB_PATTERNS,
    max_evidence_snippets: int = 40,
    max_excerpt_chars: int = 400,
) -> dict[str, Any]:
    """Parse the documentation intent.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    glob_patterns : tuple[str, ...], optional
        The optional glob patterns value.
    max_evidence_snippets : int, optional
        The optional max evidence snippets value.
    max_excerpt_chars : int, optional
        The optional max excerpt chars value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    result = _new_result()
    root = Path(project_root).expanduser().resolve()

    doc_files = _discover_doc_files(root, glob_patterns)
    summary_candidates: list[tuple[int, str, str]] = []

    for path in doc_files:
        source_file = _normalize_rel_path(path, root)
        text, error = _read_text_best_effort(path)
        if error is not None:
            _append_evidence(result, source_file, "parse_error", error, max_excerpt_chars)
            _append_warning(result, source_file, error)
            continue

        result["documentation_files_found"].append(source_file)

        if _looks_like_cache_or_generated_doc(path, text):
            _append_warning(result, source_file, "ignored generated or cache documentation")
            continue
        if _looks_like_vendor_or_font_doc(text):
            _append_warning(result, source_file, "ignored vendor or font documentation")
            continue

        first_paragraph = _extract_first_meaningful_paragraph(text)
        if first_paragraph:
            summary_candidates.append((_doc_rank(path, text), source_file, first_paragraph))

        headings = _extract_heading_lines(text)
        run_instructions = _extract_run_instructions(text)
        named_features = _extract_named_features(headings)
        external_integrations = _extract_external_integrations(text)
        architecture_terms = _extract_architecture_terms(headings, text)

        _merge_list_field(
            result,
            "declared_workflows",
            headings[:max_evidence_snippets],
            source_file,
            max_evidence_snippets,
            max_excerpt_chars,
        )
        _merge_list_field(
            result,
            "run_instructions",
            run_instructions[:max_evidence_snippets],
            source_file,
            max_evidence_snippets,
            max_excerpt_chars,
        )
        _merge_list_field(
            result,
            "named_features",
            named_features[:max_evidence_snippets],
            source_file,
            max_evidence_snippets,
            max_excerpt_chars,
        )
        _merge_list_field(
            result,
            "external_integrations",
            external_integrations[:max_evidence_snippets],
            source_file,
            max_evidence_snippets,
            max_excerpt_chars,
        )
        _merge_list_field(
            result,
            "architecture_terms",
            architecture_terms[:max_evidence_snippets],
            source_file,
            max_evidence_snippets,
            max_excerpt_chars,
        )

    result["documentation_files_found"] = _dedupe_keep_order(result["documentation_files_found"])
    result["documentation_parse_warnings"] = _dedupe_keep_order(result["documentation_parse_warnings"])
    summary, confidence = _extract_best_purpose_summary(summary_candidates)
    result["project_purpose_summary"] = summary
    result["project_purpose_summary_confidence"] = confidence
    return result
