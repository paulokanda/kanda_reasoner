"""Focused contract tests for Project Symbol Atlas CLI command helpers."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.safety_suite_cli.reasoner_symbol_atlas_commands import (  # noqa: E402
    add_reasoner_symbol_atlas_parsers,
    reasoner_symbol_atlas_cli_commands,
)


def test_reasoner_symbol_atlas_commands_public_contract() -> None:
    """The CLI helper exposes its documented public API."""
    assert callable(add_reasoner_symbol_atlas_parsers)
    assert callable(reasoner_symbol_atlas_cli_commands)


def test_reasoner_symbol_atlas_commands_register_expected_parsers() -> None:
    """The CLI helper registers Project Symbol Atlas commands."""
    parser = argparse.ArgumentParser(prog="safety-suite-test")
    subparsers = parser.add_subparsers(dest="command")

    add_reasoner_symbol_atlas_parsers(subparsers)

    actions = [action for action in parser._actions if isinstance(action, argparse._SubParsersAction)]
    assert actions, "Expected one subparser action."
    choices = set(actions[0].choices)

    expected = {
        "atlas-report",
        "symbol-atlas",
        "evidence-freshness",
        "find-symbol",
        "find-owner",
        "facade-owner",
        "main-helpers",
        "related-files",
        "logic-placement",
        "pre-patch-gate",
    }
    missing = expected.difference(choices)
    assert not missing, "Missing parser choices: " + ", ".join(sorted(missing))


def main() -> int:
    """Run tests directly without pytest."""
    test_reasoner_symbol_atlas_commands_public_contract()
    test_reasoner_symbol_atlas_commands_register_expected_parsers()
    print("Project Symbol Atlas CLI command helper contract tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
