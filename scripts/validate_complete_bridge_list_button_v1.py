"""Validate Complete Bridge List button and dynamic bridge discovery."""

from __future__ import annotations

import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

__all__: list[str] = []


PROJECT_ROOT = Path(__file__).resolve().parents[1]

def _ensure_project_root_on_path() -> None:
    """Add the project root to sys.path only for direct script execution."""
    root_text = str(PROJECT_ROOT)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)

HELPER_PATH = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_tools_shell" / "runner_help" / "complete_bridge_list_private_impl.py"
WINDOW_PATH = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_tools_shell" / "runner_help" / "window_methods_private_impl.py"
METADATA_HELPER_PATH = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_tools_shell" / "runner_help" / "bridge_metadata_classification.py"
WRAPPER_PATH = PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_tools_shell" / "runner_help" / "bridge_list_wrapper_buttons_private_impl.py"



def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _assert_ascii(path: Path) -> None:
    text = _read(path)
    bad = [char for char in text if ord(char) > 127]
    _assert(not bad, "non-ASCII character found in " + str(path))


def _assert_line_count(path: Path, maximum: int = 500) -> None:
    count = len(_read(path).splitlines())
    _assert(count <= maximum, str(path) + " has more than " + str(maximum) + " lines: " + str(count))


def _fixture_show_root(root: Path) -> Path:
    return root.parent / (root.name + "_show_project_to_AI")


def _fixture_first_prompt_files_dir(root: str | Path) -> Path:
    return _fixture_show_root(Path(root)) / "first_prompt_files"


def _fixture_freeze_after_update_dir(root: str | Path) -> Path:
    return _fixture_show_root(Path(root)) / "project_freeze_after_update"


def _make_startup_zip(zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            "00_START_HERE_FOR_AI.md",
            "# Startup\n\n## Beginning-of-day active bridges\n\n## Code Module Size Bridge\nIdeal 400 lines. Maximum 500 lines.\n",
        )
        archive.writestr(
            "05_start_of_day_master_stack.md",
            "# Stack\n\n## Code Module Size Bridge\nIdeal code module size: 400 lines or fewer. Maximum code module size: 500 lines or fewer.\n",
        )
        archive.writestr(
            "02_prompt_navigation_index.md",
            "router_bridge_governed_implementation\nrouter_bridge_patch_delivery_contract\n",
        )
        archive.writestr("03_GROUP_ASSIMILATION_INDEX.md", "No bridge here.\n")
        archive.writestr("07_daily_patch_delivery_guardrails.md", "Patch delivery bridge active.\n")
        archive.writestr("09_active_project_freeze_context.md", "freeze bridge memory active.\n")
        archive.writestr(
            "14_project_tool_boundary_canon.md",
            "---\nprompt_id: project_tool_boundary_startup_bridge\nstatus: active\nload_type: always_startup\n---\n# Project Tool Boundary Startup Bridge\n",
        )


def _make_prompt_library_zip(zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            "ACTIVE_PROMPTS/05_patch_delivery_and_validation/router_bridge_zip_fixture_dynamic.md",
            "---\nprompt_id: router_bridge_zip_fixture_dynamic\nstatus: active\nload_type: routed\n---\n# ZIP Fixture Dynamic Bridge\n",
        )
        archive.writestr(
            "ACTIVE_PROMPTS/05_patch_delivery_and_validation/router_bridge_zip_deprecated.md",
            "---\nprompt_id: router_bridge_zip_deprecated\nstatus: deprecated\nload_type: never\nactive_route: false\n---\n# Deprecated ZIP Bridge\n",
        )
        archive.writestr(
            "ACTIVE_PROMPTS/12_generalized_project_canons/project_tool_boundary_startup_bridge.md",
            "---\nprompt_id: project_tool_boundary_startup_bridge\nstatus: active\nload_type: always_startup\n---\n# Project Tool Boundary Startup Bridge\n",
        )


