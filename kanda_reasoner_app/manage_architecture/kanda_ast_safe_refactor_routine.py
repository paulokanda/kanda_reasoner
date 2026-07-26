# project-path: kanda_reasoner_app/manage_architecture/kanda_ast_safe_refactor_routine.py
"""Reusable read-only preflight and family verification for KPR-06-003 work.

The routine belongs to Architecture Review -> Large Module AST Split Audit. It
verifies exchange identity, candidate-family structure, semantic dynamic risks,
line-law compliance, and fresh authoritative AST audit results. It does not
rewrite source, mutate GUI state, alter queues, or write frozen memory.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from kanda_reasoner_app.manage_architecture.kanda_refactor_project_index import (
    capture_public_contract,
)
from kanda_reasoner_app.manage_architecture.kanda_refactor_semantic_safety import (
    check_candidate_dependency_direction,
    detect_semantic_dynamic_risks,
)

__all__ = [
    "build_exchange_preflight",
    "extract_exchange_payload",
    "module_summary",
    "run_project_ast_audit",
    "verify_candidate_family",
]


def _sha256(raw: bytes) -> str:
    """Return lowercase SHA-256 for exact bytes."""
    return hashlib.sha256(raw).hexdigest()


def _read_text(path: Path) -> str:
    """Read UTF-8 exchange or evidence text without replacement decoding."""
    return path.read_text(encoding="utf-8", errors="strict")


def _extract_field(text: str, name: str) -> str:
    """Extract one NAME: value field from a KPR exchange."""
    pattern = re.compile(r"^" + re.escape(name) + r":\s*(.+)$", re.MULTILINE)
    match = pattern.search(text)
    if match is None:
        raise ValueError("Missing field: " + name)
    return match.group(1).strip()


def _extract_block(text: str, begin: str, end: str) -> str:
    """Extract a marker-delimited text block while preserving internal bytes."""
    begin_marker = begin + "\n"
    start = text.rfind(begin_marker)
    if start < 0:
        raise ValueError("Missing marker: " + begin)
    start += len(begin_marker)
    end_marker = "\n" + end
    finish = text.find(end_marker, start)
    if finish < 0:
        raise ValueError("Missing marker: " + end)
    return text[start:finish]


def _extract_source_block(text: str) -> str:
    """Extract exact source text using the wrapper's explicit newline contract."""
    source = _extract_block(text, "TARGET_SOURCE_BEGIN", "TARGET_SOURCE_END")
    ends_with_newline_text = ""
    try:
        ends_with_newline_text = _extract_field(text, "SOURCE_TEXT_ENDS_WITH_NEWLINE")
    except ValueError:
        ends_with_newline_text = "unknown"
    normalized = ends_with_newline_text.lower()
    if normalized == "true" and not source.endswith("\n"):
        source += "\n"
    if normalized == "false" and source.endswith("\n"):
        source = source[:-1]
    return source


def extract_exchange_payload(exchange_text: str) -> dict[str, Any]:
    """Parse one KPR-06-003 exchange into exact identity and evidence fields."""
    source = _extract_source_block(exchange_text)
    audit = _extract_block(exchange_text, "AST_AUDIT_RESULT_BEGIN", "AST_AUDIT_RESULT_END")
    preflight_evidence = ""
    marker_begin = "AST_SAFE_REFACTOR_PREFLIGHT_EVIDENCE_BEGIN"
    marker_end = "AST_SAFE_REFACTOR_PREFLIGHT_EVIDENCE_END"
    if marker_begin in exchange_text and marker_end in exchange_text:
        preflight_evidence = _extract_block(exchange_text, marker_begin, marker_end)
    payload = {
        "target_relative_path": _extract_field(exchange_text, "TARGET_RELATIVE_PATH"),
        "source_sha256": _extract_field(exchange_text, "SOURCE_SHA256"),
        "current_safety_label": _extract_field(exchange_text, "CURRENT_SAFETY_LABEL"),
        "source_text": source,
        "audit_text": audit,
        "preflight_evidence_text": preflight_evidence,
    }
    try:
        payload["source_byte_length"] = int(_extract_field(exchange_text, "SOURCE_BYTE_LENGTH"))
    except (ValueError, TypeError):
        payload["source_byte_length"] = len(source.encode("utf-8"))
    return payload


