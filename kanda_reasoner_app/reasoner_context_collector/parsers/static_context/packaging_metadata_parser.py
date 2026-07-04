# project-path: kanda_reasoner_app/reasoner_context_collector/parsers/static_context/packaging_metadata_parser.py
"""Public facade for packaging metadata parsing."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from ._packaging_metadata_file_helpers import _discover_packaging_files
from ._packaging_metadata_file_parsers import (
    _parse_lockfile_names,
    _parse_pipfile,
    _parse_pyproject,
    _parse_requirements_txt,
    _parse_setup_cfg,
    _parse_setup_py,
)
from ._packaging_metadata_result_helpers import (
    _append_parse_warning,
    _dedupe_keep_order,
    _new_result,
    _normalize_rel_path,
    _truncate_text,
)

DEFAULT_PACKAGING_FILE_PATTERNS: tuple[str, ...] = (
    "pyproject.toml",
    "requirements*.txt",
    "setup.py",
    "setup.cfg",
    "Pipfile",
    "poetry.lock",
    "uv.lock",
)

__all__ = [
    "DEFAULT_PACKAGING_FILE_PATTERNS",
    "parse_packaging_metadata",
]


def parse_packaging_metadata(
    project_root: Path,
    file_patterns: tuple[str, ...] = DEFAULT_PACKAGING_FILE_PATTERNS,
    max_dependencies: int = 200,
) -> dict[str, Any]:
    """Parse the packaging metadata.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    file_patterns : tuple[str, ...], optional
        The optional file patterns value.
    max_dependencies : int, optional
        The optional max dependencies value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    result = _new_result()
    root = Path(project_root).expanduser().resolve()

    packaging_files = _discover_packaging_files(root, file_patterns)

    for path in packaging_files:
        filename = path.name.lower()
        try:
            if filename == "pyproject.toml":
                _parse_pyproject(path, root, result, max_dependencies)
            elif filename.startswith("requirements") and filename.endswith(".txt"):
                _parse_requirements_txt(path, root, result, max_dependencies)
            elif filename == "setup.cfg":
                _parse_setup_cfg(path, root, result, max_dependencies)
            elif filename == "setup.py":
                _parse_setup_py(path, root, result, max_dependencies)
            elif filename == "pipfile":
                _parse_pipfile(path, root, result, max_dependencies)
            elif filename == "poetry.lock":
                _parse_lockfile_names(path, root, result, "poetry", max_dependencies)
            elif filename == "uv.lock":
                _parse_lockfile_names(path, root, result, "uv", max_dependencies)
        except Exception as exc:
            logging.exception("Boundary failure in parse_packaging_metadata")
            result["packaging_evidence"].append(
                {
                    "source_file": _normalize_rel_path(path, root),
                    "field": "parse_error",
                    "value_excerpt": _truncate_text(str(exc)),
                }
            )
            _append_parse_warning(result, _normalize_rel_path(path, root), str(exc))

    result["packaging_files_found"] = _dedupe_keep_order(result["packaging_files_found"])
    result["declared_dependencies"] = _dedupe_keep_order(result["declared_dependencies"])[:max_dependencies]
    normalized_optional: dict[str, list[str]] = {}
    for extra_name, deps in result["declared_optional_dependencies"].items():
        normalized_optional[extra_name] = _dedupe_keep_order(deps)[:max_dependencies]
    result["declared_optional_dependencies"] = normalized_optional
    result["package_manager_signals"] = _dedupe_keep_order(result["package_manager_signals"])
    result["packaging_parse_warnings"] = _dedupe_keep_order(result["packaging_parse_warnings"])

    has_structured_source = any(
        signal in result["package_manager_signals"]
        for signal in ("pyproject", "setup.cfg", "setup.py", "pipenv")
    )
    has_dependencies = bool(result["declared_dependencies"] or result["declared_optional_dependencies"])
    if result["packaging_parse_warnings"]:
        result["packaging_confidence"] = "low"
    elif has_structured_source and has_dependencies:
        result["packaging_confidence"] = "high"
    elif has_dependencies:
        result["packaging_confidence"] = "medium"
    else:
        result["packaging_confidence"] = "unknown"

    return result
