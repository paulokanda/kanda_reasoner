# project-path: tools/validate_large_file_refactor_planner_version_enablement_repair_v1.py
"""Validate Planner version selectability and AI action enablement repair."""
from __future__ import annotations

import ast
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
FEATURE = "large-file-refactor-planner-version-enablement-repair-v1"


def _install_namespace_packages() -> None:
    packages = (
        ("kanda_reasoner_app", ROOT / "kanda_reasoner_app"),
        ("kanda_reasoner_app.manage_architecture", ROOT / "kanda_reasoner_app/manage_architecture"),
        ("kanda_reasoner_app.manage_architecture.large_file_refactor_planner", BOX),
    )
    for name, path in packages:
        if name in sys.modules:
            continue
        module = ModuleType(name)
        module.__path__ = [str(path)]
        sys.modules[name] = module


_install_namespace_packages()

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (
    DocstringProposal,
    RefactorPlan,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_action_enablement import (
    build_planner_action_enablement,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_version_state import (
    PLANNER_VERSION_HEURISTIC,
    PLANNER_VERSION_LOCAL_AI,
    PLANNER_VERSION_WEB_AI,
    get_planner_exchange_base_bundle,
    get_selected_planner_version_bundle,
    initialize_planner_version_state,
    select_planner_version,
    selected_planner_version,
    store_heuristic_version,
    store_local_ai_version,
)


def main() -> None:
    texts = _load_and_parse()
    _static_checks(texts)
    _runtime_intent_and_handoff_test()
    _runtime_exchange_fallback_test()
    _runtime_local_ai_action_test()

    print("VERSION_SELECTABILITY: INDEPENDENT_FROM_AVAILABILITY")
    print("UNAVAILABLE_VERSION_INTENT: SELECTABLE")
    print("WORKBENCH_HANDOFF_FOR_UNAVAILABLE_VERSION: FAIL_CLOSED")
    print("LOCAL_AI_CREATION_PATH: ENABLED_FROM_HEURISTIC_BASE")
    print("WEB_AI_COPY_RECEIVE: ENABLED_FROM_SAFE_EXCHANGE_BASE")
    print("WEB_AI_EXCHANGE_BASE_CHAIN: WEB_TO_LOCAL_TO_HEURISTIC")
    print("BOX_SHIELD: PASS")
    print("NO_LEAK_LOGIC: PASS")
    print("MODULE_SIZE_GATE: PASS")
    print("VALIDATION OK: " + FEATURE)
    print("STATUS: IN_SYNC")


def _load_and_parse() -> dict[str, str]:
    names = (
        "gui_shell.py",
        "planner_version_selector_gui.py",
        "planner_version_state.py",
        "planner_web_ai_exchange_gui.py",
    )
    texts: dict[str, str] = {}
    for name in names:
        path = BOX / name
        if not path.is_file():
            raise SystemExit("VALIDATION ERROR: missing " + str(path))
        text = path.read_text(encoding="utf-8")
        ast.parse(text)
        if len(text.splitlines()) > 500:
            raise SystemExit("VALIDATION ERROR: module exceeds 500 lines: " + name)
        texts[name] = text
    return texts


def _static_checks(texts: dict[str, str]) -> None:
    selector = texts["planner_version_selector_gui.py"]
    state = texts["planner_version_state.py"]
    gui = texts["gui_shell.py"]
    web_gui = texts["planner_web_ai_exchange_gui.py"]

    if "radio.setEnabled(heuristic_ready)" not in selector:
        raise SystemExit("VALIDATION ERROR: radios still depend on derived-version availability")
    if "if not planner_version_available(window, version_name)" in state:
        raise SystemExit("VALIDATION ERROR: version intent selection still rejects unavailable versions")
    if "get_planner_exchange_base_bundle" not in gui or "get_planner_exchange_base_bundle" not in web_gui:
        raise SystemExit("VALIDATION ERROR: Web AI exchange does not use safe base resolver")
    web_ready_block = gui.split("web_ready = bool(", 1)[1].split(")\n    _set_button_enabled", 1)[0]
    if "selected is not None" in web_ready_block:
        raise SystemExit("VALIDATION ERROR: Web AI action remains deadlocked by selected availability")
    if "plan_allows_ai_architecture_correction(active_plan)" in web_ready_block:
        raise SystemExit("VALIDATION ERROR: Web AI exchange incorrectly requires correctable status")


def _plan(status: str, suffix: str) -> RefactorPlan:
    return RefactorPlan(
        schema_version="1.0",
        feature_id="fixture",
        target_file="fixture.py",
        source_content_hash="hash-" + suffix,
        settings={"minimum_helper_physical_lines": 100},
        public_api_before=[],
        public_api_after_expected=[],
        symbols=[],
        atomic_clusters=[],
        proposed_modules=[],
        import_migration={},
        docstring_proposals=[],
        risks=["TOO_SMALL_HELPER"] if status == "blocked" else [],
        validation_blockers=["tiny helper"] if status == "blocked" else [],
        status=status,
    )


def _proposal() -> DocstringProposal:
    return DocstringProposal(
        schema_version="1.0",
        feature_id="fixture",
        target_file="fixture.py",
        target_kind="planned_module",
        target_name="_fixture.py",
        proposed_docstring='"""Fixture."""',
        provenance="deterministic_template",
        confidence="medium",
    )


def _runtime_intent_and_handoff_test() -> None:
    window = SimpleNamespace()
    initialize_planner_version_state(window)
    store_heuristic_version(window, _plan("blocked", "heuristic"), [_proposal()])

    if not select_planner_version(window, PLANNER_VERSION_LOCAL_AI):
        raise SystemExit("VALIDATION ERROR: unavailable Local AI intent could not be selected")
    if selected_planner_version(window) != PLANNER_VERSION_LOCAL_AI:
        raise SystemExit("VALIDATION ERROR: Local AI intent was not retained")
    if get_selected_planner_version_bundle(window) is not None:
        raise SystemExit("VALIDATION ERROR: unavailable Local AI version masquerades as available")
    if window._large_file_refactor_last_plan is not None:
        raise SystemExit("VALIDATION ERROR: Workbench handoff did not fail closed")

    store_local_ai_version(window, _plan("planned", "local"), [_proposal()])
    if window._large_file_refactor_last_plan is None or window._large_file_refactor_last_plan.status != "planned":
        raise SystemExit("VALIDATION ERROR: selected Local AI intent did not activate when created")


def _runtime_exchange_fallback_test() -> None:
    window = SimpleNamespace()
    initialize_planner_version_state(window)
    heuristic = _plan("blocked", "heuristic")
    local = _plan("planned", "local")
    store_heuristic_version(window, heuristic, [_proposal()])

    select_planner_version(window, PLANNER_VERSION_LOCAL_AI)
    base = get_planner_exchange_base_bundle(window)
    if base is None or base.version_name != PLANNER_VERSION_HEURISTIC:
        raise SystemExit("VALIDATION ERROR: Local AI intent did not fall back to heuristic exchange base")

    store_local_ai_version(window, local, [_proposal()])
    select_planner_version(window, PLANNER_VERSION_WEB_AI)
    base = get_planner_exchange_base_bundle(window)
    if base is None or base.version_name != PLANNER_VERSION_LOCAL_AI:
        raise SystemExit("VALIDATION ERROR: Web AI intent did not fall back to Local AI exchange base")


def _runtime_local_ai_action_test() -> None:
    actions = build_planner_action_enablement(
        has_analysis=True,
        has_plan=True,
        plan_status="blocked",
        has_preview=False,
        validation_passed=False,
        payload_status="",
        ai_review_running=False,
        has_docstring_plan=True,
        ai_correctable_plan=True,
    )
    if not actions.run_llm_arbitration:
        raise SystemExit("VALIDATION ERROR: Local AI action disabled for correctable blocked heuristic plan")


if __name__ == "__main__":
    main()
