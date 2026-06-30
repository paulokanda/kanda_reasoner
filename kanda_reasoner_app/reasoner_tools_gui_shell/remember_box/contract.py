# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/remember_box/contract.py
"""Public contract for the Remember Box scaffold.

The Remember Box is the future explanation-card view used by the Brain
Navigator. This scaffold is intentionally GUI-free: it builds immutable display
state only and does not import PySide6, tab navigation, main-window, or brain
rendering internals.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

__all__ = [
    "REMEMBER_BOX_ID",
    "REMEMBER_BOX_CONTRACT_VERSION",
    "RememberBoxState",
    "RememberBoxSummary",
    "build_remember_box_state",
    "clear_remember_box_state",
    "create_empty_remember_box_state",
    "get_remember_box_summary",
]

REMEMBER_BOX_ID: Final[str] = "remember_box"
REMEMBER_BOX_CONTRACT_VERSION: Final[str] = "0.1"
_PLACEHOLDER_TITLE: Final[str] = "Brain Navigator"
_PLACEHOLDER_TEXT: Final[str] = (
    "Hover or click a brain region to see how it maps to the app."
)


@dataclass(frozen=True)
class RememberBoxState:
    """Immutable display state for the future Remember Box widget.

    Attributes:
        region_id: Machine-readable brain region identifier, when selected.
        region_name: Human-readable brain structure name.
        target_tab_id: Stable tab ID associated with the selected region.
        target_tab_label: Human-visible target tab label.
        analogy_title: Short explanation title.
        analogy_text: Explanation text displayed in the card body.
        action_label: Label for the future Open Tool button.
        status: Machine-readable state such as ``placeholder`` or ``mapped``.
        is_placeholder: Whether this state is the empty/default card.
        can_open_target: Whether the future navigation controller may open a tab.
    """

    region_id: str
    region_name: str
    target_tab_id: str
    target_tab_label: str
    analogy_title: str
    analogy_text: str
    action_label: str
    status: str
    is_placeholder: bool
    can_open_target: bool


@dataclass(frozen=True)
class RememberBoxSummary:
    """Describe the public boundary of the Remember Box scaffold.

    Attributes:
        box_id: Stable Box Architecture identifier.
        contract_version: Public contract version.
        responsibility: Single responsibility statement for the box.
        owner_paths: Project-relative paths owned by this box.
        public_functions: Functions exposed by this public contract.
        forbidden_dependencies: Dependencies this scaffold must not import.
        implementation_state: Current scaffold state.
    """

    box_id: str
    contract_version: str
    responsibility: str
    owner_paths: tuple[str, ...]
    public_functions: tuple[str, ...]
    forbidden_dependencies: tuple[str, ...]
    implementation_state: str


def create_empty_remember_box_state() -> RememberBoxState:
    """Create the safe placeholder display state.

    Returns:
        Placeholder RememberBoxState used before a brain region is selected.
    """

    return RememberBoxState(
        region_id="",
        region_name="No brain region selected",
        target_tab_id="",
        target_tab_label="No target tab",
        analogy_title=_PLACEHOLDER_TITLE,
        analogy_text=_PLACEHOLDER_TEXT,
        action_label="Select a brain region",
        status="placeholder",
        is_placeholder=True,
        can_open_target=False,
    )


def clear_remember_box_state() -> RememberBoxState:
    """Return the safe placeholder state after clearing a selection.

    Returns:
        Placeholder RememberBoxState.
    """

    return create_empty_remember_box_state()


def build_remember_box_state(target: object | None) -> RememberBoxState:
    """Build display state from a brain-region target-like object.

    The function uses attribute access instead of importing the Brain Region
    Mapping box. This keeps the scaffold contract decoupled while accepting the
    same public data shape that mapping box returns.

    Args:
        target: Object exposing region, tab, and analogy attributes, or ``None``.

    Returns:
        Immutable display state for the future Remember Box widget.
    """

    if target is None:
        return create_empty_remember_box_state()

    region_id = str(getattr(target, "region_id", "") or "")
    region_name = str(getattr(target, "region_name", "Unknown brain region") or "")
    target_tab_id = str(getattr(target, "target_tab_id", "") or "")
    target_tab_label = str(getattr(target, "target_tab_label", "No target tab") or "")
    analogy_title = str(getattr(target, "analogy_title", "No mapping available") or "")
    analogy_text = str(getattr(target, "analogy_text", "") or "")
    is_known = bool(getattr(target, "is_known", False))
    can_open_target = bool(is_known and target_tab_id)

    if not analogy_text:
        analogy_text = (
            "No Remember Box explanation is available for this region yet."
        )

    return RememberBoxState(
        region_id=region_id,
        region_name=region_name or "Unknown brain region",
        target_tab_id=target_tab_id,
        target_tab_label=target_tab_label or "No target tab",
        analogy_title=analogy_title or "No mapping available",
        analogy_text=analogy_text,
        action_label="Open tool" if can_open_target else "No action available",
        status="mapped" if can_open_target else "unmapped",
        is_placeholder=False,
        can_open_target=can_open_target,
    )


def get_remember_box_summary() -> RememberBoxSummary:
    """Return Box Architecture metadata for the Remember Box scaffold.

    Returns:
        Immutable summary of the display-state box boundary.
    """

    return RememberBoxSummary(
        box_id=REMEMBER_BOX_ID,
        contract_version=REMEMBER_BOX_CONTRACT_VERSION,
        responsibility=(
            "Own the Brain Navigator explanation-card display state without "
            "owning brain rendering, tab switching, registry metadata, or "
            "mapping logic."
        ),
        owner_paths=(
            "kanda_reasoner_app/reasoner_tools_gui_shell/remember_box/",
        ),
        public_functions=(
            "create_empty_remember_box_state",
            "clear_remember_box_state",
            "build_remember_box_state",
            "get_remember_box_summary",
        ),
        forbidden_dependencies=(
            "PySide6",
            "main_window",
            "brain_navigator",
            "tab_navigation_controller",
            "tool_specs",
            "engineering_safety",
            "prompt_library",
        ),
        implementation_state="scaffold_only_display_state",
    )
