# project-path: kanda_reasoner_app/patch_governance/__init__.py
"""Patch delivery governance helpers for KANDA Reasoner.

This package contains deterministic release gates for installable patch ZIPs.
The goal is to make patch delivery safety machine-checkable instead of relying
only on chat-time memory of prompt instructions.
"""

from __future__ import annotations

from .models import (
    FREEZE_HINT_FILENAME,
    FreezePayloadError,
    build_freeze_payload,
    dump_freeze_payload_json,
    freeze_form_json_text,
    mandatory_freeze_fields,
)
from .validator import (
    PatchZipContractError,
    validate_install_script_text,
    validate_patch_zip,
)

__all__ = [
    "FREEZE_HINT_FILENAME",
    "FreezePayloadError",
    "PatchZipContractError",
    "build_freeze_payload",
    "dump_freeze_payload_json",
    "freeze_form_json_text",
    "mandatory_freeze_fields",
    "validate_install_script_text",
    "validate_patch_zip",
]
