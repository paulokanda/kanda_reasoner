"""Validate completion guard behavior for the file retrieval refactor."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def _ensure_project_root_on_path() -> None:
    """Add the project root to sys.path only for direct script execution."""
    root_text = str(ROOT)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)

BASE = ROOT / "kanda_reasoner_app" / "reasoner_engine" / "reasoner_retriever_help"

EXPECTED_OWNERSHIP = {
    "file_retrieval.py": {
        "max": 80,
        "needles": [
            "file_retrieval_core import",
            "retrieve_files,",
            "file_retrieval_evidence import",
            "build_compact_file_evidence,",
            "__all__ = [\"retrieve_files\", \"build_compact_file_evidence\"]",
        ],
        "forbidden": ["def retrieve_files(", "def build_compact_file_evidence("],
    },
    "file_retrieval_context.py": {
        "max": 500,
        "needles": ["def build_query_context(", "def candidate_file_paths(", "def reindex_file_evidence("],
    },
    "file_retrieval_core.py": {
        "max": 500,
        "needles": [
            "def retrieve_files(",
            "candidate_file_paths(retriever, query)",
            "apply_exact_and_call_scoring",
            "apply_semantic_scoring",
            "apply_advanced_and_runtime_scoring",
            "reindex_file_evidence(scored, limit)",
            "runtime_signal_connections are collector-internal",
        ],
    },
    "file_retrieval_evidence.py": {
        "max": 500,
        "needles": ["def build_compact_file_evidence(", "Functions:", "Classes:", "Advanced context:", "Runtime context:", "Qt signals:"],
    },
    "file_retrieval_scoring_exact.py": {
        "max": 500,
        "needles": ["def apply_exact_and_call_scoring(", "where-is", "which-calls", "call-site"],
    },
    "file_retrieval_scoring_semantic.py": {
        "max": 500,
        "needles": ["def apply_semantic_scoring(", "explain-chain", "topomap", "reset-cleanup"],
    },
    "file_retrieval_scoring_explain.py": {
        "max": 500,
        "needles": ["def apply_startup_scoring(", "def apply_explanation_heavy_scoring("],
    },
    "file_retrieval_scoring_runtime.py": {
        "max": 500,
        "needles": ["def apply_advanced_and_runtime_scoring(", "qt-signal-map-boost", "uncertainty-hotspot-boost"],
    },
}


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _line_count(path: Path) -> int:
    return len(_text(path).splitlines())


def _assert_v72_completion_shape() -> None:
    missing = [name for name in EXPECTED_OWNERSHIP if not (BASE / name).exists()]
    if missing:
        raise AssertionError(f"Missing file retrieval refactor files: {missing}")

    for name, spec in EXPECTED_OWNERSHIP.items():
        path = BASE / name
        count = _line_count(path)
        if count > int(spec["max"]):
            raise AssertionError(f"{name} exceeds v7.2 maximum {spec['max']}: {count}")
        body = _text(path)
        for needle in spec.get("needles", []):
            if needle not in body:
                raise AssertionError(f"{name} missing ownership marker: {needle}")
        for needle in spec.get("forbidden", []):
            if needle in body:
                raise AssertionError(f"{name} is no longer a thin facade; found: {needle}")

    substantive = [name for name in EXPECTED_OWNERSHIP if name != "file_retrieval.py"]
    too_small = [name for name in substantive if _line_count(BASE / name) < 80]
    if too_small:
        raise AssertionError(f"Unexpected tiny substantive helper modules: {too_small}")


def _assert_public_api_and_side_effect_boundaries() -> None:
    mod = importlib.import_module(
        "kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval"
    )
    if not callable(getattr(mod, "retrieve_files", None)):
        raise AssertionError("Public retrieve_files API missing from facade")
    if not callable(getattr(mod, "build_compact_file_evidence", None)):
        raise AssertionError("Public build_compact_file_evidence API missing from facade")
    if getattr(mod, "__all__", None) != ["retrieve_files", "build_compact_file_evidence"]:
        raise AssertionError("Facade __all__ changed unexpectedly")

    core = _text(BASE / "file_retrieval_core.py")
    if "runtime_signal_connections" in core and "candidate_paths" in core:
        # The string may appear in the explicit guard comment, which is desired.
        if "runtime_signal_connections are collector-internal" not in core:
            raise AssertionError("runtime_signal_connections may be leaking into candidate path logic")

    all_source = "\n".join(_text(BASE / name) for name in EXPECTED_OWNERSHIP)
    forbidden_mutations = [
        "project_freeze_ledger",
        "frozen_features_memory",
        "freeze_hint_intake",
        "write_text(",
        "open(",
        "mkdir(",
        "unlink(",
        "rmdir(",
        "shutil.",
    ]
    offenders = [needle for needle in forbidden_mutations if needle in all_source]
    if offenders:
        raise AssertionError(f"File retrieval must remain side-effect-free; found {offenders}")


def main() -> None:
    _ensure_project_root_on_path()
    _assert_v72_completion_shape()
    _assert_public_api_and_side_effect_boundaries()
    print("VALIDATION OK: file-retrieval-refactor-completion-guard-v1")


if __name__ == "__main__":
    main()
