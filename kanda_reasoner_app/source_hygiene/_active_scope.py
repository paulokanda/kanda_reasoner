# project-path: kanda_reasoner_app/source_hygiene/_active_scope.py
"""Private active-source scope shared by Source Hygiene scans."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from kanda_reasoner_app.project_exclusion_path_matching import (
    folder_rule_matches,
)
from kanda_reasoner_app.project_exclusion_policy import (
    load_reasoner_project_exclusion_rules,
)

__all__: list[str] = []

_EXTRA_INACTIVE_FOLDER_RULES = (
    "*backup*",
    "*copy*",
    "*deprecated*",
    "*older*",
    "*oldies*",
    "*scratch*",
    "_bundle_temp",
    "_generated",
    "_package_move_backup",
    "_temp_archived_installers",
    "_trash",
    "archive",
    "backup",
    "backups",
    "deprecated",
    "dev_tools_docs",
    "first_prompt_files",
    "json_splitted",
    "legacy_cleanup",
    "legacy_project_older",
    "log",
    "logs",
    "old",
    "older",
    "oldies",
    "original_backups",
    "runtime_scenarios",
    "scratch",
    "second_prompt_files",
    "second_prompt_files_building",
    "show_project_to_AI",
    "snippets",
    "temp",
    "tmp",
    "workbench",
)


@dataclass(frozen=True)
class _ActiveSourceScope:
    """Resolved folder-only exclusions for one project root."""

    root: Path
    folder_rules: tuple[str, ...]

    def includes(
        self,
        path: str | Path,
        *,
        exclude_tests: bool,
    ) -> bool:
        """Return whether one existing path belongs to active source scope."""
        candidate = Path(path)
        if candidate.is_symlink():
            return False
        try:
            resolved = candidate.resolve()
            relative = resolved.relative_to(self.root)
        except (OSError, ValueError):
            return False

        relative_posix = relative.as_posix()
        lowered_parts = tuple(part.casefold() for part in relative.parts)
        if not lowered_parts:
            return False
        if lowered_parts[0].startswith("."):
            return False
        if _is_test_fixture_path(lowered_parts):
            return False
        if exclude_tests and _is_test_path(lowered_parts, resolved.name):
            return False

        path_is_dir = resolved.is_dir()
        for rule in self.folder_rules:
            if folder_rule_matches(
                relative_posix,
                rule,
                path_is_dir=path_is_dir,
            ):
                return False
        return True


def _build_active_source_scope(
    project_root: str | Path,
) -> _ActiveSourceScope:
    """Build active Source Hygiene scope from canonical folder exclusions."""
    root = Path(project_root).expanduser().resolve()
    rules = load_reasoner_project_exclusion_rules(root)
    folder_rules = _deduplicate_rules(
        (
            *tuple(rules.get("folders", ())),
            *_EXTRA_INACTIVE_FOLDER_RULES,
        )
    )
    return _ActiveSourceScope(root=root, folder_rules=folder_rules)


def _deduplicate_rules(values: tuple[object, ...]) -> tuple[str, ...]:
    output: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = str(value or "").strip().replace("\\", "/")
        marker = text.casefold()
        if not text or marker in seen:
            continue
        seen.add(marker)
        output.append(text)
    return tuple(output)


def _is_test_fixture_path(parts: tuple[str, ...]) -> bool:
    try:
        tests_index = parts.index("tests")
    except ValueError:
        return False
    return "fixtures" in parts[tests_index + 1 :]


def _is_test_path(parts: tuple[str, ...], name: str) -> bool:
    lowered_name = str(name or "").casefold()
    return (
        "tests" in parts[:-1]
        or lowered_name == "conftest.py"
        or lowered_name.startswith("test_")
        or lowered_name.endswith("_test.py")
    )
