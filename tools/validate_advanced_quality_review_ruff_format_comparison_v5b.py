# project-path: tools/validate_advanced_quality_review_ruff_format_comparison_v5b.py
"""Validate AQR baseline-versus-Preview Ruff formatter comparison."""

# ruff: noqa: E402

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import (
    advanced_quality_cross_check_rules as cross_rules,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.advanced_quality_review_contract import (  # noqa: E501
    AnalysisExecutionStatus,
    build_analysis_identity,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.advanced_quality_review_gui_context import (  # noqa: E501
    _copy_canonical_ruff_policy,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.analyzer_adapter_contract import (  # noqa: E501
    build_adapter_input_pair,
    hash_python_tree,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.ruff_fitness_adapter import (  # noqa: E501
    RuffAdapterOptions,
    run_ruff_fitness_review,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.ruff_format_comparison import (  # noqa: E501
    RUFF_FORMAT_COMPARISON_EVIDENCE_PATH,
    load_ruff_format_comparison_summary,
)

FEATURE_ID = "advanced-quality-review-ruff-format-comparison-v5b"
PATCH_FILES = (
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/advanced_quality_cross_check_rules.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/advanced_quality_review_gui_context.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/ruff_fitness_adapter.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/ruff_format_comparison.py",
    "tools/validate_advanced_quality_review_ruff_format_comparison_v5b.py",
)
_PLANNER = "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
FROZEN_HASHES = {
    _PLANNER + "advanced_quality_review_orchestration.py": (
        "289ba6c50583db84836f38b21e9c78ffd96e445d06a1b67e65ef3eb8943c3f96"
    ),
    _PLANNER + "workbench_post_apply_ruff_validation.py": (
        "7fd0612441caeef2e4ecec54d58c2d7ad7aef90bfd5abdf7c9d39792417a8ced"
    ),
    _PLANNER + "workbench_post_apply_validator.py": (
        "b07b022cd1057163b61b4ef9620b8c51994df72dbf20c8ee663e272be1c129cc"
    ),
    _PLANNER + "analyzer_pinned_environment_spec.py": (
        "676d001f8cd75b47bc123310283143f00f6cd71c7635955849b9b8163b26a3aa"
    ),
    _PLANNER + "analyzer_environment_requirements_v1.txt": (
        "809e095393ca14ab25ec30ef591e3595c6ba4c2d759b51161adc47175cf6cdd6"
    ),
    "ruff.toml": ("52172a11111cedc04a0942130358ecb65ffa34ee98be833ef6c50cbc01bc0746"),
}


def main() -> int:
    args = _parse_args()
    root = Path(args.project_root).expanduser().resolve(strict=True)
    patch_zip = Path(args.patch_zip).expanduser().resolve(strict=True)
    ruff = Path(args.ruff_executable).expanduser().resolve(strict=True)
    _validate_patch_members(patch_zip)
    _validate_frozen_identity(root)
    _validate_source_contract(root)
    _validate_python_source(root)
    _validate_policy_copy(root)
    _validate_fake_runtime(root)
    _validate_real_runtime(root, ruff)
    _validate_touched_with_ruff(root, ruff)
    _print_markers()
    return 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--patch-zip", required=True)
    parser.add_argument("--ruff-executable", required=True)
    return parser.parse_args()


def _validate_patch_members(path: Path) -> None:
    with zipfile.ZipFile(path) as archive:
        members = tuple(sorted(archive.namelist()))
    expected = tuple(sorted((*PATCH_FILES, "KANDA_FREEZE_HINT.json")))
    _assert(members == expected, "PATCH_MEMBER_SCOPE_INVALID")
    print("PATCH_MEMBER_SCOPE_AQR_FORMAT_COMPARISON_ONLY: PASS")


def _validate_frozen_identity(root: Path) -> None:
    for relative, expected in FROZEN_HASHES.items():
        observed = _sha256(root / relative)
        _assert(observed == expected, "FROZEN_IDENTITY_MISMATCH:" + relative)
    print("PHASE4_PHASE5A_FROZEN_IDENTITY: PASS")
    print("AQR_ORCHESTRATION_BYTE_IDENTITY: PASS")


def _validate_source_contract(root: Path) -> None:
    planner = (
        root / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
    )
    gui = (planner / "advanced_quality_review_gui_context.py").read_text(
        encoding="utf-8"
    )
    adapter = (planner / "ruff_fitness_adapter.py").read_text(encoding="utf-8")
    comparison = (planner / "ruff_format_comparison.py").read_text(
        encoding="utf-8"
    )
    rules = (planner / "advanced_quality_cross_check_rules.py").read_text(
        encoding="utf-8"
    )
    _assert("include_ruff_format_check=True" in gui, "AQR_GUI_FORMAT_DISABLED")
    _assert("_copy_canonical_ruff_policy" in gui, "AQR_POLICY_COPY_MISSING")
    _assert("run_ruff_format_comparison" in adapter, "AQR_FORMAT_ADAPTER_MISSING")
    _assert(
        "--output-format" not in _format_command_slice(comparison),
        "FORMAT_JSON_FLAG_PRESENT",
    )
    for forbidden in ("--fix", "--fix-only", "--unsafe-fixes"):
        _assert(
            forbidden not in _runtime_format_argv_slice(comparison),
            "FORMAT_MUTATION_ARGUMENT_PRESENT:" + forbidden,
        )
    _assert("load_ruff_format_comparison_summary" in rules, "FORMAT_RULE_MISSING")
    _assert("new_required_paths" in rules, "FORMAT_DELTA_BLOCKER_MISSING")
    print("AQR_GUI_FORMAT_COMPARISON_ENABLED: PASS")
    print("AQR_CANONICAL_RUFF_POLICY_COPIED_TO_VIEWS: PASS")
    print("AQR_RUFF_FORMAT_CLI_COMPATIBILITY: PASS")
    print("AQR_RUFF_FORMAT_READ_ONLY: PASS")


def _format_command_slice(text: str) -> str:
    start = text.index("def _run_format_check(")
    end = text.index("def _interpret_format_execution(", start)
    return text[start:end]


def _runtime_format_argv_slice(text: str) -> str:
    section = _format_command_slice(text)
    start = section.index("argv = [")
    end = section.index("_validate_read_only_argv", start)
    return section[start:end]


def _validate_python_source(root: Path) -> None:
    for relative in PATCH_FILES:
        path = root / relative
        data = path.read_bytes()
        _assert(not data.startswith(b"\xef\xbb\xbf"), "SOURCE_BOM:" + relative)
        data.decode("ascii")
        if path.suffix == ".py":
            compile(data, str(path), "exec")
            lines = len(data.decode("ascii").splitlines())
            _assert(lines < 500, "MODULE_SIZE_LAW:" + relative + ":" + str(lines))
    print("PYTHON_COMPILE: PASS")
    print("ASCII_PYTHON_SOURCE: PASS")
    print("MODULE_SIZE_LAW_BELOW_500: PASS")


def _validate_policy_copy(root: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="kanda_aqr_v5b_policy_") as temp:
        destination = Path(temp) / "view"
        destination.mkdir()
        _copy_canonical_ruff_policy(root, destination)
        copied = destination / "ruff.toml"
        _assert(copied.is_file(), "AQR_COPIED_RUFF_POLICY_MISSING")
        _assert(_sha256(copied) == FROZEN_HASHES["ruff.toml"], "AQR_POLICY_COPY_HASH")
    print("AQR_RUFF_POLICY_VIEW_IDENTITY: PASS")


def _validate_fake_runtime(root: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="kanda_aqr_v5b_fake_") as temp:
        temp_root = Path(temp)
        analyzer = temp_root / "fake_ruff.py"
        analyzer.write_text(_fake_ruff_source(), encoding="ascii")
        scenarios = (
            ("clean", "needs", "BLOCKED", ("pkg/api.py",)),
            ("needs", "needs", "PASS", ()),
            ("needs", "clean", "PASS", ()),
        )
        for baseline_state, preview_state, decision, new_paths in scenarios:
            inputs = _fixture_inputs(temp_root, baseline_state, preview_state)
            before = (
                hash_python_tree(inputs.baseline.root_path),
                hash_python_tree(inputs.preview.root_path),
            )
            bundle = run_ruff_fitness_review(
                inputs,
                RuffAdapterOptions(
                    argv_prefix=(sys.executable, str(analyzer)),
                    engine_version="0.15.21",
                    include_format_check=True,
                ),
            )
            _assert(
                bundle.execution_status is AnalysisExecutionStatus.SUCCEEDED,
                "FAKE_FORMAT_STATUS",
            )
            summary = load_ruff_format_comparison_summary(bundle.raw_evidence_map())
            _assert(summary is not None, "FAKE_FORMAT_SUMMARY_MISSING")
            _assert(summary.new_required_paths == new_paths, "FAKE_FORMAT_DELTA")
            rule = cross_rules._ruff_regression_rule(bundle)
            _assert(rule.decision.value == decision, "FAKE_FORMAT_RULE:" + decision)
            after = (
                hash_python_tree(inputs.baseline.root_path),
                hash_python_tree(inputs.preview.root_path),
            )
            _assert(before == after, "FAKE_FORMAT_MUTATED_SOURCE")
        failed = _fixture_inputs(temp_root, "clean", "fail")
        bundle = run_ruff_fitness_review(
            failed,
            RuffAdapterOptions(
                argv_prefix=(sys.executable, str(analyzer)),
                engine_version="0.15.21",
                include_format_check=True,
            ),
        )
        _assert(
            bundle.execution_status is AnalysisExecutionStatus.FAILED,
            "FORMAT_FAILURE_NOT_CLOSED",
        )
        rule = cross_rules._ruff_regression_rule(bundle)
        _assert(rule.decision.value == "INDETERMINATE", "FORMAT_FAILURE_RULE")
    print("AQR_RUFF_FORMAT_NEW_PATH_REGRESSION_BLOCKS: PASS")
    print("AQR_RUFF_FORMAT_PERSISTENT_BASELINE_DEBT_NOT_NEW: PASS")
    print("AQR_RUFF_FORMAT_RESOLUTION_PASSES: PASS")
    print("AQR_RUFF_FORMAT_EXECUTION_FAILURE_INDETERMINATE: PASS")
    print("AQR_RUFF_FORMAT_SOURCE_IMMUTABILITY: PASS")


def _fixture_inputs(temp_root: Path, baseline_state: str, preview_state: str):
    scenario = temp_root / (
        baseline_state
        + "_"
        + preview_state
        + "_"
        + hashlib.sha1(str(len(list(temp_root.iterdir()))).encode()).hexdigest()[:6]
    )
    baseline = scenario / "baseline"
    preview = scenario / "preview"
    for root, state in ((baseline, baseline_state), (preview, preview_state)):
        package = root / "pkg"
        package.mkdir(parents=True)
        (package / "api.py").write_text("def api():\n    return 1\n", encoding="ascii")
        (root / "format_state.txt").write_text(state, encoding="ascii")
    identity = build_analysis_identity(
        project_card_identity="aqr-v5b-fixture",
        target_relative_path="pkg/api.py",
        baseline_hash=hash_python_tree(baseline),
        preview_hash=hash_python_tree(preview),
        refactor_plan_hash=_text_hash("plan"),
        analyzer_lock_hash=_text_hash("lock"),
        analyzer_config_hash=_text_hash("config"),
    )
    return build_adapter_input_pair(
        identity, baseline_root=baseline, preview_root=preview
    )


def _fake_ruff_source() -> str:
    return r"""from __future__ import annotations
import json
from pathlib import Path
import sys
args = sys.argv[1:]
command = args[0]
root = Path(args[-1]).resolve() if command == "format" else Path(args[1]).resolve()
if command == "check":
    output = Path(args[args.index("--output-file") + 1])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps([]), encoding="utf-8")
    raise SystemExit(0)
if command == "format":
    state = (root / "format_state.txt").read_text(encoding="utf-8").strip()
    if state == "clean":
        print("1 file already formatted")
        raise SystemExit(0)
    if state == "needs":
        print("Would reformat: " + str(root / "pkg" / "api.py"))
        print("1 file would be reformatted")
        raise SystemExit(1)
    print("formatter execution failed", file=sys.stderr)
    raise SystemExit(2)
raise SystemExit(7)
"""


def _validate_real_runtime(root: Path, ruff: Path) -> None:
    version = subprocess.run(
        (str(ruff), "--version"), capture_output=True, text=True, check=False
    )
    _assert(version.returncode == 0, "RUFF_VERSION_COMMAND_FAILED")
    _assert(version.stdout.strip() == "ruff 0.15.21", "RUFF_VERSION_MISMATCH")
    with tempfile.TemporaryDirectory(prefix="kanda_aqr_v5b_real_") as temp:
        temp_root = Path(temp)
        baseline = temp_root / "baseline"
        preview = temp_root / "preview"
        baseline.mkdir()
        preview.mkdir()
        shutil.copy2(root / "ruff.toml", baseline / "ruff.toml")
        shutil.copy2(root / "ruff.toml", preview / "ruff.toml")
        (baseline / "api.py").write_text("def api():\n    return 1\n", encoding="ascii")
        (preview / "api.py").write_text("def api( ):\n return 1\n", encoding="ascii")
        identity = build_analysis_identity(
            project_card_identity="aqr-v5b-real",
            target_relative_path="api.py",
            baseline_hash=hash_python_tree(baseline),
            preview_hash=hash_python_tree(preview),
            refactor_plan_hash=_text_hash("plan"),
            analyzer_lock_hash=_text_hash("lock"),
            analyzer_config_hash=_sha256(root / "ruff.toml"),
        )
        inputs = build_adapter_input_pair(
            identity, baseline_root=baseline, preview_root=preview
        )
        bundle = run_ruff_fitness_review(
            inputs,
            RuffAdapterOptions(
                argv_prefix=(str(ruff),),
                engine_version="0.15.21",
                include_format_check=True,
            ),
        )
        summary = load_ruff_format_comparison_summary(bundle.raw_evidence_map())
        _assert(summary is not None, "REAL_FORMAT_SUMMARY_MISSING")
        _assert(summary.new_required_paths == ("api.py",), "REAL_FORMAT_DELTA")
        _assert(
            cross_rules._ruff_regression_rule(bundle).decision.value == "BLOCKED",
            "REAL_FORMAT_NOT_BLOCKED",
        )
        _assert(not (baseline / ".ruff_cache").exists(), "BASELINE_RUFF_CACHE_CREATED")
        _assert(not (preview / ".ruff_cache").exists(), "PREVIEW_RUFF_CACHE_CREATED")
        _assert(
            RUFF_FORMAT_COMPARISON_EVIDENCE_PATH in bundle.raw_evidence_map(),
            "REAL_FORMAT_EVIDENCE_MISSING",
        )
    print("RUNTIME_RUFF_0_15_21: PASS")
    print("RUNTIME_RUFF_FORMAT_COMPARISON: PASS")
    print("AQR_RUFF_NO_VIEW_CACHE: PASS")


def _validate_touched_with_ruff(root: Path, ruff: Path) -> None:
    paths = tuple(str(root / item) for item in PATCH_FILES)
    common = (
        "--no-preview",
        "--no-cache",
        "--force-exclude",
        "--color",
        "never",
        "--config",
        str(root / "ruff.toml"),
    )
    lint = subprocess.run(
        (str(ruff), "check", "--no-fix", "--no-unsafe-fixes", *common, *paths),
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    _assert(lint.returncode == 0, "TOUCHED_RUFF_LINT:" + lint.stdout + lint.stderr)
    formatting = subprocess.run(
        (str(ruff), "format", "--check", *common, *paths),
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    _assert(
        formatting.returncode == 0,
        "TOUCHED_RUFF_FORMAT:" + formatting.stdout + formatting.stderr,
    )
    print("TOUCHED_MODULE_RUFF_LINT: PASS")
    print("TOUCHED_MODULE_RUFF_FORMAT_CHECK: PASS")


def _print_markers() -> None:
    print("PATCH_ZIP_CONTRACT: PASS")
    print("VALIDATION OK: " + FEATURE_ID)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


if __name__ == "__main__":
    raise SystemExit(main())
