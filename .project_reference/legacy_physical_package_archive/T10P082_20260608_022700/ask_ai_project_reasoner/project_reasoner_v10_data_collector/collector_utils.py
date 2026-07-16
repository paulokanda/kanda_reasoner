"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

__all__ = [
    "compact_whitespace",
    "normalize_path",
    "safe_json_dump",
    "sanitize_for_json",
    "short_hash",
]

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from kanda_reasoner_app.project_json_scope_filter import (
    filter_project_analysis_json_payload,
)


_EMOJI_PATTERN = re.compile(
    "["
    "\U0001F300-\U0001F5FF"
    "\U0001F600-\U0001F64F"
    "\U0001F680-\U0001F6FF"
    "\U0001F700-\U0001F77F"
    "\U0001F780-\U0001F7FF"
    "\U0001F800-\U0001F8FF"
    "\U0001F900-\U0001F9FF"
    "\U0001FA00-\U0001FA6F"
    "\U0001FA70-\U0001FAFF"
    "\u2600-\u26FF"
    "\u2700-\u27BF"
    "]+",
    flags=re.UNICODE,
)


def _sanitize_text(value: str, remove_emojis: bool = True) -> str:
    if not isinstance(value, str):
        value = str(value)

    value = value.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")

    if remove_emojis:
        value = _EMOJI_PATTERN.sub("", value)

    return value


def sanitize_for_json(data: Any, remove_emojis: bool = True) -> Any:
    if isinstance(data, dict):
        clean_dict = {}
        for key, value in data.items():
            clean_key = _sanitize_text(key, remove_emojis=remove_emojis)
            clean_dict[clean_key] = sanitize_for_json(value, remove_emojis=remove_emojis)
        return clean_dict

    if isinstance(data, list):
        return [sanitize_for_json(item, remove_emojis=remove_emojis) for item in data]

    if isinstance(data, tuple):
        return [sanitize_for_json(item, remove_emojis=remove_emojis) for item in data]

    if isinstance(data, str):
        return _sanitize_text(data, remove_emojis=remove_emojis)

    return data


def safe_read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def normalize_path(path: Path, root: Path) -> str:
    return str(path.resolve().relative_to(root.resolve())).replace("\\", "/")


def short_hash(value: str) -> str:
    return hashlib.sha1(value.encode("utf-8", errors="replace")).hexdigest()[:12]


def compact_whitespace(text: str) -> str:
    return " ".join(str(text).split())


def safe_json_dump(data: Any, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    clean_data = sanitize_for_json(data, remove_emojis=True)
    clean_data, _scope_summary = filter_project_analysis_json_payload(
        clean_data,
        source_json_path=output_path,
    )
    json_text = json.dumps(
        clean_data,
        indent=2,
        ensure_ascii=False,
    )

    json_text = json_text.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")

    output_path.write_text(
        json_text,
        encoding="utf-8",
        errors="ignore",
    )
