"""Characterization tests for Batch 25 context collector facades."""

from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.reasoner_context_collector.collector_ast import parse_python_file
from kanda_reasoner_app.reasoner_context_collector.collector_canonical_conflicts import (
    build_canonical_conflict_index,
    build_canonical_conflict_summary,
    build_legacy_shadow_hotspots,
)
from kanda_reasoner_app.reasoner_context_collector.collector_implementation_chronology import (
    build_implementation_chronology_index,
    build_implementation_chronology_summary,
    build_migration_transition_hotspots,
)
from kanda_reasoner_app.reasoner_context_collector.collector_responsibility_overlap import (
    build_overlap_hotspots,
    build_responsibility_overlap_index,
    build_responsibility_overlap_summary,
)


def _sample_inputs() -> tuple[
    list[dict[str, object]],
    dict[str, dict[str, object]],
    dict[str, dict[str, object]],
    dict[str, dict[str, object]],
    dict[str, dict[str, object]],
]:
    files_payload: list[dict[str, object]] = [
        {
            "path": "app/core/service.py",
            "subsystem_bucket": "core",
            "entry_markers": ["main"],
            "module_responsibility_summary": {
                "primary_responsibilities": ["load user profile"],
                "keywords": ["profile loader"],
            },
            "semantic_roles": ["service"],
            "symbols": [{"name": "load_profile"}],
            "calls": [{"call_name": "load_profile"}],
        },
        {
            "path": "legacy/service.py",
            "subsystem_bucket": "core",
            "module_responsibility_summary": {
                "primary_responsibilities": ["load user profile"],
                "keywords": ["profile loader"],
            },
            "semantic_roles": ["service"],
            "symbols": [{"name": "load_profile"}],
            "calls": [{"call_name": "load_profile"}],
        },
        {
            "path": "app/ui/window.py",
            "subsystem_bucket": "ui",
            "module_responsibility_summary": {
                "primary_responsibilities": ["render main window"],
            },
            "semantic_roles": ["ui"],
            "symbols": [{"name": "MainWindow"}],
            "calls": [{"call_name": "show"}],
        },
    ]
    boundary_index = {
        "app/core/service.py": {"boundary_role": "service"},
        "legacy/service.py": {"boundary_role": "service"},
        "app/ui/window.py": {"boundary_role": "controller"},
    }
    priority_index = {
        "app/core/service.py": {"priority_score": 4, "priority_rank": 1},
        "legacy/service.py": {"priority_score": 1, "priority_rank": 99},
    }
    centrality_index = {
        "app/core/service.py": {"centrality_score": 2},
        "legacy/service.py": {"centrality_score": 1},
    }
    git_index = {
        "app/core/service.py": {"commit_count": 5},
        "legacy/service.py": {"commit_count": 1},
    }
    return files_payload, boundary_index, priority_index, centrality_index, git_index


def test_context_collector_public_facades_keep_expected_outputs() -> None:
    """Exercise Batch 25 collectors through public facade imports only."""
    files_payload, boundary_index, priority_index, centrality_index, git_index = _sample_inputs()

    canonical_index = build_canonical_conflict_index(
        files_payload,
        boundary_index,
        priority_index,
        centrality_index,
        git_index,
    )
    canonical_summary = build_canonical_conflict_summary(canonical_index)
    legacy_hotspots = build_legacy_shadow_hotspots(canonical_index)

    assert canonical_summary["file_count"] == 2
    assert canonical_summary["legacy_candidate_count"] == 1
    assert canonical_index["legacy/service.py"]["conflict_status"] == "legacy_shadow"
    assert legacy_hotspots[0]["file"] == "legacy/service.py"

    overlap_index = build_responsibility_overlap_index(
        files_payload,
        boundary_index,
        canonical_index,
    )
    overlap_summary = build_responsibility_overlap_summary(overlap_index)
    assert overlap_summary["file_count"] == 3
    assert build_overlap_hotspots(overlap_index) == []

    chronology_index = build_implementation_chronology_index(
        files_payload,
        boundary_index,
        canonical_index,
        overlap_index,
        {},
        git_index,
        priority_index,
        centrality_index,
    )
    chronology_summary = build_implementation_chronology_summary(chronology_index)
    migration_hotspots = build_migration_transition_hotspots(chronology_index)

    assert chronology_summary["file_count"] == 3
    assert chronology_index["app/core/service.py"]["chronology_status"] == "current_canonical"
    assert chronology_index["legacy/service.py"]["chronology_status"] == "legacy_shadow"
    assert migration_hotspots[0]["file"] == "legacy/service.py"


def test_parse_python_file_public_facade_keeps_core_shape(tmp_path: Path) -> None:
    """Exercise collector_ast through the public parse_python_file facade."""
    sample_file = tmp_path / "sample.py"
    sample_file.write_text(
        '"""Module doc."""\n'
        "import os\n\n"
        "class A:\n"
        '    """Class doc."""\n'
        "    def run(self):\n"
        "        self.button.clicked.connect(self.handle)\n\n"
        "def helper(x):\n"
        "    return x + 1\n",
        encoding="utf-8",
    )

    payload, error = parse_python_file(sample_file)

    assert error is None
    assert payload is not None
    assert payload["imports"] == ["os"]
    assert [item["name"] for item in payload["classes"]] == ["A"]
    assert [item["name"] for item in payload["functions"]] == ["helper"]
