# project-path: tests/test_architecture_warning_cleanup_batch26_symbol_atlas_large_module_refactor.py
"""Characterization tests for Batch 26 symbol-atlas large-module refactor."""

from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import types

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_PROJECT_ROOT))
_PACKAGE_ROOT = _PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_symbol_atlas"
_PACKAGE = types.ModuleType("kanda_reasoner_app.reasoner_symbol_atlas")
_PACKAGE.__path__ = [str(_PACKAGE_ROOT)]
sys.modules.setdefault("kanda_reasoner_app.reasoner_symbol_atlas", _PACKAGE)

_REFERENCE_POLICY = types.ModuleType(
    "kanda_reasoner_app.reasoner_symbol_atlas.reference_folder_policy"
)
_REFERENCE_POLICY.PROJECT_SYMBOL_ATLAS_INACTIVE_REFERENCE_FOLDERS = (
    ".project_reference",
)

def _iter_reference_evidence_dirs(project_root: Path) -> tuple[Path, ...]:
    return (project_root / ".project_reference" / "project_analysis_evidence",)

def _normalize_policy_path(value: object) -> str:
    return str(value).replace("\\", "/")

def _is_reference_path(value: object) -> bool:
    return ".project_reference" in _normalize_policy_path(value)

_REFERENCE_POLICY.iter_reasoner_symbol_atlas_reference_evidence_dirs = (
    _iter_reference_evidence_dirs
)
_REFERENCE_POLICY.normalize_reasoner_symbol_atlas_policy_path = _normalize_policy_path
_REFERENCE_POLICY.is_reasoner_symbol_atlas_reference_path = _is_reference_path
_REFERENCE_POLICY.build_reasoner_symbol_atlas_reference_path_markers = (
    lambda: (".project_reference",)
)
sys.modules.setdefault(
    "kanda_reasoner_app.reasoner_symbol_atlas.reference_folder_policy",
    _REFERENCE_POLICY,
)

from kanda_reasoner_app.reasoner_symbol_atlas.complete_json_adapter import (
    ProjectSymbolAtlasCompleteJsonOptions,
    build_reasoner_symbol_atlas_complete_json_report,
)
from kanda_reasoner_app.reasoner_symbol_atlas.existing_code_finder import (
    ProjectSymbolAtlasExistingCodeFinderOptions,
    find_reasoner_symbol_atlas_existing_code,
)
from kanda_reasoner_app.reasoner_symbol_atlas.import_analyzer import (
    ProjectSymbolAtlasImportAnalysisOptions,
    build_reasoner_symbol_atlas_import_report,
    collect_reasoner_symbol_atlas_imports,
)
from kanda_reasoner_app.reasoner_symbol_atlas.related_file_finder import (
    ProjectSymbolAtlasRelatedFileOptions,
    find_reasoner_symbol_atlas_related_files,
)


def test_batch26_symbol_atlas_public_facades_import_and_run() -> None:
    """Public facades remain callable after helper extraction."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        source_dir = project_root / "kanda_reasoner_app" / "reasoner_symbol_atlas"
        source_dir.mkdir(parents=True)
        (source_dir / "__init__.py").write_text("", encoding="utf-8")
        (source_dir / "import_analyzer.py").write_text(
            """from .schemas import ProjectSymbol\n\n__all__ = [\"ProjectSymbol\"]\n""",
            encoding="utf-8",
        )
        tests_dir = project_root / "tests"
        tests_dir.mkdir()
        (tests_dir / "test_import_analyzer.py").write_text(
            "def test_placeholder():\n    assert True\n",
            encoding="utf-8",
        )

        import_report = build_reasoner_symbol_atlas_import_report(
            project_root,
            options=ProjectSymbolAtlasImportAnalysisOptions(
                include_tests=False,
                include_workbench=False,
            ),
        )
        assert import_report.report_type == "reasoner_symbol_atlas"
        assert "import/facade analysis completed" in import_report.summary

        imports = collect_reasoner_symbol_atlas_imports(
            project_root,
            options=ProjectSymbolAtlasImportAnalysisOptions(
                include_tests=False,
                include_workbench=False,
            ),
        )
        assert isinstance(imports, tuple)

        complete_json_report = build_reasoner_symbol_atlas_complete_json_report(
            ProjectSymbolAtlasCompleteJsonOptions(project_root=str(project_root), json_path="")
        )
        assert complete_json_report.report_type == "reasoner_symbol_atlas"

        existing = find_reasoner_symbol_atlas_existing_code(
            ProjectSymbolAtlasExistingCodeFinderOptions(
                project_root=str(project_root),
                query_text="ProjectSymbol",
                include_tests=False,
                include_workbench=False,
                max_matches=10,
            )
        )
        assert existing.query_text == "ProjectSymbol"
        assert existing.status

        related = find_reasoner_symbol_atlas_related_files(
            ProjectSymbolAtlasRelatedFileOptions(
                project_root=str(project_root),
                target_path="kanda_reasoner_app/reasoner_symbol_atlas/import_analyzer.py",
                symbol_name="ProjectSymbol",
                include_tests=False,
                include_workbench=False,
                include_evidence_files=False,
            )
        )
        assert related.target_path.endswith("import_analyzer.py")
        assert related.status


if __name__ == "__main__":
    test_batch26_symbol_atlas_public_facades_import_and_run()
