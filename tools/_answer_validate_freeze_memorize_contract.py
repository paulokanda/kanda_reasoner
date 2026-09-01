"""Shared contract for the cross-project completion routine."""

from __future__ import annotations

import importlib.util
import json
import py_compile
import tempfile
from pathlib import Path

__all__ = ["HELPER_REL", "validate_all"]

PROMPT_ID = "patch_validate_freeze_error_memory_routine_blueprint"
PROMPT_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "05_patch_delivery_and_validation/"
    "patch_validate_freeze_error_memory_routine_blueprint.md"
)
META_REL = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "patch_validate_freeze_error_memory_routine_blueprint.meta.json"
)
UI_REL = Path(
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/"
    "window_methods_private_impl.py"
)
HELPER_REL = Path(
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/"
    "answer_validate_freeze_memorize_button_private_impl.py"
)
TERMINAL_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "05_patch_delivery_and_validation/terminal_cleanup_contract.md"
)
TERMINAL_META_REL = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/terminal_cleanup_contract.meta.json"
)
DEPRECATED_BRIDGE = "router_bridge_patch_delivery_contract"


def require(condition: bool, marker: str) -> None:
    if not condition:
        raise AssertionError(marker + ": FAIL")


def read_text(root: Path, relative: Path) -> str:
    path = root / relative
    require(path.is_file(), "MISSING_FILE_" + relative.as_posix())
    return path.read_text(encoding="utf-8-sig")


def validate_prompt(root: Path) -> None:
    text = read_text(root, PROMPT_REL)
    required = (
        "version: 4.2",
        "source_stage: error-memory-pre-output-prevention-hard-gate-v1",
        "canonical continuation wrapper",
        "Pre-response continuation hard gate",
        "CURRENT LIFECYCLE POINTER",
        "First incomplete phase:",
        "never repeat a completed phase",
        "current release identity",
        "Do not request another",
        "Do not prepare a duplicate Freeze",
        "invalidates only downstream evidence",
        "fail closed",
        "KANDA_ANSWER_VALIDATE_FREEZE_MEMORIZE_CONTEXT",
        "Hard Tool-versus-Project boundary",
        "ROUTINE_POST_IMPLEMENTATION_COMPLETION",
        "Need new training prompt: NO",
        "One self-contained feature ZIP",
        "Terminal - INSTALL then VALIDATE",
        "same pasted outer block starts VALIDATE",
        "INSTALL IS NOT VALIDATION",
        "If INSTALL",
        "stop before VALIDATE",
        "VALIDATE failure: stop before Freeze",
        "stop before Freeze",
        "VALIDATION OK: <feature_id>",
        "STATUS: IN_SYNC",
        "FREEZE DISPOSITION: PREPARED_FOR_HUMAN_CONFIRMATION",
        "freeze_candidate_pre_output_audit",
        "Confirm and Write remain human-only",
        "ERROR MEMORY DISPOSITION: NOT_REQUIRED",
        "Memorize Error` remains human-only",
        "Never concatenate",
        "*_VALIDATION_REPORT.txt",
        "Every user-facing PowerShell fence is one independent paste unit",
        "Windows PowerShell 5.1-compatible APIs",
    )
    for marker in required:
        require(marker in text, "PROMPT_MARKER_" + marker)
    require(
        DEPRECATED_BRIDGE not in text.replace(
            "Never load deprecated `" + DEPRECATED_BRIDGE + "`.", ""
        ),
        "PROMPT_NO_DEPRECATED_OWNER",
    )
    require(len(text.splitlines()) <= 300, "PROMPT_LINE_LIMIT")
    require(
        "One terminal block never executes two lifecycle phases" not in text,
        "OLD_STRICT_PHASE_ISOLATION_REMOVED",
    )


