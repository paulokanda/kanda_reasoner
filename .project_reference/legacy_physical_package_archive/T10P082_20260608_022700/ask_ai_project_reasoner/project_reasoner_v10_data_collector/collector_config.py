"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CollectorConfig:
    excluded_dirs: list[str] = field(
        default_factory=lambda: [
            ".venv",
            "venv",
            "__pycache__",
            ".git",
            ".idea",
            ".mypy_cache",
            ".pytest_cache",
            "site-packages",
            "build",
            "dist",
        ]
    )
    include_tests: bool = True
    include_vendor_code: bool = False
    max_snippet_lines: int = 40
    max_docstring_length: int = 1000

    enable_edit_ready_source_index: bool = True
    include_full_source_in_file_index: bool = True
    max_anchor_context_lines: int = 3
    max_source_excerpt_lines: int = 80
    max_full_source_chars: int = 0

    enable_web_ai_symbol_index: bool = True
    enable_primary_definition_index: bool = True
    enable_stable_evidence_id_index: bool = True
    enable_entry_points_detail: bool = True
    enable_web_ai_file_responsibility_index: bool = True
    enable_web_ai_test_protection_index: bool = True
    enable_web_ai_readme: bool = True

    enable_packaging_metadata: bool = True
    enable_documentation_intent: bool = True
    max_packaging_dependencies: int = 200
    max_doc_evidence_snippets: int = 40
    max_doc_excerpt_chars: int = 400
    documentation_glob_patterns: tuple[str, ...] = (
        "README*",
        "docs/**/*.md",
        "docs/**/*.rst",
        "**/*ADR*.md",
        "**/*architecture*.md",
        "mkdocs.yml",
        "conf.py",
    )
    packaging_file_patterns: tuple[str, ...] = (
        "pyproject.toml",
        "requirements*.txt",
        "setup.py",
        "setup.cfg",
        "Pipfile",
        "poetry.lock",
        "uv.lock",
    )