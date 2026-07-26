# project-path: kanda_reasoner_app/error_memory_gui/_ai_evidence_recovery.py
"""Recover real validation evidence from project files for Error Memory lessons."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

__all__ = [
    "recover_validation_evidence",
]

TEXT_SUFFIXES = {".json", ".txt", ".md", ".log", ".out", ".yaml", ".yml"}
SKIP_DIRS = {
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    "site-packages",
    "node_modules",
}
OBSERVED_MARKERS = (
    "VALIDATION OK:",
    "ZIP CONTRACT: PASS",
    "Errors: 0",
    "STATUS: IN_SYNC",
    "FREEZE_HINT_EVIDENCE_MERGE_OK",
)
EXPECTED_FRAGMENTS = (
    "expected marker",
    "expected_marker",
    "expected regression",
    "expected additional",
    "do not invent",
    "template",
    "placeholder",
    "<expected",
)
MAX_FILE_BYTES = 900_000
MAX_FILES_SCANNED = 320
MAX_EVIDENCE_ITEMS = 8


def _safe_path(value: Any) -> Path | None:
    """Return a Path when value is usable."""
    try:
        text = str(value or "").strip()
        if not text:
            return None
        return Path(text)
    except Exception:
        return None


def _show_project_root(project_root: Path) -> Path:
    """Return the external show_project_to_AI root for a project."""
    return project_root.with_name(project_root.name + "_show_project_to_AI")


def _work_root(project_root: Path) -> Path:
    """Return the delete-after-daily-work root for a project."""
    return project_root.with_name(project_root.name + "_delete_after_daily_work")


def _candidate_roots(project_root: Any) -> list[Path]:
    """Return roots worth scanning for validation evidence."""
    root = _safe_path(project_root)
    if root is None:
        return []
    roots = [
        _show_project_root(root) / "project_freeze_after_update" / "freeze_hint_intake",
        _show_project_root(root) / "project_freeze_after_update" / "files_to_send_ai",
        _show_project_root(root) / "project_freeze_after_update" / "frozen_features_memory",
        _show_project_root(root) / "project_error_memory",
        _work_root(root),
        root / "project_freeze_after_update" / "freeze_hint_intake",
        root,
    ]
    result: list[Path] = []
    seen: set[str] = set()
    for path in roots:
        try:
            resolved = str(path.resolve())
        except Exception:
            resolved = str(path)
        if resolved not in seen and path.exists():
            result.append(path)
            seen.add(resolved)
    return result


def _as_text_items(value: Any) -> list[str]:
    """Return clean string items from scalar or iterable values."""
    if value is None:
        return []
    if isinstance(value, str):
        values: Iterable[Any] = value.replace(";", "\n").splitlines()
    elif isinstance(value, (list, tuple, set)):
        values = value
    else:
        values = [value]
    return [str(item).strip() for item in values if str(item).strip()]


def _lesson_from_context(context_text: str) -> dict[str, Any]:
    """Best-effort parse of a lesson dict from marker-wrapped or bare JSON text."""
    raw = str(context_text or "")
    begin = raw.find("KANDA_ERROR_LESSON_JSON_BEGIN")
    end = raw.find("KANDA_ERROR_LESSON_JSON_END")
    if begin >= 0 and end > begin:
        raw = raw[begin + len("KANDA_ERROR_LESSON_JSON_BEGIN"):end]
    else:
        start = raw.find("{")
        stop = raw.rfind("}")
        if start >= 0 and stop > start:
            raw = raw[start:stop + 1]
    try:
        payload = json.loads(raw)
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


def _terms_from_lesson(lesson: dict[str, Any], context_text: str) -> list[str]:
    """Build strong search terms from a lesson and its raw context."""
    payload = dict(_lesson_from_context(context_text))
    payload.update({key: value for key, value in lesson.items() if value})
    terms: list[str] = []
    for key in ("lesson_id", "source_patch_zip", "raw_error_text"):
        terms.extend(_as_text_items(payload.get(key)))
    fingerprint = payload.get("fingerprint")
    if isinstance(fingerprint, dict):
        terms.extend(_as_text_items(fingerprint.get("fingerprint_hash")))
        terms.extend(_as_text_items(fingerprint.get("components")))
    regression = payload.get("regression_check")
    if isinstance(regression, dict):
        terms.extend(_as_text_items(regression.get("expected_marker")))
        command = str(regression.get("command", "")).strip()
        if command:
            terms.append(Path(command.replace("\\", "/")).name)
    result: list[str] = []
    seen: set[str] = set()
    for term in terms:
        clean = str(term).strip()
        if len(clean) < 4:
            continue
        if clean.lower() not in seen:
            result.append(clean)
            seen.add(clean.lower())
    return result


def _iter_text_files(root: Path) -> Iterable[Path]:
    """Yield bounded text files below a root."""
    scanned = 0
    if root.is_file():
        yield root
        return
    for path in root.rglob("*"):
        if scanned >= MAX_FILES_SCANNED:
            break
        try:
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            if path.stat().st_size > MAX_FILE_BYTES:
                continue
        except Exception:
            continue
        scanned += 1
        yield path


def _looks_expected_only(line: str) -> bool:
    """Return whether a line is expected-marker text rather than observed evidence."""
    lowered = line.lower()
    return any(fragment in lowered for fragment in EXPECTED_FRAGMENTS)


def _line_has_observed_marker(line: str) -> bool:
    """Return whether a line contains an observed validation marker."""
    if _looks_expected_only(line):
        return False
    return any(marker in line for marker in OBSERVED_MARKERS)


def _file_has_strong_term(text: str, terms: list[str], path: Path) -> bool:
    """Return whether file content or path matches a lesson-specific term."""
    lowered = text.lower()
    path_text = str(path).lower()
    strong_terms = [term.lower() for term in terms if len(term) >= 6]
    if not strong_terms:
        return True
    return any(term in lowered or term in path_text for term in strong_terms)


def _relative_label(path: Path, roots: list[Path]) -> str:
    """Return a compact path label for evidence messages."""
    for root in roots:
        try:
            return str(path.relative_to(root)).replace("\\", "/")
        except Exception:
            continue
    return str(path).replace("\\", "/")


def _evidence_from_file(path: Path, roots: list[Path], terms: list[str]) -> list[str]:
    """Return observed evidence lines recovered from one file."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []
    if not _file_has_strong_term(text, terms, path):
        return []
    label = _relative_label(path, roots)
    items: list[str] = []
    for line in text.splitlines():
        clean = " ".join(line.strip().split())
        if not clean or len(clean) > 360:
            continue
        if _line_has_observed_marker(clean):
            items.append("Recovered from project file " + label + ": " + clean)
        if len(items) >= 3:
            break
    return items


def recover_validation_evidence(
    *,
    project_root: Any,
    lesson: dict[str, Any] | None = None,
    context_text: str = "",
) -> list[str]:
    """Recover observed validation evidence from project files.

    Only observed markers found in project files are returned. Expected-marker text,
    templates, and placeholders are ignored to avoid inventing validation success.
    """
    roots = _candidate_roots(project_root)
    if not roots:
        return []
    payload = lesson if isinstance(lesson, dict) else {}
    terms = _terms_from_lesson(payload, context_text)
    evidence: list[str] = []
    seen: set[str] = set()
    for root in roots:
        for path in _iter_text_files(root):
            for item in _evidence_from_file(path, roots, terms):
                key = item.lower()
                if key not in seen:
                    evidence.append(item)
                    seen.add(key)
                if len(evidence) >= MAX_EVIDENCE_ITEMS:
                    return evidence
    return evidence
