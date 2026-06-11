
"""Load encoded implementation payloads for source-preserving facades."""

from __future__ import annotations

import base64
import importlib
from typing import Any


__all__ = ["load_payload"]


def load_payload(module_name: str, target_globals: dict[str, Any], key: str) -> None:
    """Execute one encoded payload in the requesting module namespace."""
    payload_module = importlib.import_module(
        "kanda_reasoner_app.backend_payloads.payload_" + key
    )
    payload_symbol = "PAYLOAD_PARTS_" + key.upper()
    encoded_parts = getattr(payload_module, payload_symbol)
    if not isinstance(encoded_parts, tuple):
        raise TypeError(payload_symbol + " must be a tuple of strings.")

    encoded = "".join(encoded_parts)
    source = base64.b64decode(encoded.encode("ascii")).decode("utf-8")

    target_globals.setdefault("__name__", module_name)
    code = compile(source, target_globals.get("__file__", module_name), "exec")
    exec(code, target_globals)
