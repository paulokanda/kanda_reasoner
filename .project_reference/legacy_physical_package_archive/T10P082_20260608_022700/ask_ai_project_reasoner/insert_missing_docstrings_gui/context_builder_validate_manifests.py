"""Validate context builder helper manifest artifacts."""

from __future__ import annotations
"""Validate the context_builder helper manifest contract."""

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "context_builder_help.json"
ORIGIN = ROOT / "context_builder.py"
HELP_DIR = ROOT / "context_builder_help"
HELP_INIT = HELP_DIR / "__init__.py"
HELP_IMPL = HELP_DIR / "inference_private_impl.py"

REQUIRED_HEADER_FIELDS = [
    "MODULE ORIGIN",
    "MANIFEST",
    "HELP FOLDER",
    "PURPOSE",
    "EXPORTS",
    "DEPENDS ON",
    "REFACTOR DATE",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _has_module_docstring(path: Path) -> bool:
    try:
        tree = ast.parse(_read(path))
    except SyntaxError:
        return False
    return ast.get_docstring(tree) is not None


def _has_all(path: Path) -> bool:
    try:
        tree = ast.parse(_read(path))
    except SyntaxError:
        return False
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    return True
    return False


def _header_has_field(text: str, field: str) -> bool:
    needle = field + ":"
    return any(needle in line for line in text.splitlines()[:40])


def main() -> int:
    errors = []
    if not MANIFEST.exists():
        errors.append("context_builder_help.json is missing")
    else:
        try:
            json.loads(_read(MANIFEST))
        except json.JSONDecodeError as exc:
            errors.append("context_builder_help.json is invalid JSON: " + str(exc))

    if not HELP_INIT.exists():
        errors.append("__init__.py is missing")
    else:
        init_text = _read(HELP_INIT)
        for field in REQUIRED_HEADER_FIELDS:
            if not _header_has_field(init_text, field):
                errors.append("__init__.py: missing header field " + field)
        if not _has_all(HELP_INIT):
            errors.append("__init__.py: missing __all__")

    if not HELP_IMPL.exists():
        errors.append("inference_private_impl.py is missing")
    else:
        if not _has_module_docstring(HELP_IMPL):
            errors.append("inference_private_impl.py: missing module docstring")
        if not _has_all(HELP_IMPL):
            errors.append("inference_private_impl.py: missing __all__")

    if not ORIGIN.exists():
        errors.append("context_builder.py is missing")
    else:
        origin_text = _read(ORIGIN)
        if "AI CONTEXT" not in origin_text:
            errors.append("context_builder.py: missing AI CONTEXT docstring")

    if errors:
        print("FAIL - " + str(MANIFEST))
        for error in errors:
            print("  - " + error)
        return 1

    print("context_builder helper manifest ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
