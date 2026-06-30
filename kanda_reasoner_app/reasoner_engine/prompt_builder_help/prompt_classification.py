# project-path: kanda_reasoner_app/reasoner_engine/prompt_builder_help/prompt_classification.py
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
    """Support norm text behavior.
    
    Parameters
    ----------
    text : Any
        The text value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return str(text).strip().lower() if text is not None else ""


def tokenize_query(text: str) -> list[str]:
    """Support tokenize query behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    return re.findall(r"[a-zA-Z0-9_\.]+", norm_text(text))


def is_which_method_calls_question(question: str) -> bool:
    """Return whether which method calls question.
    
    Parameters
    ----------
    question : str
        The question value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
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
    """Return whether code localized explanation question.
    
    Parameters
    ----------
    question : str
        The question value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
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
    """Return whether explain implementation question.
    
    Parameters
    ----------
    question : str
        The question value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    q = norm_text(question)
    triggers = [
        "explain the implementation of",
        "explain implementation of",
        "describe the implementation of",
        "summarize the implementation of",
    ]
    return any(trigger in q for trigger in triggers)


def is_chain_or_flow_question(question: str) -> bool:
    """Return whether chain or flow question.
    
    Parameters
    ----------
    question : str
        The question value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
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


