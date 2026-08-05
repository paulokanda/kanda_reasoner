# project-path: kanda_reasoner_app/reasoner_context_collector/_complete_json_web_ai_enrichment_analysis.py
"""Static analysis helpers for complete JSON Web-AI enrichment."""

from __future__ import annotations

import ast
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from kanda_reasoner_app.reasoner_context_collector.collector_scope import (
    iter_project_python_files,
)


def _read_text(path: Path) -> str:
    """Read UTF-8 text while replacing undecodable bytes."""
    return path.read_text(encoding="utf-8", errors="replace")


def _iter_python_files(project_root: Path, *args: object, **kwargs: object) -> list[Path]:
    """Return project-scoped Python files using the canonical collector scope."""
    del args, kwargs
    return list(iter_project_python_files(project_root))


def _safe_parse(path: Path) -> ast.AST | None:
    """Parse one Python file, returning None for syntax errors."""
    try:
        return ast.parse(_read_text(path), filename=str(path))
    except SyntaxError:
        return None


def _symbol_kind(node: ast.AST) -> str:
    """Return the stable symbol-kind label for an AST definition node."""
    if isinstance(node, ast.ClassDef):
        return "class"
    if isinstance(node, ast.AsyncFunctionDef):
        return "async_function"
    if isinstance(node, ast.FunctionDef):
        return "function"
    return "symbol"


def _responsibility_from_path(rel_path: str) -> str:
    """Derive a deterministic high-level responsibility label from a path."""
    lowered = rel_path.lower()
    if "runtime" in lowered:
        return "runtime evidence collection"
    if "collector" in lowered:
        return "static evidence collection"
    if "reasoner_retriever" in lowered or "retrieval" in lowered:
        return "retrieval and evidence selection"
    if "json_splitter" in lowered:
        return "json splitting and reassembly"
    if "manage_architecture" in lowered:
        return "architecture governance"
    if "manage_workflows" in lowered:
        return "workflow governance"
    if "gui" in lowered or "window" in lowered:
        return "gui behavior"
    if lowered.startswith("tools/validate_"):
        return "validation and regression protection"
    if "test" in lowered:
        return "test support"
    return "project support"


def _is_main_guard_test(test: ast.AST) -> bool:
    """Return whether an AST test structurally matches a __main__ guard."""
    if not isinstance(test, ast.Compare):
        return False
    if not isinstance(test.left, ast.Name) or test.left.id != "__name__":
        return False
    if len(test.ops) != 1 or not isinstance(test.ops[0], ast.Eq):
        return False
    if len(test.comparators) != 1:
        return False
    comparator = test.comparators[0]
    return isinstance(comparator, ast.Constant) and comparator.value == "__main__"


def _looks_like_entry_point(tree: ast.AST) -> bool:
    """Return whether a parsed module contains a structural __main__ guard."""
    for node in ast.walk(tree):
        if isinstance(node, ast.If) and _is_main_guard_test(node.test):
            return True
    return False


def _symbol_records(
    project_root: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any], list[dict[str, Any]]]:
    """Build symbol, primary-definition, and entry-point records."""
    symbol_index: list[dict[str, Any]] = []
    primary_definitions: dict[str, Any] = {}
    entry_points: list[dict[str, Any]] = []

    for path in _iter_python_files(project_root):
        rel_path = path.relative_to(project_root).as_posix()
        tree = _safe_parse(path)
        if not isinstance(tree, ast.Module):
            continue
        module_symbols: list[dict[str, Any]] = []
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                record = {
                    "name": node.name,
                    "kind": _symbol_kind(node),
                    "file": rel_path,
                    "line": int(node.lineno or 0),
                }
                module_symbols.append(record)
                primary_definitions.setdefault(node.name, []).append(record)
        if module_symbols:
            symbol_index.append(
                {
                    "file": rel_path,
                    "responsibility": _responsibility_from_path(rel_path),
                    "symbols": module_symbols,
                }
            )
        has_main_function = any(item["name"] == "main" for item in module_symbols)
        has_main_guard = _looks_like_entry_point(tree)
        if has_main_guard or has_main_function:
            entry_points.append(
                {
                    "file": rel_path,
                    "has_main_function": has_main_function,
                    "has_main_guard": has_main_guard,
                }
            )
    return symbol_index, primary_definitions, entry_points


