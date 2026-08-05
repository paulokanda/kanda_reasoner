# project-path: kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/live_source_fallback.py
"""Live-source fallback helpers for ProjectRetriever.

This helper belongs to the Retrieval Box. It consumes the validated
Live Source Verification Box and only augments retrieval evidence when the
loaded JSON evidence does not already support an exact identifier query.

It does not write files and does not modify canonical or local-AI JSON.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

from kanda_reasoner_app.live_source_verification import (
    extract_live_source_snippet,
    verify_live_source_path,
)
from kanda_reasoner_app.reasoner_engine.v10_models import (
    EvidenceItem,
    RetrievalBundle,
)

from ._live_source_query import (
        extract_live_identifier_terms as _extract_live_identifier_terms,
        score_live_source_candidate,
    )


__all__ = [
    "augment_bundle_with_live_source_fallback",
    "extract_live_identifier_terms",
    "find_live_source_candidates",
]




def extract_live_identifier_terms(question: str) -> list[str]:
    """Return ranked live-source identifiers through the stable facade."""
    return _extract_live_identifier_terms(question)


_EXCLUDED_DIRS = {
    "__pycache__",
    ".git",
    ".history",
    ".idea",
    ".mypy_cache",
    ".project_reference",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "archive",
    "archives",
    "backup",
    "backups",
    "build",
    "coverage",
    "dist",
    "env",
    "htmlcov",
    "json_splitted",
    "legacy_physical_package_archive",
    "node_modules",
    "oldies",
    "venv",
}

_PRODUCTION_DIR_NAMES = {
    "app",
    "core",
    "engine",
    "lib",
    "package",
    "packages",
    "retriever",
    "runtime",
    "service",
    "services",
    "src",
}

_LOW_PRIORITY_DIR_NAMES = {
    "docs",
    "documentation",
    "examples",
    "samples",
    "scripts",
    "test",
    "tests",
    "tools",
}

_SOURCE_EXTENSIONS = {".py", ".md", ".txt", ".toml", ".json", ".yml", ".yaml"}

_MAX_SOURCE_FILES = 3000
_MAX_SOURCE_FILE_BYTES = 96 * 1024



def _norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(value or "").lower())


def _bundle_text(bundle: RetrievalBundle) -> str:
    parts: list[str] = []
    for item in bundle.file_evidence:
        parts.extend([item.path, item.module_name, item.reason, item.detail])
    for item in bundle.symbol_evidence:
        parts.extend([item.symbol_name, item.path, item.reason, item.detail])
    for item in bundle.snippet_evidence:
        parts.extend(
            [
                str(item.get("path", "")),
                str(item.get("anchor", "")),
                str(item.get("text", "")),
            ]
        )
    return _norm("\n".join(parts))


def _term_already_supported(term: str, bundle: RetrievalBundle) -> bool:
    if not term:
        return True
    return _norm(term) in _bundle_text(bundle)

def _is_reparse_point(path: Path) -> bool:
    """Return whether one existing Windows path is a reparse point."""
    if os.name != "nt":
        return False
    try:
        attributes = path.stat().st_file_attributes
    except (AttributeError, OSError):
        return False
    return bool(attributes & 0x400)


def _is_excluded_path(path: Path) -> bool:
    """Return True for paths outside the bounded Local AI source surface."""
    lowered_parts = {part.lower() for part in path.parts}
    if any(part in _EXCLUDED_DIRS for part in lowered_parts):
        return True
    return any(part.endswith("_show_project_to_ai") for part in lowered_parts)


def _directory_sort_key(name: str) -> tuple[int, str]:
    """Prioritize current production packages before auxiliary folders."""
    lowered = str(name or "").lower()
    if lowered.endswith("_app") or lowered in _PRODUCTION_DIR_NAMES:
        return (0, lowered)
    if lowered in _LOW_PRIORITY_DIR_NAMES:
        return (2, lowered)
    return (1, lowered)


def _source_name_sort_key(name: str) -> tuple[int, str]:
    """Inspect Python implementation files before other source-like files."""
    lowered = str(name or "").lower()
    return (0 if lowered.endswith(".py") else 1, lowered)


def _iter_candidate_source_files(project_root: Path) -> list[Path]:
    """Return bounded source-like files under project_root."""
    files: list[Path] = []
    for root, dirs, names in os.walk(
        project_root, topdown=True, followlinks=False
    ):
        root_path = Path(root)
        kept_dirs: list[str] = []
        for name in dirs:
            candidate = root_path / name
            if _is_excluded_path(candidate):
                continue
            if candidate.is_symlink() or _is_reparse_point(candidate):
                continue
            kept_dirs.append(name)
        kept_dirs.sort(key=_directory_sort_key)
        dirs[:] = kept_dirs
        if _is_excluded_path(root_path):
            continue

        for name in sorted(names, key=_source_name_sort_key):
            path = root_path / name
            if path.suffix.lower() not in _SOURCE_EXTENSIONS:
                continue
            if _is_excluded_path(path):
                continue
            if path.is_symlink() or _is_reparse_point(path):
                continue
            files.append(path)
            if len(files) >= _MAX_SOURCE_FILES:
                files.sort(key=lambda item: str(item).lower())
                return files

    files.sort(key=lambda item: str(item).lower())
    return files


def _read_small_text(
    path: Path, max_bytes: int = _MAX_SOURCE_FILE_BYTES
) -> str:
    """Read a small text file with replacement decoding."""
    try:
        if path.stat().st_size > max_bytes:
            return ""
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def find_live_source_candidates(
    project_root: str | Path,
    terms: list[str],
    *,
    limit: int = 6,
    question: str = "",
) -> list[dict[str, Any]]:
    """Find and rank live source files using multi-term query coverage."""
    root = Path(project_root).resolve()
    if not root.exists() or not root.is_dir():
        return []

    candidates: list[tuple[int, str, str, Path]] = []
    for path in _iter_candidate_source_files(root):
        try:
            relative = str(path.relative_to(root))
        except ValueError:
            continue

        path_result = verify_live_source_path(root, relative)
        if path_result.status != "ok":
            continue

        text = _read_small_text(path)
        score, anchor = score_live_source_candidate(
            relative, text, terms, question
        )
        if score <= 0 or not anchor:
            continue
        candidates.append((score, relative.lower(), anchor, path))

    candidates.sort(key=lambda item: (-item[0], item[1], item[2].lower()))
    out: list[dict[str, Any]] = []
    for score, _relative_key, anchor, path in candidates[:limit]:
        out.append({
            "score": score,
            "term": anchor,
            "path": str(path.relative_to(root)),
        })
    return out

def _next_file_id(bundle: RetrievalBundle) -> str:
    """Return the next file evidence id."""
    return "F" + str(len(bundle.file_evidence) + 1).zfill(2)


def _next_snippet_id(bundle: RetrievalBundle) -> str:
    """Return the next snippet evidence id."""
    return "SN" + str(len(bundle.snippet_evidence) + 1).zfill(2)


def _is_live_source_snippet(item: dict[str, Any]) -> bool:
    """Return True when a snippet came from live-source fallback."""
    return str(item.get("anchor", "")).startswith("LIVE_SOURCE:")


def _prioritize_snippets_for_output(
    snippets: list[dict[str, Any]],
    *,
    max_snippets: int,
) -> list[dict[str, Any]]:
    """Keep live-source snippets visible when normal JSON snippets are full.

    Normal JSON retrieval can already fill the snippet limit before fallback
    runs. In that case, appending a verified live-source snippet at the end and
    slicing would silently drop the most important fallback evidence. This
    helper keeps LIVE_SOURCE snippets first, then preserves the original order
    of the remaining snippets.
    """
    indexed = list(enumerate(snippets))
    indexed.sort(
        key=lambda pair: (
            0 if _is_live_source_snippet(pair[1]) else 1,
            pair[0],
        )
    )
    return [item for _idx, item in indexed[:max_snippets]]


def _reindex_bundle(
    bundle: RetrievalBundle,
    *,
    max_files: int,
    max_snippets: int,
) -> RetrievalBundle:
    """Reindex file/snippet ids after fallback augmentation."""
    files = sorted(bundle.file_evidence, key=lambda item: (-item.score, item.path))[
        :max_files
    ]
    snippets = _prioritize_snippets_for_output(
        list(bundle.snippet_evidence),
        max_snippets=max_snippets,
    )

    for idx, item in enumerate(files, start=1):
        item.evidence_id = "F" + str(idx).zfill(2)

    for idx, item in enumerate(snippets, start=1):
        item["snippet_id"] = "SN" + str(idx).zfill(2)

    return RetrievalBundle(
        file_evidence=files,
        symbol_evidence=bundle.symbol_evidence,
        snippet_evidence=snippets,
    )


def augment_bundle_with_live_source_fallback(
    retriever: Any,
    question: str,
    bundle: RetrievalBundle,
    *,
    max_files: int,
    max_snippets: int,
    project_root_override: str = "",
) -> RetrievalBundle:
    """Augment retrieval with verified live source when JSON evidence is weak.

    The fallback activates only for identifier-like terms that are missing from
    the current evidence bundle.
    """
    project_root = str(project_root_override or "").strip()
    if not project_root:
        project_root = str(
            getattr(retriever.idx, "project_root", "") or ""
        ).strip()
    if not project_root:
        return bundle

    terms = [
        term
        for term in extract_live_identifier_terms(question)
        if not _term_already_supported(term, bundle)
    ]

    if not terms:
        return bundle

    candidates = find_live_source_candidates(
        project_root, terms, limit=min(max_files, 6), question=question
    )
    if not candidates:
        return bundle

    existing_paths = {
        str(item.path).replace("\\", "/").lower()
        for item in bundle.file_evidence
    }
    existing_snippets = {
        (
            str(item.get("path", "")).replace("\\", "/").lower(),
            int(item.get("line", 0)),
            str(item.get("anchor", "")),
        )
        for item in bundle.snippet_evidence
    }

    for candidate in candidates:
        relative_path = str(candidate["path"])
        normalized_path = relative_path.replace("\\", "/").lower()
        if normalized_path in existing_paths:
            continue

        path_result = verify_live_source_path(project_root, relative_path)
        if path_result.status != "ok":
            continue

        term = str(candidate["term"])
        detail = "\n".join(
            [
                "Path: " + relative_path,
                "Live source fallback: verified current file under PROJECT_ROOT.",
                "Matched identifier: " + term,
                "Status: " + path_result.status,
                "SHA-256: " + path_result.sha256,
                "Size bytes: " + str(path_result.size_bytes),
                "This evidence came from live source verification, "
                "not from stale JSON.",
            ]
        )
        bundle.file_evidence.append(
            EvidenceItem(
                evidence_id=_next_file_id(bundle),
                score=1200 + int(candidate["score"]),
                path=relative_path,
                module_name=relative_path[:-3].replace("/", ".").replace("\\", ".")
                if relative_path.endswith(".py")
                else relative_path,
                reason="live_source_fallback",
                detail=detail,
            )
        )
        existing_paths.add(normalized_path)

        snippet = extract_live_source_snippet(
            project_root,
            relative_path,
            anchor=term,
            context_lines=12,
        )
        if snippet.status == "ok":
            key = (normalized_path, int(snippet.line_start), term)
            if key not in existing_snippets:
                bundle.snippet_evidence.append(
                    {
                        "snippet_id": _next_snippet_id(bundle),
                        "path": relative_path,
                        "line": snippet.line_start,
                        "anchor": "LIVE_SOURCE:" + term,
                        "text": snippet.text,
                    }
                )
                existing_snippets.add(key)

    return _reindex_bundle(bundle, max_files=max_files, max_snippets=max_snippets)
