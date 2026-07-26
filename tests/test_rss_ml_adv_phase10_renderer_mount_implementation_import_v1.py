from pathlib import Path
import ast

MODULE = Path("kanda_reasoner_app/routing_signal_scorer/ml_advisory_signal/read_only_advisory_panel_renderer_mount.py")

FORBIDDEN_IMPORT_ROOTS = {
    "os",
    "subprocess",
    "socket",
    "requests",
    "urllib",
    "http",
    "pathlib",
    "pickle",
    "shelve",
    "sqlite3",
    "openai",
    "numpy",
    "pandas",
    "sklearn",
    "tkinter",
    "PyQt5",
    "PySide6",
}

FORBIDDEN_TOKENS = (
    "open(",
    "Path(",
    "write_text",
    "read_text",
    "requests.",
    "urllib.",
    "socket.",
    "subprocess",
    "pickle",
    "sqlite3",
    "route_authority_enabled=True",
    "route_influence_enabled=True",
    "runtime_ui_mutation_enabled=True",
    "runtime_telemetry_surface_wiring_enabled=True",
    "router_calls_enabled=True",
    "advisor_calls_enabled=True",
    "provider_calls_enabled=True",
    "persistence_enabled=True",
)


def test_phase10_renderer_mount_implementation_import_boundary():
    text = MODULE.read_text(encoding="utf-8")
    tree = ast.parse(text)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                assert root not in FORBIDDEN_IMPORT_ROOTS, alias.name
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            root = module.split(".")[0]
            if node.level == 0:
                assert root not in FORBIDDEN_IMPORT_ROOTS, module
    for token in FORBIDDEN_TOKENS:
        assert token not in text, token


if __name__ == "__main__":
    test_phase10_renderer_mount_implementation_import_boundary()
    print("VALIDATION OK: phase10 read-only advisory panel renderer mount implementation import boundary")
