# project-path: kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/_live_source_query.py
"""Query extraction and ranking for bounded live-source fallback."""

from __future__ import annotations

import io
import re
import tokenize
from pathlib import PurePath


_STOP_WORDS = {
    "a", "about", "access", "after", "all", "also", "an", "and",
    "answer", "any", "are", "as", "at", "available", "be", "before",
    "brief", "class", "classes", "code", "current", "detecting", "do",
    "does", "each", "exact", "explain", "file", "files", "find", "for",
    "from", "function", "functions", "get", "give", "how", "if", "in",
    "information", "inspected", "implementation", "is", "it", "line",
    "lines", "method", "methods", "model", "modify", "names", "needed",
    "no", "not", "of", "only", "or", "other", "out", "question",
    "relevant", "responsible", "return", "rules", "say", "searching",
    "selected", "show", "source", "state", "step", "steps", "the",
    "their", "there", "this", "to", "trace", "used", "using", "when",
    "where", "which", "with", "without",
}

_LOW_VALUE_SINGLETONS = {
    "ai", "json", "local", "project", "python", "evidence", "folder", "root",
    "loaded", "explicitly", "normal", "technical", "unsupported",
}

_CONCEPT_ALIASES: tuple[tuple[tuple[str, ...], tuple[str, ...]], ...] = (
    (("selected project root", "project root"),
     ("selected_project_root", "project_root", "project_root_override")),
    (("complete local ai", "complete json", "complete project evidence"),
     ("complete_local_AI", "local_ai_json", "canonical_json")),
    (("loaded json", "json is incomplete", "json does not contain"),
     ("index_data", "artifact_type", "ensure_project_json_loaded_for_question")),
    (("live source", "live project source"),
     ("live_source_fallback", "augment_bundle_with_live_source_fallback",
      "find_live_source_candidates", "initialize_live_project",
      "local_ai_live_project_source")),
    (("project support",),
     ("show_project_to_ai", "_is_excluded_path")),
    (("symlink", "symlinks"),
     ("is_symlink", "followlinks")),
    (("junction", "junctions", "reparse point"),
     ("_is_reparse_point", "st_file_attributes")),
    (("virtual environment", "virtual environments", "venv"),
     ("_EXCLUDED_DIRS", ".venv", "venv")),
    (("build folder", "build folders", "binary", "binaries"),
     ("_EXCLUDED_DIRS", "_SOURCE_EXTENSIONS")),
    (("bounded", "source limit", "file limit"),
     ("_MAX_SOURCE_FILES", "_MAX_SOURCE_FILE_BYTES", "max_snippets")),
    (("returning bounded source evidence", "returning source evidence"),
     ("SessionService", "project_root_override", "bundle")),
    (("preferred evidence", "preferred when", "preferred source"),
     ("resolve_project_json_path", "selected_json")),
    (("shell access", "shell commands", "writes", "write access"),
     ("live_source_fallback", "verify_live_source_path")),
)

_HIGH_PRIORITY_TERMS = {
    "_is_excluded_path", "_is_reparse_point",
    "augment_bundle_with_live_source_fallback",
    "ensure_project_json_loaded_for_question", "find_live_source_candidates",
    "initialize_live_project", "project_root_override",
    "resolve_project_json_path", "sessionservice",
}

_LOW_SPECIFICITY_TERMS = {
    "artifact_type", "bundle", "canonical_json", "index_data",
    "local_ai_json", "max_snippets", "project_root", "selected_json",
}

_REFERENCE_PARTS = {
    ".project_reference", "oldies", "archive", "archives", "backup",
    "backups", "examples", "example", "samples", "sample", "vendor",
    "third_party", "generated", "legacy",
}


def _norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(value or "").lower())


def _camel_to_snake(value: str) -> str:
    text = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", str(value))
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", text)
    return text.lower()


def _add_ranked(
    ranked: dict[str, tuple[int, int, str]],
    value: str,
    priority: int,
    order: int,
) -> int:
    term = str(value or "").strip()
    if not term:
        return order
    key = term.lower()
    current = ranked.get(key)
    if current is None or priority > current[0]:
        ranked[key] = (priority, order, term)
    return order + 1