def _write_fixture_project(root: Path) -> Path:
    prompt_dir = root / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS"
    startup_dir = prompt_dir / "01_session_start_and_navigation"
    patch_dir = prompt_dir / "05_patch_delivery_and_validation"
    routing_dir = prompt_dir / "02_prompt_routing_and_indexing"
    startup_dir.mkdir(parents=True)
    patch_dir.mkdir(parents=True)
    routing_dir.mkdir(parents=True)
    (startup_dir / "start_of_day_master_stack.md").write_text(
        "# Start\n\n## Box Logic Startup Bridge\n\n## Code Module Size Bridge\nIdeal code module size: 400 lines or fewer. Maximum code module size: 500 lines or fewer.\n",
        encoding="utf-8",
    )
    (patch_dir / "router_bridge_governed_implementation.md").write_text(
        "---\nprompt_id: router_bridge_governed_implementation\nstatus: deprecated\nload_type: never\nactive_route: false\n---\n# Governed Implementation Bridge\n",
        encoding="utf-8",
    )
    (patch_dir / "router_bridge_patch_delivery_contract.md").write_text(
        "---\nprompt_id: router_bridge_patch_delivery_contract\nstatus: deprecated\nload_type: never\nactive_route: false\n---\n# Patch Delivery Bridge\n",
        encoding="utf-8",
    )
    (patch_dir / "router_bridge_user_detected_correction.md").write_text(
        "---\nprompt_id: router_bridge_user_detected_correction\nstatus: active\nload_type: routed\n---\n# User-Detected Correction Incident Dispatcher\n",
        encoding="utf-8",
    )
    boundary_dir = prompt_dir / "12_generalized_project_canons"
    boundary_dir.mkdir(parents=True)
    (boundary_dir / "project_tool_boundary_startup_bridge.md").write_text(
        "---\nprompt_id: project_tool_boundary_startup_bridge\nstatus: active\nload_type: always_startup\n---\n# Project Tool Boundary Startup Bridge\n",
        encoding="utf-8",
    )
    (routing_dir / "prompt_navigation_index.md").write_text(
        "router_bridge_governed_implementation\nrouter_bridge_patch_delivery_contract\n",
        encoding="utf-8",
    )

    prompt_tools = root / "kanda_prompt_workspace" / "prompt_tools"
    prompt_tools.mkdir(parents=True)
    (prompt_tools / "STARTUP_ROUTING_KERNEL_SOURCES.json").write_text(
        '{"startup_sources":[{"load_order":11,"canonical_source":"prompt_library/ACTIVE_PROMPTS/12_generalized_project_canons/project_tool_boundary_startup_bridge.md","generated_filename":"14_project_tool_boundary_canon.md","prompt_id":"project_tool_boundary_startup_bridge","load_mode":"always_startup","role":"Tool versus Project startup bridge"}]}\n',
        encoding="utf-8",
    )

    first_prompt_dir = _fixture_first_prompt_files_dir(root)
    first_prompt_dir.mkdir(parents=True)
    (first_prompt_dir / "tell_AI_read_before_all.md").write_text(
        "# Tell AI\n\n## Beginning-of-day active bridges\n\n## Code Module Size Bridge\nIdeal 400 lines. Maximum 500 lines.\n",
        encoding="utf-8",
    )
    _make_startup_zip(first_prompt_dir / "first_prompts_to_ai.zip")
    _make_prompt_library_zip(first_prompt_dir / "prompt_library.zip")

    frozen_dir = _fixture_freeze_after_update_dir(root) / "frozen_features_memory" / "entries"
    frozen_dir.mkdir(parents=True)
    (frozen_dir / "freeze-bridge-test.md").write_text(
        "---\nfreeze_id: \"freeze-bridge-test\"\nfeature_title: \"Beginning-of-Day Code Module Size Bridge Visibility v1\"\n---\n# Frozen Bridge\n",
        encoding="utf-8",
    )
    return root


def validate_static_files() -> None:
    _assert(HELPER_PATH.is_file(), "helper file missing")
    _assert(WINDOW_PATH.is_file(), "window file missing")
    _assert(METADATA_HELPER_PATH.is_file(), "metadata helper file missing")
    _assert(WRAPPER_PATH.is_file(), "wrapper file missing")
    _assert_ascii(HELPER_PATH)
    _assert_ascii(WINDOW_PATH)
    _assert_ascii(METADATA_HELPER_PATH)
    _assert_ascii(WRAPPER_PATH)
    _assert_line_count(HELPER_PATH)
    _assert_line_count(WINDOW_PATH)
    _assert_line_count(METADATA_HELPER_PATH)
    _assert_line_count(WRAPPER_PATH)

    helper_text = _read(HELPER_PATH)
    metadata_helper_text = _read(METADATA_HELPER_PATH)
    wrapper_text = _read(WRAPPER_PATH)
    window_text = _read(WINDOW_PATH)
    required_helper_fragments = [
        "KANDA_COMPLETE_BRIDGE_LIST_BEGIN",
        "KANDA_COMPLETE_BRIDGE_LIST_END",
        "ACTIVE STARTUP BRIDGES",
        "ON-DEMAND BRIDGES",
        "FROZEN BRIDGE MEMORIES",
        "A bridge is a direction sign",
        "analysis_first_prompt_files_dir",
        "analysis_project_freeze_after_update_dir",
        "prompt_library.zip",
        "PurePosixPath",
        "SELECTED PROJECT FEATURE HANDLING CHECKLIST",
        "_is_active_on_demand_bridge",
    ]
    for fragment in required_helper_fragments:
        _assert(fragment in helper_text, "missing helper fragment: " + fragment)
    for fragment in (
        "STARTUP_ROUTING_KERNEL_SOURCES.json",
        "is_active_on_demand_bridge",
        "always_startup",
        "never",
        "active_route",
    ):
        _assert(fragment in metadata_helper_text, "missing metadata helper fragment: " + fragment)

    required_wrapper_fragments = [
        "KANDA_STARTUP_BRIDGE_LIST_BEGIN",
        "KANDA_ON_DEMAND_BRIDGE_LIST_BEGIN",
        "build_startup_bridge_list",
        "build_on_demand_bridge_list",
        "dynamic complete bridge list",
    ]
    for fragment in required_wrapper_fragments:
        _assert(fragment in wrapper_text, "missing wrapper fragment: " + fragment)

    required_window_fragments = [
        "Bridges:",
        "copy_startup_bridge_list_button",
        "copy_on_demand_bridge_list_button",
        "bridge_list_wrapper_buttons_private_impl",
        "copy_startup_bridge_list_to_clipboard",
        "copy_on_demand_bridge_list_to_clipboard",
    ]
    for fragment in required_window_fragments:
        _assert(fragment in window_text, "missing window fragment: " + fragment)
    _assert(
        window_text.index("copy_patch_validate_freeze_routine_button")
        < window_text.index("copy_startup_bridge_list_button")
        < window_text.index("collector_layout.addLayout(project_root_row)"),
        "split bridge buttons are not near the AI answer routine controls",
    )


