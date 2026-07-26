"""Regression tests for retired project-name cleanup in active code paths."""
from __future__ import annotations

from pathlib import Path

RETIRED_NAME = "developer" + "_tools"

ACTIVE_PATHS = [
    Path("kanda_reasoner_app/project_root_resolver.py"),
    Path("kanda_reasoner_app/project_analysis_evidence_paths.py"),
    Path("kanda_reasoner_app/reasoner_tools_shell/runner_help/window_process_private_impl.py"),
    Path("tests/test_show_project_to_ai_selected_project_override_v1.py"),
    Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/reasoner_startup_canon.md"),
    Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/current_workflow_handoff_template.md"),
    Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/evidence_freshness_gate.md"),
    Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/11_productization_and_release_readiness/professional_infrastructure_roadmap.md"),
]


def test_retired_project_name_removed_from_active_paths() -> None:
    offenders: list[str] = []
    for path in ACTIVE_PATHS:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if RETIRED_NAME in text:
            offenders.append(path.as_posix())
    assert not offenders, "retired project-name reference remains in active files: " + ", ".join(offenders)


def test_project_root_resolver_exports_no_retired_name_helper() -> None:
    import kanda_reasoner_app.project_root_resolver as resolver

    assert not hasattr(resolver, "is_legacy_" + RETIRED_NAME + "_root")


def main() -> int:
    test_retired_project_name_removed_from_active_paths()
    test_project_root_resolver_exports_no_retired_name_helper()
    print("VALIDATION OK: legacy_project_name_reference_cleanup_v1")
    print("VALIDATION OK: legacy project name reference cleanup")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
