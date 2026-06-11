from __future__ import annotations

import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.source_hygiene.shadow_fixer import (  # noqa: E402
    FacadeFixResult,
    apply_safe_package_marker_fix,
    build_safe_facade_fix_plan,
    iter_empty_init_files,
    plan_safe_package_marker_fix,
)


def test_empty_init_is_planned_and_fixed(tmp_path: Path) -> None:
    tmp_path.mkdir(parents=True, exist_ok=True)
    package_dir = tmp_path / "pkg"
    package_dir.mkdir()
    init_path = package_dir / "__init__.py"
    init_path.write_text("", encoding="utf-8")

    candidates = iter_empty_init_files(tmp_path)
    assert candidates == (init_path.resolve(),)

    finding = plan_safe_package_marker_fix(init_path, tmp_path)
    assert finding is not None
    assert finding.code == "EMPTY_INIT_PACKAGE_MARKER_FIX_AVAILABLE"

    report = build_safe_facade_fix_plan(tmp_path)
    assert report.report_type == "facade_fix_plan"
    assert len(report.findings) == 1

    dry_result = apply_safe_package_marker_fix(init_path, tmp_path, dry_run=True)
    assert isinstance(dry_result, FacadeFixResult)
    assert not dry_result.changed
    assert init_path.read_text(encoding="utf-8") == ""

    result = apply_safe_package_marker_fix(init_path, tmp_path, dry_run=False)
    assert result.changed
    assert not result.error
    assert Path(result.backup_path).exists()
    text = init_path.read_text(encoding="utf-8")
    assert '"""Package marker for pkg."""' in text
    assert "__all__ = []" in text


def test_non_empty_init_is_not_modified(tmp_path: Path) -> None:
    tmp_path.mkdir(parents=True, exist_ok=True)
    package_dir = tmp_path / "pkg"
    package_dir.mkdir()
    init_path = package_dir / "__init__.py"
    original = "from .module import value\n\n__all__ = ['value']\n"
    init_path.write_text(original, encoding="utf-8")

    assert iter_empty_init_files(tmp_path) == ()
    assert plan_safe_package_marker_fix(init_path, tmp_path) is None

    result = apply_safe_package_marker_fix(init_path, tmp_path, dry_run=False)
    assert not result.changed
    assert result.error
    assert init_path.read_text(encoding="utf-8") == original


def test_outside_project_root_is_refused(tmp_path: Path) -> None:
    tmp_path.mkdir(parents=True, exist_ok=True)
    root = tmp_path / "root"
    outside = tmp_path / "outside" / "__init__.py"
    root.mkdir()
    outside.parent.mkdir()
    outside.write_text("", encoding="utf-8")

    result = apply_safe_package_marker_fix(outside, root, dry_run=False)
    assert not result.changed
    assert "outside the project root" in result.error


if __name__ == "__main__":
    for name in ("_tmp_sh006_a", "_tmp_sh006_b", "_tmp_sh006_c"):
        shutil.rmtree(name, ignore_errors=True)
    test_empty_init_is_planned_and_fixed(Path("_tmp_sh006_a"))
    test_non_empty_init_is_not_modified(Path("_tmp_sh006_b"))
    test_outside_project_root_is_refused(Path("_tmp_sh006_c"))
    print("SH006 safe mechanical facade fix tests passed.")
