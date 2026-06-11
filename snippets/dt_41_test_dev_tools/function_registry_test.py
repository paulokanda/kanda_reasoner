# function_indexer_25/function_registry_test.py

from temp.dt_25_function_indexer.function_registry import index_project_functions
from pathlib import Path


def test_function_registry_loads():
    project_root = Path(__file__).resolve().parents[2]  # Should point to EEG_KANDA
    print("Scanning:", project_root)

    registry = index_project_functions(project_root)

    assert isinstance(registry, dict)
    assert len(registry) > 0, "Registry should find at least one function"

    sample_key = next(iter(registry))
    assert "::" in sample_key
    assert hasattr(registry[sample_key], "source")

