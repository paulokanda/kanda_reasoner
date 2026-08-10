# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_shadow_validation.py
"""Layered structural, API, topology, runtime, and behavior validation in shadow."""
from __future__ import annotations

import ast
import compileall
from dataclasses import asdict, dataclass, field
import hashlib
from pathlib import Path
import subprocess
import sys
from typing import Any

from kanda_reasoner_app.project_python_fire_shield import (
    run_project_python_governed,
)

from .models import SCHEMA_VERSION
from .workbench_dynamic_python_risks import DynamicPythonRiskReport
from .workbench_execution_contract import WorkbenchExecutionContract
from .workbench_refactor_baseline import RefactorBaseline
from .workbench_sealed_payload import WorkbenchSealedPayload, verify_sealed_payload
from .workbench_shadow_backend import ShadowMaterializationResult
from .workbench_shadow_provenance import ShadowProvenanceResult

__all__ = [
    "SHADOW_VALIDATION_FEATURE_ID",
    "ShadowBehaviorEvidence",
    "ShadowValidationResult",
    "validate_shadow_refactor",
]

SHADOW_VALIDATION_FEATURE_ID = (
    "architecture-review-large-file-refactor-workbench-shadow-validation-v1"
)
_TIMEOUT_SECONDS = 120


@dataclass(frozen=True)
class ShadowBehaviorEvidence:
    """Classified pytest collection and focused behavior evidence from shadow."""

    collection_status: str
    collection_exit_code: int | None
    collected_test_lines: tuple[str, ...]
    execution_status: str
    execution_exit_code: int | None
    output_hash: str
    baseline_comparison: str
    stdout_excerpt: str
    stderr_excerpt: str

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["collected_test_lines"] = list(self.collected_test_lines)
        return data


@dataclass(frozen=True)
class ShadowValidationResult:
    """Aggregated shadow evidence used before human diff review and real apply authorization."""

    schema_version: str
    feature_id: str
    status: str
    shadow_root: str
    payload_hash: str
    structural_status: str
    api_status: str
    topology_status: str
    provenance_status: str
    runtime_status: str
    behavior_status: str
    checked_files: tuple[str, ...]
    api_before: tuple[str, ...]
    api_after: tuple[str, ...]
    dependency_graph: dict[str, tuple[str, ...]]
    behavior: ShadowBehaviorEvidence
    blockers: tuple[str, ...]
    warnings: tuple[str, ...] = field(default_factory=tuple)
    source_mutation_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["checked_files"] = list(self.checked_files)
        data["api_before"] = list(self.api_before)
        data["api_after"] = list(self.api_after)
        data["dependency_graph"] = {
            key: list(value) for key, value in self.dependency_graph.items()
        }
        data["behavior"] = self.behavior.to_dict()
        data["blockers"] = list(self.blockers)
        data["warnings"] = list(self.warnings)
        return data


