"""Regression tests for safe Tab 3 live-progress signal routing."""

from __future__ import annotations

import base64
import importlib


def _decoded_payload_s() -> str:
    payload = importlib.import_module(
        "kanda_reasoner_app.backend_payloads.payload_s"
    )
    encoded = "".join(payload.PAYLOAD_PARTS_S)
    return base64.b64decode(encoded).decode("utf-8")


def test_progress_signal_uses_qobject_receiver_not_lambda() -> None:
    """Progress must not update widgets through a raw Python lambda."""
    source = _decoded_payload_s()
    assert "progress_ready.connect(lambda" not in source
    assert "_create_progress_receiver" in source
    assert "_connect_progress_signal" in source
    assert "_tab3_progress_receiver" in source
    assert "ConnectionType.QueuedConnection" in source


def test_progress_receiver_is_cleaned_up_with_worker_lifecycle() -> None:
    """Receiver lifetime must be tied to the worker lifecycle."""
    source = _decoded_payload_s()
    assert "progress_receiver = getattr(self, \"_tab3_progress_receiver\", None)" in source
    assert "progress_receiver.deleteLater()" in source
    assert "self._tab3_progress_receiver = None" in source


if __name__ == "__main__":
    test_progress_signal_uses_qobject_receiver_not_lambda()
    test_progress_receiver_is_cleaned_up_with_worker_lifecycle()
    print("Tab 3 live progress queued receiver repair tests passed.")
