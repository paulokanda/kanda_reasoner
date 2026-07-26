"""Validate transient fixture ownership and bounded real-widget observability."""
from __future__ import annotations

import ast
from pathlib import Path

__all__ = [
    "main",
]

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
SUPPORT = TOOLS / "patch6_controlled_real_module_support.py"
WIDGET = TOOLS / "validate_large_file_refactor_workbench_real_widget_attemptability_v1.py"
FEATURE_ID = "architecture-review-workbench-real-widget-observability-transient-fixture-v1"


def _load(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="strict")


def _require(condition: bool, marker: str) -> None:
    if not condition:
        raise AssertionError(marker)
    print(marker + ": PASS")


def main() -> None:
    support = _load(SUPPORT)
    widget = _load(WIDGET)
    ast.parse(support)
    ast.parse(widget)

    _require(
        'controlled = work_root / "patch6_controlled_real"' in support
        and 'shadow = work_root / "patch6_controlled_shadow"' in support,
        "CONTROLLED_VALIDATION_FIXTURES_UNDER_TRANSIENT_GARBAGE_ROOT",
    )
    _require(
        'anchor_root / f"{live_root.name}_patch6_controlled_real"' not in support
        and 'anchor_root / f"{live_root.name}_patch6_controlled_shadow"' not in support,
        "NO_DRIVE_ROOT_SIBLING_CONTROLLED_FIXTURES",
    )
    _require(
        '".git"' in support and '".hg"' in support and '".svn"' in support,
        "CONTROLLED_COPY_EXCLUDES_VCS_GARBAGE",
    )
    _require(
        'REAL_WIDGET_STAGE_START: prepare_controlled_project' in widget
        and 'REAL_WIDGET_STAGE_START: completion_evidence_click' in widget
        and 'REAL_WIDGET_STAGE_START: transaction_summary_click' in widget,
        "REAL_WIDGET_STAGE_PROGRESS_MARKERS_PRESENT",
    )
    _require(
        '_VALIDATOR_TIMEOUT_SECONDS = 600' in widget
        and 'REAL_WIDGET_VALIDATOR_TIMEOUT:' in widget
        and 'os._exit(124)' in widget,
        "REAL_WIDGET_VALIDATOR_WATCHDOG_PRESENT",
    )
    _require(
        all(len(_load(path).splitlines()) <= 500 for path in (SUPPORT, WIDGET)),
        "TOUCHED_SOURCE_MODULES_MAX_500_LINES",
    )
    print("REAL_WIDGET_OBSERVABILITY_TRANSIENT_FIXTURE: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
