# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/griffe_public_surface.py
"""Resolve Griffe public surface from explicit exports before name fallback."""
from __future__ import annotations

__all__ = ["child_public_override", "griffe_public_state"]


def griffe_public_state(
    node: dict,
    name: str,
    *,
    explicit_export: bool | None = None,
) -> bool:
    """Return public state, preferring an explicit parent export decision."""
    if explicit_export is not None:
        return bool(explicit_export)
    value = node.get("is_public")
    if isinstance(value, bool):
        return value
    kind = str(node.get("kind") or node.get("type") or "").strip().lower()
    if kind == "alias":
        return False
    return not str(name).startswith("_")


def child_public_override(parent: dict, child_name: str) -> bool | None:
    """Return explicit child export state when parent exports are declared."""
    exports = parent.get("exports")
    if exports is None:
        return None
    if not isinstance(exports, (list, tuple)):
        return None
    names = {str(item).strip() for item in exports if str(item).strip()}
    return str(child_name).strip() in names
