"""Validate anti-hallucination prompt groups and Show Project copy buttons."""

from __future__ import annotations

import importlib.util
import json
import py_compile
import sys
from pathlib import Path

__all__ = [
    "main",
]

FEATURE_ID = "anti-hallucination-prompt-groups-show-project-copy-buttons-v1"
PROMPT_DIR = Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/09_python_quality_security_observability")
META_DIR = Path("kanda_prompt_workspace/prompt_library/METADATA")
UI_REL = Path("kanda_reasoner_app/reasoner_tools_shell/runner_help/window_methods_private_impl.py")
HELPER_REL = Path("kanda_reasoner_app/reasoner_tools_shell/runner_help/anti_hallucination_prompt_buttons_private_impl.py")
BRIDGE_REL = Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/router_bridge_governed_implementation.md")
NAV_REL = Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md")
FOLDER_REL = PROMPT_DIR / "_FOLDER_ASSIMILATION.md"
GROUP_INDEX_REL = Path("kanda_prompt_workspace/prompt_library/ROUTING/GROUP_ASSIMILATION_INDEX.md")

PROMPTS = {
    "KPR-09-001": "anti_hallucination_full_group",
    "KPR-09-002": "anti_hallucination_short_group",
    "KPR-09-003": "anti_hallucination_independent_ai_audit_full",
    "KPR-09-004": "anti_hallucination_web_evidence_audit_full",
    "KPR-09-005": "anti_hallucination_book_literature_audit_full",
    "KPR-09-006": "anti_hallucination_master_protocol_full",
    "KPR-09-007": "anti_hallucination_independent_ai_audit_short",
    "KPR-09-008": "anti_hallucination_web_evidence_audit_short",
    "KPR-09-009": "anti_hallucination_book_literature_audit_short",
    "KPR-09-010": "anti_hallucination_protocol_short",
}


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


def validate_prompts(root: Path) -> None:
    folder_text = read(root, FOLDER_REL)
    for code, prompt_id in PROMPTS.items():
        prompt_rel = PROMPT_DIR / (prompt_id + ".md")
        meta_rel = META_DIR / (prompt_id + ".meta.json")
        read(root, prompt_rel)
        meta = json.loads(read(root, meta_rel))
        if meta.get("prompt_code") != code:
            fail("Prompt code mismatch for " + prompt_id)
        if meta.get("prompt_id") != prompt_id:
            fail("Prompt id mismatch for " + prompt_id)
        if meta.get("status") != "active":
            fail("Prompt status must be active: " + prompt_id)
        require(folder_text, "`" + prompt_id + "`", "folder assimilation reference")
    print("ANTI_HALLUCINATION_PROMPT_ASSETS: PASS")


def validate_routing(root: Path) -> None:
    bridge = read(root, BRIDGE_REL)
    nav = read(root, NAV_REL)
    group_index = read(root, GROUP_INDEX_REL)
    for text, label in ((bridge, "router bridge"), (nav, "navigation index")):
        require(text, "anti_hallucination_short_group", label + " short group")
        require(text, "anti_hallucination_full_group", label + " full group")
    require(bridge, "Do not treat agreement between AIs as proof.", "router bridge anti-consensus rule")
    require(nav, "Search for disconfirming evidence", "navigation disconfirmation rule")
    require(group_index, "evidence-first anti-hallucination review", "group index anti-hallucination responsibility")
    print("ANTI_HALLUCINATION_ROUTING: PASS")


def validate_ui(root: Path) -> None:
    ui = read(root, UI_REL)
    helper = read(root, HELPER_REL)
    require(ui, 'self.anti_hallucination_label = QLabel("Anti-hallucination:")', "black label")
    require(ui, 'self.copy_anti_hallucination_full_button = QPushButton("full")', "full button")
    require(ui, 'self.copy_anti_hallucination_short_button = QPushButton("short")', "short button")
    require(ui, 'QColor("#000000")', "black label color")
    require(ui, 'QColor("#ff4d00")', "orange button color")
    require(ui, 'anti_font.setBold(True)', "bold anti-hallucination buttons")
    require(ui, 'copy_full_anti_hallucination_group_to_clipboard(self)', "full button connection")
    require(ui, 'copy_short_anti_hallucination_group_to_clipboard(self)', "short button connection")
    require(helper, 'KANDA_ANTI_HALLUCINATION_FULL_BEGIN', "full wrapper marker")
    require(helper, 'KANDA_ANTI_HALLUCINATION_SHORT_BEGIN', "short wrapper marker")
    print("SHOW_PROJECT_ANTI_HALLUCINATION_UI: PASS")


def load_helper(root: Path):
    path = root / HELPER_REL
    spec = importlib.util.spec_from_file_location("anti_hallucination_prompt_buttons_private_impl", path)
    if spec is None or spec.loader is None:
        fail("Could not load helper module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_wrapper_runtime(root: Path) -> None:
    helper = load_helper(root)
    full = helper.build_full_anti_hallucination_group(root)
    short = helper.build_short_anti_hallucination_group(root)
    if full.count("KANDA_ANTI_HALLUCINATION_FILE_BEGIN") != 5:
        fail("Full group must contain five canonical files")
    if short.count("KANDA_ANTI_HALLUCINATION_FILE_BEGIN") != 5:
        fail("Short group must contain five canonical files")
    full_order = [
        "anti_hallucination_full_group.md",
        "anti_hallucination_independent_ai_audit_full.md",
        "anti_hallucination_web_evidence_audit_full.md",
        "anti_hallucination_book_literature_audit_full.md",
        "anti_hallucination_master_protocol_full.md",
    ]
    short_order = [
        "anti_hallucination_short_group.md",
        "anti_hallucination_independent_ai_audit_short.md",
        "anti_hallucination_web_evidence_audit_short.md",
        "anti_hallucination_book_literature_audit_short.md",
        "anti_hallucination_protocol_short.md",
    ]
    for text, order in ((full, full_order), (short, short_order)):
        positions = [text.index(name) for name in order]
        if positions != sorted(positions):
            fail("Prompt group copy order is not deterministic")
    print("ANTI_HALLUCINATION_CLIPBOARD_WRAPPER_RUNTIME: PASS")


def validate_line_counts(root: Path) -> None:
    for rel in (UI_REL, HELPER_REL):
        lines = read(root, rel).splitlines()
        if len(lines) > 500:
            fail(str(rel) + " exceeds 500 physical lines: " + str(len(lines)))
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python validate_anti_hallucination_prompt_groups_show_project_buttons_v1.py <project_root>")
        return 2
    root = Path(sys.argv[1]).resolve()
    validate_prompts(root)
    validate_routing(root)
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
