"""Grounding validation helpers for Project Reasoner AI bridge."""

from __future__ import annotations
import re

from .prompt_extraction import (
    extract_allowed_file_paths,
    extract_allowed_ids,
    extract_allowed_symbols,
    extract_cited_ids,
    extract_path_like_mentions,
    extract_snippet_blocks,
    extract_snippet_text_blob,
    extract_symbol_like_mentions,
    extract_user_question,
)
from .prompt_modes import (
    is_code_localized_prompt,
    is_deterministic_prompt,
    is_generative_prompt,
    is_runtime_heavy_prompt,
)
__all__ = ['sanitize_invalid_ids', 'has_forbidden_paths', 'has_forbidden_symbols', 'looks_ungrounded_deterministic', 'looks_ungrounded_generative', 'has_forbidden_ids', 'answer_ignored_required_snippets', 'grounding_failure_reason']

def _normalize_path_for_grounding(path: str) -> str:
        """Normalize paths for grounding comparisons across Windows/POSIX."""
        text = str(path or "").strip().strip("`'\"")
        text = text.replace("\\\\", "/").replace("\\", "/")
        text = re.sub(r"/+", "/", text)
        return text.lower().rstrip(".,;:)")


def sanitize_invalid_ids(prompt: str, text: str) -> str:
        allowed_ids = extract_allowed_ids(prompt)

        def repl(match: re.Match[str]) -> str:
            token = match.group(0)
            return token if token in allowed_ids else ""

        cleaned = re.sub(r"\[(?:F|S|SN)\d{2}\]", repl, text)
        cleaned = re.sub(r"[ \t]+", " ", cleaned)
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
        return cleaned.strip()

def has_forbidden_paths(prompt: str, answer_text: str) -> bool:
        if is_generative_prompt(prompt):
            return False

        allowed_paths = extract_allowed_file_paths(prompt)
        if not allowed_paths:
            return False

        mentioned_paths = extract_path_like_mentions(answer_text)
        if not mentioned_paths:
            return False

        allowed_normalized = {
            _normalize_path_for_grounding(path)
            for path in allowed_paths
            if str(path).strip()
        }

        for path in mentioned_paths:
            normalized = _normalize_path_for_grounding(path)
            if normalized not in allowed_normalized:
                return True

        return False

def has_forbidden_symbols(prompt: str, answer_text: str) -> bool:
        allowed_symbols = extract_allowed_symbols(prompt)
        if not allowed_symbols:
            return False

        mentioned_symbols = extract_symbol_like_mentions(answer_text)
        if not mentioned_symbols:
            return False

        snippet_text_blob = extract_snippet_text_blob(prompt)
        snippet_dotted = set(
            re.findall(
                r"\b[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+\b",
                snippet_text_blob,
            )
        )

        for symbol in mentioned_symbols:
            low = symbol.lower()

            # Allow self.* instance attribute references
            if low.startswith("self."):
                continue

            # Allow Qt/PySide6 framework names
            if re.match(r"^(Q[A-Z]|PySide6|PyQt)", symbol):
                continue

            # Allow if present in the snippet text corpus of this prompt
            if symbol in snippet_dotted:
                continue

            # Allow if present in the allowed symbols set
            if symbol in allowed_symbols:
                continue

            # Allow Qt signal operation calls (clicked.connect, textChanged.connect, etc.)
            last_segment = symbol.split(".")[-1].lower()
            if last_segment in {"connect", "disconnect", "emit"}:
                continue

            # Allow all-lowercase dotted names as module paths or library calls
            if all(seg == seg.lower() for seg in symbol.split(".")):
                continue

            return True

        return False

def looks_ungrounded_deterministic(text: str) -> bool:
        suspicious_terms = [
            "test_module.py",
            "test_class_method",
            "assumed to be relevant",
            "common practices",
            "not explicitly referenced",
            "has been assumed",
            "likely indicates a typo or oversight",
            "unknown command or request",
            "shell.txt",
            "test_snippet_1.py",
            "test_snippet_2.py",
            "samplecode.py",
            "code.py",
            "image processing",
            "unknown_evidence",
            "evidence_ids=",
            "qqmainwindow.show",
            "the closest match is",
            "does not directly call",
            "there is no direct call",
        ]

        low = text.lower()
        return any(term in low for term in suspicious_terms)

