# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/griffe_api_fitness_adapter.py
"""Griffe fitness adapter for public Python API preservation evidence."""
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
from .analyzer_machine_output import load_machine_output_as_stdout, prepare_machine_output_path
from .griffe_public_surface import child_public_override, griffe_public_state
from .analyzer_process_runtime import (
    BoundedProcessRequest,
    CancellationToken,
    ProcessExecutionEvidence,
    run_bounded_process,
)

__all__ = [
    "GRIFFE_FITNESS_CHARACTERISTIC",
    "GriffeAdapterOptions",
    "run_griffe_api_fitness_review",
]

GRIFFE_FITNESS_CHARACTERISTIC = "public_contract_preservation"
_MISSING_DEFAULT = "<KANDA_MISSING_DEFAULT>"


@dataclass(frozen=True)
class _Parameter:
    name: str
    kind: str
    default: str
    annotation: str


@dataclass(frozen=True)
class _ApiSymbol:
    path: str
    kind: str
    public: bool
    parameters: tuple[_Parameter, ...]
    returns: str
    alias_target: str


class GriffeAdapterOptions:
    """Immutable command policy for Griffe baseline/Preview API snapshots."""

    __slots__ = (
        "argv_prefix",
        "engine_version",
        "package_name",
        "extra_dump_args",
        "timeout_seconds",
    )

    def __init__(
        self,
        *,
        argv_prefix: Iterable[str],
        engine_version: str,
        package_name: str,
        extra_dump_args: Iterable[str] = (),
        timeout_seconds: float = 60.0,
    ) -> None:
        prefix = tuple(str(item) for item in argv_prefix)
        if not prefix or not prefix[0].strip():
            raise ValueError("GRIFFE_ARGV_PREFIX_EMPTY")
        if not str(engine_version or "").strip():
            raise ValueError("GRIFFE_ENGINE_VERSION_EMPTY")
        if not str(package_name or "").strip():
            raise ValueError("GRIFFE_PACKAGE_NAME_EMPTY")
        if float(timeout_seconds) <= 0:
            raise ValueError("GRIFFE_TIMEOUT_NOT_POSITIVE")
        self.argv_prefix = prefix
        self.engine_version = str(engine_version).strip()
        self.package_name = str(package_name).strip()
        self.extra_dump_args = tuple(str(item) for item in extra_dump_args)
        self.timeout_seconds = float(timeout_seconds)


def run_griffe_api_fitness_review(
    inputs: AdapterInputPair,
    options: GriffeAdapterOptions,
    *,
    cancellation_token: CancellationToken | None = None,
    progress_callback=None,
) -> AdapterEvidenceBundle:
    """Dump baseline and Preview APIs and emit explicit public-contract breakages."""
    blockers = validate_adapter_preconditions(
        inputs,
        engine_id="griffe",
        engine_version=options.engine_version,
    )
    if blockers:
        raise ValueError("GRIFFE_PRECONDITION_BLOCKED:" + "|".join(blockers))
    token = cancellation_token or CancellationToken()
    baseline_execution = _run_dump(
        "baseline",
        Path(inputs.baseline.root_path),
        options,
        token,
        progress_callback,
    )
    preview_execution = _run_dump(
        "preview",
        Path(inputs.preview.root_path),
        options,
        token,
        progress_callback,
    )
    raw_evidence = {
        "griffe/baseline.json": baseline_execution.stdout_text.encode("utf-8"),
        "griffe/preview.json": preview_execution.stdout_text.encode("utf-8"),
    }
    diagnostics: list[str] = []
    baseline_model = _parse_api_model(
        baseline_execution,
        package_name=options.package_name,
        diagnostics=diagnostics,
    )
    preview_model = _parse_api_model(
        preview_execution,
        package_name=options.package_name,
        diagnostics=diagnostics,
    )
    preview_findings = _compare_models(
        baseline_model,
        preview_model,
        engine_version=options.engine_version,
        raw_bytes=raw_evidence["griffe/preview.json"],
        diagnostics=diagnostics,
    )
    if diagnostics:
        preview_findings = tuple(
            sorted(
                (*preview_findings, _uncertainty_finding(
                    options.engine_version,
                    raw_evidence["griffe/preview.json"],
                    diagnostics,
                )),
                key=lambda item: item.semantic_key,
            )
        )
    post_blockers = validate_adapter_postconditions(inputs, raw_evidence=raw_evidence)
    if post_blockers:
        raise RuntimeError("GRIFFE_POSTCONDITION_BLOCKED:" + "|".join(post_blockers))
    execution_status = _combined_status(
        baseline_execution,
        preview_execution,
        diagnostics,
    )
    return AdapterEvidenceBundle(
        engine_id="griffe",
        engine_version=options.engine_version,
        protected_characteristic=GRIFFE_FITNESS_CHARACTERISTIC,
        analysis_identity_hash=inputs.analysis_identity.identity_hash,
        execution_status=execution_status,
        baseline_execution=baseline_execution,
        preview_execution=preview_execution,
        baseline_findings=(),
        preview_findings=preview_findings,
        deltas=build_finding_deltas((), preview_findings),
        raw_evidence=tuple(sorted(raw_evidence.items())),
        diagnostics=tuple(sorted(set(diagnostics))),
    )


