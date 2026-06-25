"""Default ignore-rule handling for the ignore-rules tab."""

from __future__ import annotations

from kanda_reasoner_app.project_root_resolver import is_reasoner_project_root

__all__ = [
    "IgnoreRulesDefaultsMixin",
]


class IgnoreRulesDefaultsMixin:
    """Provide default and Project-Reasoner-specific ignore rules."""

    def _is_reasoner_project_root(self) -> bool:
        """Return True when the active root appears to be Project Reasoner."""
        if self._project_root is None:
            return False

        return is_reasoner_project_root(self._project_root)

    def _reasoner_project_folder_defaults(self) -> list[str]:
        """Return noisy-source defaults for Project Reasoner only."""
        if not self._is_reasoner_project_root():
            return []

        return [
            "LEGACY_PROJECT_older",
            "snippets",
            "legacy_cleanup",
            "oldies_deprecated",
            "older_deprecated",
            "LOGIC_insert_mssg_dcstrngs",
            "CHATS_insrt_mssg_dcstrngs",
            "old",
            "older",
            "oldies",
            "deprecated",
            "archive",
            "backup",
            "backups",
            "original_backups",
            "_package_move_backup",
            "zz_scalp_mesh_viewer_old_deprecated",
            "dev_tools_docs",
            "*deprecated*",
            "*older*",
            "*oldies*",
            "*backup*",
            "*copy*",
            "*scratch*",
            "workbench",
        ]

    def _default_rules(self) -> dict[str, list[str]]:
        """Return project-agnostic defaults plus profile-specific rules."""
        folders = [
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
            ".project_reference",
    "_project_reference",
            "project_freeze_ledger",
        ]
        folders.extend(self._reasoner_project_folder_defaults())

        return {
            "folders": folders,
            "files": [
                "*.log",
                "*.tmp",
            ],
            "extensions": [".pyc", ".pyo", ".log", ".tmp", ".bak", ".swp"],
        }

    def _merge_with_default_rules(
        self,
        rules: dict[str, list[str]],
    ) -> dict[str, list[str]]:
        """Add new built-in exclusions without removing project-specific rules."""
        default = self._default_rules()
        merged: dict[str, list[str]] = {}
        for key in ("folders", "files", "extensions"):
            values: list[str] = []
            seen: set[str] = set()
            for item in list(rules.get(key, [])) + list(default.get(key, [])):
                text = str(item or "").strip()
                if not text:
                    continue
                marker = text.lower()
                if marker in seen:
                    continue
                seen.add(marker)
                values.append(text)
            merged[key] = values
        return merged
