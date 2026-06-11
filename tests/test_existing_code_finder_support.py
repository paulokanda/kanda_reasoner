"""Contract tests for private existing-code finder support helpers."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_symbol_atlas import _existing_code_finder_support as support  # noqa: E402


def test_existing_code_finder_support_contract() -> None:
    assert hasattr(support, "run_existing_code_component_plan")
    assert hasattr(support, "structured_decision_evidence")
    assert hasattr(support, "format_existing_code_summary")
    assert support.__all__ == []


def main() -> int:
    test_existing_code_finder_support_contract()
    print("Existing code finder support contract tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
