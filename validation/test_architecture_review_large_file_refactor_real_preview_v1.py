# project-path: validation/test_architecture_review_large_file_refactor_real_preview_v1.py
"""Validate real moved-code preview generation for Large File Refactor Workbench."""
from __future__ import annotations

import hashlib
from pathlib import Path
from types import SimpleNamespace
import tempfile

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.cst_real_preview_writer import (
    REAL_PREVIEW_FEATURE_ID,
    build_and_write_real_preview,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (
    FEATURE_ID,
    SCHEMA_VERSION,
    ModuleAnalysisReport,
    PlannerSettings,
    ProposedModule,
    RefactorPlan,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_dependency_readiness import (
    build_workbench_dependency_readiness,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_plan_intake import (
    build_workbench_plan_intake,
)


def main() -> None:
    """Run focused validation checks."""
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "sample_project"
        root.mkdir()
        target = root / "large_target.py"
        target.write_text(_sample_source(), encoding="utf-8")
        source_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        plan = _sample_plan(target, source_hash)
        analysis = _sample_analysis(target, source_hash)
        candidate = SimpleNamespace(path=str(target))
        intake = build_workbench_plan_intake(
            plan=plan,
            analysis=analysis,
            active_project_root=str(root),
            planner_candidates=[candidate],
        )
        _expect(intake.ready_for_real_preview, "intake should be ready")
        readiness = build_workbench_dependency_readiness(intake)
        _expect(readiness.ready_for_real_preview_writer, "dependency readiness should be ready")
        result = build_and_write_real_preview(
            plan=plan,
            intake=intake,
            dependency_readiness=readiness,
            active_project_root=str(root),
        )
        _expect(result.feature_id == REAL_PREVIEW_FEATURE_ID, "unexpected real preview feature id")
        _expect(result.status == "real_preview_written", "real preview should be written")
        _expect(not result.source_mutation_enabled, "source mutation must remain disabled")
        _expect(result.written_files, "preview writer must write files")
        preview_root = Path(result.preview_root)
        facade = preview_root / "large_target.py"
        helper = preview_root / "_large_target_function.py"
        _expect(facade.is_file(), "facade preview missing")
        _expect(helper.is_file(), "helper preview missing")
        facade_text = facade.read_text(encoding="utf-8")
        helper_text = helper.read_text(encoding="utf-8")
        _expect("from ._large_target_function import helper" in facade_text, "facade re-export missing")
        _expect("def helper" in helper_text, "moved helper body missing")
        _expect("return value + 1" in helper_text, "moved helper content missing")
        _expect("def run" in facade_text, "facade retained public function")
        _expect("KANDA PREVIEW ARTIFACT" in helper_text, "preview watermark missing")
        _expect(not str(preview_root).startswith(str(root)), "preview root must not be project source")
        _expect((preview_root / "REAL_PREVIEW_MANIFEST.json").is_file(), "manifest missing")
    print("VALIDATION OK: architecture-review-large-file-refactor-real-preview-v1")
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")


def _sample_source() -> str:
    """Return a small source module with one movable helper."""
    return '''"""Sample target module."""

import os

VALUE = 3


def run(value: int) -> int:
    """Public facade-owned function."""
    return helper(value) + VALUE


# important helper comment
def helper(value: int) -> int:
    return value + 1
'''


def _sample_plan(target: Path, source_hash: str) -> RefactorPlan:
    """Build a minimal valid split plan."""
    settings = PlannerSettings().to_dict()
    modules = [
        ProposedModule(
            schema_version=SCHEMA_VERSION,
            filename="large_target.py",
            role="public_facade",
            symbols=["run"],
            estimated_lines=30,
            exports=["run"],
            status="planned",
        ),
        ProposedModule(
            schema_version=SCHEMA_VERSION,
            filename="_large_target_function.py",
            role="function_helper",
            symbols=["helper"],
            estimated_lines=20,
            status="planned",
            line_limit_justification="Small helper justified by dependency boundary.",
        ),
    ]
    return RefactorPlan(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        target_file=str(target),
        source_content_hash=source_hash,
        settings=settings,
        public_api_before=["run"],
        public_api_after_expected=["run"],
        symbols=[],
        atomic_clusters=[],
        proposed_modules=modules,
        import_migration={"status": "preview_only"},
        docstring_proposals=[],
        risks=[],
        validation_blockers=[],
        status="planned",
    )


def _sample_analysis(target: Path, source_hash: str) -> ModuleAnalysisReport:
    """Build minimal analysis evidence with matching source hash."""
    return ModuleAnalysisReport(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        target_file=str(target),
        source_content_hash=source_hash,
        line_count_physical=len(_sample_source().splitlines()),
        module_docstring_present=True,
        module_docstring_preview="Sample target module.",
        all_names=[],
        public_api_symbols=["run"],
        imports=[],
        symbols=[],
        constants=[],
        assignments=[],
        global_statements=[],
        nonlocal_statements=[],
        module_level_calls=[],
        if_main_present=False,
        nested_symbol_count=0,
        missing_docstring_count=0,
    )


def _expect(condition: bool, message: str) -> None:
    """Raise an assertion with a clear message."""
    if not condition:
        raise AssertionError(message)


if __name__ == "__main__":
    main()
