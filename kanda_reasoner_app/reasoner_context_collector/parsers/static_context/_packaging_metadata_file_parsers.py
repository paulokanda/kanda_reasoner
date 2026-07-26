# project-path: kanda_reasoner_app/reasoner_context_collector/parsers/static_context/_packaging_metadata_file_parsers.py
"""Per-file parsers for packaging metadata collection."""

from __future__ import annotations

import configparser
import re
from pathlib import Path
from typing import Any

try:
    import tomllib  # Python 3.11+
except ImportError:  # pragma: no cover
    _tomllib = None
else:
    _tomllib = tomllib

from ._packaging_metadata_file_helpers import (
    _clean_dependency_line,
    _is_suspicious_dependency_line,
    _parse_dependency_lines,
    _read_text_best_effort,
)
from ._packaging_metadata_result_helpers import (
    _add_package_manager_signal,
    _append_parse_warning,
    _merge_dependencies,
    _merge_entrypoints,
    _merge_optional_dependencies,
    _merge_tooling,
    _normalize_rel_path,
    _set_if_empty,
)

__all__: list[str] = []


def _parse_pyproject(path: Path, project_root: Path, result: dict[str, Any], max_dependencies: int) -> None:
    """Support parse pyproject behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    project_root : Path
        The project root path.
    result : dict[str, Any]
        The result value.
    max_dependencies : int
        The max dependencies value.
    """
    
    if _tomllib is None:
        raise RuntimeError("tomllib is not available in this Python version")
    source_file = _normalize_rel_path(path, project_root)
    text, read_warnings = _read_text_best_effort(path)
    for warning in read_warnings:
        _append_parse_warning(result, source_file, warning)
    data = _tomllib.loads(text)

    _add_package_manager_signal(result, "pyproject")
    result["packaging_files_found"].append(source_file)

    project = data.get("project", {}) if isinstance(data, dict) else {}
    build_system = data.get("build-system", {}) if isinstance(data, dict) else {}
    tool = data.get("tool", {}) if isinstance(data, dict) else {}

    if isinstance(project, dict):
        _set_if_empty(result, "project_name", str(project.get("name", "")), source_file)
        _set_if_empty(result, "declared_version", str(project.get("version", "")), source_file)

        dependencies = [str(item) for item in project.get("dependencies", []) if str(item).strip()]
        optional_dependencies = {
            str(extra_name): [str(item) for item in items if str(item).strip()]
            for extra_name, items in project.get("optional-dependencies", {}).items()
            if isinstance(items, list)
        }
        _merge_dependencies(result, dependencies, max_dependencies, source_file)
        _merge_optional_dependencies(result, optional_dependencies, max_dependencies, source_file)

        entries: list[dict[str, str]] = []
        for group_name in ("scripts", "gui-scripts"):
            group = project.get(group_name, {})
            if isinstance(group, dict):
                for name, target in group.items():
                    entries.append(
                        {
                            "group": group_name,
                            "name": str(name),
                            "target": str(target),
                            "source_file": source_file,
                        }
                    )
        _merge_entrypoints(result, entries, source_file)

    if isinstance(build_system, dict):
        _set_if_empty(result, "build_backend", str(build_system.get("build-backend", "")), source_file)

    if isinstance(tool, dict):
        tooling = {str(key): value for key, value in tool.items()}
        _merge_tooling(result, tooling, source_file)


def _parse_requirements_txt(path: Path, project_root: Path, result: dict[str, Any], max_dependencies: int) -> None:
    """Support parse requirements txt behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    project_root : Path
        The project root path.
    result : dict[str, Any]
        The result value.
    max_dependencies : int
        The max dependencies value.
    """
    
    source_file = _normalize_rel_path(path, project_root)
    text, read_warnings = _read_text_best_effort(path)
    for warning in read_warnings:
        _append_parse_warning(result, source_file, warning)
    dependencies = _parse_dependency_lines(text)

    _add_package_manager_signal(result, "requirements")
    result["packaging_files_found"].append(source_file)
    _merge_dependencies(result, dependencies, max_dependencies, source_file)


def _parse_setup_cfg(path: Path, project_root: Path, result: dict[str, Any], max_dependencies: int) -> None:
    """Support parse setup cfg behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    project_root : Path
        The project root path.
    result : dict[str, Any]
        The result value.
    max_dependencies : int
        The max dependencies value.
    """
    
    source_file = _normalize_rel_path(path, project_root)
    text, read_warnings = _read_text_best_effort(path)
    for warning in read_warnings:
        _append_parse_warning(result, source_file, warning)
    parser = configparser.ConfigParser()
    parser.read_string(text)

    _add_package_manager_signal(result, "setup.cfg")
    result["packaging_files_found"].append(source_file)

    if parser.has_section("metadata"):
        _set_if_empty(result, "project_name", parser.get("metadata", "name", fallback=""), source_file)
        _set_if_empty(result, "declared_version", parser.get("metadata", "version", fallback=""), source_file)

    if parser.has_section("options"):
        dependencies = _parse_dependency_lines(parser.get("options", "install_requires", fallback=""))
        _merge_dependencies(result, dependencies, max_dependencies, source_file)

    if parser.has_section("options.extras_require"):
        optional_dependencies: dict[str, list[str]] = {}
        for extra_name, value in parser.items("options.extras_require"):
            optional_dependencies[str(extra_name)] = _parse_dependency_lines(value)
        _merge_optional_dependencies(result, optional_dependencies, max_dependencies, source_file)

    if parser.has_section("options.entry_points"):
        entries: list[dict[str, str]] = []
        for group_name, value in parser.items("options.entry_points"):
            for raw_line in value.splitlines():
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                name, target = line.split("=", 1)
                entries.append(
                    {
                        "group": group_name,
                        "name": name.strip(),
                        "target": target.strip(),
                        "source_file": source_file,
                    }
                )
        _merge_entrypoints(result, entries, source_file)


