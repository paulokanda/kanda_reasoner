"""Semantic record contract for Brick Wall Q15 path authority."""
from __future__ import annotations

from typing import Mapping, Sequence

__all__: list[str] = []

REQUIRED_FAMILIES = {
    "SUPPORT_ROOT",
    "TRANSIENT_GARBAGE_ROOT",
    "PREVIEW",
    "SHADOW",
    "ERROR_MEMORY",
    "FREEZE_MEMORY",
}
ALLOWED_BASES = {
    "ACTIVE_PROJECT_ROOT",
    "PROJECT_SUPPORT_ROOT",
    "TRANSIENT_GARBAGE_ROOT",
}
ALLOWED_LIFETIMES = {
    "CANONICAL_SOURCE",
    "DURABLE_PROJECT_SUPPORT",
    "TRANSIENT_GARBAGE",
}
RECORD_FIELDS = (
    "path_basis",
    "primary_box",
    "paths_required",
    "no_path_evidence",
    "canonical_base_root_owner",
    "canonical_support_root_facade",
    "canonical_transient_root_facade",
    "path_families",
    "duplicate_authorities",
    "hardcoded_project_paths",
    "unresolved_adapters",
    "blockers",
    "tests",
    "decision",
    "may_proceed_to_final_precode",
    "may_begin_coding",
    "may_write_source",
)
FAMILY_FIELDS = (
    "family",
    "artifact_class",
    "owner_module",
    "public_facade",
    "contract_symbol",
    "base_root_class",
    "delegates_to",
    "bounded_child",
    "consumers",
    "compatibility_adapter",
    "adapter_scope",
    "create_write_owner",
    "lifetime",
    "containment_verified",
    "tests",
    "blocked_duplicate_formulas",
)


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _text_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def _fields(record: Mapping[str, object], fields: Sequence[str]) -> None:
    missing = [field for field in fields if field not in record]
    if missing:
        raise AssertionError("missing fields: " + ", ".join(missing))


def _validate_family(family: Mapping[str, object]) -> None:
    _fields(family, FAMILY_FIELDS)
    text_fields = (
        "family",
        "artifact_class",
        "owner_module",
        "public_facade",
        "contract_symbol",
        "base_root_class",
        "delegates_to",
        "bounded_child",
        "create_write_owner",
        "lifetime",
    )
    for field in text_fields:
        if not _nonempty(family[field]):
            raise AssertionError(f"empty family field: {field}")
    if family["base_root_class"] not in ALLOWED_BASES:
        raise AssertionError("invalid base-root class")
    if family["lifetime"] not in ALLOWED_LIFETIMES:
        raise AssertionError("invalid lifetime")
    if not _text_list(family["consumers"]):
        raise AssertionError("family consumers missing")
    if not _text_list(family["tests"]):
        raise AssertionError("family tests missing")
    if not _text_list(family["blocked_duplicate_formulas"]):
        raise AssertionError("blocked duplicate formulas missing")
    if family["containment_verified"] is not True:
        raise AssertionError("family containment unresolved")
    adapter = family["compatibility_adapter"]
    if not isinstance(adapter, bool):
        raise AssertionError("compatibility_adapter must be boolean")
    if adapter and not _nonempty(family["adapter_scope"]):
        raise AssertionError("compatibility adapter scope missing")
    if not adapter and family["adapter_scope"] not in (None, "", "N/A"):
        raise AssertionError("non-adapter carries adapter scope")
    if family["family"] == "PREVIEW":
        if family["base_root_class"] != "PROJECT_SUPPORT_ROOT":
            raise AssertionError("Preview base root is not durable support")
        if family["lifetime"] != "DURABLE_PROJECT_SUPPORT":
            raise AssertionError("Preview lifetime is not durable")
    if family["family"] == "SHADOW":
        if family["base_root_class"] != "TRANSIENT_GARBAGE_ROOT":
            raise AssertionError("Shadow base root is not transient")
        if family["lifetime"] != "TRANSIENT_GARBAGE":
            raise AssertionError("Shadow lifetime is not transient")
    if family["family"] in {"ERROR_MEMORY", "FREEZE_MEMORY"}:
        if family["base_root_class"] != "PROJECT_SUPPORT_ROOT":
            raise AssertionError("durable memory escaped Project Support")
        if family["lifetime"] != "DURABLE_PROJECT_SUPPORT":
            raise AssertionError("durable memory lifetime is invalid")


