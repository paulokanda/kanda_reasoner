# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/grimp_topology_fitness_adapter.py
"""Grimp topology fitness adapter for baseline and Preview import graphs."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Iterable

from .advanced_quality_evidence_models import (
    FindingLocation,
    FindingSeverity,
    RawEvidenceReference,
    build_normalized_finding,
)
from .advanced_quality_review_contract import AnalysisExecutionStatus
from .analyzer_adapter_contract import (
    AdapterEvidenceBundle,
    AdapterInputPair,
    build_finding_deltas,
    validate_adapter_postconditions,
    validate_adapter_preconditions,
)
from .analyzer_process_runtime import (
    BoundedProcessRequest,
    CancellationToken,
    ProcessExecutionEvidence,
    run_bounded_process,
)
from .analyzer_specific_delta_strategies import (
    GraphTopologyDelta,
    build_graph_topology_deltas,
)
from .workbench_project_support_paths import (
    analyzer_cache_root_blockers,
    analyzer_engine_cache_root,
)

__all__ = [
    "GRIMP_FITNESS_CHARACTERISTIC",
    "GrimpAdapterOptions",
    "GrimpGraphEvidence",
    "GrimpTopologyReviewResult",
    "run_grimp_topology_review",
]

GRIMP_FITNESS_CHARACTERISTIC = "dependency_topology_integrity"


@dataclass(frozen=True)
class GrimpGraphEvidence:
    """Hold one deterministic import graph snapshot from the adapter-side probe."""

    package_name: str
    modules: tuple[str, ...]
    edges: tuple[tuple[str, str], ...]
    cycle_breakers: tuple[tuple[str, str], ...]

    def to_dict(self) -> dict[str, object]:
        """Return stable JSON-ready graph evidence."""
        return {
            "package_name": self.package_name,
            "modules": list(self.modules),
            "edges": [list(item) for item in self.edges],
            "cycle_breakers": [list(item) for item in self.cycle_breakers],
        }


@dataclass(frozen=True)
class GrimpTopologyReviewResult:
    """Keep generic adapter evidence and graph-specific deltas side by side."""

    bundle: AdapterEvidenceBundle
    baseline_graph: GrimpGraphEvidence
    preview_graph: GrimpGraphEvidence
    topology_deltas: tuple[GraphTopologyDelta, ...]


class GrimpAdapterOptions:
    """Immutable command and cache policy for one Grimp topology review."""

    __slots__ = (
        "active_project_root",
        "analysis_key",
        "argv_prefix",
        "config_hash",
        "engine_version",
        "exclude_type_checking_imports",
        "package_name",
        "timeout_seconds",
    )

    def __init__(
        self,
        *,
        argv_prefix: Iterable[str],
        engine_version: str,
        package_name: str,
        active_project_root: str | Path,
        config_hash: str,
        analysis_key: str,
        exclude_type_checking_imports: bool = False,
        timeout_seconds: float = 60.0,
    ) -> None:
        prefix = tuple(str(item) for item in argv_prefix)
        if not prefix or not prefix[0].strip():
            raise ValueError("GRIMP_ARGV_PREFIX_EMPTY")
        if not str(engine_version or "").strip():
            raise ValueError("GRIMP_ENGINE_VERSION_EMPTY")
        if not str(package_name or "").strip():
            raise ValueError("GRIMP_PACKAGE_NAME_EMPTY")
        if not str(config_hash or "").strip():
            raise ValueError("GRIMP_CONFIG_HASH_EMPTY")
        if not str(analysis_key or "").strip():
            raise ValueError("GRIMP_ANALYSIS_KEY_EMPTY")
        if float(timeout_seconds) <= 0:
            raise ValueError("GRIMP_TIMEOUT_NOT_POSITIVE")
        self.argv_prefix = prefix
        self.engine_version = str(engine_version).strip()
        self.package_name = str(package_name).strip()
        self.active_project_root = str(
            Path(active_project_root).expanduser().resolve(strict=False)
        )
        self.config_hash = str(config_hash).strip()
        self.analysis_key = str(analysis_key).strip()
        self.exclude_type_checking_imports = bool(exclude_type_checking_imports)
        self.timeout_seconds = float(timeout_seconds)


def run_grimp_topology_review(
    inputs: AdapterInputPair,
    options: GrimpAdapterOptions,
    *,
    cancellation_token: CancellationToken | None = None,
    progress_callback=None,
) -> GrimpTopologyReviewResult:
    """Run Grimp probe on sealed baseline and Preview and compute graph deltas."""
    blockers = validate_adapter_preconditions(
        inputs,
        engine_id="grimp",
        engine_version=options.engine_version,
    )
    if blockers:
        raise ValueError("GRIMP_PRECONDITION_BLOCKED:" + "|".join(blockers))
    cache_root = analyzer_engine_cache_root(
        options.active_project_root,
        engine_id="grimp",
        engine_version=options.engine_version,
        config_hash=options.config_hash,
        analysis_key=options.analysis_key,
    )
    cache_blockers = analyzer_cache_root_blockers(
        options.active_project_root,
        cache_root,
    )
    if cache_blockers:
        raise ValueError("GRIMP_CACHE_OWNERSHIP_BLOCKED:" + "|".join(cache_blockers))
    cache_root.mkdir(parents=True, exist_ok=True)
    token = cancellation_token or CancellationToken()
    baseline_execution = _run_probe(
        "baseline",
        Path(inputs.baseline.root_path),
        cache_root / "baseline",
        options,
        token,
        progress_callback,
    )
    preview_execution = _run_probe(
        "preview",
        Path(inputs.preview.root_path),
        cache_root / "preview",
        options,
        token,
        progress_callback,
    )
    raw_evidence = {
        "grimp/baseline.json": baseline_execution.stdout_text.encode("utf-8"),
        "grimp/preview.json": preview_execution.stdout_text.encode("utf-8"),
    }
    diagnostics: list[str] = []
    baseline_graph = _parse_graph(
        baseline_execution,
        expected_package=options.package_name,
        diagnostics=diagnostics,
    )
    preview_graph = _parse_graph(
        preview_execution,
        expected_package=options.package_name,
        diagnostics=diagnostics,
    )
    baseline_findings = _graph_findings(
        baseline_graph,
        engine_version=options.engine_version,
        raw_path="grimp/baseline.json",
        raw_bytes=raw_evidence["grimp/baseline.json"],
    )
    preview_findings = _graph_findings(
        preview_graph,
        engine_version=options.engine_version,
        raw_path="grimp/preview.json",
        raw_bytes=raw_evidence["grimp/preview.json"],
    )
    post_blockers = validate_adapter_postconditions(inputs, raw_evidence=raw_evidence)
    if post_blockers:
        raise RuntimeError("GRIMP_POSTCONDITION_BLOCKED:" + "|".join(post_blockers))
    execution_status = _combined_status(
        baseline_execution,
        preview_execution,
        diagnostics,
    )
    bundle = AdapterEvidenceBundle(
        engine_id="grimp",
        engine_version=options.engine_version,
        protected_characteristic=GRIMP_FITNESS_CHARACTERISTIC,
        analysis_identity_hash=inputs.analysis_identity.identity_hash,
        execution_status=execution_status,
        baseline_execution=baseline_execution,
        preview_execution=preview_execution,
        baseline_findings=baseline_findings,
        preview_findings=preview_findings,
        deltas=build_finding_deltas(baseline_findings, preview_findings),
        raw_evidence=tuple(sorted(raw_evidence.items())),
        diagnostics=tuple(sorted(set(diagnostics))),
    )
    return GrimpTopologyReviewResult(
        bundle=bundle,
        baseline_graph=baseline_graph,
        preview_graph=preview_graph,
        topology_deltas=build_graph_topology_deltas(
            baseline_graph.edges,
            preview_graph.edges,
            baseline_cycle_breakers=baseline_graph.cycle_breakers,
            preview_cycle_breakers=preview_graph.cycle_breakers,
        ),
    )


def _run_probe(
    label: str,
    root: Path,
    cache_dir: Path,
    options: GrimpAdapterOptions,
    token: CancellationToken,
    progress_callback,
) -> ProcessExecutionEvidence:
    """Run one adapter-side Grimp JSON probe through the frozen bounded runtime."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    argv = [
        *options.argv_prefix,
        "--root",
        str(root),
        "--package",
        options.package_name,
        "--cache-dir",
        str(cache_dir),
    ]
    if options.exclude_type_checking_imports:
        argv.append("--exclude-type-checking-imports")
    return run_bounded_process(
        BoundedProcessRequest(
            engine_id="grimp_" + label,
            argv=tuple(argv),
            cwd=str(root),
            timeout_seconds=options.timeout_seconds,
        ),
        cancellation_token=token,
        progress_callback=progress_callback,
    )


