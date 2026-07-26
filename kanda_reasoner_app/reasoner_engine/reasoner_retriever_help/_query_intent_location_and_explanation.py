# project-path: kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/_query_intent_location_and_explanation.py
"""Implement private location, explanation, and topomap intent predicates.

The public functions remain owned by query_intents.py. This module contains
only subordinate predicate implementations and does not import the facade.
"""
from __future__ import annotations

def _is_where_is_called_question(q: str) -> bool:
    """Return whether where is called question.
    
    Parameters
    ----------
    q : str
        The q value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    terms = [
        "who calls ",
        "where is ",
        "where is the ",
        "where is this ",
        "where is it called",
        "where is it invoked",
        "where is actually called",
        "where is actually invoked",
        "called in ",
        "invoked in ",
        "references ",
        "reference to ",
        "who invokes ",
    ]
    return any(term in q for term in terms) and (
        "call" in q or "called" in q or "invoke" in q or "invoked" in q or "reference" in q
    )

def _is_where_is_question(q: str) -> bool:
    """Return whether where is question.
    
    Parameters
    ----------
    q : str
        The q value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    terms = [
        "where is ",
        "where is the ",
        "where is this ",
        "where defined",
        "where is defined",
        "where is declared",
        "in which file is",
        "what file defines",
        "which file defines",
        "what file contains",
        "which file contains",
        "what file records",
        "which file records",
        "what file has",
        "which file has",
        "what file includes",
        "which file includes",
        "what file is the source of",
        "which file is the source of",
        "where implemented",
        "where is implemented",
    ]
    return any(term in q for term in terms)

def _is_which_method_calls_question(q: str) -> bool:
    """Return whether which method calls question.
    
    Parameters
    ----------
    q : str
        The q value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    terms = [
        "which method calls",
        "what method calls",
        "which function calls",
        "what function calls",
        "who calls",
        "directly calls",
        "calls qtimer.singleshot",
        "calls self.",
    ]
    return any(term in q for term in terms)

def _is_explain_chain_question(q: str) -> bool:
    """Return whether explain chain question.
    
    Parameters
    ----------
    q : str
        The q value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    terms = [
        "explain chain",
        "explain the chain",
        "trace the chain",
        "trace the startup",
        "startup chain",
        "execution chain",
        "call chain",
        "flow from",
        "sequence from",
        "explain directly in plain prose the chain",
        "timeline chain",
        "reset chain",
        "cleanup chain",
    ]
    return any(term in q for term in terms)

def _is_explanatory_question(q: str) -> bool:
    """Return whether explanatory question.
    
    Parameters
    ----------
    q : str
        The q value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    terms = [
        "explain",
        "trace",
        "summarize",
        "describe",
        "walk through",
        "architecture",
        "flow",
        "chain",
        "implementation of",
        "responsibility split",
    ]
    return any(term in q for term in terms)

def _is_code_localized_explanation_question(q: str) -> bool:
    """Return whether code localized explanation question.
    
    Parameters
    ----------
    q : str
        The q value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    explanation_terms = [
        "explain",
        "trace",
        "walk through",
        "describe",
        "summarize",
        "implementation",
        "flow",
        "chain",
    ]
    code_terms = [
        "with code",
        "show code",
        "include code",
        "code localization",
        "code location",
        "where in code",
        "show snippets",
        "show snippet",
        "line numbers",
        "file path and code",
        "symbol and code",
        "code evidence",
        "with code evidence",
        "line-level snippet",
        "line-level snippets",
        "line level snippet",
        "line level snippets",
    ]
    return any(term in q for term in explanation_terms) and any(term in q for term in code_terms)

def _is_topomap_explanation_question(q: str) -> bool:
    """Return whether topomap explanation question.
    
    Parameters
    ----------
    q : str
        The q value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    if "topomap" not in q and "amplitude map" not in q:
        return False

    implementation_terms = [
        "implement",
        "implements",
        "implemented",
        "implementation",
        "creating",
        "updating",
        "participate in creating",
        "participate in updating",
        "modules participate",
        "which code implements",
        "which modules participate",
    ]

    return (
        _is_explanatory_question(q)
        or any(term in q for term in implementation_terms)
    )

def _is_topomap_implementation_question(q: str) -> bool:
    """Return whether topomap implementation question.
    
    Parameters
    ----------
    q : str
        The q value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    if "topomap" not in q and "amplitude map" not in q:
        return False

    terms = [
        "implement",
        "implements",
        "implemented",
        "implementation",
        "which code implements",
        "which modules participate",
        "participate in creating",
        "participate in updating",
        "creating",
        "updating",
    ]
    return any(term in q for term in terms)
