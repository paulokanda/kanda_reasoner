# project-path: kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/output_firewall.py
"""Output firewall for Phase 1a advisory signal objects."""

from __future__ import annotations

from dataclasses import fields, is_dataclass
from enum import Enum
from typing import Any


FORBIDDEN_ADVISORY_FIELD_NAMES = frozenset(
    {
        "route",
        "selected_route",
        "final_route",
        "selected_prompt",
        "final_prompt",
        "decision",
        "override",
        "must_route",
        "must_not_route",
        "ranking",
        "rankings",
        "winner",
        "best_candidate",
        "advisory_rankings",
        "advisory_explanation",
        "explanation",
        "notes",
        "free_text",
    }
)

FORBIDDEN_AUTHORITY_TOKENS = frozenset(
    {
        "final route",
        "selected route",
        "override router",
        "must route",
        "winner",
        "best candidate",
        "ranking",
        "rankings",
        "route authority",
    }
)


def validate_advisory_output(output: Any) -> None:
    """Reject route-authority fields or free-text authority leaks."""

    _walk_value(output, path="output")


def _walk_value(value: Any, *, path: str) -> None:
    """Support walk value behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    path : str
        The file or folder path.
    """
    
    if is_dataclass(value):
        for field in fields(value):
            _validate_name(field.name, path)
            _walk_value(getattr(value, field.name), path=f"{path}.{field.name}")
        return
    if isinstance(value, tuple):
        for index, item in enumerate(value):
            _walk_value(item, path=f"{path}[{index}]")
        return
    if isinstance(value, list):
        raise TypeError(f"{path} must not contain list values; use immutable tuples")
    if isinstance(value, dict):
        raise TypeError(f"{path} must not contain generic dictionaries")
    if isinstance(value, Enum):
        _validate_text(value.value, path)
        return
    if isinstance(value, str):
        _validate_text(value, path)
        return
    if isinstance(value, (bool, int, float)) or value is None:
        return
    raise TypeError(f"{path} contains unsupported type: {type(value).__name__}")


def _validate_name(name: str, path: str) -> None:
    """Support validate name behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    path : str
        The file or folder path.
    """
    
    normalized = name.strip().lower()
    if normalized in FORBIDDEN_ADVISORY_FIELD_NAMES:
        raise ValueError(f"Forbidden advisory field name at {path}: {name}")


def _validate_text(text: str, path: str) -> None:
    """Support validate text behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    path : str
        The file or folder path.
    """
    
    normalized = text.strip().lower()
    for token in FORBIDDEN_AUTHORITY_TOKENS:
        if token in normalized:
            raise ValueError(f"Forbidden advisory authority token at {path}: {token}")
