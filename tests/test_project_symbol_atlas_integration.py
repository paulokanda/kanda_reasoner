"""Canonical contract test for Engineering Safety Atlas integration."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.engineering_safety.reasoner_symbol_atlas_integration import (  # noqa: E402
    __all__ as integration_exports,
    build_engineering_safety_reasoner_symbol_atlas_context,
    engineering_safety_reasoner_symbol_atlas_evidence_lines,
    format_engineering_safety_reasoner_symbol_atlas_markdown,
)


def test_reasoner_symbol_atlas_integration_public_contract() -> None:
    assert "build_engineering_safety_reasoner_symbol_atlas_context" in integration_exports
    assert "engineering_safety_reasoner_symbol_atlas_evidence_lines" in integration_exports
    assert "format_engineering_safety_reasoner_symbol_atlas_markdown" in integration_exports
    assert callable(build_engineering_safety_reasoner_symbol_atlas_context)
    assert callable(engineering_safety_reasoner_symbol_atlas_evidence_lines)
    assert callable(format_engineering_safety_reasoner_symbol_atlas_markdown)


def main() -> int:
    test_reasoner_symbol_atlas_integration_public_contract()
    print("Engineering Safety Project Symbol Atlas integration contract tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
