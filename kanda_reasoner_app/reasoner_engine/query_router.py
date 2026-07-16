# project-path: kanda_reasoner_app/reasoner_engine/query_router.py
"""Support V10 project reasoning and evidence handling."""

from __future__ import annotations

from dataclasses import dataclass

from kanda_reasoner_app.reasoner_engine._query_router_rules import (
    CODE_EXPLANATION_TERMS,
    CODE_LOCALIZATION_TERMS,
    DISCOVERY_TERMS,
    EXPLANATORY_CORE_TERMS,
    EXPLANATORY_TERMS,
    FILE_LOCATOR_TERMS,
    RESPONSIBILITY_TERMS,
    SIGNAL_ACTION_TERMS,
    SYMBOL_LOCATOR_TERMS,
    WHICH_CALLS_TERMS,
    WHICH_CALLS_WITH_CODE_EXTRA_TERMS,
    WIDGET_LISTING_TERMS,
    code_localization_matches as _code_localization_matches,
    exact_file_locator_matches as _exact_file_locator_matches,
    exact_symbol_locator_matches as _exact_symbol_locator_matches,
    explanatory_matches as _explanatory_matches,
    has_any_term as _has_any_term,
    listing_or_discovery_matches as _listing_or_discovery_matches,
    norm_text as _norm_text,
    one_line_locator_matches as _one_line_locator_matches,
    responsibility_matches as _responsibility_matches,
    signal_or_action_matches as _signal_or_action_matches,
    which_calls_matches as _which_calls_matches,
    widget_listing_matches as _widget_listing_matches,
)

__all__ = [
    "QueryRouteDecision",
    "route_query_intent",
    "is_one_line_locator_question",
    "is_exact_file_locator_question",
    "is_exact_symbol_locator_question",
    "is_which_calls_question",
    "is_signal_or_action_question",
    "is_responsibility_question",
    "is_widget_listing_question",
    "is_listing_or_discovery_question",
    "is_explanatory_question",
    "is_code_localization_question",
    "is_locator_plus_explanation_question",
]

@dataclass(frozen=True)
class QueryRouteDecision:
    """Represent query route decision."""
    
    route: str
    intent_name: str
    reason: str


def _norm(text: str) -> str:
    """Support norm behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    str
        The string result.
    """

    return _norm_text(text)

def _has_any(text: str, terms: tuple[str, ...]) -> bool:
    """Support has any behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    terms : tuple[str, ...]
        The terms value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """

    return _has_any_term(text, terms)

def _which_calls_needs_code_answer(q: str) -> bool:
    """Support which calls needs code answer behavior.
    
    Parameters
    ----------
    q : str
        The q value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return (
        is_code_localization_question(q)
        or is_explanatory_question(q)
        or _has_any(q, WHICH_CALLS_WITH_CODE_EXTRA_TERMS)
    )


def is_one_line_locator_question(q: str) -> bool:
    """Return whether one line locator question.
    
    Parameters
    ----------
    q : str
        The q value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """

    return _one_line_locator_matches(q)

def is_exact_file_locator_question(q: str) -> bool:
    """Return whether exact file locator question.
    
    Parameters
    ----------
    q : str
        The q value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """

    return _exact_file_locator_matches(q)

def is_exact_symbol_locator_question(q: str) -> bool:
    """Return whether exact symbol locator question.
    
    Parameters
    ----------
    q : str
        The q value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """

    return _exact_symbol_locator_matches(q)

def is_which_calls_question(q: str) -> bool:
    """Return whether which calls question.
    
    Parameters
    ----------
    q : str
        The q value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """

    return _which_calls_matches(q)

def is_signal_or_action_question(q: str) -> bool:
    """Return whether signal or action question.
    
    Parameters
    ----------
    q : str
        The q value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """

    return _signal_or_action_matches(q)

def is_responsibility_question(q: str) -> bool:
    """Return whether responsibility question.
    
    Parameters
    ----------
    q : str
        The q value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """

    return _responsibility_matches(q)

def is_widget_listing_question(q: str) -> bool:
    """Return whether widget listing question.
    
    Parameters
    ----------
    q : str
        The q value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """

    return _widget_listing_matches(q)

def is_listing_or_discovery_question(q: str) -> bool:
    """Return whether listing or discovery question.
    
    Parameters
    ----------
    q : str
        The q value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """

    return _listing_or_discovery_matches(q)

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

    return _explanatory_matches(q)

def is_code_localization_question(q: str) -> bool:
    """Return whether code localization question.
    
    Parameters
    ----------
    q : str
        The q value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """

    return _code_localization_matches(q)

def is_locator_plus_explanation_question(q: str) -> bool:
    """Return whether locator plus explanation question.
    
    Parameters
    ----------
    q : str
        The q value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return is_exact_file_locator_question(q) and (
        is_code_localization_question(q)
        or is_explanatory_question(q)
        or "flow" in q
        or "chain" in q
        or "what code shows" in q
    )


def route_query_intent(question: str) -> QueryRouteDecision:
    """Support route query intent behavior.
    
    Parameters
    ----------
    question : str
        The question value.
    
    Returns
    -------
    QueryRouteDecision
        The query route decision result.
    """

    q = _norm(question)
    return _run_query_route(q)


def _run_query_route(q: str) -> QueryRouteDecision:
    """Apply the preserved query-route precedence tree."""
    if is_one_line_locator_question(q):
        return QueryRouteDecision(
            route="deterministic",
            intent_name="one_line_locator",
            reason="Strict exact-output locator question.",
        )
    if is_which_calls_question(q):
        if _which_calls_needs_code_answer(q):
            return QueryRouteDecision(
                route="generative",
                intent_name="which_calls_with_code",
                reason="Caller lookup question also requests snippet/code evidence.",
            )
    
        return QueryRouteDecision(
            route="deterministic",
            intent_name="which_calls",
            reason="Exact call-site lookup question.",
        )
    if is_locator_plus_explanation_question(q):
        return QueryRouteDecision(
            route="generative",
            intent_name="locator_plus_explanation",
            reason="Locator question also requests explanation/flow/code evidence.",
        )
    if is_exact_file_locator_question(q):
        return QueryRouteDecision(
            route="deterministic",
            intent_name="exact_file_locator",
            reason="Exact file or location lookup question.",
        )
    if is_exact_symbol_locator_question(q):
        return QueryRouteDecision(
            route="deterministic",
            intent_name="exact_symbol_locator",
            reason="Exact symbol lookup question.",
        )
    if is_widget_listing_question(q):
        return QueryRouteDecision(
            route="generative",
            intent_name="widget_listing",
            reason="Widget/button listing question requiring synthesized answer.",
        )
    if is_code_localization_question(q):
        return QueryRouteDecision(
            route="generative",
            intent_name="code_localized_explanation",
            reason="Explanation requested with code and localization.",
        )
    if is_signal_or_action_question(q):
        return QueryRouteDecision(
            route="generative",
            intent_name="signal_action",
            reason="Signal, slot, or Qt action question.",
        )
    if is_listing_or_discovery_question(q):
        return QueryRouteDecision(
            route="ranked",
            intent_name="discovery",
            reason="Discovery question with multiple likely candidates.",
        )
    if is_explanatory_question(q):
        return QueryRouteDecision(
            route="generative",
            intent_name="explanation",
            reason="Explanation or synthesis question.",
        )
    return QueryRouteDecision(
        route="ranked",
        intent_name="default_ranked",
        reason="Fallback to ranked retrieval.",
    )
