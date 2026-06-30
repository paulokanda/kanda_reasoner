# project-path: kanda_reasoner_app/json_splitter/json_splitter_8_help/source_loader_private_impl.py
"""Loader for the source-preserving json_splitter_8 facade."""

from __future__ import annotations

import base64
from typing import Any, MutableMapping

from .source_part_1_private_impl import SOURCE_PART_1 as _SOURCE_PART_1
from .source_part_2_private_impl import SOURCE_PART_2 as _SOURCE_PART_2

__all__ = ["load_json_splitter_8_source"]


def _decode_source() -> str:
    """Support decode source behavior.
    
    Returns
    -------
    str
        The string result.
    """
    
    payload = "".join([_SOURCE_PART_1, _SOURCE_PART_2])
    return base64.b64decode(payload.encode("ascii")).decode("utf-8")


def load_json_splitter_8_source(target_globals: MutableMapping[str, Any]) -> None:
    """Load the json splitter 8 source.
    
    Parameters
    ----------
    target_globals : MutableMapping[str, Any]
        The target globals value.
    """
    
    source = _decode_source()
    filename = str(target_globals.get("__file__", "json_splitter_8.py"))
    code = compile(source, filename, "exec")
    exec(code, target_globals)
    try:
        from kanda_reasoner_app.project_json_scope_filter import (
            install_json_splitter_project_exclusion_filter as _pa024_install_filter,
        )
        _pa024_install_filter(target_globals)  # PA024_PROJECT_EXCLUSION_RULES_SOURCE_INSTALL
    except Exception as exc:
        raise RuntimeError("Project exclusion filter install failed.") from exc
