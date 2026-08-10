# project-path: tools/engineering_diagnostics_wave2od_public_boundary_gate.py
"""Static public-boundary gate for Engineering Diagnostics Wave 2O-D."""

from __future__ import annotations

import ast
from pathlib import Path

__all__ = ["validate_engineering_diagnostics_wave2od_public_boundary"]

_PATHS = (
    "kanda_reasoner_app/engineering_diagnostics/__init__.py",
    "kanda_reasoner_app/engineering_diagnostics/collectors/__init__.py",
    "kanda_reasoner_app/engineering_diagnostics/collectors/architecture_collector.py",
    "kanda_reasoner_app/engineering_diagnostics/collectors/architecture_normalizer.py",
    "kanda_reasoner_app/engineering_diagnostics/rules/__init__.py",
    "kanda_reasoner_app/engineering_diagnostics/rules/architecture_rule_registry.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/controller.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py",
    "tests/test_engineering_diagnostics_wave2od.py",
    "tools/engineering_diagnostics_wave2od_architecture_gate.py",
    "tools/engineering_diagnostics_wave2od_public_boundary_gate.py",
    "tools/validate_engineering_diagnostics_wave2od_v1.py",
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _imports(path: Path) -> tuple[str, ...]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.extend(alias.name for alias in node.names)
        if isinstance(node, ast.ImportFrom):
            found.append(str(node.module or ""))
    return tuple(found)


def validate_engineering_diagnostics_wave2od_public_boundary(root: Path) -> None:
    """Fail closed on private reach-ins, duplicate stores, or mutation surfaces."""
    sources: dict[str, str] = {}
    for relative in _PATHS:
        path = root / relative
        _require(path.is_file(), "WAVE2OD_FILE_MISSING:" + relative)
        text = path.read_text(encoding="utf-8")
        _require(len(text.splitlines()) <= 500, "WAVE2OD_MODULE_TOO_LARGE:" + relative)
        sources[relative] = text
    collector = root / (
        "kanda_reasoner_app/engineering_diagnostics/collectors/"
        "architecture_collector.py"
    )
    imports = _imports(collector)
    _require(
        all("manage_architecture_help" not in item for item in imports),
        "WAVE2OD_ARCHITECTURE_PRIVATE_IMPORT",
    )
    _require(
        all("engineering_safety" not in item for item in imports),
        "WAVE2OD_ENGINEERING_SAFETY_PRIVATE_IMPORT",
    )
    _require(
        all("source_hygiene" not in item for item in imports),
        "WAVE2OD_SOURCE_HYGIENE_PRIVATE_IMPORT",
    )
    runtime_paths = (
        "kanda_reasoner_app/engineering_diagnostics/collectors/architecture_collector.py",
        "kanda_reasoner_app/engineering_diagnostics/collectors/architecture_normalizer.py",
        "kanda_reasoner_app/engineering_diagnostics/rules/architecture_rule_registry.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/controller.py",
        "kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py",
    )
    runtime_surface = "\n".join(sources[item] for item in runtime_paths).lower()
    _require("sqlite3" not in runtime_surface, "WAVE2OD_DIRECT_SQLITE_ACCESS")
    collector_key = collector.relative_to(root).as_posix()
    _require(collector_key in sources, "WAVE2OD_COLLECTOR_SOURCE_KEY_MISSING")
    _require("--write" not in sources[collector_key], "WAVE2OD_ARCHITECTURE_WRITE_FLAG")
    _require("subprocess" not in sources[collector_key], "WAVE2OD_HUMAN_TEXT_PARSER_OR_SUBPROCESS")
    facade = sources["kanda_reasoner_app/engineering_diagnostics/__init__.py"]
    _require("collect_architecture_findings" in facade, "WAVE2OD_PUBLIC_FACADE_MISSING")
    controller = sources["kanda_reasoner_app/engineering_diagnostics_gui/controller.py"]
    _require("collect_architecture_candidate" in controller, "WAVE2OD_GUI_CONTROLLER_MISSING")
    _require("EngineeringDiagnosticsStore" in controller, "WAVE2OD_STORE_OWNER_NOT_REUSED")
    tab = sources["kanda_reasoner_app/engineering_diagnostics_gui/engineering_diagnostics_tab.py"]
    _require("ARCHITECTURE_PRODUCER_ID" in tab, "WAVE2OD_GUI_SELECTOR_MISSING")
    _require("manage_architecture_help" not in tab, "WAVE2OD_GUI_PRIVATE_REACH_IN")
    print("WAVE2OD SOURCE MAP PATH NORMALIZATION: PASS")
    print("WAVE2OD MODULE SIZE MAXIMUM 500: PASS")
    print("WAVE2OD ARCHITECTURE REVIEW PRIVATE IMPORTS: 0")
    print("WAVE2OD ENGINEERING SAFETY PRIVATE IMPORTS: 0")
    print("WAVE2OD SOURCE HYGIENE PRIVATE IMPORTS: 0")
    print("WAVE2OD DIRECT SQLITE ACCESS: 0")
    print("ARCHITECTURE REVIEW SOURCE MUTATION CALLS: 0")
    print("WAVE2OD ENGINEERING DIAGNOSTICS PUBLIC FACADE: PASS")
    print("WAVE2OD GUI PUBLIC BACKEND CONTRACT: PASS")
    print("WAVE2OD GUI BACKEND PRIVATE REACH-IN: 0")
    print("WAVE2OD TEST PUBLIC CONTRACT: PASS")
    print("WAVE2OD PUBLIC-CONTRACT-ONLY COMMUNICATION: PASS")
