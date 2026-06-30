# project-path: kanda_reasoner_app/reasoner_engine/v10_models.py
"""Support V10 project reasoning and evidence handling."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class EvidenceItem:
    """Represent evidence item."""
    
    evidence_id: str
    score: int
    path: str
    module_name: str
    reason: str
    detail: str


@dataclass
class SymbolEvidenceItem:
    """Represent symbol evidence item."""
    
    evidence_id: str
    score: int
    symbol_name: str
    kind: str
    path: str
    line: int
    reason: str
    detail: str


@dataclass
class RetrievalBundle:
    """Represent retrieval bundle."""
    
    file_evidence: list[EvidenceItem] = field(default_factory=list)
    symbol_evidence: list[SymbolEvidenceItem] = field(default_factory=list)
    snippet_evidence: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ConversationTurn:
    """Represent conversation turn."""
    
    question: str
    answer: str
    prompt: str
    retrieval: RetrievalBundle
    selected_model: str