def looks_ungrounded_generative(text: str) -> bool:
        suspicious_terms = [
            "test_module.py",
            "test_class_method",
            "shell.txt",
            "test_snippet_1.py",
            "test_snippet_2.py",
            "samplecode.py",
            "image processing",
            "unknown_evidence",
            "evidence_ids=",
            "qqmainwindow.show",
        ]

        low = text.lower()
        return any(term in low for term in suspicious_terms)

def has_forbidden_ids(prompt: str, answer_text: str) -> bool:
        allowed_ids = extract_allowed_ids(prompt)
        cited_ids = extract_cited_ids(answer_text)
        return not cited_ids.issubset(allowed_ids)

def answer_ignored_required_snippets(prompt: str, answer_text: str) -> bool:
        q = extract_user_question(prompt)
        snippet_blocks = extract_snippet_blocks(prompt)

        if not snippet_blocks:
            return False

        code_localized = (
                "with code" in q
                or "show code" in q
                or "include code" in q
                or "code localization" in q
                or "code location" in q
                or "show snippets" in q
                or "show snippet" in q
                or "line numbers" in q
                or "file path and code" in q
                or "symbol and code" in q
                or "code evidence" in q
                or "with code evidence" in q
                or "line-level snippet" in q
                or "line-level snippets" in q
                or "line level snippet" in q
                or "line level snippets" in q
        )

        if not code_localized:
            return False

        answer_low = answer_text.lower()

        snippet_id_hits = sum(
            1 for block in snippet_blocks
            if str(block["snippet_id"]).lower() in answer_low
        )
        anchor_hits = sum(
            1 for block in snippet_blocks
            if str(block["anchor"]).lower() in answer_low
        )
        path_hits = sum(
            1 for block in snippet_blocks
            if str(block["path"]).lower() in answer_low
        )

        short_anchor_hits = sum(
            1
            for block in snippet_blocks
            if str(block.get("anchor", "")).split(".")[-1].strip().lower() in answer_low
        )

        snippet_code_hits = 0
        for block in snippet_blocks:
            snippet_lines = [
                ln.strip()
                for ln in str(block.get("text", "")).splitlines()
                if len(ln.strip()) > 10
            ]
            if any(ln.lower() in answer_low for ln in snippet_lines):
                snippet_code_hits += 1

        return (
                snippet_id_hits
                + anchor_hits
                + path_hits
                + short_anchor_hits
                + snippet_code_hits
        ) == 0

def grounding_failure_reason(prompt: str, answer_text: str) -> str:
        if is_deterministic_prompt(prompt):
            if looks_ungrounded_deterministic(answer_text):
                return "looks_ungrounded_deterministic"
            if has_forbidden_ids(prompt, answer_text):
                return "forbidden_ids"
            if has_forbidden_paths(prompt, answer_text):
                return "forbidden_paths"
            return ""

        if is_generative_prompt(prompt):
            if answer_ignored_required_snippets(prompt, answer_text):
                return "ignored_required_snippets"
            if looks_ungrounded_generative(answer_text):
                return "looks_ungrounded_generative"
            if has_forbidden_ids(prompt, answer_text):
                return "forbidden_ids"
            if has_forbidden_paths(prompt, answer_text):
                return "forbidden_paths"

            enforce_forbidden_symbols = not (
                    is_code_localized_prompt(prompt)
                    or is_runtime_heavy_prompt(prompt)
            )

            if enforce_forbidden_symbols and has_forbidden_symbols(prompt, answer_text):
                return "forbidden_symbols"

            return ""

        if looks_ungrounded_deterministic(answer_text):
            return "looks_ungrounded_default"
        if has_forbidden_ids(prompt, answer_text):
            return "forbidden_ids"
        if has_forbidden_paths(prompt, answer_text):
            return "forbidden_paths"
        if has_forbidden_symbols(prompt, answer_text):
            return "forbidden_symbols"
        return ""



