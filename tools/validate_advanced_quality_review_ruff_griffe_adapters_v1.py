# project-path: tools/validate_advanced_quality_review_ruff_griffe_adapters_v1.py
"""Focused validation for Ruff and Griffe Advanced Quality Review adapters."""
from __future__ import annotations

import hashlib
from pathlib import Path
import sys
import tempfile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.advanced_quality_review_contract import (  # noqa: E501
    AnalysisExecutionStatus,
    build_analysis_identity,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.analyzer_adapter_contract import (  # noqa: E501
    AdapterDeltaState,
    build_adapter_input_pair,
    hash_python_tree,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.griffe_api_fitness_adapter import (  # noqa: E501
    GriffeAdapterOptions,
    run_griffe_api_fitness_review,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.ruff_fitness_adapter import (  # noqa: E501
    RuffAdapterOptions,
    run_ruff_fitness_review,
)

FEATURE_ID = "advanced-quality-review-ruff-griffe-fitness-adapters-v1"
PLANNER_ROOT = PROJECT_ROOT / "kanda_reasoner_app" / "manage_architecture" / "large_file_refactor_planner"
TOUCHED_MODULES = (
    PLANNER_ROOT / "analyzer_adapter_contract.py",
    PLANNER_ROOT / "ruff_fitness_adapter.py",
    PLANNER_ROOT / "griffe_api_fitness_adapter.py",
)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="kanda_release4_adapters_") as temp_text:
        temp_root = Path(temp_text)
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
        _validate_ruff(inputs, fake_analyzer)
        _validate_griffe(inputs, fake_analyzer)
        _validate_malformed_fail_closed(inputs, fake_analyzer)
        _validate_mutation_detection(temp_root, fake_analyzer)
    _validate_source_contracts()
    _validate_module_size_policy()
    print("RUFF_BASELINE_PREVIEW_JSON_EVIDENCE: PASS")
    print("RUFF_NEW_FINDING_DELTA: PASS")
    print("RUFF_NO_FIX_SOURCE_IMMUTABILITY: PASS")
    print("RUFF_OPTIONAL_FORMAT_CHECK_EVIDENCE: PASS")
    print("GRIFFE_BASELINE_PREVIEW_API_MODELS: PASS")
    print("GRIFFE_PUBLIC_SYMBOL_REMOVAL: PASS")
    print("GRIFFE_PARAMETER_AND_DEFAULT_CHANGE: PASS")
    print("GRIFFE_ALIAS_TARGET_CHANGE: PASS")
    print("GRIFFE_API_UNCERTAINTY_FAILS_CLOSED: PASS")
    print("ADAPTER_PRE_POSTCONDITION_CONTRACT: PASS")
    print("ADAPTER_MUTATION_DETECTION_FAILS_CLOSED: PASS")
    print("ADAPTER_RAW_EVIDENCE_PROVENANCE: PASS")
    print("EXTERNAL_ANALYZERS_REMAIN_ADAPTER_DETAILS: PASS")
    print("SOURCE_ASCII_UTF8_NO_BOM: PASS")
    print("MODULE_SIZE_POLICY_101_499: PASS")
    print("ADVANCED_QUALITY_REVIEW_RUFF_GRIFFE_ADAPTERS: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


def _analysis_identity(baseline: Path, preview: Path):
    return build_analysis_identity(
        project_card_identity="card-release4-fixture",
        target_relative_path="pkg/api.py",
        baseline_hash=hash_python_tree(baseline),
        preview_hash=hash_python_tree(preview),
        refactor_plan_hash=_hash_text("plan"),
        analyzer_lock_hash=_hash_text("lock"),
        analyzer_config_hash=_hash_text("config"),
    )


def _validate_ruff(inputs, fake_analyzer: Path) -> None:
    before_baseline = hash_python_tree(inputs.baseline.root_path)
    before_preview = hash_python_tree(inputs.preview.root_path)
    bundle = run_ruff_fitness_review(
        inputs,
        RuffAdapterOptions(
            argv_prefix=(sys.executable, str(fake_analyzer)),
            engine_version="0.test",
            include_format_check=True,
        ),
    )
    assert bundle.execution_status is AnalysisExecutionStatus.SUCCEEDED
    states = {(item.state, item.finding.rule_id) for item in bundle.deltas}
    assert (AdapterDeltaState.PERSISTENT, "F401") in states
    assert (AdapterDeltaState.NEW, "F821") in states
    assert hash_python_tree(inputs.baseline.root_path) == before_baseline
    assert hash_python_tree(inputs.preview.root_path) == before_preview
    raw_map = bundle.raw_evidence_map()
    assert "ruff/baseline.json" in raw_map
    assert "ruff/preview.json" in raw_map
    assert "ruff/format_baseline.txt" in raw_map
    assert "ruff/format_preview.txt" in raw_map
    _validate_raw_references(bundle)


def _validate_griffe(inputs, fake_analyzer: Path) -> None:
    bundle = run_griffe_api_fitness_review(
        inputs,
        GriffeAdapterOptions(
            argv_prefix=(sys.executable, str(fake_analyzer)),
            engine_version="1.test",
            package_name="pkg",
        ),
    )
    assert bundle.execution_status is AnalysisExecutionStatus.SUCCEEDED
    rules = {item.rule_id for item in bundle.preview_findings}
    required = {
        "GRIFFE_PUBLIC_SYMBOL_REMOVED",
        "GRIFFE_PARAMETER_DEFAULT_CHANGED",
        "GRIFFE_REQUIRED_PARAMETER_ADDED",
        "GRIFFE_PARAMETER_ORDER_CHANGED",
        "GRIFFE_ALIAS_TARGET_CHANGED",
    }
    assert required <= rules, sorted(rules)
    assert all(item.state is AdapterDeltaState.NEW for item in bundle.deltas)
    _validate_raw_references(bundle)


def _validate_malformed_fail_closed(inputs, fake_analyzer: Path) -> None:
    ruff = run_ruff_fitness_review(
        inputs,
        RuffAdapterOptions(
            argv_prefix=(sys.executable, str(fake_analyzer)),
            engine_version="0.test",
            extra_check_args=("--malformed",),
        ),
    )
    assert ruff.execution_status is AnalysisExecutionStatus.FAILED
    assert any("MALFORMED_JSON" in item for item in ruff.diagnostics)
    griffe = run_griffe_api_fitness_review(
        inputs,
        GriffeAdapterOptions(
            argv_prefix=(sys.executable, str(fake_analyzer)),
            engine_version="1.test",
            package_name="malformed",
        ),
    )
    assert griffe.execution_status is AnalysisExecutionStatus.FAILED
    rules = {item.rule_id for item in griffe.preview_findings}
    assert "GRIFFE_API_MODEL_UNCERTAIN" in rules


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
        run_ruff_fitness_review(
            inputs,
            RuffAdapterOptions(
                argv_prefix=(sys.executable, str(fake_analyzer)),
                engine_version="0.test",
                extra_check_args=("--mutate",),
            ),
        )
    except RuntimeError as error:
        assert "ANALYZER_MUTATION_DETECTED" in str(error)
    else:
        raise AssertionError("Ruff mutation was not rejected.")


def _validate_raw_references(bundle) -> None:
    raw_map = bundle.raw_evidence_map()
    for finding in bundle.preview_findings:
        reference = finding.raw_evidence_reference
        data = raw_map[reference.relative_path]
        assert hashlib.sha256(data).hexdigest() == reference.sha256
        assert len(data) == reference.byte_size


def _validate_source_contracts() -> None:
    ruff_text = (PLANNER_ROOT / "ruff_fitness_adapter.py").read_text(encoding="utf-8")
    griffe_text = (PLANNER_ROOT / "griffe_api_fitness_adapter.py").read_text(encoding="utf-8")
    contract_text = (PLANNER_ROOT / "analyzer_adapter_contract.py").read_text(encoding="utf-8")
    assert "RUFF_MUTATING_ARGUMENT_FORBIDDEN" in ruff_text
    assert "subprocess" not in ruff_text
    assert "subprocess" not in griffe_text
    assert "import ruff" not in ruff_text
    assert "import griffe" not in griffe_text
    assert "run_bounded_process" in ruff_text
    assert "run_bounded_process" in griffe_text
    assert "ANALYZER_MUTATION_DETECTED" in contract_text
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
        (package / "__init__.py").write_text("from .api import api\n", encoding="utf-8")
        (package / "api.py").write_text(
            "def api(x=1):\n    return x\n",
            encoding="utf-8",
        )


def _hash_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _fake_analyzer_source() -> str:
    return r'''from __future__ import annotations
import json
from pathlib import Path
import sys

args = sys.argv[1:]
command = args[0]
if "--fix" in args or "--unsafe-fixes" in args:
    raise SystemExit(9)

if command == "check":
    root = Path(args[1]).resolve()
    if "--mutate" in args:
        target = root / "pkg" / "api.py"
        target.write_text(target.read_text(encoding="utf-8") + "# changed\n", encoding="utf-8")
    if "--malformed" in args:
        print("not-json")
        raise SystemExit(0)
    findings = [
        {
            "code": "F401",
            "filename": str(root / "pkg" / "api.py"),
            "message": "module imported but unused",
            "location": {"row": 1 if root.name == "baseline" else 9, "column": 1},
            "end_location": {"row": 1 if root.name == "baseline" else 9, "column": 5},
        }
    ]
    if "preview" in root.name:
        findings.append(
            {
                "code": "F821",
                "filename": str(root / "pkg" / "api.py"),
                "message": "undefined name missing_name",
                "location": {"row": 4, "column": 8},
                "end_location": {"row": 4, "column": 20},
            }
        )
    print(json.dumps(findings))
    raise SystemExit(0)

if command == "format":
    print("[]")
    raise SystemExit(0)

if command == "dump":
    package = args[1]
    search_index = args.index("--search") + 1
    root = Path(args[search_index]).resolve()
    if package == "malformed":
        print("not-json")
        raise SystemExit(0)
    baseline = "baseline" in root.name
    members = {
        "api": {
            "name": "api",
            "path": "pkg.api",
            "kind": "function",
            "is_public": True,
            "parameters": [
                {"name": "x", "kind": "positional_or_keyword", "default": "1" if baseline else "2"},
            ] + ([] if baseline else [{"name": "y", "kind": "positional_or_keyword"}]),
            "returns": "int",
        },
        "Alias": {
            "name": "Alias",
            "path": "pkg.Alias",
            "kind": "alias",
            "is_public": True,
            "target_path": "pkg.old_target" if baseline else "pkg.new_target",
        },
    }
    if baseline:
        members["gone"] = {
            "name": "gone",
            "path": "pkg.gone",
            "kind": "function",
            "is_public": True,
            "parameters": [],
            "returns": None,
        }
    payload = {
        "pkg": {
            "name": "pkg",
            "path": "pkg",
            "kind": "module",
            "is_public": True,
            "members": members,
        }
    }
    print(json.dumps(payload))
    raise SystemExit(0)

raise SystemExit(7)
'''


if __name__ == "__main__":
    raise SystemExit(main())