def _run_dump(
    label: str,
    root: Path,
    options: GriffeAdapterOptions,
    token: CancellationToken,
    progress_callback,
) -> ProcessExecutionEvidence:
    output_path = prepare_machine_output_path(root, "griffe", label, ".json")
    execution = run_bounded_process(
        BoundedProcessRequest(
            engine_id="griffe_" + label,
            argv=(
                *options.argv_prefix,
                "dump",
                options.package_name,
                "--search",
                str(root),
                "--no-inspection",
                "--output",
                str(output_path),
                *options.extra_dump_args,
            ),
            cwd=str(root),
            timeout_seconds=options.timeout_seconds,
        ),
        cancellation_token=token,
        progress_callback=progress_callback,
    )
    return load_machine_output_as_stdout(execution, output_path)



def _parse_api_model(
    execution: ProcessExecutionEvidence,
    *,
    package_name: str,
    diagnostics: list[str],
) -> dict[str, _ApiSymbol]:
    if execution.status is not AnalysisExecutionStatus.SUCCEEDED:
        diagnostics.append(
            execution.engine_id + ":PROCESS_STATUS=" + execution.status.value
        )
        return {}
    try:
        payload = json.loads(execution.stdout_text)
    except json.JSONDecodeError as error:
        diagnostics.append(execution.engine_id + ":MALFORMED_JSON:" + str(error))
        return {}
    root = payload.get(package_name) if isinstance(payload, dict) else None
    if root is None and isinstance(payload, dict) and _looks_like_object(payload):
        root = payload
    if not isinstance(root, dict):
        diagnostics.append(execution.engine_id + ":PACKAGE_ROOT_MISSING")
        return {}
    model: dict[str, _ApiSymbol] = {}
    _walk_object(root, package_name, model, diagnostics)
    return model


def _walk_object(
    node: dict,
    fallback_path: str,
    model: dict[str, _ApiSymbol],
    diagnostics: list[str],
    public_override: bool | None = None,
) -> None:
    name = str(node.get("name") or fallback_path.rsplit(".", 1)[-1]).strip()
    path = str(node.get("path") or fallback_path).strip()
    if not path:
        diagnostics.append("GRIFFE_OBJECT_PATH_EMPTY:" + fallback_path)
        return
    kind = _canonical_text(node.get("kind") or node.get("type") or "unknown")
    public = griffe_public_state(node, name, explicit_export=public_override)
    parameters = _parameters(node.get("parameters"), diagnostics, path)
    returns = _canonical_json(node.get("returns"))
    alias_target = _alias_target(node)
    model[path] = _ApiSymbol(
        path=path,
        kind=kind,
        public=public,
        parameters=parameters,
        returns=returns,
        alias_target=alias_target,
    )
    members = node.get("members")
    if members is None:
        return
    if isinstance(members, dict):
        iterable = members.items()
    elif isinstance(members, list):
        iterable = ((str(index), value) for index, value in enumerate(members))
    else:
        diagnostics.append("GRIFFE_MEMBERS_INVALID:" + path)
        return
    for member_name, child in iterable:
        if not isinstance(child, dict):
            diagnostics.append("GRIFFE_MEMBER_INVALID:" + path + "." + str(member_name))
            continue
        child_name = str(child.get("name") or member_name)
        _walk_object(
            child, path + "." + child_name, model, diagnostics,
            child_public_override(node, child_name),
        )


