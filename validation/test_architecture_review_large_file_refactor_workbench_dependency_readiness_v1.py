# project-path: validation/test_architecture_review_large_file_refactor_workbench_dependency_readiness_v1.py
"""Validate Workbench dependency-readiness foundation for real refactor preview."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
import py_compile
import tempfile

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (
    FEATURE_ID,
    SCHEMA_VERSION,
    ModuleAnalysisReport,
    PlannerSettings,
    RefactorPlan,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.source_encoding_profile import (
    build_source_encoding_profile,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.symbol_dependency_builder import (
    build_symbol_dependency_report,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_dependency_readiness import (
    build_workbench_dependency_readiness,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_plan_intake import (
    build_workbench_plan_intake,
)


@dataclass(frozen=True)
class _Candidate:
    """Small candidate stand-in for Workbench intake validation."""

    path: str


def main() -> None:
    """Run focused readiness validation."""
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp).resolve()
        target = project / "large_module.py"
        target.write_text(_sample_source(), encoding="utf-8", newline="\n")
        source_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        plan = _plan(target, source_hash)
        analysis = _analysis(target, source_hash)
        intake = build_workbench_plan_intake(
            plan=plan,
            analysis=analysis,
            active_project_root=str(project),
            planner_candidates=[_Candidate(path=str(target))],
        )
        if not intake.ready_for_real_preview:
            raise AssertionError(f"intake unexpectedly blocked: {intake.blockers}")
        profile = build_source_encoding_profile(target)
        if profile.encoding.lower().replace("-", "_") not in {"utf_8", "utf_8_sig"}:
            raise AssertionError(f"unexpected encoding: {profile.encoding}")
        if profile.newline_style != "lf":
            raise AssertionError(f"unexpected newline style: {profile.newline_style}")
        report = build_symbol_dependency_report(target)
        symbol_names = {symbol.name for symbol in report.symbols}
        if symbol_names != {"helper", "Consumer"}:
            raise AssertionError(f"symbol extraction mismatch: {symbol_names}")
        consumer = next(symbol for symbol in report.symbols if symbol.name == "Consumer")
        if "helper" not in consumer.internal_dependencies:
            raise AssertionError("internal dependency on helper was not detected")
        if "Path" not in consumer.import_dependencies:
            raise AssertionError("import dependency on Path was not detected")
        if "CONFIG" not in consumer.global_dependencies:
            raise AssertionError("global dependency on CONFIG was not detected")
        readiness = build_workbench_dependency_readiness(intake)
        if readiness.source_mutation_enabled:
            raise AssertionError("dependency readiness must not enable source mutation")
        if readiness.dependency_report is None:
            raise AssertionError("dependency report missing from readiness result")
    _assert_module_sizes()
    _py_compile_changed_modules()
    print("VALIDATION OK: architecture-review-large-file-refactor-workbench-dependency-readiness-v1")
    print("STATUS: IN_SYNC")


def _sample_source() -> str:
    """Return a dependency-rich Python source sample."""
    return (
        "\"\"\"Sample large-module candidate.\"\"\"\n"
        "from pathlib import Path\n"
        "\n"
        "CONFIG = {\"root\": Path(\".\")}\n"
        "\n"
        "def helper(value: str) -> str:\n"
        "    return value.strip()\n"
        "\n"
        "class Consumer:\n"
        "    def build(self, name: str) -> Path:\n"
        "        return CONFIG[\"root\"] / helper(name)\n"
    )


def _plan(target: Path, source_hash: str) -> RefactorPlan:
    """Build a minimal validated Planner plan."""
    return RefactorPlan(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        target_file=str(target),
        source_content_hash=source_hash,
        settings=PlannerSettings().to_dict(),
        public_api_before=["Consumer", "helper"],
        public_api_after_expected=["Consumer", "helper"],
        symbols=[],
        atomic_clusters=[],
        proposed_modules=[],
        import_migration={},
        docstring_proposals=[],
        risks=[],
        validation_blockers=[],
        status="ready",
    )


def _analysis(target: Path, source_hash: str) -> ModuleAnalysisReport:
    """Build a minimal matching Planner analysis report."""
    return ModuleAnalysisReport(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        target_file=str(target),
        source_content_hash=source_hash,
        line_count_physical=9,
        module_docstring_present=True,
        module_docstring_preview="Sample large-module candidate.",
        all_names=["Consumer", "helper"],
        public_api_symbols=["Consumer", "helper"],
        imports=[],
        symbols=[],
        constants=["CONFIG"],
        assignments=["CONFIG"],
        global_statements=[],
        nonlocal_statements=[],
        module_level_calls=[],
        if_main_present=False,
        nested_symbol_count=0,
        missing_docstring_count=0,
        risk_flags=[],
        analysis_errors=[],
    )


def _assert_module_sizes() -> None:
    """Ensure new/touched modules obey the physical-line hard cap."""
    root = Path(__file__).resolve().parents[1]
    paths = [
        root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/source_encoding_profile.py",
        root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/symbol_dependency_builder.py",
        root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_dependency_readiness.py",
        root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_dependency_formatting.py",
        root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_gui.py",
    ]
    for path in paths:
        lines = path.read_text(encoding="utf-8").splitlines()
        if len(lines) > 500:
            raise AssertionError(f"module exceeds 500 physical lines: {path}")


def _py_compile_changed_modules() -> None:
    """Compile changed Python modules without importing PySide runtime."""
    root = Path(__file__).resolve().parents[1]
    paths = [
        root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/source_encoding_profile.py",
        root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/symbol_dependency_builder.py",
        root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_dependency_readiness.py",
        root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_dependency_formatting.py",
        root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_gui.py",
        root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/__init__.py",
    ]
    for path in paths:
        py_compile.compile(str(path), doraise=True)


if __name__ == "__main__":
    main()
