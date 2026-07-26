"""Static characterization tests for local-freeze dialog support extraction."""
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.freeze_after_update_gui._local_freeze_dialog_widgets import (
    FreezeLocalFreezeDialogSupportMixin,
    LocalFreezeDialogWidgets,
    build_local_freeze_dialog_widgets,
)
from kanda_reasoner_app.freeze_after_update_gui.freeze_after_update_tab import (
    FreezeAfterUpdateTab,
)


def _source() -> str:
    return Path(sys.modules[FreezeLocalFreezeDialogSupportMixin.__module__].__file__).read_text(encoding="utf-8")


def test_local_dialog_support_stays_below_facade_and_import_compatible() -> None:
    source = _source()

    assert issubclass(FreezeAfterUpdateTab, FreezeLocalFreezeDialogSupportMixin)
    assert hasattr(FreezeAfterUpdateTab, "_raise_existing_local_freeze_dialog")
    assert hasattr(FreezeAfterUpdateTab, "_clear_local_freeze_dialog_reference")
    assert hasattr(FreezeAfterUpdateTab, "_build_heuristic_local_freeze_inputs")
    assert LocalFreezeDialogWidgets.__name__ in source
    assert build_local_freeze_dialog_widgets.__name__ in source
    assert "freeze_after_update_tab" not in source


def test_local_dialog_widget_builder_preserves_labels_and_buttons() -> None:
    source = _source()

    for snippet in (
        'QDialog(parent)',
        '"New Local Freeze Entry"',
        '"Local AI"',
        '"Heuristics (default)"',
        '"Refresh AI Models"',
        '"Freeze entry fields"',
        '"Preview and validation"',
        '"Fill Form Now"',
        '"Copy Formulary to AI"',
        '"Receive Formulary from AI"',
        '"Preview Freeze Entry"',
        '"Confirm and Write Freeze Entry"',
        '"Ignore this Freeze"',
    ):
        assert snippet in source


def test_local_dialog_support_preserves_safe_fallback_contract_text() -> None:
    source = _source()

    assert "Current validated feature - replace with exact feature title" in source
    assert "Do not freeze without current feature validation evidence." in source
    assert "project_freeze_after_update/frozen_features_memory/" in source
    assert "Do not store project-specific frozen memory inside project_freeze_ledger." in source
    assert "Freeze hint intake was unavailable, so the safe starter draft was kept." in source


def main() -> int:
    test_local_dialog_support_stays_below_facade_and_import_compatible()
    test_local_dialog_widget_builder_preserves_labels_and_buttons()
    test_local_dialog_support_preserves_safe_fallback_contract_text()
    print("VALIDATION OK: freeze-after-update-local-dialog-widgets-refactor")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