def _compare_models(
    baseline: dict[str, _ApiSymbol],
    preview: dict[str, _ApiSymbol],
    *,
    engine_version: str,
    raw_bytes: bytes,
    diagnostics: list[str],
) -> tuple:
    findings = []
    reference = RawEvidenceReference(
        engine_id="griffe",
        relative_path="griffe/preview.json",
        sha256=hashlib.sha256(raw_bytes).hexdigest(),
        byte_size=len(raw_bytes),
    )
    for path, old in sorted(baseline.items()):
        if not old.public:
            continue
        new = preview.get(path)
        if new is None:
            findings.append(_finding(
                engine_version, "GRIFFE_PUBLIC_SYMBOL_REMOVED", path,
                "public symbol removed", FindingSeverity.BLOCKER, reference,
            ))
            continue
        if not new.public:
            findings.append(_finding(
                engine_version, "GRIFFE_PUBLIC_EXPORT_REMOVED", path,
                "public export became private", FindingSeverity.BLOCKER, reference,
            ))
        if old.kind != new.kind:
            findings.append(_finding(
                engine_version, "GRIFFE_PUBLIC_KIND_CHANGED", path,
                "public symbol kind changed", FindingSeverity.BLOCKER, reference,
                (("baseline_kind", old.kind), ("preview_kind", new.kind)),
            ))
        if old.alias_target != new.alias_target and (old.alias_target or new.alias_target):
            findings.append(_finding(
                engine_version, "GRIFFE_ALIAS_TARGET_CHANGED", path,
                "public alias target changed", FindingSeverity.BLOCKER, reference,
                (("baseline_target", old.alias_target), ("preview_target", new.alias_target)),
            ))
        findings.extend(_parameter_breakages(old, new, engine_version, reference))
        if old.returns != new.returns:
            findings.append(_finding(
                engine_version, "GRIFFE_RETURN_ANNOTATION_CHANGED", path,
                "public return annotation changed", FindingSeverity.WARNING, reference,
                (("baseline_returns", old.returns), ("preview_returns", new.returns)),
            ))
    if not baseline:
        diagnostics.append("GRIFFE_BASELINE_API_MODEL_EMPTY")
    if not preview:
        diagnostics.append("GRIFFE_PREVIEW_API_MODEL_EMPTY")
    return tuple(sorted(findings, key=lambda item: item.semantic_key))


def _parameter_breakages(
    old: _ApiSymbol,
    new: _ApiSymbol,
    engine_version: str,
    reference: RawEvidenceReference,
) -> list:
    findings = []
    old_map = {item.name: item for item in old.parameters}
    new_map = {item.name: item for item in new.parameters}
    for name, parameter in old_map.items():
        candidate = new_map.get(name)
        if candidate is None:
            findings.append(_finding(
                engine_version, "GRIFFE_PARAMETER_REMOVED", old.path,
                "public parameter removed", FindingSeverity.BLOCKER, reference,
                (("parameter", name),),
            ))
            continue
        if parameter.kind != candidate.kind:
            findings.append(_finding(
                engine_version, "GRIFFE_PARAMETER_KIND_CHANGED", old.path,
                "public parameter kind changed", FindingSeverity.BLOCKER, reference,
                (("parameter", name),),
            ))
        if parameter.default != candidate.default:
            findings.append(_finding(
                engine_version, "GRIFFE_PARAMETER_DEFAULT_CHANGED", old.path,
                "public parameter default changed", FindingSeverity.WARNING, reference,
                (("parameter", name),),
            ))
    for name, parameter in new_map.items():
        if name not in old_map and parameter.default == _MISSING_DEFAULT:
            findings.append(_finding(
                engine_version, "GRIFFE_REQUIRED_PARAMETER_ADDED", old.path,
                "required public parameter added", FindingSeverity.BLOCKER, reference,
                (("parameter", name),),
            ))
    if tuple(item.name for item in old.parameters) != tuple(item.name for item in new.parameters):
        findings.append(_finding(
            engine_version, "GRIFFE_PARAMETER_ORDER_CHANGED", old.path,
            "public parameter order changed", FindingSeverity.WARNING, reference,
        ))
    return findings


