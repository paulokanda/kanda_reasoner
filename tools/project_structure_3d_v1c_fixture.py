# project-path: tools/project_structure_3d_v1c_fixture.py
"""Deterministic complete-JSON and Freeze fixtures for v1C validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from kanda_reasoner_app.freeze_after_update.paths import build_paths
from kanda_reasoner_app.project_analysis_evidence_paths import (
    analysis_json_complete_dir,
)

__all__ = ["write_semantic_complete_json", "write_semantic_freeze_entry"]


def _function(
    name: str,
    line: int,
    *,
    qualname: str | None = None,
    parent: str = "",
    calls: list[str] | None = None,
) -> dict[str, Any]:
    """Return one compact complete-JSON function record."""
    return {
        "name": name,
        "qualname": qualname or name,
        "lineno": line,
        "line_end": line + 5,
        "symbol_kind": "function",
        "parent_symbol": parent,
        "is_async": False,
        "decorator_names": [],
        "docstring": name + " behavior.",
        "docstring_summary": {"summary": name + " behavior."},
        "calls": [{"call_name": item} for item in (calls or [])],
    }


def _class(
    name: str,
    line: int,
    *,
    bases: list[str] | None = None,
    methods: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Return one compact complete-JSON class record."""
    return {
        "name": name,
        "qualname": name,
        "lineno": line,
        "line_end": line + 30,
        "symbol_kind": "class",
        "bases": list(bases or []),
        "methods": list(methods or []),
        "docstring": name + " class.",
        "docstring_summary": {"summary": name + " class."},
    }


def write_semantic_complete_json(project_root: Path) -> Path:
    """Write one deterministic semantic complete-JSON fixture."""
    evidence = analysis_json_complete_dir(project_root)
    evidence.mkdir(parents=True, exist_ok=True)
    path = evidence / (project_root.name + "__complete.json")
    child_run = _function(
        "run",
        12,
        qualname="Child.run",
        parent="Child",
        calls=["helper"],
    )
    payload = {
        "source_file_index": {
            "app/base.py": {
                "file": "app/base.py",
                "module_name": "app.base",
                "line_count": 40,
                "symbol_count": 1,
            },
            "app/child.py": {
                "file": "app/child.py",
                "module_name": "app.child",
                "line_count": 80,
                "symbol_count": 2,
            },
            "app/helpers.py": {
                "file": "app/helpers.py",
                "module_name": "app.helpers",
                "line_count": 30,
                "symbol_count": 1,
            },
            "tests/test_child.py": {
                "file": "tests/test_child.py",
                "module_name": "tests.test_child",
                "line_count": 35,
                "symbol_count": 1,
            },
        },
        "symbol_index": {
            "Base": {"file": "app/base.py", "kind": "class"},
            "Child": {"file": "app/child.py", "kind": "class"},
            "helper": {"file": "app/helpers.py", "kind": "function"},
        },
        "primary_definition_index": {
            "Base": "app/base.py",
            "Child": "app/child.py",
            "helper": "app/helpers.py",
        },
        "import_graph": {
            "app.base": [],
            "app.child": ["app.base", "app.helpers"],
            "app.helpers": [],
            "tests.test_child": ["app.child"],
        },
        "files": [
            {
                "path": "app/base.py",
                "module_name": "app.base",
                "classes": [_class("Base", 3)],
                "functions": [],
            },
            {
                "path": "app/child.py",
                "module_name": "app.child",
                "classes": [
                    _class("Child", 5, bases=["Base"], methods=[child_run])
                ],
                "functions": [],
            },
            {
                "path": "app/helpers.py",
                "module_name": "app.helpers",
                "classes": [],
                "functions": [_function("helper", 4)],
            },
            {
                "path": "tests/test_child.py",
                "module_name": "tests.test_child",
                "classes": [],
                "functions": [_function("test_child_run", 5, calls=["Child.run"])],
            },
        ],
        "call_edges": [
            {
                "from_file": "app/child.py",
                "from_symbol": "Child.run",
                "to_call": "helper",
                "line": 15,
            },
            {
                "from_file": "tests/test_child.py",
                "from_symbol": "test_child_run",
                "to_call": "Child.run",
                "line": 8,
            },
        ],
        "web_ai_test_protection_index": {
            "app/child.py": {
                "source_file": "app/child.py",
                "linked_tests": [
                    {
                        "test_file": "tests/test_child.py",
                        "confidence": "high",
                    }
                ],
            }
        },
        "web_ai_file_responsibility_index": {
            "app/child.py": {"primary_responsibility": "Child behavior."},
        },
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def write_semantic_freeze_entry(project_root: Path) -> Path:
    """Write one Freeze fixture through the canonical public path owner."""
    entries = build_paths(project_root).entries_root
    entries.mkdir(parents=True, exist_ok=True)
    path = entries / "freeze-20260723-semantic-fixture.md"
    path.write_text(
        "---\n"
        'freeze_id: "freeze-20260723-semantic-fixture"\n'
        'box: "app/child.py"\n'
        'status: "frozen"\n'
        'date: "2026-07-23"\n'
        "protected_paths:\n"
        '  - "app/child.py"\n'
        "do_not_touch_summary:\n"
        '  - "Preserve Child behavior."\n'
        "superseded_by: null\n"
        "---\n\n"
        "# Semantic fixture\n",
        encoding="utf-8",
    )
    return path
