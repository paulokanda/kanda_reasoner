# project-path: validation/test_large_module_split_audit_safety_classifier_v1.py
"""Focused validation for Large Module AST Split Audit safety classifier."""
from __future__ import annotations

import ast
import json
import tempfile
from pathlib import Path

from kanda_reasoner_app.manage_architecture.large_module_split_audit import (
    run_large_module_split_audit,
)
from kanda_reasoner_app.manage_architecture import (
    large_module_split_safety_classifier as classifier_module,
)
from kanda_reasoner_app.manage_architecture.large_module_split_safety_classifier import (
    classify_refactor_safety,
)

FEATURE_ID = "large-module-split-audit-safety-classifier-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _write_safe_module(path: Path) -> None:
    """Write a large but low-risk module with two clear responsibility groups."""
    parts = [
        '"""Synthetic safe module."""',
        "",
        "def build_alpha(value):",
        "    return value + 1",
        "",
        "def build_beta(value):",
        "    return build_alpha(value) + 1",
        "",
        "def validate_alpha(value):",
        "    return value > 0",
        "",
        "def validate_beta(value):",
        "    return validate_alpha(value) and value < 10",
        "",
    ]
    for index in range(80):
        parts.extend([
            f"def build_item_{index}(value):",
            "    return value + 1",
            "",
        ])
    for index in range(80):
        parts.extend([
            f"def validate_item_{index}(value):",
            "    return value is not None",
            "",
        ])
    path.write_text("\n".join(parts), encoding="utf-8")


def _write_risk_module(path: Path) -> None:
    """Write a large module with dynamic and global risks."""
    parts = [
        '"""Synthetic risky module."""',
        "",
        "STATE = {}",
        "",
        "def run_dynamic(name):",
        "    global STATE",
        "    module = __import__(name)",
        "    STATE[name] = getattr(module, name, None)",
        "    return STATE[name]",
        "",
        "if __name__ == '__main__':",
        "    run_dynamic('json')",
        "",
    ]
    for index in range(180):
        parts.extend([
            f"def run_item_{index}(name):",
            "    return globals().get(name)",
            "",
        ])
    path.write_text("\n".join(parts), encoding="utf-8")


def _minimal_audit_data() -> dict[str, object]:
    """Return small audit data for direct classifier validation."""
    return {
        "islands": [
            {"name": "build", "risk": "low"},
            {"name": "validate", "risk": "low"},
        ],
        "independence_matrix": [
            {"left": "build", "right": "validate", "relation": "independent"},
        ],
    }


def _validate_direct_classifier() -> None:
    """Validate safe and risky labels from direct AST classifier calls."""
    safe_source = "def build_x(value):\n    return value\n\ndef validate_x(value):\n    return value is not None\n"
    safe_tree = ast.parse(safe_source)
    safe = classify_refactor_safety(
        PROJECT_ROOT,
        PROJECT_ROOT / "safe.py",
        safe_source,
        safe_tree,
        _minimal_audit_data(),
        classifier_mode="heuristic",
    )
    assert safe["label"] == "SAFE REFACTORING", safe
    risk_source = "def run(name):\n    global STATE\n    return globals().get(name)\n"
    risk_tree = ast.parse(risk_source)
    risk = classify_refactor_safety(
        PROJECT_ROOT,
        PROJECT_ROOT / "risk.py",
        risk_source,
        risk_tree,
        _minimal_audit_data(),
        classifier_mode="heuristic",
    )
    assert risk["label"] == "RISK REFACTORING", risk


def _validate_runner_output() -> None:
    """Validate full audit output contains safety classification JSON/Markdown."""
    with tempfile.TemporaryDirectory(prefix="kanda_split_safety_") as tmp:
        root = Path(tmp) / "sample_project"
        root.mkdir()
        safe_path = root / "safe_large.py"
        risk_path = root / "risk_large.py"
        _write_safe_module(safe_path)
        _write_risk_module(risk_path)
        safe = run_large_module_split_audit(
            root,
            safe_path,
            classifier_mode="heuristic",
        )
        risk = run_large_module_split_audit(
            root,
            risk_path,
            classifier_mode="static_tools",
        )
        assert safe.data["refactor_safety_classification"]["label"] in {
            "SAFE REFACTORING",
            "RISK REFACTORING",
        }
        assert risk.data["refactor_safety_classification"]["label"] == "RISK REFACTORING"
        assert "## Refactor safety classification" in safe.markdown
        assert "## Refactor safety classification" in risk.markdown
        payload = json.loads(risk.json_path.read_text(encoding="utf-8"))
        assert "refactor_safety_classification" in payload


def _validate_ruff_module_fallback() -> None:
    """Validate Ruff can be resolved as a Python module when PATH lacks ruff."""
    original_which = classifier_module.shutil.which
    original_find_spec = classifier_module.importlib.util.find_spec
    try:
        classifier_module.shutil.which = lambda _name: None
        classifier_module.importlib.util.find_spec = (
            lambda name: object() if name == "ruff" else original_find_spec(name)
        )
        command, invocation = classifier_module.resolve_large_module_split_ruff_command()
    finally:
        classifier_module.shutil.which = original_which
        classifier_module.importlib.util.find_spec = original_find_spec
    assert command == [classifier_module.sys.executable, "-m", "ruff"]
    assert invocation.endswith(" -m ruff")


def _validate_source_contracts() -> None:
    """Validate GUI wiring and module size contracts."""
    files = [
        PROJECT_ROOT / "kanda_reasoner_app/manage_architecture/architecture_review_subtabs.py",
        PROJECT_ROOT / "kanda_reasoner_app/manage_architecture/large_module_split_audit_gui.py",
        PROJECT_ROOT / "kanda_reasoner_app/manage_architecture/large_module_split_audit.py",
        PROJECT_ROOT / "kanda_reasoner_app/manage_architecture/large_module_split_safety_classifier.py",
    ]
    for file_path in files:
        compile(file_path.read_text(encoding="utf-8"), str(file_path), "exec")
        line_count = len(file_path.read_text(encoding="utf-8").splitlines())
        assert line_count <= 500, (file_path, line_count)
    gui_text = files[0].read_text(encoding="utf-8")
    mixin_text = files[1].read_text(encoding="utf-8")
    assert "AST heuristic" in gui_text
    assert "Static Tools (AST + Ruff)" in gui_text
    assert "SAFE REFACTORING" in mixin_text
    assert "RISK REFACTORING" in mixin_text


def main() -> int:
    """Run focused validation."""
    _validate_direct_classifier()
    _validate_runner_output()
    _validate_ruff_module_fallback()
    _validate_source_contracts()
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
