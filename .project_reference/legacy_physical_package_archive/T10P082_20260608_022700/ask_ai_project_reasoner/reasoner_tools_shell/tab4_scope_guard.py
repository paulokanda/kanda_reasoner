"""Dynamic scope guard helpers for Tab 4 project collection.

Tab 4 must collect only inside the project root selected by the user.
The selected root is dynamic: it may be this Project Reasoner checkout or
another project folder. Broad roots such as a drive root are rejected and
resolved to the active tool project when no safer project root is available.
Tab 8 non-project rules are loaded from GUI preferences and exported to
runtime and collector subprocesses.
"""

from __future__ import annotations

__all__ = [
    "apply_tab4_scope_environment",
    "is_broad_scan_root",
    "is_inside_project_root",
    "load_tab8_ignore_rules",
    "resolve_tab4_project_root",
    "tab8_rules_to_env_json",
]

import json
import os
from pathlib import Path

CANONICAL_PACKAGE_NAME = "kanda_reasoner_app"
LEGACY_PACKAGE_NAME = "_".join(("ask", "ai", "project", "reasoner"))


def _reasoner_package_dirs(root: Path) -> list[Path]:
    return [root / LEGACY_PACKAGE_NAME, root / CANONICAL_PACKAGE_NAME]


def _has_reasoner_package(root: Path) -> bool:
    return any(path.is_dir() for path in _reasoner_package_dirs(root))


def _installed_package_dir(root: Path) -> Path:
    for path in _reasoner_package_dirs(root):
        if path.is_dir():
            return path
    return root / LEGACY_PACKAGE_NAME


def _safe_resolve(path: Path) -> Path:
    """Resolve a path without failing on inaccessible locations."""
    try:
        return path.expanduser().resolve()
    except Exception:
        return path.expanduser()


def _module_project_root() -> Path:
    """Return the project root that contains this helper module."""
    here = _safe_resolve(Path(__file__))
    for parent in here.parents:
        if _has_reasoner_package(parent):
            return parent
    if len(here.parents) >= 3:
        return here.parents[2]
    return here.parent


def _path_from_value(value: object | None) -> Path | None:
    """Convert a user/environment value to a path."""
    if value is None:
        return None
    text = str(value).strip().strip('"')
    if not text:
        return None
    try:
        return _safe_resolve(Path(text))
    except Exception:
        return None


def _looks_like_package_root(path: Path) -> bool:
    """Return True when path contains the Reasoner package."""
    try:
        return _has_reasoner_package(path)
    except Exception:
        return False


def is_broad_scan_root(path: object) -> bool:
    """Return True for roots that are too broad for Tab 4 collection."""
    candidate = _path_from_value(path)
    if candidate is None:
        return True
    try:
        resolved = _safe_resolve(candidate)
        anchor = Path(resolved.anchor) if resolved.anchor else None
        if anchor is not None and resolved == anchor:
            return True
        home = _safe_resolve(Path.home())
        if resolved == home:
            return True
        # Avoid treating the Python install or an environment as a project root.
        lower_parts = {part.lower() for part in resolved.parts}
        if "site-packages" in lower_parts:
            return True
    except Exception:
        return True
    return False


def _normalize_candidate(candidate: Path) -> Path:
    """Normalize a candidate project root without hard-coded project names."""
    candidate = _safe_resolve(candidate)
    if candidate.is_file():
        candidate = candidate.parent
    if candidate.name in {LEGACY_PACKAGE_NAME, CANONICAL_PACKAGE_NAME}:
        return candidate.parent
    return candidate


def _env_project_root_values() -> list[object]:
    """Return environment values that may carry the active project root."""
    keys = [
        "PROJECT_REASONER_PROJECT_ROOT",
        "KANDA_RUNTIME_PROJECT_ROOT",
        "PROJECT_REASONER_SCAN_ROOT",
        "KANDA_REASONER_SCAN_ROOT",
        "PROJECT_ROOT",
    ]
    return [os.environ.get(key) for key in keys]


def resolve_tab4_project_root(raw: object | None, fallback: object | None = None) -> Path:
    """Resolve the Tab 4 project root dynamically.

    Rules:
    1. Respect the selected root when it is a real, non-broad directory.
    2. If the user selected the package folder, use its parent project folder.
    3. If a broad root such as a drive root was selected, fall back to the
       current tool project root instead of scanning the whole drive.
    4. Never hard-code a specific path or project folder name.
    """
    module_root = _module_project_root()
    values: list[object] = [raw, fallback]
    values.extend(_env_project_root_values())

    broad_candidates: list[Path] = []
    for value in values:
        candidate = _path_from_value(value)
        if candidate is None:
            continue
        candidate = _normalize_candidate(candidate)
        if is_broad_scan_root(candidate):
            broad_candidates.append(candidate)
            continue
        return candidate

    for candidate in broad_candidates:
        try:
            module_root.relative_to(candidate)
            return module_root
        except (OSError, json.JSONDecodeError, TypeError):
            continue

    return module_root


