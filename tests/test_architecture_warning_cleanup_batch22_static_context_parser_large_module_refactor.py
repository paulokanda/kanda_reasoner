"""Characterization tests for static context parser large-module refactor."""

from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.reasoner_context_collector.parsers.static_context.documentation_intent_parser import (
    parse_documentation_intent,
)
from kanda_reasoner_app.reasoner_context_collector.parsers.static_context.packaging_metadata_parser import (
    parse_packaging_metadata,
)


def test_static_context_parser_facades_keep_public_behavior(tmp_path: Path) -> None:
    """Verify parser facades still collect documentation and packaging signals."""

    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (tmp_path / "README.md").write_text(
        "# Kanda Reasoner\n\n"
        "Kanda Reasoner is a project analysis tool for AI handoff.\n\n"
        "## Run\n"
        "Run with python -m kanda_reasoner_app.\n\n"
        "## Feature: Static Context\n"
        "OpenAI integration and Google Calendar references.\n",
        encoding="utf-8",
    )
    (docs_dir / "architecture.md").write_text(
        "# Architecture\n\n"
        "The app uses a GUI shell and a static context collector workflow.\n",
        encoding="utf-8",
    )
    (tmp_path / "pyproject.toml").write_text(
        "[project]\n"
        "name = \"demo-kanda\"\n"
        "version = \"1.2.3\"\n"
        "dependencies = [\"PySide6>=6\", \"requests\"]\n"
        "[project.optional-dependencies]\n"
        "dev = [\"pytest\"]\n"
        "[project.scripts]\n"
        "kanda = \"kanda_reasoner_app.__main__:main\"\n"
        "[build-system]\n"
        "build-backend = \"hatchling.build\"\n",
        encoding="utf-8",
    )

    documentation = parse_documentation_intent(tmp_path)
    packaging = parse_packaging_metadata(tmp_path)

    assert documentation["project_purpose_summary"]
    assert "README.md" in documentation["documentation_files_found"]
    assert "Feature: Static Context" in documentation["named_features"]
    assert "openai" in documentation["external_integrations"]
    assert packaging["project_name"] == "demo-kanda"
    assert packaging["declared_version"] == "1.2.3"
    assert "pyproject" in packaging["package_manager_signals"]
    assert "PySide6>=6" in packaging["declared_dependencies"]
    assert packaging["declared_optional_dependencies"]["dev"] == ["pytest"]
    assert packaging["packaging_confidence"] == "high"