def validate_record(record: Mapping[str, object]) -> None:
    _fields(record, RECORD_FIELDS)
    if not _nonempty(record["path_basis"]) or not _nonempty(record["primary_box"]):
        raise AssertionError("path basis or primary box missing")
    if not isinstance(record["paths_required"], bool):
        raise AssertionError("paths_required must be boolean")
    for field, message in (
        ("blockers", "path-authority blockers remain"),
        ("duplicate_authorities", "duplicate path authorities remain"),
        ("hardcoded_project_paths", "hardcoded project paths remain"),
        ("unresolved_adapters", "compatibility adapters remain unresolved"),
    ):
        if _text_list(record[field]):
            raise AssertionError(message)
    if record["may_begin_coding"] is not False:
        raise AssertionError("Q15 cannot authorize coding")
    if record["may_write_source"] is not False:
        raise AssertionError("Q15 cannot authorize source writing")
    if record["paths_required"] is False:
        if not _text_list(record["no_path_evidence"]):
            raise AssertionError("not-applicable path evidence missing")
        if record["path_families"] not in ([], None):
            raise AssertionError("not-applicable record carries path families")
        if record["decision"] != "NOT_APPLICABLE":
            raise AssertionError("not-applicable decision invalid")
        if record["may_proceed_to_final_precode"] is not True:
            raise AssertionError("not-applicable record cannot progress")
        return
    root_fields = (
        "canonical_base_root_owner",
        "canonical_support_root_facade",
        "canonical_transient_root_facade",
    )
    for field in root_fields:
        if not _nonempty(record[field]):
            raise AssertionError(f"empty root authority field: {field}")
    if record["decision"] != "COMPLETE":
        raise AssertionError("required path-authority decision is not COMPLETE")
    if record["may_proceed_to_final_precode"] is not True:
        raise AssertionError("final pre-code progression missing")
    families = record["path_families"]
    if not isinstance(families, list) or not families:
        raise AssertionError("path-family set missing")
    names: list[str] = []
    owners: dict[str, tuple[str, str]] = {}
    for family in families:
        if not isinstance(family, Mapping):
            raise AssertionError("path family is not a mapping")
        _validate_family(family)
        name = str(family["family"])
        names.append(name)
        owner = (str(family["owner_module"]), str(family["public_facade"]))
        if name in owners and owners[name] != owner:
            raise AssertionError("path family has competing public owners")
        owners[name] = owner
    if len(names) != len(set(names)):
        raise AssertionError("duplicate path-family record")
    missing = REQUIRED_FAMILIES.difference(names)
    if missing:
        raise AssertionError("required path families missing: " + ", ".join(sorted(missing)))
    if not _text_list(record["tests"]):
        raise AssertionError("record tests missing")


def build_family(
    name: str,
    module: str,
    facade: str,
    base: str,
    delegate: str,
    child: str,
    lifetime: str,
    *,
    adapter: bool = False,
) -> dict[str, object]:
    return {
        "family": name,
        "artifact_class": name,
        "owner_module": module,
        "public_facade": facade,
        "contract_symbol": facade,
        "base_root_class": base,
        "delegates_to": delegate,
        "bounded_child": child,
        "consumers": ["current governed caller"],
        "compatibility_adapter": adapter,
        "adapter_scope": "legacy or generated-path hint normalization" if adapter else "N/A",
        "create_write_owner": module,
        "lifetime": lifetime,
        "containment_verified": True,
        "tests": ["Q15 focused path-authority matrix"],
        "blocked_duplicate_formulas": ["hardcoded suffix join", "independent root formula"],
    }


def valid_required_record() -> dict[str, object]:
    families = [
        build_family(
            "SUPPORT_ROOT",
            "kanda_reasoner_app.project_support_boundary",
            "canonical_project_support_root",
            "ACTIVE_PROJECT_ROOT",
            "active_project_root",
            "<project>_show_project_to_AI",
            "DURABLE_PROJECT_SUPPORT",
        ),
        build_family(
            "TRANSIENT_GARBAGE_ROOT",
            "kanda_reasoner_app.project_support_boundary",
            "canonical_transient_garbage_root",
            "ACTIVE_PROJECT_ROOT",
            "active_project_root",
            "<project>_delete_after_daily_work",
            "TRANSIENT_GARBAGE",
        ),
        build_family(
            "PREVIEW",
            "workbench_project_support_paths",
            "preview_runs_root",
            "PROJECT_SUPPORT_ROOT",
            "canonical_project_support_root",
            "large_file_refactor_workbench/preview",
            "DURABLE_PROJECT_SUPPORT",
        ),
        build_family(
            "SHADOW",
            "workbench_project_support_paths",
            "shadow_runs_root",
            "TRANSIENT_GARBAGE_ROOT",
            "canonical_transient_garbage_root",
            "large_file_refactor_shadow",
            "TRANSIENT_GARBAGE",
        ),
        build_family(
            "ERROR_MEMORY",
            "kanda_reasoner_app.error_memory.paths",
            "resolve_project_error_memory_root",
            "PROJECT_SUPPORT_ROOT",
            "show_project_to_ai_root_from_hint",
            "project_error_memory",
            "DURABLE_PROJECT_SUPPORT",
            adapter=True,
        ),
        build_family(
            "FREEZE_MEMORY",
            "kanda_reasoner_app.project_analysis_evidence_paths",
            "analysis_project_freeze_after_update_dir",
            "PROJECT_SUPPORT_ROOT",
            "show_project_to_ai_root_from_hint",
            "project_freeze_after_update",
            "DURABLE_PROJECT_SUPPORT",
            adapter=True,
        ),
    ]
    return {
        "path_basis": "Current exact source and public facade audit",
        "primary_box": "Prompt library governance",
        "paths_required": True,
        "no_path_evidence": [],
        "canonical_base_root_owner": "kanda_reasoner_app.project_support_boundary",
        "canonical_support_root_facade": "canonical_project_support_root",
        "canonical_transient_root_facade": "canonical_transient_garbage_root",
        "path_families": families,
        "duplicate_authorities": [],
        "hardcoded_project_paths": [],
        "unresolved_adapters": [],
        "blockers": [],
        "tests": ["Q15 canonical and negative path-authority cases"],
        "decision": "COMPLETE",
        "may_proceed_to_final_precode": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }


def valid_not_applicable_record() -> dict[str, object]:
    record = valid_required_record()
    record.update(
        paths_required=False,
        no_path_evidence=["No path derivation, use, or artifact placement is involved"],
        canonical_base_root_owner="N/A",
        canonical_support_root_facade="N/A",
        canonical_transient_root_facade="N/A",
        path_families=[],
        decision="NOT_APPLICABLE",
    )
    return record
