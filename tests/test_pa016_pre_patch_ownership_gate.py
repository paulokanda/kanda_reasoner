"""Tests for PA016 pre-patch ownership gate."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_symbol_atlas.pre_patch_gate import (  # noqa: E402
    PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_DUPLICATE_SYMBOL_RISK,
    PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_SAFE_TO_PATCH,
    PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_WRONG_TARGET_FILE,
    ProjectSymbolAtlasPrePatchGateOptions,
    build_reasoner_symbol_atlas_pre_patch_gate_report,
    run_reasoner_symbol_atlas_pre_patch_gate,
)


def _write_file(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _make_basic_project(root: Path) -> None:
    _write_file(root / "pkg" / "__init__.py", "")
    _write_file(
        root / "pkg" / "feature.py",
        '\n'.join([
            '"""Feature owner."""',
            "",
            "def build_feature():",
            "    return 'ok'",
            "",
        ]),
    )
    _write_file(
        root / "tests" / "test_feature.py",
        "from pkg.feature import build_feature\n\n\ndef test_feature():\n    assert build_feature() == 'ok'\n",
    )


def test_pa016_safe_to_patch_for_owned_file() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _make_basic_project(root)
        decision = run_reasoner_symbol_atlas_pre_patch_gate(
            ProjectSymbolAtlasPrePatchGateOptions(
                project_root=str(root),
                task_description="update backend feature owner",
                target_path="pkg/feature.py",
                symbol_name="build_feature",
                require_test_protection=False,
            )
        )
        assert decision.primary_edit_target.replace("\\", "/").endswith("pkg/feature.py")
        assert decision.status == PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_SAFE_TO_PATCH
        assert decision.safe_to_patch is True
        assert decision.facade_patch_risk is False
        assert decision.duplicate_symbol_risk is False


def test_pa016_blocks_facade_target() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _make_basic_project(root)
        _write_file(
            root / "feature_facade.py",
            "from pkg.feature import build_feature\n\n__all__ = ['build_feature']\n",
        )
        decision = run_reasoner_symbol_atlas_pre_patch_gate(
            ProjectSymbolAtlasPrePatchGateOptions(
                project_root=str(root),
                task_description="update feature implementation",
                target_path="feature_facade.py",
                symbol_name="build_feature",
                require_test_protection=False,
            )
        )
        assert decision.safe_to_patch is False
        assert decision.facade_patch_risk is True or decision.wrong_target_file is True
        assert decision.status in {
            PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_WRONG_TARGET_FILE,
            "facade_patch_risk",
            "needs_owner_review",
        }


def test_pa016_detects_duplicate_symbol_risk() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _make_basic_project(root)
        _write_file(
            root / "pkg" / "other.py",
            "def build_feature():\n    return 'duplicate'\n",
        )
        decision = run_reasoner_symbol_atlas_pre_patch_gate(
            ProjectSymbolAtlasPrePatchGateOptions(
                project_root=str(root),
                task_description="add feature implementation",
                target_path="pkg/feature.py",
                symbol_name="build_feature",
                require_test_protection=False,
            )
        )
        assert decision.safe_to_patch is False
        assert decision.duplicate_symbol_risk is True
        assert decision.status == PROJECT_SYMBOL_ATLAS_PRE_PATCH_STATUS_DUPLICATE_SYMBOL_RISK


def test_pa016_builds_report() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _make_basic_project(root)
        report = build_reasoner_symbol_atlas_pre_patch_gate_report(
            ProjectSymbolAtlasPrePatchGateOptions(
                project_root=str(root),
                task_description="update backend feature owner",
                target_path="pkg/feature.py",
                symbol_name="build_feature",
                require_test_protection=False,
            )
        )
        assert report.symbols
        assert "Pre-patch ownership gate" in report.summary
        assert "pre_patch_gate" in report.input_sources


def main() -> int:
    test_pa016_safe_to_patch_for_owned_file()
    test_pa016_blocks_facade_target()
    test_pa016_detects_duplicate_symbol_risk()
    test_pa016_builds_report()
    print("PA016 Pre-patch ownership gate tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
