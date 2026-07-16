"""Support V10 project reasoning and evidence handling."""

# ------------------------------------------------------------------------
# MODULE ORIGIN : E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\reasoner_retriever.py
# MANIFEST      : E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\reasoner_retriever_help.json
# HELP FOLDER   : E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\reasoner_retriever_help
# PURPOSE       : Own snippet retrieval, snippet scoring, snippet file resolution, and snippet reading helpers for ProjectRetriever.
# EXPORTS       : score_runtime_anchor_for_question, find_anchor_line_in_file, resolve_existing_project_file_path, build_runtime_anchor_snippets, extract_runtime_anchors_from_detail, retrieve_snippets, score_symbol_snippet_candidate, score_file_snippet_candidate, snippet_radius_for_symbol, read_snippet
# DEPENDS ON    : query_intents.py, query_text.py
# REFACTOR DATE : 2026-04-10
# ------------------------------------------------------------------------
from __future__ import annotations

import os
import re
from typing import Any

from kanda_reasoner_app.project_reasoner_v10.v10_models import (
    EvidenceItem,
    SymbolEvidenceItem,
)
from kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_intents import (
    detect_query_intents,
    is_runtime_heavy_question,
)
from kanda_reasoner_app.project_reasoner_v10.reasoner_retriever_help.query_text import (
    is_allowed_project_path,
    is_auxiliary_ui_path,
    norm_text,
    safe_read_text,
    tokenize_query,
)

__all__ = [
    "score_runtime_anchor_for_question",
    "find_anchor_line_in_file",
    "resolve_existing_project_file_path",
    "build_runtime_anchor_snippets",
    "extract_runtime_anchors_from_detail",
    "retrieve_snippets",
    "score_symbol_snippet_candidate",
    "score_file_snippet_candidate",
    "snippet_radius_for_symbol",
    "read_snippet",
]


from .snippet_retrieval_help import snippet_retrieval_part_1_private_impl as _sr_part_1
from .snippet_retrieval_help import snippet_retrieval_part_2_private_impl as _sr_part_2
from .snippet_retrieval_help import snippet_retrieval_part_3_private_impl as _sr_part_3

def score_runtime_anchor_for_question(*args, **kwargs):
    return _sr_part_1._sr_score_runtime_anchor_for_question_impl(*args, **kwargs)



def find_anchor_line_in_file(*args, **kwargs):
    return _sr_part_1._sr_find_anchor_line_in_file_impl(*args, **kwargs)



def resolve_existing_project_file_path(
    retriever,
    logical_path: str,
) -> tuple[str, str] | tuple[None, None]:
    logical_path = str(logical_path or "").strip()
    if not logical_path:
        return None, None

    def _is_candidate_safe(rel_candidate: str) -> bool:
        try:
            full = os.path.realpath(
                os.path.join(retriever.idx.project_root, rel_candidate)
            )
            root = os.path.realpath(retriever.idx.project_root)
            return full.startswith(root)
        except OSError:
            return False

    direct_abs = os.path.join(retriever.idx.project_root, logical_path)
    if os.path.exists(direct_abs) and _is_candidate_safe(logical_path):
        return logical_path, direct_abs

    logical_low = logical_path.replace("\\", "/").lower().strip("/")
    logical_base = os.path.basename(logical_low)

    candidate_sources: set[str] = set()
    candidate_sources.update(
        str(path).replace("\\", "/").strip()
        for path in retriever.idx.files_by_path.keys()
    )
    candidate_sources.update(
        str(path).replace("\\", "/").strip()
        for path in retriever.idx.runtime_events_by_file.keys()
    )

    exact_matches: list[str] = []
    basename_matches: list[str] = []

    for known_path in sorted(candidate_sources):
        known_low = known_path.lower().strip("/")
        abs_known = os.path.join(retriever.idx.project_root, known_path)
        if os.path.exists(abs_known):
            if known_low == logical_low:
                exact_matches.append(known_path)
                continue
            if os.path.basename(known_low) == logical_base:
                basename_matches.append(known_path)

    candidates = exact_matches if exact_matches else basename_matches

    if not candidates:
        disk_matches: list[str] = []
        for root, _dirs, files in os.walk(retriever.idx.project_root):
            for file_name in files:
                if file_name.lower() != logical_base:
                    continue
                abs_found = os.path.join(root, file_name)
                rel_found = os.path.relpath(
                    abs_found,
                    retriever.idx.project_root,
                ).replace("\\", "/")
                disk_matches.append(rel_found)
        candidates = disk_matches

    if not candidates:
        return None, None

    def rank_candidate(path: str) -> tuple[int, str]:
        low = path.replace("\\", "/").lower()
        score = 0
        if "reasoner_runtime_collector" in low:
            score += 500
        if "/runtime_collector/" in low:
            score += 400
        if low.endswith("/runtime_runner.py"):
            score += 300
        if "runtime" in low:
            score += 120
        if "collector" in low:
            score += 100
        if "scenario" in low:
            score += 60
        return score, path

    safe_candidates = [c for c in candidates if _is_candidate_safe(c)]
    if not safe_candidates:
        return None, None

    rel_path = max(safe_candidates, key=rank_candidate)
    abs_path = os.path.join(retriever.idx.project_root, rel_path)
    return rel_path, abs_path


