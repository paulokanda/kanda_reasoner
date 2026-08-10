# project-path: kanda_reasoner_app/engineering_diagnostics/grouping.py
"""Deterministic, read-only grouping for diagnostic findings."""

from __future__ import annotations

import hashlib
from pathlib import PurePosixPath
from types import MappingProxyType
from typing import Iterable, Mapping

from .bom_adapter import BOM_PRODUCER_ID
from .collectors import (
    ARCHITECTURE_PRODUCER_ID,
    RUFF_PRODUCER_ID,
    SHADOW_PRODUCER_ID,
)
from .fingerprinting import canonical_json, normalize_relative_path
from .grouping_models import DiagnosticGroupRecord
from .models import DiagnosticFindingRecord, DiagnosticRunRecord
from .shadow_relational_grouping import build_shadow_relational_diagnostic_groups

__all__ = [
    "build_deterministic_diagnostic_groups",
    "index_diagnostic_groups",
    "primary_diagnostic_group",
]

_RECIPE_PRECEDENCE = {
    "bom.rule_file.v1": 10,
    "ruff.rule_file.v1": 20,
    "ruff.rule_structural_parent.v1": 30,
    "architecture.rule_boundary.v1": 40,
    "architecture.rule_owner_box.v1": 50,
    "ruff.rule_package.v1": 60,
    "shadow.relational_component.v1": 70,
}


def _text(value: object) -> str:
    return str(value or "").strip()


