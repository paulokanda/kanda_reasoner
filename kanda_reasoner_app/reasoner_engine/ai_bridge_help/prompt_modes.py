# project-path: kanda_reasoner_app/reasoner_engine/ai_bridge_help/prompt_modes.py
"""Prompt classification helpers for Project Reasoner AI bridge."""

from __future__ import annotations
import re

from .prompt_extraction import extract_user_question
__all__ = ['is_code_localized_prompt', 'is_runtime_heavy_prompt', 'is_one_line_prompt', 'is_direct_responsibility_prompt', 'is_deterministic_prompt', 'is_locator_plus_explanation_prompt', 'is_generative_prompt']

def is_code_localized_prompt(prompt: str) -> bool:
        """Return whether code localized prompt.
        
        Parameters
        ----------
        prompt : str
            The prompt value.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        q = extract_user_question(prompt)

        explanation_terms = [
            "explain",
            "trace",
            "walk through",
            "describe",
            "summarize",
            "implementation",
            "implemented",
            "flow",
            "chain",
            "what code shows",
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
            "snippet",
            "snippets",
            "exact snippet",
            "exact snippets",
            "verbatim code",
            "line numbers",
            "line-level evidence",
            "line-level snippet",
            "line-level snippets",
            "line level snippet",
            "line level snippets",
            "file path and code",
            "symbol and code",
            "code evidence",
            "with code evidence",
            "strict evidence",
            "what code shows",
        ]

        return any(term in q for term in explanation_terms) and any(term in q for term in code_terms)

def is_runtime_heavy_prompt(prompt: str) -> bool:
        """Return whether runtime heavy prompt.
        
        Parameters
        ----------
        prompt : str
            The prompt value.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        q = extract_user_question(prompt)

        runtime_terms = [
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

        if any(term in q for term in runtime_terms):
            return True

        if re.search(r"\bon_[a-z0-9_]+\b", q):
            return True

        return False

def is_one_line_prompt(prompt: str) -> bool:
        """Return whether one line prompt.
        
        Parameters
        ----------
        prompt : str
            The prompt value.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        q = extract_user_question(prompt)
        return "answer only in one line" in q

def is_direct_responsibility_prompt(prompt: str) -> bool:
        """Return True for direct responsibility/role/purpose questions."""
        q = extract_user_question(prompt)

        patterns = [
            r"\bwhat\s+is\s+the\s+responsibility\s+of\s+`?[a-zA-Z_][a-zA-Z0-9_\.]*`?",
            r"\bwhat\s+is\s+the\s+role\s+of\s+`?[a-zA-Z_][a-zA-Z0-9_\.]*`?",
            r"\bwhat\s+is\s+the\s+purpose\s+of\s+`?[a-zA-Z_][a-zA-Z0-9_\.]*`?",
            r"\bwhat\s+does\s+`?[a-zA-Z_][a-zA-Z0-9_\.]*`?\s+do\b",
        ]
        return any(re.search(pattern, q) for pattern in patterns)

def is_deterministic_prompt(prompt: str) -> bool:
        """Return whether deterministic prompt.
        
        Parameters
        ----------
        prompt : str
            The prompt value.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        q = extract_user_question(prompt)

        if is_locator_plus_explanation_prompt(prompt):
            return False

        if is_direct_responsibility_prompt(prompt):
            return True

        triggers = [
            "where is ",
            "where is the ",
            "where is this ",
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
            "which method calls",
            "what method calls",
            "which function calls",
            "what function calls",
            "directly calls",
            "exact path",
            "answer only in one line",

            "which symbol owns",
            "what symbol owns",
            "which symbol handles",
            "what symbol handles",
            "which method owns",
            "what method owns",
            "which function owns",
            "what function owns",
            "entry point",
            "entry file",
            "entry script",

        ]
        return any(trigger in q for trigger in triggers)

def is_locator_plus_explanation_prompt(prompt: str) -> bool:
        """Return whether locator plus explanation prompt.
        
        Parameters
        ----------
        prompt : str
            The prompt value.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        q = extract_user_question(prompt)

        code_terms = [
            "with code",
            "show code",
            "include code",
            "code localization",
            "code location",
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

        explanation_terms = [
            "explain",
            "trace",
            "walk through",
            "describe",
            "summarize",
            "flow",
            "chain",
            "what code shows",
        ]

        is_locator = any(
            trigger in q
            for trigger in [
                "where is ",
                "where is the ",
                "where is this ",
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
        )

        wants_explanation = any(term in q for term in explanation_terms)
        wants_code = any(term in q for term in code_terms)

        return is_locator and (wants_explanation or wants_code)

def is_generative_prompt(prompt: str) -> bool:
        """Return whether generative prompt.
        
        Parameters
        ----------
        prompt : str
            The prompt value.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        q = extract_user_question(prompt)

        if is_locator_plus_explanation_prompt(prompt):
            return True

        if is_deterministic_prompt(prompt):
            return False

        explanation_terms = [
            "explain",
            "summarize",
            "describe",
            "walk through",
            "architecture",
            "responsibility split",
            "implementation of",
        ]

        flow_terms = [
            "trace the chain",
            "trace the flow",
            "explain the chain",
            "startup chain",
            "execution chain",
            "call chain",
            "flow from",
            "sequence from",
            "timeline chain",
            "reset chain",
            "cleanup chain",
            "reset flow",
            "cleanup flow",
        ]

        code_localization_terms = [
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

        has_explanation_intent = any(term in q for term in explanation_terms)
        has_flow_intent = any(term in q for term in flow_terms)
        import re as _re

        if _re.search(r"\btrace the .+ flow\b", q):
            has_flow_intent = True
        if _re.search(r"\bdescribe the .+ flow\b", q):
            has_flow_intent = True
        if _re.search(r"\bexplain the .+ flow\b", q):
            has_flow_intent = True

        has_code_localization_intent = any(term in q for term in code_localization_terms)

        signal_action_terms = [
            "signal",
            "slot",
            "connects",
            "connected to",
            "signal handler",
            "signal connection",
            "which handler",
            "what handler",
            "which slot",
            "what slot",
            "what signal",
            "which signal",
        ]

        has_signal_action_intent = any(term in q for term in signal_action_terms)

        widget_listing_terms = [
            "list all buttons",
            "list all widgets",
            "list the buttons",
            "list the widgets",
            "all buttons with",
            "all buttons and",
            "buttons with their",
            "buttons and their",
            "widgets with their",
            "widgets and their",
        ]
        has_widget_listing_intent = any(term in q for term in widget_listing_terms)

        return (
                has_explanation_intent
                or has_flow_intent
                or has_code_localization_intent
                or has_signal_action_intent
                or has_widget_listing_intent
        )



