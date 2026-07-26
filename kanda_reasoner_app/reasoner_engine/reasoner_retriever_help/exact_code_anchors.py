# project-path: kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/exact_code_anchors.py
"""Exact code-anchor helpers for Project Q&A retrieval.

This module keeps filename and function anchoring deterministic for code
questions. It has no file-system side effects and never reads generated
evidence as source truth.
"""
from __future__ import annotations

import os
import re
from dataclasses import replace
from typing import Iterable

from kanda_reasoner_app.reasoner_engine.v10_models import RetrievalBundle

__all__ = [
    "extract_question_file_names",
    "extract_question_excluded_file_names",
    "extract_question_excluded_path_fragments",
    "extract_strict_requested_file_paths",
    "path_matches_strict_requested_path",
    "extract_question_symbol_names",
    "path_matches_requested_file",
    "strict_evidence_requested",
    "missing_requested_files",
    "filter_bundle_to_requested_files",
    "project_qa_run_analysis_trace_requested",
    "path_matches_project_qa_run_analysis_trace_file",
    "path_is_project_qa_run_analysis_distractor",
]


def _normalize_path(value: str) -> str:
    """Return a lowercase slash-normalized path string."""
    return str(value or "").replace("\\", "/").lower().strip()


def _base_name(value: str) -> str:
    """Return a lowercase base filename from a path-like string."""
    return os.path.basename(_normalize_path(value))


PROJECT_QA_RUN_ANALYSIS_TRACE_FILES = (
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/signal_wiring.py",
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window.py",
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/analysis_controller.py",
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/project_qa_analysis_runner.py",
)

PROJECT_QA_RUN_ANALYSIS_DISTRACTOR_PATH_FRAGMENTS = (
    "kanda_reasoner_app/reasoner_runtime_collector/runner.py",
    "kanda_reasoner_app/reasoner_context_collector/runner.py",
    "kanda_reasoner_app/reasoner_tools_shell/runner.py",
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/",
)


def project_qa_run_analysis_trace_requested(question: str) -> bool:
    """Return True for Project Q&A Run Analysis button-path questions."""
    q = str(question or "").lower()
    if "run analysis" not in q:
        return False
    has_project_qa_context = (
        "project q&a" in q
        or "project qa" in q
        or "project q and a" in q
        or "project q/a" in q
        or "local-ai json" in q
        or "canonical json" in q
    )
    if not has_project_qa_context:
        return False
    trace_terms = (
        "trace",
        "workflow",
        "button click",
        "from button",
        "button to",
        "clicked callback",
        "button path",
        "signal wiring",
        "facade method",
        "controller method",
        "command it builds",
        "runner function",
        "step by step",
        "call chain",
        "execution path",
        "main modules involved",
        "local-ai json creation",
        "local ai json creation",
        "canonical json creation",
        "json creation",
    )
    return any(term in q for term in trace_terms)


def path_matches_project_qa_run_analysis_trace_file(path: str) -> bool:
    """Return True for the owned Project Q&A Run Analysis path files."""
    normalized = _normalize_path(path)
    return any(normalized.endswith(target) for target in PROJECT_QA_RUN_ANALYSIS_TRACE_FILES)


def path_is_project_qa_run_analysis_distractor(path: str) -> bool:
    """Return True for generic runner files outside the Project Q&A path."""
    normalized = _normalize_path(path)
    return any(fragment in normalized for fragment in PROJECT_QA_RUN_ANALYSIS_DISTRACTOR_PATH_FRAGMENTS)


NEGATIVE_ANCHOR_MARKERS = (
    "do not mention",
    "do not discuss",
    "do not use",
    "do not retrieve",
    "do not retrieve or use",
    "do not retrieve/use",
    "do not include",
    "do not infer from",
    "exclude",
    "avoid",
    "never mention",
    "without mentioning",
    "without discussing",
)


def _is_negative_filename_mention(text: str, start: int) -> bool:
    """Return True when a filename appears in a local negative rule."""
    prefix = text[max(0, start - 128):start].lower()
    sentence_start = max(prefix.rfind("."), prefix.rfind("\n"), prefix.rfind(";"), prefix.rfind(":"))
    local_prefix = prefix[sentence_start + 1:] if sentence_start >= 0 else prefix
    return any(marker in local_prefix for marker in NEGATIVE_ANCHOR_MARKERS)


def extract_question_excluded_file_names(question: str) -> set[str]:
    """Extract Python filenames that appear in negative retrieval rules."""
    text = str(question or "")
    out: set[str] = set()
    for match in re.finditer(r"[A-Za-z0-9_\-]+\.py", text):
        if _is_negative_filename_mention(text, match.start()):
            name = match.group(0).lower().strip()
            if name:
                out.add(name)
    return out


