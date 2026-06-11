# test_embedding_index_test.py

from pathlib import Path
from temp.dt_13_embedding_tools.embedding_index import build_docstring_index

def test_docstring_index_builds():
    index = build_docstring_index(Path("EEG_KANDA"))
    print(f"📦 Total functions indexed: {len(index)}")

    assert isinstance(index, dict)
    assert len(index) > 0, "Should find at least one function in project"
