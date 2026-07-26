# project-path: kanda_reasoner_app/manage_architecture/_large_module_split_audit_symbol_analysis.py
"""Pure symbol-level AST analysis helpers for large-module split auditing."""
from __future__ import annotations

import ast
import re
from typing import Any

__all__: list[str] = []

GUI_IMPORT_PREFIXES = ("PySide6", "PyQt", "tkinter")


GUI_NAME_HINTS = (
    "QApplication",
    "QCheckBox",
    "QComboBox",
    "QDialog",
    "QFileDialog",
    "QLabel",
    "QLineEdit",
    "QMainWindow",
    "QMessageBox",
    "QPlainTextEdit",
    "QPushButton",
    "QTableWidget",
    "QTimer",
    "QThread",
    "QVBoxLayout",
    "QHBoxLayout",
    "QWidget",
)


WIDGET_ATTR_HINTS = (
    "action",
    "btn",
    "button",
    "checkbox",
    "combo",
    "dialog",
    "edit",
    "label",
    "layout",
    "menu",
    "preview",
    "statusbar",
    "table",
    "toolbar",
    "widget",
    "window",
)


WRITE_METHODS = {"write_text", "write_bytes", "write", "dump", "dumps"}


DELETE_METHODS = {"unlink", "remove", "rmtree", "delete"}


ARCHIVE_NAMES = {"ZipFile", "zipfile", "make_archive", "unpack_archive"}


SUBPROCESS_NAMES = {"subprocess", "Popen", "run", "check_call", "check_output"}


class _SymbolVisitor(ast.NodeVisitor):
    """Represent symbol visitor."""
    
    def __init__(self, imports: dict[str, str]) -> None:
        """Support init behavior.
        
        Parameters
        ----------
        imports : dict[str, str]
            The imports value.
        """
        
        self.imports = imports
        self.called_self_methods: set[str] = set()
        self.self_attr_reads: set[str] = set()
        self.self_attr_writes: set[str] = set()
        self.imports_used: set[str] = set()
        self.gui_touches: set[str] = set()
        self.side_effects: set[str] = set()

    def visit_Name(self, node: ast.Name) -> Any:
        """Support visit name behavior.
        
        Parameters
        ----------
        node : ast.Name
            The syntax tree node.
        
        Returns
        -------
        Any
            The any result.
        """
        
        if node.id in self.imports:
            qualified = self.imports[node.id]
            self.imports_used.add(qualified)
            if qualified.startswith(GUI_IMPORT_PREFIXES) or node.id in GUI_NAME_HINTS:
                self.gui_touches.add(node.id)
        if node.id in GUI_NAME_HINTS:
            self.gui_touches.add(node.id)
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> Any:
        """Support visit attribute behavior.
        
        Parameters
        ----------
        node : ast.Attribute
            The syntax tree node.
        
        Returns
        -------
        Any
            The any result.
        """
        
        root_name = _root_name(node)
        if root_name == "self":
            attr = node.attr
            if isinstance(node.ctx, ast.Store):
                self.self_attr_writes.add(attr)
            elif isinstance(node.ctx, ast.Load):
                self.self_attr_reads.add(attr)
            if _looks_like_widget_attr(attr):
                self.gui_touches.add(f"self.{attr}")
        if node.attr == "connect":
            self.side_effects.add("signal_wiring")
        if node.attr == "clipboard":
            self.side_effects.add("clipboard")
        if node.attr in WRITE_METHODS:
            self.side_effects.add("file_write")
        if node.attr in DELETE_METHODS:
            self.side_effects.add("file_delete")
        if node.attr in {"start", "quit", "terminate"} and root_name and "thread" in root_name.lower():
            self.side_effects.add("thread_or_timer")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> Any:
        """Support visit call behavior.
        
        Parameters
        ----------
        node : ast.Call
            The syntax tree node.
        
        Returns
        -------
        Any
            The any result.
        """
        
        call_name = _call_name(node.func)
        if isinstance(node.func, ast.Attribute) and _root_name(node.func) == "self":
            self.called_self_methods.add(node.func.attr)
        lowered = call_name.lower()
        if "qmessagebox" in lowered:
            self.side_effects.add("message_box")
            self.gui_touches.add("QMessageBox")
        if "qfiledialog" in lowered:
            self.side_effects.add("file_dialog")
            self.gui_touches.add("QFileDialog")
        if "clipboard" in lowered:
            self.side_effects.add("clipboard")
        if any(name.lower() in lowered for name in ARCHIVE_NAMES):
            self.side_effects.add("archive")
        if any(name.lower() == lowered or lowered.endswith("." + name.lower()) for name in SUBPROCESS_NAMES):
            self.side_effects.add("subprocess")
        if "qthread" in lowered or "qtimer" in lowered:
            self.side_effects.add("thread_or_timer")
            self.gui_touches.add(call_name)
        if call_name == "open":
            if any(_literal_write_mode(arg) for arg in node.args[1:2]):
                self.side_effects.add("file_write")
        self.generic_visit(node)


