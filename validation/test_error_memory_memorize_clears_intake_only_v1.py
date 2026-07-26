"""Validate Error Memory Memorize Error clears intake only.

This validation avoids importing PySide6. It statically checks the GUI source
for the required state transition:
- successful Memorize Error calls a helper that clears raw_error_edit only;
- the helper does not clear received_preview_edit;
- matching pending intake files are consumed only after a lesson id match;
- selection/import/manual paste clear pending tracking so unrelated pending files
  are not consumed by mistake.
"""

from __future__ import annotations

import ast
from pathlib import Path


FEATURE_ID = "error-memory-memorize-clears-intake-only-v1"
EXPECTED_MARKER = "VALIDATION OK: " + FEATURE_ID
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "kanda_reasoner_app" / "error_memory_gui" / "error_memory_tab.py"


class FunctionFinder(ast.NodeVisitor):
    """Collect class methods by name."""

    def __init__(self) -> None:
        self.functions: dict[str, ast.FunctionDef] = {}

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: N802
        self.functions[node.name] = node
        self.generic_visit(node)


def calls_attr(node: ast.AST, attr_name: str) -> bool:
    """Return True when the AST calls an attribute with the given name."""
    for child in ast.walk(node):
        if isinstance(child, ast.Call) and isinstance(child.func, ast.Attribute):
            if child.func.attr == attr_name:
                return True
    return False


def attr_call_on(node: ast.AST, object_attr: str, method_name: str) -> bool:
    """Return True when self.<object_attr>.<method_name>() is called."""
    for child in ast.walk(node):
        if not isinstance(child, ast.Call):
            continue
        func = child.func
        if not isinstance(func, ast.Attribute) or func.attr != method_name:
            continue
        value = func.value
        if not isinstance(value, ast.Attribute) or value.attr != object_attr:
            continue
        owner = value.value
        if isinstance(owner, ast.Name) and owner.id == "self":
            return True
    return False


def source_segment(node: ast.AST) -> str:
    """Return source segment for a node."""
    text = ast.get_source_segment(SOURCE_TEXT, node)
    return text or ""


SOURCE_TEXT = SOURCE.read_text(encoding="utf-8")
tree = ast.parse(SOURCE_TEXT)
finder = FunctionFinder()
finder.visit(tree)
functions = finder.functions

required = [
    "_memorize_error_from_text_window",
    "_clear_ai_assisted_intake_after_memorize",
    "_consume_loaded_pending_intake_file_if_matches",
    "_load_pending_ai_assisted_error_lesson_intake",
]
missing = [name for name in required if name not in functions]
if missing:
    raise AssertionError("Missing required methods: " + ", ".join(missing))

memorize = functions["_memorize_error_from_text_window"]
clear_helper = functions["_clear_ai_assisted_intake_after_memorize"]
consume_helper = functions["_consume_loaded_pending_intake_file_if_matches"]
load_pending = functions["_load_pending_ai_assisted_error_lesson_intake"]

if not calls_attr(memorize, "_clear_ai_assisted_intake_after_memorize"):
    raise AssertionError("Memorize Error must call the intake-only clear helper after save")

memorize_text = source_segment(memorize)
if "path is not None" not in memorize_text:
    raise AssertionError("Memorize Error must clear intake only after save returns a path")

if not attr_call_on(clear_helper, "raw_error_edit", "clear"):
    raise AssertionError("The intake-only clear helper must clear raw_error_edit")

if attr_call_on(clear_helper, "received_preview_edit", "clear"):
    raise AssertionError("The intake-only clear helper must not clear Error Editor")

if attr_call_on(memorize, "received_preview_edit", "clear"):
    raise AssertionError("Memorize Error must not clear Error Editor on success")

consume_text = source_segment(consume_helper)
for expected in [
    "loaded_lesson_id != saved_lesson_id",
    "pending_path.unlink()",
    "self._loaded_pending_intake_file = \"\"",
    "self._loaded_pending_intake_lesson_id = \"\"",
]:
    if expected not in consume_text:
        raise AssertionError("Pending intake consume guard missing: " + expected)

load_text = source_segment(load_pending)
if "self._loaded_pending_intake_lesson_id = lesson_id" not in load_text:
    raise AssertionError("Pending intake loader must remember the loaded lesson id")

if "self._loaded_pending_intake_lesson_id = \"\"" not in SOURCE_TEXT:
    raise AssertionError("Non-pending lesson actions must be able to reset pending tracking")

print(EXPECTED_MARKER)
