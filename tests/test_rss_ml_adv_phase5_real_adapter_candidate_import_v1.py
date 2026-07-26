import ast
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULES = [
    PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "real_adapter_candidate_contract.py",
    PROJECT_ROOT / "kanda_reasoner_app" / "routing_signal_scorer" / "ml_advisory_signal" / "offline_real_adapter_candidate.py",
]
FORBIDDEN_IMPORTS = {
    "os",
    "pathlib",
    "subprocess",
    "requests",
    "urllib",
    "httpx",
    "socket",
    "openai",
    "sklearn",
    "numpy",
    "pandas",
}
FORBIDDEN_TEXT = (
    "open(",
    "Path(",
    "requests.",
    "urllib.",
    "socket.",
    "subprocess.",
)


def _import_root(node):
    if isinstance(node, ast.Import):
        return [alias.name.split(".")[0] for alias in node.names]
    if isinstance(node, ast.ImportFrom) and node.module:
        return [node.module.split(".")[0]]
    return []


def test_candidate_modules_have_no_forbidden_imports_or_io_text():
    for module_path in MODULES:
        text = module_path.read_text(encoding="utf-8")
        tree = ast.parse(text)
        roots = []
        for node in ast.walk(tree):
            roots.extend(_import_root(node))
        forbidden = sorted(set(roots).intersection(FORBIDDEN_IMPORTS))
        assert forbidden == [], f"forbidden imports in {module_path}: {forbidden}"
        offenders = [item for item in FORBIDDEN_TEXT if item in text]
        assert offenders == [], f"forbidden text in {module_path}: {offenders}"


def main():
    test_candidate_modules_have_no_forbidden_imports_or_io_text()


if __name__ == "__main__":
    main()
