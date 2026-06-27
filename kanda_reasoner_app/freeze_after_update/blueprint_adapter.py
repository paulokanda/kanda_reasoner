"""Adapter from the GUI-facing box to the blueprint freeze generator.

The app box owns GUI/controller integration. The generator logic that creates
project_freeze_after_update templates live in KANDA's blueprint freeze box:

    project_freeze_ledger/freeze_tools/freeze_after_update_generator.py
"""

from __future__ import annotations

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


def _rewrite_payload_project(payload: dict[str, Any], project_root: str | Path, owner_root: Path) -> dict[str, Any]:
    """Expose active project identity while keeping external state paths."""
    result = dict(payload)
    result["project_root"] = str(Path(project_root).expanduser().resolve(strict=False))
    result["freeze_state_owner_root"] = str(owner_root)
    if "box_root" in result:
        result["box_root"] = str(owner_root / "project_freeze_after_update")
    return result

def inspect_box(project_root: str | Path) -> dict[str, Any]:
    """Inspect the project-local box through the blueprint generator."""
    module = load_generator()
    owner_root = freeze_state_owner_root(project_root)
    payload = module.inspect_freeze_after_update_box(owner_root)
    return _rewrite_payload_project(payload, project_root, owner_root)


def ensure_box(project_root: str | Path) -> dict[str, Any]:
    """Create or validate the project-local box through the blueprint generator."""
    module = load_generator()
    owner_root = freeze_state_owner_root(project_root)
    payload = module.ensure_freeze_after_update_box(owner_root)
    return _rewrite_payload_project(payload, project_root, owner_root)


def generate_ai_send_files(project_root: str | Path) -> dict[str, Any]:
    """Generate AI-send files through the blueprint generator."""
    module = load_generator()
    owner_root = freeze_state_owner_root(project_root)
    payload = module.generate_freeze_after_update_ai_files(owner_root)
    return _rewrite_payload_project(payload, project_root, owner_root)
