# project-path: kanda_reasoner_app/reasoner_symbol_atlas/logic_placement_advisor_helpers_private.py
"""Private heuristics for the Project Symbol Atlas logic placement advisor."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .schemas import (
    ProjectModuleRecord,
    ProjectSymbol,
    normalize_project_atlas_text,
)

__all__: list[str] = []


def _coerce_project_root(project_root: str | Path) -> Path:
    root = Path(project_root).expanduser().resolve(strict=False)
    if not root.exists():
        raise FileNotFoundError("Project root does not exist: " + str(project_root))
    if not root.is_dir():
        raise NotADirectoryError("Project root is not a directory: " + str(project_root))
    return root


def _normalize_token_text(value: str) -> str:
    return normalize_project_atlas_text(value).lower().replace("-", "_").replace(" ", "_")


def _infer_owner_box_from_text(text: str) -> str:
    lowered = _normalize_token_text(text)
    rules = (
        ("reasoner_symbol_atlas", ("atlas", "find_symbol", "owner_map", "pre_patch", "existing_code")),
        (
            "project_analysis_evidence",
            (
                "tab_4",
                "tab4",
                "collect_project_structure",
                "json_complete",
                "project_analysis_evidence",
                "tab_5",
                "tab5",
                "json_splitted",
                "split_structure",
            ),
        ),
        ("gui_shell", ("gui", "tab", "panel", "button", "widget", "window", "pyside", "display")),
        ("safety_suite_cli", ("cli", "command_line", "command", "argparse", "list_tools")),
        ("source_hygiene", ("bom", "shadow", "source_hygiene", "facade_fix", "encoding")),
        (
            "engineering_safety",
            ("risk_radar", "risk_change", "crash_triage", "refactor_playbook", "engineering_safety"),
        ),
        ("governance_automation", ("release_notes", "push_plan", "on_every_push", "governance_automation")),
        ("stack_compatibility", ("stack", "dependency", "compatibility", "cuda", "pyside6", "numpy")),
        ("reliability_guidance", ("api_contract", "property_test", "reliability")),
        ("governance", ("canon", "governance", "freeze")),
        ("tests", ("test", "tests")),
    )
    for owner_box, tokens in rules:
        if any(token in lowered for token in tokens):
            return owner_box
    return "unknown"


def _infer_owner_box_from_path(path_value: str) -> str:
    lowered = str(Path(path_value)).replace("\\", "/").lower()
    path_rules = (
        ("reasoner_symbol_atlas", ("reasoner_symbol_atlas/",)),
        ("project_analysis_evidence", ("project_analysis_evidence", "project_analysis_evidence_paths")),
        ("gui_shell", ("reasoner_tools_gui", "gui_shell", "_gui", "/gui/")),
        ("safety_suite_cli", ("safety_suite_cli",)),
        ("source_hygiene", ("source_hygiene",)),
        ("engineering_safety", ("engineering_safety",)),
        ("governance_automation", ("governance_automation",)),
        ("stack_compatibility", ("stack_compatibility",)),
        ("reliability_guidance", ("reliability_guidance",)),
        ("tests", ("tests/",)),
    )
    for owner_box, tokens in path_rules:
        if any(token in lowered for token in tokens):
            return owner_box
    return "unknown"


def _find_target_record(
    project_root: Path,
    modules: Iterable[ProjectModuleRecord],
    target_path: str,
) -> ProjectModuleRecord | None:
    if not target_path:
        return None
    target = Path(target_path)
    if target.is_absolute():
        try:
            target_key = str(target.resolve(strict=False).relative_to(project_root))
            target_key = target_key.replace("\\", "/").lower()
        except ValueError:
            target_key = str(target.resolve(strict=False)).replace("\\", "/").lower()
    else:
        target_key = str(target).replace("\\", "/").lower()
    for record in modules:
        record_key = str(Path(record.path)).replace("\\", "/").lower()
        if record_key == target_key or record_key.endswith("/" + target_key):
            return record
    return None


def _find_symbol_matches(
    symbols: Iterable[ProjectSymbol], symbol_name: str
) -> tuple[ProjectSymbol, ...]:
    name = normalize_project_atlas_text(symbol_name)
    if not name:
        return tuple()
    lowered = name.lower()
    exact = [symbol for symbol in symbols if symbol.name.lower() == lowered]
    if exact:
        return tuple(exact)
    return tuple(symbol for symbol in symbols if lowered in symbol.name.lower())


def _record_for_preferred_symbol(
    modules: Iterable[ProjectModuleRecord],
    matches: tuple[ProjectSymbol, ...],
) -> ProjectModuleRecord | None:
    if not matches:
        return None
    records_by_path = {record.path: record for record in modules}
    preferred_roles = (
        "canonical_owner",
        "private_helper",
        "facade",
        "compatibility_facade",
        "ambiguous_owner",
    )
    for role in preferred_roles:
        for symbol in matches:
            if symbol.owner_role == role and symbol.path in records_by_path:
                return records_by_path[symbol.path]
    for symbol in matches:
        if symbol.path in records_by_path:
            return records_by_path[symbol.path]
    return None


def _choose_recommended_box(
    task_box: str,
    target_record: ProjectModuleRecord | None,
    symbol_record: ProjectModuleRecord | None,
) -> str:
    if task_box != "unknown":
        return task_box
    if target_record is not None:
        path_box = _infer_owner_box_from_path(target_record.path)
        if path_box != "unknown":
            return path_box
    if symbol_record is not None:
        path_box = _infer_owner_box_from_path(symbol_record.path)
        if path_box != "unknown":
            return path_box
    return "unknown"


def _choose_primary_record(
    modules: Iterable[ProjectModuleRecord],
    target_record: ProjectModuleRecord | None,
    symbol_record: ProjectModuleRecord | None,
    recommended_box: str,
) -> ProjectModuleRecord | None:
    if target_record is not None:
        return target_record
    if symbol_record is not None:
        return symbol_record
    candidates = [
        record for record in modules if _infer_owner_box_from_path(record.path) == recommended_box
    ]
    for role in (
        "canonical_owner",
        "private_helper",
        "facade",
        "compatibility_facade",
        "unknown",
    ):
        for record in candidates:
            if record.owner_role == role:
                return record
    return candidates[0] if candidates else None


def _candidate_paths_for_box(
    modules: Iterable[ProjectModuleRecord],
    owner_box: str,
    primary_path: str,
) -> tuple[str, ...]:
    paths: list[str] = []
    for record in modules:
        if record.path == primary_path:
            continue
        if _infer_owner_box_from_path(record.path) == owner_box:
            paths.append(record.path)
    return tuple(paths[:8])


def _tests_to_run_for_owner_box(owner_box: str, primary_path: str) -> tuple[str, ...]:
    commands = [
        "python kanda_reasoner_app\\manage_architecture\\manage_architecture.py --root <PROJECT_ROOT> --validate",
        "python kanda_reasoner_app\\manage_workflows\\manage_workflows.py --root <PROJECT_ROOT> --validate",
    ]
    if primary_path:
        commands.insert(0, "python -m py_compile " + primary_path)
    return tuple(commands)