def validate_metadata(root: Path) -> None:
    data = json.loads(read_text(root, META_REL))
    require(data.get("prompt_id") == PROMPT_ID, "META_PROMPT_ID")
    require(data.get("prompt_code") == "KPR-05-005", "META_PROMPT_CODE")
    require(data.get("version") == "4.2", "META_VERSION")
    require(
        data.get("source_stage") == "error-memory-pre-output-prevention-hard-gate-v1",
        "META_SOURCE_STAGE",
    )
    require(data.get("status") == "active", "META_STATUS")
    require(data.get("load_type") == "on_request", "META_LOAD_TYPE")


def validate_terminal_contract(root: Path) -> None:
    text = read_text(root, TERMINAL_REL)
    meta = json.loads(read_text(root, TERMINAL_META_REL))
    for marker in (
        "version: 2.5",
        "Chained INSTALL -> VALIDATE continuation",
        "Enter",
        "Enter again",
        "Clear-Host",
        "same already-pasted outer",
        "If INSTALL fails or throws",
        "Do not put validation logic inside `INSTALL.ps1`",
        "and do not put installation",
    ):
        require(marker in text, "TERMINAL_MARKER_" + marker)
    require("Start-Sleep -Seconds 2" not in text, "TERMINAL_NO_TIMED_CLEAR")
    require(meta.get("version") == "2.5", "TERMINAL_META_VERSION")
    require(
        meta.get("source_stage") == "chained-install-validate-terminal-continuation-v1",
        "TERMINAL_META_SOURCE_STAGE",
    )


def _load_button_helper(root: Path):
    path = root / HELPER_REL
    spec = importlib.util.spec_from_file_location("kanda_answer_routine_helper", path)
    require(spec is not None and spec.loader is not None, "HELPER_IMPORT_SPEC")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_button(root: Path) -> None:
    ui = read_text(root, UI_REL)
    helper = read_text(root, HELPER_REL)
    for marker in (
        "Answer, Validate, Freeze, Memorize Error",
        "Install + Validate Flow",
        "Install -> Enter x2 -> Clear-Host -> Validate",
        "answer_validate_freeze_memorize_button_private_impl",
        "copy_answer_validate_freeze_memorize_to_clipboard(self)",
        "terminal_cleanup_contract.md",
    ):
        require(marker in ui, "UI_MARKER_" + marker)
    for marker in (
        "Terminal chain rule:",
        "Stop rule:",
        "Freeze rule:",
        "Error Memory end rule:",
        "PowerShell paste rule:",
    ):
        require(marker in helper, "HELPER_MARKER_" + marker)
    require(
        "separate INSTALL, VALIDATE, FREEZE, and ERROR MEMORY terminal blocks"
        not in helper,
        "HELPER_OLD_SEPARATE_RULE_REMOVED",
    )
    py_compile.compile(str(root / UI_REL), doraise=True)
    py_compile.compile(str(root / HELPER_REL), doraise=True)
    require(len(ui.splitlines()) <= 500, "UI_MODULE_LINE_LIMIT")
    require(len(helper.splitlines()) <= 500, "HELPER_MODULE_LINE_LIMIT")

    module = _load_button_helper(root)
    with tempfile.TemporaryDirectory(prefix="kanda_chain_") as tmp:
        external_project = Path(tmp) / "eeg_kanda"
        external_project.mkdir()
        wrapped = module.build_answer_validate_freeze_memorize_wrapper(
            external_project,
            tool_root=root,
        )
        require("Terminal chain rule:" in wrapped, "WRAPPER_CHAIN_RULE")
        require("Stop rule:" in wrapped, "WRAPPER_STOP_RULE")
        require("Pre-response continuation hard gate" in wrapped, "WRAPPER_CONTINUATION_HARD_GATE")
        require("CURRENT LIFECYCLE POINTER" in wrapped, "WRAPPER_LIFECYCLE_POINTER")
        require("version: 4.2" in wrapped, "WRAPPER_PROMPT_VERSION")
        require(
            "INSTALL -> Enter -> Enter -> Clear-Host -> VALIDATE" in wrapped,
            "WRAPPER_CHAIN_SEQUENCE",
        )


def validate_all(root: Path) -> None:
    validate_prompt(root)
    validate_metadata(root)
    validate_terminal_contract(root)
    validate_button(root)
