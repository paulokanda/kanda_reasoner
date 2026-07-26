"""Validate semantic strategy handling for AQR heuristic blockers."""

from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class _Context:
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]


def _load_strategy(service_path: Path):
    source = service_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(service_path))
    target = next(
        (
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef) and node.name == "_aqr_strategy"
        ),
        None,
    )
    if target is None:
        raise AssertionError("_aqr_strategy not found")
    module = ast.Module(
        body=[
            ast.ImportFrom(module="__future__", names=[ast.alias(name="annotations")], level=0),
            target,
        ],
        type_ignores=[],
    )
    ast.fix_missing_locations(module)
    namespace = {
        "Any": Any,
        "WorkbenchStageCorrectionContext": _Context,
    }
    exec(compile(module, str(service_path), "exec"), namespace)
    return namespace["_aqr_strategy"]


def _context(*, blockers: tuple[str, ...], warnings: tuple[str, ...]) -> _Context:
    return _Context(blockers=blockers, warnings=warnings)


def _assert_equal(actual: str, expected: str, marker: str) -> None:
    if actual != expected:
        raise AssertionError(f"{marker}: expected {expected!r}, got {actual!r}")
    print(marker + ": PASS")


def validate(project_root: Path) -> None:
    service_path = project_root / (
        "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
        "workbench_stage_correction_service.py"
    )
    strategy = _load_strategy(service_path)

    ruff_only = _context(
        blockers=(
            "AQR_QUALITY_DECISION:BLOCKED",
            "AQR_RULE:AQR_RUFF_NEW_REGRESSION:BLOCKED",
        ),
        warnings=(
            "AQR_GRIMP_TOPOLOGY_DELTA:New import edges match approved Preview evidence.",
            "AQR_GRIFFE_PUBLIC_CONTRACT:No public API contract breakage was detected.",
        ),
    )
    _assert_equal(
        strategy(ruff_only, object()),
        "balanced",
        "AQR_RUFF_ONLY_BLOCKER_IGNORES_PASS_RATIONALE_TOKENS",
    )

    grimp_rule = _context(
        blockers=("AQR_RULE:AQR_GRIMP_TOPOLOGY_DELTA:BLOCKED",),
        warnings=("AQR_RUFF_NEW_REGRESSION:Preview introduces no new Ruff findings.",),
    )
    _assert_equal(
        strategy(grimp_rule, object()),
        "dependency_dominant",
        "AQR_BLOCKING_GRIMP_RULE_SELECTS_DEPENDENCY_STRATEGY",
    )

    import_stage = _context(
        blockers=("AQR_STAGE:IMPORT_GRAPH:FAILED",),
        warnings=(),
    )
    _assert_equal(
        strategy(import_stage, object()),
        "dependency_dominant",
        "AQR_FAILED_IMPORT_GRAPH_SELECTS_DEPENDENCY_STRATEGY",
    )

    griffe_rule = _context(
        blockers=("AQR_RULE:AQR_GRIFFE_PUBLIC_CONTRACT:REVIEW_REQUIRED",),
        warnings=(),
    )
    _assert_equal(
        strategy(griffe_rule, object()),
        "responsibility_dominant",
        "AQR_BLOCKING_GRIFFE_RULE_SELECTS_RESPONSIBILITY_STRATEGY",
    )

    api_stage = _context(
        blockers=("AQR_STAGE:API_REVIEW:FAILED",),
        warnings=(),
    )
    _assert_equal(
        strategy(api_stage, object()),
        "responsibility_dominant",
        "AQR_FAILED_API_REVIEW_SELECTS_RESPONSIBILITY_STRATEGY",
    )

    pass_warning_only = _context(
        blockers=("AQR_RULE:AQR_MYPY_TYPE_CONTRACT:REVIEW_REQUIRED",),
        warnings=(
            "AQR_GRIMP_TOPOLOGY_DELTA:PASS rationale containing GRIMP and TOPOLOGY_DELTA.",
            "AQR_GRIFFE_PUBLIC_CONTRACT:PASS rationale containing GRIFFE and PUBLIC_CONTRACT.",
        ),
    )
    _assert_equal(
        strategy(pass_warning_only, object()),
        "balanced",
        "AQR_PASS_WARNING_TEXT_HAS_NO_STRATEGY_AUTHORITY",
    )

    line_count = len(service_path.read_text(encoding="utf-8").splitlines())
    if not 101 <= line_count <= 499:
        raise AssertionError(f"Touched source line count outside 101-499: {line_count}")
    print("TOUCHED_MODULE_LINE_LAW_101_499: PASS")
    print("AQR_HEURISTIC_BLOCKER_SEMANTIC_STRATEGY_V2: PASS")
    print("VALIDATION OK: aqr-heuristic-blocker-semantic-strategy-v2")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    validate(Path(args.project_root).expanduser().resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
