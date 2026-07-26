"""Smoke coverage for Batch 16 public contracts and active helpers."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

_PROMPT_TOOLS = Path(__file__).resolve().parents[1] / "kanda_prompt_workspace" / "prompt_tools"
_PROMPT_TOOLS_TEXT = str(_PROMPT_TOOLS)
if _PROMPT_TOOLS_TEXT not in sys.path:
    sys.path.insert(0, _PROMPT_TOOLS_TEXT)

import startup_kernel.boot_text as startup_boot_text
import startup_kernel.constants as startup_constants
import startup_kernel.core_helpers as startup_core_helpers
import startup_kernel.generic_helpers as startup_generic_helpers
import startup_kernel.paste_after_uploading_body as startup_paste_after_uploading_body
import startup_kernel.paste_readme_text as startup_paste_readme_text
import startup_kernel.prompt_library_manifest as startup_prompt_library_manifest
import startup_kernel.prompt_library_payload as startup_prompt_library_payload
import startup_kernel.prompt_library_zip as startup_prompt_library_zip
import startup_kernel.read_order as startup_read_order
import startup_kernel.readme_body as startup_readme_body
import startup_kernel.source_resolution as startup_source_resolution
import startup_kernel.start_here_body_intro as startup_start_here_body_intro
import startup_kernel.start_here_body_routing as startup_start_here_body_routing
import startup_kernel.start_here_lists as startup_start_here_lists
import startup_kernel.start_here_text as startup_start_here_text
import startup_kernel.startup_literal_texts as startup_literal_texts
import startup_kernel.startup_names as startup_names
import startup_kernel.startup_source_map as startup_source_map
import startup_kernel.zip_contract as startup_zip_contract
import startup_kernel.zip_delivery as startup_zip_delivery

import kanda_reasoner_app.error_memory_gui._clipboard_export as clipboard_export
import kanda_reasoner_app.error_memory_gui._correction_guard as correction_guard
import kanda_reasoner_app.error_memory_gui._intake_actions_mixin as intake_actions_mixin
import kanda_reasoner_app.error_memory_gui._intake_blueprint as intake_blueprint
import kanda_reasoner_app.error_memory_gui._lesson_actions as lesson_actions
import kanda_reasoner_app.error_memory_gui._memorize_flow as memorize_flow
import kanda_reasoner_app.error_memory_gui._pending_rows as pending_rows
import kanda_reasoner_app.error_memory_gui._project_roots as project_roots
import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help._action_summary as action_summary
import kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help._run_execution as run_execution
import scripts.validate_architecture_warning_cleanup_batch13_public_surface_docstrings_v1 as batch13_validator
import scripts.validate_architecture_warning_cleanup_batch14_import_side_effects_v1 as batch14_validator
import scripts.validate_bridge_error_memory_implementation_error_gate_v1 as bridge_validator
import scripts.validate_complete_bridge_list_button_v1 as complete_bridge_validator
import scripts.validate_error_memory_tab_refactor_completion_guard_v1 as error_tab_completion_validator
import scripts.validate_error_memory_tab_refactor_train_car_1_v1 as error_tab_train_car_validator
import scripts.validate_startup_code_module_size_bridge_visible_v1 as size_bridge_validator
import scripts.validate_terminal_cleanup_bridge_initial_prompts_v1 as terminal_bridge_validator
import tools.validate_error_memory_tab_pending_loader_refactor_v1 as pending_loader_validator
import tools.validate_large_module_v70_context_validator_correction_v1 as large_module_validator
import tools.validate_router_bridge_module_size_law_v1 as router_bridge_validator

# Static architecture coverage only. These imports are intentionally guarded so
# headless validation does not require Qt/PySide6 or package-mode startup-kernel imports.
if TYPE_CHECKING:
    import kanda_prompt_workspace.prompt_tools.startup_kernel.boot_text as pkg_startup_boot_text
    import kanda_prompt_workspace.prompt_tools.startup_kernel.constants as pkg_startup_constants
    import kanda_prompt_workspace.prompt_tools.startup_kernel.core_helpers as pkg_startup_core_helpers
    import kanda_prompt_workspace.prompt_tools.startup_kernel.generic_helpers as pkg_startup_generic_helpers
    import kanda_prompt_workspace.prompt_tools.startup_kernel.paste_after_uploading_body as pkg_startup_paste_after_uploading_body
    import kanda_prompt_workspace.prompt_tools.startup_kernel.paste_readme_text as pkg_startup_paste_readme_text
    import kanda_prompt_workspace.prompt_tools.startup_kernel.prompt_library_manifest as pkg_startup_prompt_library_manifest
    import kanda_prompt_workspace.prompt_tools.startup_kernel.prompt_library_payload as pkg_startup_prompt_library_payload
    import kanda_prompt_workspace.prompt_tools.startup_kernel.prompt_library_zip as pkg_startup_prompt_library_zip
    import kanda_prompt_workspace.prompt_tools.startup_kernel.read_order as pkg_startup_read_order
    import kanda_prompt_workspace.prompt_tools.startup_kernel.readme_body as pkg_startup_readme_body
    import kanda_prompt_workspace.prompt_tools.startup_kernel.source_resolution as pkg_startup_source_resolution
    import kanda_prompt_workspace.prompt_tools.startup_kernel.start_here_body_intro as pkg_startup_start_here_body_intro
    import kanda_prompt_workspace.prompt_tools.startup_kernel.start_here_body_routing as pkg_startup_start_here_body_routing
    import kanda_prompt_workspace.prompt_tools.startup_kernel.start_here_lists as pkg_startup_start_here_lists
    import kanda_prompt_workspace.prompt_tools.startup_kernel.start_here_text as pkg_startup_start_here_text
    import kanda_prompt_workspace.prompt_tools.startup_kernel.startup_literal_texts as pkg_startup_literal_texts
    import kanda_prompt_workspace.prompt_tools.startup_kernel.startup_names as pkg_startup_names
    import kanda_prompt_workspace.prompt_tools.startup_kernel.startup_source_map as pkg_startup_source_map
    import kanda_prompt_workspace.prompt_tools.startup_kernel.zip_contract as pkg_startup_zip_contract
    import kanda_prompt_workspace.prompt_tools.startup_kernel.zip_delivery as pkg_startup_zip_delivery
    import kanda_reasoner_app.error_memory_gui._project_paths_mixin as error_project_paths_mixin
    import kanda_reasoner_app.freeze_after_update_gui._local_ai_formulary as freeze_local_ai_formulary
    import kanda_reasoner_app.templates.green_sonar_monitor as green_sonar_monitor

_RUNTIME_MODULES = (
    startup_boot_text,
    startup_constants,
    startup_core_helpers,
    startup_generic_helpers,
    startup_paste_after_uploading_body,
    startup_paste_readme_text,
    startup_prompt_library_manifest,
    startup_prompt_library_payload,
    startup_prompt_library_zip,
    startup_read_order,
    startup_readme_body,
    startup_source_resolution,
    startup_start_here_body_intro,
    startup_start_here_body_routing,
    startup_start_here_lists,
    startup_start_here_text,
    startup_literal_texts,
    startup_names,
    startup_source_map,
    startup_zip_contract,
    startup_zip_delivery,
    clipboard_export,
    correction_guard,
    intake_actions_mixin,
    intake_blueprint,
    lesson_actions,
    memorize_flow,
    pending_rows,
    project_roots,
    action_summary,
    run_execution,
    batch13_validator,
    batch14_validator,
    bridge_validator,
    complete_bridge_validator,
    error_tab_completion_validator,
    error_tab_train_car_validator,
    size_bridge_validator,
    terminal_bridge_validator,
    pending_loader_validator,
    large_module_validator,
    router_bridge_validator,
)

_STATIC_ONLY_TARGETS = (
    "kanda_prompt_workspace.prompt_tools.startup_kernel.boot_text",
    "kanda_prompt_workspace.prompt_tools.startup_kernel.constants",
    "kanda_prompt_workspace.prompt_tools.startup_kernel.core_helpers",
    "kanda_prompt_workspace.prompt_tools.startup_kernel.generic_helpers",
    "kanda_prompt_workspace.prompt_tools.startup_kernel.source_resolution",
    "kanda_reasoner_app.error_memory_gui._project_paths_mixin",
    "kanda_reasoner_app.freeze_after_update_gui._local_ai_formulary",
    "kanda_reasoner_app.templates.green_sonar_monitor",
)


def test_batch16_runtime_safe_public_contracts_are_importable() -> None:
    """Verify selected runtime-safe public modules remain directly importable."""

    for module in _RUNTIME_MODULES:
        assert module.__name__


def test_batch16_static_only_contract_targets_are_declared() -> None:
    """Document headless-safe static coverage for GUI/package-path targets."""

    assert len(_STATIC_ONLY_TARGETS) == 8
    assert "kanda_reasoner_app.templates.green_sonar_monitor" in _STATIC_ONLY_TARGETS
