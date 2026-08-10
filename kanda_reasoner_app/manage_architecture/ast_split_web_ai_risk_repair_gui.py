# project-path: kanda_reasoner_app/manage_architecture/ast_split_web_ai_risk_repair_gui.py
"""Compatibility shim for the renamed AST Split Web AI GUI module.

New active code must import ast_split_web_ai_gui. This module keeps
legacy direct imports working without claiming public symbol ownership.
"""

from __future__ import annotations


__all__: list[str] = []
