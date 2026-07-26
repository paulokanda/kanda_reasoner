# project-path: tools/validate_aqr_sonar_real_widget_visibility_fixture_v1.py
"""Validate that the AQR sonar real-widget fixture shows its host first."""

from __future__ import annotations

import ast
from pathlib import Path

FEATURE_ID = "aqr-sonar-real-widget-visibility-fixture-v1"
TARGET = Path(
    "tools/validate_workbench_correction_route_reuse_and_aqr_sonar_real_widget_v1.py"
)


def require(condition: bool, marker: str) -> None:
    if not condition:
        raise AssertionError(marker)
    print(marker + ": PASS")


def call_line(tree: ast.AST, dotted_name: str) -> int | None:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        names: list[str] = []
        while isinstance(func, ast.Attribute):
            names.append(func.attr)
            func = func.value
        if isinstance(func, ast.Name):
            names.append(func.id)
        full = ".".join(reversed(names))
        if full == dotted_name:
            return int(getattr(node, "lineno", 0))
    return None


def main() -> int:
    source = TARGET.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(TARGET))

    host_show = call_line(tree, "window.show")
    sonar_start = call_line(tree, "start_aqr_sonar")
    require(host_show is not None, "AQR_SONAR_REAL_WIDGET_FIXTURE_SHOWS_HOST")
    require(sonar_start is not None, "AQR_SONAR_REAL_WIDGET_FIXTURE_STARTS_SONAR")
    require(
        int(host_show) < int(sonar_start),
        "AQR_SONAR_HOST_VISIBLE_BEFORE_SONAR_ASSERTION",
    )
    require(
        "REAL_WIDGET_HOST_VISIBLE_BEFORE_SONAR_ASSERTION" in source,
        "AQR_SONAR_HOST_VISIBILITY_PRECONDITION_ASSERTED",
    )
    require(
        "AQR_SONAR_VISIBLE_TO_REAL_WIDGET_HOST" in source
        and ".isVisibleTo(window)" in source,
        "AQR_SONAR_VISIBILITY_ASSERTED_AGAINST_REAL_HOST",
    )
    require(
        "window.close()" in source,
        "AQR_SONAR_REAL_WIDGET_FIXTURE_CLOSES_HOST",
    )

    print("AQR_SONAR_REAL_WIDGET_VISIBILITY_FIXTURE: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
