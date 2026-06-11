"""Compatibility facade for deterministic heuristic docstring builders."""

from __future__ import annotations

from kanda_reasoner_app.backend_payloads.loader import load_payload

load_payload(__name__, globals(), "i")

_payload_function_summary = function_summary
_payload_class_summary = class_summary
_payload_module_summary = module_summary
_payload_build_module_docstring = build_module_docstring
_payload_build_class_docstring = build_class_docstring
_payload_iter_function_parameters = iter_function_parameters
_payload_build_function_docstring = build_function_docstring


def function_summary(*args, **kwargs):
    """Return a conservative one-line summary for a function name."""
    return _payload_function_summary(*args, **kwargs)


def class_summary(*args, **kwargs):
    """Return a conservative one-line summary for a class name."""
    return _payload_class_summary(*args, **kwargs)


def module_summary(*args, **kwargs):
    """Return a conservative one-line summary for a module path."""
    return _payload_module_summary(*args, **kwargs)


def build_module_docstring(*args, **kwargs):
    """Return a neutral heuristic module docstring."""
    return _payload_build_module_docstring(*args, **kwargs)


def build_class_docstring(*args, **kwargs):
    """Return a neutral heuristic class docstring."""
    return _payload_build_class_docstring(*args, **kwargs)


def iter_function_parameters(*args, **kwargs):
    """Yield function parameter metadata in deterministic order."""
    return _payload_iter_function_parameters(*args, **kwargs)


def build_function_docstring(*args, **kwargs):
    """Return a neutral heuristic function docstring."""
    return _payload_build_function_docstring(*args, **kwargs)


__all__ = [
    "function_summary",
    "class_summary",
    "module_summary",
    "build_module_docstring",
    "build_class_docstring",
    "iter_function_parameters",
    "build_function_docstring",
]
