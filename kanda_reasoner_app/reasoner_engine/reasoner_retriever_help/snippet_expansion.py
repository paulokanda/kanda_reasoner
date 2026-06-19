# -"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR
# MODULE ORIGIN : <PROJECT_ROOT>\kanda_reasoner_app\reasoner_engine\reasoner_retriever.py
# MANIFEST      : <PROJECT_ROOT>\kanda_reasoner_app\reasoner_engine\reasoner_retriever_help.json
# HELP FOLDER   : <PROJECT_ROOT>\kanda_reasoner_app\reasoner_engine\reasoner_retriever_help
# PURPOSE       : Expand snippet-derived callee names for retrieval refinement.
# EXPORTS       : _extract_named_callees
# DEPENDS ON    : none
# REFACTOR DATE : 2026-04-11
# -"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR

"""


MODULE ORIGIN: <PROJECT_ROOT>sk_ai_project_reasoner/project_reasoner_v10
easoner_retriever.py
MANIFEST: <PROJECT_ROOT>sk_ai_project_reasoner/project_reasoner_v10
easoner_retriever_help.json
HELP FOLDER: <PROJECT_ROOT>sk_ai_project_reasoner/project_reasoner_v10
easoner_retriever_help
PURPOSE: Own snippet callee extraction helpers.
DEPENDS ON:
REFACTOR DATE: 2026-04-10
"""
from __future__ import annotations

__all__ = [
]
__all__ = ["_extract_named_callees"]
# a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-
# MODULE ORIGIN : <PROJECT_ROOT>\kanda_reasoner_app\reasoner_engine\reasoner_retriever.py
# MANIFEST      : <PROJECT_ROOT>\kanda_reasoner_app\reasoner_engine\reasoner_retriever_help.json
# HELP FOLDER   : <PROJECT_ROOT>\kanda_reasoner_app\reasoner_engine\reasoner_retriever_help
# PURPOSE       : Extract named callees and imported symbols from snippet text for query expansion.
# EXPORTS       : none
# DEPENDS ON    : none
# REFACTOR DATE : 2026-04-10
# a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-a--,-

import re

__all__: list[str] = []

CALL_RE = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(")

FROM_IMPORT_RE = re.compile(
    r"from\s+[\w\.]+\s+import\s+\(\s*([A-Za-z_][A-Za-z0-9_]*)",
    re.MULTILINE,
)

SIMPLE_IMPORT_RE = re.compile(r"from\s+[\w\.]+\s+import\s+([A-Za-z_][A-Za-z0-9_]*)")

IGNORE_CALLS = {
    "hasattr", "getattr", "setattr", "isinstance", "len", "print",
    "dict", "list", "set", "tuple", "int", "str", "float", "bool",
}

def _extract_named_callees(snippet_text: str) -> set[str]:
    names = set()

    for m in CALL_RE.finditer(snippet_text or ""):
        name = m.group(1)
        if name not in IGNORE_CALLS and not name.startswith("_re"):
            names.add(name)

    for m in FROM_IMPORT_RE.finditer(snippet_text or ""):
        names.add(m.group(1))

    for m in SIMPLE_IMPORT_RE.finditer(snippet_text or ""):
        names.add(m.group(1))

    return names
