#!/usr/bin/env python3
"""Configuration dataclass for the local AI docstring generator.

Phase 4 additions
-----------------
- ``min_confidence`` — gate the validator's confidence threshold.
- ``max_line_length`` — forwarded to the validator for line-length checks.
- ``max_todo_ratio`` — forwarded to the validator for TODO-density checks.
- ``allow_invented_params`` / ``allow_invented_raises`` — escape hatches for
  the AST ground-truth guards (useful when debugging edge cases).
- ``include_private`` — explicit flag to document ``_`` and ``__`` prefixed
  symbols (they are always walked by the AST, but this flag makes the intent
  unambiguous and can be surfaced in the GUI and CLI).
- ``uncertain_annotation`` — whether to append ``# AI-UNCERTAIN`` comments to
  low-confidence docstrings.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass
class AIConfig:
    """Settings that control how the AI docstring generator connects and behaves.

    Parameters
    ----------
    base_url : str, optional
        Base URL of the OpenAI-compatible inference endpoint.
        Defaults to Ollama's local server.
    model : str, optional
        Model name to request.  Must be available at *base_url*.
    timeout_seconds : float, optional
        Per-request timeout in seconds.
    max_tokens : int, optional
        Maximum tokens the model may emit per docstring.
    temperature : float, optional
        Sampling temperature.  Keep low (0.05–0.15) for precise docstrings.
    fallback_to_heuristic : bool, optional
        When ``True`` (default), fall back to the heuristic generator on any
        AI failure.  Set to ``False`` to treat failures as hard errors.
    workers : int, optional
        Maximum parallel file-processing threads.
    cache_enabled : bool, optional
        Cache AI-generated docstrings keyed by source hash.
    cache_path : str, optional
        Path of the JSON cache file relative to the project root.
    docstring_style : str, optional
        Docstring format: only ``"numpy"`` is implemented.
    include_private : bool, optional
        When ``True``, explicitly document ``_`` and ``__`` prefixed symbols.
        The AST walker always visits private symbols; this flag makes the
        intent visible in the GUI, CLI, and logs.  Default ``True``.
    min_confidence : str, optional
        Minimum validator confidence required to accept a docstring.  One of
        ``"high"``, ``"medium"``, ``"low"``.  Default ``"low"`` — accept
        everything that passes fatal checks.  Set to ``"medium"`` for stricter
        pipelines that avoid low-quality TODO-heavy docstrings.
    max_line_length : int, optional
        Maximum line length enforced by the validator.  Default 88.
    max_todo_ratio : float, optional
        Maximum fraction of non-blank lines that may contain ``TODO`` before
        the validator flags the docstring as low-confidence.  Default 0.5.
    allow_invented_params : bool, optional
        Disable the invented-parameter guard.  Default ``False``.
    allow_invented_raises : bool, optional
        Disable the invented-exception guard.  Default ``False``.
    uncertain_annotation : bool, optional
        When ``True`` (default), append a ``# AI-UNCERTAIN`` comment to
        docstrings whose validator confidence is ``"low"``.
    """

    base_url: str = "http://localhost:11434/v1"
    model: str = "codellama:13b"
    timeout_seconds: float = 30.0
    max_tokens: int = 512
    temperature: float = 0.1
    fallback_to_heuristic: bool = True
    workers: int = 4
    cache_enabled: bool = True
    cache_path: str = ".docstring_cache.json"
    docstring_style: str = "numpy"

    # Phase 4 additions
    include_private: bool = True
    min_confidence: str = "low"
    max_line_length: int = 88
    max_todo_ratio: float = 0.5
    allow_invented_params: bool = False
    allow_invented_raises: bool = False
    uncertain_annotation: bool = True

    # Runtime-only: not persisted to JSON.
    _api_key: str = field(default="", repr=False)

    # ------------------------------------------------------------------
    # Alternative constructors
    # ------------------------------------------------------------------

    @classmethod
    def from_json(cls, path: str | Path) -> "AIConfig":
        """Load an :class:`AIConfig` from a JSON file.

        Parameters
        ----------
        path : str | Path
            Path to the JSON config file.

        Returns
        -------
        AIConfig
            Populated configuration instance.

        Raises
        ------
        FileNotFoundError
            If *path* does not exist.
        ValueError
            If the JSON is malformed or contains unknown keys.
        """
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"AI config not found: {p}")
        raw = json.loads(p.read_text(encoding="utf-8"))
        raw.pop("_api_key", None)
        known = {f for f in cls.__dataclass_fields__ if not f.startswith("_")}
        unknown = set(raw) - known
        if unknown:
            raise ValueError(f"Unknown AIConfig keys: {sorted(unknown)}")
        return cls(**raw)

    @classmethod
    def default(cls) -> "AIConfig":
        """Return a default :class:`AIConfig` instance.

        Returns
        -------
        AIConfig
            Instance with all defaults applied.
        """
        return cls()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def to_json(self, path: str | Path) -> None:
        """Save this config to a JSON file.

        Parameters
        ----------
        path : str | Path
            Destination file path.  Parent directories are created if absent.
        """
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        data = {k: v for k, v in asdict(self).items() if not k.startswith("_")}
        p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @property
    def chat_endpoint(self) -> str:
        """Return the full chat-completions URL.

        Returns
        -------
        str
            URL combining *base_url* and the OpenAI completions path.
        """
        return self.base_url.rstrip("/") + "/chat/completions"

    def validation_config(self) -> "ValidationConfig":
        """Build a :class:`ValidationConfig` from this instance's fields.

        Returns
        -------
        ValidationConfig
            Ready to pass to :func:`docstring_validator.validate`.
        """
        from docstring_validator import ValidationConfig
        return ValidationConfig(
            max_line_length=self.max_line_length,
            max_todo_ratio=self.max_todo_ratio,
            min_confidence=self.min_confidence,
            allow_invented_params=self.allow_invented_params,
            allow_invented_raises=self.allow_invented_raises,
        )

    def validate(self) -> list[str]:
        """Return a list of validation error messages (empty if valid).

        Returns
        -------
        list[str]
            Human-readable error descriptions.
        """
        errors: list[str] = []
        if not self.base_url.startswith(("http://", "https://")):
            errors.append(f"base_url must start with http:// or https://, got: {self.base_url!r}")
        if not self.model.strip():
            errors.append("model must not be empty.")
        if self.timeout_seconds <= 0:
            errors.append(f"timeout_seconds must be > 0, got {self.timeout_seconds}.")
        if self.max_tokens < 64:
            errors.append(f"max_tokens must be >= 64, got {self.max_tokens}.")
        if not (0.0 <= self.temperature <= 2.0):
            errors.append(f"temperature must be in [0, 2], got {self.temperature}.")
        if self.workers < 1:
            errors.append(f"workers must be >= 1, got {self.workers}.")
        if self.min_confidence not in {"high", "medium", "low"}:
            errors.append(f"min_confidence must be 'high', 'medium', or 'low', got {self.min_confidence!r}.")
        if not (0.0 <= self.max_todo_ratio <= 1.0):
            errors.append(f"max_todo_ratio must be in [0, 1], got {self.max_todo_ratio}.")
        if self.max_line_length < 40:
            errors.append(f"max_line_length must be >= 40, got {self.max_line_length}.")
        return errors
