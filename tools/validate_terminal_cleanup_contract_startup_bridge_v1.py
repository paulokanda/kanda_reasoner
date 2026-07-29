"""Validate terminal-cleanup startup bridge prompt and patch contracts."""

from __future__ import annotations

import json
import py_compile
import sys
import zipfile
from pathlib import Path

FEATURE_ID = "terminal-cleanup-contract-startup-bridge-v1"
PATCH_NAME = "kanda_terminal_cleanup_contract_startup_bridge_v1_patch.zip"

CHANGED_FILES = [
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/terminal_cleanup_contract.md",
    "kanda_prompt_workspace/prompt_library/METADATA/terminal_cleanup_contract.meta.json",
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/start_of_day_master_stack.md",
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/implementation_and_delivery_protocol.md",
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/patch_install_delivery_error_register.md",
    "kanda_prompt_workspace/prompt_library/HUMAN_APPENDIX/KANDA_HUMAN_PROJECT_ACTION_MENU_APPENDIX.md",
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/daily_patch_delivery_guardrails.md",
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/pre_output_contract_gates.md",
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md",
    "kanda_prompt_workspace/prompt_library/METADATA/implementation_and_delivery_protocol.meta.json",
    "kanda_prompt_workspace/prompt_library/METADATA/patch_install_delivery_error_register.meta.json",
    "kanda_prompt_workspace/prompt_library/METADATA/pre_output_contract_gates.meta.json",
    "kanda_prompt_workspace/prompt_library/METADATA/start_of_day_master_stack.meta.json",
    "tools/validate_terminal_cleanup_contract_startup_bridge_v1.py",
]

PROTECTED_ABSENT = [
    "kanda_reasoner_app/error_memory_gui/_ai_response_validator.py",
    "kanda_reasoner_app/error_memory_gui/_ai_prompt_builder.py",
    "kanda_reasoner_app/error_memory_gui/_memorize_flow.py",
    "kanda_reasoner_app/error_memory_gui/_ai_correction_action.py",
    "kanda_reasoner_app/error_memory_gui/_ai_correction_persistence.py",
    "kanda_reasoner_app/error_memory_gui/_lesson_status_summary.py",
    "kanda_reasoner_app/error_memory_gui/_table_view.py",
]


def _read(root: Path, rel: str) -> str:
    path = root / rel
    if not path.exists():
        raise AssertionError("Missing file: " + rel)
    return path.read_text(encoding="utf-8")


def _assert_contains(text: str, needle: str, rel: str) -> None:
    if needle not in text:
        raise AssertionError(rel + " missing: " + needle)


def _assert_prompt_contract(project_root: Path) -> None:
    contract_rel = CHANGED_FILES[0]
    contract = _read(project_root, contract_rel)
    for needle in [
        "prompt_id: terminal_cleanup_contract",
        "load_type: always_startup",
        "prompt_code: KPR-05-007",
        "Clean-prompt entry guard",
        "If `>>` is visible",
        "NONINTERACTIVE_AUTOMATION",
        "PHASE",
        "ERROR TYPE",
        "INSTALL_SUCCESS",
        "INSTALL_ERROR",
        "VALIDATION",
        "FREEZE",
        "RECOVERY",
        "INSTALL OK. Terminal will clear in 2 seconds...",
        "Start-Sleep -Seconds 2",
        "Read-Host \"Press Enter to clear terminal\"",
        "Read-Host \"Press Enter again to clear\"",
        "Do not mix the timed success footer and Enter, Enter footer.",
        "Do not use `exit`, `Stop-Process`, `Restart-Computer`",
        "Do not use inline `python -c`",
        "Paste-unit contract",
        "one complete paste unit",
        "Windows PowerShell 5.1-compatible APIs",
    ]:
        _assert_contains(contract, needle, contract_rel)
    if "wait 5 seconds" in contract or "5 second" in contract:
        raise AssertionError("terminal_cleanup_contract contains stale 5-second wording")


