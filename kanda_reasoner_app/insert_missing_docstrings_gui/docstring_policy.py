#!/usr/bin/env python3
# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/docstring_policy.py
"""Project-level policy for AI-generated docstrings."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass
class DocstringPolicy:
    """Project-specific documentation rules.

    The policy layer complements generic validator and config settings with
    repository conventions. Missing keys fall back to sensible defaults so the
    tool remains usable even when no policy file exists.
    """

    style: str = "numpy"
    module_summary_max_sentences: int = 2
    max_source_lines_in_prompt: int = 80
    max_import_lines_in_prompt: int = 10
    max_sibling_docstrings_in_prompt: int = 3
    include_attributes_for_classes: bool = True
    include_raises_section: bool = True
    include_private_by_default: bool = True
    require_module_docstrings: bool = True
    require_init_module_docstrings: bool = False
    prefer_todo_for_unknowns: bool = True
    class_requires_attributes_when_detected: bool = True
    notes_enabled: bool = False
    required_sections_by_kind: dict[str, list[str]] = field(
        default_factory=lambda: {
            "module": [],
            "class": [],
            "function": ["Parameters", "Returns"],
            "method": ["Parameters", "Returns"],
        }
    )

    @classmethod
    def default(cls) -> "DocstringPolicy":
        """Support default behavior.
        
        Returns
        -------
        'DocstringPolicy'
            The 'docstring policy' result.
        """
        
        return cls()

    @classmethod
    def from_json(cls, path: str | Path) -> "DocstringPolicy":
        """Support from json behavior.
        
        Parameters
        ----------
        path : str | Path
            The file or folder path.
        
        Returns
        -------
        'DocstringPolicy'
            The 'docstring policy' result.
        """
        
        policy_path = Path(path)
        if not policy_path.exists():
            raise FileNotFoundError(f"Docstring policy not found: {policy_path}")
        raw = json.loads(policy_path.read_text(encoding="utf-8"))
        known = {name for name in cls.__dataclass_fields__}
        unknown = set(raw) - known
        if unknown:
            raise ValueError(f"Unknown DocstringPolicy keys: {sorted(unknown)}")
        return cls(**raw)

    @classmethod
    def load_for_project(cls, root: str | Path) -> "DocstringPolicy":
        """Load the for project.
        
        Parameters
        ----------
        root : str | Path
            The root path.
        
        Returns
        -------
        'DocstringPolicy'
            The 'docstring policy' result.
        """
        
        root_path = Path(root)
        for filename in ("docstring_policy.json", ".docstring_policy.json"):
            candidate = root_path / filename
            if candidate.exists():
                return cls.from_json(candidate)
        return cls.default()

    def to_json(self, path: str | Path) -> None:
        """Support to json behavior.
        
        Parameters
        ----------
        path : str | Path
            The file or folder path.
        """
        
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(asdict(self), indent=2, ensure_ascii=False), encoding="utf-8")

    def prompt_rules_for_kind(self, kind: str) -> list[str]:
        """Support prompt rules for kind behavior.
        
        Parameters
        ----------
        kind : str
            The kind value.
        
        Returns
        -------
        list[str]
            The list of values.
        """
        
        rules: list[str] = []
        if self.prefer_todo_for_unknowns:
            rules.append("If details are unclear, use TODO placeholders instead of guessing.")
        required = self.required_sections_by_kind.get(kind, [])
        if required:
            rules.append(f"Preferred sections for {kind}: {', '.join(required)}.")
        if kind == "class" and self.class_requires_attributes_when_detected:
            rules.append("Include an Attributes section when class fields are visible in code.")
        if kind in {"function", "method"} and self.include_raises_section:
            rules.append("Include Raises only for exceptions supported by the source.")
        return rules
