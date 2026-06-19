"""Focused tests for PA007A Project Analysis Evidence path normalizer."""

from __future__ import annotations

import sys
from pathlib import Path
import tempfile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_symbol_atlas.evidence_paths import (  # noqa: E402
    PROJECT_SYMBOL_ATLAS_STATUS_CANONICAL_READY,
    PROJECT_SYMBOL_ATLAS_STATUS_DUAL_EVIDENCE,
    PROJECT_SYMBOL_ATLAS_STATUS_MIGRATION_AVAILABLE,
    PROJECT_SYMBOL_ATLAS_STATUS_MISSING_EVIDENCE,
    build_project_analysis_evidence_path_summary,
    get_reasoner_symbol_atlas_canonical_evidence_dir,
    get_reasoner_symbol_atlas_legacy_evidence_dir,
    resolve_project_analysis_evidence_paths,
)


def _make_temp_root() -> Path:
    root = Path(tempfile.mkdtemp()) / "sample_project"
    root.mkdir(parents=True)
    return root


def test_pa007a_missing_evidence_uses_dynamic_project_root() -> None:
    root = _make_temp_root()
    paths = resolve_project_analysis_evidence_paths(root)

    assert paths.status == PROJECT_SYMBOL_ATLAS_STATUS_MISSING_EVIDENCE
    assert paths.canonical_exists is False
    assert paths.legacy_exists is False
    assert paths.migration_needed is False
    assert Path(paths.canonical_evidence_dir) == root / "project_analysis_evidence"
    assert Path(paths.legacy_evidence_dir) == (
        root / "_project_reference" / "project_analysis_evidence"
    )


def test_pa007a_legacy_only_reports_migration_available() -> None:
    root = _make_temp_root()
    legacy = root / "_project_reference" / "project_analysis_evidence"
    legacy.mkdir(parents=True)

    paths = resolve_project_analysis_evidence_paths(root)

    assert paths.status == PROJECT_SYMBOL_ATLAS_STATUS_MIGRATION_AVAILABLE
    assert paths.canonical_exists is False
    assert paths.legacy_exists is True
    assert paths.migration_needed is True


def test_pa007a_canonical_only_is_ready() -> None:
    root = _make_temp_root()
    canonical = root / "project_analysis_evidence"
    canonical.mkdir(parents=True)

    paths = resolve_project_analysis_evidence_paths(root)

    assert paths.status == PROJECT_SYMBOL_ATLAS_STATUS_CANONICAL_READY
    assert paths.canonical_exists is True
    assert paths.legacy_exists is False
    assert paths.migration_needed is False


def test_pa007a_dual_evidence_prefers_canonical() -> None:
    root = _make_temp_root()
    (root / "project_analysis_evidence").mkdir(parents=True)
    (root / "_project_reference" / "project_analysis_evidence").mkdir(parents=True)

    paths = resolve_project_analysis_evidence_paths(root)

    assert paths.status == PROJECT_SYMBOL_ATLAS_STATUS_DUAL_EVIDENCE
    assert paths.canonical_exists is True
    assert paths.legacy_exists is True
    assert paths.migration_needed is False
    assert "Prefer canonical evidence" in " ".join(paths.notes)


def test_pa007a_helpers_and_summary_are_stable() -> None:
    root = _make_temp_root()

    canonical = get_reasoner_symbol_atlas_canonical_evidence_dir(root)
    legacy = get_reasoner_symbol_atlas_legacy_evidence_dir(root)
    summary = build_project_analysis_evidence_path_summary(root)

    assert canonical == root / "project_analysis_evidence"
    assert legacy == root / "_project_reference" / "project_analysis_evidence"
    assert "Project Analysis Evidence Paths" in summary
    assert str(canonical) in summary
    assert str(legacy) in summary


def test_pa007a_module_has_no_project_specific_root_literal() -> None:
    module_path = (
        PROJECT_ROOT
        / 'ask_' 'ai_project_reasoner'
        / "reasoner_symbol_atlas"
        / "evidence_paths.py"
    )
    source = module_path.read_text(encoding="utf-8")

    assert "E:\\developer_tools" not in source
    assert "<PROJECT_ROOT>" not in source


if __name__ == "__main__":
    test_pa007a_missing_evidence_uses_dynamic_project_root()
    test_pa007a_legacy_only_reports_migration_available()
    test_pa007a_canonical_only_is_ready()
    test_pa007a_dual_evidence_prefers_canonical()
    test_pa007a_helpers_and_summary_are_stable()
    test_pa007a_module_has_no_project_specific_root_literal()
    print("PA007A Project Analysis Evidence path normalizer tests passed.")
