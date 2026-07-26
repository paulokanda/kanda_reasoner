from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULES = (
    ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "advisor_comparison_contract.py",
    ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "offline_advisor_comparison.py",
)
FORBIDDEN_IMPORT_ROOTS = {
    "requests",
    "urllib",
    "httpx",
    "socket",
    "subprocess",
    "sqlite3",
    "pickle",
    "shelve",
    "pathlib",
    "os",
    "json",
}
FORBIDDEN_TEXT = (
    "open(",
    "Path(",
    "requests.",
    "urllib.",
    "sqlite3",
    "pickle",
    "subprocess",
)


def test_phase4_comparison_modules_do_not_import_io_or_provider_dependencies() -> None:
    for module_path in MODULES:
        source = module_path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name.split(".")[0] not in FORBIDDEN_IMPORT_ROOTS
            elif isinstance(node, ast.ImportFrom) and node.module:
                assert node.module.split(".")[0] not in FORBIDDEN_IMPORT_ROOTS
        for forbidden in FORBIDDEN_TEXT:
            assert forbidden not in source


if __name__ == "__main__":
    test_phase4_comparison_modules_do_not_import_io_or_provider_dependencies()
