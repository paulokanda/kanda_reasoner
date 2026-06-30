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

__all__ = [
    "augment_bundle_with_live_source_fallback",
    "extract_live_identifier_terms",
    "find_live_source_candidates",
]


_EXCLUDED_DIRS = {
    "__pycache__",
    ".git",
    ".idea",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "env",
    "build",
    "dist",
    "node_modules",
    "htmlcov",
    "coverage",
    "json_splitted",
}

_SOURCE_EXTENSIONS = {".py", ".md", ".txt", ".toml", ".json", ".yml", ".yaml"}


def _norm(value: str) -> str:
    """Return a simple lowercase alphanumeric normalization."""
    return re.sub(r"[^a-z0-9]+", "", str(value or "").lower())


def _camel_to_snake(value: str) -> str:
    """Convert a CamelCase token to snake_case."""
    text = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", str(value))
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)
    return text.lower()


def extract_live_identifier_terms(question: str) -> list[str]:
    """Extract exact identifier-like terms from a user question."""
    raw_terms = re.findall(
        r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*|[A-Za-z0-9_\-]+\.py",
        question,
    )
    out: list[str] = []
    seen: set[str] = set()

    stop_words = {
        "what",
        "where",
        "which",
        "when",
        "why",
        "how",
        "does",
        "about",
        "responsibility",
        "responsible",
        "class",
        "function",
        "method",
        "file",
        "module",
        "project",
        "define",
        "defines",
        "defined",
        "implementation",
        "explain",
        "show",
    }

    for term in raw_terms:
        stripped = term.strip()
        if not stripped:
            continue

        lower = stripped.lower()
        is_python_file = lower.endswith(".py")
        has_identifier_shape = (
            "_" in stripped
            or "." in stripped
            or any(char.isupper() for char in stripped[1:])
            or len(stripped) >= 10
        )

        if lower in stop_words and not is_python_file:
            continue

        if not is_python_file and not has_identifier_shape:
            continue

        key = stripped.lower()
        if key in seen:
            continue

        seen.add(key)
        out.append(stripped)

    return out[:6]


def _bundle_text(bundle: RetrievalBundle) -> str:
    """Return normalized text for already retrieved evidence."""
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
    """Return True when existing evidence already mentions term."""
    if not term:
        return True
    return _norm(term) in _bundle_text(bundle)


def _candidate_file_tokens(term: str) -> set[str]:
    """Build normalized filename/path tokens for one identifier term."""
    tokens = {_norm(term)}
    snake = _camel_to_snake(term)
    tokens.add(_norm(snake))
    if not term.lower().endswith(".py"):
        tokens.add(_norm(snake + ".py"))
    return {token for token in tokens if token}


def _is_excluded_path(path: Path) -> bool:
    """Return True for directories/files that should not be scanned."""
    lowered_parts = {part.lower() for part in path.parts}
    return any(part in _EXCLUDED_DIRS for part in lowered_parts)


def _iter_candidate_source_files(project_root: Path) -> list[Path]:
    """Return bounded source-like files under project_root."""
    files: list[Path] = []
    for root, dirs, names in os.walk(project_root):
        root_path = Path(root)
        dirs[:] = [
            name for name in dirs if name.lower() not in _EXCLUDED_DIRS
        ]
        if _is_excluded_path(root_path):
            continue

        for name in names:
            path = root_path / name
            if path.suffix.lower() not in _SOURCE_EXTENSIONS:
                continue
            if _is_excluded_path(path):
                continue
            files.append(path)

    files.sort(key=lambda item: str(item).lower())
    return files


def _read_small_text(path: Path, max_bytes: int = 2 * 1024 * 1024) -> str:
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
    limit: int = 4,
) -> list[dict[str, Any]]:
    """Find live source files that match identifier terms."""
    root = Path(project_root).resolve()
    if not root.exists() or not root.is_dir():
        return []

    term_tokens: dict[str, set[str]] = {
        term: _candidate_file_tokens(term) for term in terms
    }
    candidates: list[tuple[int, str, str, Path]] = []

    for path in _iter_candidate_source_files(root):
        try:
            relative = str(path.relative_to(root))
        except ValueError:
            continue

        relative_norm = _norm(relative)
        file_norm = _norm(path.name)
        text = ""

        for term, tokens in term_tokens.items():
            score = 0
            if any(token and token in file_norm for token in tokens):
                score += 900
            if any(token and token in relative_norm for token in tokens):
                score += 300

            if score < 900:
                text = text or _read_small_text(path)
                text_norm = _norm(text)
                if _norm(term) in text_norm:
                    score += 500

            if score <= 0:
                continue

            # Prefer Python implementation files for symbol questions.
            if path.suffix.lower() == ".py":
                score += 120

            candidates.append((score, relative.lower(), term, path))

    candidates.sort(key=lambda item: (-item[0], item[1], item[2].lower()))

    out: list[dict[str, Any]] = []
    seen_paths: set[str] = set()

    for score, _relative_key, term, path in candidates:
        relative = str(path.relative_to(root))
        if relative in seen_paths:
            continue
        seen_paths.add(relative)
        out.append({"score": score, "term": term, "path": relative})
        if len(out) >= limit:
            break

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
) -> RetrievalBundle:
    """Augment retrieval with verified live source when JSON evidence is weak.

    The fallback activates only for identifier-like terms that are missing from
    the current evidence bundle.
    """
    project_root = str(getattr(retriever.idx, "project_root", "") or "").strip()
    if not project_root:
        return bundle

    terms = [
        term
        for term in extract_live_identifier_terms(question)
        if not _term_already_supported(term, bundle)
    ]

    if not terms:
        return bundle

    candidates = find_live_source_candidates(project_root, terms, limit=4)
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
                "This evidence came from live source verification, not from stale JSON.",
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
