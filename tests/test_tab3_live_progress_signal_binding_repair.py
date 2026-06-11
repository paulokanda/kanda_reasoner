"""Regression test for Tab 3 live progress signal binding."""

from __future__ import annotations

import base64

from kanda_reasoner_app.backend_payloads.payload_s import PAYLOAD_PARTS_S


def test_tab3_progress_signal_uses_queued_receiver_binding() -> None:
    """Ensure progress is routed through the safe queued receiver path."""
    source = base64.b64decode("".join(PAYLOAD_PARTS_S)).decode("utf-8")

    assert "progress_ready.connect(self._handle_worker_progress)" not in source
    assert "progress_ready.connect(lambda payload: handle_worker_progress(self, payload))" not in source
    assert "_create_progress_receiver" in source
    assert "_connect_progress_signal" in source
    assert "_tab3_progress_receiver" in source
    assert "ConnectionType.QueuedConnection" in source
    assert "def handle_worker_progress(self, payload" in source


if __name__ == "__main__":
    test_tab3_progress_signal_uses_queued_receiver_binding()
    print("Tab 3 live progress signal binding repair tests passed.")
