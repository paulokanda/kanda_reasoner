# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/tool_specs.py
"""Tool registry definitions for the Reasoner tools GUI shell."""

from __future__ import annotations

from dataclasses import dataclass

__all__ = [
    "TOOLS",
    "ToolSpec",
]

_CANONICAL_PACKAGE_NAME = "kanda_reasoner_app"


def _module_path(*parts: str) -> str:
    """Return a canonical dotted module path."""
    return ".".join((_CANONICAL_PACKAGE_NAME, *parts))


def _source_path(*parts: str) -> str:
    """Return a canonical slash-separated source hint."""
    return "/".join((_CANONICAL_PACKAGE_NAME, *parts))


@dataclass(frozen=True)
class ToolSpec:
    """Represent tool spec."""
    
    step_title: str
    module_candidates: tuple[str, ...] = ()
    class_candidates: tuple[str, ...] = ()
    source_hint: str = ""
    help_catalog: str | None = None
    tab_id: str | None = None
    tab_kind: str = "lazy_tool"
    visible_in_shell: bool = True


TOOLS: tuple[ToolSpec, ...] = (
    ToolSpec(
        step_title="Brain Navigator",
        source_hint=_source_path("reasoner_tools_gui_shell", "brain_navigator", "contract.py"),
        tab_id="brain_navigator",
        tab_kind="builtin_brain_navigator",
    ),
    ToolSpec(
        step_title="Audit Project",
        module_candidates=(
            _module_path("manage_architecture", "manage_architecture_gui"),
        ),
        class_candidates=("ArchitectureManagerWindow",),
        source_hint=_source_path("manage_architecture", "manage_architecture_gui.py"),
        help_catalog="tab1_architecture.json",
        tab_id="architecture_review",
    ),
    ToolSpec(
        step_title="Workflow Review",
        module_candidates=(
            _module_path("manage_workflows", "manage_workflows_gui"),
        ),
        class_candidates=("WorkflowManagerWindow",),
        source_hint=_source_path("manage_workflows", "manage_workflows_gui.py"),
        help_catalog="tab2_workflow.json",
        tab_id="workflow_review",
        visible_in_shell=False,
    ),
    ToolSpec(
        step_title="Docstring Assistant",
        module_candidates=(
            _module_path("insert_missing_docstrings_gui", "insert_missing_docstrings_gui"),
        ),
        class_candidates=("MissingDocstringsWindow",),
        source_hint=_source_path(
            "insert_missing_docstrings_gui",
            "insert_missing_docstrings_gui.py",
        ),
        help_catalog="docstring_assistant.json",
        tab_id="docstring_assistant",
    ),
    ToolSpec(
        step_title="Show Project to AI",
        module_candidates=(
            _module_path("reasoner_context_collector", "runner"),
        ),
        class_candidates=("CollectorRunnerWindow",),
        source_hint=_source_path("reasoner_context_collector", "runner.py"),
        help_catalog="project_structure_map.json",
        tab_id="project_structure_map",
    ),
    ToolSpec(
        step_title="Project Structure 3D",
        module_candidates=(
            _module_path(
                "project_structure_visualizer",
                "project_structure_3d_tab",
            ),
        ),
        class_candidates=("ProjectStructure3DWidget",),
        source_hint=_source_path(
            "project_structure_visualizer",
            "project_structure_3d_tab.py",
        ),
        help_catalog="project_structure_3d.json",
        tab_id="project_structure_3d",
    ),
    ToolSpec(
        step_title="Config AI",
        module_candidates=(
            _module_path("reasoner_engine", "config_ai_tab"),
        ),
        class_candidates=("ConfigAITab",),
        source_hint=_source_path("reasoner_engine", "config_ai_tab.py"),
        help_catalog="config_ai.json",
        tab_id="config_web_ai",
    ),
    ToolSpec(
        step_title="Web AI",
        module_candidates=(
            _module_path("reasoner_engine", "project_web_ai_tab"),
        ),
        class_candidates=("ProjectWebAITab",),
        source_hint=_source_path("reasoner_engine", "project_web_ai_tab.py"),
        help_catalog="web_ai.json",
        tab_id="project_web_ai",
    ),
    ToolSpec(
        step_title="Error Memory",
        module_candidates=(
            _module_path("error_memory_gui", "error_memory_tab"),
        ),
        class_candidates=("ErrorMemoryTab",),
        source_hint=_source_path("error_memory_gui", "error_memory_tab.py"),
        tab_id="error_memory",
    ),
    ToolSpec(
        step_title="Refactor Report",
        module_candidates=(
            _module_path("daily_rfctr_report", "daily_refactor_report"),
        ),
        class_candidates=("StateVectorCompiler",),
        source_hint=_source_path("daily_rfctr_report", "daily_refactor_report.py"),
        help_catalog="refactor_report.json",
        tab_id="refactor_report",
        visible_in_shell=False,
    ),
    ToolSpec(
        step_title="Local AI",
        module_candidates=(
            _module_path("reasoner_engine", "ai_reasoner_main_window"),
        ),
        class_candidates=("JsonProjectReasonerV10",),
        source_hint=_source_path("reasoner_engine", "ai_reasoner_main_window.py"),
        help_catalog="ai_reasoner_main_window_help.json",
        tab_id="project_qa",
    ),
    ToolSpec(
        step_title="Freeze Feature After Update",
        module_candidates=(
            _module_path("freeze_after_update_gui", "freeze_after_update_tab"),
        ),
        class_candidates=("FreezeAfterUpdateTab",),
        source_hint=_source_path("freeze_after_update_gui", "freeze_after_update_tab.py"),
        tab_id="freeze_feature_after_update",
    ),
    ToolSpec(
        step_title="Exclusion Rules",
        source_hint=_source_path("reasoner_tools_gui_shell", "ignore_rules_tab.py"),
        help_catalog="exclusion_rules.json",
        tab_id="exclusion_rules",
        tab_kind="builtin_ignore_rules",
    ),
    ToolSpec(
        step_title="Prompt Library",
        source_hint=_source_path("prompt_library_gui", "prompt_library_tab.py"),
        help_catalog="prompt_library.json",
        tab_id="prompt_library",
        tab_kind="builtin_prompt_library",
    ),
    ToolSpec(
        step_title="Kanda Memo Prompts",
        source_hint=_source_path("reasoner_tools_gui_shell", "kanda_memo_prompts", "contract.py"),
        tab_id="kanda_memo_prompts",
        tab_kind="builtin_kanda_memo_prompts",
    ),
)
