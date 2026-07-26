# project-path: tools/validate_project_aa_boxed_dynamic_local_ai_run_analysis_v4.py
"""Tool wrapper for boxed Project A&A dynamic local-AI validation repair."""

from __future__ import annotations

import runpy
from pathlib import Path

__all__: list[str] = []


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    script = project_root / "validation/test_project_aa_boxed_dynamic_local_ai_run_analysis_v4.py"
    runpy.run_path(str(script), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
