"""Focused public-contract test for Project Symbol Atlas CLI module."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.safety_suite_cli import (  # noqa: E402
    reasoner_symbol_atlas_commands,
)


def test_pa019b_cli_module_public_contract_is_importable() -> None:
    """The atlas CLI helper must expose its documented public API."""
    exported_names = set(reasoner_symbol_atlas_commands.__all__)

    assert "add_reasoner_symbol_atlas_parsers" in exported_names
    assert "reasoner_symbol_atlas_cli_commands" in exported_names
    assert callable(reasoner_symbol_atlas_commands.add_reasoner_symbol_atlas_parsers)
    assert isinstance(reasoner_symbol_atlas_commands.reasoner_symbol_atlas_cli_commands(), tuple)


def test_pa019b_cli_module_registers_atlas_commands() -> None:
    """The public parser-registration API must add atlas subcommands."""
    parser = argparse.ArgumentParser(prog="safety-suite-test")
    subparsers = parser.add_subparsers(dest="command")

    reasoner_symbol_atlas_commands.add_reasoner_symbol_atlas_parsers(subparsers)

    registered = set(subparsers.choices)
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

    missing = expected - registered
    assert not missing, "missing atlas CLI commands: " + ", ".join(sorted(missing))


def main() -> int:
    """Run focused tests without pytest."""
    test_pa019b_cli_module_public_contract_is_importable()
    test_pa019b_cli_module_registers_atlas_commands()
    print("PA019B Project Symbol Atlas CLI module contract tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
