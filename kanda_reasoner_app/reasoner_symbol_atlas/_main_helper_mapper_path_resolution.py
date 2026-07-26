# project-path: kanda_reasoner_app/reasoner_symbol_atlas/_main_helper_mapper_path_resolution.py
"""Private path-resolution logic for Project Symbol Atlas main/helper mapping."""

from __future__ import annotations

from pathlib import Path

from .schemas import ProjectModuleRecord


def _coerce_project_root(project_root: str | Path) -> Path:
    """Support coerce project root behavior.

    Parameters
    ----------
    project_root : str | Path
        The project root path.

    Returns
    -------
    Path
        The resolved path.
    """

    root = Path(project_root).expanduser().resolve(strict=False)
    if not root.exists():
        raise FileNotFoundError("Project root does not exist: " + str(project_root))
    if not root.is_dir():
        raise NotADirectoryError(
            "Project root is not a directory: " + str(project_root)
        )
    return root


def _find_target_record(
    project_root: Path,
    modules: tuple[ProjectModuleRecord, ...],
    target_path: str,
    symbol_name: str,
) -> ProjectModuleRecord | None:
    """Support find target record behavior.

    Parameters
    ----------
    project_root : Path
        The project root path.
    modules : tuple[ProjectModuleRecord, ...]
        The modules value.
    target_path : str
        The target path value.
    symbol_name : str
        The symbol name value.

    Returns
    -------
    ProjectModuleRecord | None
        The project module record result.
    """

    if target_path:
        normalized_target = _normalize_path_for_compare(project_root, target_path)
        for record in modules:
            if _normalize_record_path(record.path) == normalized_target:
                return record
    if symbol_name:
        matches = [
            record
            for record in modules
            for symbol in record.symbols
            if symbol.name == symbol_name and symbol.is_public
        ]
        if matches:
            return sorted(
                matches,
                key=lambda item: (item.owner_role != "canonical_owner", item.path),
            )[0]
    return None


def _normalize_path_for_compare(project_root: Path, path_text: str) -> str:
    """Support normalize path for compare behavior.

    Parameters
    ----------
    project_root : Path
        The project root path.
    path_text : str
        The path text value.

    Returns
    -------
    str
        The string result.
    """

    path = Path(path_text)
    if path.is_absolute():
        try:
            path = path.relative_to(project_root)
        except ValueError:
            pass
    return _normalize_record_path(str(path))


def _normalize_record_path(path_text: str) -> str:
    """Support normalize record path behavior.

    Parameters
    ----------
    path_text : str
        The path text value.

    Returns
    -------
    str
        The string result.
    """

    return str(Path(path_text)).replace("\\", "/")
