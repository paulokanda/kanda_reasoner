"""Canonical intent detection functions used by both retriever and router."""
import re
from typing import Any

def norm_text(value: Any) -> str:
    return str(value).strip().lower() if value is not None else ""

def is_which_method_calls_question(q: str) -> bool:
    q = norm_text(q)
    terms = ["which method calls", "what method calls", "which function calls",
             "what function calls", "who calls", "directly calls",
             "calls qtimer.singleshot", "calls self."]
    return any(term in q for term in terms)

def is_explanatory_question(q: str) -> bool:
    q = norm_text(q)
    terms = ["explain", "trace", "summarize", "describe", "walk through",
             "architecture", "flow", "chain", "implementation of",
             "responsibility split", "responsibility of", "role of",
             "purpose of", "what does", "what is the role"]
    return any(term in q for term in terms)

# ... all other is_* functions





