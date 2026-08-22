# project-path: kanda_reasoner_app/reasoner_context_collector/collector_responsibility_overlap_help/scoring.py
"""Private scoring helpers for collector_responsibility_overlap."""

from __future__ import annotations
# PASS_068A_OVERLAP_CONSTANT_BINDINGS_START
# Explicit module-level bindings preserve the helper-extraction runtime values
# while remaining statically visible to Ruff and other source analyzers.
GENERIC_TOKENS = set(['ui', 'widget', 'button', 'dialog', 'window', 'tab', 'panel', 'bar', 'menu', 'layout', 'tool', 'tools', 'template', 'templates', 'base', 'common', 'utils', 'util', 'helper', 'helpers', 'core', 'main', 'app', 'manager', 'controller', 'service', 'data', 'file', 'files', 'module', 'modules', 'test', 'tests', 'view', 'builder', 'handler'])
GENERIC_CALL_ROOTS = set(['connect', 'emit', 'show', 'hide', 'update', 'refresh', 'clear', 'reset', 'close', 'open', 'load', 'save', 'append', 'remove', 'settext', 'setvalue', 'setenabled', 'setvisible', 'addwidget', 'addlayout', 'addtab', 'setlayout', 'setcentralwidget', 'resize', 'move', 'exec', 'exec_', 'start', 'stop', 'plot', 'render', 'draw'])
GENERIC_ROLE_TOKENS = set(['ui', 'service', 'controller', 'domain', 'general', 'visualization'])
MIN_OVERLAP_SCORE = 1.55
MIN_HOTSPOT_SCORE = 1.95
# PASS_068A_OVERLAP_CONSTANT_BINDINGS_END


__all__: list[str] = []

def _jaccard(a: set[str], b: set[str]) -> float:
    """Support jaccard behavior.
    
    Parameters
    ----------
    a : set[str]
        The a value.
    b : set[str]
        The b value.
    
    Returns
    -------
    float
        The floating-point result.
    """
    
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
    """Support strong signal count behavior.
    
    Parameters
    ----------
    base_name_score : float
        The base name score value.
    semantic_role_score : float
        The semantic role score value.
    summary_term_score : float
        The summary term score value.
    symbol_score : float
        The symbol score value.
    call_score : float
        The call score value.
    
    Returns
    -------
    int
        The integer result.
    """
    
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
    """Support passes gate behavior.
    
    Parameters
    ----------
    base_name_score : float
        The base name score value.
    semantic_role_score : float
        The semantic role score value.
    summary_term_score : float
        The summary term score value.
    symbol_score : float
        The symbol score value.
    call_score : float
        The call score value.
    overlap_score : float
        The overlap score value.
    strong_signal_count : int
        The strong signal count value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
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
