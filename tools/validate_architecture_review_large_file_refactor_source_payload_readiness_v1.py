# project-path: tools/validate_architecture_review_large_file_refactor_source_payload_readiness_v1.py
"""Run the source payload readiness feature validation."""
from __future__ import annotations

import runpy
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VALIDATION_SCRIPT = (
    PROJECT_ROOT
    / "validation"
    / "test_architecture_review_large_file_refactor_source_payload_readiness_v1.py"
)

FEATURE_ID = "architecture-review-large-file-refactor-source-payload-readiness-v1"

def main() -> int:
    """Run the validation script without importing a test module."""
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    namespace = runpy.run_path(str(VALIDATION_SCRIPT))
    namespace["test_source_payload_readiness"]()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
