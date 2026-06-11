"""Direct tests for handoff_zip_exporter_support public contract."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_context_bundle.handoff_zip_exporter_support import (  # noqa: E402
    __all__ as SUPPORT_ALL,
    context_from_project,
    ordered_export_paths,
    package_specs,
    timestamp_value,
)


def test_support_contract_exports_only_helper_surface() -> None:
    public_names = set(SUPPORT_ALL)
    assert "context_from_project" in public_names
    assert "ordered_export_paths" in public_names
    assert "package_specs" in public_names
    assert "timestamp_value" in public_names
    assert "DEFAULT_PART_SIZE_MB" not in public_names
    assert "CONSERVATIVE_PART_SIZE_MB" not in public_names
    assert "is_destination_inside_project_root" not in public_names


def test_support_imports_are_callable() -> None:
    assert callable(context_from_project)
    assert callable(ordered_export_paths)
    assert callable(package_specs)
    assert timestamp_value("20260102_030405") == "20260102_030405"


if __name__ == "__main__":
    test_support_contract_exports_only_helper_surface()
    test_support_imports_are_callable()
    print("handoff_zip_exporter_support direct tests passed.")
