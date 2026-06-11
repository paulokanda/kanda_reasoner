"""Contract tests for Tab 3 Local AI startup safety."""

from __future__ import annotations

import base64

from kanda_reasoner_app.backend_payloads.payload_t import PAYLOAD_PARTS_T


def _decoded_payload_t() -> str:
    """Return the decoded Tab 3 window-state payload."""
    return base64.b64decode("".join(PAYLOAD_PARTS_T)).decode("utf-8")


def test_local_ai_checkbox_starts_off_without_using_saved_enabled_state() -> None:
    """Tab 3 Local AI must start off even if prior prefs saved it on."""
    source = _decoded_payload_t()

    assert 'self._ai_enabled_checkbox = QCheckBox("Enable local AI")' in source
    assert "self._ai_enabled_checkbox.setChecked(False)" in source
    assert 'safe_bool(self._prefs.get("ai_enabled"), False)' not in source
    assert "Local AI starts off for safety" in source


def test_local_ai_enabled_state_is_not_persisted_as_true() -> None:
    """Tab 3 should not reopen with Local AI enabled from persisted prefs."""
    source = _decoded_payload_t()

    assert '"ai_enabled": False,' in source
    assert '"ai_enabled": self._ai_enabled_checkbox.isChecked(),' not in source


if __name__ == "__main__":
    test_local_ai_checkbox_starts_off_without_using_saved_enabled_state()
    test_local_ai_enabled_state_is_not_persisted_as_true()
    print("Tab 3 start Local AI off contract tests passed.")