def _parse_graph(
    execution: ProcessExecutionEvidence,
    *,
    expected_package: str,
    diagnostics: list[str],
) -> GrimpGraphEvidence:
    """Parse strict probe JSON without importing Grimp into the policy core."""
    if execution.status is not AnalysisExecutionStatus.SUCCEEDED:
        diagnostics.append(execution.engine_id + ":PROCESS_STATUS=" + execution.status.value)
        return _empty_graph(expected_package)
    try:
        payload = json.loads(execution.stdout_text)
    except json.JSONDecodeError as error:
        diagnostics.append(execution.engine_id + ":MALFORMED_JSON:" + str(error))
        return _empty_graph(expected_package)
    if not isinstance(payload, dict):
        diagnostics.append(execution.engine_id + ":GRAPH_JSON_ROOT_NOT_OBJECT")
        return _empty_graph(expected_package)
    package = str(payload.get("package_name") or "").strip()
    if package != expected_package:
        diagnostics.append(execution.engine_id + ":PACKAGE_IDENTITY_MISMATCH")
        return _empty_graph(expected_package)
    try:
        modules = tuple(sorted(_string_items(payload.get("modules"))))
        edges = tuple(sorted(_edge_items(payload.get("edges"))))
        cycle_breakers = tuple(sorted(_edge_items(payload.get("cycle_breakers"))))
    except ValueError as error:
        diagnostics.append(execution.engine_id + ":GRAPH_SCHEMA_INVALID:" + str(error))
        return _empty_graph(expected_package)
    return GrimpGraphEvidence(package, modules, edges, cycle_breakers)


