# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/brain_region_mapping/contract.py
"""Public contract for the Brain Region Mapping box.

This pure data box maps stable brain-region identifiers to stable tab
identifiers and analogy text. It deliberately avoids PySide6, QWebEngine,
main-window, tab-widget, and registry imports so it can be tested independently.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from ._mapping_data import RAW_BRAIN_REGION_TARGETS

__all__ = [
    "BRAIN_REGION_MAPPING_BOX_ID",
    "BRAIN_REGION_MAPPING_CONTRACT_VERSION",
    "BrainRegionMappingSummary",
    "BrainRegionTarget",
    "get_brain_region_mapping_summary",
    "is_known_brain_region",
    "list_brain_region_ids",
    "list_brain_region_targets",
    "resolve_brain_region",
]

BRAIN_REGION_MAPPING_BOX_ID: Final[str] = "brain_region_mapping"
BRAIN_REGION_MAPPING_CONTRACT_VERSION: Final[str] = "0.2"


@dataclass(frozen=True)
class BrainRegionTarget:
    """Resolved mapping from a brain structure to an app tab.

    Attributes:
        region_id: Stable machine-readable brain region identifier.
        region_name: Human-readable neuroanatomical region name.
        target_tab_id: Stable target tab identifier from the tab registry.
        target_tab_label: Human-visible tab label expected for the target tab.
        analogy_title: Short explanation title connecting anatomy to app logic.
        analogy_text: Longer explanation for the Remember Box.
        tooltip_text: Compact hover tooltip text.
        category: Navigation category used by the future fancy index.
        is_known: Whether the region_id was found in the canonical mapping.
    """

    region_id: str
    region_name: str
    target_tab_id: str
    target_tab_label: str
    analogy_title: str
    analogy_text: str
    tooltip_text: str
    category: str
    is_known: bool = True


@dataclass(frozen=True)
class BrainRegionMappingSummary:
    """Describe the public boundary of the Brain Region Mapping box.

    Attributes:
        box_id: Stable Box Architecture identifier for this data box.
        contract_version: Public contract version.
        responsibility: Single responsibility statement for the box.
        owner_paths: Project-relative paths owned by this box.
        public_functions: Functions exposed by the public contract.
        target_count: Number of known brain-region mappings.
        implementation_state: Current implementation state.
    """

    box_id: str
    contract_version: str
    responsibility: str
    owner_paths: tuple[str, ...]
    public_functions: tuple[str, ...]
    target_count: int
    implementation_state: str


def _build_targets() -> tuple[BrainRegionTarget, ...]:
    """Build immutable target records from private raw mapping data.

    Returns:
        Tuple of immutable BrainRegionTarget records.
    """

    return tuple(BrainRegionTarget(**item) for item in RAW_BRAIN_REGION_TARGETS)


_TARGETS: Final[tuple[BrainRegionTarget, ...]] = _build_targets()
_TARGETS_BY_ID: Final[dict[str, BrainRegionTarget]] = {
    target.region_id: target for target in _TARGETS
}


def list_brain_region_targets() -> tuple[BrainRegionTarget, ...]:
    """Return all known brain-region targets in canonical display order.

    Returns:
        Immutable tuple of known brain-region mappings.
    """

    return _TARGETS


def list_brain_region_ids() -> tuple[str, ...]:
    """Return all known brain-region identifiers in canonical order.

    Returns:
        Immutable tuple of region identifiers.
    """

    return tuple(target.region_id for target in _TARGETS)


def is_known_brain_region(region_id: str) -> bool:
    """Return whether a brain-region identifier exists in the mapping.

    Args:
        region_id: Candidate machine-readable brain region identifier.

    Returns:
        True when the region is present in the canonical mapping.
    """

    return region_id in _TARGETS_BY_ID


def resolve_brain_region(region_id: str) -> BrainRegionTarget:
    """Resolve a brain-region identifier to a target tab and analogy.

    Unknown regions return a safe fallback target instead of raising. This keeps
    the future Brain Navigator optional and disable-safe.

    Args:
        region_id: Machine-readable brain region identifier received from the
            future JavaScript/Qt bridge.

    Returns:
        Known mapping target or a safe unknown-region target.
    """

    if region_id in _TARGETS_BY_ID:
        return _TARGETS_BY_ID[region_id]

    safe_region_id = str(region_id or "unknown_region")
    return BrainRegionTarget(
        region_id=safe_region_id,
        region_name="Unknown brain region",
        target_tab_id="",
        target_tab_label="No target tab",
        analogy_title="No mapping available",
        analogy_text=(
            "This brain region is not mapped yet. The Brain Navigator can show "
            "this safe fallback without changing tabs or crashing the app."
        ),
        tooltip_text="Unknown brain region",
        category="Unmapped",
        is_known=False,
    )


def get_brain_region_mapping_summary() -> BrainRegionMappingSummary:
    """Return the Brain Region Mapping public contract summary.

    Returns:
        Immutable summary of the mapping box boundary for tests and future
        registry integration.
    """

    return BrainRegionMappingSummary(
        box_id=BRAIN_REGION_MAPPING_BOX_ID,
        contract_version=BRAIN_REGION_MAPPING_CONTRACT_VERSION,
        responsibility=(
            "Map stable brain-region identifiers to stable tab identifiers, "
            "human labels, tooltip text, and Remember Box analogy text."
        ),
        owner_paths=(
            "kanda_reasoner_app/reasoner_tools_gui_shell/brain_region_mapping/",
        ),
        public_functions=(
            "list_brain_region_targets",
            "list_brain_region_ids",
            "is_known_brain_region",
            "resolve_brain_region",
            "get_brain_region_mapping_summary",
        ),
        target_count=len(_TARGETS),
        implementation_state="pure_mapping_box",
    )
