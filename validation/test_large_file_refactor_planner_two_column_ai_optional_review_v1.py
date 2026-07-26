"""Focused validation for Planner two-column layout and optional AI review."""
from __future__ import annotations

import argparse
from pathlib import Path

import importlib.util
import sys
import types

FEATURE = "large-file-refactor-planner-two-column-ai-optional-review-v1"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _load_contract_modules(project_root: Path):
    box = project_root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
    package_name = "planner_validation_pkg"
    package = types.ModuleType(package_name)
    package.__path__ = [str(box)]
    sys.modules[package_name] = package

    service_name = "kanda_reasoner_app.reasoner_engine.local_ai_chat_service"
    service = types.ModuleType(service_name)
    class LocalAIChatError(RuntimeError):
        pass
    service.LocalAIChatError = LocalAIChatError
    service.get_local_ai_model_candidates = lambda selection: []
    service.chat_with_local_model = lambda *args, **kwargs: ("", "")
    sys.modules[service_name] = service

    models = _load_module(package_name + ".models", box / "models.py")
    enablement = _load_module(
        package_name + ".planner_action_enablement",
        box / "planner_action_enablement.py",
    )
    review = _load_module(
        package_name + ".planner_local_ai_plan_review",
        box / "planner_local_ai_plan_review.py",
    )
    return models, enablement, review



MODELS = None
ENABLEMENT = None
REVIEW_MODULE = None


def _symbol(name: str, lines: int, start: int):
    return MODELS.RefactorSymbol(
        schema_version=MODELS.SCHEMA_VERSION,
        name=name,
        kind="function",
        visibility="private",
        start_line=start,
        end_line=start + lines - 1,
        physical_lines=lines,
    )


def _fixture():
    symbols = [_symbol("a", 300, 1), _symbol("b", 300, 301), _symbol("c", 80, 601)]
    report = MODELS.ModuleAnalysisReport(
        schema_version=MODELS.SCHEMA_VERSION,
        feature_id=MODELS.FEATURE_ID,
        target_file="C:/project/target.py",
        source_content_hash="abc",
        line_count_physical=700,
        module_docstring_present=True,
        module_docstring_preview="test",
        all_names=[],
        public_api_symbols=[],
        imports=[],
        symbols=symbols,
        constants=[],
        assignments=[],
        global_statements=[],
        nonlocal_statements=[],
        module_level_calls=[],
        if_main_present=False,
        nested_symbol_count=0,
        missing_docstring_count=0,
    )
    modules = [
        MODELS.ProposedModule(
            schema_version=MODELS.SCHEMA_VERSION,
            filename="target.py",
            role="public_facade",
            symbols=[],
            estimated_lines=30,
            status="planned",
        ),
        MODELS.ProposedModule(
            schema_version=MODELS.SCHEMA_VERSION,
            filename="_target_analysis.py",
            role="analysis_helper",
            symbols=["a", "b"],
            estimated_lines=700,
            risk_flags=["TOO_LARGE_COHESIVE_GROUP"],
            status="warning",
        ),
        MODELS.ProposedModule(
            schema_version=MODELS.SCHEMA_VERSION,
            filename="_target_validation.py",
            role="validation_helper",
            symbols=["c"],
            estimated_lines=100,
            status="planned",
        ),
    ]
    plan = MODELS.RefactorPlan(
        schema_version=MODELS.SCHEMA_VERSION,
        feature_id=MODELS.FEATURE_ID,
        target_file=report.target_file,
        source_content_hash=report.source_content_hash,
        settings={
            "ideal_physical_lines": 400,
            "maximum_physical_lines": 500,
            "minimum_helper_physical_lines": 100,
        },
        public_api_before=[],
        public_api_after_expected=[],
        symbols=symbols,
        atomic_clusters=[],
        proposed_modules=modules,
        import_migration={},
        docstring_proposals=[],
        risks=["TOO_LARGE_COHESIVE_GROUP"],
        validation_blockers=[
            "Planned module _target_analysis.py exceeds maximum lines."
        ],
        status="blocked",
    )
    return report, plan


