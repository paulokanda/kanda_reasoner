"""Characterization tests for Batch 23 safety-suite CLI refactor."""

from __future__ import annotations

from io import StringIO

from kanda_reasoner_app.safety_suite_cli.commands import (
    available_cli_commands,
    build_safety_suite_parser,
    run_cli,
)


def test_batch23_safety_suite_cli_public_facade_still_runs() -> None:
    """Exercise the public CLI facade after private helper extraction."""

    commands = available_cli_commands()
    assert "list-tools" in commands
    assert "symbol-atlas" in commands

    parser = build_safety_suite_parser()
    parsed = parser.parse_args(["list-tools"])
    assert parsed.command == "list-tools"

    stdout = StringIO()
    stderr = StringIO()
    exit_code = run_cli(["list-tools"], stdout=stdout, stderr=stderr)

    assert exit_code == 0
    assert stderr.getvalue() == ""
    assert "list-tools" in stdout.getvalue()
    assert "symbol-atlas" in stdout.getvalue()
