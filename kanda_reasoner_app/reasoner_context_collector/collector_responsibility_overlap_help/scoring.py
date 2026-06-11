"""Private scoring helpers for collector_responsibility_overlap."""

from __future__ import annotations
# PASS_068A_OVERLAP_CONSTANT_BINDINGS_START
# Runtime bindings restored after helper extraction.
globals().update({
    'GENERIC_TOKENS': set(['ui', 'widget', 'button', 'dialog', 'window', 'tab', 'panel', 'bar', 'menu', 'layout', 'tool', 'tools', 'template', 'templates', 'base', 'common', 'utils', 'util', 'helper', 'helpers', 'core', 'main', 'app', 'manager', 'controller', 'service', 'data', 'file', 'files', 'module', 'modules', 'test', 'tests', 'view', 'builder', 'handler']),
    'GENERIC_CALL_ROOTS': set(['connect', 'emit', 'show', 'hide', 'update', 'refresh', 'clear', 'reset', 'close', 'open', 'load', 'save', 'append', 'remove', 'settext', 'setvalue', 'setenabled', 'setvisible', 'addwidget', 'addlayout', 'addtab', 'setlayout', 'setcentralwidget', 'resize', 'move', 'exec', 'exec_', 'start', 'stop', 'plot', 'render', 'draw']),
    'GENERIC_ROLE_TOKENS': set(['ui', 'service', 'controller', 'domain', 'general', 'visualization']),
    'MIN_OVERLAP_SCORE': 1.55,
    'MIN_HOTSPOT_SCORE': 1.95,
})
# PASS_068A_OVERLAP_CONSTANT_BINDINGS_END

from typing import Any

__all__: list[str] = []

def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    union = a | b
    if not union:
        return 0.0
    return len(a & b) / len(union)

def _strong_signal_count(
    base_name_score: float,
    semantic_role_score: float,
    summary_term_score: float,
    symbol_score: float,
    call_score: float,
) -> int:
    count = 0
    if base_name_score >= 0.55:
        count += 1
    if semantic_role_score >= 0.55:
        count += 1
    if summary_term_score >= 0.35:
        count += 1
    if symbol_score >= 0.30:
        count += 1
    if call_score >= 0.30:
        count += 1
    return count

def _passes_gate(
    base_name_score: float,
    semantic_role_score: float,
    summary_term_score: float,
    symbol_score: float,
    call_score: float,
    overlap_score: float,
    strong_signal_count: int,
) -> bool:
    if base_name_score >= 0.60 and summary_term_score >= 0.30:
        return True

    if summary_term_score >= 0.45 and symbol_score >= 0.35:
        return True

    if semantic_role_score >= 0.60 and summary_term_score >= 0.35 and call_score >= 0.25:
        return True

    if strong_signal_count >= 4 and overlap_score >= MIN_OVERLAP_SCORE:
        return True

    if symbol_score >= 0.40 and call_score >= 0.35 and summary_term_score >= 0.25:
        return True

    return False
