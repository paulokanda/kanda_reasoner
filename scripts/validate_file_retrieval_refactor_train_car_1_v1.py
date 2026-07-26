"""Validate train-car 1 behavior for the file retrieval refactor."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]

def _ensure_project_root_on_path() -> None:
    """Add the project root to sys.path only for direct script execution."""
    root_text = str(ROOT)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)

BASE = ROOT / "kanda_reasoner_app" / "reasoner_engine" / "reasoner_retriever_help"

EXPECTED_FILES = {
    "file_retrieval.py": "thin facade",
    "file_retrieval_context.py": "query and candidate context",
    "file_retrieval_core.py": "retrieval orchestration",
    "file_retrieval_evidence.py": "compact evidence rendering",
    "file_retrieval_scoring_exact.py": "exact/call-site scoring",
    "file_retrieval_scoring_semantic.py": "semantic/topical scoring",
    "file_retrieval_scoring_explain.py": "startup/explanation scoring",
    "file_retrieval_scoring_runtime.py": "runtime/uncertainty scoring",
}


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def _assert_structure() -> None:
    missing = [name for name in EXPECTED_FILES if not (BASE / name).exists()]
    if missing:
        raise AssertionError(f"Missing refactor files: {missing}")

    for name in EXPECTED_FILES:
        count = _line_count(BASE / name)
        if count > 500:
            raise AssertionError(f"{name} exceeds v7.2 maximum: {count}")

    facade = (BASE / "file_retrieval.py").read_text(encoding="utf-8")
    required_facade_text = [
        "from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_core import",
        "from kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval_evidence import",
        "__all__ = [\"retrieve_files\", \"build_compact_file_evidence\"]",
    ]
    for needle in required_facade_text:
        if needle not in facade:
            raise AssertionError(f"Facade missing expected text: {needle}")

    if "def retrieve_files(" in facade or "def build_compact_file_evidence(" in facade:
        raise AssertionError("file_retrieval.py must remain a thin import facade")

    context = (BASE / "file_retrieval_context.py").read_text(encoding="utf-8")
    if "runtime_signal_connections are collector-internal" in context:
        raise AssertionError("collector-internal runtime signal warning belongs in core loop")

    core = (BASE / "file_retrieval_core.py").read_text(encoding="utf-8")
    for needle in [
        "candidate_file_paths(retriever, query)",
        "apply_exact_and_call_scoring",
        "apply_semantic_scoring",
        "apply_advanced_and_runtime_scoring",
        "retriever._build_compact_file_evidence(path, reasons)",
        "reindex_file_evidence(scored, limit)",
    ]:
        if needle not in core:
            raise AssertionError(f"Core missing expected retrieval step: {needle}")


def _fake_retriever(build_compact):
    class FakeRetriever:
        def __init__(self):
            self.idx = SimpleNamespace(
                project_summary={"entry_files": ["shell/kanda_main.py"]},
                packaging_metadata={"packaging_files_found": ["pyproject.toml"]},
                documentation_intent={"documentation_files_found": ["docs/help.md"]},
                semantic_roles={"shell/kanda_main.py": {"roles": ["entry"]}},
                files_by_path={
                    "shell/kanda_main.py": {
                        "module_name": "shell.kanda_main",
                        "docstring": "Build startup and show main window",
                        "strings": ["QApplication build_and_show retriever.v.main_window.showmaximized"],
                        "comments": ["startup launcher"],
                        "entry_markers": ["def main"],
                        "ui_keyword_hits": ["show addtab"],
                        "semantic_hints": ["startup"],
                        "functions": [
                            {
                                "qualname": "main",
                                "name": "main",
                                "lineno": 10,
                                "calls": [{"call_name": "build_and_show"}],
                            }
                        ],
                        "classes": [],
                        "imports": [],
                        "full_source": "def main(): build_and_show()\nretriever.v.main_window.show()\n",
                    },
                    "runtime_collector/runtime_runner.py": {
                        "module_name": "runtime_collector.runtime_runner",
                        "docstring": "runtime probe signal connections on_apply_clicked",
                        "strings": ["runtime_runner_probe_apply_button probe apply button clicked signal_connection"],
                        "comments": ["runtime"],
                        "functions": [
                            {
                                "qualname": "on_apply_clicked",
                                "name": "on_apply_clicked",
                                "lineno": 5,
                                "calls": [{"call_name": "emit"}],
                            }
                        ],
                        "classes": [],
                        "imports": [],
                        "full_source": "def on_apply_clicked(): emit()\n",
                    },
                },
                runtime_events_by_file={"runtime_collector/runtime_runner.py": [{"event": "x"}]},
                widgets_by_file={},
                ui_actions_by_file={},
                boundaries_by_file={},
                hotspots_by_file={"runtime_collector/runtime_runner.py": [1]},
                import_graph_out={},
                call_graph_out={"runtime_collector/runtime_runner.py": ["emit"]},
                subsystems=[{"name": "runtime", "files": ["runtime_collector/runtime_runner.py"]}],
                execution_chains={"startup_chain": [{"file": "shell/kanda_main.py"}]},
                qt_signal_map=[
                    {
                        "source_file": "runtime_collector/runtime_runner.py",
                        "signal_name": "clicked",
                        "target": "on_apply_clicked",
                        "source_symbol": "runtime_runner_probe_apply_button",
                    }
                ],
            )

        def _build_compact_file_evidence(self, path, reasons):
            return build_compact(self, path, reasons)

        def _question_has_profile_alias(self, q, alias):
            return any(term in q for term in self._profile_alias_terms(alias))

        def _text_has_profile_alias(self, text, alias):
            return any(term in text for term in self._profile_alias_terms(alias))

        def _profile_alias_terms(self, alias):
            return {
                "top_navigation": ["navbar"],
                "navbar_builder_terms": ["navbar"],
                "notebook_builder_terms": ["notebook", "addtab"],
                "reset_cleanup": ["reset", "cleanup", "snapshot"],
                "builder_callsite_markers": ["build_and_show", "addtab"],
                "timeline_symbol_terms": ["timeline"],
                "topomap_symbol_terms": ["topomap", "amplitude_map"],
                "reset_cleanup_symbol_terms": ["reset", "cleanup", "disconnect"],
                "topomap": ["topomap"],
            }.get(alias, [])

        def _profile_owner_paths(self, alias):
            return {
                "timeline_owner_paths": ["timeline"],
                "topomap_owner_paths": ["topomap"],
                "reset_cleanup_owner_paths": ["core/snapshot"],
            }.get(alias, [])

        def _collect_file_context_blobs(self, path):
            if path == "runtime_collector/runtime_runner.py":
                return {
                    "widgets": "",
                    "ui_actions": "",
                    "boundaries": "",
                    "runtime": "runtime_runner_probe_apply_button probe apply button clicked signal_connection on_apply_clicked",
                    "hotspots": "warning try exception",
                }
            return {
                "widgets": "",
                "ui_actions": "addtab",
                "boundaries": "boundary",
                "runtime": "",
                "hotspots": "",
            }

        def _get_runtime_anchor_summary(self, path, limit=12):
            if path == "runtime_collector/runtime_runner.py":
                return ["runtime_runner_probe_apply_button", "on_apply_clicked"], [
                    "probe apply button clicked"
                ]
            return [], []

        def _score_advanced_file_context(self, q, path, tokens, reasons):
            if "advanced" in q and path == "shell/kanda_main.py":
                reasons.append("advanced-context-test")
                return 77
            return 0

        def _score_runtime_signal_matches(self, q, reasons):
            if "signal" in q:
                reasons.append("runtime-signal-test")
                return 55, {"runtime_collector/runtime_runner.py"}
            return 0, set()

    return FakeRetriever()


def _assert_behavior() -> None:
    mod = importlib.import_module(
        "kanda_reasoner_app.reasoner_engine.reasoner_retriever_help.file_retrieval"
    )
    retriever = _fake_retriever(mod.build_compact_file_evidence)
    results = mod.retrieve_files(
        retriever,
        "startup chain runtime probe button signal-slot connections on_apply_clicked advanced",
        10,
    )
    if not results:
        raise AssertionError("retrieve_files returned no evidence for synthetic index")

    by_path = {item.path: item for item in results}
    if "shell/kanda_main.py" not in by_path:
        raise AssertionError("startup file missing from retrieval result")
    if "runtime_collector/runtime_runner.py" not in by_path:
        raise AssertionError("runtime file missing from retrieval result")

    runtime_reason = by_path["runtime_collector/runtime_runner.py"].reason
    for needle in [
        "runtime-heavy-question-runtime-boost",
        "runtime-signal-path-boost",
        "qt-signal-map-boost",
    ]:
        if needle not in runtime_reason:
            raise AssertionError(f"runtime retrieval reason missing {needle}: {runtime_reason}")

    detail = by_path["runtime_collector/runtime_runner.py"].detail
    for needle in ["Path: runtime_collector/runtime_runner.py", "Runtime context:", "Qt signals:"]:
        if needle not in detail:
            raise AssertionError(f"compact evidence missing {needle}")

    if [item.evidence_id for item in results] != [f"F{i:02d}" for i in range(1, len(results) + 1)]:
        raise AssertionError("file evidence IDs are not reindexed as F01..Fn")


def main() -> None:
    _ensure_project_root_on_path()
    _assert_structure()
    _assert_behavior()
    print("VALIDATION OK: file-retrieval-refactor-train-car-1-v1")


if __name__ == "__main__":
    main()
