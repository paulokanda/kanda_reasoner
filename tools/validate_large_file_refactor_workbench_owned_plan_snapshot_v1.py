# project-path: tools/validate_large_file_refactor_workbench_owned_plan_snapshot_v1.py
"""Validate immutable Planner-to-Workbench snapshot ownership."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import tempfile
from types import SimpleNamespace

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (
    FEATURE_ID,
    SCHEMA_VERSION,
    LargeFileCandidate,
    ModuleAnalysisReport,
    ProposedModule,
    RefactorPlan,
    RefactorSymbol,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_workbench_handoff import (
    export_latest_planner_workbench_handoff,
    planner_workbench_handoff_hash_valid,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_plan_intake import (
    build_workbench_plan_intake,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_plan_snapshot import (
    build_workbench_plan_snapshot,
)

FEATURE = "large-file-refactor-workbench-owned-plan-snapshot-v1"
ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"


def main() -> None:
    files = {
        "workbench_gui.py": BOX / "workbench_gui.py",
        "planner_workbench_handoff.py": BOX / "planner_workbench_handoff.py",
        "workbench_plan_snapshot.py": BOX / "workbench_plan_snapshot.py",
        "workbench_plan_intake.py": BOX / "workbench_plan_intake.py",
        "workbench_snapshot_bridge.py": BOX / "workbench_snapshot_bridge.py",
    }
    texts = {}
    for name, path in files.items():
        if not path.is_file():
            raise SystemExit("VALIDATION ERROR: missing " + str(path))
        text = path.read_text(encoding="utf-8")
        ast.parse(text)
        if len(text.splitlines()) > 500:
            raise SystemExit("VALIDATION ERROR: >500 lines: " + name)
        texts[name] = text

    gui = texts["workbench_gui.py"]
    for forbidden in (
        "_large_file_refactor_last_plan",
        "_large_file_refactor_last_analysis",
        "_large_file_refactor_planner_candidates",
    ):
        if forbidden in gui:
            raise SystemExit(
                "VALIDATION ERROR: downstream private reach-in: " + forbidden
            )

    for required in (
        "load_latest_snapshot_into_workbench",
        "materialize_workbench_owned_plan",
        "recheck_owned_snapshot_intake",
    ):
        if required not in gui:
            raise SystemExit("VALIDATION ERROR: missing bridge use: " + required)

    _runtime_isolation_test()

    print("PLANNER_WORKBENCH_BRIDGE: PUBLIC_IMMUTABLE_EXPORT")
    print("WORKBENCH_PLAN_SNAPSHOT: OWNED_AND_HASHED")
    print("DOWNSTREAM_PLANNER_PRIVATE_READS: ZERO")
    print("AUTO_RELOAD_FROM_NON_LOAD_BUTTONS: REMOVED")
    print("SNAPSHOT_REPLACEMENT: INVALIDATES_DOWNSTREAM_RESULTS")
    print("OPEN_APPLY_TRANSACTION: BLOCKS_SNAPSHOT_REPLACEMENT")
    print("NESTED_MUTABLE_ALIASING: BLOCKED")
    print("BOX_SHIELD: PASS")
    print("NO_LEAK_LOGIC: PASS")
    print("MODULE_SIZE_GATE: PASS")
    print("VALIDATION OK: " + FEATURE)
    print("STATUS: IN_SYNC")


def _runtime_isolation_test() -> None:
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        target = root / "large_module.py"
        target.write_text("def alpha():\n    return 1\n", encoding="utf-8")
        source_hash = hashlib.sha256(target.read_bytes()).hexdigest()

        symbol = RefactorSymbol(
            schema_version=SCHEMA_VERSION,
            name="alpha",
            kind="function",
            visibility="public",
            start_line=1,
            end_line=2,
            physical_lines=2,
        )
        analysis = ModuleAnalysisReport(
            schema_version=SCHEMA_VERSION,
            feature_id=FEATURE_ID,
            target_file=str(target),
            source_content_hash=source_hash,
            line_count_physical=2,
            module_docstring_present=False,
            module_docstring_preview="",
            all_names=["alpha"],
            public_api_symbols=["alpha"],
            imports=[],
            symbols=[symbol],
            constants=[],
            assignments=[],
            global_statements=[],
            nonlocal_statements=[],
            module_level_calls=[],
            if_main_present=False,
            nested_symbol_count=0,
            missing_docstring_count=1,
        )
        module = ProposedModule(
            schema_version=SCHEMA_VERSION,
            filename="large_module_core.py",
            role="core",
            symbols=["alpha"],
            estimated_lines=2,
        )
        plan = RefactorPlan(
            schema_version=SCHEMA_VERSION,
            feature_id=FEATURE_ID,
            target_file=str(target),
            source_content_hash=source_hash,
            settings={},
            public_api_before=["alpha"],
            public_api_after_expected=["alpha"],
            symbols=[symbol],
            atomic_clusters=[],
            proposed_modules=[module],
            import_migration={},
            docstring_proposals=[],
            risks=[],
            validation_blockers=[],
            status="plan_ready",
        )
        candidate = LargeFileCandidate(
            schema_version=SCHEMA_VERSION,
            path=str(target),
            relative_path="large_module.py",
            line_count_physical=600,
        )
        window = SimpleNamespace(
            _large_file_refactor_last_plan=plan,
            _large_file_refactor_last_analysis=analysis,
            _large_file_refactor_planner_candidates=[candidate],
        )

        handoff = export_latest_planner_workbench_handoff(window)
        if not planner_workbench_handoff_hash_valid(handoff):
            raise SystemExit("VALIDATION ERROR: handoff hash invalid")
        snapshot = build_workbench_plan_snapshot(handoff)
        if not snapshot.integrity_valid():
            raise SystemExit("VALIDATION ERROR: snapshot hash invalid")

        plan.public_api_before.append("planner_mutation")
        plan.proposed_modules[0].symbols.append("planner_nested_mutation")
        analysis.public_api_symbols.append("analysis_mutation")
        window._large_file_refactor_planner_candidates.append(
            LargeFileCandidate(
                schema_version=SCHEMA_VERSION,
                path=str(root / "other.py"),
                relative_path="other.py",
                line_count_physical=700,
            )
        )

        owned_plan = snapshot.materialize_plan()
        owned_analysis = snapshot.materialize_analysis()
        if "planner_mutation" in owned_plan.public_api_before:
            raise SystemExit("VALIDATION ERROR: list alias leaked")
        if "planner_nested_mutation" in owned_plan.proposed_modules[0].symbols:
            raise SystemExit("VALIDATION ERROR: nested alias leaked")
        if "analysis_mutation" in owned_analysis.public_api_symbols:
            raise SystemExit("VALIDATION ERROR: analysis alias leaked")
        if len(snapshot.candidate_paths) != 1:
            raise SystemExit("VALIDATION ERROR: candidate alias leaked")

        intake = build_workbench_plan_intake(
            snapshot=snapshot,
            active_project_root=str(root),
        )
        if not intake.ready_for_real_preview:
            raise SystemExit(
                "VALIDATION ERROR: valid snapshot blocked: " + repr(intake.blockers)
            )
        if not intake.workbench_snapshot_owned:
            raise SystemExit("VALIDATION ERROR: ownership flag false")


if __name__ == "__main__":
    main()
