#!/usr/bin/env python3
# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/ai_config.py
"""Configuration dataclass for the local AI docstring generator."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass
class AIConfig:
    """Settings that control how the AI docstring generator connects and behaves."""

    base_url: str = "http://localhost:11434/v1"
    model: str = "codellama:13b"
    timeout_seconds: float = 30.0
    max_tokens: int = 512
    temperature: float = 0.0
    fallback_to_heuristic: bool = True
    require_ai_success: bool = False
    use_structured_outputs: bool = True
    workers: int = 1
    cache_enabled: bool = True
    cache_path: str = ".docstring_cache.json"
    docstring_style: str = "numpy"
    include_private: bool = True
    min_confidence: str = "low"
    max_line_length: int = 88
    max_todo_ratio: float = 0.5
    allow_invented_params: bool = False
    allow_invented_raises: bool = False
    uncertain_annotation: bool = True
    max_docstring_length: int = 4000
    seed: int | None = 7
    _api_key: str = field(default="", repr=False)

    @classmethod
    def from_json(cls, path: str | Path) -> "AIConfig":
        """Support from json behavior.
        
        Parameters
        ----------
        path : str | Path
            The file or folder path.
        
        Returns
        -------
        'AIConfig'
            The 'aiconfig' result.
        """
        
        config_path = Path(path)
        if not config_path.exists():
            raise FileNotFoundError(f"AI config not found: {config_path}")
        raw = json.loads(config_path.read_text(encoding="utf-8"))
        raw.pop("_api_key", None)
        known = {name for name in cls.__dataclass_fields__ if not name.startswith("_")}
        unknown = set(raw) - known
        if unknown:
            raise ValueError(f"Unknown AIConfig keys: {sorted(unknown)}")
        cfg = cls(**raw)
        if cfg.require_ai_success:
            cfg.fallback_to_heuristic = False
        return cfg

    @classmethod
    def default(cls) -> "AIConfig":
        """Support default behavior.
        
        Returns
        -------
        'AIConfig'
            The 'aiconfig' result.
        """
        
        return cls()

    def to_json(self, path: str | Path) -> None:
        """Support to json behavior.
        
        Parameters
        ----------
        path : str | Path
            The file or folder path.
        """
        
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        data = {key: value for key, value in asdict(self).items() if not key.startswith("_")}
        output_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
