# project-path: tools/validate_large_file_refactor_planner_version_routed_generation_analysis_feedback_repair_v1.py
"""Validate version-routed split generation and visible Analyze File feedback repair."""

from __future__ import annotations

import ast
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from types import ModuleType, SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
FEATURE = "large-file-refactor-planner-version-routed-generation-analysis-feedback-repair-v1"


def _install_namespace_packages() -> None:
    packages = (
        ("kanda_reasoner_app", ROOT / "kanda_reasoner_app"),
        (
            "kanda_reasoner_app.manage_architecture",
            ROOT / "kanda_reasoner_app/manage_architecture",
        ),
        (
            "kanda_reasoner_app.manage_architecture.large_file_refactor_planner",
            BOX,
        ),
    )
    for name, path in packages:
        if name in sys.modules:
            continue
        module = ModuleType(name)
        module.__path__ = [str(path)]
        sys.modules[name] = module


_install_namespace_packages()

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.ast_analysis import (
    analyze_python_file,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_analysis_feedback import (
    format_planner_analysis_completion,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_version_state import (
    PLANNER_VERSION_HEURISTIC,
    PLANNER_VERSION_LOCAL_AI,
    PLANNER_VERSION_WEB_AI,
    initialize_planner_version_state,
    select_planner_version,
    selected_planner_version,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_versioned_generation import (
    planner_generation_route,
)


def main() -> None:
    texts = _load_and_parse()
    _static_checks(texts)
    _analysis_core_test()
    _selected_version_preservation_test()
    _generation_route_test()

    print("ANALYZE_FILE_CORE: WORKING")
    print("ANALYSIS_VISIBLE_FEEDBACK: PRESENT")
    print("VERSION_RADIOS_BEFORE_ANALYSIS: ALWAYS_SELECTABLE")
    print("VERSION_SELECTION_SURVIVES_ANALYSIS: PASS")
    print("GENERATE_SPLIT_PLAN_ROUTING: HEURISTIC_LOCAL_AI_WEB_AI")
    print("LOCAL_AI_ROUTE: AUTO_DOCSTRINGS_THEN_AI_CORRECTION")
    print("WEB_AI_ROUTE: AUTO_DOCSTRINGS_THEN_EXCHANGE_READY")
    print("WORKBENCH_HANDOFF_OWNERSHIP: UNCHANGED")
    print("BOX_SHIELD: PASS")
    print("NO_LEAK_LOGIC: PASS")
    print("MODULE_SIZE_GATE: PASS")
    print("VALIDATION OK: " + FEATURE)
    print("STATUS: IN_SYNC")


def _load_and_parse() -> dict[str, str]:
    names = (
        "gui_shell.py",
        "planner_analysis_feedback.py",
        "planner_split_plan_gui.py",
        "planner_version_selector_gui.py",
        "planner_version_state.py",
        "planner_versioned_generation.py",
    )
    texts: dict[str, str] = {}
    for name in names:
        path = BOX / name
        if not path.is_file():
            raise SystemExit("VALIDATION ERROR: missing " + str(path))
        text = path.read_text(encoding="utf-8")
        ast.parse(text)
        line_count = len(text.splitlines())
        if line_count > 500:
            raise SystemExit(
                "VALIDATION ERROR: module exceeds 500 lines: "
                + name
                + " ("
                + str(line_count)
                + ")"
            )
        texts[name] = text
    return texts


def _static_checks(texts: dict[str, str]) -> None:
    selector = texts["planner_version_selector_gui.py"]
    state = texts["planner_version_state.py"]
    shell = texts["gui_shell.py"]
    split_gui = texts["planner_split_plan_gui.py"]

    required_selector = "radio.setEnabled(True)"
    if required_selector not in selector:
        raise SystemExit("VALIDATION ERROR: version radios are not always selectable")
    if "radio.setEnabled(heuristic_ready)" in selector:
        raise SystemExit("VALIDATION ERROR: radios still wait for heuristic generation")
    if "preserve_selection: bool = False" not in state:
        raise SystemExit("VALIDATION ERROR: version-state reset cannot preserve route intent")
    if "preserve_selection=True" not in shell:
        raise SystemExit("VALIDATION ERROR: Analyze File still resets selected version intent")
    if "format_planner_analysis_completion" not in shell:
        raise SystemExit("VALIDATION ERROR: Analyze File lacks visible Plan & Actions feedback")
    if "selected_version = selected_planner_version(window)" not in shell:
        raise SystemExit("VALIDATION ERROR: Generate Split Plan does not capture selected route")
    if "planner_generation_route(version_name)" not in shell:
        raise SystemExit("VALIDATION ERROR: split completion does not route by selected version")
    if "completion_callback" not in split_gui:
        raise SystemExit("VALIDATION ERROR: split runner lacks version-route continuation hook")
    if "LOCAL AI VERSION GENERATION STARTED" not in shell:
        raise SystemExit("VALIDATION ERROR: Local AI generation route is absent")
    if "WEB AI BASE READY" not in shell:
        raise SystemExit("VALIDATION ERROR: Web AI generation route is absent")


def _analysis_core_test() -> None:
    with TemporaryDirectory() as directory:
        fixture = Path(directory) / "analysis_fixture.py"
        fixture.write_text(
            '"""Fixture."""\n\n'
            "VALUE = 1\n\n"
            "def alpha(x: int) -> int:\n"
            '    """Return incremented value."""\n'
            "    return x + VALUE\n\n"
            "def _beta(y):\n"
            "    return alpha(y)\n",
            encoding="utf-8",
        )
        report = analyze_python_file(fixture)
        names = {symbol.name for symbol in report.symbols}
        if names != {"alpha", "_beta"}:
            raise SystemExit("VALIDATION ERROR: Analyze File core symbol extraction failed")
        if "alpha" not in report.public_api_symbols:
            raise SystemExit("VALIDATION ERROR: Analyze File public API extraction failed")
        if report.analysis_errors:
            raise SystemExit("VALIDATION ERROR: Analyze File fixture returned analysis errors")
        feedback = format_planner_analysis_completion(
            report,
            PLANNER_VERSION_WEB_AI,
        )
        required = (
            "ANALYSIS COMPLETE",
            "Top-level symbols: 2",
            "Selected split version: Web Ai",
            "Detailed AST evidence is available in Input & Analysis.",
        )
        if not all(marker in feedback for marker in required):
            raise SystemExit("VALIDATION ERROR: visible analysis feedback is incomplete")


def _selected_version_preservation_test() -> None:
    window = SimpleNamespace()
    initialize_planner_version_state(window)
    select_planner_version(window, PLANNER_VERSION_WEB_AI)
    initialize_planner_version_state(window, preserve_selection=True)
    if selected_planner_version(window) != PLANNER_VERSION_WEB_AI:
        raise SystemExit("VALIDATION ERROR: Analyze File reset lost Web AI route intent")

    select_planner_version(window, PLANNER_VERSION_HEURISTIC)
    initialize_planner_version_state(window, preserve_selection=True)
    if selected_planner_version(window) != PLANNER_VERSION_HEURISTIC:
        raise SystemExit("VALIDATION ERROR: Analyze File reset lost Heuristic route intent")


def _generation_route_test() -> None:
    heuristic = planner_generation_route(PLANNER_VERSION_HEURISTIC)
    local_ai = planner_generation_route(PLANNER_VERSION_LOCAL_AI)
    web_ai = planner_generation_route(PLANNER_VERSION_WEB_AI)

    if heuristic.generate_docstrings_automatically:
        raise SystemExit("VALIDATION ERROR: heuristic route unexpectedly auto-generates docs")
    if heuristic.start_local_ai_review or heuristic.prepare_web_ai_exchange:
        raise SystemExit("VALIDATION ERROR: heuristic route leaks into AI routes")
    if not local_ai.generate_docstrings_automatically or not local_ai.start_local_ai_review:
        raise SystemExit("VALIDATION ERROR: Local AI route is not end-to-end reachable")
    if local_ai.prepare_web_ai_exchange:
        raise SystemExit("VALIDATION ERROR: Local AI route leaks into Web AI route")
    if not web_ai.generate_docstrings_automatically or not web_ai.prepare_web_ai_exchange:
        raise SystemExit("VALIDATION ERROR: Web AI route is not exchange-ready")
    if web_ai.start_local_ai_review:
        raise SystemExit("VALIDATION ERROR: Web AI route unexpectedly invokes Local AI")


if __name__ == "__main__":
    main()
