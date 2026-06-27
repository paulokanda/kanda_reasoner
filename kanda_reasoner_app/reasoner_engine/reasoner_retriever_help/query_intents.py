"""Support V10 project reasoning and evidence handling."""

# -"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR
# MODULE ORIGIN : kanda_reasoner_app/reasoner_engine\reasoner_retriever.py
# MANIFEST      : kanda_reasoner_app/reasoner_engine\reasoner_retriever_help.json
# HELP FOLDER   : kanda_reasoner_app/reasoner_engine\reasoner_retriever_help
# PURPOSE       : Classify retrieval-intent shapes from a normalized question string.
# EXPORTS       : is_startup_question, is_explicit_call_chain_question, is_main_window_show_responsibility_question, is_qtimer_showmaximized_question, is_where_is_called_question, is_where_is_question, is_which_method_calls_question, is_explain_chain_question, is_explanatory_question, is_code_localized_explanation_question, is_topomap_explanation_question, is_topomap_implementation_question, is_runtime_heavy_question, is_packaging_metadata_question, is_documentation_intent_question, detect_query_intents
# DEPENDS ON    : query_text.py
# REFACTOR DATE : 2026-04-10
# -"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR
from __future__ import annotations

import re

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
    call_chain_terms = [
        "self.v.main_window.show()",
        "self.v.main_window.show",
        "calls self.v.main_window.show",
        "method that calls self.v.main_window.show",
    ]
    return any(term in q for term in call_chain_terms)

def is_main_window_show_responsibility_question(q: str) -> bool:
    terms = [
        "showing the main window",
        "responsible for showing the main window",
        "method most directly responsible for showing the main window",
        "symbol most directly responsible for showing the main window",
        "main window is shown",
    ]
    return any(term in q for term in terms)

def is_qtimer_showmaximized_question(q: str) -> bool:
    return "qtimer.singleshot" in q and "self.v.main_window.showmaximized" in q

def is_where_is_called_question(q: str) -> bool:
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

def is_where_is_question(q: str) -> bool:
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

def is_which_method_calls_question(q: str) -> bool:
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

def is_explain_chain_question(q: str) -> bool:
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

def is_explanatory_question(q: str) -> bool:
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

def is_code_localized_explanation_question(q: str) -> bool:
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

def is_topomap_explanation_question(q: str) -> bool:
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
        is_explanatory_question(q)
        or any(term in q for term in implementation_terms)
    )

def is_topomap_implementation_question(q: str) -> bool:
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

def is_runtime_heavy_question(q: str) -> bool:
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
    q = norm_text(q)

    return {
        "where_is": is_where_is_question(q),
        "which_calls": is_which_method_calls_question(q),
        "explain_chain": is_explain_chain_question(q),
        "startup": is_startup_question(q),
        "explicit_call_chain": is_explicit_call_chain_question(q),
        "main_window_show": is_main_window_show_responsibility_question(q),
        "qtimer_showmaximized": is_qtimer_showmaximized_question(q),
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