def extract_live_identifier_terms(question: str) -> list[str]:
    """Return specific identifiers and implementation concepts in rank order."""
    text = str(question or "")
    lowered = text.lower()
    ranked: dict[str, tuple[int, int, str]] = {}
    order = 0

    for phrases, aliases in _CONCEPT_ALIASES:
        if any(phrase in lowered for phrase in phrases):
            for alias in aliases:
                order = _add_ranked(ranked, alias, 120, order)

    raw_identifiers = re.findall(
        r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*"
        r"|[A-Za-z0-9_\-]+\.py",
        text,
    )
    for value in raw_identifiers:
        lower = value.lower()
        shaped = (
            "_" in value
            or "." in value
            or any(char.isupper() for char in value[1:])
        )
        if lower in _LOW_VALUE_SINGLETONS or lower in _STOP_WORDS:
            continue
        if shaped:
            order = _add_ranked(ranked, value, 150, order)

    words = re.findall(r"[A-Za-z][A-Za-z0-9_-]+", text)
    for value in words:
        lower = value.lower()
        if lower in _STOP_WORDS or lower in _LOW_VALUE_SINGLETONS:
            continue
        if len(lower) < 6:
            continue
        order = _add_ranked(ranked, lower, 25, order)

    ordered = sorted(
        (
            (priority, first_order, term)
            for priority, first_order, term in ranked.values()
        ),
        key=lambda item: (-item[0], item[1], item[2].lower()),
    )
    return [term for _priority, _order, term in ordered[:36]]



def _python_code_text(text: str) -> str:
    """Return Python code tokens while omitting comments and strings."""
    names: list[str] = []
    try:
        tokens = tokenize.generate_tokens(io.StringIO(text).readline)
        for token in tokens:
            if token.type == tokenize.NAME:
                names.append(token.string)
    except (IndentationError, SyntaxError, tokenize.TokenError):
        return text
    return " ".join(names)

def _term_tokens(term: str) -> set[str]:
    tokens = {_norm(term), _norm(_camel_to_snake(term))}
    if not term.lower().endswith(".py"):
        tokens.add(_norm(_camel_to_snake(term) + ".py"))
    return {token for token in tokens if token}


def _term_weight(term: str) -> int:
    if term.lower() in _HIGH_PRIORITY_TERMS:
        return 12
    if term.lower() in _LOW_SPECIFICITY_TERMS:
        return 4
    if "_" in term or "." in term or any(char.isupper() for char in term[1:]):
        return 9
    if len(term) >= 12:
        return 5
    return 3


def _path_adjustment(relative: str, question: str) -> int:
    parts = {part.lower() for part in PurePath(relative).parts}
    question_lower = question.lower()
    asks_reference = any(
        term in question_lower
        for term in ("reference", "oldies", "archive", "backup", "example")
    )
    adjustment = 0
    if parts & _REFERENCE_PARTS and not asks_reference:
        adjustment -= 2400
    name = PurePath(relative).name.lower()
    if "local ai" in question_lower and "web ai" not in question_lower:
        if "project_web_ai" in relative.lower():
            adjustment -= 2800
    asks_tests = any(term in question_lower for term in ("test", "validator"))
    if not asks_tests and (
        "test" in parts
        or "tests" in parts
        or name.startswith("test_")
        or name.startswith("validate_")
    ):
        adjustment -= 3500
    is_python = relative.lower().endswith(".py")
    asks_implementation = any(
        term in question_lower
        for term in ("implementation", "python source", "class", "function")
    )
    if is_python:
        adjustment += 240
    elif asks_implementation:
        adjustment -= 1600
    return adjustment



def _definition_score(text: str, term: str, weight: int) -> int:
    """Reward exact Python definitions over incidental token mentions."""
    names = {term, _camel_to_snake(term)}
    score = 0
    for name in names:
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
            continue
        escaped = re.escape(name)
        flags = re.MULTILINE | re.IGNORECASE
        if re.search(r"^\s*def\s+" + escaped + r"\b", text, flags):
            score = max(score, 280 * weight)
        if re.search(r"^\s*class\s+" + escaped + r"\b", text, flags):
            score = max(score, 280 * weight)
        if re.search(r"^\s*" + escaped + r"\s*=", text, flags):
            score = max(score, 80 * weight)
    return score

def score_live_source_candidate(
    relative: str,
    text: str,
    terms: list[str],
    question: str,
) -> tuple[int, str]:
    """Score one source file and return its best snippet anchor."""
    relative_norm = _norm(relative)
    file_norm = _norm(PurePath(relative).name)
    searchable_text = (
        _python_code_text(text) if relative.lower().endswith(".py") else text
    )
    text_norm = _norm(searchable_text)
    score = _path_adjustment(relative, question)
    matched: list[tuple[int, str]] = []

    for term in terms:
        tokens = _term_tokens(term)
        weight = _term_weight(term)
        term_score = 0
        if any(token in file_norm for token in tokens):
            term_score += 140 * weight
        if any(token in relative_norm for token in tokens):
            term_score += 55 * weight
        normalized_term = _norm(term)
        if normalized_term and normalized_term in text_norm:
            term_score += 35 * weight
        if relative.lower().endswith(".py"):
            term_score += _definition_score(text, term, weight)
        if term_score:
            score += term_score
            matched.append((term_score, term))

    distinct = len(matched)
    score += min(distinct, 8) * min(distinct, 8) * 18
    if not matched:
        return 0, ""

    matched.sort(key=lambda item: (-item[0], item[1].lower()))
    return score, matched[0][1]