def validate_shadow_refactor(
    *,
    contract: WorkbenchExecutionContract,
    baseline: RefactorBaseline,
    sealed_payload: WorkbenchSealedPayload,
    materialization: ShadowMaterializationResult,
    provenance: ShadowProvenanceResult,
    dynamic_risks: DynamicPythonRiskReport,
) -> ShadowValidationResult:
    """Run layered validation against only the already-materialized sealed payload."""
    blockers: list[str] = []
    warnings: list[str] = list(dynamic_risks.warnings)
    if not contract.integrity_valid():
        blockers.append("EXECUTION_CONTRACT_HASH_MISMATCH")
    if not baseline.integrity_valid():
        blockers.append("REFACTOR_BASELINE_HASH_MISMATCH")
    valid_payload, payload_blockers = verify_sealed_payload(sealed_payload)
    if not valid_payload:
        blockers.extend(payload_blockers)
    if materialization.status != "shadow_materialized":
        blockers.append("SHADOW_NOT_MATERIALIZED")
        blockers.extend(materialization.blockers)
    if provenance.status != "shadow_provenance_pass":
        blockers.append("SHADOW_PROVENANCE_NOT_PROVEN")
        blockers.extend(provenance.blockers)
    blockers.extend(dynamic_risks.blockers)

    shadow_root = Path(materialization.shadow_root).resolve()
    structural_blockers, checked_files = _validate_structural(
        shadow_root, contract, sealed_payload
    )
    blockers.extend(structural_blockers)
    structural_status = "STRUCTURAL_PASS" if not structural_blockers else "STRUCTURAL_FAIL"

    api_before = tuple(sorted(_baseline_api_names(contract, baseline)))
    api_after, api_blockers = _shadow_api_manifest(shadow_root, contract)
    blockers.extend(api_blockers)
    if set(api_before) == set(api_after):
        api_status = "API_EQUIVALENT"
    else:
        api_status = "API_MISMATCH"
        blockers.append("PUBLIC_API_EQUIVALENCE_FAILED")

    graph, topology_blockers = _dependency_topology(shadow_root, contract, sealed_payload)
    blockers.extend(topology_blockers)
    topology_status = "TOPOLOGY_PASS" if not topology_blockers else "TOPOLOGY_FAIL"

    runtime_blockers = _runtime_validation(shadow_root, contract)
    blockers.extend(runtime_blockers)
    runtime_status = "RUNTIME_PASS" if not runtime_blockers else "RUNTIME_FAIL"

    behavior = _behavior_validation(shadow_root, contract, baseline)
    behavior_status = behavior.execution_status
    if behavior.collection_status in {"COLLECTION_FAILED", "NO_TESTS_COLLECTED"}:
        warnings.append(behavior.collection_status)
    if behavior.execution_status == "BEHAVIOR_FAILED":
        blockers.append("SHADOW_BEHAVIOR_VALIDATION_FAILED")
    if behavior.execution_status == "BEHAVIOR_NOT_RUN":
        warnings.append("SHADOW_BEHAVIOR_VALIDATION_NOT_RUN")
    if behavior.baseline_comparison == "BASELINE_PASS_SHADOW_FAIL":
        blockers.append("BEHAVIOR_REGRESSION_FROM_BASELINE")

    unique_blockers = tuple(sorted(set(blockers)))
    unique_warnings = tuple(sorted(set(warnings)))
    status = "shadow_validation_pass" if not unique_blockers else "shadow_validation_failed"
    return ShadowValidationResult(
        schema_version=SCHEMA_VERSION,
        feature_id=SHADOW_VALIDATION_FEATURE_ID,
        status=status,
        shadow_root=str(shadow_root),
        payload_hash=sealed_payload.payload_hash,
        structural_status=structural_status,
        api_status=api_status,
        topology_status=topology_status,
        provenance_status=provenance.status,
        runtime_status=runtime_status,
        behavior_status=behavior_status,
        checked_files=tuple(checked_files),
        api_before=api_before,
        api_after=tuple(sorted(api_after)),
        dependency_graph=graph,
        behavior=behavior,
        blockers=unique_blockers,
        warnings=unique_warnings,
        source_mutation_enabled=False,
    )


def _validate_structural(
    shadow_root: Path,
    contract: WorkbenchExecutionContract,
    payload: WorkbenchSealedPayload,
) -> tuple[list[str], list[str]]:
    blockers: list[str] = []
    checked: list[str] = []
    project_root = Path(contract.active_project_root).resolve()
    for item in payload.files:
        destination = Path(item.destination_path).resolve()
        try:
            relative = destination.relative_to(project_root)
        except ValueError:
            blockers.append(f"SHADOW_STRUCTURAL_DESTINATION_OUTSIDE_PROJECT:{item.relative_path}")
            continue
        path = (shadow_root / relative).resolve()
        checked.append(str(path))
        if not path.is_file():
            blockers.append(f"SHADOW_FILE_MISSING:{item.relative_path}")
            continue
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != item.content_hash:
            blockers.append(f"SHADOW_FILE_HASH_MISMATCH:{item.relative_path}")
            continue
        source = ""
        try:
            source = raw.decode("utf-8")
            ast.parse(source, type_comments=True)
            compile(source, str(path), "exec")
        except (UnicodeDecodeError, SyntaxError) as exc:
            blockers.append(f"SHADOW_FILE_COMPILE_FAILED:{item.relative_path}:{exc}")
        physical_lines = len(source.splitlines())
        if not 100 < physical_lines < 500:
            blockers.append(f"SHADOW_MODULE_SIZE_VIOLATION:{item.relative_path}:{physical_lines}")
    package_root = _common_package_root([Path(item) for item in checked], shadow_root)
    if package_root and not compileall.compile_dir(
        str(package_root), quiet=2, force=True, legacy=True
    ):
        blockers.append("SHADOW_COMPILEALL_FAILED")
    return blockers, checked


