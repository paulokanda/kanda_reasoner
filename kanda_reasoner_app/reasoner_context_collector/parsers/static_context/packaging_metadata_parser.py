# project-path: kanda_reasoner_app/reasoner_context_collector/parsers/static_context/packaging_metadata_parser.py
"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

import logging

import configparser
import re
from pathlib import Path
from typing import Any

try:
    import tomllib  # Python 3.11+
except ImportError:  # pragma: no cover
    _tomllib = None


# PASS_068A_TOMLLIB_ALIAS_START
try:
    _tomllib
except NameError:
    try:
        _tomllib = tomllib
    except NameError:
        _tomllib = None
# PASS_068A_TOMLLIB_ALIAS_END
DEFAULT_PACKAGING_FILE_PATTERNS: tuple[str, ...] = (
    "pyproject.toml",
    "requirements*.txt",
    "setup.py",
    "setup.cfg",
    "Pipfile",
    "poetry.lock",
    "uv.lock",
)


def _normalize_rel_path(path: Path, root: Path) -> str:
    """Support normalize rel path behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    root : Path
        The root path.
    
    Returns
    -------
    str
        The string result.
    """
    
    return str(path.relative_to(root)).replace("\\", "/")


def _truncate_text(value: str, max_chars: int = 200) -> str:
    """Support truncate text behavior.
    
    Parameters
    ----------
    value : str
        The input value.
    max_chars : int, optional
        The optional max chars value.
    
    Returns
    -------
    str
        The string result.
    """
    
    value = value.strip()
    if len(value) <= max_chars:
        return value
    return value[: max_chars - 3].rstrip() + "..."


def _dedupe_keep_order(items: list[str]) -> list[str]:
    """Support dedupe keep order behavior.
    
    Parameters
    ----------
    items : list[str]
        The item values.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        normalized = str(item).strip()
        if not normalized:
            continue
        key = normalized.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(normalized)
    return out


def _new_result() -> dict[str, Any]:
    """Support new result behavior.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    return {
        "project_name": "",
        "declared_version": "",
        "build_backend": "",
        "package_manager_signals": [],
        "declared_dependencies": [],
        "declared_optional_dependencies": {},
        "declared_entrypoints": [],
        "declared_tooling": {},
        "packaging_files_found": [],
        "packaging_evidence": [],
        "packaging_parse_warnings": [],
        "packaging_confidence": "unknown",
    }


def _append_evidence(result: dict[str, Any], source_file: str, field_name: str, value: str) -> None:
    """Support append evidence behavior.
    
    Parameters
    ----------
    result : dict[str, Any]
        The result value.
    source_file : str
        The source file value.
    field_name : str
        The field name value.
    value : str
        The input value.
    """
    
    result["packaging_evidence"].append(
        {
            "source_file": source_file,
            "field": field_name,
            "value_excerpt": _truncate_text(value),
        }
    )


def _append_parse_warning(result: dict[str, Any], source_file: str, message: str) -> None:
    """Support append parse warning behavior.
    
    Parameters
    ----------
    result : dict[str, Any]
        The result value.
    source_file : str
        The source file value.
    message : str
        The message text.
    """
    
    warning = f"{source_file}: {message}" if source_file else message
    result["packaging_parse_warnings"].append(warning)


def _add_package_manager_signal(result: dict[str, Any], signal: str) -> None:
    """Support add package manager signal behavior.
    
    Parameters
    ----------
    result : dict[str, Any]
        The result value.
    signal : str
        The signal value.
    """
    
    if signal not in result["package_manager_signals"]:
        result["package_manager_signals"].append(signal)


def _set_if_empty(result: dict[str, Any], key: str, value: str, source_file: str) -> None:
    """Support set if empty behavior.
    
    Parameters
    ----------
    result : dict[str, Any]
        The result value.
    key : str
        The key value.
    value : str
        The input value.
    source_file : str
        The source file value.
    """
    
    cleaned = value.strip()
    if cleaned and not result.get(key):
        result[key] = cleaned
        _append_evidence(result, source_file, key, cleaned)


def _merge_dependencies(result: dict[str, Any], dependencies: list[str], max_dependencies: int, source_file: str) -> None:
    """Support merge dependencies behavior.
    
    Parameters
    ----------
    result : dict[str, Any]
        The result value.
    dependencies : list[str]
        The dependencies value.
    max_dependencies : int
        The max dependencies value.
    source_file : str
        The source file value.
    """
    
    current = list(result["declared_dependencies"])
    result["declared_dependencies"] = _dedupe_keep_order(current + dependencies)[:max_dependencies]
    for dep in dependencies[:20]:
        _append_evidence(result, source_file, "declared_dependencies", dep)


def _merge_optional_dependencies(
    result: dict[str, Any],
    optional_dependencies: dict[str, list[str]],
    max_dependencies: int,
    source_file: str,
) -> None:
    """Support merge optional dependencies behavior.
    
    Parameters
    ----------
    result : dict[str, Any]
        The result value.
    optional_dependencies : dict[str, list[str]]
        The optional dependencies value.
    max_dependencies : int
        The max dependencies value.
    source_file : str
        The source file value.
    """
    
    current = dict(result["declared_optional_dependencies"])
    for extra_name, deps in optional_dependencies.items():
        merged = _dedupe_keep_order(current.get(extra_name, []) + deps)[:max_dependencies]
        current[extra_name] = merged
        for dep in deps[:20]:
            _append_evidence(result, source_file, f"declared_optional_dependencies.{extra_name}", dep)
    result["declared_optional_dependencies"] = current


