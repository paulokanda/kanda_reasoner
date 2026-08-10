# project-path: tools/validate_fire_shield_windows_path_literal_v1.py
"""Focused Windows path-literal regression for Fire Shield v1."""

from __future__ import annotations

import tempfile
from dataclasses import replace
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_fire_shield import (
    FireShieldError,
    FireShieldPhase,
    build_fire_shield_context,
    scan_project_python_source,
)
from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry
from kanda_reasoner_app.project_support_boundary import ProjectSelectionMode


def gate(name: str, condition: bool) -> None:
    """Print one stable PASS marker or fail immediately."""
    if not condition:
        raise RuntimeError(name + ": FAIL")
    print(name + ": PASS")


def expect_block(name: str, marker: str, action) -> None:
    """Require one action to fail with the expected Fire Shield marker."""
    try:
        action()
    except FireShieldError as exc:
        gate(name, marker in str(exc))
        return
    raise RuntimeError(name + ": FAIL - operation unexpectedly allowed")


def build_external_context(base: Path):
    """Build one registry-backed external Project context."""
    tool_root = base / "tool" / "kanda_reasoner"
    project_root = base / "project" / "sample_project"
    registry_path = base / "registry" / "projects.json"
    (tool_root / "kanda_reasoner_app").mkdir(parents=True, exist_ok=True)
    (tool_root / "kanda_reasoner_app" / "tool_core.py").write_text(
        "TOOL = True\n",
        encoding="utf-8",
    )
    (project_root / "src").mkdir(parents=True, exist_ok=True)
    registry = ProjectSelectionRegistry(
        tool_source_root=tool_root,
        registry_path=registry_path,
    )
    registry.register_explicit_selection(
        project_root,
        ProjectSelectionMode.EXPLICIT_EXTERNAL_PROJECT,
    )
    return build_fire_shield_context(
        project_root,
        phase=FireShieldPhase.PROJECT_SOURCE_MUTATION,
        operation_id="windows-path-literal-regression",
        tool_source_root=tool_root,
        registry_path=registry_path,
    )


def main() -> int:
    """Prove escaped Windows Tool paths cannot bypass source scanning."""
    with tempfile.TemporaryDirectory(prefix="kanda_fire_shield_windows_literal_") as raw:
        context = build_external_context(Path(raw))
        windows_tool_root = Path(r"E:\kanda_reasoner")
        windows_context = replace(
            context,
            boundary=replace(
                context.boundary,
                tool_source_root=windows_tool_root,
            ),
        )
        escaped_source = (
            "TOOL = " + repr(str(windows_tool_root)) + "\n"
        ).encode("utf-8")
        expect_block(
            "FIRE_SHIELD_WINDOWS_ESCAPED_TOOL_ROOT_LITERAL_DENIED",
            "FIRE_SHIELD_PROJECT_TOOL_PATH_LEAK_BLOCKED",
            lambda: scan_project_python_source(
                windows_context,
                escaped_source,
                "src/windows_tool_path.py",
            ),
        )
        scan_project_python_source(
            windows_context,
            b"TOOL = r'E:\\kanda_reasoner2'\n",
            "src/tool_sibling_path.py",
        )
        gate("FIRE_SHIELD_TOOL_ROOT_SIBLING_REFERENCE_ALLOWED", True)
        expect_block(
            "FIRE_SHIELD_WINDOWS_FORWARD_SLASH_TOOL_ROOT_DENIED",
            "FIRE_SHIELD_PROJECT_TOOL_PATH_LEAK_BLOCKED",
            lambda: scan_project_python_source(
                windows_context,
                b"TOOL = 'E:/kanda_reasoner/tools'\n",
                "src/windows_forward_slash_tool_path.py",
            ),
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