def build_runtime_anchor_snippets(
    retriever,
    question: str,
    file_evidence: list[EvidenceItem],
    limit: int,
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    seen: set[tuple[str, int, str]] = set()
    question_low = norm_text(question)

    file_cache: dict[str, str] = {}

    def _get_file_text(abs_path: str) -> str:
        if abs_path not in file_cache:
            file_cache[abs_path] = safe_read_text(abs_path)
        return file_cache[abs_path]

    def _find_anchor_line_cached(abs_path: str, anchor: str) -> int | None:
        try:
            text = _get_file_text(abs_path)
        except OSError:
            return None
        lines = text.splitlines()
        anchor_low = anchor.lower()
        for idx, line in enumerate(lines, start=1):
            if anchor_low in line.lower():
                return idx
        return None

    def _read_snippet_cached(abs_path: str, line: int, radius: int) -> str:
        text = _get_file_text(abs_path)
        lines = text.splitlines()
        if not lines:
            return ""
        start = max(1, line - radius)
        end = min(len(lines), line + radius)
        snippet_lines: list[str] = []
        for idx in range(start, end + 1):
            snippet_lines.append(str(idx).rjust(5) + " | " + lines[idx - 1])
        return "\n".join(snippet_lines)

    def _fallback_line_cached(abs_path: str) -> int:
        try:
            text = _get_file_text(abs_path)
        except Exception:
            return 1
        lines = text.splitlines()
        preferred_tokens = [
            "on_apply_clicked",
            "on_text_changed",
            "on_close_clicked",
            "clicked.connect",
            "qpushbutton",
            "qlineedit",
            "probe",
        ]
        for idx, line in enumerate(lines, start=1):
            low = line.lower()
            if any(token in low for token in preferred_tokens):
                return idx
        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()
            if stripped.startswith("def ") or stripped.startswith("class "):
                return idx
        return 1

    def _dedupe_keep_order(values: list[str]) -> list[str]:
        out_values: list[str] = []
        seen_values: set[str] = set()
        for value in values:
            value = str(value or "").strip()
            if not value:
                continue
            key = value.lower()
            if key in seen_values:
                continue
            seen_values.add(key)
            out_values.append(value)
        return out_values

    def _candidate_terms_for_anchor(anchor: str) -> list[str]:
        anchor_low = norm_text(anchor)
        candidates: list[str] = [anchor]

        alias_map = {
            "runtime_runner_probe_apply_button": [
                "runtime_runner_probe_apply_button",
                "on_apply_clicked",
                "apply_button",
                "apply",
                "probe",
            ],
            "runtime_runner_probe_line_edit": [
                "runtime_runner_probe_line_edit",
                "on_text_changed",
                "line_edit",
                "text_changed",
                "probe",
            ],
            "runtime_runner_probe_close_button": [
                "runtime_runner_probe_close_button",
                "on_close_clicked",
                "close_button",
                "close",
                "probe",
            ],
            "on_apply_clicked": [
                "on_apply_clicked",
                "apply_clicked",
                "apply",
                "probe",
            ],
            "on_text_changed": [
                "on_text_changed",
                "text_changed",
                "line_edit",
                "probe",
            ],
            "on_close_clicked": [
                "on_close_clicked",
                "close_clicked",
                "close",
                "probe",
            ],
        }

        candidates.extend(alias_map.get(anchor_low, []))

        if anchor_low.startswith("runtime_runner_probe_"):
            trimmed = anchor_low.replace("runtime_runner_probe_", "")
            candidates.append(trimmed)
            candidates.append(trimmed.replace("_button", ""))
            candidates.append(trimmed.replace("_line_edit", ""))
            candidates.append(trimmed.replace("_close_button", ""))

        if "apply" in question_low:
            candidates.extend(["on_apply_clicked", "apply", "probe"])
        if "text" in question_low:
            candidates.extend(["on_text_changed", "text_changed", "probe"])
        if "close" in question_low:
            candidates.extend(["on_close_clicked", "close", "probe"])
        if "button" in question_low:
            candidates.extend(["button", "clicked", "probe"])

        return _dedupe_keep_order(candidates)

    for item in file_evidence[:8]:
        logical_path = item.path
        resolved_rel_path, abs_path = retriever._resolve_existing_project_file_path(
            logical_path
        )
        if not resolved_rel_path or not abs_path:
            continue

        detail_text = str(item.detail or "")
        if (
            "Runtime anchors:" not in detail_text
            and "Runtime context:" not in detail_text
        ):
            continue

        anchors = retriever._extract_runtime_anchors_from_detail(detail_text)
        if not anchors:
            anchors, _previews = retriever._get_runtime_anchor_summary(
                logical_path,
                limit=12,
            )

        ranked_anchors = sorted(
            anchors,
            key=lambda anchor: retriever._score_runtime_anchor_for_question(
                question,
                anchor,
            ),
            reverse=True,
        )

        found_for_file = False

        for anchor in ranked_anchors:
            for candidate_term in _candidate_terms_for_anchor(anchor):
                line = _find_anchor_line_cached(abs_path, candidate_term)
                if line is None:
                    continue

                key = (resolved_rel_path, line, candidate_term)
                if key in seen:
                    continue
                seen.add(key)

                out.append(
                    {
                        "path": resolved_rel_path,
                        "line": line,
                        "anchor": candidate_term,
                        "text": _read_snippet_cached(abs_path, line, radius=18),
                    }
                )
                found_for_file = True

                if len(out) >= limit:
                    return out

                break

        if not found_for_file:
            line = _fallback_line_cached(abs_path)
            key = (resolved_rel_path, line, "runtime-file-fallback")
            if key not in seen:
                seen.add(key)
                out.append(
                    {
                        "path": resolved_rel_path,
                        "line": line,
                        "anchor": "runtime-file-fallback",
                        "text": _read_snippet_cached(abs_path, line, radius=18),
                    }
                )

                if len(out) >= limit:
                    return out

    return out


def extract_runtime_anchors_from_detail(*args, **kwargs):
    return _sr_part_1._sr_extract_runtime_anchors_from_detail_impl(*args, **kwargs)



def retrieve_snippets(*args, **kwargs):
    return _sr_part_2._sr_retrieve_snippets_impl(*args, **kwargs)



def score_symbol_snippet_candidate(*args, **kwargs):
    return _sr_part_3._sr_score_symbol_snippet_candidate_impl(*args, **kwargs)



def score_file_snippet_candidate(*args, **kwargs):
    return _sr_part_3._sr_score_file_snippet_candidate_impl(*args, **kwargs)



def snippet_radius_for_symbol(*args, **kwargs):
    return _sr_part_3._sr_snippet_radius_for_symbol_impl(*args, **kwargs)



def read_snippet(*args, **kwargs):
    return _sr_part_3._sr_read_snippet_impl(*args, **kwargs)








def _bind_snippet_retrieval_private_impl_globals():
    root_globals = globals()
    _sr_part_1._bind_root_globals(root_globals)
    _sr_part_2._bind_root_globals(root_globals)
    _sr_part_3._bind_root_globals(root_globals)


_bind_snippet_retrieval_private_impl_globals()
