"""Run focused validation for Planner two-column optional-AI review."""
from __future__ import annotations

import argparse
import runpy
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    test_path = root / "validation/test_large_file_refactor_planner_two_column_ai_optional_review_v1.py"
    namespace = runpy.run_path(str(test_path))
    namespace["validate"](root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