def _validate_ai_unavailable_fallback() -> None:
    report, plan = _fixture()
    original = REVIEW_MODULE.get_local_ai_model_candidates
    try:
        REVIEW_MODULE.get_local_ai_model_candidates = lambda selection: []
        result = REVIEW_MODULE.review_and_correct_plan_with_local_ai(report, plan)
    finally:
        REVIEW_MODULE.get_local_ai_model_candidates = original
    assert result.status == "skipped_unavailable"
    assert result.plan is plan
    assert result.fallback_used


def _validate_bounded_correction_loop() -> None:
    report, plan = _fixture()
    responses = iter(
        [
            '{"verdict":"needs_correction","reassignments":['
            '{"symbol":"b","target_module":"_target_validation.py"}],'
            '"rationale":"rebalance helpers","warnings":[]}',
            '{"verdict":"valid","reassignments":[],"rationale":"balanced",'
            '"warnings":[]}',
        ]
    )
    original_candidates = REVIEW_MODULE.get_local_ai_model_candidates
    original_chat = REVIEW_MODULE.chat_with_local_model
    try:
        REVIEW_MODULE.get_local_ai_model_candidates = lambda selection: ["mock-model"]
        REVIEW_MODULE.chat_with_local_model = lambda *args, **kwargs: (
            next(responses),
            "mock-model",
        )
        result = REVIEW_MODULE.review_and_correct_plan_with_local_ai(
            report,
            plan,
            max_rounds=3,
        )
    finally:
        REVIEW_MODULE.get_local_ai_model_candidates = original_candidates
        REVIEW_MODULE.chat_with_local_model = original_chat
    assert result.status == "corrected"
    assert result.plan.status == "planned"
    modules = {item.filename: item for item in result.plan.proposed_modules}
    assert modules["_target_analysis.py"].estimated_lines <= 500
    assert modules["_target_validation.py"].estimated_lines <= 500
    assert "b" in modules["_target_validation.py"].symbols


def _validate_preview_waits_for_ai_review() -> None:
    running = ENABLEMENT.build_planner_action_enablement(
        has_analysis=True,
        has_plan=True,
        plan_status="planned",
        has_preview=False,
        validation_passed=False,
        payload_status="",
        ai_review_running=True,
    )
    assert not running.generate_preview
    complete = ENABLEMENT.build_planner_action_enablement(
        has_analysis=True,
        has_plan=True,
        plan_status="planned",
        has_preview=False,
        validation_passed=False,
        payload_status="",
        ai_review_running=False,
    )
    assert complete.generate_preview


def _validate_source_contracts(project_root: Path) -> None:
    box = project_root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
    gui = (box / "gui_shell.py").read_text(encoding="utf-8")
    layout = (box / "planner_two_column_layout.py").read_text(encoding="utf-8")
    review = (box / "planner_local_ai_plan_review.py").read_text(encoding="utf-8")
    assert "build_planner_two_column_splitter" in gui
    assert "planning_row = QHBoxLayout()" in gui
    assert "workflow_row = QHBoxLayout()" in gui
    assert "Use local AI when available" in gui
    assert "start_optional_plan_review_for_window" in gui
    assert "QSplitter(Qt.Horizontal)" in layout
    assert "setChildrenCollapsible(False)" in layout
    assert "skipped_unavailable" in review
    assert "_MAX_REVIEW_ROUNDS = 3" in review
    assert "Atomic cluster corrections" in review

    touched = [
        box / "gui_shell.py",
        box / "planner_action_enablement.py",
        box / "planner_two_column_layout.py",
        box / "planner_local_ai_plan_review.py",
        box / "planner_local_ai_review_gui.py",
        box / "planner_local_ai_review_formatting.py",
    ]
    for path in touched:
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        assert line_count <= 500, f"Module too large: {path} has {line_count} lines"


def validate(project_root: Path) -> None:
    global MODELS, ENABLEMENT, REVIEW_MODULE
    MODELS, ENABLEMENT, REVIEW_MODULE = _load_contract_modules(project_root)
    _validate_ai_unavailable_fallback()
    _validate_bounded_correction_loop()
    _validate_preview_waits_for_ai_review()
    _validate_source_contracts(project_root)
    print("VALIDATION OK: " + FEATURE)
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root")
    args = parser.parse_args()
    validate(Path(args.project_root).resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