def _root_name(node: ast.AST) -> str:
    """Support root name behavior.
    
    Parameters
    ----------
    node : ast.AST
        The syntax tree node.
    
    Returns
    -------
    str
        The string result.
    """
    
    current = node
    while isinstance(current, ast.Attribute):
        current = current.value
    if isinstance(current, ast.Call):
        return _root_name(current.func)
    if isinstance(current, ast.Name):
        return current.id
    return ""


def _call_name(node: ast.AST) -> str:
    """Support call name behavior.
    
    Parameters
    ----------
    node : ast.AST
        The syntax tree node.
    
    Returns
    -------
    str
        The string result.
    """
    
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = _call_name(node.value)
        return f"{prefix}.{node.attr}" if prefix else node.attr
    return ""


def _literal_write_mode(node: ast.AST) -> bool:
    """Support literal write mode behavior.
    
    Parameters
    ----------
    node : ast.AST
        The syntax tree node.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return any(flag in node.value for flag in ("w", "a", "+"))
    return False


def _looks_like_widget_attr(attr: str) -> bool:
    """Support looks like widget attr behavior.
    
    Parameters
    ----------
    attr : str
        The attr value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    lowered = attr.lower()
    return any(hint in lowered for hint in WIDGET_ATTR_HINTS)


def _candidate_label(name: str, side_effects: list[str], gui_touches: list[str]) -> str:
    """Support candidate label behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    side_effects : list[str]
        The side effects value.
    gui_touches : list[str]
        The gui touches value.
    
    Returns
    -------
    str
        The string result.
    """
    
    tokens = set(filter(None, re.split(r"_+", name.lower().strip("_"))))
    if tokens & {"build", "ui", "layout", "controls", "panel", "button", "buttons"}:
        return "ui_builder"
    if tokens & {"root", "project", "path", "folder", "browse", "refresh", "open"}:
        return "project_root_paths"
    if tokens & {"table", "row", "selected", "selection", "preview"}:
        return "table_selection"
    if tokens & {"receive", "import", "zip", "formatted", "formulary"}:
        return "receive_import"
    if tokens & {"pending", "intake", "load", "loader"}:
        return "pending_intake"
    if tokens & {"draft", "clean", "delete", "dismiss"} or "file_delete" in side_effects:
        return "draft_cleanup"
    if tokens & {"clipboard", "copy", "export"} or "clipboard" in side_effects:
        return "clipboard_export"
    if tokens & {"worker", "run", "mode", "audit", "validate", "scan", "write"}:
        return "audit_runner"
    if tokens & {"help", "prompt", "protocol"}:
        return "prompt_help"
    if gui_touches:
        return "gui_actions"
    return "general"


def _risk_for(side_effects: list[str], gui_touches: list[str], writes: set[str]) -> str:
    """Support risk for behavior.
    
    Parameters
    ----------
    side_effects : list[str]
        The side effects value.
    gui_touches : list[str]
        The gui touches value.
    writes : set[str]
        The writes value.
    
    Returns
    -------
    str
        The string result.
    """
    
    high = {"file_delete", "subprocess", "thread_or_timer", "signal_wiring"}
    medium = {"file_write", "archive", "clipboard", "file_dialog", "message_box"}
    if high.intersection(side_effects):
        return "high"
    if medium.intersection(side_effects) or gui_touches or len(writes) > 4:
        return "medium"
    return "low"
