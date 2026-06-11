# embedding_tools/embedding_index.py

from temp.dt_25_function_indexer.function_registry import index_project_functions
from pathlib import Path

def build_docstring_index(project_root: Path):
    function_registry = index_project_functions(project_root)
    index = {}
    for key, record in function_registry.items():
        # INCLUDE ALL FUNCTIONS even if they have no docstrings
        index[key] = record.doc.strip() if record.doc else ""
    return index