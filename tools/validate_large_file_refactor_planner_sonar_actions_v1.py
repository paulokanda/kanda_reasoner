# project-path: tools/validate_large_file_refactor_planner_sonar_actions_v1.py
"""Validate Planner sonar feedback for long-running planning actions."""

from __future__ import annotations

import ast
from pathlib import Path

FEATURE_ID = "large-file-refactor-planner-sonar-actions-v1"
ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"


def require(text: str, needle: str, label: str) -> None:
    """Fail when one required contract marker is absent."""

    if needle not in text:
        raise SystemExit("VALIDATION ERROR: missing " + label + ": " + needle)


def main() -> None:
    """Validate source contracts, box isolation, and module size."""

    files = {
        "gui_shell.py": BOX / "gui_shell.py",
        "planner_local_ai_review_gui.py": BOX / "planner_local_ai_review_gui.py",
        "planner_sonar_activity.py": BOX / "planner_sonar_activity.py",
        "planner_split_plan_gui.py": BOX / "planner_split_plan_gui.py",
    }

    texts: dict[str, str] = {}
    for name, path in files.items():
        if not path.is_file():
            raise SystemExit("VALIDATION ERROR: missing file: " + str(path))
        text = path.read_text(encoding="utf-8")
        ast.parse(text)
        line_count = len(text.splitlines())
        if line_count > 500:
            raise SystemExit(
                "VALIDATION ERROR: module exceeds 500 lines: "
                + name
                + "="
                + str(line_count)
            )
        texts[name] = text

    gui = texts["gui_shell.py"]
    ai_gui = texts["planner_local_ai_review_gui.py"]
    sonar = texts["planner_sonar_activity.py"]
    split_gui = texts["planner_split_plan_gui.py"]

    require(
        gui,
        "start_split_plan_generation_for_window",
        "background split-plan runner",
    )
    require(
        gui,
        'activity_label="Ask Local LLM for Ambiguous Symbols"',
        "manual LLM activity label",
    )
    require(
        gui,
        "_large_file_refactor_split_plan_running",
        "split-plan busy state",
    )
    require(
        split_gui,
        "threading.Thread(",
        "background deterministic planning",
    )
    require(
        split_gui,
        "start_split_plan_sonar(window, target_label)",
        "split-plan sonar start",
    )
    require(
        split_gui,
        'activity_label="Generate Split Plan"',
        "automatic AI continuation label",
    )
    require(
        ai_gui,
        "start_local_ai_review_sonar(",
        "AI sonar start",
    )
    require(
        ai_gui,
        "finish_planner_sonar_success",
        "AI sonar success finish",
    )
    require(
        ai_gui,
        "finish_planner_sonar_error",
        "AI sonar error finish",
    )
    require(
        sonar,
        "from kanda_reasoner_app.templates.green_sonar_monitor import",
        "public sonar template contract",
    )
    require(
        sonar,
        "Planner remains pre-implementation and does not write source",
        "pre-implementation scope message",
    )

    forbidden = (
        "workbench_gui",
        "transactional_guarded_apply",
        "post_apply_validator",
        "rollback_executor",
    )
    combined = "\n".join(texts.values())
    for needle in forbidden:
        if needle in combined:
            raise SystemExit(
                "VALIDATION ERROR: cross-box contamination marker: " + needle
            )

    print("PLANNER_SONAR_ACTIONS: PRESENT")
    print("GENERATE_SPLIT_PLAN: BACKGROUND_WITH_SONAR")
    print("LOCAL_AI_REVIEW: BACKGROUND_WITH_SONAR")
    print("SONAR_TEMPLATE: PUBLIC_CONTRACT_USED")
    print("PLANNER_ROLE: PRE_IMPLEMENTATION_PRESERVED")
    print("WORKBENCH_CONTAMINATION: NONE")
    print("BOX_SHIELD: PASS")
    print("NO_LEAK_LOGIC: PASS")
    print("MODULE_SIZE_GATE: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