def build_exchange_preflight(exchange_text: str) -> dict[str, Any]:
    """Verify exact exchange identity and summarize baseline evidence."""
    payload = extract_exchange_payload(exchange_text)
    source = str(payload["source_text"])
    source_bytes = source.encode("utf-8")
    expected_hash = str(payload["source_sha256"])
    actual_hash = _sha256(source_bytes)
    byte_length = len(source_bytes)
    expected_length = int(payload["source_byte_length"])
    preflight_json: dict[str, Any] | None = None
    preflight_text = str(payload["preflight_evidence_text"])
    if preflight_text.strip():
        try:
            decoded = json.loads(preflight_text)
            if isinstance(decoded, dict):
                preflight_json = decoded
        except json.JSONDecodeError:
            preflight_json = None
    return {
        "target_relative_path": payload["target_relative_path"],
        "initial_label": payload["current_safety_label"],
        "source_sha256_expected": expected_hash,
        "source_sha256_actual": actual_hash,
        "source_identity_match": actual_hash == expected_hash,
        "source_byte_length_expected": expected_length,
        "source_byte_length_actual": byte_length,
        "source_byte_length_match": expected_length == byte_length,
        "audit_text_sha256": _sha256(str(payload["audit_text"]).encode("utf-8")),
        "semantic_dynamic_findings": detect_semantic_dynamic_risks(
            source,
            str(payload["target_relative_path"]),
        ),
        "preflight_evidence_valid_json": preflight_json is not None if preflight_text.strip() else False,
        "preflight_evidence": preflight_json,
    }


def _top_level_symbols(tree: ast.Module) -> list[dict[str, Any]]:
    """Capture bounded top-level symbol identity for one candidate module."""
    symbols: list[dict[str, Any]] = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            symbols.append({"kind": "class", "name": node.name, "line": int(node.lineno)})
        elif isinstance(node, ast.AsyncFunctionDef):
            symbols.append({"kind": "async_function", "name": node.name, "line": int(node.lineno)})
        elif isinstance(node, ast.FunctionDef):
            symbols.append({"kind": "function", "name": node.name, "line": int(node.lineno)})
    return symbols


def module_summary(project_root: Path | str, relative_path: str) -> dict[str, Any]:
    """Return deterministic source-family evidence for one candidate module."""
    root = Path(project_root).resolve()
    path = (root / relative_path).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError("CANDIDATE_PATH_OUTSIDE_ACTIVE_PROJECT_ROOT") from exc
    raw = path.read_bytes()
    source = raw.decode("utf-8", errors="strict")
    tree = ast.parse(source, filename=str(path))
    contract = capture_public_contract(root, relative_path)
    return {
        "relative_path": relative_path.replace("\\", "/"),
        "sha256": _sha256(raw),
        "line_count": len(source.splitlines()),
        "ascii_only": all(byte < 128 for byte in raw),
        "utf8_bom": raw.startswith(b"\xef\xbb\xbf"),
        "top_level_symbols": _top_level_symbols(tree),
        "public_contract": contract,
        "semantic_dynamic_findings": detect_semantic_dynamic_risks(source, relative_path),
    }


def run_project_ast_audit(project_root: Path | str, relative_path: str) -> dict[str, Any]:
    """Run the authoritative read-only AST Split Audit for one candidate module."""
    root = Path(project_root).resolve()
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    from kanda_reasoner_app.manage_architecture.large_module_split_audit import (
        run_large_module_split_audit,
    )

    target = (root / relative_path).resolve()
    result = run_large_module_split_audit(root, target, classifier_mode="heuristic")
    classification = result.data["refactor_safety_classification"]
    return {
        "relative_path": relative_path.replace("\\", "/"),
        "label": classification["label"],
        "score": classification["score"],
        "hard_blockers": list(classification["hard_blockers"]),
        "warnings": list(classification["warnings"]),
        "markdown": result.markdown,
    }


