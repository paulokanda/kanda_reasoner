"""Private extraction helpers for collector_responsibility_overlap."""

from __future__ import annotations
# PASS_068A_OVERLAP_CONSTANT_BINDINGS_START
# Runtime bindings restored after helper extraction.
globals().update({
    'GENERIC_TOKENS': set(['ui', 'widget', 'button', 'dialog', 'window', 'tab', 'panel', 'bar', 'menu', 'layout', 'tool', 'tools', 'template', 'templates', 'base', 'common', 'utils', 'util', 'helper', 'helpers', 'core', 'main', 'app', 'manager', 'controller', 'service', 'data', 'file', 'files', 'module', 'modules', 'test', 'tests', 'view', 'builder', 'handler']),
    'GENERIC_CALL_ROOTS': set(['connect', 'emit', 'show', 'hide', 'update', 'refresh', 'clear', 'reset', 'close', 'open', 'load', 'save', 'append', 'remove', 'settext', 'setvalue', 'setenabled', 'setvisible', 'addwidget', 'addlayout', 'addtab', 'setlayout', 'setcentralwidget', 'resize', 'move', 'exec', 'exec_', 'start', 'stop', 'plot', 'render', 'draw']),
    'GENERIC_ROLE_TOKENS': set(['ui', 'service', 'controller', 'domain', 'general', 'visualization']),
    'MIN_OVERLAP_SCORE': 1.55,
    'MIN_HOTSPOT_SCORE': 1.95,
})
# PASS_068A_OVERLAP_CONSTANT_BINDINGS_END

from typing import Any

__all__: list[str] = []

def _symbol_name_set(file_record: dict[str, Any]) -> set[str]:
    out: set[str] = set()

    for fn in file_record.get("functions", []):
        if isinstance(fn, dict):
            name = str(fn.get("name", "")).strip().lower()
            if name and name not in GENERIC_TOKENS and len(name) >= 4:
                out.add(name)

    for cls in file_record.get("classes", []):
        if not isinstance(cls, dict):
            continue

        cls_name = str(cls.get("name", "")).strip().lower()
        if cls_name and cls_name not in GENERIC_TOKENS and len(cls_name) >= 4:
            out.add(cls_name)

        for method in cls.get("methods", []):
            if isinstance(method, dict):
                name = str(method.get("name", "")).strip().lower()
                if name and name not in GENERIC_TOKENS and len(name) >= 4:
                    out.add(name)

    return out

def _call_name_roots(file_record: dict[str, Any]) -> set[str]:
    out: set[str] = set()

    def add_call_name(call_name: str) -> None:
        text = str(call_name).strip().lower()
        if not text:
            return
        root = text.split(".")[-1]
        if (
            root
            and root not in GENERIC_CALL_ROOTS
            and root not in GENERIC_TOKENS
            and len(root) >= 5
        ):
            out.add(root)

    for fn in file_record.get("functions", []):
        if not isinstance(fn, dict):
            continue
        for call in fn.get("calls", []):
            if isinstance(call, dict):
                add_call_name(call.get("call_name", ""))

    for cls in file_record.get("classes", []):
        if not isinstance(cls, dict):
            continue
        for method in cls.get("methods", []):
            if not isinstance(method, dict):
                continue
            for call in method.get("calls", []):
                if isinstance(call, dict):
                    add_call_name(call.get("call_name", ""))

    return out

def _file_record_map(files_payload: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for record in files_payload:
        path = str(record.get("path", "")).strip()
        if path:
            out[path] = record
    return out
