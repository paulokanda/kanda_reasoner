# project-path: scripts/repair_architecture_warning_cleanup_batch19_static_coverage_exports_v1.py
"""Repair Batch 19 static coverage/export metadata and line-count warnings.

This script is intentionally behavior-neutral. It does not move logic and it
must not execute target module source. It uses AST parsing, tokenize string-line
protection, py_compile, and AST equivalence checks for whitespace-only compacts.
"""

from __future__ import annotations

import ast
import py_compile
import re
import sys
import tokenize
from pathlib import Path

FEATURE_ID = "architecture-warning-cleanup-batch19-static-coverage-exports-v1"
MAX_LINE_THRESHOLD = 500

RETRIEVER_HELP_INIT = Path(
    "kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/__init__.py"
)

LINE_COUNT_TARGETS = (
    "kanda_reasoner_app/routing_signal_scorer/generator_candidate_human_decision_recording_finalization_design.py",
    "kanda_reasoner_app/routing_signal_scorer/generator_candidate_human_decision_recording_implementation_design.py",
    "kanda_reasoner_app/routing_signal_scorer/generator_candidate_human_decision_recording_patch_boundary_design.py",
    "kanda_reasoner_app/routing_signal_scorer/generator_candidate_human_decision_recording_patch_design.py",
    "kanda_reasoner_app/routing_signal_scorer/generator_candidate_patch_file_set_design.py",
    "kanda_reasoner_app/routing_signal_scorer/generator_candidate_patch_preflight_design.py",
    "kanda_reasoner_app/routing_signal_scorer/generator_candidate_proposal_review_design.py",
    "kanda_reasoner_app/routing_signal_scorer/adviser_offline/gold_expansion/gold_set_expansion_plan.py",
    "kanda_reasoner_app/reasoner_context_collector/collector_widget_layout_index.py",
    "kanda_reasoner_app/reasoner_context_collector/collector_state_lifecycle.py",
    "kanda_reasoner_app/reasoner_engine/reasoner_retriever_help/snippet_retrieval.py",
)


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def _write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def _literal_dunder_all(path: Path) -> list[str]:
    tree = ast.parse(_read_text(path), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    value = ast.literal_eval(node.value)
                    if isinstance(value, (list, tuple)) and all(isinstance(item, str) for item in value):
                        return list(value)
                    raise ValueError(f"{path}: __all__ is not a literal list/tuple of strings")
    return []


def _sync_retriever_help_exports(project_root: Path) -> bool:
    path = project_root / RETRIEVER_HELP_INIT
    if not path.is_file():
        return False

    exported = _literal_dunder_all(path)
    if not exported:
        return False

    text = _read_text(path)
    desired = "EXPORTS: " + ", ".join(exported)
    lines = text.splitlines(keepends=True)
    changed = False
    in_raw_docstring = False

    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith(('r"""', '"""')):
            in_raw_docstring = not in_raw_docstring
            continue
        if in_raw_docstring and stripped.startswith("EXPORTS:"):
            newline = "\n" if line.endswith("\n") else ""
            replacement = desired + newline
            if line != replacement:
                lines[index] = replacement
                changed = True
            break

    if not changed:
        return False

    new_text = "".join(lines)
    ast.parse(new_text, filename=str(path))
    _write_text(path, new_text)
    py_compile.compile(str(path), doraise=True)
    return True


def _string_literal_lines(path: Path) -> set[int]:
    protected: set[int] = set()
    with path.open("rb") as handle:
        for token in tokenize.tokenize(handle.readline):
            if token.type == tokenize.STRING:
                start_line = token.start[0]
                end_line = token.end[0]
                protected.update(range(start_line, end_line + 1))
    return protected


def _ast_signature(text: str, path: Path) -> str:
    return ast.dump(ast.parse(text, filename=str(path)), include_attributes=False)


def _compact_blank_lines_to_threshold(path: Path) -> bool:
    if not path.is_file():
        return False

    original = _read_text(path)
    original_lines = original.splitlines(keepends=True)
    if len(original_lines) <= MAX_LINE_THRESHOLD:
        return False

    before_signature = _ast_signature(original, path)
    protected_lines = _string_literal_lines(path)
    target_remove_count = len(original_lines) - MAX_LINE_THRESHOLD
    removable_indexes = [
        index
        for index, line in enumerate(original_lines)
        if not line.strip() and (index + 1) not in protected_lines
    ]

    if len(removable_indexes) < target_remove_count:
        raise RuntimeError(
            f"{path}: only {len(removable_indexes)} safe blank lines available; "
            f"need {target_remove_count} to reach {MAX_LINE_THRESHOLD} lines"
        )

    remove_set = set(removable_indexes[-target_remove_count:])
    new_lines = [line for index, line in enumerate(original_lines) if index not in remove_set]
    new_text = "".join(new_lines)

    after_signature = _ast_signature(new_text, path)
    if after_signature != before_signature:
        raise RuntimeError(f"{path}: AST changed after whitespace-only compaction")
    if len(new_text.splitlines()) > MAX_LINE_THRESHOLD:
        raise RuntimeError(f"{path}: compaction did not reduce line count below threshold")

    _write_text(path, new_text)
    py_compile.compile(str(path), doraise=True)
    return True


def main() -> int:
    project_root = _project_root()
    changed: list[str] = []

    if _sync_retriever_help_exports(project_root):
        changed.append(str(RETRIEVER_HELP_INIT).replace("\\", "/"))

    for relative in LINE_COUNT_TARGETS:
        path = project_root / relative
        if _compact_blank_lines_to_threshold(path):
            changed.append(relative)

    print(f"REPAIR OK: {FEATURE_ID}")
    if changed:
        print("Changed files:")
        for relative in changed:
            print(f" - {relative}")
    else:
        print("No changes needed; target files already satisfy Batch 19 constraints.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