def _assert_startup_bridge(project_root: Path) -> None:
    rel = CHANGED_FILES[2]
    text = _read(project_root, rel)
    for needle in [
        "BEGINNING_OF_DAY_TERMINAL_CLEANUP_CONTRACT_BRIDGE_V1_START",
        "TERMINAL_CLEANUP_CONTRACT_STARTUP_BRIDGE",
        "KPR-05-007 terminal_cleanup_contract",
        "wait about 2 seconds",
        "ask for Enter, ask for Enter again",
        "Never close the terminal",
        "one independent paste unit",
        "do not use user-facing `else`, `elseif`, or `finally`",
    ]:
        _assert_contains(text, needle, rel)
    if "wait 5 seconds" in text or "5 second pause" in text:
        raise AssertionError("start_of_day_master_stack contains stale 5-second wording")


def _assert_references(project_root: Path) -> None:
    reference_files = [
        CHANGED_FILES[3],
        CHANGED_FILES[4],
        CHANGED_FILES[5],
        CHANGED_FILES[6],
        CHANGED_FILES[7],
        CHANGED_FILES[8],
    ]
    for rel in reference_files:
        text = _read(project_root, rel)
        _assert_contains(text, "terminal_cleanup_contract", rel)
        if rel.endswith("implementation_and_delivery_protocol.md"):
            if "wait 5 seconds" in text or "5 second pause" in text:
                raise AssertionError(rel + " contains stale 5-second implementation wording")
        if rel.endswith("KANDA_HUMAN_PROJECT_ACTION_MENU_APPENDIX.md"):
            if "wait 5 seconds" in text:
                raise AssertionError(rel + " contains stale 5-second human-facing wording")


def _assert_metadata(project_root: Path) -> None:
    meta = json.loads(_read(project_root, CHANGED_FILES[1]))
    if meta.get("prompt_id") != "terminal_cleanup_contract":
        raise AssertionError("terminal_cleanup_contract metadata prompt_id mismatch")
    if meta.get("load_type") != "always_startup":
        raise AssertionError("terminal_cleanup_contract must be always_startup")
    for rel in CHANGED_FILES[9:13]:
        data = json.loads(_read(project_root, rel))
        blob = json.dumps(data)
        if rel.endswith("start_of_day_master_stack.meta.json"):
            _assert_contains(blob, "BEGINNING_OF_DAY_TERMINAL_CLEANUP_CONTRACT_BRIDGE_V1_START", rel)
        else:
            _assert_contains(blob, "terminal_cleanup_contract", rel)


def _assert_zip_contract(project_root: Path) -> None:
    drive_root = Path(project_root.anchor)
    candidates = [
        drive_root / PATCH_NAME,
        drive_root / (project_root.name + "_delete_after_daily_work") / PATCH_NAME,
        Path(__file__).resolve().parents[1] / PATCH_NAME,
    ]
    zip_path = next((p for p in candidates if p.exists()), None)
    if zip_path is None:
        return
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    required = set(CHANGED_FILES) | {
        "INSTALL.ps1",
        "VALIDATE.ps1",
        "FREEZE.ps1",
        "PATCH_README.txt",
        "KANDA_FREEZE_HINT.json",
    }
    missing = sorted(required - names)
    if missing:
        raise AssertionError("ZIP missing required entries: " + repr(missing))
    forbidden = sorted(set(PROTECTED_ABSENT) & names)
    if forbidden:
        raise AssertionError("ZIP includes protected files: " + repr(forbidden))


def main() -> int:
    if len(sys.argv) > 1:
        project_root = Path(sys.argv[1]).resolve()
    else:
        project_root = Path(__file__).resolve().parents[1]
    for rel in CHANGED_FILES:
        path = project_root / rel
        if not path.exists():
            raise AssertionError("Missing changed file: " + rel)
        if path.suffix == ".py":
            py_compile.compile(str(path), doraise=True)
            lines = len(path.read_text(encoding="utf-8").splitlines())
            if lines > 500:
                raise AssertionError("Python file exceeds 500 lines: " + rel)
    _assert_prompt_contract(project_root)
    _assert_startup_bridge(project_root)
    _assert_references(project_root)
    _assert_metadata(project_root)
    _assert_zip_contract(project_root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
