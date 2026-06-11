"""Regression test for Tab 3 hidden guided-folder import dependency."""

from __future__ import annotations

import importlib


def test_guided_folder_mode_actual_tab3_wiring_contract_imports() -> None:
    module = importlib.import_module(
        "kanda_reasoner_app.insert_missing_docstrings_gui."
        "guided_folder_mode.actual_tab3_wiring"
    )
    assert callable(module.install_safe_mode_actual_tab3_wiring)
    assert callable(module.move_safe_mode_radio_to_layout)


def test_guided_folder_mode_install_is_non_destructive() -> None:
    module = importlib.import_module(
        "kanda_reasoner_app.insert_missing_docstrings_gui."
        "guided_folder_mode.actual_tab3_wiring"
    )
    result = module.install_safe_mode_actual_tab3_wiring(object())
    assert result["installed"] is True
    assert result["move_method_available"] is False


def main() -> int:
    """Run Tab 3 hidden dependency regression tests without pytest."""
    test_guided_folder_mode_actual_tab3_wiring_contract_imports()
    test_guided_folder_mode_install_is_non_destructive()
    print("Tab 3 hidden dependency regression tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
