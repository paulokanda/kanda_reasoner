# project-path: kanda_reasoner_app/reasoner_symbol_atlas/_main_helper_mapper_helper_selection.py
"""Private helper-selection logic for Project Symbol Atlas main/helper mapping."""

from __future__ import annotations

from pathlib import Path

from ._main_helper_mapper_contract import (
    _HELPER_SUFFIXES,
    _MainHelperDecisionLike,
    _STATUS_NO_HELPERS_FOUND,
    _STATUS_READY,
)
from .output_policy import is_active_atlas_path
from .schemas import ProjectModuleRecord, normalize_project_atlas_text


def _record_is_active(record: ProjectModuleRecord) -> bool:
    """Support record is active behavior.

    Parameters
    ----------
    record : ProjectModuleRecord
        The record value.

    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """

    return is_active_atlas_path(record.path)


def _active_records(
    records: tuple[ProjectModuleRecord, ...],
) -> tuple[ProjectModuleRecord, ...]:
    """Support active records behavior.

    Parameters
    ----------
    records : tuple[ProjectModuleRecord, ...]
        The record values.

    Returns
    -------
    tuple[ProjectModuleRecord, ...]
        The tuple of values.
    """

    return tuple(record for record in records if _record_is_active(record))


def _target_is_helper_like(record: ProjectModuleRecord) -> bool:
    """Support target is helper like behavior.

    Parameters
    ----------
    record : ProjectModuleRecord
        The record value.

    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """

    if _record_is_private_helper(record):
        return True
    return _has_helper_suffix(record)


def _record_is_low_signal_support_file(record: ProjectModuleRecord) -> bool:
    """Support record is low signal support file behavior.

    Parameters
    ----------
    record : ProjectModuleRecord
        The record value.

    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """

    stem = _module_stem(record).lower()
    low_signal_tokens = (
        "smoke",
        "probe",
        "static_context",
        "diagnostic",
        "status",
        "validation",
    )
    return any(token in stem for token in low_signal_tokens)


def _target_role(record: ProjectModuleRecord) -> str:
    """Support target role behavior.

    Parameters
    ----------
    record : ProjectModuleRecord
        The record value.

    Returns
    -------
    str
        The string result.
    """

    if _record_is_private_helper(record):
        return "helper"
    if _has_helper_suffix(record):
        return "helper"
    if record.owner_role in {"facade", "compatibility_facade"}:
        return "facade"
    return "main"


def _select_main_record(
    target_record: ProjectModuleRecord,
    modules: tuple[ProjectModuleRecord, ...],
) -> ProjectModuleRecord:
    """Select the main owner for a target without inventing weak owners.

    Facade classification is a review signal, not enough evidence to move
    ownership to a loosely related smoke/probe file. Only helper-shaped targets
    should search for a separate main owner.
    """

    if not _target_is_helper_like(target_record):
        return target_record
    candidates = _main_candidates_for_helper(target_record, modules)
    if candidates:
        return candidates[0]
    return target_record


def _main_candidates_for_helper(
    helper_record: ProjectModuleRecord,
    modules: tuple[ProjectModuleRecord, ...],
) -> tuple[ProjectModuleRecord, ...]:
    """Support main candidates for helper behavior.

    Parameters
    ----------
    helper_record : ProjectModuleRecord
        The helper record value.
    modules : tuple[ProjectModuleRecord, ...]
        The modules value.

    Returns
    -------
    tuple[ProjectModuleRecord, ...]
        The tuple of values.
    """

    helper_stem = _module_stem(helper_record)
    base_stem = _strip_helper_suffix(helper_stem)
    candidates: list[tuple[int, ProjectModuleRecord]] = []
    for record in modules:
        if (
            record.path == helper_record.path
            or record.is_test_file
            or not _record_is_active(record)
        ):
            continue
        if _record_is_low_signal_support_file(record):
            continue
        score = 0
        record_stem = _module_stem(record)
        if record_stem == base_stem:
            score += 60
        if _module_imports(record, helper_record):
            score += 40
        if record.owner_role == "canonical_owner":
            score += 10
        if score > 0:
            candidates.append((score, record))
    return tuple(
        record
        for _score, record in sorted(
            candidates, key=lambda item: (-item[0], item[1].path)
        )
    )


def _select_helper_records(
    target_record: ProjectModuleRecord,
    main_record: ProjectModuleRecord,
    modules: tuple[ProjectModuleRecord, ...],
    max_helpers: int,
) -> tuple[ProjectModuleRecord, ...]:
    """Support select helper records behavior.

    Parameters
    ----------
    target_record : ProjectModuleRecord
        The target record value.
    main_record : ProjectModuleRecord
        The main record value.
    modules : tuple[ProjectModuleRecord, ...]
        The modules value.
    max_helpers : int
        The max helpers value.

    Returns
    -------
    tuple[ProjectModuleRecord, ...]
        The tuple of values.
    """

    scored: list[tuple[int, ProjectModuleRecord]] = []
    for record in modules:
        if (
            record.path == main_record.path
            or record.is_test_file
            or not _record_is_active(record)
        ):
            continue
        score = _helper_score(main_record, record)
        if (
            record.path == target_record.path
            and _target_role(target_record) == "helper"
        ):
            score += 100
        if score > 0:
            scored.append((score, record))
    ordered = [
        record
        for _score, record in sorted(scored, key=lambda item: (-item[0], item[1].path))
    ]
    return tuple(ordered[: max(0, int(max_helpers))])


