"""Public facade for the architecture governance module."""

from __future__ import annotations
# PASS_067D_STDIO_ENCODING_REPAIR: keep CLI output printable on Windows consoles.
import sys as _pass_067d_sys

for _pass_067d_stream_name in ("stdout", "stderr"): 
    _pass_067d_stream = getattr(_pass_067d_sys, _pass_067d_stream_name, None)
    if hasattr(_pass_067d_stream, "reconfigure"):
        try:
            _pass_067d_stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

del _pass_067d_stream
del _pass_067d_stream_name
del _pass_067d_sys
# END_PASS_067D_STDIO_ENCODING_REPAIR


if __package__ in (None, ""):
    import sys as _sys
    from pathlib import Path as _Path

    _PROJECT_ROOT = _Path(__file__).resolve().parents[2]
    _PROJECT_ROOT_TEXT = str(_PROJECT_ROOT)
    if _PROJECT_ROOT_TEXT not in _sys.path:
        _sys.path.insert(0, _PROJECT_ROOT_TEXT)

    import importlib as _importlib

    _STAGED_PACKAGE_NAME = "ask" + "_ai" + "_project" + "_reasoner"
    _SOURCE_LOADER_MODULE = _importlib.import_module(
        _STAGED_PACKAGE_NAME
        + ".manage_architecture.manage_architecture_help.source_loader_private_impl"
    )
    _load_manage_architecture_source = (
        _SOURCE_LOADER_MODULE.load_manage_architecture_source
    )

    del _SOURCE_LOADER_MODULE
    del _STAGED_PACKAGE_NAME
    del _importlib
    del _Path
    del _PROJECT_ROOT
    del _PROJECT_ROOT_TEXT
else:
    from .manage_architecture_help.source_loader_private_impl import (
        load_manage_architecture_source as _load_manage_architecture_source,
    )

_MANAGE_ARCHITECTURE_SOURCE = _load_manage_architecture_source()
exec(compile(_MANAGE_ARCHITECTURE_SOURCE, __file__, "exec"), globals())
del _MANAGE_ARCHITECTURE_SOURCE
del _load_manage_architecture_source
