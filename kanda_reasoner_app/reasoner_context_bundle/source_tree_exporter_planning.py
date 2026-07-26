# project-path: kanda_reasoner_app/reasoner_context_bundle/source_tree_exporter_planning.py
"""Archive grouping and part-name planning for source-tree export."""

from __future__ import annotations

import zipfile
from pathlib import Path

from .source_tree_exporter_archive_io import _write_zip
from .source_tree_exporter_shared import (
    _REBALANCE_LAST_PART_MIN_RATIO,
    _REBALANCE_PREVIOUS_PART_MIN_RATIO,
    _ZIP_OVERHEAD_ESTIMATE_BYTES,
)

def _estimate_record_size(record: dict[str, Any]) -> int:
    """Support estimate record size behavior.
    
    Parameters
    ----------
    record : dict[str, Any]
        The record value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    return int(record.get("size_bytes", 0)) + _ZIP_OVERHEAD_ESTIMATE_BYTES

def _candidate_zip_size(
    records: list[dict[str, Any]],
    temp_dir: Path,
    filename: str,
    *,
    compression: int = zipfile.ZIP_DEFLATED,
    compresslevel: int | None = 9,
) -> int:
    """Support candidate zip size behavior.
    
    Parameters
    ----------
    records : list[dict[str, Any]]
        The record values.
    temp_dir : Path
        The temp dir value.
    filename : str
        The file name.
    compression : int, optional
        The optional compression value.
    compresslevel : int | None, optional
        The optional compresslevel value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    candidate = temp_dir / filename
    if candidate.exists():
        candidate.unlink()
    _write_zip(candidate, records, compression=compression, compresslevel=compresslevel)
    return candidate.stat().st_size

