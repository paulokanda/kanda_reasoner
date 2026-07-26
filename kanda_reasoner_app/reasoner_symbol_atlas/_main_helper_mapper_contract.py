# project-path: kanda_reasoner_app/reasoner_symbol_atlas/_main_helper_mapper_contract.py
"""Neutral private contracts for main/helper mapper modules."""

from __future__ import annotations

from typing import Protocol

__all__: list[str] = []

_HELPER_SUFFIXES = (
    "_commands",
    "_command",
    "_helpers",
    "_helper",
    "_actions",
    "_action",
    "_adapter",
    "_adapters",
    "_writer",
    "_writers",
    "_schema",
    "_schemas",
    "_mapper",
    "_resolver",
    "_classifier",
    "_scanner",
    "_indexer",
    "_report",
    "_reports",
    "_utils",
    "_utility",
    "_utilities",
)
_STATUS_NO_HELPERS_FOUND = "no_helpers_found"
_STATUS_READY = "ready"


class _MainHelperDecisionLike(Protocol):
    """Structural view required by private decision formatting."""

    status: str
    target_role: str
    target_path: str
    main_path: str
    helper_paths: tuple[str, ...]
    confidence: str
    evidence: tuple[str, ...]
    warnings: tuple[str, ...]
    tests_to_run: tuple[str, ...]
