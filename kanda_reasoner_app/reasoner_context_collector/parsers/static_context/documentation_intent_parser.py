# project-path: kanda_reasoner_app/reasoner_context_collector/parsers/static_context/documentation_intent_parser.py
"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any


DEFAULT_DOCUMENTATION_GLOB_PATTERNS: tuple[str, ...] = (
    "README*",
    "docs/**/*.md",
    "docs/**/*.rst",
    "**/*ADR*.md",
    "**/*architecture*.md",
    "mkdocs.yml",
    "conf.py",
)


def _normalize_rel_path(path: Path, root: Path) -> str:
    """Support normalize rel path behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    root : Path
        The root path.
    
    Returns
    -------
    str
        The string result.
    """
    
    return str(path.relative_to(root)).replace("\\", "/")


def _truncate_text(value: str, max_chars: int) -> str:
    """Support truncate text behavior.
    
    Parameters
    ----------
    value : str
        The input value.
    max_chars : int
        The max chars value.
    
    Returns
    -------
    str
        The string result.
    """
    
    value = value.strip()
    if len(value) <= max_chars:
        return value
    return value[: max_chars - 3].rstrip() + "..."


def _dedupe_keep_order(items: list[str]) -> list[str]:
    """Support dedupe keep order behavior.
    
    Parameters
    ----------
    items : list[str]
        The item values.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        cleaned = str(item).strip()
        if not cleaned:
            continue
        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(cleaned)
    return out


def _new_result() -> dict[str, Any]:
    """Support new result behavior.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    return {
        "project_purpose_summary": "",
        "project_purpose_summary_confidence": "unknown",
        "declared_workflows": [],
        "architecture_terms": [],
        "run_instructions": [],
        "named_features": [],
        "external_integrations": [],
        "documentation_files_found": [],
        "documentation_evidence": [],
        "documentation_parse_warnings": [],
    }


def _append_evidence(
    result: dict[str, Any],
    source_file: str,
    field_name: str,
    value: str,
    max_excerpt_chars: int,
) -> None:
    """Support append evidence behavior.
    
    Parameters
    ----------
    result : dict[str, Any]
        The result value.
    source_file : str
        The source file value.
    field_name : str
        The field name value.
    value : str
        The input value.
    max_excerpt_chars : int
        The max excerpt chars value.
    """
    
    result["documentation_evidence"].append(
        {
            "source_file": source_file,
            "field": field_name,
            "value_excerpt": _truncate_text(value, max_excerpt_chars),
        }
    )


def _append_warning(result: dict[str, Any], source_file: str, message: str) -> None:
    """Support append warning behavior.
    
    Parameters
    ----------
    result : dict[str, Any]
        The result value.
    source_file : str
        The source file value.
    message : str
        The message text.
    """
    
    warning = f"{source_file}: {message}" if source_file else message
    result["documentation_parse_warnings"].append(warning)


def _set_if_empty(
    result: dict[str, Any],
    key: str,
    value: str,
    source_file: str,
    max_excerpt_chars: int,
) -> None:
    """Support set if empty behavior.
    
    Parameters
    ----------
    result : dict[str, Any]
        The result value.
    key : str
        The key value.
    value : str
        The input value.
    source_file : str
        The source file value.
    max_excerpt_chars : int
        The max excerpt chars value.
    """
    
    cleaned = value.strip()
    if cleaned and not result.get(key):
        result[key] = cleaned
        _append_evidence(result, source_file, key, cleaned, max_excerpt_chars)


def _merge_list_field(
    result: dict[str, Any],
    field_name: str,
    values: list[str],
    source_file: str,
    max_evidence_snippets: int,
    max_excerpt_chars: int,
) -> None:
    """Support merge list field behavior.
    
    Parameters
    ----------
    result : dict[str, Any]
        The result value.
    field_name : str
        The field name value.
    values : list[str]
        The input values.
    source_file : str
        The source file value.
    max_evidence_snippets : int
        The max evidence snippets value.
    max_excerpt_chars : int
        The max excerpt chars value.
    """
    
    current = list(result[field_name])
    result[field_name] = _dedupe_keep_order(current + values)
    for value in values[:max_evidence_snippets]:
        _append_evidence(result, source_file, field_name, value, max_excerpt_chars)


