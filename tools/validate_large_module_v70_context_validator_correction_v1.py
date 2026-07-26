"""Forward-compatible validation of historical v7 context correction under the current source contract."""

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
    print("LARGE_MODULE_CONTEXT_VALIDATOR_FORWARD_COMPATIBLE: PASS")
    print("VALIDATION OK: large-module-v70-context-validator-correction-v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
