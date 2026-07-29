"""Shared contract for the cross-project completion routine."""

from __future__ import annotations

import importlib.util
import json
import py_compile
import tempfile
from pathlib import Path

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
BRIDGE_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "12_generalized_project_canons/project_tool_boundary_startup_bridge.md"
)
FOLDER_CARD_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "05_patch_delivery_and_validation/_FOLDER_ASSIMILATION.md"
)
NAV_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "02_prompt_routing_and_indexing/prompt_navigation_index.md"
)
SOURCE_MAP_REL = Path(
    "kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json"
)
UI_REL = Path(
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/"
    "window_methods_private_impl.py"
)
HELPER_REL = Path(
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/"
    "answer_validate_freeze_memorize_button_private_impl.py"
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
        "version: 3.1",
        "canonical continuation wrapper",
        "KANDA_ANSWER_VALIDATE_FREEZE_MEMORIZE_CONTEXT",
        "Hard Tool-versus-Project boundary",
        "ROUTINE_POST_IMPLEMENTATION_COMPLETION",
        "INSTALLATION_FAILURE",
        "ANSWER VALIDATE FREEZE MEMORIZE ROUTINE IDENTITY",
        "Need new training prompt: NO",
        "Continue from the last reliable marker",
        "build one self-contained patch ZIP",
        "No ZIP link may be emitted alone",
        "INSTALL IS NOT VALIDATION",
        "VALIDATION OK: <feature_id>",
        "STATUS: IN_SYNC",
        "freeze_code_intake_and_form_protocol",
        "error_memory_active_ready_json_template",
        "KANDA_ERROR_LESSON_JSON_BEGIN",
        "Confirm and Write remains an explicit human action",
        "explicitly uses Memorize Error",
        "selected external Project does not become prompt-library authority",
        "return the completed user-facing answer",
        "Paste-safe PowerShell hard gate",
        "Every user-facing PowerShell code fence is one independent paste unit",
        "Windows PowerShell 5.1-compatible APIs",
        "lesson-powershell-detached-else-interactive-paste-footer-v1",
        "lesson-powershell-validation-wrapper-marker-and-finally-v1",
    )
    for marker in required:
        require(marker in text, "PROMPT_MARKER_" + marker)
    require(DEPRECATED_BRIDGE not in text.replace(
        "Never load or depend on deprecated `" + DEPRECATED_BRIDGE + "`.", ""
    ), "PROMPT_NO_DEPRECATED_OWNER")
    require(text.count("pre_output_contract_gates") == 1, "PROMPT_OWNER_UNIQUE_PRE_OUTPUT")
    require(len(text.splitlines()) <= 300, "PROMPT_LINE_LIMIT")


def validate_metadata(root: Path) -> None:
    data = json.loads(read_text(root, META_REL))
    require(data.get("prompt_id") == PROMPT_ID, "META_PROMPT_ID")
    require(data.get("prompt_code") == "KPR-05-005", "META_PROMPT_CODE")
    require(data.get("version") == "3.1", "META_VERSION")
    require(data.get("status") == "active", "META_STATUS")
    require(data.get("load_type") == "on_request", "META_LOAD_TYPE")
    required = list(data.get("required_companion_prompts") or [])
    optional = list(data.get("optional_companion_prompts") or [])
    require(len(required) == len(set(required)), "META_REQUIRED_UNIQUE")
    require(len(optional) == len(set(optional)), "META_OPTIONAL_UNIQUE")
    expected_required = {
        "project_tool_boundary_canon",
        "brick_wall_comprehensive_quality_gate",
        "bundle_gated_development_workflow",
        "implementation_and_delivery_protocol",
        "pre_output_contract_gates",
        "patch_install_delivery_error_register",
        "terminal_cleanup_contract",
    }
    require(set(required) == expected_required, "META_REQUIRED_OWNER_SET")
    expected_optional = {
        "freeze_code_intake_and_form_protocol",
        "error_memory_ai_formulary_startup_canon",
        "error_memory_active_ready_correction_blueprint",
        "error_memory_active_ready_json_template",
        "error_memory_model_template",
    }
    require(set(optional) == expected_optional, "META_OPTIONAL_OWNER_SET")
    require(DEPRECATED_BRIDGE not in required + optional, "META_NO_DEPRECATED_BRIDGE")