def _is_ignored_doc_path(path: Path, project_root: Path) -> bool:
    """Support is ignored doc path behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    project_root : Path
        The project root path.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    ignored_parts = {
        ".git",
        ".idea",
        ".venv",
        "venv",
        "__pycache__",
        ".mypy_cache",
        ".pytest_cache",
        "site-packages",
        "build",
        "dist",
        "cache",
        "logs",
        "outputs",
    }

    try:
        relative_parts = path.relative_to(project_root).parts[:-1]
    except Exception:
        relative_parts = path.parts[:-1]

    for part in relative_parts:
        lowered = str(part).strip().lower()
        if lowered in ignored_parts:
            return True
        if lowered.startswith("."):
            return True
    return False


def _discover_doc_files(
    project_root: Path,
    glob_patterns: tuple[str, ...],
) -> list[Path]:
    """Support discover doc files behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    glob_patterns : tuple[str, ...]
        The glob patterns value.
    
    Returns
    -------
    list[Path]
        The list of values.
    """
    
    found: list[Path] = []
    for pattern in glob_patterns:
        for candidate in project_root.glob(pattern):
            if candidate.is_file() and not _is_ignored_doc_path(candidate, project_root):
                found.append(candidate)
        for candidate in project_root.glob(f"**/{pattern}"):
            if candidate.is_file() and not _is_ignored_doc_path(candidate, project_root):
                found.append(candidate)

    unique: dict[str, Path] = {}
    for path in found:
        unique[str(path.resolve()).lower()] = path.resolve()
    return sorted(unique.values(), key=lambda item: str(item).lower())


def _extract_heading_lines(text: str) -> list[str]:
    """Support extract heading lines behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    headings: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#"):
            headings.append(line.lstrip("#").strip())
            continue
        if re.match(r"^[A-Za-z0-9][A-Za-z0-9\s\-_]{2,}$", line):
            headings.append(line)
    return _dedupe_keep_order(headings)


def _extract_run_instructions(text: str) -> list[str]:
    """Support extract run instructions behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    matches: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        lowered = line.lower()
        if not line:
            continue
        if (
            "python " in lowered
            or "pip install" in lowered
            or "pytest" in lowered
            or "uv run" in lowered
            or "poetry run" in lowered
            or "streamlit run" in lowered
            or "flask run" in lowered
            or "uvicorn " in lowered
        ):
            matches.append(line)
    return _dedupe_keep_order(matches)


def _extract_named_features(headings: list[str]) -> list[str]:
    """Support extract named features behavior.
    
    Parameters
    ----------
    headings : list[str]
        The headings value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    features: list[str] = []
    for heading in headings:
        lowered = heading.lower()
        if any(
            keyword in lowered
            for keyword in (
                "feature",
                "capability",
                "workflow",
                "pipeline",
                "module",
                "architecture",
                "overview",
                "system",
            )
        ):
            features.append(heading)
    return _dedupe_keep_order(features)


def _extract_external_integrations(text: str) -> list[str]:
    """Support extract external integrations behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    integrations: list[str] = []
    patterns = (
        "openai",
        "anthropic",
        "ollama",
        "postgres",
        "sqlite",
        "redis",
        "mongodb",
        "docker",
        "fastapi",
        "flask",
        "django",
        "pyside",
        "pyqt",
        "slack",
        "github",
        "gitlab",
        "s3",
        "azure",
        "gcp",
    )
    lowered = text.lower()
    for item in patterns:
        if item in lowered:
            integrations.append(item)
    return _dedupe_keep_order(integrations)


def _extract_architecture_terms(headings: list[str], text: str) -> list[str]:
    """Support extract architecture terms behavior.
    
    Parameters
    ----------
    headings : list[str]
        The headings value.
    text : str
        The text value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    candidates = list(headings)
    patterns = re.findall(
        r"\b(controller|service|manager|builder|registry|router|pipeline|adapter|bridge|collector|parser|orchestrator|plugin|engine|loader)\b",
        text,
        flags=re.IGNORECASE,
    )
    candidates.extend(patterns)
    return _dedupe_keep_order(candidates)


