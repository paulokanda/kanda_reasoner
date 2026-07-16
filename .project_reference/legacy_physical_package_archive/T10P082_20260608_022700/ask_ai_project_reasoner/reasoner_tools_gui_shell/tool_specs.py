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
    module_candidates: tuple[str, ...]
    class_candidates: tuple[str, ...]
    source_hint: str
    help_catalog: str | None = None


TOOLS: tuple[ToolSpec, ...] = (
    ToolSpec(
        step_title="First step: check/correct architecture",
        module_candidates=(
            _module_path("manage_architecture", "manage_architecture_gui"),
        ),
        class_candidates=("ArchitectureManagerWindow",),
        source_hint=_source_path("manage_architecture", "manage_architecture_gui.py"),
        help_catalog="tab1_architecture.json",
    ),
    ToolSpec(
        step_title="Second step: check/correct workflow",
        module_candidates=(
            _module_path("manage_workflows", "manage_workflows_gui"),
        ),
        class_candidates=("WorkflowManagerWindow",),
        source_hint=_source_path("manage_workflows", "manage_workflows_gui.py"),
        help_catalog="tab2_workflow.json",
    ),
    ToolSpec(
        step_title="Third step: insert missing docstrings",
        module_candidates=(
            _module_path("insert_missing_docstrings_gui", "insert_missing_docstrings_gui"),
        ),
        class_candidates=("MissingDocstringsWindow",),
        source_hint=_source_path("insert_missing_docstrings_gui", "insert_missing_docstrings_gui.py"),
    ),
    ToolSpec(
        step_title="Fourth step: collect project structure",
        module_candidates=(
            _module_path("reasoner_context_collector", "runner"),
        ),
        class_candidates=("CollectorRunnerWindow",),
        source_hint=_source_path("reasoner_context_collector", "runner.py"),
    ),
    ToolSpec(
        step_title="Fifth step: Split structure to AI import",
        module_candidates=(
            _module_path("json_splitter", "json_splitter_8"),
        ),
        class_candidates=("JsonSplitterPanel", "JsonSplitterWindow"),
        source_hint=_source_path("json_splitter", "json_splitter_8.py"),
    ),
    ToolSpec(
        step_title="Sixth step: daily refactor report",
        module_candidates=(
            _module_path("daily_rfctr_report", "daily_refactor_report"),
        ),
        class_candidates=("StateVectorCompiler",),
        source_hint=_source_path("daily_rfctr_report", "daily_refactor_report.py"),
    ),
    ToolSpec(
        step_title="Seventh step: Ask AI about project",
        module_candidates=(
            _module_path("project_reasoner_v10", "ai_reasoner_main_window"),
            "ai_reasoner_main_window",
        ),
        class_candidates=("JsonProjectReasonerV10",),
        source_hint=_source_path("project_reasoner_v10", "ai_reasoner_main_window.py"),
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
        "help_catalog": None,
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

    globals()["TOOLS"] = (*cleaned_tools, engineering_safety_spec)


_gui002r_register_engineering_safety_tab()
# END GUI002R_ENGINEERING_SAFETY_TAB_OWNER_REGISTRATION