def _file_responsibility_index(
    project_root: Path,
    symbol_index: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Build one deterministic responsibility record per Python source file."""
    by_file = {entry["file"]: entry for entry in symbol_index}
    records: list[dict[str, Any]] = []
    for path in _iter_python_files(project_root):
        rel_path = path.relative_to(project_root).as_posix()
        entry = by_file.get(rel_path, {})
        records.append(
            {
                "file": rel_path,
                "responsibility": _responsibility_from_path(rel_path),
                "public_symbols": [
                    item["name"]
                    for item in entry.get("symbols", [])
                    if not item["name"].startswith("_")
                ],
            }
        )
    return records


_GENERIC_PROTECTION_SYMBOLS = {
    "build",
    "clear",
    "close",
    "get",
    "load",
    "main",
    "open",
    "refresh",
    "run",
    "save",
    "set",
    "update",
    "validate",
    "require",
    "validate_static",
    "validate_real_qt",
    "validate_source_contract",
    "request_identity",
    "read_text",
    "load_json",
    "build_parser",
}
_PROTECTION_TOKEN_PATTERN = re.compile(r"[A-Za-z_][A-Za-z0-9_]{2,}")


def _protection_kind(relative_path: str) -> str:
    """Return the supported regression-protection kind for one Python path."""
    lowered = relative_path.casefold()
    parts = [part.casefold() for part in Path(relative_path).parts]
    if lowered.startswith("tools/validate_") and lowered.endswith(".py"):
        return "validator"
    if "test" in Path(relative_path).name.casefold() or "tests" in parts:
        return "test"
    return ""


def _production_protection_tokens(
    item: dict[str, Any],
) -> tuple[str, tuple[str, ...]]:
    """Return source-stem and public-symbol tokens for protection matching."""
    stem = Path(str(item["file"])).stem.casefold()
    symbols: list[str] = []
    for symbol in item.get("public_symbols", []):
        folded = str(symbol).casefold()
        if len(folded) < 4 or folded in _GENERIC_PROTECTION_SYMBOLS:
            continue
        if folded not in symbols:
            symbols.append(folded)
    return stem, tuple(symbols)



_STATE_SUFFIXES = (
    "_identity",
    "_epoch",
    "_hash",
    "_worker",
    "_context",
    "_snapshot",
    "_approval_id",
    "_session_id",
    "_project_id",
    "_model_id",
    "_gateway_id",
)
_STATE_FRAGMENTS = (
    "active",
    "request",
    "identity",
    "epoch",
    "hash",
    "worker",
    "context",
    "snapshot",
    "approval",
    "session",
    "project",
    "config",
    "model",
    "gateway",
    "provider",
    "chat",
    "source",
)
_STATE_IDENTIFIER_EXCLUSIONS = {
    "kanda_reasoner_app",
    "reasoner_engine",
    "project",
    "support",
    "runtimeerror",
    "__future__",
    "__class__",
    "__name__",
    "__init__",
}


def _state_identifiers(text: str) -> tuple[str, ...]:
    """Return bounded state identifiers useful for behavior protection."""
    found: list[str] = []
    for raw in _PROTECTION_TOKEN_PATTERN.findall(text):
        folded = raw.casefold()
        if len(folded) < 6 or folded in _STATE_IDENTIFIER_EXCLUSIONS:
            continue
        if not any(fragment in folded for fragment in _STATE_FRAGMENTS):
            continue
        is_camel = (
            not raw.isupper()
            and any(character.isupper() for character in raw[1:])
        )
        is_state = folded.startswith("_") or folded.endswith(_STATE_SUFFIXES)
        if not is_camel and not is_state:
            continue
        if folded.startswith("validate_") or folded.startswith("test_"):
            continue
        if folded not in found:
            found.append(folded)
    return tuple(found[:120])


def _state_identifier_weight(identifier: str) -> int:
    """Return deterministic weight for one shared state identifier."""
    if identifier.startswith("_active_"):
        return 360
    if identifier in {
        "projectwebairequestidentity",
        "project_epoch",
        "context_hash",
        "evidence_context_hash",
        "waiting_for_worker",
    }:
        return 300
    if identifier.endswith(("_identity", "_epoch", "_hash")):
        return 220
    return 100


def _protection_matches(
    production_path: str,
    production_stem: str,
    production_symbols: tuple[str, ...],
    production_state_identifiers: tuple[str, ...],
    protection_path: str,
    protection_text: str,
    protection_tokens: set[str],
) -> tuple[int, tuple[str, ...]]:
    """Return ranked match evidence between source and protection code."""
    path_folded = protection_path.casefold()
    reasons: list[str] = []
    score = 0
    if production_path.casefold() in protection_text:
        reasons.append("source_path")
        score += 200
    if production_stem in protection_tokens or production_stem in path_folded:
        reasons.append("source_stem:" + production_stem)
        score += 40
    for symbol in production_symbols:
        if symbol in protection_tokens:
            reasons.append("symbol:" + symbol)
            score += 100
    for identifier in production_state_identifiers:
        if identifier in protection_tokens:
            reasons.append("state_identifier:" + identifier)
            score += _state_identifier_weight(identifier)
    return score, tuple(reasons)

def _test_protection_index(
    project_root: Path,
    responsibility_index: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Build test and validator protection evidence for project source files."""
    production_details: list[
        tuple[dict[str, Any], str, tuple[str, ...], tuple[str, ...]]
    ] = []
    for item in responsibility_index:
        production_path = str(item["file"])
        if _protection_kind(production_path):
            continue
        production_stem, production_symbols = _production_protection_tokens(item)
        state_identifiers = _state_identifiers(
            _read_text(project_root / production_path)
        )
        production_details.append(
            (item, production_stem, production_symbols, state_identifiers)
        )
    source_tokens = {
        token
        for _, production_stem, production_symbols, state_identifiers
        in production_details
        for token in (production_stem, *production_symbols, *state_identifiers)
        if token
    }
    protections: list[tuple[str, str, str, set[str]]] = []
    token_to_protections: dict[str, list[int]] = {}
    for path in _iter_python_files(project_root):
        relative = path.relative_to(project_root).as_posix()
        kind = _protection_kind(relative)
        if not kind:
            continue
        text_folded = _read_text(path).casefold()
        text_tokens = set(_PROTECTION_TOKEN_PATTERN.findall(text_folded))
        matched_tokens = text_tokens.intersection(source_tokens)
        index = len(protections)
        protections.append((relative, kind, text_folded, text_tokens))
        for token in matched_tokens:
            token_to_protections.setdefault(token, []).append(index)

    records: list[dict[str, Any]] = []
    for (
        item,
        production_stem,
        production_symbols,
        production_state_identifiers,
    ) in production_details:
        production_path = str(item["file"])
        candidate_indexes: set[int] = set()
        for token in (
            production_stem,
            *production_symbols,
            *production_state_identifiers,
        ):
            candidate_indexes.update(token_to_protections.get(token, []))
        matches: list[dict[str, Any]] = []
        for index in sorted(candidate_indexes):
            (
                protection_path,
                kind,
                protection_text,
                protection_tokens,
            ) = protections[index]
            if protection_path == production_path:
                continue
            score, reasons = _protection_matches(
                production_path,
                production_stem,
                production_symbols,
                production_state_identifiers,
                protection_path,
                protection_text,
                protection_tokens,
            )
            if score:
                matches.append(
                    {
                        "file": protection_path,
                        "kind": kind,
                        "score": score,
                        "match_reasons": list(reasons),
                    }
                )
        matches.sort(
            key=lambda record: (
                -int(record["score"]),
                str(record["kind"]),
                str(record["file"]),
            )
        )
        protected_identifiers = sorted(
            {
                reason.split(":", 1)[1]
                for record in matches
                for reason in record["match_reasons"]
                if reason.startswith("state_identifier:")
            }
        )
        related_tests = [
            record["file"] for record in matches if record["kind"] == "test"
        ]
        related_validators = [
            record["file"]
            for record in matches
            if record["kind"] == "validator"
        ]
        records.append(
            {
                "file": production_path,
                "has_related_test": bool(related_tests),
                "related_tests": related_tests[:10],
                "has_related_validator": bool(related_validators),
                "related_validators": related_validators[:20],
                "has_related_protection": bool(matches),
                "protected_identifiers": protected_identifiers[:80],
                "protection_matches": matches[:20],
            }
        )
    return records

def _stable_evidence_index(sections: dict[str, Any]) -> dict[str, Any]:
    """Build deterministic short evidence identifiers for generated sections."""
    evidence: dict[str, Any] = {}
    for section_name, section_value in sorted(sections.items()):
        encoded = json.dumps(section_value, sort_keys=True, default=str)
        evidence_id = hashlib.sha256(
            (section_name + "\n" + encoded).encode("utf-8")
        ).hexdigest()[:16]
        evidence[evidence_id] = {
            "section": section_name,
            "sha256_16": evidence_id,
        }
    return evidence
