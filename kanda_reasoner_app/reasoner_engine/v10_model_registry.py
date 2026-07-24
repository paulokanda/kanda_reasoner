# project-path: kanda_reasoner_app/reasoner_engine/v10_model_registry.py
"""Discover local Ollama models for the Project Reasoner V10 GUI."""

from __future__ import annotations

import json
import subprocess
from urllib.parse import urlsplit
from collections.abc import Iterable
from typing import Any

import requests

DEFAULT_OLLAMA_BASE_URL = "http://127.0.0.1:11434/v1"
TIMEOUT = 20


class LocalModelRegistry:
    """Return models from the globally configured local endpoint."""

    def __init__(self, *, base_url: str = "", preferred_model: str | None = None) -> None:
        runtime_base, runtime_model = _runtime_configuration()
        self._base_url = _normalize_base_url(base_url or runtime_base)
        self._preferred_model = runtime_model if preferred_model is None else str(preferred_model or "").strip()
        root = self._base_url[:-3] if self._base_url.endswith("/v1") else self._base_url
        self._tags_url = root.rstrip("/") + "/api/tags"
        self._models_url = self._base_url.rstrip("/") + "/models"

    def list_models(self) -> list[str]:
        """Return every model currently visible through supported Ollama APIs."""
        models: list[str] = []
        models.extend(self._from_tags())
        models.extend(self._from_v1_models())
        models.extend(self._from_ollama_cli())
        return _preferred_first(_unique_sorted_model_names(models), self._preferred_model)

    def _from_tags(self) -> list[str]:
        """Support from tags behavior.
        
        Returns
        -------
        list[str]
            The list of values.
        """
        
        try:
            response = requests.get(self._tags_url, timeout=TIMEOUT)
            response.raise_for_status()
            data = response.json()

            items = data.get("models", [])
            out: list[str] = []
            for item in items:
                if not isinstance(item, dict):
                    continue
                name = _first_text_value(item, ("name", "model", "id"))
                if name:
                    out.append(name)
            return _unique_sorted_model_names(out)
        except (requests.RequestException, json.JSONDecodeError, ValueError):
            return []

    def _from_v1_models(self) -> list[str]:
        """Support from v1 models behavior.
        
        Returns
        -------
        list[str]
            The list of values.
        """
        
        try:
            response = requests.get(self._models_url, timeout=TIMEOUT)
            response.raise_for_status()
            data = response.json()
            items = data.get("data", [])
            out: list[str] = []
            for item in items:
                if not isinstance(item, dict):
                    continue
                model_id = _first_text_value(item, ("id", "name", "model"))
                if model_id:
                    out.append(model_id)
            return _unique_sorted_model_names(out)
        except (requests.RequestException, json.JSONDecodeError, ValueError):
            return []

    def _from_ollama_cli(self) -> list[str]:
        """Support from ollama cli behavior.
        
        Returns
        -------
        list[str]
            The list of values.
        """
        
        if not _is_default_ollama_endpoint(self._base_url):
            return []
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=TIMEOUT,
                check=False,
            )
        except (OSError, subprocess.SubprocessError, ValueError):
            return []

        if result.returncode != 0:
            return []

        return _parse_ollama_list_output(result.stdout)


def _first_text_value(item: dict[str, Any], keys: Iterable[str]) -> str:
    """Return the first non-empty text value for the supplied keys."""
    for key in keys:
        value = str(item.get(key, "")).strip()
        if value:
            return value
    return ""


def _parse_ollama_list_output(output: str) -> list[str]:
    """Parse model names from the tabular output of ``ollama list``."""
    names: list[str] = []
    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        first_column = line.split(maxsplit=1)[0].strip()
        if not first_column or first_column.upper() == "NAME":
            continue

        names.append(first_column)

    return _unique_sorted_model_names(names)


def _unique_sorted_model_names(names: Iterable[str]) -> list[str]:
    """Normalize, deduplicate, and sort model names for stable GUI display."""
    unique = {str(name).strip() for name in names if str(name).strip()}
    return sorted(unique, key=str.casefold)


def _normalize_base_url(value: str) -> str:
    clean = str(value or DEFAULT_OLLAMA_BASE_URL).strip().rstrip("/")
    if clean.endswith("/chat/completions"):
        clean = clean[: -len("/chat/completions")]
    if not clean.endswith("/v1"):
        clean += "/v1"
    return clean


def _runtime_configuration() -> tuple[str, str]:
    from kanda_reasoner_app.local_ai_runtime_state import (
        runtime_local_ai_configuration_snapshot,
    )

    snapshot = runtime_local_ai_configuration_snapshot()
    if snapshot is None:
        return DEFAULT_OLLAMA_BASE_URL, ""
    return snapshot.base_url, snapshot.model_id


def _is_default_ollama_endpoint(base_url: str) -> bool:
    parts = urlsplit(base_url)
    return parts.hostname in {"127.0.0.1", "localhost"} and (parts.port or 80) == 11434


def _preferred_first(models: list[str], preferred: str) -> list[str]:
    clean = str(preferred or "").strip()
    ordered = list(models)
    if clean in ordered:
        ordered.remove(clean)
        ordered.insert(0, clean)
    return ordered
