# project-path: tools/validate_patch_delivery_root_drive_staging_breach_gate_v1.py
"""Run validation for root-drive staging breach enforcement."""

from __future__ import annotations

from pathlib import Path
import runpy
import sys

__all__: list[str] = []

FEATURE_ID = "patch-delivery-root-drive-staging-breach-enforcement-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    """Execute the focused validation module."""
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    validation_path = PROJECT_ROOT / "validation" / "test_patch_delivery_root_drive_staging_breach_gate_v1.py"
    namespace = runpy.run_path(str(validation_path))
    result = namespace["main"]()
    if int(result) != 0:
        raise SystemExit(result)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
