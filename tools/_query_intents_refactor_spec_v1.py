# project-path: tools/_query_intents_refactor_spec_v1.py
"""Static specification and data-characterization helpers for the query-intent AST-safe facade refactor.

This module holds the immutable characterization data (hashes, path contracts,
public-name surface, baseline corpus terms) and the pure, dependency-free
helpers that only need that data. Splitting it out keeps the runtime validator
under the 101-499 line gate while preserving the public contract unchanged.
"""
from __future__ import annotations

import ast
import hashlib
import inspect
import json
import warnings
from pathlib import Path
from typing import Any

__all__ = []

FEATURE_ID = "query-intents-ast-safe-facade-refactor-v1"
MODULE_NAME = (
    "kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.query_intents"
)
HELPER_MODULE_NAME = (
    "kanda_reasoner_app.reasoner_engine.reasoner_retriever_help."
    "_query_intent_location_and_explanation"
)
TARGET_RELATIVE_PATH = Path(
    "kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/query_intents.py"
)
HELPER_RELATIVE_PATH = Path(
    "kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/"
    "_query_intent_location_and_explanation.py"
)
MANIFEST_RELATIVE_PATH = Path(
    "kanda_reasoner_app/reasoner_engine/reasoner_retriever_help.json"
)
VALIDATOR_RELATIVE_PATH = Path(
    "tools/validate_query_intents_ast_safe_refactor_v1.py"
)
EXPECTED_HASHES = {
    TARGET_RELATIVE_PATH.as_posix():
        "37f0610afc9c4a3ec88c8df0b6e354386804d84c7dd5d84aa464dc03c1c28f0c",
    HELPER_RELATIVE_PATH.as_posix():
        "2e8c3b13252f8d83e8d5790a2fe303f78794c61a466b74442a9bb2a51fa4d57a",
    MANIFEST_RELATIVE_PATH.as_posix():
        "3ca3695e0a15cf308dcb8c35dc9c2c379809bc445ea260cdd6cd02e2373fa09e",
}
BASELINE_ENTRY = "validation_data/query_intents_baseline.py.txt"
BASELINE_SOURCE_SHA256 = (
    "7d62db6c9eda1d397d2c58e1d7f93d400a30ad1cef3edbd0526417e096e70026"
)
EXPECTED_CONSUMERS_ENTRY = "validation_data/query_intents_expected_consumers.json"
EXPECTED_CONSUMERS_SHA256 = "6dd16f6c0c87b8792c7a81138301f19922d02916587b058ce39aa6fa994d9488"
ERROR_LESSON_ENTRIES = (
    "payload/error_memory_receive_blocks/KANDA_ERROR_LESSON_JSON_query_intents_public_docstring_whitespace_v1.txt",
    "payload/error_memory_receive_blocks/KANDA_ERROR_LESSON_JSON_query_intents_consumer_count_drift_v1.txt",
)
RAW_ERROR_ENTRIES = (
    "payload/error_memory_receive_blocks/RAW_ERROR_EVIDENCE_query_intents_public_docstring_whitespace_v1.txt",
    "payload/error_memory_receive_blocks/RAW_ERROR_EVIDENCE_query_intents_consumer_count_drift_v1.txt",
)
PUBLIC_NAMES = (
    'is_startup_question',
    'is_explicit_call_chain_question',
    'is_main_window_show_responsibility_question',
    'is_qtimer_showmaximized_question',
    'is_where_is_called_question',
    'is_where_is_question',
    'is_which_method_calls_question',
    'is_explain_chain_question',
    'is_explanatory_question',
    'is_code_localized_explanation_question',
    'is_topomap_explanation_question',
    'is_topomap_implementation_question',
    'is_runtime_heavy_question',
    'is_packaging_metadata_question',
    'is_documentation_intent_question',
    'detect_query_intents',
)
BASELINE_TERMS = (
    'Support V10 project reasoning and evidence handling.', '\\bon_[a-z0-9_]+\\b', 'adr', 'ambiguous',
    'amplitude map', 'app start', 'application start', 'architecture',
    'architecture doc', 'architecture terms', 'build backend', 'call',
    'call chain', 'callback', 'called', 'called in ',
    'calls qtimer.singleshot', 'calls self.', 'calls self.v.main_window.show', 'chain',
    'cleanup chain', 'code evidence', 'code localization', 'code location',
    'code_localized_explanation', 'connect', 'console script', 'creating',
    'declared dependencies', 'declared dependency', 'dependencies', 'dependency',
    'describe', 'directly calls', 'disconnect', 'docs',
    'documentation', 'documentation intent', 'documentation_intent', 'emit',
    'entry point', 'entrypoint', 'event loop', 'exception',
    'execution at runtime', 'execution chain', 'explain', 'explain chain',
    'explain directly in plain prose the chain', 'explain the chain', 'explain_chain', 'explanatory',
    'explicit_call_chain', 'external integrations', 'file path and code', 'flow',
    'flow from', 'gui script', 'handler', 'implement',
    'implementation', 'implementation of', 'implemented', 'implements',
    'in which file is', 'include code', 'invoke', 'invoked',
    'invoked in ', 'launch', 'line level snippet', 'line level snippets',
    'line numbers', 'line-level snippet', 'line-level snippets', 'listener',
    'main entry', 'main window', 'main window is shown', 'main_window_show',
    'method most directly responsible for showing the main window', 'method that calls self.v.main_window.show', 'modules participate', 'named features',
    'open app', 'package info', 'package manager', 'package metadata',
    'packaging info', 'packaging metadata', 'packaging_metadata', 'participate in creating',
    'participate in updating', 'pipfile', 'poetry.lock', 'probe',
    'project purpose', 'pyproject', 'qapplication', 'qtimer.singleshot',
    'qtimer_showmaximized', 'readme', 'reference', 'reference to ',
    'references ', 'requirements', 'reset chain', 'responsibility split',
    'responsible for showing the main window', 'risk', 'run instructions', 'runtime',
    'runtime trace', 'runtime_heavy', 'self.v.main_window.show', 'self.v.main_window.show()',
    'self.v.main_window.showmaximized', 'sequence from', 'setup.cfg', 'setup.py',
    'show code', 'show snippet', 'show snippets', 'show(',
    'showing the main window', 'showmaximized', 'signal', 'slot',
    'start up', 'startup', 'startup chain', 'summarize',
    'symbol and code', 'symbol most directly responsible for showing the main window', 'thread', 'timeline chain',
    'timer', 'tooling', 'topomap', 'topomap_explanation',
    'topomap_implementation', 'trace', 'trace at runtime', 'trace the chain',
    'trace the startup', 'uncertainty', 'unclear', 'unknown',
    'until main window is shown', 'until the main window is shown', 'updating', 'uv.lock',
    'walk through', 'warning', 'what does this project do', 'what file contains',
    'what file defines', 'what file has', 'what file includes', 'what file is the source of',
    'what file records', 'what function calls', 'what is this project for', 'what method calls',
    'where defined', 'where implemented', 'where in code', 'where is ',
    'where is actually called', 'where is actually invoked', 'where is declared', 'where is defined',
    'where is implemented', 'where is it called', 'where is it invoked', 'where is the ',
    'where is this ', 'where_is', 'which code implements', 'which file contains',
    'which file defines', 'which file has', 'which file includes', 'which file is the source of',
    'which file records', 'which function calls', 'which method calls', 'which modules participate',
    'which_calls', 'who calls', 'who calls ', 'who invokes ',
    'with code', 'with code evidence', 'workflow described',
)