def _helper_score(
    main_record: ProjectModuleRecord, candidate: ProjectModuleRecord
) -> int:
    """Support helper score behavior.

    Parameters
    ----------
    main_record : ProjectModuleRecord
        The main record value.
    candidate : ProjectModuleRecord
        The candidate value.

    Returns
    -------
    int
        The integer result.
    """

    score = 0
    main_stem = _module_stem(main_record)
    candidate_stem = _module_stem(candidate)
    if candidate_stem.startswith(main_stem + "_") and _has_helper_suffix(candidate):
        score += 80
    if _module_imports(main_record, candidate):
        score += 50
    if _module_imports(candidate, main_record):
        score += 15
    if score > 0 and _record_is_private_helper(candidate):
        score += 10
    return score


def _module_imports(source: ProjectModuleRecord, target: ProjectModuleRecord) -> bool:
    """Support module imports behavior.

    Parameters
    ----------
    source : ProjectModuleRecord
        The source value.
    target : ProjectModuleRecord
        The target value.

    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """

    target_module = normalize_project_atlas_text(target.module)
    if not target_module:
        return False
    imports = {normalize_project_atlas_text(item) for item in source.imports}
    if target_module in imports:
        return True
    return any(
        item.endswith("." + target_module.rsplit(".", 1)[-1]) for item in imports
    )


def _module_stem(record: ProjectModuleRecord) -> str:
    """Support module stem behavior.

    Parameters
    ----------
    record : ProjectModuleRecord
        The record value.

    Returns
    -------
    str
        The string result.
    """

    path = Path(record.path)
    if path.name == "__init__.py":
        return path.parent.name
    return path.stem


def _strip_helper_suffix(stem: str) -> str:
    """Support strip helper suffix behavior.

    Parameters
    ----------
    stem : str
        The stem value.

    Returns
    -------
    str
        The string result.
    """
    for suffix in sorted(_HELPER_SUFFIXES, key=len, reverse=True):
        if stem.endswith(suffix):
            return stem[: -len(suffix)]
    return stem


def _has_helper_suffix(record: ProjectModuleRecord) -> bool:
    """Support has helper suffix behavior.

    Parameters
    ----------
    record : ProjectModuleRecord
        The record value.

    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    stem = _module_stem(record)
    return any(stem.endswith(suffix) for suffix in _HELPER_SUFFIXES)


def _record_is_private_helper(record: ProjectModuleRecord) -> bool:
    """Support record is private helper behavior.

    Parameters
    ----------
    record : ProjectModuleRecord
        The record value.

    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """

    return record.owner_role == "private_helper" or "private_helper" in tuple(
        record.evidence
    )


def _public_helper_warnings(
    helper_records: tuple[ProjectModuleRecord, ...],
) -> tuple[str, ...]:
    """Support public helper warnings behavior.

    Parameters
    ----------
    helper_records : tuple[ProjectModuleRecord, ...]
        The helper records value.

    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """

    warnings: list[str] = []
    for record in helper_records:
        public_symbols = [symbol.name for symbol in record.symbols if symbol.is_public]
        if public_symbols and not _record_is_private_helper(record):
            warnings.append(
                "Helper exposes public symbols: "
                + record.path
                + " -> "
                + ", ".join(sorted(public_symbols)[:8])
            )
    return tuple(warnings)


def _related_tests_to_run(
    modules: tuple[ProjectModuleRecord, ...],
    main_record: ProjectModuleRecord,
    helper_records: tuple[ProjectModuleRecord, ...],
) -> tuple[str, ...]:
    """Support related tests to run behavior.

    Parameters
    ----------
    modules : tuple[ProjectModuleRecord, ...]
        The modules value.
    main_record : ProjectModuleRecord
        The main record value.
    helper_records : tuple[ProjectModuleRecord, ...]
        The helper records value.

    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """

    return tuple()


def _decision_status(
    target_record: ProjectModuleRecord,
    main_record: ProjectModuleRecord,
    helper_records: tuple[ProjectModuleRecord, ...],
    merge_status: str,
) -> tuple[str, str, tuple[str, ...]]:
    """Support decision status behavior.

    Parameters
    ----------
    target_record : ProjectModuleRecord
        The target record value.
    main_record : ProjectModuleRecord
        The main record value.
    helper_records : tuple[ProjectModuleRecord, ...]
        The helper records value.
    merge_status : str
        The merge status value.

    Returns
    -------
    tuple[str, str, tuple[str, ...]]
        The tuple of values.
    """
    evidence = ["Evidence merge status: " + merge_status]
    if target_record.path != main_record.path:
        evidence.append(
            "Target is helper-like; main owner selected from related files."
        )
    if helper_records:
        evidence.append("Helper candidates found: " + str(len(helper_records)))
        return _STATUS_READY, "medium", tuple(evidence)
    evidence.append("No helper candidates were found for the selected main file.")
    return (
        _STATUS_NO_HELPERS_FOUND,
        "medium",
        tuple(evidence),
    )


def _format_decision_summary(decision: _MainHelperDecisionLike) -> str:
    """Support format decision summary behavior.

    Parameters
    ----------
    decision : ProjectSymbolAtlasMainHelperDecision
        The decision value.

    Returns
    -------
    str
        The string result.
    """

    return (
        f"Main/helper map status={decision.status}; "
        f"target_role={decision.target_role}; main={decision.main_path}; "
        f"helper_count={len(decision.helper_paths)}; confidence={decision.confidence}"
    )
