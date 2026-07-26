# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_version_state.py
"""Isolated Planner version ownership for heuristic, Local AI, and Web AI plans."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass

from .models import DocstringProposal, RefactorPlan
from .planner_version_preference_box import (
    PLANNER_ROUTE_HEURISTIC,
    PLANNER_ROUTE_LOCAL_AI,
    PLANNER_ROUTE_PREFERENCE_KEY,
    PLANNER_ROUTE_WEB_AI,
    load_last_used_planner_route,
    remember_last_used_planner_route,
    _default_settings_factory as _preference_box_settings_factory,
)

__all__ = [
    "PLANNER_VERSION_HEURISTIC",
    "PLANNER_VERSION_LOCAL_AI",
    "PLANNER_VERSION_WEB_AI",
    "PLANNER_VERSION_PREFERENCE_KEY",
    "PlannerVersionBundle",
    "get_planner_version_bundle",
    "get_selected_planner_version_bundle",
    "get_planner_exchange_base_bundle",
    "get_last_generated_native_bundle",
    "initialize_planner_version_state",
    "planner_version_available",
    "select_planner_version",
    "selected_planner_version",
    "persist_planner_version_preference",
    "stored_planner_version_preference",
    "store_heuristic_version",
    "store_local_ai_version",
    "store_web_ai_version",
]

PLANNER_VERSION_HEURISTIC = PLANNER_ROUTE_HEURISTIC
PLANNER_VERSION_LOCAL_AI = PLANNER_ROUTE_LOCAL_AI
PLANNER_VERSION_WEB_AI = PLANNER_ROUTE_WEB_AI
PLANNER_VERSION_PREFERENCE_KEY = PLANNER_ROUTE_PREFERENCE_KEY
_KNOWN_VERSIONS = frozenset(
    {
        PLANNER_VERSION_HEURISTIC,
        PLANNER_VERSION_LOCAL_AI,
        PLANNER_VERSION_WEB_AI,
    }
)


@dataclass(frozen=True)
class PlannerVersionBundle:
    """One isolated Planner plan version and its accepted docstring proposals."""

    version_name: str
    plan: RefactorPlan
    docstring_proposals: tuple[DocstringProposal, ...]


def initialize_planner_version_state(
    window: object,
    *,
    preserve_selection: bool = False,
) -> None:
    """Initialize version slots while optionally preserving selected intent."""

    selected_before = (
        selected_planner_version(window)
        if preserve_selection
        else stored_planner_version_preference(window)
    )
    window._large_file_refactor_heuristic_version = None
    window._large_file_refactor_local_ai_version = None
    window._large_file_refactor_web_ai_version = None
    window._large_file_refactor_selected_version = selected_before
    window._large_file_refactor_last_plan = None
    window._large_file_refactor_last_generated_native_version = None
    window._large_file_refactor_docstring_proposals = []


def store_heuristic_version(
    window: object,
    plan: RefactorPlan,
    proposals: list[DocstringProposal],
) -> PlannerVersionBundle:
    """Store a new deterministic version and invalidate derived AI versions."""

    bundle = _make_bundle(PLANNER_VERSION_HEURISTIC, plan, proposals)
    window._large_file_refactor_heuristic_version = bundle
    window._large_file_refactor_local_ai_version = None
    window._large_file_refactor_web_ai_version = None
    window._large_file_refactor_last_generated_native_version = PLANNER_VERSION_HEURISTIC
    _sync_selected_to_active(window)
    return bundle


def store_local_ai_version(
    window: object,
    plan: RefactorPlan,
    proposals: list[DocstringProposal],
) -> PlannerVersionBundle:
    """Store a Local AI version and invalidate any Web AI derivative."""

    bundle = _make_bundle(PLANNER_VERSION_LOCAL_AI, plan, proposals)
    window._large_file_refactor_local_ai_version = bundle
    window._large_file_refactor_web_ai_version = None
    window._large_file_refactor_last_generated_native_version = PLANNER_VERSION_LOCAL_AI
    _sync_selected_to_active(window)
    return bundle


def store_web_ai_version(
    window: object,
    plan: RefactorPlan,
    proposals: list[DocstringProposal],
) -> PlannerVersionBundle:
    """Store one human-accepted, validated Web AI proposal version."""

    bundle = _make_bundle(PLANNER_VERSION_WEB_AI, plan, proposals)
    window._large_file_refactor_web_ai_version = bundle
    _sync_selected_to_active(window)
    return bundle


def select_planner_version(window: object, version_name: str) -> bool:
    """Select a known version intent and project it only when it exists.

    Version intent is independent from version availability. This lets the user
    choose Local AI or Web AI before that derived version has been created,
    while the Workbench handoff remains fail-closed until the selected version
    actually exists.
    """

    if version_name not in _KNOWN_VERSIONS:
        raise ValueError("Unknown Planner version: " + version_name)
    window._large_file_refactor_selected_version = version_name
    _sync_selected_to_active(window)
    return True


def stored_planner_version_preference(window: object) -> str:
    """Return the remembered route from the isolated preference box."""

    del window
    return load_last_used_planner_route(
        settings_factory=_new_planner_version_settings,
    )

def selected_planner_version(window: object) -> str:
    """Return selected Planner version name, defaulting to Local AI."""

    try:
        value = str(window._large_file_refactor_selected_version)
    except AttributeError:
        value = PLANNER_VERSION_LOCAL_AI
    return value if value in _KNOWN_VERSIONS else PLANNER_VERSION_LOCAL_AI


def planner_version_available(window: object, version_name: str) -> bool:
    """Return whether one isolated Planner version exists."""

    return get_planner_version_bundle(window, version_name) is not None


def get_planner_version_bundle(
    window: object,
    version_name: str,
) -> PlannerVersionBundle | None:
    """Return one stored immutable-version wrapper without changing selection."""

    if version_name == PLANNER_VERSION_HEURISTIC:
        value = _heuristic_bundle_value(window)
    elif version_name == PLANNER_VERSION_LOCAL_AI:
        value = _local_ai_bundle_value(window)
    elif version_name == PLANNER_VERSION_WEB_AI:
        value = _web_ai_bundle_value(window)
    else:
        raise ValueError("Unknown Planner version: " + version_name)
    return value if isinstance(value, PlannerVersionBundle) else None


def get_selected_planner_version_bundle(
    window: object,
) -> PlannerVersionBundle | None:
    """Return currently selected version bundle when available."""

    return get_planner_version_bundle(window, selected_planner_version(window))




def get_last_generated_native_bundle(
    window: object,
) -> PlannerVersionBundle | None:
    """Return the most recently generated Heuristic or Local AI version.

    Web AI export is intentionally independent from the currently selected
    display radio. The clipboard package always uses the latest native Planner
    generation result so selecting an imported Web AI version cannot silently
    change the export base.
    """

    try:
        version_name = window._large_file_refactor_last_generated_native_version
    except AttributeError:
        version_name = None
    if version_name not in {PLANNER_VERSION_HEURISTIC, PLANNER_VERSION_LOCAL_AI}:
        return None
    return get_planner_version_bundle(window, version_name)


def get_planner_exchange_base_bundle(
    window: object,
) -> PlannerVersionBundle | None:
    """Return the latest native generation used as the Web AI export base."""

    return get_last_generated_native_bundle(window)


def persist_planner_version_preference(
    window: object,
    version_name: str,
) -> bool:
    """Persist one stable route ID through the isolated preference box."""

    del window
    if version_name not in _KNOWN_VERSIONS:
        raise ValueError("Unknown Planner version: " + version_name)
    return remember_last_used_planner_route(
        version_name,
        settings_factory=_new_planner_version_settings,
    )


def _new_planner_version_settings() -> object:
    """Compatibility seam returning the isolated box endpoint, never host state."""

    return _preference_box_settings_factory()


def _heuristic_bundle_value(window: object) -> object | None:
    """Read the Heuristic bundle slot without reflection."""

    try:
        return window._large_file_refactor_heuristic_version
    except AttributeError:
        return None


def _local_ai_bundle_value(window: object) -> object | None:
    """Read the Local AI bundle slot without reflection."""

    try:
        return window._large_file_refactor_local_ai_version
    except AttributeError:
        return None


def _web_ai_bundle_value(window: object) -> object | None:
    """Read the imported Web AI bundle slot without reflection."""

    try:
        return window._large_file_refactor_web_ai_version
    except AttributeError:
        return None


def _make_bundle(
    version_name: str,
    plan: RefactorPlan,
    proposals: list[DocstringProposal],
) -> PlannerVersionBundle:
    """Deep-copy nested planning structures so versions never alias each other."""

    return PlannerVersionBundle(
        version_name=version_name,
        plan=deepcopy(plan),
        docstring_proposals=tuple(deepcopy(list(proposals))),
    )


def _sync_selected_to_active(window: object) -> None:
    """Project only the selected version into the existing public handoff state."""

    bundle = get_selected_planner_version_bundle(window)
    if bundle is None:
        window._large_file_refactor_last_plan = None
        window._large_file_refactor_docstring_proposals = []
        return
    window._large_file_refactor_last_plan = deepcopy(bundle.plan)
    window._large_file_refactor_docstring_proposals = deepcopy(
        list(bundle.docstring_proposals)
    )
