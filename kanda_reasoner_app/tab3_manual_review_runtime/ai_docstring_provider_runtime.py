# project-path: kanda_reasoner_app/tab3_manual_review_runtime/ai_docstring_provider_runtime.py
"""AI docstring provider contract for Tab 3 review drafts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import PureWindowsPath
from typing import Callable

from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_style_runtime import (
    apply_ai_docstring_style_contract as _apply_ai_docstring_style_contract,
    normalize_normalized_docstring_for_verbosity as _normalize_normalized_docstring_for_verbosity,
)

__all__ = [
    "AI_DOCSTRING_PROVIDER_CONTRACT",
    "AIProviderRequest",
    "AIProviderResult",
    "ProviderCallable",
    "build_ai_provider_request",
    "build_openai_compatible_messages",
    "fallback_ai_provider_result",
    "generate_ai_docstring_with_fallback",
    "normalize_ai_docstring_output",
    "normalize_ai_docstring_output_for_verbosity",
]

AI_DOCSTRING_PROVIDER_CONTRACT = "tab3_ai_docstring_provider_contract_v1"
ProviderCallable = Callable[["AIProviderRequest"], "AIProviderResult"]


@dataclass(frozen=True)
class AIProviderRequest:
    """Input contract for one AI-assisted docstring draft request."""

    project_root: str
    relative_file_path: str
    symbol_kind: str
    symbol_name: str
    signature: str
    source_snippet: str
    heuristic_draft: str
    docstring_style: str = "numpy"
    docstring_verbosity: str = "concise"


@dataclass(frozen=True)
class AIProviderResult:
    """Output contract for one AI-assisted docstring draft result."""

    provider_name: str
    success: bool
    docstring_body: str
    status: str
    error_message: str = ""
    used_fallback: bool = False


def build_ai_provider_request(
    row: dict,
    module_text: str,
    project_root: str = "",
    heuristic_draft: str = "",
    docstring_style: str = "numpy",
    docstring_verbosity: str = "concise",
) -> AIProviderRequest:
    """Build one provider request from a Tab 3 report row."""
    file_path = str(row.get("file") or row.get("path") or "").strip()
    symbol_name = str(row.get("target_name") or row.get("name") or "module").strip()
    symbol_kind = str(row.get("target_kind") or row.get("kind") or "module").strip()
    signature = str(row.get("signature") or row.get("target_signature") or "").strip()
    line_number = _safe_int(row.get("line") or row.get("insert_line") or 1, 1)
    draft = heuristic_draft or str(
        row.get("draft_docstring") or row.get("suggested_docstring") or ""
    )
    return AIProviderRequest(
        project_root=str(project_root or "").strip(),
        relative_file_path=_relative_file_path(file_path, str(project_root or "")),
        symbol_kind=symbol_kind or "module",
        symbol_name=symbol_name or "module",
        signature=signature,
        source_snippet=_nearby_source(module_text, line_number),
        heuristic_draft=normalize_ai_docstring_output(draft),
        docstring_style=str(docstring_style or "numpy").strip() or "numpy",
        docstring_verbosity=_normalize_verbosity(docstring_verbosity),
    )


def build_openai_compatible_messages(request: AIProviderRequest) -> list[dict[str, str]]:
    """Build provider-neutral messages for an OpenAI-compatible chat endpoint."""
    verbosity = _normalize_verbosity(request.docstring_verbosity)
    system = (
        "You generate Python docstrings for human review. "
        "Return only the docstring body. Do not include triple quotes, markdown, "
        "source code, explanations, invented parameters, or invented behavior. "
        "Keep NumPy-style section headers when parameters or returns are present. "
        + _verbosity_system_instruction(verbosity)
    )
    user = "\n".join(
        [
            "Create one docstring draft for the selected Python symbol.",
            "Style: " + request.docstring_style,
            "Verbosity: " + verbosity,
            _verbosity_user_contract(verbosity),
            "File: " + request.relative_file_path,
            "Symbol kind: " + request.symbol_kind,
            "Symbol name: " + request.symbol_name,
            "Signature: " + (request.signature or "<unknown>"),
            "Frozen heuristic draft:",
            request.heuristic_draft or "<none>",
            "Source snippet:",
            request.source_snippet,
        ]
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def generate_ai_docstring_with_fallback(
    request: AIProviderRequest,
    provider: ProviderCallable,
    fallback_provider_name: str = "heuristic_fallback",
) -> AIProviderResult:
    """Return a provider result, falling back to the heuristic draft on failure."""
    try:
        result = provider(request)
    except Exception as exc:
        return fallback_ai_provider_result(
            request,
            fallback_provider_name,
            "provider raised " + exc.__class__.__name__,
        )
    body = _apply_ai_docstring_style_contract(
        normalize_ai_docstring_output(result.docstring_body), request
    )
    if result.success and body:
        return AIProviderResult(
            provider_name=result.provider_name or "unknown_ai_provider",
            success=True,
            docstring_body=body,
            status=result.status or "ai_draft_generated",
            error_message=result.error_message,
            used_fallback=False,
        )
    return fallback_ai_provider_result(
        request,
        fallback_provider_name,
        result.error_message or result.status or "provider returned no usable docstring",
    )


def fallback_ai_provider_result(
    request: AIProviderRequest,
    provider_name: str = "heuristic_fallback",
    error_message: str = "AI provider unavailable.",
) -> AIProviderResult:
    """Return a fallback result using the frozen heuristic draft."""
    body = normalize_ai_docstring_output_for_verbosity(
        request.heuristic_draft, request.docstring_verbosity
    )
    return AIProviderResult(
        provider_name=provider_name,
        success=bool(body),
        docstring_body=body,
        status="AI UNAVAILABLE - HEURISTIC FALLBACK" if body else "AI DRAFT UNAVAILABLE",
        error_message=str(error_message or ""),
        used_fallback=True,
    )


def normalize_ai_docstring_output(text: str) -> str:
    """Normalize AI output to a docstring body without quotes or code fences."""
    value = str(text or "").strip()
    if not value:
        return ""
    value = _strip_markdown_fence(value)
    value = _extract_first_triple_quoted_body(value)
    value = _strip_outer_single_line_quotes(value)
    value = _drop_explanation_tail(value)
    value = _drop_source_wrapper_lines(value)
    return _normalize_body_indentation(value).strip()


def normalize_ai_docstring_output_for_verbosity(text: str, verbosity: str) -> str:
    """Normalize AI output and apply deterministic verbosity safety rules."""
    return _normalize_normalized_docstring_for_verbosity(
        normalize_ai_docstring_output(text), verbosity
    )


def _normalize_verbosity(value: str) -> str:
    """Return a supported AI docstring verbosity value."""
    normalized = str(value or "").strip().lower()
    if normalized in {"concise", "balanced", "detailed"}:
        return normalized
    return "concise"


def _verbosity_system_instruction(verbosity: str) -> str:
    """Return prompt guidance for the requested docstring verbosity."""
    if verbosity == "detailed":
        return (
            "VERBOSITY CONTRACT: DETAILED. Use a detailed but reviewable "
            "docstring. Produce a visibly more detailed docstring than concise mode. Use one summary sentence, then one "
            "short explanatory paragraph when source behavior is visible, then "
            "NumPy-style Parameters and Returns sections when applicable. Keep "
            "the text factual and reviewable; do not invent behavior."
        )
    if verbosity == "balanced":
        return (
            "VERBOSITY CONTRACT: BALANCED. Produce a middle-length docstring. "
            "Use one summary sentence and concise NumPy-style Parameters and "
            "Returns sections when applicable. Avoid long explanatory paragraphs; "
            "one short behavior sentence is allowed only when useful."
        )
    return (
        "VERBOSITY CONTRACT: CONCISE. Use a concise docstring. Produce the shortest useful docstring. "
        "For modules and classes, prefer one sentence only. For functions and "
        "methods, use one short summary plus only necessary NumPy-style "
        "Parameters and Returns sections. Avoid extra explanatory paragraphs. Do not include an explanatory paragraph."
    )


def _verbosity_user_contract(verbosity: str) -> str:
    """Return a user-message contract that makes style differences explicit."""
    if verbosity == "detailed":
        return (
            "Detailed output shape: summary sentence, one short explanatory "
            "paragraph when behavior is visible, then NumPy-style sections. "
            "Do not reuse a concise one-line answer for detailed mode."
        )
    if verbosity == "balanced":
        return (
            "Balanced output shape: summary sentence, concise NumPy-style "
            "sections, and no long explanatory paragraph."
        )
    return (
        "Concise output shape: shortest useful answer. No explanatory paragraph. "
        "For a simple module/class, one sentence is enough."
    )


def _strip_markdown_fence(value: str) -> str:
    """Remove one surrounding markdown code fence if present."""
    stripped = value.strip()
    if not stripped.startswith("```"):
        return stripped
    lines = stripped.splitlines()
    if len(lines) >= 2 and lines[-1].strip().startswith("```"):
        return "\n".join(lines[1:-1]).strip()
    return stripped.strip("`").strip()


def _extract_first_triple_quoted_body(value: str) -> str:
    """Extract the first triple-quoted body from model output when present."""
    for marker in ('"""', "'''"):
        start = value.find(marker)
        if start < 0:
            continue
        body_start = start + len(marker)
        end = value.find(marker, body_start)
        if end >= 0:
            return value[body_start:end].strip()
    return value.strip()


