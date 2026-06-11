"""Support V10 project reasoning and evidence handling."""

from __future__ import annotations

import re
from typing import Any

__all__ = [
    "norm_text",
    "tokenize_query",
    "is_which_method_calls_question",
    "is_code_localized_explanation_question",
    "is_explain_implementation_question",
    "is_chain_or_flow_question",
]


def norm_text(text: Any) -> str:
    return str(text).strip().lower() if text is not None else ""


def tokenize_query(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9_\.]+", norm_text(text))


def is_which_method_calls_question(question: str) -> bool:
    q = norm_text(question)
    triggers = [
        "which method calls",
        "which function calls",
        "who calls",
        "what calls",
        "what exact snippet shows that call site",
        "call site",
    ]
    return any(trigger in q for trigger in triggers) and (
        "call" in q or "calls" in q or "called" in q
    )


def is_code_localized_explanation_question(question: str) -> bool:
    q = norm_text(question)

    explanation_terms = [
        "explain",
        "trace",
        "walk through",
        "describe",
        "flow",
        "chain",
        "implementation",
        "implemented",
        "what code shows",
    ]

    code_terms = [
        "with code",
        "show code",
        "include code",
        "code localization",
        "code and code localization",
        "with code and code localization",
        "code evidence",
        "with code evidence",
        "line-level snippet",
        "line-level snippets",
        "line level snippet",
        "line level snippets",
        "where in code",
        "snippet",
        "snippets",
        "what code shows",
    ]

    return any(term in q for term in explanation_terms) and any(
        term in q for term in code_terms
    )


def is_explain_implementation_question(question: str) -> bool:
    q = norm_text(question)
    triggers = [
        "explain the implementation of",
        "explain implementation of",
        "describe the implementation of",
        "summarize the implementation of",
    ]
    return any(trigger in q for trigger in triggers)


def is_chain_or_flow_question(question: str) -> bool:
    q = norm_text(question)
    triggers = [
        "startup chain",
        "trace the chain",
        "explain the chain",
        "flow from",
        "sequence from",
        "describe the chain",
        "trace the flow",
        "describe the flow",
        "timeline chain",
        "reset chain",
        "cleanup chain",
        "reset flow",
        "cleanup flow",
        "what code shows the reset flow",
        "what code shows the cleanup flow",
    ]
    return any(trigger in q for trigger in triggers)