def _finding(
    engine_version: str,
    rule_id: str,
    path: str,
    message: str,
    severity: FindingSeverity,
    reference: RawEvidenceReference,
    metadata: tuple[tuple[str, str], ...] = (),
):
    relative = path.replace(".", "/") + ".py"
    return build_normalized_finding(
        engine_id="griffe",
        engine_version=engine_version,
        rule_id=rule_id,
        normalized_relative_path=relative,
        symbol_identity=path,
        normalized_message_signature=message,
        severity=severity,
        location=FindingLocation(),
        raw_evidence_reference=reference,
        metadata=metadata,
    )


def _uncertainty_finding(engine_version: str, raw_bytes: bytes, diagnostics: list[str]):
    reference = RawEvidenceReference(
        engine_id="griffe",
        relative_path="griffe/preview.json",
        sha256=hashlib.sha256(raw_bytes).hexdigest(),
        byte_size=len(raw_bytes),
    )
    return _finding(
        engine_version,
        "GRIFFE_API_MODEL_UNCERTAIN",
        "griffe_api_model",
        "API model contains uncertainty diagnostics",
        FindingSeverity.WARNING,
        reference,
        (("diagnostic_count", str(len(set(diagnostics)))),),
    )


def _parameters(value, diagnostics: list[str], path: str) -> tuple[_Parameter, ...]:
    if value is None:
        return ()
    if isinstance(value, dict):
        items = list(value.values())
    elif isinstance(value, list):
        items = value
    else:
        diagnostics.append("GRIFFE_PARAMETERS_INVALID:" + path)
        return ()
    result: list[_Parameter] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            diagnostics.append("GRIFFE_PARAMETER_INVALID:" + path + ":" + str(index))
            continue
        name = str(item.get("name") or "").strip()
        if not name:
            diagnostics.append("GRIFFE_PARAMETER_NAME_EMPTY:" + path + ":" + str(index))
            continue
        default = _MISSING_DEFAULT if "default" not in item else _canonical_json(item.get("default"))
        result.append(_Parameter(
            name=name,
            kind=_canonical_text(item.get("kind") or "unknown"),
            default=default,
            annotation=_canonical_json(item.get("annotation")),
        ))
    return tuple(result)



def _alias_target(node: dict) -> str:
    for key in ("target_path", "target", "canonical_path"):
        value = node.get(key)
        if value not in (None, ""):
            return _canonical_text(value)
    return ""


def _canonical_text(value) -> str:
    if isinstance(value, str):
        return value.strip().lower()
    return _canonical_json(value).lower()


def _canonical_json(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _looks_like_object(payload: dict) -> bool:
    return any(key in payload for key in ("name", "kind", "members", "path"))


def _combined_status(
    baseline: ProcessExecutionEvidence,
    preview: ProcessExecutionEvidence,
    diagnostics: list[str],
) -> AnalysisExecutionStatus:
    statuses = {baseline.status, preview.status}
    if AnalysisExecutionStatus.CANCELLED in statuses:
        return AnalysisExecutionStatus.CANCELLED
    if AnalysisExecutionStatus.TIMED_OUT in statuses:
        return AnalysisExecutionStatus.TIMED_OUT
    if AnalysisExecutionStatus.FAILED in statuses:
        return AnalysisExecutionStatus.FAILED
    if diagnostics:
        return AnalysisExecutionStatus.FAILED
    return AnalysisExecutionStatus.SUCCEEDED
