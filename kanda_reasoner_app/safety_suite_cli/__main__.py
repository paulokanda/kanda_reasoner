# project-path: kanda_reasoner_app/safety_suite_cli/__main__.py
"""Executable public entry point for the KANDA safety-suite CLI."""

from __future__ import annotations

from .commands import main


if __name__ == "__main__":
    raise SystemExit(main())
