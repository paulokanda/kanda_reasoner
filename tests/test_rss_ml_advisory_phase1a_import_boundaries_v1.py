from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEATURE_ID = "rss_ml_advisory_prompt_intake_boundary_v1"
SOURCE_DIRS = (
    ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal",
    ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "prompt_intake_boundary",
)
FORBIDDEN_IMPORT_ROOTS = {
    "os",
    "socket",
    "subprocess",
    "requests",
    "urllib",
    "http",
    "sqlite3",
    "pickle",
    "shelve",
    "openai",
    "anthropic",
    "numpy",
    "pandas",
    "sklearn",
    "torch",
    "tensorflow",
}
FORBIDDEN_PROJECT_IMPORT_FRAGMENTS = (
    "project_freeze_after_update",
    "project_freeze_ledger",
    "prompt_library",
    "ACTIVE_PROMPTS",
    "router_canon",
    "first_AI_deliver",
)


def _source_files() -> list[Path]:
    files: list[Path] = []
    for source_dir in SOURCE_DIRS:
        files.extend(sorted(source_dir.glob("*.py")))
    return files


def test_phase1a_modules_do_not_import_forbidden_capabilities() -> None:
    for path in _source_files():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split(".")[0]
                    assert root not in FORBIDDEN_IMPORT_ROOTS, (path, alias.name)
            if isinstance(node, ast.ImportFrom) and node.module:
                root = node.module.split(".")[0]
                assert root not in FORBIDDEN_IMPORT_ROOTS, (path, node.module)
                for fragment in FORBIDDEN_PROJECT_IMPORT_FRAGMENTS:
                    assert fragment not in node.module, (path, node.module)


def test_phase1a_modules_do_not_call_open_or_eval_exec() -> None:
    forbidden_calls = {"open", "eval", "exec", "compile", "__import__"}
    for path in _source_files():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                assert node.func.id not in forbidden_calls, (path, node.func.id)


if __name__ == "__main__":
    test_phase1a_modules_do_not_import_forbidden_capabilities()
    test_phase1a_modules_do_not_call_open_or_eval_exec()
    print(f"VALIDATION OK: {FEATURE_ID}")
