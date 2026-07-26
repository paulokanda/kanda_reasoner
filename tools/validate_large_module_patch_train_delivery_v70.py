"""Forward-compatible validation of historical patch-train behavior after delegation to current Class 05 owners."""

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
    print("PATCH_TRAIN_DELIVERY_DELEGATED_TO_CLASS05: PASS")
    print("VALIDATION OK: large-module-patch-train-delivery-v7-0")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
