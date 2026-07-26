# project-path: kanda_reasoner_app/reasoner_engine/ai_bridge_help/_prompt_extraction_blocks.py
"""Implementation helpers for prompt evidence block parsing."""

from __future__ import annotations

import re
from typing import Any

__all__: list[str] = []


def extract_runtime_anchors_from_detail(detail_text: str) -> list[str]:
    """Extract the runtime anchors from detail."""
    anchors: list[str] = []

    for line in detail_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("Runtime anchors: "):
            raw = stripped[len("Runtime anchors: "):]
            anchors.extend([part.strip() for part in raw.split("|") if part.strip()])

    return anchors


def extract_snippet_text_blob(prompt: str) -> str:
    """Return concatenated snippet text, including live-source snippets."""
    blocks = extract_snippet_blocks(prompt)
    return "\n".join(str(block.get("text", "")) for block in blocks)


def extract_snippet_blocks(prompt: str) -> list[dict[str, Any]]:
    """Extract SOURCE SNIPPETS and LIVE SOURCE EVIDENCE snippet blocks."""
    blocks: list[dict[str, Any]] = []
    lines = prompt.splitlines()

    in_snippet_section = False
    current: dict[str, Any] | None = None

    section_starters = {
        "SOURCE SNIPPETS",
        "LIVE SOURCE EVIDENCE",
    }
    hard_section_enders = {
        "STRICT GROUNDING RULE",
        "CITATION RULE",
        "PREFERENCE MODE",
        "FINAL TASK REMINDER",
        "INSTRUCTIONS",
    }

    for line in lines:
        stripped = line.strip()

        if stripped in section_starters:
            if current is not None:
                current["text"] = "\n".join(current["text_lines"]).rstrip()
                blocks.append(current)
            in_snippet_section = True
            current = None
            continue

        if stripped in hard_section_enders:
            if current is not None:
                current["text"] = "\n".join(current["text_lines"]).rstrip()
                blocks.append(current)
                current = None
            if stripped == "STRICT GROUNDING RULE":
                break
            in_snippet_section = False
            continue

        if not in_snippet_section:
            continue

        match = re.match(r"^\[(SN\d{2})\]\s+(.+?):(\d+)\s+anchor=(.+)$", stripped)
        if match:
            if current is not None:
                current["text"] = "\n".join(current["text_lines"]).rstrip()
                blocks.append(current)

            current = {
                "snippet_id": match.group(1),
                "path": match.group(2).strip(),
                "line": int(match.group(3)),
                "anchor": match.group(4).strip(),
                "text_lines": [],
            }
            continue

        if current is None:
            continue

        current["text_lines"].append(line)

    if current is not None:
        current["text"] = "\n".join(current["text_lines"]).rstrip()
        blocks.append(current)

    return blocks


def extract_file_evidence_blocks(prompt: str) -> list[dict[str, Any]]:
    """Extract the file evidence blocks."""
    blocks: list[dict[str, Any]] = []
    lines = prompt.splitlines()

    in_file_section = False
    current: dict[str, Any] | None = None

    for line in lines:
        stripped = line.strip()

        if stripped == "FILE EVIDENCE":
            in_file_section = True
            current = None
            continue

        if stripped == "SYMBOL EVIDENCE":
            if current is not None:
                current["detail"] = "\n".join(current["detail_lines"]).strip()
                blocks.append(current)
            break

        if not in_file_section:
            continue

        match = re.match(r"^\[(F\d{2})\]\s+score=(\d+)\s*$", stripped)
        if match:
            if current is not None:
                current["detail"] = "\n".join(current["detail_lines"]).strip()
                blocks.append(current)

            current = {
                "file_id": match.group(1),
                "score": int(match.group(2)),
                "path": "",
                "detail_lines": [],
            }
            continue

        if current is None:
            continue

        if stripped.startswith("Path: "):
            current["path"] = stripped[len("Path: "):].strip()

        current["detail_lines"].append(line)

    return blocks


def extract_symbol_evidence_blocks(prompt: str) -> list[dict[str, Any]]:
    """Extract the symbol evidence blocks."""
    blocks: list[dict[str, Any]] = []
    lines = prompt.splitlines()

    in_symbol_section = False
    current: dict[str, Any] | None = None

    for line in lines:
        stripped = line.strip()

        if stripped == "SYMBOL EVIDENCE":
            in_symbol_section = True
            current = None
            continue

        if stripped in {"SOURCE SNIPPETS", "LIVE SOURCE EVIDENCE"}:
            if current is not None:
                current["detail"] = "\n".join(current["detail_lines"]).strip()
                blocks.append(current)
            break

        if not in_symbol_section:
            continue

        match = re.match(r"^\[(S\d{2})\]\s+score=(\d+)\s*$", stripped)
        if match:
            if current is not None:
                current["detail"] = "\n".join(current["detail_lines"]).strip()
                blocks.append(current)

            current = {
                "symbol_id": match.group(1),
                "score": int(match.group(2)),
                "symbol_name": "",
                "path": "",
                "line": 0,
                "detail_lines": [],
            }
            continue

        if current is None:
            continue

        if stripped.startswith("Symbol: "):
            current["symbol_name"] = stripped[len("Symbol: "):].strip()

        location_match = re.match(r"^Location:\s+(.+?):(\d+)\s*$", stripped)
        if location_match:
            current["path"] = location_match.group(1).strip()
            current["line"] = int(location_match.group(2))

        current["detail_lines"].append(line)

    return blocks


def extract_user_question(prompt: str) -> str:
    """Extract the user question."""
    match = re.search(
        r"USER QUESTION\s*\n(.+?)(?:\n\s*\nPROJECT SUMMARY|\n\s*\nCONVERSATION MEMORY|\Z)",
        prompt,
        flags=re.DOTALL,
    )
    if not match:
        return prompt.strip().lower()
    return match.group(1).strip().lower()