def validate_builder_output() -> None:
    import kanda_reasoner_app.reasoner_tools_shell.runner_help.complete_bridge_list_private_impl as bridge_impl

    temp_parent = Path(tempfile.mkdtemp(prefix="kanda_bridge_list_test_"))
    original_first_prompt_files_dir = bridge_impl.analysis_first_prompt_files_dir
    original_freeze_after_update_dir = bridge_impl.analysis_project_freeze_after_update_dir
    try:
        bridge_impl.analysis_first_prompt_files_dir = _fixture_first_prompt_files_dir
        bridge_impl.analysis_project_freeze_after_update_dir = _fixture_freeze_after_update_dir
        project_root = _write_fixture_project(temp_parent / "kanda_reasoner")
        output = bridge_impl.build_complete_bridge_list(project_root)
        required_output_fragments = [
            "KANDA_COMPLETE_BRIDGE_LIST_BEGIN",
            "KANDA_COMPLETE_BRIDGE_LIST_END",
            "emergency AI memory reminder",
            "A bridge is a direction sign",
            "ACTIVE STARTUP BRIDGES",
            "ON-DEMAND BRIDGES",
            "FROZEN BRIDGE MEMORIES",
            "Code Module Size Bridge",
            "project_tool_boundary_startup_bridge",
            "router_bridge_user_detected_correction",
            "router_bridge_zip_fixture_dynamic",
            "SELECTED PROJECT FEATURE HANDLING CHECKLIST",
            "Never merge a selected Project feature into KANDA Tool source",
            "Beginning-of-Day Code Module Size Bridge Visibility v1",
            "400 lines or fewer",
            "500 lines or fewer",
        ]
        for fragment in required_output_fragments:
            _assert(fragment in output, "missing output fragment: " + fragment)
        startup = output.split("ACTIVE STARTUP BRIDGES", 1)[1].split("ON-DEMAND BRIDGES", 1)[0]
        on_demand = output.split("ON-DEMAND BRIDGES", 1)[1].split("FROZEN BRIDGE MEMORIES", 1)[0]
        _assert(
            "project_tool_boundary_startup_bridge" in startup,
            "always-startup boundary bridge is absent from Startup Bridges",
        )
        _assert(
            "project_tool_boundary_startup_bridge" not in on_demand,
            "always-startup boundary bridge leaked into On-Demand Bridges",
        )
        for forbidden in (
            "router_bridge_governed_implementation",
            "router_bridge_patch_delivery_contract",
            "router_bridge_zip_deprecated",
        ):
            _assert(forbidden not in on_demand, "inactive bridge leaked on-demand: " + forbidden)
        on_demand_lines = on_demand.splitlines()
        _assert(
            sum(line.startswith("- router_bridge_user_detected_correction --") for line in on_demand_lines) == 1,
            "active routed bridge missing or duplicated",
        )
        _assert(
            sum(line.startswith("- router_bridge_zip_fixture_dynamic --") for line in on_demand_lines) == 1,
            "active ZIP bridge missing or duplicated",
        )
    finally:
        bridge_impl.analysis_first_prompt_files_dir = original_first_prompt_files_dir
        bridge_impl.analysis_project_freeze_after_update_dir = original_freeze_after_update_dir
        shutil.rmtree(temp_parent, ignore_errors=True)


def main() -> int:
    _ensure_project_root_on_path()
    validate_static_files()
    validate_builder_output()
    print("VALIDATION OK: complete-bridge-list-button-v1")
    print("VALIDATION OK: complete-bridge-list-button-v1-validation-repair-v2")
    print("VALIDATION OK: complete-bridge-list-button-v1-validation-repair-v3")
    print("VALIDATION OK: complete-bridge-classification-and-selected-project-feature-checklist-v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
