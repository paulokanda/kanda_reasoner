"""Support V10 project reasoning and evidence handling."""

# -"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR
# MODULE ORIGIN : E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\reasoner_retriever.py
# MANIFEST      : E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\reasoner_retriever_help.json
# HELP FOLDER   : E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\reasoner_retriever_help
# PURPOSE       : Normalize query and path text and expose shared pure text utilities.
# EXPORTS       : norm_text, tokenize_query, safe_read_text, file_name_from_path, is_allowed_project_path, is_auxiliary_ui_path, last_part_match_in_query
# DEPENDS ON    : none
# REFACTOR DATE : 2026-04-10
# -"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR
from __future__ import annotations

import os
import re
from typing import Any

__all__ = [
    "norm_text",
    "tokenize_query",
    "safe_read_text",
    "file_name_from_path",
    "is_allowed_project_path",
    "is_auxiliary_ui_path",
    "last_part_match_in_query",
]

def norm_text(value: Any) -> str:
    return str(value).strip().lower() if value is not None else ""

def tokenize_query(text: str) -> list[str]:
    tokens = re.findall(r"[a-zA-Z0-9_\.]+", text.lower())
    stop_words = {
        "the",
        "is",
        "are",
        "a",
        "an",
        "of",
        "to",
        "me",
        "show",
        "which",
        "what",
        "where",
        "who",
        "does",
        "do",
        "in",
        "on",
        "for",
        "and",
        "or",
        "with",
        "created",
        "creates",
        "create",
        "that",
        "this",
        "app",
        "about",
        "how",
        "from",
        "based",
        "using",
        "only",
        "current",
        "project",
        "defined",
        "definition",
        "declare",
        "declared",
    }
    return [token for token in tokens if token not in stop_words]

def safe_read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return handle.read()

def file_name_from_path(path: str) -> str:
    return os.path.basename(path.replace("\\", "/")).lower()

def is_allowed_project_path(path: str) -> bool:
    low = path.replace("\\", "/").lower().lstrip("/")

    # developer_tools/ is the reasoner tool itself, not the EEG project.
    # It is not indexed in the JSON and must not enter evidence as noise.
    if low.startswith("developer_tools/"):
        return False

    blocked_parts = [
        "/.git/",
        "/.idea/",
        "/.venv/",
        "/venv/",
        "/env/",
        "/site-packages/",
        "/__pycache__/",
        "/build/",
        "/dist/",
        "/scratches/",
        "/consoles/",
        "/external libraries/",
        "/logic_main_app/chats/",
    ]

    low_with_slashes = "/" + low
    return not any(part in low_with_slashes for part in blocked_parts)

def is_auxiliary_ui_path(path: str) -> bool:
    low = path.replace("\\", "/").lower()
    auxiliary_terms = [
        "help",
        "tooltip",
        "popup",
        "modal",
        "dialog",
        "warning",
    ]
    return any(term in low for term in auxiliary_terms)

def last_part_match_in_query(names: list[str], q: str) -> bool:
    for name in names:
        low = norm_text(name)
        tail = low.split(".")[-1]
        if tail and tail in q:
            return True
    return False






