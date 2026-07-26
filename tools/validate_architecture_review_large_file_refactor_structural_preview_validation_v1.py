# project-path: tools/validate_architecture_review_large_file_refactor_structural_preview_validation_v1.py
"""Run focused validation for structural real-preview validation."""
from __future__ import annotations

import runpy
from pathlib import Path


def main() -> None:
    """Execute the focused validation script."""
    root = Path(__file__).resolve().parents[1]
    script = root / "validation" / "test_architecture_review_large_file_refactor_structural_preview_validation_v1.py"
    runpy.run_path(str(script), run_name="__main__")


if __name__ == "__main__":
    main()
