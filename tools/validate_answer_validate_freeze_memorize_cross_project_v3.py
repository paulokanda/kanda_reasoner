"""Validate the shared Answer/Validate/Freeze cross-project contract."""

from __future__ import annotations

import sys
from pathlib import Path

from _answer_validate_freeze_memorize_contract import validate_all

FEATURE_ID = "answer-validate-freeze-cross-project-routine-v3"


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    validate_all(root)
    print("TOOL_PROJECT_BOUNDARY: PASS")
    print("BUTTON_CONTEXT_ENVELOPE: PASS")
    print("NO_RETRAINING_CONTINUATION: PASS")
    print("DEPRECATED_ROUTER_BRIDGE_REJECTED: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
