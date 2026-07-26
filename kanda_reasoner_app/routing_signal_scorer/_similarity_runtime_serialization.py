"""Corpus loading, tokenization, and lexical similarity primitives."""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Mapping


def _load_similarity_corpus() -> dict[str, object]:
    """Load the frozen routing-similarity corpus."""

    corpus_path = (
        Path(__file__).resolve().parent
        / "design"
        / "routing_signal_scorer_v2_similarity_test_corpus.json"
    )
    data = json.loads(corpus_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return {"cases": []}
    return data


def _text_profile(text: str) -> dict[str, set[str]]:
    """Build token and bigram sets for lexical similarity."""

    tokens = _tokenize_for_similarity(text)
    bigrams = {
        tokens[index] + " " + tokens[index + 1]
        for index in range(max(0, len(tokens) - 1))
    }
    return {
        "tokens": set(tokens),
        "bigrams": bigrams,
    }


def _tokenize_for_similarity(text: str) -> list[str]:
    """Tokenize text with the deterministic runtime-lite policy."""

    raw = re.findall(r"[a-z0-9_]+", str(text or "").lower())
    stop_words = {
        "a",
        "an",
        "and",
        "are",
        "as",
        "be",
        "by",
        "for",
        "from",
        "give",
        "i",
        "if",
        "in",
        "include",
        "is",
        "it",
        "me",
        "must",
        "of",
        "on",
        "or",
        "the",
        "this",
        "to",
        "use",
        "what",
        "when",
        "with",
        "you",
    }
    return [item for item in raw if len(item) > 1 and item not in stop_words]


def _profile_similarity(
    left: Mapping[str, set[str]],
    right: Mapping[str, set[str]],
) -> float:
    """Calculate the weighted similarity between two lexical profiles."""

    left_tokens = set(left.get("tokens", set()))
    right_tokens = set(right.get("tokens", set()))
    left_bigrams = set(left.get("bigrams", set()))
    right_bigrams = set(right.get("bigrams", set()))

    token_score = _jaccard(left_tokens, right_tokens)
    bigram_score = _jaccard(left_bigrams, right_bigrams)
    containment = _containment(left_tokens, right_tokens)
    return (0.5 * token_score) + (0.25 * bigram_score) + (0.25 * containment)


def _jaccard(left: set[str], right: set[str]) -> float:
    """Return the Jaccard score for two non-empty sets."""

    if not left or not right:
        return 0.0
    union = left | right
    if not union:
        return 0.0
    return len(left & right) / len(union)


def _containment(query: set[str], candidate: set[str]) -> float:
    """Return query-token containment in the candidate set."""

    if not query or not candidate:
        return 0.0
    return len(query & candidate) / len(query)