def is_inside_project_root(path: object, project_root: object) -> bool:
    """Return True when path is inside project_root."""
    try:
        value = _safe_resolve(Path(str(path)))
        root = resolve_tab4_project_root(project_root)
        value.relative_to(root)
        return True
    except Exception:
        return False


def _dedupe(values: list[object]) -> list[str]:
    """Deduplicate rule values while preserving order."""
    output: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = str(value or "").strip()
        if not text:
            continue
        marker = text.lower()
        if marker in seen:
            continue
        seen.add(marker)
        output.append(text)
    return output


def _project_agnostic_default_rules() -> dict[str, list[str]]:
    """Return project-agnostic default exclusions."""
    return {
        "folders": [
            "__pycache__",
            ".git",
            ".idea",
            ".vscode",
            ".pytest_cache",
            ".mypy_cache",
            ".ruff_cache",
            ".coverage",
            "htmlcov",
            ".venv",
            "venv",
            "env",
            "build",
            "dist",
            "node_modules",
        ],
        "files": ["*.log", "*.tmp"],
        "extensions": [".pyc", ".pyo", ".log", ".tmp", ".bak", ".swp"],
    }


def _candidate_project_keys(root: Path) -> list[str]:
    """Return possible preference keys for a project root."""
    keys = []
    for value in (root, _safe_resolve(root)):
        text = str(value)
        if text not in keys:
            keys.append(text)
    return keys


def _merge_rules(base: dict[str, list[str]], extra: object) -> dict[str, list[str]]:
    """Merge a rules payload into a base rules dictionary."""
    if not isinstance(extra, dict):
        return base
    for key in ("folders", "files", "extensions"):
        base[key] = _dedupe(list(extra.get(key, [])) + list(base.get(key, [])))
    return base


def load_tab8_ignore_rules(project_root: object) -> dict[str, list[str]]:
    """Load Tab 8 ignore rules for project_root and merge generic defaults."""
    root = resolve_tab4_project_root(project_root)
    rules = _project_agnostic_default_rules()
    prefs_candidates = [
        root / ".reasoner_tools_gui_prefs.json",
        _installed_package_dir(root) / "reasoner_tools_shell" / ".collector_runner_prefs.json",
    ]

    for prefs_path in prefs_candidates:
        try:
            if not prefs_path.exists():
                continue
            data = json.loads(prefs_path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                continue
            project_rules = data.get("project_ignore_rules", {})
            if isinstance(project_rules, dict):
                for key in _candidate_project_keys(root):
                    if key in project_rules:
                        rules = _merge_rules(rules, project_rules.get(key))
                        break
            rules = _merge_rules(rules, data.get("ignore_rules"))
            rules = _merge_rules(rules, data.get("tab8_ignore_rules"))
            rules = _merge_rules(rules, data.get("project_exclusion_rules"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, TypeError):
            continue

    for key in ("folders", "files", "extensions"):
        rules[key] = _dedupe(list(rules.get(key, [])))
    return rules


def tab8_rules_to_env_json(project_root: object) -> str:
    """Serialize Tab 8 rules for child subprocesses."""
    return json.dumps(load_tab8_ignore_rules(project_root), ensure_ascii=True, sort_keys=True)


def apply_tab4_scope_environment(env: dict[str, str], project_root: object) -> dict[str, str]:
    """Return an environment constrained to the dynamic Tab 4 project root."""
    root = resolve_tab4_project_root(project_root)
    root_text = str(root)
    env = dict(env)
    current_pythonpath = env.get("PYTHONPATH", "")
    path_parts = [part for part in current_pythonpath.split(os.pathsep) if part]
    if root_text not in path_parts:
        path_parts.insert(0, root_text)
    env["PYTHONPATH"] = os.pathsep.join(path_parts)
    rules_json = tab8_rules_to_env_json(root)
    env["PROJECT_REASONER_PROJECT_ROOT"] = root_text
    env["KANDA_RUNTIME_PROJECT_ROOT"] = root_text
    env["PROJECT_REASONER_SCAN_ROOT"] = root_text
    env["KANDA_REASONER_SCAN_ROOT"] = root_text
    env["PROJECT_REASONER_IGNORE_RULES_JSON"] = rules_json
    env["PROJECT_REASONER_TAB8_IGNORE_RULES_JSON"] = rules_json
    env["KANDA_REASONER_TAB8_IGNORE_RULES_JSON"] = rules_json
    env.setdefault("PYTHONWARNINGS", "ignore::SyntaxWarning")
    return env