def extract_question_excluded_path_fragments(question: str) -> set[str]:
    """Extract path fragments such as scripts/ from negative rules."""
    text = str(question or "")
    pattern = r"(?:[A-Za-z0-9_\-]+[\\/])+(?:[A-Za-z0-9_\-]+(?:\.py)?)?"
    out: set[str] = set()
    for match in re.finditer(pattern, text):
        if _is_negative_filename_mention(text, match.start()):
            fragment = _normalize_path(match.group(0)).strip("/")
            if fragment:
                out.add(fragment + ("/" if match.group(0).endswith(("/", "\\")) else ""))
    return out


def _path_matches_excluded_fragment(path: str, fragments: Iterable[str]) -> bool:
    """Return True when path matches a negative path fragment."""
    normalized = _normalize_path(path).strip("/")
    for fragment in fragments:
        item = _normalize_path(fragment).strip("/")
        if not item:
            continue
        if normalized == item:
            return True
        if normalized.startswith(item + "/"):
            return True
        if "/" + item + "/" in "/" + normalized + "/":
            return True
    return False




STRICT_REQUESTED_FILE_MARKERS = (
    "retrieve evidence only from this exact file:",
    "retrieve evidence only from these exact files:",
    "retrieve evidence only from this file:",
    "retrieve evidence only from these files:",
    "use evidence only from this exact file:",
    "use evidence only from these exact files:",
    "answer only from this exact file:",
    "answer only from these exact files:",
)

_STRICT_REQUEST_STOP_MARKERS = (
    "\nquestion:",
    "\nrules:",
    "\nexpected",
    "\nif ",
    "\ndo not ",
)


def _extract_marker_span(text: str, marker: str) -> str:
    """Return the bounded text span after a strict requested-file marker."""
    lower = text.lower()
    start = lower.find(marker)
    if start < 0:
        return ""
    span = text[start + len(marker):]
    lower_span = span.lower()
    stop_positions = [
        lower_span.find(stop)
        for stop in _STRICT_REQUEST_STOP_MARKERS
        if lower_span.find(stop) >= 0
    ]
    if stop_positions:
        span = span[:min(stop_positions)]
    return span


def extract_strict_requested_file_paths(question: str) -> set[str]:
    """Extract explicit allow-listed paths from strict exact-file prompts."""
    text = str(question or "")
    out: set[str] = set()
    for marker in STRICT_REQUESTED_FILE_MARKERS:
        span = _extract_marker_span(text, marker)
        if not span:
            continue
        for match in re.finditer(r"[A-Za-z0-9_./\\\-]+\.py", span):
            value = _normalize_path(match.group(0)).strip("./ ")
            if value:
                out.add(value)
    return out


def path_matches_strict_requested_path(path: str, requested_paths: Iterable[str]) -> bool:
    """Return True when path matches an explicit strict allow-list path."""
    normalized = _normalize_path(path).strip("/")
    base = _base_name(path)
    for item in requested_paths:
        wanted = _normalize_path(item).strip("/")
        if not wanted:
            continue
        if "/" not in wanted:
            if base == wanted:
                return True
            continue
        if normalized == wanted or normalized.endswith("/" + wanted):
            return True
    return False


def extract_question_file_names(question: str) -> set[str]:
    """Extract exact positive Python filenames requested in a question.

    Filenames that appear only inside negative instructions such as
    "do not mention reasoner_runtime_collector/runner.py" are exclusions,
    not retrieval anchors. Treating them as positive anchors leaks distractor
    runner files into strict evidence packs.
    """
    text = str(question or "")
    out: set[str] = set()
    for match in re.finditer(r"[A-Za-z0-9_\-]+\.py", text):
        if _is_negative_filename_mention(text, match.start()):
            continue
        name = match.group(0).lower().strip()
        if name:
            out.add(name)
    return out


def extract_question_symbol_names(question: str) -> set[str]:
    """Extract exact identifier-like names requested in a question."""
    raw = re.findall(
        r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)?",
        str(question or ""),
    )
    stop = {
        "answer",
        "call",
        "code",
        "does",
        "evidence",
        "explain",
        "file",
        "from",
        "function",
        "mode",
        "module",
        "only",
        "project",
        "question",
        "retrieved",
        "strict",
        "symbol",
        "what",
        "which",
    }
    out: set[str] = set()
    for item in raw:
        low = item.lower()
        if low in stop:
            continue
        if "_" in item or "." in item or item.endswith("Py"):
            out.add(low)
    return out


