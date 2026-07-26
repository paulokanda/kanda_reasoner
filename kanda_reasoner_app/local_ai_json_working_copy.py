"""Compatibility shim for the canonical Local-AI JSON contract module.

The implementation moved to local_ai_json_contract because this filename is
classified as stale/reference-looking by architecture validation.  Keep this
module as a thin import-compatible facade for older tests or external scripts.
New active code must import kanda_reasoner_app.local_ai_json_contract.
"""

from __future__ import annotations

from kanda_reasoner_app.local_ai_json_contract import (
    LocalAIJsonCopyPaths,
    LocalAIJsonCopyResult,
    build_default_paths,
    ensure_local_ai_copy,
    refresh_local_ai_copy,
)
