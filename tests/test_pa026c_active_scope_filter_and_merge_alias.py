"""Tests for PA026C active-scope Atlas target filtering."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_symbol_atlas import (  # noqa: E402
    implementation_responsibility_resolver as responsibility_resolver,
)
from kanda_reasoner_app.reasoner_symbol_atlas import main_helper_mapper  # noqa: E402
from kanda_reasoner_app.reasoner_symbol_atlas import related_file_finder  # noqa: E402
from kanda_reasoner_app.reasoner_symbol_atlas.implementation_responsibility_resolver import (  # noqa: E402
    PROJECT_SYMBOL_ATLAS_RESPONSIBILITY_STATUS_NEEDS_OWNER_REVIEW,
    ProjectSymbolAtlasImplementationResponsibilityOptions,
    resolve_reasoner_symbol_atlas_implementation_responsibility,
)
from kanda_reasoner_app.reasoner_symbol_atlas.main_helper_mapper import (  # noqa: E402
    ProjectSymbolAtlasMainHelperOptions,
    map_reasoner_symbol_atlas_main_helpers,
)
from kanda_reasoner_app.reasoner_symbol_atlas.related_file_finder import (  # noqa: E402
    ProjectSymbolAtlasRelatedFileOptions,
    find_reasoner_symbol_atlas_related_files,
)
from kanda_reasoner_app.reasoner_symbol_atlas.schemas import (  # noqa: E402
    ProjectModuleRecord,
    ProjectSymbolAtlasReport,
)

from kanda_reasoner_app.reasoner_symbol_atlas.evidence_merger import (  # noqa: E402
    ProjectSymbolAtlasEvidenceMergeOptions,
    build_reasoner_symbol_atlas_live_json_merge_report,
    build_reasoner_symbol_atlas_merged_evidence_report,
)


def _temporary_project_root() -> str:
    path = Path(tempfile.mkdtemp(prefix="pa026b_project_"))
    (path / 'ask_' 'ai_project_reasoner').mkdir()
    (path / "tests").mkdir()
    return str(path)


def test_pa026c_main_helper_does_not_select_project_reference_as_main() -> None:
    """A legacy/reference module must not replace the active target as main."""

    project_root = _temporary_project_root()
    target = ProjectModuleRecord(
        module="reasoner_tools_gui_engineering_safety_panel",
        path="reasoner_tools_gui_engineering_safety_panel.py",
        owner_role="facade",
    )
    inactive_reference = ProjectModuleRecord(
        module="_project_reference.CANNON.brain_dashboard",
        path="_project_reference/CANNON/brain_dashboard_pyside_25fps_anatomy_v5_hover_tooltip_fixed_visible.py",
        owner_role="canonical_owner",
        imports=("reasoner_tools_gui_engineering_safety_panel",),
    )
    active_helper = ProjectModuleRecord(
        module="reasoner_tools_gui_engineering_safety_panel_commands",
        path="reasoner_tools_gui_engineering_safety_panel_commands.py",
        owner_role="private_helper",
    )
    report = ProjectSymbolAtlasReport(
        project_root=project_root,
        modules=(target, inactive_reference, active_helper),
    )
    summary = SimpleNamespace(status="json_canonical")

    original_merge = main_helper_mapper.merge_reasoner_symbol_atlas_live_and_json_evidence
    main_helper_mapper.merge_reasoner_symbol_atlas_live_and_json_evidence = (  # type: ignore[assignment]
        lambda _options: (report, summary)
    )
    try:
        decision = map_reasoner_symbol_atlas_main_helpers(
            ProjectSymbolAtlasMainHelperOptions(
                project_root=project_root,
                target_path="reasoner_tools_gui_engineering_safety_panel.py",
            )
        )
    finally:
        main_helper_mapper.merge_reasoner_symbol_atlas_live_and_json_evidence = original_merge  # type: ignore[assignment]

    assert decision.main_path == "reasoner_tools_gui_engineering_safety_panel.py"
    assert "reasoner_tools_gui_engineering_safety_panel_commands.py" in decision.helper_paths
    joined = "\n".join((decision.main_path,) + decision.helper_paths)
    assert "_project_reference" not in joined


def test_pa026c_responsibility_falls_back_to_active_target_when_main_is_inactive() -> None:
    """Implementation responsibility must not emit inactive primary targets."""

    project_root = _temporary_project_root()
    target_path = "reasoner_tools_gui_engineering_safety_panel.py"

    fake_placement = SimpleNamespace(
        status="ready",
        recommended_owner_box="gui_shell",
        primary_target_path=target_path,
        forbidden_boxes=("project_analysis_evidence", "source_hygiene"),
        tests_to_run=(
            "python tests\\test_gui003_engineering_safety_panel_actions.py",
            "python _project_reference\\old_test.py",
        ),
        reasons=("placement ready",),
    )
    fake_facade = SimpleNamespace(
        status="needs_owner_review",
        target_is_facade=True,
        target_path=target_path,
        likely_real_owner_path="",
        reasons=("facade needs review",),
        facade_evidence=("target appears facade-like",),
    )
    fake_main_helper = SimpleNamespace(
        status="ready",
        main_path="_project_reference/CANNON/brain_dashboard_pyside_25fps_anatomy_v5_hover_tooltip_fixed_visible.py",
        helper_paths=(
            "_project_reference/CANNON/helper.py",
            "reasoner_tools_gui_engineering_safety_panel_commands.py",
        ),
        tests_to_run=(
            "python tests\\test_gui004_engineering_safety_panel_command_map.py",
            "python tests_archive\\test_old_gui.py",
        ),
        public_helper_warnings=tuple(),
        evidence=("main helper evidence",),
    )

    original_placement = responsibility_resolver.advise_reasoner_symbol_atlas_logic_placement
    original_facade = responsibility_resolver.resolve_reasoner_symbol_atlas_facade_owner
    original_main_helper = responsibility_resolver.map_reasoner_symbol_atlas_main_helpers
    responsibility_resolver.advise_reasoner_symbol_atlas_logic_placement = lambda _options: fake_placement  # type: ignore[assignment]
    responsibility_resolver.resolve_reasoner_symbol_atlas_facade_owner = lambda _options: fake_facade  # type: ignore[assignment]
    responsibility_resolver.map_reasoner_symbol_atlas_main_helpers = lambda _options: fake_main_helper  # type: ignore[assignment]
    try:
        decision = resolve_reasoner_symbol_atlas_implementation_responsibility(
            ProjectSymbolAtlasImplementationResponsibilityOptions(
                project_root=project_root,
                task_description="Review GUI button wiring before patching.",
                target_path=target_path,
                symbol_name="create_engineering_safety_panel",
            )
        )
    finally:
        responsibility_resolver.advise_reasoner_symbol_atlas_logic_placement = original_placement  # type: ignore[assignment]
        responsibility_resolver.resolve_reasoner_symbol_atlas_facade_owner = original_facade  # type: ignore[assignment]
        responsibility_resolver.map_reasoner_symbol_atlas_main_helpers = original_main_helper  # type: ignore[assignment]

    assert decision.status == PROJECT_SYMBOL_ATLAS_RESPONSIBILITY_STATUS_NEEDS_OWNER_REVIEW
    assert decision.primary_edit_target == target_path
    assert "reasoner_tools_gui_engineering_safety_panel_commands.py" in decision.secondary_helper_targets
    rendered = "\n".join(
        (decision.primary_edit_target,)
        + decision.secondary_helper_targets
        + decision.files_not_to_touch
        + decision.tests_to_run
        + decision.reasons
    )
    assert "_project_reference" not in rendered
    assert "tests_archive" not in rendered


def test_pa026c_related_files_use_public_contract_for_generic_token_filtering() -> None:
    """Generic path tokens must not make unrelated helpers look related."""

    project_root = _temporary_project_root()
    target_path = "reasoner_tools_gui_engineering_safety_panel.py"
    target = ProjectModuleRecord(
        module="reasoner_tools_gui_engineering_safety_panel",
        path=target_path,
        owner_role="facade",
    )
    active_helper = ProjectModuleRecord(
        module="reasoner_tools_gui_engineering_safety_panel_commands",
        path="reasoner_tools_gui_engineering_safety_panel_commands.py",
        owner_role="private_helper",
    )
    unrelated_gui_helper = ProjectModuleRecord(
        module="kanda_reasoner_app.insert_missing_docstrings_gui.gui_scope_helpers",
        path='ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/gui_scope_helpers.py',
        owner_role="private_helper",
    )
    unrelated_runtime_helper = ProjectModuleRecord(
        module="kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_utils",
        path='ask_' 'ai_project_reasoner' '/reasoner_runtime_collector/runtime_trace_utils.py',
        owner_role="private_helper",
    )
    report = ProjectSymbolAtlasReport(
        project_root=project_root,
        modules=(target, active_helper, unrelated_gui_helper, unrelated_runtime_helper),
    )
    summary = SimpleNamespace(status="json_canonical")
    fake_main_helper = SimpleNamespace(
        status="ready",
        main_path=target_path,
        helper_paths=("reasoner_tools_gui_engineering_safety_panel_commands.py",),
        tests_to_run=tuple(),
    )
    fake_facade = SimpleNamespace(
        status="owner_not_found",
        target_is_facade=False,
        target_path=target_path,
        likely_real_owner_path="",
    )

    original_merge = related_file_finder.merge_reasoner_symbol_atlas_live_and_json_evidence
    original_main_helper = related_file_finder.map_reasoner_symbol_atlas_main_helpers
    original_facade = related_file_finder.resolve_reasoner_symbol_atlas_facade_owner
    related_file_finder.merge_reasoner_symbol_atlas_live_and_json_evidence = (  # type: ignore[assignment]
        lambda _options: (report, summary)
    )
    related_file_finder.map_reasoner_symbol_atlas_main_helpers = lambda _options: fake_main_helper  # type: ignore[assignment]
    related_file_finder.resolve_reasoner_symbol_atlas_facade_owner = lambda _options: fake_facade  # type: ignore[assignment]
    try:
        decision = find_reasoner_symbol_atlas_related_files(
            ProjectSymbolAtlasRelatedFileOptions(
                project_root=project_root,
                target_path=target_path,
                include_tests=False,
                include_workbench=False,
                include_evidence_files=False,
            )
        )
    finally:
        related_file_finder.merge_reasoner_symbol_atlas_live_and_json_evidence = original_merge  # type: ignore[assignment]
        related_file_finder.map_reasoner_symbol_atlas_main_helpers = original_main_helper  # type: ignore[assignment]
        related_file_finder.resolve_reasoner_symbol_atlas_facade_owner = original_facade  # type: ignore[assignment]

    assert "reasoner_tools_gui_engineering_safety_panel_commands.py" in decision.helper_files
    joined = "\n".join(decision.related_files)
    assert "insert_missing_docstrings_gui" not in joined
    assert "runtime_trace_utils" not in joined



def test_pa026c_live_json_merge_alias_preserves_public_contract() -> None:
    """The PA023 public merge-report name must remain importable."""

    assert build_reasoner_symbol_atlas_live_json_merge_report is not None
    assert build_reasoner_symbol_atlas_merged_evidence_report is not None
    assert ProjectSymbolAtlasEvidenceMergeOptions is not None


def main() -> int:
    test_pa026c_main_helper_does_not_select_project_reference_as_main()
    test_pa026c_responsibility_falls_back_to_active_target_when_main_is_inactive()
    test_pa026c_related_files_use_public_contract_for_generic_token_filtering()
    test_pa026c_live_json_merge_alias_preserves_public_contract()
    print("PA026C active-scope pre-patch target filter tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
