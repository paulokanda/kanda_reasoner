# project-path: tools/validate_architecture_review_large_file_refactor_planner_llm_arbitration_contracts_v1.py
"""Tool wrapper for Large File Refactor Planner LLM arbitration validation."""
from __future__ import annotations

import runpy
from pathlib import Path


def main() -> int:
    """Run the focused LLM arbitration validator."""
    project_root = Path(__file__).resolve().parents[1]
    script = project_root / "validation" / "test_architecture_review_large_file_refactor_planner_llm_arbitration_contracts_v1.py"
    runpy.run_path(str(script), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
