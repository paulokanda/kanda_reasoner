"""PA027 tests for inactive reference-folder policy."""

from __future__ import annotations

import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_exclusion_policy import (
    filter_reasoner_path_strings,
    should_exclude_reasoner_project_path,
)
from kanda_reasoner_app.reasoner_symbol_atlas.evidence_freshness import (
    ProjectSymbolAtlasEvidenceFreshnessOptions,
    check_reasoner_symbol_atlas_evidence_freshness,
)
from kanda_reasoner_app.reasoner_symbol_atlas.evidence_migration import (
    plan_project_analysis_evidence_migration,
)
from kanda_reasoner_app.reasoner_symbol_atlas.evidence_paths import (
    get_reasoner_symbol_atlas_reference_evidence_dirs,
    resolve_project_analysis_evidence_paths,
)
from kanda_reasoner_app.reasoner_symbol_atlas.output_policy import (
    is_active_atlas_path,
    sanitize_atlas_markdown_text,
)
from kanda_reasoner_app.reasoner_symbol_atlas.reference_folder_policy import (
    PROJECT_SYMBOL_ATLAS_INACTIVE_REFERENCE_FOLDERS,
    is_reasoner_symbol_atlas_reference_path,
)


def test_pa027_project_exclusion_policy_excludes_dot_reference_folder() -> None:
    """The project-level exclusion policy must exclude both reference names."""
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        active = root / 'ask_' 'ai_project_reasoner' / "active.py"
        old_ref = root / "_project_reference" / "memo.py"
        dot_ref = root / ".project_reference" / "memo.py"
        for path in (active, old_ref, dot_ref):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("print('x')\n", encoding="utf-8")

        assert should_exclude_reasoner_project_path(old_ref, root)
        assert should_exclude_reasoner_project_path(dot_ref, root)
        assert not should_exclude_reasoner_project_path(active, root)

        filtered = filter_reasoner_path_strings(
            [
                'ask_' 'ai_project_reasoner' '/active.py',
                "_project_reference/memo.py",
                ".project_reference/memo.py",
            ],
            root,
        )
        assert filtered == ['ask_' 'ai_project_reasoner' '/active.py']


def test_pa027_atlas_output_policy_excludes_reference_folders() -> None:
    """Atlas active-scope policy must reject memo/reference paths."""
    assert PROJECT_SYMBOL_ATLAS_INACTIVE_REFERENCE_FOLDERS == (
        "_project_reference",
        ".project_reference",
    )
    assert is_reasoner_symbol_atlas_reference_path("_project_reference/CANNON/a.py")
    assert is_reasoner_symbol_atlas_reference_path(".project_reference/memos/a.py")
    assert not is_reasoner_symbol_atlas_reference_path(
        'ask_' 'ai_project_reasoner' '/reasoner_symbol_atlas/output_policy.py'
    )
    assert not is_active_atlas_path("_project_reference/CANNON/a.py")
    assert not is_active_atlas_path(".project_reference/memos/a.py")
    assert is_active_atlas_path(
        'ask_' 'ai_project_reasoner' '/reasoner_symbol_atlas/output_policy.py'
    )


def test_pa027_sanitizer_removes_dot_reference_recommendations() -> None:
    """Sanitized reports must not recommend either reference folder as active."""
    raw = "\n".join(
        [
            "# Project Symbol Atlas Report",
            "## Decision Details",
            '- target_path=ask_' 'ai_project_reasoner' '/reasoner_symbol_atlas/output_policy.py',
            "- primary_edit_target=.project_reference/memos/old_owner.py",
            "- main_path=_project_reference/CANNON/old_main.py",
            "- helper_path=.project_reference/memos/old_helper.py",
            "- related_file=.project_reference/memos/old_helper.py",
            "- test_to_run=python .project_reference/memos/test_old.py",
            '- related_file=ask_' 'ai_project_reasoner' '/reasoner_symbol_atlas/output_policy.py',
        ]
    )
    rendered = sanitize_atlas_markdown_text(raw)
    assert "_project_reference" not in rendered
    assert ".project_reference" not in rendered
    assert (
        'active_target_path=ask_' 'ai_project_reasoner' '/reasoner_symbol_atlas/output_policy.py'
        in rendered
    )
    assert 'related_file=ask_' 'ai_project_reasoner' '/reasoner_symbol_atlas/output_policy.py' in rendered


def test_pa027_evidence_paths_report_both_reference_evidence_dirs() -> None:
    """Evidence path resolver must know old and dot reference memo folders."""
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        dot_evidence = root / ".project_reference" / "project_analysis_evidence"
        dot_evidence.mkdir(parents=True)
        paths = resolve_project_analysis_evidence_paths(root)
        reference_dirs = get_reasoner_symbol_atlas_reference_evidence_dirs(root)

        assert paths.legacy_exists is True
        assert paths.migration_needed is True
        assert Path(paths.legacy_evidence_dir) == dot_evidence.resolve(strict=False)
        assert len(reference_dirs) == 2
        joined = "\n".join(paths.reference_evidence_dirs + paths.notes)
        assert "_project_reference" in joined
        assert ".project_reference" in joined


def test_pa027_migration_can_plan_from_dot_reference_evidence() -> None:
    """Migration helper should support the dot reference folder as a source."""
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        source = root / ".project_reference" / "project_analysis_evidence" / "x.json"
        source.parent.mkdir(parents=True)
        source.write_text('{"ok": true}\n', encoding="utf-8")

        report = plan_project_analysis_evidence_migration(root)
        assert report.status == "migration_available"
        assert report.planned_copy_count == 1
        assert ".project_reference" in report.legacy_evidence_root
        assert report.files[0].relative_path == "x.json"


def test_pa027_freshness_ignores_reference_folder_files() -> None:
    """Freshness live scan must not count memo/reference folder files as new code."""
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        active = root / 'ask_' 'ai_project_reasoner' / "active.py"
        memo = root / ".project_reference" / "memos" / "ignored.py"
        json_path = root / "project_analysis_evidence" / "json_complete" / "project__complete.json"
        for path in (active, memo, json_path):
            path.parent.mkdir(parents=True, exist_ok=True)
        active.write_text("print('active')\n", encoding="utf-8")
        memo.write_text("print('memo')\n", encoding="utf-8")
        payload = {
            "project_root": str(root.resolve(strict=False)),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_file_index": {
                'ask_' 'ai_project_reasoner' '/active.py': {
                    "path": 'ask_' 'ai_project_reasoner' '/active.py'
                }
            },
        }
        json_path.write_text(json.dumps(payload), encoding="utf-8")

        summary = check_reasoner_symbol_atlas_evidence_freshness(
            ProjectSymbolAtlasEvidenceFreshnessOptions(
                project_root=str(root),
                json_path=str(json_path),
            )
        )
        assert ".project_reference/memos/ignored.py" not in summary.new_source_files
        assert 'ask_' 'ai_project_reasoner' '/active.py' not in summary.new_source_files


def main() -> int:
    test_pa027_project_exclusion_policy_excludes_dot_reference_folder()
    test_pa027_atlas_output_policy_excludes_reference_folders()
    test_pa027_sanitizer_removes_dot_reference_recommendations()
    test_pa027_evidence_paths_report_both_reference_evidence_dirs()
    test_pa027_migration_can_plan_from_dot_reference_evidence()
    test_pa027_freshness_ignores_reference_folder_files()
    print("PA027 reference-folder policy tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
