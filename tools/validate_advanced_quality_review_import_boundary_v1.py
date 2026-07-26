"""Validate Advanced Quality Review dependency inversion boundaries."""
from __future__ import annotations

import ast
from dataclasses import fields
from pathlib import Path
import sys
from typing import Iterable

__all__ = [
    "main",
]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import (  # noqa: E402
    analyzer_adapter_contract as contracts,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.grimp_topology_fitness_adapter import (  # noqa: E402
    GrimpTopologyReviewResult,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.mypy_fitness_adapter import (  # noqa: E402
    MypyFitnessReviewResult,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.vulture_fitness_adapter import (  # noqa: E402
    VultureFitnessReviewResult,
)

FEATURE_ID = "advanced-quality-review-import-boundary-fitness-function-v1"
MODULE_ROOT = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "manage_architecture"
    / "large_file_refactor_planner"
)

POLICY_MODULES = (
    "advanced_quality_review_contract.py",
    "advanced_quality_evidence_models.py",
    "advanced_quality_cross_check_rules.py",
    "analyzer_adapter_contract.py",
)

CONCRETE_ADAPTER_MODULES = {
    "griffe_api_fitness_adapter",
    "grimp_topology_fitness_adapter",
    "mypy_fitness_adapter",
    "ruff_fitness_adapter",
    "vulture_fitness_adapter",
}

EXTERNAL_ANALYZER_PACKAGES = {
    "ruff",
    "griffe",
    "grimp",
    "mypy",
    "vulture",
}

REQUIRED_PROTOCOL_FIELDS = {
    "GrimpTopologyResultView": {"bundle", "topology_deltas"},
    "MypyFitnessResultView": {
        "capability_mode",
        "bundle",
        "relocation_deltas",
    },
    "VultureFitnessResultView": {"bundle", "candidate_deltas"},
}

ADAPTER_RESULT_FIELDS = {
    GrimpTopologyReviewResult: {"bundle", "topology_deltas"},
    MypyFitnessReviewResult: {
        "capability_mode",
        "bundle",
        "relocation_deltas",
    },
    VultureFitnessReviewResult: {"bundle", "candidate_deltas"},
}


def main() -> int:
    """Run static and structural dependency-boundary validation."""
    _validate_policy_import_boundaries()
    _validate_contract_protocol_surface()
    _validate_concrete_results_satisfy_contract_views()
    _validate_cross_check_depends_on_contract_views()
    _validate_orchestration_is_explicit_composition_root()
    _validate_source_contracts()

    markers = (
        "AQR_POLICY_NO_CONCRETE_ADAPTER_IMPORTS: PASS",
        "AQR_POLICY_NO_EXTERNAL_ANALYZER_PACKAGE_IMPORTS: PASS",
        "AQR_ADAPTER_RESULT_VIEWS_OWNED_BY_CONTRACT: PASS",
        "AQR_CONCRETE_RESULTS_STRUCTURALLY_SATISFY_CONTRACT_VIEWS: PASS",
        "AQR_CROSS_CHECK_DEPENDS_ON_CONTRACT_VIEWS_ONLY: PASS",
        "AQR_ORCHESTRATION_REMAINS_EXPLICIT_ADAPTER_COMPOSITION_ROOT: PASS",
        "AQR_DEPENDENCY_DIRECTION_FITNESS_FUNCTION: PASS",
        "SOURCE_ASCII_UTF8_NO_BOM: PASS",
        "MODULE_SIZE_POLICY_101_499: PASS",
        f"VALIDATION OK: {FEATURE_ID}",
        "STATUS: IN_SYNC",
    )
    for marker in markers:
        print(marker)
    return 0


def _validate_policy_import_boundaries() -> None:
    concrete_violations: list[str] = []
    package_violations: list[str] = []

    for filename in POLICY_MODULES:
        path = MODULE_ROOT / filename
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for imported in _iter_imported_module_names(tree):
            root_name = imported.split(".", 1)[0]
            leaf_name = imported.rsplit(".", 1)[-1]
            if leaf_name in CONCRETE_ADAPTER_MODULES:
                concrete_violations.append(f"{filename}:{imported}")
            if root_name in EXTERNAL_ANALYZER_PACKAGES:
                package_violations.append(f"{filename}:{imported}")

    assert not concrete_violations, (
        "POLICY_CONCRETE_ADAPTER_IMPORT_VIOLATION:" + ",".join(concrete_violations)
    )
    assert not package_violations, (
        "POLICY_EXTERNAL_ANALYZER_IMPORT_VIOLATION:" + ",".join(package_violations)
    )


def _validate_contract_protocol_surface() -> None:
    source = (MODULE_ROOT / "analyzer_adapter_contract.py").read_text(
        encoding="utf-8"
    )
    tree = ast.parse(source)
    class_names = {
        node.name
        for node in tree.body
        if isinstance(node, ast.ClassDef)
    }
    exported = set(getattr(contracts, "__all__", ()))

    for name, required_fields in REQUIRED_PROTOCOL_FIELDS.items():
        assert name in class_names, f"MISSING_RESULT_VIEW_PROTOCOL:{name}"
        assert name in exported, f"RESULT_VIEW_PROTOCOL_NOT_EXPORTED:{name}"
        protocol_type = getattr(contracts, name)
        protocol_annotations = set(
            getattr(protocol_type, "__annotations__", {})
        )
        assert required_fields <= protocol_annotations, (
            f"RESULT_VIEW_PROTOCOL_FIELDS_MISSING:{name}:"
            + ",".join(sorted(required_fields - protocol_annotations))
        )


def _validate_concrete_results_satisfy_contract_views() -> None:
    for result_type, required_fields in ADAPTER_RESULT_FIELDS.items():
        observed_fields = {item.name for item in fields(result_type)}
        assert required_fields <= observed_fields, (
            f"CONCRETE_RESULT_CONTRACT_MISMATCH:{result_type.__name__}:"
            + ",".join(sorted(required_fields - observed_fields))
        )


def _validate_cross_check_depends_on_contract_views() -> None:
    path = MODULE_ROOT / "advanced_quality_cross_check_rules.py"
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imports = set(_iter_imported_module_names(tree))

    assert not any(
        imported.rsplit(".", 1)[-1] in CONCRETE_ADAPTER_MODULES
        for imported in imports
    ), "CROSS_CHECK_IMPORTS_CONCRETE_ADAPTER"

    for protocol_name in REQUIRED_PROTOCOL_FIELDS:
        assert protocol_name in source, (
            "CROSS_CHECK_MISSING_CONTRACT_VIEW:" + protocol_name
        )

    forbidden_type_names = (
        "GrimpTopologyReviewResult",
        "MypyFitnessReviewResult",
        "VultureFitnessReviewResult",
    )
    for forbidden in forbidden_type_names:
        assert forbidden not in source, (
            "CROSS_CHECK_CONCRETE_RESULT_TYPE_LEAK:" + forbidden
        )


def _validate_orchestration_is_explicit_composition_root() -> None:
    path = MODULE_ROOT / "advanced_quality_review_orchestration.py"
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imports = set(_iter_imported_module_names(tree))
    leaves = {item.rsplit(".", 1)[-1] for item in imports}
    assert CONCRETE_ADAPTER_MODULES <= leaves, (
        "ORCHESTRATION_COMPOSITION_ROOT_MISSING_ADAPTERS:"
        + ",".join(sorted(CONCRETE_ADAPTER_MODULES - leaves))
    )


def _validate_source_contracts() -> None:
    paths = [MODULE_ROOT / name for name in POLICY_MODULES]
    paths.append(Path(__file__).resolve())

    for path in paths:
        raw = path.read_bytes()
        assert not raw.startswith(b"\xef\xbb\xbf"), f"UTF8_BOM_FORBIDDEN:{path.name}"
        raw.decode("ascii")
        line_count = len(raw.decode("ascii").splitlines())
        assert 101 <= line_count <= 499, (
            f"MODULE_SIZE_OUT_OF_RANGE:{path.name}:{line_count}"
        )


def _iter_imported_module_names(tree: ast.AST) -> Iterable[str]:
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name
        elif isinstance(node, ast.ImportFrom) and node.module:
            yield node.module


if __name__ == "__main__":
    raise SystemExit(main())
