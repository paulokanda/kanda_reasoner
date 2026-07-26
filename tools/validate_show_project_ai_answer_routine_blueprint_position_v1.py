"""Validate the current Show Project to AI recovery wrapper contract."""

from __future__ import annotations

import json
import py_compile
import sys
from pathlib import Path

__all__: list[str] = []

PROMPT_ID = "patch_validate_freeze_error_memory_routine_blueprint"
PROMPT_REL = (
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "05_patch_delivery_and_validation/"
    "patch_validate_freeze_error_memory_routine_blueprint.md"
)
META_REL = (
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "patch_validate_freeze_error_memory_routine_blueprint.meta.json"
)
UI_REL = (
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/"
    "window_methods_private_impl.py"
)


def require(condition: bool, marker: str) -> None:
    if not condition:
        raise AssertionError(marker + ": FAIL")


def read_text(root: Path, rel: str) -> str:
    path = root / rel
    require(path.is_file(), "MISSING_FILE_" + rel)
    return path.read_text(encoding="utf-8-sig")


def version_tuple(value: object) -> tuple[int, ...]:
    return tuple(int(part) for part in str(value).split("."))


def validate_wrapper(root: Path) -> None:
    text = read_text(root, PROMPT_REL)
    required = (
        "prompt_id: patch_validate_freeze_error_memory_routine_blueprint",
        "prompt_code: KPR-05-005",
        "This prompt is a thin wrapper",
        "STARTUP_DELIVERY_FAILURE",
        "PROJECT_HANDOFF_FAILURE",
        "PATCH_BUILD_OR_DELIVERY_FAILURE",
        "VALIDATION_FAILURE",
        "FREEZE_INTAKE_FAILURE",
        "ERROR_MEMORY_INTAKE_FAILURE",
        "project_tool_boundary_canon",
        "bundle_gated_development_workflow",
        "implementation_and_delivery_protocol",
        "router_bridge_patch_delivery_contract",
        "pre_output_contract_gates",
        "patch_install_delivery_error_register",
        "terminal_cleanup_contract",
        "freeze_code_intake_and_form_protocol",
        "diagnose exact failure",
        "RECOVERY ROUTINE BLOCKED",
        "May freeze: NO",
        "does not authorize implementation",
    )
    for marker in required:
        require(marker in text, "WRAPPER_MARKER_" + marker)
    forbidden = (
        "KANDA_ERROR_LESSON_JSON_BEGIN",
        "KANDA_ERROR_LESSON_JSON_END",
        "Windows 11 Install code contract",
        "combined Windows 11 PowerShell terminal block",
        "pending_ai_assisted_error_lesson_intake",
        "FREEZE_HINT_EVIDENCE_MERGE_OK: <feature_id>",
    )
    for marker in forbidden:
        require(marker not in text, "WRAPPER_DUPLICATED_DOCTRINE_" + marker)
    require(len(text.splitlines()) <= 180, "WRAPPER_LINE_LIMIT")


def validate_metadata(root: Path) -> None:
    data = json.loads(read_text(root, META_REL))
    require(data.get("prompt_id") == PROMPT_ID, "META_PROMPT_ID")
    require(data.get("prompt_code") == "KPR-05-005", "META_PROMPT_CODE")
    require(version_tuple(data.get("version", "0")) >= (2, 0), "META_VERSION")
    require(data.get("status") == "active", "META_STATUS")
    require(data.get("load_type") == "on_request", "META_LOAD_TYPE")
    required = set(data.get("required_companion_prompts") or [])
    optional = set(data.get("optional_companion_prompts") or [])
    require(required == {"project_tool_boundary_canon", "brick_wall_comprehensive_quality_gate"}, "META_REQUIRED_OWNER_SET")
    require(
        {
            "bundle_gated_development_workflow",
            "implementation_and_delivery_protocol",
            "pre_output_contract_gates",
            "patch_install_delivery_error_register",
            "terminal_cleanup_contract",
            "freeze_code_intake_and_form_protocol",
        }.issubset(optional),
        "META_OPTIONAL_OWNER_DISPATCH",
    )
    require("dynamic project-linked daily-work staging" not in str(data.get("description") or "").lower(), "META_NO_EMBEDDED_STAGING_DOCTRINE")


def validate_ui(root: Path) -> None:
    text = read_text(root, UI_REL)
    required = (
        "AI answer Routine Blueprint:",
        "copy_patch_validate_freeze_routine_button",
        "Answer, Validate, Freeze, Memorize Error",
        "patch_validate_freeze_error_memory_routine_blueprint.md",
        "QApplication.clipboard().setText",
        "project_root / prompt_rel",
    )
    for marker in required:
        require(marker in text, "UI_MARKER_" + marker)
    require("Downloads" not in text and "Desktop" not in text, "UI_NO_GENERIC_FALLBACK")
    py_compile.compile(str(root / UI_REL), doraise=True)


FEATURE_ID = "show-project-ai-answer-routine-blueprint-position-v1"


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    validate_wrapper(root)
    validate_metadata(root)
    validate_ui(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
