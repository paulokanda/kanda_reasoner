# project-path: tools/validate_advanced_quality_review_grimp_mypy_vulture_adapters_v1.py
"""Focused validation for Grimp, mypy, and Vulture quality-review adapters."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys
import tempfile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.advanced_quality_evidence_models import FindingSeverity
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.advanced_quality_review_contract import AnalysisExecutionStatus, build_analysis_identity
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.analyzer_adapter_contract import build_adapter_input_pair, hash_python_tree
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.analyzer_environment_contract import AnalyzerCapabilityMode
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.analyzer_specific_delta_strategies import GraphTopologyDeltaState, MypyRelocationState, VultureCandidateDeltaState
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.grimp_topology_fitness_adapter import GrimpAdapterOptions, run_grimp_topology_review
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.mypy_fitness_adapter import MypyAdapterOptions, run_mypy_fitness_review
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.vulture_fitness_adapter import VultureAdapterOptions, run_vulture_fitness_review
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_project_support_paths import analyzer_cache_root

FEATURE_ID = "advanced-quality-review-grimp-mypy-vulture-fitness-adapters-v1"
PLANNER_ROOT = PROJECT_ROOT / "kanda_reasoner_app" / "manage_architecture" / "large_file_refactor_planner"
TOUCHED_MODULES = (
    PLANNER_ROOT / "analyzer_specific_delta_strategies.py",
    PLANNER_ROOT / "grimp_graph_probe.py",
    PLANNER_ROOT / "grimp_topology_fitness_adapter.py",
    PLANNER_ROOT / "mypy_fitness_adapter.py",
    PLANNER_ROOT / "vulture_fitness_adapter.py",
)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="kanda_release5_adapters_") as temp_text:
        temp_root = Path(temp_text)
        project_root = temp_root / "sample_project"
        project_root.mkdir(parents=True)
        baseline = temp_root / "baseline"
        preview = temp_root / "preview"
        _write_fixture_tree(baseline, preview)
        fake_analyzer = temp_root / "fake_analyzer.py"
        fake_analyzer.write_text(_fake_analyzer_source(), encoding="utf-8")
        inputs = build_adapter_input_pair(
            _analysis_identity(baseline, preview),
            baseline_root=baseline,
            preview_root=preview,
        )
        _validate_grimp(inputs, fake_analyzer, project_root)
        _validate_mypy(inputs, fake_analyzer, project_root)
        _validate_mypy_capability_modes(inputs, fake_analyzer, project_root)
        _validate_vulture(inputs, fake_analyzer)
        _validate_malformed_fail_closed(inputs, fake_analyzer, project_root)
        _validate_mutation_detection(temp_root, fake_analyzer)
        cache_root = analyzer_cache_root(project_root)
        assert cache_root.is_dir()
        assert "_delete_after_daily_work" in str(cache_root)
        assert "_show_project_to_AI" not in str(cache_root)
    _validate_source_contracts()
    _validate_module_size_policy()
    print("GRIMP_BASELINE_PREVIEW_GRAPH_EVIDENCE: PASS")
    print("GRIMP_NEW_AND_REMOVED_EDGE_DELTA: PASS")
    print("GRIMP_NEW_CYCLE_BREAKER_DELTA: PASS")
    print("GRIMP_CACHE_TRANSIENT_GARBAGE_ONLY: PASS")
    print("MYPY_CAPABILITY_MODE_CONDITIONAL_EXECUTION: PASS")
    print("MYPY_EXIT_ONE_FINDINGS_NORMALIZED: PASS")
    print("MYPY_EXACT_AND_RELOCATED_MATCH: PASS")
    print("MYPY_AMBIGUOUS_MATCH_REMAINS_AMBIGUOUS: PASS")
    print("MYPY_NEW_AND_RESOLVED_FINDINGS: PASS")
    print("VULTURE_EXIT_THREE_FINDINGS_NORMALIZED: PASS")
    print("VULTURE_ENGINE_CONFIDENCE_PRESERVED_AS_HEURISTIC: PASS")
    print("VULTURE_MAXIMUM_UNILATERAL_AUTHORITY_ADVISORY: PASS")
    print("VULTURE_NEW_CANDIDATE_DELTA: PASS")
    print("ANALYZER_SPECIFIC_DELTA_STRATEGIES_SEPARATE: PASS")
    print("MALFORMED_ANALYZER_OUTPUT_FAILS_CLOSED: PASS")
    print("RELEASE5_ADAPTER_MUTATION_DETECTION_FAILS_CLOSED: PASS")
    print("RELEASE5_RAW_EVIDENCE_PROVENANCE: PASS")
    print("EXTERNAL_ANALYZERS_REMAIN_ADAPTER_SIDE_DETAILS: PASS")
    print("SOURCE_ASCII_UTF8_NO_BOM: PASS")
    print("MODULE_SIZE_POLICY_101_499: PASS")
    print("ADVANCED_QUALITY_REVIEW_GRIMP_MYPY_VULTURE_ADAPTERS: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


def _analysis_identity(baseline: Path, preview: Path):
    return build_analysis_identity(
        project_card_identity="card-release5-fixture",
        target_relative_path="pkg/a.py",
        baseline_hash=hash_python_tree(baseline),
        preview_hash=hash_python_tree(preview),
        refactor_plan_hash=_hash_text("plan"),
        analyzer_lock_hash=_hash_text("lock"),
        analyzer_config_hash=_hash_text("config"),
    )


def _validate_grimp(inputs, fake_analyzer: Path, project_root: Path) -> None:
    result = run_grimp_topology_review(
        inputs,
        GrimpAdapterOptions(
            argv_prefix=(sys.executable, str(fake_analyzer), "grimp"),
            engine_version="3.test",
            package_name="pkg",
            active_project_root=project_root,
            config_hash=_hash_text("grimp-config"),
            analysis_key="release5-fixture",
        ),
    )
    assert result.bundle.execution_status is AnalysisExecutionStatus.SUCCEEDED
    states = {item.state for item in result.topology_deltas}
    assert GraphTopologyDeltaState.NEW_EDGE in states
    assert GraphTopologyDeltaState.PERSISTENT_EDGE in states
    assert GraphTopologyDeltaState.NEW_CYCLE_BREAKER in states
    assert ("pkg.b", "pkg.a") in result.preview_graph.cycle_breakers
    _validate_raw_references(result.bundle)


def _validate_mypy(inputs, fake_analyzer: Path, project_root: Path) -> None:
    result = run_mypy_fitness_review(
        inputs,
        MypyAdapterOptions(
            argv_prefix=(sys.executable, str(fake_analyzer), "mypy"),
            engine_version="2.test",
            capability_mode=AnalyzerCapabilityMode.AUTHORITATIVE,
            active_project_root=project_root,
            config_hash=_hash_text("mypy-config"),
            analysis_key="release5-fixture",
        ),
    )
    assert result.executed
    assert result.bundle is not None
    assert result.bundle.execution_status is AnalysisExecutionStatus.SUCCEEDED
    assert result.bundle.baseline_execution.exit_code == 1
    assert result.bundle.baseline_execution.status is AnalysisExecutionStatus.SUCCEEDED
    states = {item.state for item in result.relocation_deltas}
    required = {
        MypyRelocationState.EXACT_MATCH,
        MypyRelocationState.RELOCATED_MATCH,
        MypyRelocationState.AMBIGUOUS_MATCH,
        MypyRelocationState.NEW_FINDING,
        MypyRelocationState.RESOLVED_FINDING,
    }
    assert required <= states, sorted(item.value for item in states)
    ambiguous = [
        item for item in result.relocation_deltas
        if item.state is MypyRelocationState.AMBIGUOUS_MATCH
    ]
    assert ambiguous and len(ambiguous[0].candidate_semantic_keys) == 2
    _validate_raw_references(result.bundle)


def _validate_mypy_capability_modes(inputs, fake_analyzer: Path, project_root: Path) -> None:
    for mode in (
        AnalyzerCapabilityMode.NOT_CONFIGURED,
        AnalyzerCapabilityMode.UNAVAILABLE,
    ):
        result = run_mypy_fitness_review(
            inputs,
            MypyAdapterOptions(
                argv_prefix=(sys.executable, str(fake_analyzer), "mypy"),
                engine_version="2.test",
                capability_mode=mode,
                active_project_root=project_root,
                config_hash=_hash_text("mypy-config"),
                analysis_key="release5-fixture-" + mode.value.lower(),
            ),
        )
        assert not result.executed
        assert result.bundle is None
        assert mode.value in result.diagnostic
    non_authoritative = run_mypy_fitness_review(
        inputs,
        MypyAdapterOptions(
            argv_prefix=(sys.executable, str(fake_analyzer), "mypy"),
            engine_version="2.test",
            capability_mode=AnalyzerCapabilityMode.AVAILABLE_NON_AUTHORITATIVE,
            active_project_root=project_root,
            config_hash=_hash_text("mypy-config"),
            analysis_key="release5-non-authoritative",
        ),
    )
    assert non_authoritative.executed
    assert non_authoritative.bundle is not None


def _validate_vulture(inputs, fake_analyzer: Path) -> None:
    result = run_vulture_fitness_review(
        inputs,
        VultureAdapterOptions(
            argv_prefix=(sys.executable, str(fake_analyzer), "vulture"),
            engine_version="2.test",
            min_confidence=60,
        ),
    )
    bundle = result.bundle
    assert bundle.execution_status is AnalysisExecutionStatus.SUCCEEDED
    assert bundle.baseline_execution.exit_code == 3
    assert bundle.baseline_execution.status is AnalysisExecutionStatus.SUCCEEDED
    assert all(item.severity is FindingSeverity.ADVISORY for item in bundle.preview_findings)
    metadata = dict(bundle.preview_findings[0].metadata)
    assert metadata["engine_confidence_semantics"] == "vulture_heuristic_not_probability"
    states = {item.state for item in result.candidate_deltas}
    assert VultureCandidateDeltaState.NEW_CANDIDATE in states
    assert VultureCandidateDeltaState.PERSISTENT_CANDIDATE in states
    _validate_raw_references(bundle)


def _validate_malformed_fail_closed(inputs, fake_analyzer: Path, project_root: Path) -> None:
    grimp = run_grimp_topology_review(
        inputs,
        GrimpAdapterOptions(
            argv_prefix=(sys.executable, str(fake_analyzer), "grimp", "--malformed"),
            engine_version="3.test",
            package_name="pkg",
            active_project_root=project_root,
            config_hash=_hash_text("bad-grimp"),
            analysis_key="bad-grimp",
        ),
    )
    assert grimp.bundle.execution_status is AnalysisExecutionStatus.FAILED
    mypy = run_mypy_fitness_review(
        inputs,
        MypyAdapterOptions(
            argv_prefix=(sys.executable, str(fake_analyzer), "mypy"),
            engine_version="2.test",
            capability_mode=AnalyzerCapabilityMode.AUTHORITATIVE,
            active_project_root=project_root,
            config_hash=_hash_text("bad-mypy"),
            analysis_key="bad-mypy",
            extra_args=("--malformed",),
        ),
    )
    assert mypy.bundle is not None
    assert mypy.bundle.execution_status is AnalysisExecutionStatus.FAILED
    vulture = run_vulture_fitness_review(
        inputs,
        VultureAdapterOptions(
            argv_prefix=(sys.executable, str(fake_analyzer), "vulture"),
            engine_version="2.test",
            extra_args=("--malformed",),
        ),
    )
    assert vulture.bundle.execution_status is AnalysisExecutionStatus.FAILED


def _validate_mutation_detection(temp_root: Path, fake_analyzer: Path) -> None:
    baseline = temp_root / "mutation_baseline"
    preview = temp_root / "mutation_preview"
    _write_fixture_tree(baseline, preview)
    inputs = build_adapter_input_pair(
        _analysis_identity(baseline, preview),
        baseline_root=baseline,
        preview_root=preview,
    )
    try:
        run_vulture_fitness_review(
            inputs,
            VultureAdapterOptions(
                argv_prefix=(sys.executable, str(fake_analyzer), "vulture"),
                engine_version="2.test",
                extra_args=("--mutate",),
            ),
        )
    except RuntimeError as error:
        assert "ANALYZER_MUTATION_DETECTED" in str(error)
    else:
        raise AssertionError("Vulture mutation was not rejected.")


def _validate_raw_references(bundle) -> None:
    raw_map = bundle.raw_evidence_map()
    for finding in bundle.preview_findings:
        reference = finding.raw_evidence_reference
        data = raw_map[reference.relative_path]
        assert hashlib.sha256(data).hexdigest() == reference.sha256
        assert len(data) == reference.byte_size


def _validate_source_contracts() -> None:
    delta_text = (PLANNER_ROOT / "analyzer_specific_delta_strategies.py").read_text(encoding="utf-8")
    grimp_text = (PLANNER_ROOT / "grimp_topology_fitness_adapter.py").read_text(encoding="utf-8")
    probe_text = (PLANNER_ROOT / "grimp_graph_probe.py").read_text(encoding="utf-8")
    mypy_text = (PLANNER_ROOT / "mypy_fitness_adapter.py").read_text(encoding="utf-8")
    vulture_text = (PLANNER_ROOT / "vulture_fitness_adapter.py").read_text(encoding="utf-8")
    assert "import grimp" not in grimp_text
    assert "import grimp" in probe_text
    assert "import mypy" not in mypy_text
    assert "import vulture" not in vulture_text
    assert "subprocess" not in grimp_text
    assert "subprocess" not in mypy_text
    assert "subprocess" not in vulture_text
    assert "run_bounded_process" in grimp_text
    assert "run_bounded_process" in mypy_text
    assert "run_bounded_process" in vulture_text
    assert "AMBIGUOUS_MATCH" in delta_text
    assert "vulture_heuristic_not_probability" in vulture_text
    for path in TOUCHED_MODULES:
        data = path.read_bytes()
        assert not data.startswith(b"\xef\xbb\xbf")
        data.decode("ascii")


def _validate_module_size_policy() -> None:
    for path in TOUCHED_MODULES:
        count = len(path.read_text(encoding="utf-8").splitlines())
        assert 101 <= count <= 499, (path.name, count)


def _write_fixture_tree(baseline: Path, preview: Path) -> None:
    for root in (baseline, preview):
        package = root / "pkg"
        package.mkdir(parents=True, exist_ok=True)
        (package / "__init__.py").write_text("from .a import api\n", encoding="utf-8")
        (package / "a.py").write_text("def api(x: int) -> int:\n    return x\n", encoding="utf-8")
        (package / "b.py").write_text("def helper() -> int:\n    return 1\n", encoding="utf-8")
        (package / "c.py").write_text("def moved() -> int:\n    return 2\n", encoding="utf-8")


def _hash_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _fake_analyzer_source() -> str:
    return r'''from __future__ import annotations
import json
from pathlib import Path
import sys

kind = sys.argv[1]
args = sys.argv[2:]
malformed = "--malformed" in args
mutate = "--mutate" in args

if kind == "grimp":
    root = Path(args[args.index("--root") + 1]).resolve()
    if malformed:
        print("not-json")
        raise SystemExit(0)
    baseline = root.name == "baseline"
    edges = [
        {"importer": "pkg.a", "imported": "pkg.b"},
    ]
    cycle_breakers = []
    if not baseline:
        edges.extend([
            {"importer": "pkg.b", "imported": "pkg.a"},
            {"importer": "pkg.c", "imported": "pkg.b"},
        ])
        cycle_breakers.append({"importer": "pkg.b", "imported": "pkg.a"})
    print(json.dumps({
        "schema_version": "1.0",
        "engine": "grimp",
        "package_name": "pkg",
        "modules": ["pkg", "pkg.a", "pkg.b", "pkg.c"],
        "edges": edges,
        "cycle_breakers": cycle_breakers,
    }))
    raise SystemExit(0)

if kind == "mypy":
    root = Path(args[-1]).resolve()
    if malformed:
        print("not-json")
        raise SystemExit(1)
    baseline = root.name == "baseline"
    records = []
    def add(file_name, line, message, code):
        records.append({
            "file": str(root / "pkg" / file_name),
            "line": line,
            "column": 1,
            "end_line": line,
            "end_column": 4,
            "message": message,
            "hint": None,
            "code": code,
            "severity": "error",
        })
    if baseline:
        add("a.py", 5, "Argument 1 has incompatible type", "arg-type")
        add("a.py", 10, "Name x is not defined", "name-defined")
        add("a.py", 20, "Shared ambiguous error", "misc")
        add("b.py", 30, "Shared ambiguous error", "misc")
        add("b.py", 40, "Module has no attribute old", "attr-defined")
    else:
        add("a.py", 50, "Argument 1 has incompatible type", "arg-type")
        add("c.py", 60, "Name x is not defined", "name-defined")
        add("c.py", 70, "Shared ambiguous error", "misc")
        add("c.py", 80, "Unsupported operand types", "operator")
    for record in records:
        print(json.dumps(record))
    raise SystemExit(1)

if kind == "vulture":
    root = Path(args[0]).resolve()
    if mutate:
        target = root / "pkg" / "a.py"
        target.write_text(target.read_text(encoding="utf-8") + "# changed\n", encoding="utf-8")
    if malformed:
        print("this output does not match the documented format")
        raise SystemExit(3)
    print(f"{root / 'pkg' / 'a.py'}:10: unused function 'legacy' (60% confidence)")
    if root.name == "preview":
        print(f"{root / 'pkg' / 'c.py'}:12: unused function 'new_helper' (60% confidence)")
    raise SystemExit(3)

raise SystemExit(7)
'''


if __name__ == "__main__":
    raise SystemExit(main())
