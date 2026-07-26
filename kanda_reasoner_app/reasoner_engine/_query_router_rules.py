# project-path: kanda_reasoner_app/reasoner_engine/_query_router_rules.py
"""Private vocabulary and pure matching rules for query routing."""

from __future__ import annotations

__all__: list[str] = []

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


def norm_text(text: str) -> str:
    """Normalize query text for deterministic matching."""
    return text.strip().lower()


def has_any_term(text: str, terms: tuple[str, ...]) -> bool:
    """Return whether any configured term occurs in text."""
    return any(term in text for term in terms)


def one_line_locator_matches(q: str) -> bool:
    """Return whether q asks for strict one-line locator output."""
    return (
        "answer only in one line" in q
        or "<file path> | <symbol> | <evidence ids>" in q
    )


def exact_file_locator_matches(q: str) -> bool:
    """Return whether q matches exact file-location vocabulary."""
    return has_any_term(q, FILE_LOCATOR_TERMS)


def exact_symbol_locator_matches(q: str) -> bool:
    """Return whether q matches exact symbol-location vocabulary."""
    return has_any_term(q, SYMBOL_LOCATOR_TERMS)


def which_calls_matches(q: str) -> bool:
    """Return whether q asks for call-site lookup."""
    return has_any_term(q, WHICH_CALLS_TERMS)


def signal_or_action_matches(q: str) -> bool:
    """Return whether q asks about signals, slots, or actions."""
    return has_any_term(q, SIGNAL_ACTION_TERMS)


def responsibility_matches(q: str) -> bool:
    """Return whether q asks about responsibility or purpose."""
    return has_any_term(q, RESPONSIBILITY_TERMS)


def widget_listing_matches(q: str) -> bool:
    """Return whether q asks for a widget listing."""
    return has_any_term(q, WIDGET_LISTING_TERMS)


def listing_or_discovery_matches(q: str) -> bool:
    """Return whether q asks for ranked discovery."""
    return has_any_term(q, DISCOVERY_TERMS)


def explanatory_matches(q: str) -> bool:
    """Return whether q asks for explanation or synthesis."""
    return has_any_term(q, EXPLANATORY_TERMS)


def code_localization_matches(q: str) -> bool:
    """Return whether q asks for explanation with code localization."""
    return has_any_term(q, CODE_EXPLANATION_TERMS) and has_any_term(
        q, CODE_LOCALIZATION_TERMS
    )