def _parse_setup_py(path: Path, project_root: Path, result: dict[str, Any], max_dependencies: int) -> None:
    """Support parse setup py behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    project_root : Path
        The project root path.
    result : dict[str, Any]
        The result value.
    max_dependencies : int
        The max dependencies value.
    """
    
    source_file = _normalize_rel_path(path, project_root)
    text, read_warnings = _read_text_best_effort(path)
    for warning in read_warnings:
        _append_parse_warning(result, source_file, warning)

    _add_package_manager_signal(result, "setup.py")
    result["packaging_files_found"].append(source_file)

    name_match = re.search(r'name\s*=\s*[\'\"]([^\'\"]+)[\'\"]', text)
    version_match = re.search(r'version\s*=\s*[\'\"]([^\'\"]+)[\'\"]', text)
    if name_match:
        _set_if_empty(result, "project_name", name_match.group(1), source_file)
    if version_match:
        _set_if_empty(result, "declared_version", version_match.group(1), source_file)

    install_requires_match = re.search(r"install_requires\s*=\s*\[(.*?)\]", text, re.DOTALL)
    if install_requires_match:
        dependencies = re.findall(r'[\'\"]([^\'\"]+)[\'\"]', install_requires_match.group(1))
        clean_dependencies = [dep for dep in (_clean_dependency_line(item) for item in dependencies) if dep and not _is_suspicious_dependency_line(dep)]
        _merge_dependencies(result, clean_dependencies, max_dependencies, source_file)

    entries: list[dict[str, str]] = []
    console_script_block = re.search(r"console_scripts\s*[:=]\s*\[(.*?)\]", text, re.DOTALL)
    if console_script_block:
        for item in re.findall(r'[\'\"]([^\'\"]+)[\'\"]', console_script_block.group(1)):
            if "=" not in item:
                continue
            name, target = item.split("=", 1)
            entries.append(
                {
                    "group": "console_scripts",
                    "name": name.strip(),
                    "target": target.strip(),
                    "source_file": source_file,
                }
            )
    _merge_entrypoints(result, entries, source_file)


def _parse_pipfile(path: Path, project_root: Path, result: dict[str, Any], max_dependencies: int) -> None:
    """Support parse pipfile behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    project_root : Path
        The project root path.
    result : dict[str, Any]
        The result value.
    max_dependencies : int
        The max dependencies value.
    """
    
    source_file = _normalize_rel_path(path, project_root)
    text, read_warnings = _read_text_best_effort(path)
    for warning in read_warnings:
        _append_parse_warning(result, source_file, warning)

    _add_package_manager_signal(result, "pipenv")
    result["packaging_files_found"].append(source_file)

    if _tomllib is not None:
        try:
            data = _tomllib.loads(text)
        except Exception:
            data = {}
    else:
        data = {}

    dependencies: list[str] = []
    optional_dependencies: dict[str, list[str]] = {}
    packages = data.get("packages", {}) if isinstance(data, dict) else {}
    dev_packages = data.get("dev-packages", {}) if isinstance(data, dict) else {}

    if isinstance(packages, dict):
        dependencies.extend(str(name) for name in packages.keys())
    if isinstance(dev_packages, dict):
        optional_dependencies["dev"] = [str(name) for name in dev_packages.keys()]

    _merge_dependencies(result, dependencies, max_dependencies, source_file)
    _merge_optional_dependencies(result, optional_dependencies, max_dependencies, source_file)


def _parse_lockfile_names(path: Path, project_root: Path, result: dict[str, Any], signal_name: str, max_dependencies: int) -> None:
    """Support parse lockfile names behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    project_root : Path
        The project root path.
    result : dict[str, Any]
        The result value.
    signal_name : str
        The signal name value.
    max_dependencies : int
        The max dependencies value.
    """
    
    source_file = _normalize_rel_path(path, project_root)
    text, read_warnings = _read_text_best_effort(path)
    for warning in read_warnings:
        _append_parse_warning(result, source_file, warning)
    names = re.findall(r'(?m)^\s*name\s*=\s*"([^"]+)"\s*$', text)

    _add_package_manager_signal(result, signal_name)
    result["packaging_files_found"].append(source_file)
    _merge_dependencies(result, names, max_dependencies, source_file)