def _graph_findings(
    graph: GrimpGraphEvidence,
    *,
    engine_version: str,
    raw_path: str,
    raw_bytes: bytes,
) -> tuple:
    """Normalize graph edges and cycle-breaker candidates as visible evidence."""
    reference = RawEvidenceReference(
        engine_id="grimp",
        relative_path=raw_path,
        sha256=hashlib.sha256(raw_bytes).hexdigest(),
        byte_size=len(raw_bytes),
    )
    findings = []
    for importer, imported in graph.edges:
        findings.append(
            build_normalized_finding(
                engine_id="grimp",
                engine_version=engine_version,
                rule_id="GRIMP_IMPORT_EDGE",
                normalized_relative_path=importer.replace(".", "/") + ".py",
                symbol_identity=importer + "->" + imported,
                normalized_message_signature="direct import edge",
                severity=FindingSeverity.INFO,
                location=FindingLocation(),
                raw_evidence_reference=reference,
                metadata=(("imported", imported),),
            )
        )
    for importer, imported in graph.cycle_breakers:
        findings.append(
            build_normalized_finding(
                engine_id="grimp",
                engine_version=engine_version,
                rule_id="GRIMP_CYCLE_BREAKER_CANDIDATE",
                normalized_relative_path=importer.replace(".", "/") + ".py",
                symbol_identity=importer + "->" + imported,
                normalized_message_signature="cycle breaker candidate",
                severity=FindingSeverity.WARNING,
                location=FindingLocation(),
                raw_evidence_reference=reference,
                metadata=(("imported", imported),),
            )
        )
    return tuple(sorted(findings, key=lambda item: item.semantic_key))


def _string_items(value: object) -> tuple[str, ...]:
    """Return validated nonempty string sequence from one graph JSON field."""
    if not isinstance(value, list):
        raise ValueError("GRAPH_STRING_LIST_REQUIRED")
    result = []
    for item in value:
        text = str(item or "").strip()
        if not text:
            raise ValueError("GRAPH_STRING_ITEM_EMPTY")
        result.append(text)
    return tuple(result)


def _edge_items(value: object) -> tuple[tuple[str, str], ...]:
    """Return validated directed edges from list-of-object probe output."""
    if not isinstance(value, list):
        raise ValueError("GRAPH_EDGE_LIST_REQUIRED")
    result: list[tuple[str, str]] = []
    for item in value:
        if not isinstance(item, dict):
            raise ValueError("GRAPH_EDGE_OBJECT_REQUIRED")
        importer = str(item.get("importer") or "").strip()
        imported = str(item.get("imported") or "").strip()
        if not importer or not imported:
            raise ValueError("GRAPH_EDGE_ENDPOINT_EMPTY")
        result.append((importer, imported))
    return tuple(result)


def _empty_graph(package_name: str) -> GrimpGraphEvidence:
    """Return explicit empty evidence for failed or malformed graph execution."""
    return GrimpGraphEvidence(package_name, (), (), ())


def _combined_status(
    baseline: ProcessExecutionEvidence,
    preview: ProcessExecutionEvidence,
    diagnostics: list[str],
) -> AnalysisExecutionStatus:
    """Combine process and parser evidence without synthetic success."""
    statuses = (baseline.status, preview.status)
    if any(status is AnalysisExecutionStatus.TIMED_OUT for status in statuses):
        return AnalysisExecutionStatus.TIMED_OUT
    if any(status is AnalysisExecutionStatus.CANCELLED for status in statuses):
        return AnalysisExecutionStatus.CANCELLED
    if any(status is not AnalysisExecutionStatus.SUCCEEDED for status in statuses):
        return AnalysisExecutionStatus.FAILED
    if diagnostics:
        return AnalysisExecutionStatus.FAILED
    return AnalysisExecutionStatus.SUCCEEDED