def validate_bridge_and_navigation(root: Path) -> None:
    bridge = read_text(root, BRIDGE_REL)
    for marker in (
        "version: 2.0",
        "Cross-project release ownership",
        "patch payload owner            = active_project_root",
        "Freeze intake and memory       = active_project_support_root",
        "canonical routine prompt       = tool_source_root",
        "must not ask the user to retrain it",
        "Installation is not validation",
    ):
        require(marker in bridge, "BRIDGE_MARKER_" + marker)
    source_map = json.loads(read_text(root, SOURCE_MAP_REL))
    sources = source_map.get("sources") or source_map.get("startup_sources") or []
    matches = [
        item for item in sources
        if item.get("prompt_id") == "project_tool_boundary_startup_bridge"
    ]
    require(len(matches) == 1, "SOURCE_MAP_BRIDGE_IDENTITY")
    require(
        matches[0].get("generated_filename") == "14_project_tool_boundary_canon.md",
        "SOURCE_MAP_BRIDGE_GENERATED_FILENAME",
    )
    card = read_text(root, FOLDER_CARD_REL)
    require("`router_bridge_patch_delivery_contract`: deprecated" in card, "CARD_DEPRECATED_BRIDGE")
    require("`pre_output_contract_gates` and `implementation_and_delivery_protocol` must not" in card, "CARD_ACTIVE_OWNER_NOT_TOMBSTONE")
    nav = read_text(root, NAV_REL)
    require("without retraining" in nav, "NAV_NO_RETRAINING_ROUTE")


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
        "resolved selected Project",
        "answer_validate_freeze_memorize_button_private_impl",
        "copy_answer_validate_freeze_memorize_to_clipboard(self)",
    ):
        require(marker in ui, "UI_MARKER_" + marker)
    require("patch_validate_freeze_error_memory_routine_blueprint.md" not in ui, "UI_NO_SELECTED_PROJECT_PROMPT_AUTHORITY")
    for marker in (
        "KANDA_ANSWER_VALIDATE_FREEZE_MEMORIZE_CONTEXT_BEGIN",
        "Selected project source root:",
        "KANDA Reasoner tool root:",
        "Selected Project Support root:",
        "Selected project-linked transient root:",
        "Canonical prompt source:",
        "Need new training prompt: NO",
        "PowerShell paste rule:",
    ):
        require(marker.lower() in helper.lower(), "HELPER_MARKER_" + marker)
    py_compile.compile(str(root / UI_REL), doraise=True)
    py_compile.compile(str(root / HELPER_REL), doraise=True)
    require(len(ui.splitlines()) <= 500, "UI_MODULE_LINE_LIMIT")
    require(len(helper.splitlines()) <= 500, "HELPER_MODULE_LINE_LIMIT")

    module = _load_button_helper(root)
    with tempfile.TemporaryDirectory(prefix="kanda_cross_project_") as tmp:
        tmp_root = Path(tmp)
        external_project = tmp_root / "eeg_kanda"
        external_project.mkdir()
        wrapped = module.build_answer_validate_freeze_memorize_wrapper(
            external_project,
            tool_root=root,
        )
        expected_support = external_project.parent / "eeg_kanda_show_project_to_AI"
        expected_transient = external_project.parent / "eeg_kanda_delete_after_daily_work"
        require("Selected project slug: eeg_kanda" in wrapped, "WRAPPER_EXTERNAL_SLUG")
        require("Selected project source root: " + str(external_project.resolve()) in wrapped, "WRAPPER_EXTERNAL_ROOT")
        require("Same physical root: NO" in wrapped, "WRAPPER_EXTERNAL_SAME_PHYSICAL")
        require("Selected Project Support root: " + str(expected_support.resolve()) in wrapped, "WRAPPER_EXTERNAL_SUPPORT")
        require("Selected project-linked transient root: " + str(expected_transient.resolve()) in wrapped, "WRAPPER_EXTERNAL_TRANSIENT")
        require("Canonical prompt source: " + str((root / PROMPT_REL).resolve()) in wrapped, "WRAPPER_TOOL_PROMPT_SOURCE")
        require("Need new training prompt: NO" in wrapped, "WRAPPER_NO_RETRAINING")
        require("PowerShell paste rule:" in wrapped, "WRAPPER_PASTE_SAFE_RULE")
        self_host = module.build_answer_validate_freeze_memorize_wrapper(root, tool_root=root)
        require("Same physical root: YES" in self_host, "WRAPPER_SELF_HOST_SAME_PHYSICAL")


def validate_all(root: Path) -> None:
    validate_prompt(root)
    validate_metadata(root)
    validate_bridge_and_navigation(root)
    validate_button(root)
