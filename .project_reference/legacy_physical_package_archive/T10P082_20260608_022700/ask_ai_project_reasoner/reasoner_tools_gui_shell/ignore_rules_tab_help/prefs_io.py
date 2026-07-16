"""Preference loading and saving for the ignore-rules tab."""

from __future__ import annotations

__all__ = [
    "IgnoreRulesPrefsMixin",
]

import json

from PySide6.QtWidgets import QMessageBox


class IgnoreRulesPrefsMixin:
    """Provide persistence operations for ignore-rules state."""

    def _read_prefs(self) -> dict:
        """Read the shared GUI prefs file."""
        try:
            if self.prefs_path.exists():
                data = json.loads(self.prefs_path.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    return data
        except Exception:
            pass
        return {}

    def _write_prefs(self, data: dict) -> None:
        """Write the shared GUI prefs file."""
        self.prefs_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def _get_project_rules_from_prefs(
        self,
        data: dict,
    ) -> dict[str, list[str]] | None:
        """Return saved rules for the active project, if present."""
        project_rules = data.get("project_ignore_rules", {})
        if isinstance(project_rules, dict):
            rules = project_rules.get(self._project_key)
            if isinstance(rules, dict):
                return {
                    "folders": list(rules.get("folders", [])),
                    "files": list(rules.get("files", [])),
                    "extensions": list(rules.get("extensions", [])),
                }

        legacy_rules = data.get("ignore_rules", {})
        if self._project_key == "__global__" and isinstance(legacy_rules, dict):
            return {
                "folders": list(legacy_rules.get("folders", [])),
                "files": list(legacy_rules.get("files", [])),
                "extensions": list(legacy_rules.get("extensions", [])),
            }

        if (
            self._project_key != "__global__"
            and self._is_reasoner_project_root()
            and isinstance(legacy_rules, dict)
            and not isinstance(project_rules, dict)
        ):
            return {
                "folders": list(legacy_rules.get("folders", [])),
                "files": list(legacy_rules.get("files", [])),
                "extensions": list(legacy_rules.get("extensions", [])),
            }

        return None

    def _load_rules(self) -> None:
        """Load the rule set for the active project key."""
        self._loading_rules = True
        try:
            data = self._read_prefs()
            rules = self._get_project_rules_from_prefs(data)
            if rules is None:
                rules = self._default_rules()
            else:
                rules = self._merge_with_default_rules(rules)
            self._rules = rules
            self._populate_list(self.folder_list, rules.get("folders", []))
            self._populate_list(self.file_list, rules.get("files", []))
            self._populate_list(self.ext_list, rules.get("extensions", []))
        except Exception:
            rules = self._default_rules()
            self._rules = rules
            self._populate_list(self.folder_list, rules.get("folders", []))
            self._populate_list(self.file_list, rules.get("files", []))
            self._populate_list(self.ext_list, rules.get("extensions", []))
        finally:
            self._loading_rules = False

    def _save_rules(self) -> None:
        """Save the current rule lists for the active project key."""
        if self._loading_rules:
            return

        folders = [
            self.folder_list.item(i).text()
            for i in range(self.folder_list.count())
        ]
        files = [
            self.file_list.item(i).text()
            for i in range(self.file_list.count())
        ]
        extensions = [
            self.ext_list.item(i).text()
            for i in range(self.ext_list.count())
        ]
        self._rules = {"folders": folders, "files": files, "extensions": extensions}

        try:
            data = self._read_prefs()
            project_rules = data.get("project_ignore_rules", {})
            if not isinstance(project_rules, dict):
                project_rules = {}
            project_rules[self._project_key] = self._rules
            data["project_ignore_rules"] = project_rules
            data["active_project_ignore_rules_key"] = self._project_key
            data["ignore_rules"] = self._rules
            self._write_prefs(data)
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"Failed to save rules: {exc}")

    def _reset_defaults(self) -> None:
        """Reset the active project's exclusions to default rules."""
        default = self._default_rules()
        self._populate_list(self.folder_list, default["folders"])
        self._populate_list(self.file_list, default["files"])
        self._populate_list(self.ext_list, default["extensions"])
        self._save_rules()
