# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/tab_navigation_controller.py
"""Tab Navigation Controller Box for stable tab-id based navigation.

This module is intentionally free of PySide6 imports. It owns the pure
navigation contract that converts stable tab IDs into notebook indexes and
optionally calls a caller-provided index setter.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass

__all__ = [
    "TAB_NAVIGATION_CONTROLLER_BOX_ID",
    "TAB_NAVIGATION_CONTROLLER_CONTRACT_VERSION",
    "TabNavigationController",
    "TabNavigationResult",
    "TabNavigationSummary",
    "build_tab_id_index_map",
    "create_tab_navigation_controller",
    "get_tab_navigation_controller_summary",
]

TAB_NAVIGATION_CONTROLLER_BOX_ID = "tab_navigation_controller"
TAB_NAVIGATION_CONTROLLER_CONTRACT_VERSION = "0.1"
IndexSetter = Callable[[int], None]
CurrentIndexReader = Callable[[], int]


@dataclass(frozen=True)
class TabNavigationResult:
    """Result returned by a tab navigation request.

    Attributes:
        success: Whether the requested tab was opened.
        tab_id: Stable tab ID requested by the caller.
        tab_index: Resolved tab index, when known.
        reason: Machine-readable reason describing the result.
    """

    success: bool
    tab_id: str
    tab_index: int | None
    reason: str


@dataclass(frozen=True)
class TabNavigationSummary:
    """Summary of the Tab Navigation Controller Box boundary."""

    box_id: str
    contract_version: str
    implementation_state: str
    public_functions: tuple[str, ...]
    owner_paths: tuple[str, ...]
    forbidden_dependencies: tuple[str, ...]


class TabNavigationController:
    """Open tabs by stable tab ID through a caller-provided adapter.

    The controller does not own a GUI notebook and does not import MainWindow or
    PySide6. A GUI owner may bind a ``set_current_index`` callback, allowing this
    controller to route requests without knowing GUI implementation details.
    """

    def __init__(
        self,
        tab_index_by_id: Mapping[str, int] | None = None,
        *,
        set_current_index: IndexSetter | None = None,
        get_current_index: CurrentIndexReader | None = None,
    ) -> None:
        """Initialize the controller.

        Args:
            tab_index_by_id: Mapping from stable tab IDs to notebook indexes.
            set_current_index: Optional callback used to open a tab index.
            get_current_index: Optional callback used to read active tab index.
        """

        self._tab_index_by_id: dict[str, int] = {}
        self._set_current_index = set_current_index
        self._get_current_index = get_current_index
        if tab_index_by_id:
            self.refresh_tab_index_map(tab_index_by_id)

    def refresh_tab_index_map(self, tab_index_by_id: Mapping[str, int]) -> None:
        """Replace the tab ID to index mapping.

        Args:
            tab_index_by_id: Mapping from stable tab IDs to non-negative indexes.

        Raises:
            ValueError: If a tab ID is empty or an index is negative.
        """

        cleaned: dict[str, int] = {}
        for tab_id, tab_index in tab_index_by_id.items():
            normalized_tab_id = str(tab_id).strip()
            if not normalized_tab_id:
                raise ValueError("tab_id must not be empty")
            if int(tab_index) < 0:
                raise ValueError("tab_index must not be negative")
            cleaned[normalized_tab_id] = int(tab_index)
        self._tab_index_by_id = cleaned

    def get_tab_index_by_id(self, tab_id: str) -> int | None:
        """Return the current index for ``tab_id`` or ``None`` when unknown."""

        return self._tab_index_by_id.get(str(tab_id).strip())

    def can_open_tab(self, tab_id: str) -> bool:
        """Return whether ``tab_id`` is known to this controller."""

        return self.get_tab_index_by_id(tab_id) is not None

    def open_tab_by_id(self, tab_id: str) -> TabNavigationResult:
        """Open a tab by stable ID.

        Args:
            tab_id: Stable tab ID requested by another box.

        Returns:
            TabNavigationResult describing success or safe failure.
        """

        normalized_tab_id = str(tab_id).strip()
        tab_index = self.get_tab_index_by_id(normalized_tab_id)
        if tab_index is None:
            return TabNavigationResult(
                success=False,
                tab_id=normalized_tab_id,
                tab_index=None,
                reason="unknown_tab_id",
            )

        if self._set_current_index is None:
            return TabNavigationResult(
                success=False,
                tab_id=normalized_tab_id,
                tab_index=tab_index,
                reason="navigation_not_bound",
            )

        self._set_current_index(tab_index)
        return TabNavigationResult(
            success=True,
            tab_id=normalized_tab_id,
            tab_index=tab_index,
            reason="opened",
        )

    def get_current_index(self) -> int | None:
        """Return the current tab index when a reader callback is bound."""

        if self._get_current_index is None:
            return None
        return int(self._get_current_index())

    def list_registered_tab_ids(self) -> tuple[str, ...]:
        """Return registered tab IDs in index order."""

        return tuple(
            tab_id
            for tab_id, _index in sorted(
                self._tab_index_by_id.items(),
                key=lambda item: item[1],
            )
        )


def build_tab_id_index_map(
    tab_specs: Iterable[object],
    *,
    first_index: int = 0,
) -> dict[str, int]:
    """Build a stable tab ID to index map from registry-like specs.

    Args:
        tab_specs: Iterable of objects exposing a ``tab_id`` attribute.
        first_index: Index assigned to the first spec.

    Returns:
        Mapping from tab IDs to visible tab indexes.

    Raises:
        ValueError: If a spec has no tab ID or duplicates a tab ID.
    """

    if first_index < 0:
        raise ValueError("first_index must not be negative")

    mapping: dict[str, int] = {}
    for offset, spec in enumerate(tab_specs):
        raw_tab_id = getattr(spec, "tab_id", None)
        tab_id = str(raw_tab_id or "").strip()
        if not tab_id:
            raise ValueError("tab spec is missing tab_id")
        if tab_id in mapping:
            raise ValueError(f"duplicate tab_id: {tab_id}")
        mapping[tab_id] = first_index + offset
    return mapping


def create_tab_navigation_controller(
    tab_index_by_id: Mapping[str, int] | None = None,
    *,
    set_current_index: IndexSetter | None = None,
    get_current_index: CurrentIndexReader | None = None,
) -> TabNavigationController:
    """Create a Tab Navigation Controller through the public contract."""

    return TabNavigationController(
        tab_index_by_id,
        set_current_index=set_current_index,
        get_current_index=get_current_index,
    )


def get_tab_navigation_controller_summary() -> TabNavigationSummary:
    """Return Box Architecture metadata for this public contract."""

    return TabNavigationSummary(
        box_id=TAB_NAVIGATION_CONTROLLER_BOX_ID,
        contract_version=TAB_NAVIGATION_CONTROLLER_CONTRACT_VERSION,
        implementation_state="pure_controller_box",
        public_functions=(
            "build_tab_id_index_map",
            "create_tab_navigation_controller",
            "get_tab_navigation_controller_summary",
            "TabNavigationController.open_tab_by_id",
            "TabNavigationController.get_tab_index_by_id",
        ),
        owner_paths=(
            "kanda_reasoner_app/reasoner_tools_gui_shell/tab_navigation_controller.py",
        ),
        forbidden_dependencies=(
            "PySide6",
            "main_window",
            "brain_navigator",
            "remember_box",
            "engineering_safety",
            "prompt_library",
        ),
    )
