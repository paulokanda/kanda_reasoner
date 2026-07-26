# project-path: kanda_reasoner_app/manage_architecture/warning_test_protection_family_evidence.py
"""Score strong existing-test family relationships for warning remediation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

__all__ = [
    "TestFamilyEvidence",
    "score_test_family_evidence",
]

_ROLE_TOKENS = {
    "action",
    "adapter",
    "builder",
    "contract",
    "controller",
    "dialog",
    "engine",
    "formatting",
    "gui",
    "intake",
    "layout",
    "manifest",
    "models",
    "orchestration",
    "orchestrator",
    "policy",
    "qt",
    "runtime",
    "service",
    "spec",
    "store",
    "worker",
}

_NOISE_TOKENS = {
    "py",
    "test",
    "tests",
    "validation",
    "validate",
}


@dataclass(frozen=True, slots=True)
class TestFamilyEvidence:
    """Describe bounded evidence that a test already owns a source family."""

    score_bonus: int
    reasons: tuple[str, ...]
    is_strong: bool


def _tokens(value: str) -> tuple[str, ...]:
    """Return normalized identifier tokens without version and test noise."""
    raw = re.findall(r"[a-z0-9]+", value.lower().replace("\\", "/"))
    return tuple(
        token
        for token in raw
        if token not in _NOISE_TOKENS
        and not re.fullmatch(r"v\d+", token)
        and not token.isdigit()
    )


def _feature_tokens(source_stem: str) -> set[str]:
    """Return meaningful source-family tokens, excluding implementation roles."""
    tokens = set(_tokens(source_stem))
    meaningful = tokens - _ROLE_TOKENS
    return meaningful or tokens


def _test_name_tokens(test_path: Path) -> set[str]:
    """Return tokens from the test filename and its two nearest parent folders."""
    parts = [test_path.stem]
    parents = list(test_path.parts[:-1])
    parts.extend(parents[-2:])
    return set(_tokens("_".join(parts)))


def _imports_source_package_sibling(
    source_module: str,
    imported_modules: set[str],
) -> bool:
    """Return True when a test imports a sibling from the same source package."""
    source_package, separator, _ = source_module.rpartition(".")
    if not separator:
        return False
    prefix = source_package + "."
    return any(
        imported != source_module and imported.startswith(prefix)
        for imported in imported_modules
    )


def score_test_family_evidence(
    *,
    source_module: str,
    source_stem: str,
    test_path: Path,
    imported_modules: set[str],
    source_public_symbols: tuple[str, ...],
    test_text: str,
) -> TestFamilyEvidence:
    """Score only strong, explainable existing-test family relationships."""
    feature_tokens = _feature_tokens(source_stem)
    test_tokens = _test_name_tokens(test_path)
    overlap = sorted(feature_tokens & test_tokens)
    sibling_import = _imports_source_package_sibling(
        source_module,
        imported_modules,
    )
    symbol_hit = any(
        re.search(rf"\b{re.escape(symbol)}\b", test_text)
        for symbol in source_public_symbols
    )

    score = 0
    reasons: list[str] = []

    if sibling_import:
        score += 5
        reasons.append("imports_source_package_sibling")

    if len(overlap) >= 2:
        score += min(8, 2 * len(overlap))
        reasons.append("test_name_matches_feature_family")

    if symbol_hit:
        score += 2
        reasons.append("references_source_public_symbol")

    strong = (
        sibling_import
        and len(overlap) >= 2
        and symbol_hit
    ) or (
        len(overlap) >= 3
        and symbol_hit
    )

    if strong:
        reasons.append("strong_existing_test_family")

    return TestFamilyEvidence(
        score_bonus=score,
        reasons=tuple(sorted(set(reasons))),
        is_strong=strong,
    )
