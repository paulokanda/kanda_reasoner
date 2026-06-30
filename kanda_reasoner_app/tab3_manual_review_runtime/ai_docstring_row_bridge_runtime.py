# project-path: kanda_reasoner_app/tab3_manual_review_runtime/ai_docstring_row_bridge_runtime.py
"""Bridge AI docstring provider results into Tab 3 review rows."""

from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_provider_runtime import (
    AIProviderRequest,
    AIProviderResult,
    ProviderCallable,
    build_ai_provider_request,
    generate_ai_docstring_with_fallback,
    normalize_ai_docstring_output,
)
from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_style_runtime import (
    apply_ai_docstring_style_contract,
    selected_ai_docstring_verbosity_from_owner,
)
from kanda_reasoner_app.tab3_manual_review_runtime.ai_style_diagnostics_runtime import (
    append_ai_style_trace,
    source_names_from_snippet,
    short_trace_text,
)

__all__ = [
    "AI_DOCSTRING_ROW_BRIDGE_CONTRACT",
    "apply_ai_result_to_review_row",
    "build_review_row_ai_request",
    "generate_ai_review_draft_for_row",
]

AI_DOCSTRING_ROW_BRIDGE_CONTRACT = "tab3_ai_docstring_row_bridge_v1"


def build_review_row_ai_request(
    owner: object,
    row: dict,
    module_text: str,
    heuristic_draft: str = "",
) -> AIProviderRequest:
    """Build an AI provider request from one selected review row."""
    return build_ai_provider_request(
        row=row,
        module_text=module_text,
        project_root=_project_root_for_owner(owner),
        heuristic_draft=_best_existing_heuristic_draft(row, heuristic_draft, module_text),
        docstring_style=_docstring_style_for_owner(owner),
        docstring_verbosity=_docstring_verbosity_for_owner(owner),
    )


def generate_ai_review_draft_for_row(
    owner: object,
    row: dict,
    module_text: str,
    provider: ProviderCallable | None = None,
) -> str:
    """Generate one AI review draft and store provider state on the row.

    This bridge does not modify source files. When no real provider is attached
    yet, or when the provider fails, it stores a fallback result using the
    frozen heuristic draft so the preview remains usable.
    """
    heuristic_draft = _best_existing_heuristic_draft(row, "", module_text)
    request = build_review_row_ai_request(owner, row, module_text, heuristic_draft)
    append_ai_style_trace(
        owner,
        "request",
        style=request.docstring_verbosity,
        kind=request.symbol_kind,
        name=request.symbol_name,
        signature=request.signature or "<none>",
        source_len=len(request.source_snippet),
        source_names=source_names_from_snippet(request.source_snippet),
        heuristic=short_trace_text(request.heuristic_draft),
    )
    active_provider = provider or _provider_from_owner(owner) or _unavailable_provider
    result = generate_ai_docstring_with_fallback(request, active_provider)
    append_ai_style_trace(
        owner,
        "provider_result",
        provider=result.provider_name,
        success=result.success,
        fallback=result.used_fallback,
        status=result.status,
        raw=short_trace_text(result.docstring_body),
    )
    apply_ai_result_to_review_row(row, result, request, owner)
    _append_output(owner, "[review] AI draft style: " + request.docstring_verbosity + "\n")
    return str(row.get("draft_docstring") or result.docstring_body)


def apply_ai_result_to_review_row(
    row: dict,
    result: AIProviderResult,
    request: AIProviderRequest | None = None,
    owner: object | None = None,
) -> None:
    """Store one AI provider result on a mutable review row."""
    body = normalize_ai_docstring_output(result.docstring_body)
    normalized_body = body
    if request is not None:
        body = apply_ai_docstring_style_contract(body, request)
        row["ai_docstring_verbosity"] = request.docstring_verbosity
    if owner is not None:
        append_ai_style_trace(
            owner,
            "row_store",
            style=row.get("ai_docstring_verbosity", ""),
            normalized=short_trace_text(normalized_body),
            styled=short_trace_text(body),
            changed=normalized_body != body,
        )
    row["ai_draft_docstring"] = body
    row["ai_provider"] = result.provider_name
    row["ai_status"] = result.status
    row["ai_error"] = result.error_message
    row["ai_used_fallback"] = bool(result.used_fallback)
    row["selected_draft_source"] = "heuristic_fallback" if result.used_fallback else "ai"
    if body:
        row["draft_docstring"] = body


def _best_existing_heuristic_draft(row: dict, preferred: str, module_text: str) -> str:
    """Return the best available deterministic draft for fallback/context."""
    for value in (
        preferred,
        row.get("suggested_docstring"),
        row.get("docstring"),
    ):
        body = normalize_ai_docstring_output(str(value or ""))
        if body:
            return body
    try:
        from kanda_reasoner_app.tab3_manual_review_runtime import heuristic_suggestion

        return normalize_ai_docstring_output(
            heuristic_suggestion._suggest_manual_review_heuristic(row, module_text)
        )
    except Exception:
        return "Support the selected object behavior."


def _provider_from_owner(owner: object) -> ProviderCallable | None:
    """Return an attached or Local AI provider callable for one review row."""
    for name in ("_ai_docstring_provider", "ai_docstring_provider"):
        provider = getattr(owner, name, None)
        if callable(provider):
            return provider
    try:
        from kanda_reasoner_app.tab3_manual_review_runtime import (
            ai_openai_compatible_provider_runtime,
        )

        return ai_openai_compatible_provider_runtime.local_openai_compatible_provider_from_owner(owner)
    except Exception:
        return None


def _unavailable_provider(request: AIProviderRequest) -> AIProviderResult:
    """Return a failed provider result so the contract fallback is used."""
    del request
    return AIProviderResult(
        provider_name="local_ai_unavailable",
        success=False,
        docstring_body="",
        status="AI provider not connected yet.",
        error_message="No AI docstring provider is connected.",
        used_fallback=False,
    )


def _project_root_for_owner(owner: object) -> str:
    """Return the active project root text from Tab 3 owner controls."""
    for name in ("_root_path_edit", "root_path_edit", "_project_root_edit"):
        widget = getattr(owner, name, None)
        text_method = getattr(widget, "text", None)
        if callable(text_method):
            value = str(text_method() or "").strip()
            if value:
                return value
    value = str(getattr(owner, "project_root", "") or "").strip()
    if value:
        return value
    return str(Path.cwd())


def _docstring_style_for_owner(owner: object) -> str:
    """Return the selected docstring style, defaulting to numpy."""
    for name in ("_docstring_style_combo", "docstring_style_combo"):
        widget = getattr(owner, name, None)
        current_text = getattr(widget, "currentText", None)
        if callable(current_text):
            value = str(current_text() or "").strip()
            if value:
                return value
    return "numpy"


def _docstring_verbosity_for_owner(owner: object) -> str:
    """Return selected AI docstring verbosity, defaulting to concise."""
    return selected_ai_docstring_verbosity_from_owner(owner)


def _append_output(owner: object, text: str) -> None:
    """Append text to the Tab 3 output when possible."""
    append_text = getattr(owner, "_append_text", None)
    if callable(append_text):
        append_text(text)
