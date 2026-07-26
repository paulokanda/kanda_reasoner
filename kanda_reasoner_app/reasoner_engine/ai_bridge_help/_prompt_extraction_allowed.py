# project-path: kanda_reasoner_app/reasoner_engine/ai_bridge_help/_prompt_extraction_allowed.py
"""Implementation helpers for prompt allowlist parsing."""

from __future__ import annotations

import re

__all__: list[str] = []


def extract_allowed_ids(prompt: str) -> set[str]:
    """Extract the allowed ids."""
    return set(re.findall(r"\[(?:F|S|SN)\d{2}\]", prompt))


def extract_cited_ids(text: str) -> set[str]:
    """Extract the cited ids."""
    return set(re.findall(r"\[(?:F|S|SN)\d{2}\]", text))


def extract_allowed_symbols(prompt: str) -> set[str]:
    """Extract the allowed symbols."""
    allowed: set[str] = set()

    symbol_pattern = re.compile(r"^Symbol:\s+(.+?)\s*$", flags=re.MULTILINE)
    for match in symbol_pattern.findall(prompt):
        symbol = match.strip()
        if symbol:
            allowed.add(symbol)

    snippet_anchor_pattern = re.compile(
        r"^\[(SN\d{2})\]\s+.+?:\d+\s+anchor=(.+)$",
        flags=re.MULTILINE,
    )

    for _snippet_id, anchor in snippet_anchor_pattern.findall(prompt):
        anchor = anchor.strip()
        if anchor:
            allowed.add(anchor)
            if anchor.startswith("LIVE_SOURCE:"):
                allowed.add(anchor[len("LIVE_SOURCE:"):].strip())

    # Also extract dotted names from compact file evidence detail lines.
    file_detail_pattern = re.compile(
        r"^(?:Functions|Classes|Calls out):\s+(.+)$",
        flags=re.MULTILINE,
    )
    for detail_match in file_detail_pattern.findall(prompt):
        for token in re.findall(
            r"\b[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+\b",
            detail_match,
        ):
            allowed.add(token)

    return allowed


def extract_allowed_file_paths(prompt: str) -> set[str]:
    """Extract the allowed file paths."""
    allowed: set[str] = set()
    current_file_id = None

    for line in prompt.splitlines():
        stripped = line.strip()

        file_match = re.match(r"^\[(F\d{2})\]\s+score=", stripped)
        if file_match:
            current_file_id = file_match.group(1)
            continue

        if stripped.startswith("Path: ") and current_file_id is not None:
            allowed.add(stripped[len("Path: "):].strip())
            current_file_id = None
            continue

        location_match = re.match(r"^Location:\s+(.+?):(\d+)\s*$", stripped)
        if location_match:
            allowed.add(location_match.group(1).strip())
            continue

        snippet_match = re.match(r"^\[(SN\d{2})\]\s+(.+?):(\d+)\s+anchor=(.+)$", stripped)
        if snippet_match:
            allowed.add(snippet_match.group(2).strip())
            continue

    return allowed


def extract_path_like_mentions(text: str) -> set[str]:
    """Extract slash or backslash path-like mentions from answer text."""
    return set(
        re.findall(
            r"\b[A-Za-z0-9_\-\\/]+(?:[\\/][A-Za-z0-9_\-\.]+)+\b",
            text,
        )
    )


def extract_symbol_like_mentions(text: str) -> set[str]:
    """Extract the symbol like mentions."""
    candidates = set(
        re.findall(r"\b[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+\b", text)
    )

    excluded_prefixes = {
        "f01",
        "f02",
        "f03",
        "f04",
        "f05",
        "f06",
        "f07",
        "f08",
        "f09",
        "f10",
        "f11",
        "f12",
        "f13",
        "f14",
        "s01",
        "s02",
        "s03",
        "s04",
        "s05",
        "s06",
        "s07",
        "s08",
        "s09",
        "s10",
        "s11",
        "s12",
        "s13",
        "s14",
        "sn01",
        "sn02",
        "sn03",
        "sn04",
        "sn05",
        "sn06",
        "sn07",
        "sn08",
        "sn09",
        "sn10",
    }

    filtered: set[str] = set()
    for candidate in candidates:
        low = candidate.lower()
        if low.split(".")[0] in excluded_prefixes:
            continue
        filtered.add(candidate)

    return filtered