def _line_law_status(summary: dict[str, Any]) -> dict[str, Any]:
    """Evaluate the strict project line law for one permanent source module."""
    count = int(summary["line_count"])
    return {
        "relative_path": summary["relative_path"],
        "line_count": count,
        "pass": 100 < count < 500,
    }


def verify_candidate_family(
    project_root: Path | str,
    family_relative_paths: list[str],
    *,
    facade_relative_path: str = "",
    helper_relative_paths: list[str] | None = None,
    audit_output_dir: Path | str | None = None,
) -> dict[str, Any]:
    """Verify one candidate source family without modifying project source."""
    root = Path(project_root).resolve()
    summaries: list[dict[str, Any]] = []
    audits: list[dict[str, Any]] = []
    line_law: list[dict[str, Any]] = []
    for relative_path in family_relative_paths:
        summary = module_summary(root, relative_path)
        summaries.append(summary)
        line_law.append(_line_law_status(summary))
        audit = run_project_ast_audit(root, relative_path)
        audits.append({key: value for key, value in audit.items() if key != "markdown"})
        if audit_output_dir is not None:
            output_dir = Path(audit_output_dir).resolve()
            output_dir.mkdir(parents=True, exist_ok=True)
            safe_name = relative_path.replace("/", "__").replace("\\", "__") + ".md"
            (output_dir / safe_name).write_text(
                str(audit["markdown"]),
                encoding="utf-8",
                newline="\n",
            )
    dependency_direction: dict[str, Any] = {
        "pass": True,
        "violations": [],
        "status": "not_requested",
    }
    if facade_relative_path and helper_relative_paths:
        dependency_direction = check_candidate_dependency_direction(
            root,
            facade_relative_path=facade_relative_path,
            helper_relative_paths=helper_relative_paths,
        )
        dependency_direction["status"] = "checked"
    failures: list[str] = []
    for item in summaries:
        if item["utf8_bom"]:
            failures.append("UTF8_BOM:" + item["relative_path"])
        if item["semantic_dynamic_findings"]:
            failures.append("SEMANTIC_DYNAMIC_RISK:" + item["relative_path"])
    for item in line_law:
        if not item["pass"]:
            failures.append("LINE_LAW_101_499:" + item["relative_path"])
    for item in audits:
        if item["label"] != "SAFE REFACTORING" or item["hard_blockers"]:
            failures.append("FRESH_AST_AUDIT:" + item["relative_path"])
    if not dependency_direction.get("pass", False):
        failures.append("DEPENDENCY_DIRECTION")
    return {
        "schema_version": "1.0",
        "kind": "ast_safe_refactor_family_verification",
        "project_root": str(root),
        "candidate_family": summaries,
        "line_law": line_law,
        "dependency_direction": dependency_direction,
        "fresh_audits": audits,
        "failures": failures,
        "pass": not failures,
    }


def _write_json(path: str, payload: dict[str, Any]) -> None:
    """Write deterministic UTF-8 JSON evidence when explicitly requested."""
    output_path = Path(path).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    """CLI entry point for exchange preflight and candidate-family verification."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--exchange", required=True)
    parser.add_argument("--candidate-root", default="")
    parser.add_argument("--family", action="append", default=[])
    parser.add_argument("--facade", default="")
    parser.add_argument("--helper", action="append", default=[])
    parser.add_argument("--output-json", default="")
    parser.add_argument("--audit-output-dir", default="")
    args = parser.parse_args()

    exchange_text = _read_text(Path(args.exchange).expanduser().resolve())
    preflight = build_exchange_preflight(exchange_text)
    payload: dict[str, Any] = {"exchange_preflight": preflight}
    exit_code = 0
    if not preflight["source_identity_match"] or not preflight["source_byte_length_match"]:
        exit_code = 2
    if args.candidate_root and args.family:
        verification = verify_candidate_family(
            args.candidate_root,
            list(args.family),
            facade_relative_path=args.facade,
            helper_relative_paths=list(args.helper),
            audit_output_dir=args.audit_output_dir or None,
        )
        payload["candidate_verification"] = verification
        if not verification["pass"]:
            exit_code = max(exit_code, 3)
    output = json.dumps(payload, indent=2, sort_keys=True)
    print(output)
    if args.output_json:
        _write_json(args.output_json, payload)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