def _merge_entrypoints(result: dict[str, Any], entries: list[dict[str, str]], source_file: str) -> None:
    """Support merge entrypoints behavior.
    
    Parameters
    ----------
    result : dict[str, Any]
        The result value.
    entries : list[dict[str, str]]
        The entries value.
    source_file : str
        The source file value.
    """
    
    current = list(result["declared_entrypoints"])
    seen = {(item.get("group", ""), item.get("name", ""), item.get("target", "")) for item in current if isinstance(item, dict)}
    for entry in entries:
        key = (entry.get("group", ""), entry.get("name", ""), entry.get("target", ""))
        if key in seen:
            continue
        seen.add(key)
        current.append(entry)
        _append_evidence(result, source_file, "declared_entrypoints", f"{entry.get('group', '')}:{entry.get('name', '')}={entry.get('target', '')}")
    result["declared_entrypoints"] = current


def _merge_tooling(result: dict[str, Any], tooling: dict[str, Any], source_file: str) -> None:
    """Support merge tooling behavior.
    
    Parameters
    ----------
    result : dict[str, Any]
        The result value.
    tooling : dict[str, Any]
        The tooling value.
    source_file : str
        The source file value.
    """
    
    current = dict(result["declared_tooling"])
    for key, value in tooling.items():
        if key not in current:
            current[key] = value
            _append_evidence(result, source_file, f"declared_tooling.{key}", str(value))
    result["declared_tooling"] = current


def _looks_nul_padded(text: str) -> bool:
    """Support looks nul padded behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    if not text:
        return False
    nul_count = text.count("\x00")
    return nul_count > 0 and (nul_count / max(1, len(text))) >= 0.05


def _read_text_best_effort(path: Path) -> tuple[str, list[str]]:
    """Support read text best effort behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    tuple[str, list[str]]
        The tuple of values.
    """
    
    warnings: list[str] = []
    raw = path.read_bytes()
    if not raw:
        return "", warnings
    if b"\x00" in raw:
        for encoding in ("utf-16", "utf-16-le", "utf-16-be"):
            try:
                text = raw.decode(encoding)
                warnings.append(f"decoded with {encoding} after NUL-byte detection")
                return text.replace("\ufeff", ""), warnings
            except Exception:
                continue
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("utf-8", errors="replace")
        warnings.append("decoded with utf-8 replacement")
    if _looks_nul_padded(text):
        warnings.append("removed NUL padding from decoded text")
        text = text.replace("\x00", "")
    return text.replace("\ufeff", ""), warnings


def _clean_dependency_line(line: str) -> str:
    """Support clean dependency line behavior.
    
    Parameters
    ----------
    line : str
        The line value.
    
    Returns
    -------
    str
        The string result.
    """
    
    cleaned = line.strip().replace("\x00", "")
    if not cleaned:
        return ""
    if " #" in cleaned:
        cleaned = cleaned.split(" #", 1)[0].rstrip()
    if " ;" in cleaned:
        cleaned = cleaned.split(" ;", 1)[0].rstrip()
    if cleaned.lower().startswith("-e "):
        cleaned = cleaned[3:].strip()
    if "@ file://" in cleaned.lower():
        cleaned = cleaned.split("@", 1)[0].strip()
    return cleaned


def _is_suspicious_dependency_line(line: str) -> bool:
    """Support is suspicious dependency line behavior.
    
    Parameters
    ----------
    line : str
        The line value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    if not line:
        return True
    lowered = line.lower()
    if "\ufffd" in line or "\x00" in line:
        return True
    if any(token in lowered for token in ("original file:", "source file:", "included fonts", "pytest's cache plugin")):
        return True
    alnum = sum(ch.isalnum() for ch in line)
    return alnum == 0


def _discover_packaging_files(project_root: Path, file_patterns: tuple[str, ...]) -> list[Path]:
    """Support discover packaging files behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    file_patterns : tuple[str, ...]
        The file patterns value.
    
    Returns
    -------
    list[Path]
        The list of values.
    """
    
    found: list[Path] = []
    for pattern in file_patterns:
        for path in project_root.glob(pattern):
            if path.is_file():
                found.append(path)
        for path in project_root.glob(f"**/{pattern}"):
            if path.is_file():
                found.append(path)
    unique: dict[str, Path] = {}
    for path in found:
        unique[str(path.resolve()).lower()] = path.resolve()
    return sorted(unique.values(), key=lambda item: str(item).lower())


def _parse_dependency_lines(text: str) -> list[str]:
    """Support parse dependency lines behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    dependencies: list[str] = []
    for raw_line in text.splitlines():
        if "\x00" in raw_line:
            continue
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith(("-r", "--requirement", "--find-links", "-f", "--extra-index-url", "--index-url")):
            continue
        cleaned = _clean_dependency_line(line)
        if not cleaned or _is_suspicious_dependency_line(cleaned):
            continue
        dependencies.append(cleaned)
    return _dedupe_keep_order(dependencies)


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


# PASS_070B_STATIC_CONTEXT_SCOPE_OVERRIDE
def _discover_packaging_files(root, *args, **kwargs):
    """Support discover packaging files behavior.
    
    Parameters
    ----------
    root : object
        The root path.
    *args : object
        The positional arguments.
    **kwargs : object
        The kwargs value.
    """
    
    from kanda_reasoner_app.reasoner_context_collector.collector_scope import iter_project_packaging_files
    return list(iter_project_packaging_files(root))
