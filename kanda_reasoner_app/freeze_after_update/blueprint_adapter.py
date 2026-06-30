# project-path: kanda_reasoner_app/freeze_after_update/blueprint_adapter.py
"""Adapter from the GUI-facing box to the blueprint freeze generator.

The app box owns GUI/controller integration. The generator logic that creates
project_freeze_after_update templates live in KANDA's blueprint freeze box:

    project_freeze_ledger/freeze_tools/freeze_after_update_generator.py
"""

from __future__ import annotations


__all__ = [
    'ensure_box',
    'generate_ai_send_files',
    'generator_path',
    'inspect_box',
    'kanda_project_root',
    'load_generator',
]
import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

from kanda_reasoner_app.project_analysis_evidence_paths import project_analysis_evidence_root


_GENERATOR_MODULE_NAME = "kanda_freeze_after_update_blueprint_generator"


def kanda_project_root() -> Path:
    """Return the KANDA Reasoner project root that owns the blueprint box."""
    return Path(__file__).resolve().parents[2]


def generator_path() -> Path:
    """Return the blueprint generator path."""
    return kanda_project_root() / "project_freeze_ledger" / "freeze_tools" / "freeze_after_update_generator.py"


def load_generator() -> ModuleType:
    """Load the blueprint generator without importing it as an app package."""
    path = generator_path()
    if not path.exists():
        raise FileNotFoundError(f"Missing blueprint generator: {path}")
    spec = importlib.util.spec_from_file_location(_GENERATOR_MODULE_NAME, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load blueprint generator: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[_GENERATOR_MODULE_NAME] = module
    spec.loader.exec_module(module)
    return module




def freeze_state_owner_root(project_root: str | Path) -> Path:
    """Return the external owner root passed to legacy blueprint generators."""
    return project_analysis_evidence_root(project_root)


def _selected_project_root(project_root: str | Path) -> Path:
    """Return the real selected source project root."""
    return Path(project_root).expanduser().resolve(strict=False)


def _base_payload(status: str, project_root: str | Path, owner_root: Path, message: str) -> dict[str, Any]:
    """Build a generator-shaped payload without calling the blueprint module."""
    return {
        "status": status,
        "project_root": str(_selected_project_root(project_root)),
        "freeze_state_owner_root": str(owner_root),
        "box_root": str(owner_root / "project_freeze_after_update"),
        "message": message,
        "missing_paths": [],
        "created_paths": [],
        "output_zip": "",
        "output_instruction": "",
        "freeze_count": 0,
    }


def _rewrite_payload_project(payload: dict[str, Any], project_root: str | Path, owner_root: Path) -> dict[str, Any]:
    """Expose active project identity while keeping external state paths."""
    result = dict(payload)
    result["project_root"] = str(_selected_project_root(project_root))
    result["freeze_state_owner_root"] = str(owner_root)
    if "box_root" in result:
        result["box_root"] = str(owner_root / "project_freeze_after_update")
    return result

def inspect_box(project_root: str | Path) -> dict[str, Any]:
    """Inspect the selected project external support box through the blueprint generator."""
    selected_root = _selected_project_root(project_root)
    owner_root = freeze_state_owner_root(project_root)
    if not selected_root.exists() or not selected_root.is_dir():
        return _base_payload(
            "invalid_project_root",
            selected_root,
            owner_root,
            "Project root does not exist or is not a directory.",
        )
    if not owner_root.exists():
        payload = _base_payload(
            "incomplete",
            selected_root,
            owner_root,
            "Freeze Feature After Update box is missing required paths.",
        )
        payload["missing_paths"] = [
            "project_freeze_after_update",
            "project_freeze_after_update/frozen_features_memory",
            "project_freeze_after_update/frozen_features_memory/entries",
            "project_freeze_after_update/files_to_send_ai",
        ]
        return payload
    module = load_generator()
    payload = module.inspect_freeze_after_update_box(owner_root)
    return _rewrite_payload_project(payload, project_root, owner_root)


def ensure_box(project_root: str | Path) -> dict[str, Any]:
    """Create or validate the selected project external support box through the blueprint generator."""
    selected_root = _selected_project_root(project_root)
    owner_root = freeze_state_owner_root(project_root)
    if not selected_root.exists() or not selected_root.is_dir():
        return _base_payload(
            "invalid_project_root",
            selected_root,
            owner_root,
            "Project root does not exist or is not a directory.",
        )
    owner_root.mkdir(parents=True, exist_ok=True)
    module = load_generator()
    payload = module.ensure_freeze_after_update_box(owner_root)
    return _rewrite_payload_project(payload, project_root, owner_root)


def generate_ai_send_files(project_root: str | Path) -> dict[str, Any]:
    """Generate AI-send files through the blueprint generator."""
    selected_root = _selected_project_root(project_root)
    owner_root = freeze_state_owner_root(project_root)
    if not selected_root.exists() or not selected_root.is_dir():
        return _base_payload(
            "invalid_project_root",
            selected_root,
            owner_root,
            "Project root does not exist or is not a directory.",
        )
    owner_root.mkdir(parents=True, exist_ok=True)
    module = load_generator()
    payload = module.generate_freeze_after_update_ai_files(owner_root)
    return _rewrite_payload_project(payload, project_root, owner_root)
