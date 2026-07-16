# project-path: kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/query_intents.py
"""Classify retrieval-intent shapes while preserving the public facade."""

# -----------------------------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/reasoner_engine/reasoner_retriever.py
# MANIFEST      : kanda_reasoner_app/reasoner_engine/reasoner_retriever_help.json
# HELP FOLDER   : kanda_reasoner_app/reasoner_engine/reasoner_retriever_help
# PURPOSE       : Preserve public query-intent imports and aggregate detections.
# DEPENDS ON    : _query_intent_location_and_explanation.py, query_text.py
# REFACTOR DATE : 2026-07-11
# -----------------------------------------------------------------------------
from __future__ import annotations

import re

from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help._query_intent_location_and_explanation import (
    _is_code_localized_explanation_question,
    _is_explain_chain_question,
    _is_explanatory_question,
    _is_topomap_explanation_question,
    _is_topomap_implementation_question,
    _is_where_is_called_question,
    _is_where_is_question,
    _is_which_method_calls_question,
)
from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.query_text import norm_text

__all__ = [
    "is_startup_question",
    "is_explicit_call_chain_question",
    "is_main_window_show_responsibility_question",
    "is_qtimer_showmaximized_question",
    "is_where_is_called_question",
    "is_where_is_question",
    "is_which_method_calls_question",
    "is_explain_chain_question",
    "is_explanatory_question",
    "is_code_localized_explanation_question",
    "is_topomap_explanation_question",
    "is_topomap_implementation_question",
    "is_runtime_heavy_question",
    "is_packaging_metadata_question",
    "is_documentation_intent_question",
    "detect_query_intents",
]

def is_startup_question(q: str) -> bool:
    """Return whether startup question.
    
    Parameters
    ----------
    q : str
        The q value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    startup_terms = [
        "startup",
        "start up",
        "main entry",
        "entry point",
        "main window",
        "launch",
        "open app",
        "application start",
        "app start",
        "until the main window is shown",
        "until main window is shown",
        "qapplication",
        "showmaximized",
        "show(",
    ]
    return any(term in q for term in startup_terms)

def is_explicit_call_chain_question(q: str) -> bool:
    """Return whether explicit call chain question.
    
    Parameters
    ----------
    q : str
        The q value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    call_chain_terms = [
        "self.v.main_window.show()",
        "self.v.main_window.show",
        "calls self.v.main_window.show",
        "method that calls self.v.main_window.show",
    ]
    return any(term in q for term in call_chain_terms)

def is_main_window_show_responsibility_question(q: str) -> bool:
    """Return whether main window show responsibility question.
    
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
        "showing the main window",
        "responsible for showing the main window",
        "method most directly responsible for showing the main window",
        "symbol most directly responsible for showing the main window",
        "main window is shown",
    ]
    return any(term in q for term in terms)

def _matches_delayed_main_window_maximize_question(q: str) -> bool:
    """Return whether the normalized query names the delayed maximize call."""
    return "qtimer.singleshot" in q and "self.v.main_window.showmaximized" in q


def is_qtimer_showmaximized_question(q: str) -> bool:
    """Return whether qtimer showmaximized question.
    
    Parameters
    ----------
    q : str
        The q value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    return _matches_delayed_main_window_maximize_question(q)

def is_where_is_called_question(q: str) -> bool:
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
    return _is_where_is_called_question(q)

def is_where_is_question(q: str) -> bool:
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
    return _is_where_is_question(q)

def is_which_method_calls_question(q: str) -> bool:
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
    return _is_which_method_calls_question(q)

def is_explain_chain_question(q: str) -> bool:
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
    return _is_explain_chain_question(q)

def is_explanatory_question(q: str) -> bool:
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
    return _is_explanatory_question(q)

def is_code_localized_explanation_question(q: str) -> bool:
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
    return _is_code_localized_explanation_question(q)

def is_topomap_explanation_question(q: str) -> bool:
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
    return _is_topomap_explanation_question(q)

def is_topomap_implementation_question(q: str) -> bool:
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
    return _is_topomap_implementation_question(q)

def is_runtime_heavy_question(q: str) -> bool:
    """Return whether runtime heavy question.
    
    Parameters
    ----------
    q : str
        The q value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    q = norm_text(q)

    generic_terms = [
        "runtime",
        "signal",
        "slot",
        "connect",
        "disconnect",
        "emit",
        "timer",
        "thread",
        "event loop",
        "callback",
        "handler",
        "listener",
        "probe",
        "trace at runtime",
        "runtime trace",
        "execution at runtime",
    ]

    if any(term in q for term in generic_terms):
        return True

    if re.search(r"\bon_[a-z0-9_]+\b", q):
        return True

    return False

def is_packaging_metadata_question(q: str) -> bool:
    """Return whether packaging metadata question.
    
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
        "package metadata",
        "packaging metadata",
        "package info",
        "packaging info",
        "dependency",
        "dependencies",
        "requirements",
        "pyproject",
        "setup.py",
        "setup.cfg",
        "pipfile",
        "poetry.lock",
        "uv.lock",
        "build backend",
        "entrypoint",
        "entry point",
        "console script",
        "gui script",
        "tooling",
        "package manager",
        "declared dependency",
        "declared dependencies",
    ]
    return any(term in q for term in terms)

def is_documentation_intent_question(q: str) -> bool:
    """Return whether documentation intent question.
    
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
        "readme",
        "documentation",
        "docs",
        "project purpose",
        "what does this project do",
        "what is this project for",
        "run instructions",
        "architecture terms",
        "named features",
        "external integrations",
        "workflow described",
        "documentation intent",
        "adr",
        "architecture doc",
    ]
    return any(term in q for term in terms)

def detect_query_intents(q: str) -> dict[str, bool]:
    """Detect the query intents.
    
    Parameters
    ----------
    q : str
        The q value.
    
    Returns
    -------
    dict[str, bool]
        The mapped values.
    """
    
    q = norm_text(q)

    return {
        "where_is": is_where_is_question(q),
        "which_calls": is_which_method_calls_question(q),
        "explain_chain": is_explain_chain_question(q),
        "startup": is_startup_question(q),
        "explicit_call_chain": is_explicit_call_chain_question(q),
        "main_window_show": is_main_window_show_responsibility_question(q),
        "qtimer_showmaximized": _matches_delayed_main_window_maximize_question(q),
        "topomap_explanation": is_topomap_explanation_question(q),
        "topomap_implementation": is_topomap_implementation_question(q),
        "explanatory": is_explanatory_question(q),
        "code_localized_explanation": is_code_localized_explanation_question(q),
        "runtime_heavy": is_runtime_heavy_question(q),
        "packaging_metadata": is_packaging_metadata_question(q),
        "documentation_intent": is_documentation_intent_question(q),
        "uncertainty": (
            "uncertainty" in q
            or "unclear" in q
            or "ambiguous" in q
            or "warning" in q
            or "exception" in q
            or "risk" in q
            or "unknown" in q
        ),
    }
