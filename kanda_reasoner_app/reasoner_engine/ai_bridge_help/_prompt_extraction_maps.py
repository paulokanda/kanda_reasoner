# project-path: kanda_reasoner_app/reasoner_engine/ai_bridge_help/_prompt_extraction_maps.py
"""Implementation helpers for prompt ids, scores, and locator parsing."""

from __future__ import annotations

import re

__all__: list[str] = []


def extract_symbol_id_map(prompt: str) -> dict[str, str]:
    """Extract the symbol id map."""
    out: dict[str, str] = {}
    current_symbol_id = None

    for line in prompt.splitlines():
        stripped = line.strip()

        m_score = re.match(r"^\[(S\d{2})\]\s+score=(\d+)\s*$", stripped)
        if m_score:
            current_symbol_id = m_score.group(1)
            continue

        m_symbol = re.match(r"^Symbol:\s+(.+?)\s*$", stripped)
        if m_symbol and current_symbol_id is not None:
            out[m_symbol.group(1).strip()] = current_symbol_id
            current_symbol_id = None

    return out


def extract_file_id_map(prompt: str) -> dict[str, str]:
    """Extract the file id map."""
    out: dict[str, str] = {}
    current_file_id = None

    for line in prompt.splitlines():
        stripped = line.strip()

        m_score = re.match(r"^\[(F\d{2})\]\s+score=(\d+)\s*$", stripped)
        if m_score:
            current_file_id = m_score.group(1)
            continue

        m_path = re.match(r"^Path:\s+(.+?)\s*$", stripped)
        if m_path and current_file_id is not None:
            out[m_path.group(1).strip()] = current_file_id
            current_file_id = None

    return out


def extract_symbol_score_map(prompt: str) -> list[tuple[str, str, str, int]]:
    """Extract the symbol score map."""
    items: list[tuple[str, str, str, int]] = []

    current_symbol_id = None
    current_score = None
    current_symbol_name = None

    for line in prompt.splitlines():
        stripped = line.strip()

        m_score = re.match(r"^\[(S\d{2})\]\s+score=(\d+)\s*$", stripped)
        if m_score:
            current_symbol_id = m_score.group(1)
            current_score = int(m_score.group(2))
            current_symbol_name = None
            continue

        m_symbol = re.match(r"^Symbol:\s+(.+?)\s*$", stripped)
        if m_symbol and current_symbol_id is not None:
            current_symbol_name = m_symbol.group(1).strip()
            continue

        m_location = re.match(r"^Location:\s+(.+?):(\d+)\s*$", stripped)
        if (
            m_location
            and current_symbol_id is not None
            and current_score is not None
            and current_symbol_name is not None
        ):
            symbol_path = m_location.group(1).strip()
            items.append(
                (current_symbol_id, current_symbol_name, symbol_path, current_score)
            )
            current_symbol_id = None
            current_score = None
            current_symbol_name = None

    return items


def extract_file_score_map(prompt: str) -> list[tuple[str, str, int]]:
    """Extract the file score map."""
    items: list[tuple[str, str, int]] = []
    current_file_id = None
    current_score = None

    for line in prompt.splitlines():
        stripped = line.strip()

        m_score = re.match(r"^\[(F\d{2})\]\s+score=(\d+)\s*$", stripped)
        if m_score:
            current_file_id = m_score.group(1)
            current_score = int(m_score.group(2))
            continue

        m_path = re.match(r"^Path:\s+(.+?)\s*$", stripped)
        if m_path and current_file_id is not None and current_score is not None:
            items.append((current_file_id, m_path.group(1).strip(), current_score))
            current_file_id = None
            current_score = None

    return items


def extract_locator_target(question: str) -> str:
    """Extract the locator target."""
    q = question.strip().lower()

    prefixes = [
        "which file contains",
        "what file contains",
        "which file records",
        "what file records",
        "which file has",
        "what file has",
        "which file includes",
        "what file includes",
        "which file is the source of",
        "what file is the source of",
        "which file defines",
        "what file defines",
        "in which file is",
        "where is",
        "where is the",
        "where is this",
        "which symbol owns",
        "what symbol owns",
        "which symbol handles",
        "what symbol handles",
        "which method owns",
        "what method owns",
        "which function owns",
        "what function owns",
        "which symbol directly calls",
    ]

    for prefix in prefixes:
        if q.startswith(prefix):
            target = q[len(prefix):].strip()
            target = target.rstrip(" ?.")
            if target.startswith("the "):
                target = target[4:]
            return target

    return ""


def extract_one_line_triplet(text: str) -> str:
    """Extract the one line triplet."""
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.count("|") == 2:
            return stripped
    return text.strip()
