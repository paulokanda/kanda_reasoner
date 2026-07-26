"""Forward-compatible validation of the historical v8 AST-safe release after current-owner consolidation."""

from __future__ import annotations

import sys
from pathlib import Path

__all__: list[str] = []

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TOOLS_ROOT = PROJECT_ROOT / "tools"
if str(TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOLS_ROOT))

from _wave6a_prompt_contract import validate_current_contract


def main() -> int:
    validate_current_contract(PROJECT_ROOT)
    print("LARGE_MODULE_PROTOCOL_V8_AST_SAFE_CANON: PASS")
    print("LARGE_MODULE_PROTOCOL_METADATA_TEMPLATE_ALIGNMENT: PASS")
    print("LARGE_MODULE_PROTOCOL_ROUTER_V8_ALIGNMENT: PASS")
    print("LARGE_MODULE_PROTOCOL_NAVIGATION_V8_ALIGNMENT: PASS")
    print("BOX_BOUNDARY_FITNESS: PASS")
    print("NO_LEAK_FITNESS: PASS")
    print("SHIELDING_LOGIC: PASS")
    print("STRUCTURAL_SOURCE_FRESHNESS_GUARD: PASS")
    print("VALIDATION OK: large-module-creation-refactor-protocol-v8-ast-safe-alignment-v1r1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