def _group_id(run: DiagnosticRunRecord, recipe_id: str, key: tuple[str, ...]) -> str:
    payload = canonical_json(
        {
            "group_contract": "engineering_diagnostics.grouping.v1",
            "project_id": run.project_id,
            "producer_id": run.producer_id,
            "scope_fingerprint": run.scope_fingerprint,
            "producer_version": run.producer_version,
            "configuration_fingerprint": run.configuration_fingerprint,
            "recipe_id": recipe_id,
            "key": key,
        }
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _package_path(relative_path: str) -> str:
    parent = PurePosixPath(normalize_relative_path(relative_path)).parent.as_posix()
    return "<project-root>" if parent in ("", ".") else parent


def _structural_parent(symbol_id: str) -> str:
    symbol = _text(symbol_id)
    if not symbol:
        return ""
    return symbol.rsplit(".", 1)[0] if "." in symbol else symbol


def _recipe_candidates(
    run: DiagnosticRunRecord,
    finding: DiagnosticFindingRecord,
) -> tuple[tuple[str, tuple[str, ...], str, str, Mapping[str, object]], ...]:
    code = _text(finding.code)
    path = normalize_relative_path(finding.relative_path)
    candidates: list[
        tuple[str, tuple[str, ...], str, str, Mapping[str, object]]
    ] = []
    if run.producer_id == BOM_PRODUCER_ID:
        candidates.append(
            (
                "bom.rule_file.v1",
                (code, path),
                code + " in " + path,
                "high",
                {"rule": code, "relative_path": path},
            )
        )
    elif run.producer_id == RUFF_PRODUCER_ID:
        candidates.append(
            (
                "ruff.rule_file.v1",
                (code, path),
                code + " in " + path,
                "high",
                {"rule": code, "relative_path": path},
            )
        )
        parent = _structural_parent(finding.symbol_id)
        if parent:
            candidates.append(
                (
                    "ruff.rule_structural_parent.v1",
                    (code, path, parent),
                    code + " under " + path + "::" + parent,
                    "high",
                    {
                        "rule": code,
                        "relative_path": path,
                        "structural_parent": parent,
                    },
                )
            )
        package = _package_path(path)
        candidates.append(
            (
                "ruff.rule_package.v1",
                (code, package),
                code + " across package " + package,
                "medium",
                {"rule": code, "package": package},
            )
        )
    elif run.producer_id == ARCHITECTURE_PRODUCER_ID:
        boundary = _text(finding.evidence.get("boundary"))
        owner = _text(finding.evidence.get("owner"))
        if boundary:
            candidates.append(
                (
                    "architecture.rule_boundary.v1",
                    (code, boundary),
                    code + " at boundary " + boundary,
                    "high",
                    {"rule": code, "boundary": boundary},
                )
            )
        if owner:
            candidates.append(
                (
                    "architecture.rule_owner_box.v1",
                    (code, owner),
                    code + " in owner Box " + owner,
                    "medium",
                    {"rule": code, "owner_box": owner},
                )
            )
    return tuple(candidates)


def build_deterministic_diagnostic_groups(
    run: DiagnosticRunRecord,
    findings: tuple[DiagnosticFindingRecord, ...],
) -> tuple[DiagnosticGroupRecord, ...]:
    """Create multi-member diagnostic groups without writing Project state."""
    if run.producer_id == SHADOW_PRODUCER_ID:
        return build_shadow_relational_diagnostic_groups(run, findings)
    buckets: dict[
        tuple[str, tuple[str, ...]],
        dict[str, object],
    ] = {}
    for finding in findings:
        if finding.run_id != run.run_id:
            raise ValueError("GROUPING_FINDING_RUN_ID_MISMATCH")
        for recipe_id, key, label, confidence, evidence in _recipe_candidates(
            run,
            finding,
        ):
            bucket = buckets.setdefault(
                (recipe_id, key),
                {
                    "label": label,
                    "confidence": confidence,
                    "evidence": dict(evidence),
                    "members": [],
                },
            )
            members = bucket["members"]
            if not isinstance(members, list):
                raise RuntimeError("GROUPING_BUCKET_MEMBER_TYPE_INVALID")
            members.append(finding.issue_fingerprint)

    groups: list[DiagnosticGroupRecord] = []
    for (recipe_id, key), bucket in sorted(
        buckets.items(),
        key=lambda item: (
            _RECIPE_PRECEDENCE.get(item[0][0], 999),
            item[0][0],
            item[0][1],
        ),
    ):
        members = tuple(sorted(set(bucket["members"])))
        if len(members) < 2:
            continue
        evidence = dict(bucket["evidence"])
        evidence.update(
            {
                "member_count": len(members),
                "grouping_mode": "deterministic_same_rule",
                "root_cause_claimed": False,
            }
        )
        groups.append(
            DiagnosticGroupRecord(
                group_id=_group_id(run, recipe_id, key),
                project_id=run.project_id,
                producer_id=run.producer_id,
                scope_fingerprint=run.scope_fingerprint,
                kind="DETERMINISTIC",
                recipe_id=recipe_id,
                label=str(bucket["label"]),
                confidence=str(bucket["confidence"]),
                member_issue_fingerprints=members,
                evidence=MappingProxyType(evidence),
            )
        )
    return tuple(groups)


def _group_sort_key(group: DiagnosticGroupRecord) -> tuple[object, ...]:
    return (
        0 if group.kind == "MANUAL" else 1,
        0 if group.confidence == "high" else 1,
        _RECIPE_PRECEDENCE.get(group.recipe_id, 999),
        -len(group.member_issue_fingerprints),
        group.group_id,
    )


def index_diagnostic_groups(
    groups: Iterable[DiagnosticGroupRecord],
) -> Mapping[str, tuple[DiagnosticGroupRecord, ...]]:
    """Return an immutable issue-fingerprint to groups lookup."""
    indexed: dict[str, list[DiagnosticGroupRecord]] = {}
    for group in groups:
        for fingerprint in group.member_issue_fingerprints:
            indexed.setdefault(fingerprint, []).append(group)
    normalized = {
        fingerprint: tuple(sorted(values, key=_group_sort_key))
        for fingerprint, values in indexed.items()
    }
    return MappingProxyType(normalized)


def primary_diagnostic_group(
    groups: Iterable[DiagnosticGroupRecord],
) -> DiagnosticGroupRecord | None:
    """Choose a display group without changing or hiding other memberships."""
    ordered = tuple(sorted(tuple(groups), key=_group_sort_key))
    return ordered[0] if ordered else None