def _extract_first_meaningful_paragraph(text: str) -> str:
    """Support extract first meaningful paragraph behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    str
        The string result.
    """
    
    disallowed_starts = (
        "#",
        "##",
        "###",
        "ai analysis summary",
        "analysis summary",
        "summary",
    )
    blocks = re.split(r"\n\s*\n", text)
    for block in blocks:
        cleaned_lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not cleaned_lines:
            continue
        cleaned = " ".join(cleaned_lines).strip()
        lowered = cleaned.lower()
        if len(cleaned) < 40:
            continue
        if any(lowered.startswith(prefix) for prefix in disallowed_starts):
            continue
        if any(
            marker in lowered
            for marker in (
                "**original file:**",
                "original file:",
                "**created:**",
                "created:",
                "**source file:**",
                "source file:",
                "**generated:**",
                "generated:",
                "last updated:",
                "auto-generated",
                "autogenerated",
            )
        ):
            continue
        if cleaned.startswith("#"):
            continue
        sentence_like = (
            "." in cleaned
            or " is " in lowered
            or " are " in lowered
            or " provides " in lowered
            or " application " in lowered
            or " project " in lowered
            or " tool " in lowered
            or " system " in lowered
        )
        if not sentence_like:
            continue
        return cleaned
    return ""


def _looks_like_vendor_or_font_doc(text: str) -> bool:
    """Support looks like vendor or font doc behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    lowered = text.lower()
    markers = (
        "included fonts",
        "roboto-",
        "font license",
        "font family",
        "open font license",
        "this package contains fonts",
        "ofl.txt",
    )
    return any(marker in lowered for marker in markers)


def _looks_like_cache_or_generated_doc(path: Path, text: str) -> bool:
    """Support looks like cache or generated doc behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    text : str
        The text value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    lowered = text.lower()
    path_low = str(path).replace("\\", "/").lower()
    if any(token in path_low for token in (".pytest_cache", ".mypy_cache", ".ruff_cache", "site-packages")):
        return True
    markers = (
        "pytest's cache plugin",
        "provides the `--lf` and `--ff` options",
        "generated automatically",
        "do not edit this file directly",
        "autogenerated",
    )
    return any(marker in lowered for marker in markers)


def _read_text_best_effort(path: Path) -> tuple[str, str | None]:
    """Support read text best effort behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    tuple[str, str | None]
        The tuple of values.
    """
    
    try:
        return path.read_text(encoding="utf-8", errors="replace"), None
    except Exception as exc:
        return "", str(exc)


def _doc_rank(path: Path, text: str) -> int:
    """Support doc rank behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    text : str
        The text value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    path_low = str(path).replace("\\", "/").lower()
    name_low = path.name.lower()
    score = 0
    if name_low == "readme.md":
        score += 220
    elif name_low.startswith("readme"):
        score += 180
    if any(token in path_low for token in ("/docs/architecture", "adr", "architecture")):
        score += 120
    if "/docs/" in path_low:
        score += 80
    if any(token in path_low for token in ("guide", "onboarding", "overview", "design")):
        score += 40
    if _looks_like_vendor_or_font_doc(text):
        score -= 250
    if _looks_like_cache_or_generated_doc(path, text):
        score -= 300
    if name_low.endswith(".txt"):
        score -= 30
    if _extract_first_meaningful_paragraph(text):
        score += 40
    return score


def _extract_best_purpose_summary(
    candidates: list[tuple[int, str, str]],
) -> tuple[str, str]:
    """Support extract best purpose summary behavior.
    
    Parameters
    ----------
    candidates : list[tuple[int, str, str]]
        The candidates value.
    
    Returns
    -------
    tuple[str, str]
        The tuple of values.
    """
    
    if not candidates:
        return "", "unknown"
    best_rank, _source_file, summary = sorted(candidates, key=lambda item: item[0], reverse=True)[0]
    if best_rank >= 220:
        confidence = "high"
    elif best_rank >= 120:
        confidence = "medium"
    elif best_rank > 0:
        confidence = "low"
    else:
        confidence = "unknown"
    return summary, confidence


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


# PASS_069C_STATIC_CONTEXT_SCOPE_OVERRIDE_START
def _discover_doc_files(root, *args, **kwargs):
    """Support discover doc files behavior.
    
    Parameters
    ----------
    root : object
        The root path.
    *args : object
        The positional arguments.
    **kwargs : object
        The kwargs value.
    """
    
    from kanda_reasoner_app.reasoner_context_collector.collector_scope import iter_project_documentation_files
    return list(iter_project_documentation_files(root))
# PASS_069C_STATIC_CONTEXT_SCOPE_OVERRIDE_END
