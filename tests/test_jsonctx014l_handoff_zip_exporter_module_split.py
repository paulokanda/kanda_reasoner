"""JSONCTX014L regression tests for multi-profile exporter module split."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_context_bundle import handoff_zip_exporter
from kanda_reasoner_app.reasoner_context_bundle import handoff_zip_exporter_support
from kanda_reasoner_app.reasoner_context_bundle import handoff_zip_exporter_writer


def test_exporter_modules_remain_below_architecture_split_threshold() -> None:
    modules = [
        handoff_zip_exporter,
        handoff_zip_exporter_support,
        handoff_zip_exporter_writer,
    ]

    for module in modules:
        path = Path(module.__file__)
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        assert line_count < 500, (str(path), line_count)


def test_public_exporter_surface_remains_available() -> None:
    assert handoff_zip_exporter.DEFAULT_PART_SIZE_MB == 40
    assert handoff_zip_exporter.CONSERVATIVE_PART_SIZE_MB == 25
    assert callable(handoff_zip_exporter.export_json_handoff_zip_parts)
    assert callable(handoff_zip_exporter.is_destination_inside_project_root)
    assert callable(handoff_zip_exporter.main)


def test_helper_modules_declare_explicit_public_surfaces() -> None:
    assert "DEFAULT_PART_SIZE_MB" not in handoff_zip_exporter_support.__all__
    assert "CONSERVATIVE_PART_SIZE_MB" not in handoff_zip_exporter_support.__all__
    assert "is_destination_inside_project_root" not in handoff_zip_exporter_support.__all__
    assert "ordered_export_paths" in handoff_zip_exporter_support.__all__
    assert "package_specs" in handoff_zip_exporter_support.__all__
    assert "write_package_parts" in handoff_zip_exporter_writer.__all__
    assert "write_external_readme" in handoff_zip_exporter_writer.__all__


if __name__ == "__main__":
    test_exporter_modules_remain_below_architecture_split_threshold()
    test_public_exporter_surface_remains_available()
    test_helper_modules_declare_explicit_public_surfaces()
    print("JSONCTX014L handoff ZIP exporter module split tests passed.")
