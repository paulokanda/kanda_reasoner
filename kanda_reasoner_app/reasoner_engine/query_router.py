"""Support V10 project reasoning and evidence handling."""

from __future__ import annotations

from dataclasses import dataclass


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

FILE_LOCATOR_TERMS = (
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
    "which file owns",
    "what file owns",
    "where implemented",
    "where is implemented",
    "entry point",
    "entry file",
    "entry script",
    "main entry",
    "application entry",
    "app entry",
    "which file is the entry",
    "what file is the entry",
)

SYMBOL_LOCATOR_TERMS = (
    "does the class ",
    "does the method ",
    "does the function ",
    "does the symbol ",
    "list symbols in ",
    "list methods in ",
    "list functions in ",
    "which class owns method",
    "which symbol directly calls",
    "which symbol owns",
    "what symbol owns",
    "which symbol handles",
    "what symbol handles",
    "which method owns",
    "what method owns",
    "which function owns",
    "what function owns",
)

WHICH_CALLS_TERMS = (
    "which method calls",
    "what method calls",
    "which function calls",
    "what function calls",
    "who calls",
    "directly calls",
    "calls qtimer.singleshot",
    "calls self.",
)

SIGNAL_ACTION_TERMS = (
    "signal",
    "slot",
    "connects",
    "connected to",
    "emit",
    "emits",
    "clicked",
    "textchanged",
    "signal handler",
    "qt signal",
    "signal connection",
    "what connects",
    "which handler",
)

RESPONSIBILITY_TERMS = (
    "responsibility of",
    "role of",
    "purpose of",
    "what does",
    "what is the role",
    "what is the purpose",
)

WIDGET_LISTING_TERMS = (
    "list all buttons",
    "list all widgets",
    "list all labels",
    "list the buttons",
    "list the widgets",
    "all buttons with",
    "all widgets with",
    "all buttons and",
    "all widgets and",
    "buttons and their",
    "buttons with their",
    "widgets and their",
    "widgets with their",
    "list all dropdowns",
    "list all combobox",
    "list the dropdowns",
    "all dropdowns",
    "all comboboxes",
    "dropdowns and their",
    "dropdowns with their",
)

DISCOVERY_TERMS = (
    "what modules are related",
    "which files are involved",
    "which modules are involved",
    "where is topomap implemented",
    "is there already",
    "find modules for",
    "locate likely",
    "what seems responsible",
    "show relevant files",
    "which parts are related",
    "which files are related",
    "what files seem responsible",
    "what files seem related",
    "rank candidates",
    "list all",
    "list the",
    "show all",
    "show me all",
    "show me the",
    "all files",
    "all classes",
    "all methods",
)

EXPLANATORY_CORE_TERMS = (
    "explain",
    "trace",
    "summarize",
    "describe",
    "walk through",
    "architecture",
    "flow",
    "chain",
    "implementation of",
    "how does",
    "how do",
    "how is",
    "how are",
    "main window class",
    "tab switching",
    "tab switch logic",
    "tab switch",
    "switching logic",
    "how does the",
    "how is the",
    "which files implement",
    "what files implement",
    "files that implement",
    "files implement",
    "which modules implement",
    "what modules implement",
)

EXPLANATORY_TERMS = EXPLANATORY_CORE_TERMS + RESPONSIBILITY_TERMS

CODE_EXPLANATION_TERMS = (
    "explain",
    "trace",
    "walk through",
    "describe",
    "summarize",
    "implementation",
    "flow",
    "chain",
)

CODE_LOCALIZATION_TERMS = (
    "with code",
    "show code",
    "include code",
    "code localization",
    "code and code localization",
    "with code and code localization",
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
)

WHICH_CALLS_WITH_CODE_EXTRA_TERMS = (
    "snippet",
    "snippets",
    "call site",
    "code",
    "what exact snippet shows",
)


@dataclass(frozen=True)
class QueryRouteDecision:
    route: str
    intent_name: str
    reason: str


def _norm(text: str) -> str:
    return text.strip().lower()


def _has_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term in text for term in terms)


def _which_calls_needs_code_answer(q: str) -> bool:
    return (
        is_code_localization_question(q)
        or is_explanatory_question(q)
        or _has_any(q, WHICH_CALLS_WITH_CODE_EXTRA_TERMS)
    )


def is_one_line_locator_question(q: str) -> bool:
    return (
        "answer only in one line" in q
        or "<file path> | <symbol> | <evidence ids>" in q
    )


def is_exact_file_locator_question(q: str) -> bool:
    return _has_any(q, FILE_LOCATOR_TERMS)


def is_exact_symbol_locator_question(q: str) -> bool:
    return _has_any(q, SYMBOL_LOCATOR_TERMS)


def is_which_calls_question(q: str) -> bool:
    return _has_any(q, WHICH_CALLS_TERMS)


def is_signal_or_action_question(q: str) -> bool:
    return _has_any(q, SIGNAL_ACTION_TERMS)


def is_responsibility_question(q: str) -> bool:
    return _has_any(q, RESPONSIBILITY_TERMS)


def is_widget_listing_question(q: str) -> bool:
    return _has_any(q, WIDGET_LISTING_TERMS)


def is_listing_or_discovery_question(q: str) -> bool:
    return _has_any(q, DISCOVERY_TERMS)


def is_explanatory_question(q: str) -> bool:
    return _has_any(q, EXPLANATORY_TERMS)


def is_code_localization_question(q: str) -> bool:
    return _has_any(q, CODE_EXPLANATION_TERMS) and _has_any(q, CODE_LOCALIZATION_TERMS)


def is_locator_plus_explanation_question(q: str) -> bool:
    return is_exact_file_locator_question(q) and (
        is_code_localization_question(q)
        or is_explanatory_question(q)
        or "flow" in q
        or "chain" in q
        or "what code shows" in q
    )


def route_query_intent(question: str) -> QueryRouteDecision:
    q = _norm(question)


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