def _single_record_fits(
    record: dict[str, Any],
    hard_cap: int,
    temp_dir: Path,
    *,
    compression: int = zipfile.ZIP_DEFLATED,
    compresslevel: int | None = 9,
) -> bool:
    """Support single record fits behavior.
    
    Parameters
    ----------
    record : dict[str, Any]
        The record value.
    hard_cap : int
        The hard cap value.
    temp_dir : Path
        The temp dir value.
    compression : int, optional
        The optional compression value.
    compresslevel : int | None, optional
        The optional compresslevel value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return (
        _candidate_zip_size(
            [record],
            temp_dir,
            "single_record_probe.zip",
            compression=compression,
            compresslevel=compresslevel,
        )
        <= hard_cap
    )

def _initial_groups(
    records: list[dict[str, Any]],
    hard_cap: int,
    planning_target: int,
    temp_dir: Path,
    *,
    compression: int = zipfile.ZIP_DEFLATED,
    compresslevel: int | None = 9,
) -> list[list[dict[str, Any]]]:
    """Support initial groups behavior.
    
    Parameters
    ----------
    records : list[dict[str, Any]]
        The record values.
    hard_cap : int
        The hard cap value.
    planning_target : int
        The planning target value.
    temp_dir : Path
        The temp dir value.
    compression : int, optional
        The optional compression value.
    compresslevel : int | None, optional
        The optional compresslevel value.
    
    Returns
    -------
    list[list[dict[str, Any]]]
        The list of values.
    """
    
    groups: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    current_estimate = 0
    for record in records:
        estimate = _estimate_record_size(record)
        if estimate > hard_cap and not _single_record_fits(
            record,
            hard_cap,
            temp_dir,
            compression=compression,
            compresslevel=compresslevel,
        ):
            raise ValueError(
                "A single project file cannot fit under the selected ZIP size cap: "
                + str(record.get("path"))
                + " ("
                + str(record.get("size_bytes", 0))
                + " bytes; cap "
                + str(hard_cap)
                + " bytes). Increase the radio-button ZIP size or exclude this file."
            )
        if current and current_estimate + estimate > planning_target:
            groups.append(current)
            current = []
            current_estimate = 0
        current.append(record)
        current_estimate += estimate
    if current:
        groups.append(current)
    return groups

def _enforce_group_caps(
    groups: list[list[dict[str, Any]]],
    hard_cap: int,
    temp_dir: Path,
    *,
    compression: int = zipfile.ZIP_DEFLATED,
    compresslevel: int | None = 9,
) -> list[list[dict[str, Any]]]:
    """Support enforce group caps behavior.
    
    Parameters
    ----------
    groups : list[list[dict[str, Any]]]
        The groups value.
    hard_cap : int
        The hard cap value.
    temp_dir : Path
        The temp dir value.
    compression : int, optional
        The optional compression value.
    compresslevel : int | None, optional
        The optional compresslevel value.
    
    Returns
    -------
    list[list[dict[str, Any]]]
        The list of values.
    """
    
    stable = False
    while not stable:
        stable = True
        new_groups: list[list[dict[str, Any]]] = []
        for group in groups:
            if not group:
                continue
            size = _candidate_zip_size(
                group,
                temp_dir,
                "cap_probe.zip",
                compression=compression,
                compresslevel=compresslevel,
            )
            if size <= hard_cap:
                new_groups.append(group)
                continue
            if len(group) == 1:
                record = group[0]
                raise ValueError(
                    "A single project file exceeds the selected ZIP hard cap after compression: "
                    + str(record.get("path"))
                    + " (cap "
                    + str(hard_cap)
                    + " bytes). Increase the radio-button ZIP size or exclude this file."
                )
            split_at = max(1, len(group) // 2)
            new_groups.append(group[:split_at])
            new_groups.append(group[split_at:])
            stable = False
        groups = new_groups
    return groups

def _rebalance_tiny_final_group(
    groups: list[list[dict[str, Any]]],
    hard_cap: int,
    temp_dir: Path,
    *,
    compression: int = zipfile.ZIP_DEFLATED,
    compresslevel: int | None = 9,
) -> list[list[dict[str, Any]]]:
    """Support rebalance tiny final group behavior.
    
    Parameters
    ----------
    groups : list[list[dict[str, Any]]]
        The groups value.
    hard_cap : int
        The hard cap value.
    temp_dir : Path
        The temp dir value.
    compression : int, optional
        The optional compression value.
    compresslevel : int | None, optional
        The optional compresslevel value.
    
    Returns
    -------
    list[list[dict[str, Any]]]
        The list of values.
    """
    
    if len(groups) < 2:
        return groups
    previous = list(groups[-2])
    final = list(groups[-1])
    final_size = _candidate_zip_size(
        final,
        temp_dir,
        "rebalance_final_probe.zip",
        compression=compression,
        compresslevel=compresslevel,
    )
    if final_size >= int(hard_cap * _REBALANCE_LAST_PART_MIN_RATIO):
        return groups
    while previous:
        candidate_move = previous[-1]
        candidate_previous = previous[:-1]
        candidate_final = [candidate_move] + final
        if not candidate_previous:
            break
        previous_size = _candidate_zip_size(
            candidate_previous,
            temp_dir,
            "rebalance_previous_probe.zip",
            compression=compression,
            compresslevel=compresslevel,
        )
        new_final_size = _candidate_zip_size(
            candidate_final,
            temp_dir,
            "rebalance_final_new_probe.zip",
            compression=compression,
            compresslevel=compresslevel,
        )
        if previous_size > hard_cap or new_final_size > hard_cap:
            break
        if previous_size < int(hard_cap * _REBALANCE_PREVIOUS_PART_MIN_RATIO):
            break
        previous = candidate_previous
        final = candidate_final
        final_size = new_final_size
        if final_size >= int(hard_cap * _REBALANCE_LAST_PART_MIN_RATIO):
            break
    groups[-2] = previous
    groups[-1] = final
    return groups

def _part_filename(slug: str, index: int, total: int) -> str:
    """Support part filename behavior.
    
    Parameters
    ----------
    slug : str
        The slug value.
    index : int
        The index value.
    total : int
        The total value.
    
    Returns
    -------
    str
        The string result.
    """
    
    width = max(2, len(str(total)))
    return (
        slug
        + "__source_archive_part"
        + str(index).zfill(width)
        + "_of_"
        + str(total).zfill(width)
        + ".zip"
    )

def _png_asset_part_filename(slug: str, index: int, total: int) -> str:
    """Support png asset part filename behavior.
    
    Parameters
    ----------
    slug : str
        The slug value.
    index : int
        The index value.
    total : int
        The total value.
    
    Returns
    -------
    str
        The string result.
    """
    
    width = max(2, len(str(total)))
    return (
        slug
        + "__png_assets_part"
        + str(index).zfill(width)
        + "_of_"
        + str(total).zfill(width)
        + ".zip"
    )