def _baseline_api_names(
    contract: WorkbenchExecutionContract,
    baseline: RefactorBaseline,
) -> set[str]:
    api = contract.public_api_preservation_map
    explicit = api.get("before", [])
    if explicit:
        return {str(item) for item in explicit}
    manifest = baseline.public_api_manifest
    names = manifest.get("public_api", manifest.get("names", []))
    return {str(item) for item in names if str(item)}


def _shadow_api_manifest(
    shadow_root: Path,
    contract: WorkbenchExecutionContract,
) -> tuple[set[str], list[str]]:
    project_root = Path(contract.active_project_root).resolve()
    target = Path(contract.target_file).resolve()
    try:
        relative = target.relative_to(project_root)
    except ValueError:
        return set(), ["SHADOW_API_TARGET_OUTSIDE_PROJECT"]
    path = shadow_root / relative
    if not path.is_file():
        return set(), ["SHADOW_API_FACADE_MISSING"]
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), type_comments=True)
    except (OSError, SyntaxError) as exc:
        return set(), [f"SHADOW_API_PARSE_FAILED:{exc}"]
    explicit_all = _literal_all(tree)
    if explicit_all is not None:
        return set(explicit_all), []
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not node.name.startswith("_"):
                names.add(node.name)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                local = alias.asname or alias.name
                if not local.startswith("_") and local != "*":
                    names.add(local)
    return names, ["SHADOW_API_INFERRED_WITHOUT_LITERAL_ALL"]


def _literal_all(tree: ast.Module) -> list[str] | None:
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        if not any(isinstance(target, ast.Name) and target.id == "__all__" for target in targets):
            continue
        value = node.value
        if not isinstance(value, (ast.List, ast.Tuple)):
            return None
        names: list[str] = []
        for item in value.elts:
            if not isinstance(item, ast.Constant) or not isinstance(item.value, str):
                return None
            names.append(item.value)
        return names
    return None


def _dependency_topology(
    shadow_root: Path,
    contract: WorkbenchExecutionContract,
    payload: WorkbenchSealedPayload,
) -> tuple[dict[str, tuple[str, ...]], list[str]]:
    graph: dict[str, set[str]] = {}
    module_stems = {Path(item.relative_path).stem for item in payload.files}
    blockers: list[str] = []
    for item in payload.files:
        path = _shadow_file_path(
            shadow_root, Path(contract.active_project_root).resolve(), payload, item.relative_path
        )
        if path is None or not path.is_file():
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), type_comments=True)
        deps: set[str] = set()
        for node in tree.body:
            if isinstance(node, ast.ImportFrom) and node.level == 1 and node.module:
                stem = node.module.split(".")[0]
                if stem in module_stems:
                    deps.add(stem)
        graph[Path(item.relative_path).stem] = deps
    blockers.extend(_cycle_blockers(graph))
    frozen_graph = {key: tuple(sorted(value)) for key, value in sorted(graph.items())}
    return frozen_graph, blockers


def _shadow_file_path(
    shadow_root: Path,
    project_root: Path,
    payload: WorkbenchSealedPayload,
    relative_name: str,
) -> Path | None:
    for item in payload.files:
        if item.relative_path != relative_name:
            continue
        try:
            relative = Path(item.destination_path).resolve().relative_to(project_root)
        except ValueError:
            return None
        return (shadow_root / relative).resolve()
    return None


def _cycle_blockers(graph: dict[str, set[str]]) -> list[str]:
    visiting: set[str] = set()
    visited: set[str] = set()
    blockers: list[str] = []

    def visit(node: str, trail: tuple[str, ...]) -> None:
        if node in visiting:
            blockers.append("SHADOW_IMPORT_CYCLE:" + "->".join((*trail, node)))
            return
        if node in visited:
            return
        visiting.add(node)
        for dep in graph.get(node, set()):
            visit(dep, (*trail, node))
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        visit(node, ())
    return blockers


def _runtime_validation(shadow_root: Path, contract: WorkbenchExecutionContract) -> list[str]:
    blockers: list[str] = []
    for target in contract.runtime_validation_targets:
        path = Path(target).resolve()
        try:
            relative = path.relative_to(Path(contract.active_project_root).resolve())
        except ValueError:
            blockers.append(f"RUNTIME_TARGET_OUTSIDE_PROJECT:{target}")
            continue
        shadow_path = shadow_root / relative
        if shadow_path.suffix == ".py" and not shadow_path.is_file():
            blockers.append(f"RUNTIME_TARGET_MISSING:{relative.as_posix()}")
    return blockers


