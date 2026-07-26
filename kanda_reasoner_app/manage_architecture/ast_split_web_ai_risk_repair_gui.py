# project-path: kanda_reasoner_app/manage_architecture/ast_split_web_ai_risk_repair_gui.py
"""Compatibility shim for the renamed AST Split Web AI GUI module.

New active code must import ast_split_web_ai_gui. This module keeps
legacy direct imports working without claiming public symbol ownership.
"""

from __future__ import annotations

from .ast_split_web_ai_gui import (
    add_ast_split_web_ai_risk_repair_button,
    bind_ast_split_web_ai_single_output,
    build_ast_split_web_ai_risk_repair_wrapper,
    build_safe_refactor_how_to_bundle,
    copy_ast_split_web_ai_risk_repair_wrapper,
    copy_safe_refactor_how_to_bundle,
)

__all__: list[str] = []