def _strip_outer_single_line_quotes(value: str) -> str:
    """Strip simple matching single-line quote wrappers."""
    stripped = value.strip()
    if len(stripped) >= 2 and stripped[0] == stripped[-1] and stripped[0] in ('"', "'"):
        return stripped[1:-1].strip()
    return stripped


def _drop_explanation_tail(value: str) -> str:
    """Remove common explanatory tails after the docstring body."""
    stop_prefixes = (
        "explanation:",
        "rationale:",
        "notes:",
        "here is",
        "the docstring",
    )
    kept: list[str] = []
    for line in value.splitlines():
        if line.strip().lower().startswith(stop_prefixes):
            break
        kept.append(line)
    return "\n".join(kept).strip()


def _drop_source_wrapper_lines(value: str) -> str:
    """Drop source-code wrapper lines if the model returned a code fragment."""
    dropped_prefixes = ("def ", "async def ", "class ", "return ")
    lines = []
    for line in value.splitlines():
        if line.lstrip().startswith(dropped_prefixes):
            continue
        if line.strip() in ("pass", "...", "}", ")"):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def _normalize_body_indentation(value: str) -> str:
    """Remove common indentation from a multiline docstring body."""
    lines = value.expandtabs(4).splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    indents = [len(line) - len(line.lstrip(" ")) for line in lines if line.strip()]
    margin = min(indents) if indents else 0
    if margin <= 0:
        return "\n".join(lines)
    return "\n".join(line[margin:] if len(line) >= margin else line for line in lines)


def _nearby_source(module_text: str, line_number: int) -> str:
    """Return a bounded source snippet around a 1-based line number."""
    lines = str(module_text or "").splitlines()
    if not lines:
        return ""
    index = max(0, line_number - 1)
    start = max(0, index - 8)
    end = min(len(lines), index + 18)
    return "\n".join(lines[start:end])


def _relative_file_path(file_path: str, project_root: str) -> str:
    """Return a stable relative file path for Windows-style or POSIX paths."""
    raw_file = str(file_path or "").strip().replace("\\", "/")
    raw_root = str(project_root or "").strip().replace("\\", "/")
    if raw_file and raw_root and raw_file.lower().startswith(raw_root.rstrip("/").lower() + "/"):
        return raw_file[len(raw_root.rstrip("/")) + 1 :]
    if raw_file:
        try:
            return str(PureWindowsPath(raw_file)).replace("\\", "/")
        except ValueError:
            return raw_file
    return ""


def _safe_int(value: object, default: int) -> int:
    """Return an integer value or a default."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default