def _behavior_validation(
    shadow_root: Path,
    contract: WorkbenchExecutionContract,
    baseline: RefactorBaseline,
) -> ShadowBehaviorEvidence:
    targets = [str(Path(item).resolve()) for item in contract.test_targets if Path(item).exists()]
    shadow_targets: list[str] = []
    project_root = Path(contract.active_project_root).resolve()
    for target in targets:
        try:
            relative = Path(target).resolve().relative_to(project_root)
        except ValueError:
            continue
        candidate = shadow_root / relative
        if candidate.exists():
            shadow_targets.append(str(candidate))
    if not shadow_targets:
        return ShadowBehaviorEvidence(
            collection_status="NO_TEST_TARGETS",
            collection_exit_code=None,
            collected_test_lines=(),
            execution_status="BEHAVIOR_NOT_RUN",
            execution_exit_code=None,
            output_hash="",
            baseline_comparison="BASELINE_EVIDENCE_INSUFFICIENT",
            stdout_excerpt="",
            stderr_excerpt="",
        )
    collect = _run_pytest(project_root, shadow_root, ["--collect-only", "-q", *shadow_targets])
    collected_lines = tuple(line for line in collect.stdout.splitlines() if "::" in line)
    if collect.returncode == 5:
        collection_status = "NO_TESTS_COLLECTED"
    elif collect.returncode == 0:
        collection_status = "COLLECTION_PASS"
    else:
        collection_status = "COLLECTION_FAILED"
    if collection_status != "COLLECTION_PASS":
        return ShadowBehaviorEvidence(
            collection_status=collection_status,
            collection_exit_code=collect.returncode,
            collected_test_lines=collected_lines,
            execution_status="BEHAVIOR_NOT_RUN",
            execution_exit_code=None,
            output_hash="",
            baseline_comparison="BASELINE_EVIDENCE_INSUFFICIENT",
            stdout_excerpt=_excerpt(collect.stdout),
            stderr_excerpt=_excerpt(collect.stderr),
        )
    run = _run_pytest(project_root, shadow_root, ["-q", *shadow_targets])
    output_hash = hashlib.sha256((run.stdout + "\n" + run.stderr).encode("utf-8")).hexdigest()
    execution_status = "BEHAVIOR_PASS" if run.returncode == 0 else "BEHAVIOR_FAILED"
    baseline_state = baseline.behavior_baseline.status
    if baseline_state in {"passed", "behavior_baseline_pass", "BEHAVIOR_BASELINE_PASS", "BEHAVIOR_VALIDATED_PASS"}:
        comparison = "BASELINE_PASS_SHADOW_PASS" if run.returncode == 0 else "BASELINE_PASS_SHADOW_FAIL"
    else:
        comparison = "BASELINE_EVIDENCE_INSUFFICIENT"
    return ShadowBehaviorEvidence(
        collection_status=collection_status,
        collection_exit_code=collect.returncode,
        collected_test_lines=collected_lines,
        execution_status=execution_status,
        execution_exit_code=run.returncode,
        output_hash=output_hash,
        baseline_comparison=comparison,
        stdout_excerpt=_excerpt(run.stdout),
        stderr_excerpt=_excerpt(run.stderr),
    )


def _run_pytest(
    project_root: Path,
    shadow_root: Path,
    args: list[str],
) -> subprocess.CompletedProcess[str]:
    argv = ["-m", "pytest", *args]
    try:
        return run_project_python_governed(
            project_root,
            argv,
            cwd=shadow_root,
            timeout=_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        return subprocess.CompletedProcess(
            argv, 124, exc.stdout or "", exc.stderr or "timeout"
        )


def _common_package_root(paths: list[Path], fallback: Path) -> Path:
    if not paths:
        return fallback
    parents = [path.parent.resolve() for path in paths]
    common = parents[0]
    while not all(_is_relative_to(path, common) for path in parents):
        if common.parent == common:
            return fallback
        common = common.parent
    return common


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _excerpt(text: str, limit: int = 4000) -> str:
    return text if len(text) <= limit else text[:limit] + "\n...<truncated>"
