import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILES = [
    ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "offline_evaluation_contract.py",
    ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "offline_evaluation_harness.py",
]

FORBIDDEN_IMPORT_ROOTS = {
    "requests",
    "httpx",
    "urllib",
    "socket",
    "subprocess",
    "pickle",
    "shelve",
    "sqlite3",
    "pathlib",
    "openai",
    "numpy",
    "pandas",
    "sklearn",
    "torch",
}

FORBIDDEN_PROJECT_IMPORT_PARTS = {
    "prompt_library",
    "project_freeze_after_update",
    "project_freeze_ledger",
    "router_canon",
    "prompt_registry",
    "providers",
    "embeddings",
    "vector_store",
}

FORBIDDEN_CALLS = {"open", "compile", "exec", "eval", "__import__"}


def _import_root(name):
    return name.split(".")[0]


def test_phase2_source_files_have_no_forbidden_imports_or_calls():
    for path in SOURCE_FILES:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert _import_root(alias.name) not in FORBIDDEN_IMPORT_ROOTS, alias.name
                    for part in FORBIDDEN_PROJECT_IMPORT_PARTS:
                        assert part not in alias.name, alias.name
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                assert _import_root(module) not in FORBIDDEN_IMPORT_ROOTS, module
                for part in FORBIDDEN_PROJECT_IMPORT_PARTS:
                    assert part not in module, module
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    assert node.func.id not in FORBIDDEN_CALLS, node.func.id


def test_phase2_source_files_do_not_create_mlrt_113():
    for path in SOURCE_FILES:
        text = path.read_text(encoding="utf-8").lower()
        assert "mlrt_113" not in text
        assert "mlrt-113" not in text
        assert "mlrt113" not in text