def _sha256(path: Path) -> str:
    """Return the SHA-256 digest for a file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _assert(condition: bool, message: str) -> None:
    """Raise a deterministic validation error when condition is false."""
    if not condition:
        raise AssertionError(message)


def _build_corpus() -> list[str]:
    """Build the fixed characterization corpus used for baseline capture."""
    items = {
        "",
        "plain unrelated question",
        "ON_CLICKED handler",
        "QTimer.SingleShot self.v.main_window.showMaximized",
    }
    for term in BASELINE_TERMS:
        items.add(term)
        items.add("please " + term)
        items.add(term.upper())
    combo_terms = list(BASELINE_TERMS[:30])
    for left, right in zip(combo_terms, reversed(combo_terms)):
        items.add(left + " " + right)
    return sorted(items)


def _parse_source(text: str, filename: str) -> ast.Module:
    """Parse Python while suppressing non-fatal syntax warnings."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", SyntaxWarning)
        return ast.parse(text, filename=filename)


def _digest(value: Any) -> str:
    """Return a deterministic JSON digest for validation evidence."""
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def _snapshot(module: Any) -> dict[str, Any]:
    """Return public-contract and behavior characterization data."""
    contract: dict[str, Any] = {}
    for name in PUBLIC_NAMES:
        obj = getattr(module, name)
        contract[name] = {
            "signature": str(inspect.signature(obj)),
            "annotations": dict(getattr(obj, "__annotations__", {})),
            "doc": getattr(obj, "__doc__", None),
            "module": getattr(obj, "__module__", None),
            "qualname": getattr(obj, "__qualname__", None),
        }
    rows = []
    for query in _build_corpus():
        values = {name: getattr(module, name)(query) for name in PUBLIC_NAMES}
        rows.append([query, values])
    return {"all": module.__all__, "contract": contract, "rows": rows}