def path_matches_requested_file(path: str, requested_file_names: Iterable[str]) -> bool:
    """Return True when path belongs to an exact requested filename."""
    names = {str(name).lower() for name in requested_file_names if str(name).strip()}
    if not names:
        return False
    normalized = _normalize_path(path)
    base = _base_name(path)
    return base in names or any(normalized.endswith("/" + name) for name in names)


def strict_evidence_requested(question: str) -> bool:
    """Return True when the user asks not to infer outside evidence."""
    q = str(question or "").lower()
    markers = [
        "strict evidence",
        "use only evidence",
        "only file evidence",
        "answer only from evidence",
        "only from evidence snippets",
        "do not infer",
        "do not discuss",
        "if that file is not present",
        "if the exact file is not retrieved",
    ]
    return any(marker in q for marker in markers)


def missing_requested_files(question: str, evidence_items: Iterable[object]) -> list[str]:
    """Return requested filenames absent from retrieved file evidence."""
    requested = sorted(extract_question_file_names(question))
    if not requested:
        return []
    present_paths = [str(getattr(item, "path", "")) for item in evidence_items]
    missing: list[str] = []
    for name in requested:
        if not any(path_matches_requested_file(path, {name}) for path in present_paths):
            missing.append(name)
    return missing


def _append_reason(reason: str, marker: str) -> str:
    """Append a retrieval reason marker without duplicating it."""
    text = str(reason or "").strip()
    if marker in text:
        return text
    if not text:
        return marker
    return text + ", " + marker


def _reindex_file_items(items: Iterable[object]) -> list[object]:
    """Return file evidence with stable F-number ids after filtering."""
    out: list[object] = []
    for idx, item in enumerate(items, start=1):
        out.append(
            replace(
                item,
                evidence_id="F" + str(idx).zfill(2),
                reason=_append_reason(
                    getattr(item, "reason", ""),
                    "strict-anchored-file-filter",
                ),
            )
        )
    return out


def _reindex_symbol_items(items: Iterable[object]) -> list[object]:
    """Return symbol evidence with stable S-number ids after filtering."""
    out: list[object] = []
    for idx, item in enumerate(items, start=1):
        out.append(
            replace(
                item,
                evidence_id="S" + str(idx).zfill(2),
                reason=_append_reason(
                    getattr(item, "reason", ""),
                    "strict-anchored-symbol-filter",
                ),
            )
        )
    return out


def _reindex_snippets(snippets: Iterable[dict[str, object]]) -> list[dict[str, object]]:
    """Return snippet evidence with stable SN-number ids after filtering."""
    out: list[dict[str, object]] = []
    for idx, item in enumerate(snippets, start=1):
        copied = dict(item)
        copied["snippet_id"] = "SN" + str(idx).zfill(2)
        out.append(copied)
    return out


def filter_bundle_to_requested_files(
    question: str,
    bundle: RetrievalBundle,
) -> RetrievalBundle:
    """Restrict strict evidence bundles to explicitly requested files.

    An explicit phrase such as "retrieve evidence only from this exact file:"
    creates a hard allow-list. Scoring cannot keep helper files, validation
    scripts, or other distractors outside that allow-list.
    """
    strict_paths = extract_strict_requested_file_paths(question)
    requested = extract_question_file_names(question)
    excluded = extract_question_excluded_file_names(question)
    excluded_fragments = extract_question_excluded_path_fragments(question)
    run_analysis_trace = project_qa_run_analysis_trace_requested(question)
    if (
        not strict_paths
        and not requested
        and not run_analysis_trace
        and not excluded
        and not excluded_fragments
    ):
        return bundle

    def _matches_filter(path_value: str) -> bool:
        if excluded and path_matches_requested_file(path_value, excluded):
            return False
        if excluded_fragments and _path_matches_excluded_fragment(path_value, excluded_fragments):
            return False
        if strict_paths:
            return path_matches_strict_requested_path(path_value, strict_paths)
        if requested and path_matches_requested_file(path_value, requested):
            return True
        if run_analysis_trace and path_matches_project_qa_run_analysis_trace_file(path_value):
            return True
        return not requested and not run_analysis_trace

    file_items = [
        item
        for item in bundle.file_evidence
        if _matches_filter(getattr(item, "path", ""))
    ]
    symbol_items = [
        item
        for item in bundle.symbol_evidence
        if _matches_filter(getattr(item, "path", ""))
    ]
    snippet_items = [
        item
        for item in bundle.snippet_evidence
        if _matches_filter(str(item.get("path", "")))
    ]

    return RetrievalBundle(
        file_evidence=_reindex_file_items(file_items),
        symbol_evidence=_reindex_symbol_items(symbol_items),
        snippet_evidence=_reindex_snippets(snippet_items),
    )
