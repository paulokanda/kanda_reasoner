#!/usr/bin/env python3
# -*- coding: ascii -*-
"""Public facade for the independent KANDA Reasoner Portable workflow."""

from __future__ import annotations

import sys
from pathlib import Path

__all__ = ["main"]


def main() -> int:
    """Run the independent Portable workflow from its canonical project root."""

    sys.dont_write_bytecode = True
    project_root = Path(__file__).resolve().parents[1]
    project_root_text = str(project_root)
    if project_root_text not in sys.path:
        sys.path.insert(0, project_root_text)

    from portable.cli import main as cli_main

    return cli_main(project_root=project_root)


if __name__ == "__main__":
    raise SystemExit(main())
