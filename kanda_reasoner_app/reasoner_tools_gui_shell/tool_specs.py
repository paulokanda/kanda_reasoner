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
    step_title: str
    module_candidates: tuple[str, ...] = ()
    class_candidates: tuple[str, ...] = ()
    source_hint: str = ""
    help_catalog: str | None = None
    tab_id: str | None = None
    tab_kind: str = "lazy_tool"


TOOLS: tuple[ToolSpec, ...] = (
    ToolSpec(
        step_title="Brain Navigator",
        source_hint=_source_path("reasoner_tools_gui_shell", "brain_navigator", "contract.py"),
        tab_id="brain_navigator",
        tab_kind="builtin_brain_navigator",
    ),
    ToolSpec(
        step_title="Architecture Review",
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
    ),
    ToolSpec(
        step_title="Docstring Assistant",
        module_candidates=(
            _module_path("insert_missing_docstrings_gui", "insert_missing_docstrings_gui"),
        ),
        class_candidates=("MissingDocstringsWindow",),
        source_hint=_source_path("insert_missing_docstrings_gui", "insert_missing_docstrings_gui.py"),
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
    ),
    ToolSpec(
        step_title="Project Q&A",
        module_candidates=(
            _module_path("project_reasoner_v10", "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window"),
            "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window",
        ),
        class_candidates=("JsonProjectReasonerV10",),
        source_hint=_source_path("project_reasoner_v10", "ai_reasoner_main_window.py"),
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
        tab_id="exclusion_rules",
        tab_kind="builtin_ignore_rules",
    ),
    ToolSpec(
        step_title="Prompt Library",
        source_hint=_source_path("prompt_library_gui", "prompt_library_tab.py"),
        tab_id="prompt_library",
        tab_kind="builtin_prompt_library",
    ),
)

# BEGIN GUI002R_ENGINEERING_SAFETY_TAB_OWNER_REGISTRATION
def _gui002r_register_engineering_safety_tab() -> None:
    """Register Engineering Safety in the tool specs owner module."""
    import dataclasses as _gui002r_dataclasses
    import sys as _gui002r_sys

    module = _gui002r_sys.modules.get(__name__)
    if module is None:
        return

    tool_spec_class = getattr(module, "ToolSpec", None)
    if tool_spec_class is None:
        return

    try:
        current_tools = tuple(getattr(module, "TOOLS"))
    except Exception:
        return

    canonical_title = "Engineering Safety"
    cleaned_tools = tuple(
        spec for spec in current_tools
        if getattr(spec, "step_title", "") != canonical_title
    )

    payload = {
        "step_title": canonical_title,
        "module_candidates": ("reasoner_tools_gui_engineering_safety_panel",),
        "class_candidates": ("create_engineering_safety_panel",),
        "source_hint": "reasoner_tools_gui_engineering_safety_panel.py",
        "help_catalog": "engineering_safety.json",
        "tab_id": "engineering_safety",
        "tab_kind": "lazy_tool",
    }

    try:
        if _gui002r_dataclasses.is_dataclass(tool_spec_class):
            field_names = {
                field.name for field in _gui002r_dataclasses.fields(tool_spec_class)
            }
            kwargs = {
                key: value for key, value in payload.items()
                if key in field_names
            }
            engineering_safety_spec = tool_spec_class(**kwargs)
        else:
            try:
                engineering_safety_spec = tool_spec_class(**payload)
            except TypeError:
                fallback_payload = dict(payload)
                fallback_payload.pop("help_catalog", None)
                engineering_safety_spec = tool_spec_class(**fallback_payload)
    except Exception:
        return

    insert_after_title = "Workflow Review"
    insert_at = len(cleaned_tools)
    for index, spec in enumerate(cleaned_tools):
        if getattr(spec, "step_title", "") == insert_after_title:
            insert_at = index + 1
            break

    globals()["TOOLS"] = (
        *cleaned_tools[:insert_at],
        engineering_safety_spec,
        *cleaned_tools[insert_at:],
    )


_gui002r_register_engineering_safety_tab()
# END GUI002R_ENGINEERING_SAFETY_TAB_OWNER_REGISTRATION
