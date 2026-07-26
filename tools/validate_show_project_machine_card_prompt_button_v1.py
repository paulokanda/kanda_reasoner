"""Validate Show Project Machine-Card prompt wrapper and GUI control."""

from __future__ import annotations

import importlib.util
import py_compile
import sys
from pathlib import Path

__all__ = [
    "main",
]

FEATURE_ID = "show-project-machine-card-prompt-copy-button-v1"
UI_REL = Path(
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/"
    "window_methods_private_impl.py"
)
HELPER_REL = Path(
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/"
    "machine_card_prompt_button_private_impl.py"
)
CANON_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "12_generalized_project_canons/architecture_review_project_card_machine_canon.md"
)


def fail(message: str) -> None:
    raise AssertionError(message)


def read(root: Path, rel: Path) -> str:
    path = root / rel
    if not path.is_file():
        fail("Missing file: " + str(rel))
    return path.read_text(encoding="utf-8-sig")


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        fail("Missing " + label + ": " + needle)


def load_helper(root: Path):
    path = root / HELPER_REL
    spec = importlib.util.spec_from_file_location(
        "machine_card_prompt_button_private_impl",
        path,
    )
    if spec is None or spec.loader is None:
        fail("Could not load Machine-Card helper module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_canonical_prompt(root: Path) -> None:
    canon = read(root, CANON_REL)
    require(canon, "Prompt code: KPR-12-005", "Machine-Card prompt code")
    require(
        canon,
        "Prompt ID: architecture_review_project_card_machine_canon",
        "Machine-Card prompt id",
    )
    require(canon, "The machine processes the card; it does not become the card owner.", "core card-machine principle")
    print("MACHINE_CARD_CANONICAL_PROMPT_RESOLUTION: PASS")


def validate_ui(root: Path) -> None:
    ui = read(root, UI_REL)
    required = [
        'self.anti_hallucination_label = QLabel("Anti-hallucination:")',
        'self.copy_anti_hallucination_full_button = QPushButton("full")',
        'self.copy_anti_hallucination_short_button = QPushButton("short")',
        'self.machine_card_label = QLabel("Machine-Card:")',
        'self.copy_machine_card_logic_button = QPushButton("MCard Logic")',
    ]
    positions = []
    for needle in required:
        require(ui, needle, "Show Project control")
        positions.append(ui.index(needle))
    if positions != sorted(positions):
        fail("Machine-Card controls must appear after Anti-hallucination controls")
    require(ui, 'machine_card_label_palette.setColor(QPalette.WindowText, QColor("#000000"))', "black Machine-Card label")
    require(ui, 'machine_card_button_palette.setColor(QPalette.ButtonText, QColor("#ff4d00"))', "orange MCard Logic button")
    require(ui, "machine_card_button_font.setBold(True)", "bold MCard Logic button")
    require(ui, "copy_machine_card_logic_to_clipboard(self)", "MCard Logic button connection")
    print("SHOW_PROJECT_MACHINE_CARD_UI_ORDER_AND_STYLE: PASS")


def validate_wrapper_runtime(root: Path) -> None:
    helper = load_helper(root)
    wrapper = helper.build_machine_card_logic_wrapper(root)
    canon = read(root, CANON_REL).rstrip()
    require(wrapper, "KANDA_MACHINE_CARD_LOGIC_BEGIN", "wrapper begin marker")
    require(wrapper, "KANDA_MACHINE_CARD_LOGIC_END", "wrapper end marker")
    require(wrapper, "Prompt code: KPR-12-005", "wrapper prompt code")
    require(
        wrapper,
        "Prompt id: architecture_review_project_card_machine_canon",
        "wrapper prompt id",
    )
    if canon not in wrapper:
        fail("Machine-Card wrapper does not contain the exact canonical prompt text")
    if wrapper.count("KANDA_MACHINE_CARD_PROMPT_FILE_BEGIN") != 1:
        fail("Machine-Card wrapper must contain exactly one canonical prompt section")
    print("MACHINE_CARD_CLIPBOARD_WRAPPER_RUNTIME: PASS")


def validate_line_counts(root: Path) -> None:
    for rel in (UI_REL, HELPER_REL):
        count = len(read(root, rel).splitlines())
        if count >= 500:
            fail(str(rel) + " must remain below 500 physical lines: " + str(count))
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python validate_show_project_machine_card_prompt_button_v1.py <project_root>")
        return 2
    root = Path(sys.argv[1]).resolve()
    validate_canonical_prompt(root)
    validate_ui(root)
    validate_wrapper_runtime(root)
    validate_line_counts(root)
    py_compile.compile(str(root / UI_REL), doraise=True)
    py_compile.compile(str(root / HELPER_REL), doraise=True)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
