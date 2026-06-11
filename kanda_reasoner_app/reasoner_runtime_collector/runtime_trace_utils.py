"""Support runtime evidence collection for Project Reasoner."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


def now_iso() -> str:
    return datetime.now().isoformat(timespec="milliseconds")


def sanitize_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value)
    return text.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")


def sanitize_data(data: Any) -> Any:
    if isinstance(data, dict):
        return {
            sanitize_text(key): sanitize_data(value)
            for key, value in data.items()
        }
    if isinstance(data, list):
        return [sanitize_data(item) for item in data]
    if isinstance(data, tuple):
        return [sanitize_data(item) for item in data]
    if isinstance(data, str):
        return sanitize_text(data)
    return data


def safe_json_dump(data: Any, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    clean_data = sanitize_data(data)
    json_text = json.dumps(clean_data, indent=2, ensure_ascii=False)
    json_text = json_text.encode("utf-8", errors="ignore").decode("utf-8", errors="ignore")
    output_path.write_text(json_text, encoding="utf-8", errors="ignore")