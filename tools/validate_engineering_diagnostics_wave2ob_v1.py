# project-path: tools/validate_engineering_diagnostics_wave2ob_v1.py
"""Validate Engineering Diagnostics GUI Wave 2O-B against frozen 2O-A."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import os
from pathlib import Path
import subprocess
import sys
from typing import Iterable

from tools.engineering_diagnostics_wave2ob_architecture_gate import (
    validate_engineering_diagnostics_wave2ob_architecture_non_regression,
)
from tools.engineering_diagnostics_wave2ob_public_boundary_gate import (
    validate_engineering_diagnostics_wave2ob_public_boundary,
)

FEATURE_ID = "kanda-reasoner-engineering-diagnostics-gui-wave2ob-v1"
PACKAGE_REVISION = "v1r1"
_FROZEN_BACKEND_HASHES = {
    "kanda_reasoner_app/engineering_diagnostics/__init__.py": "4a29f3ba39fff1e9357189f5185d27ff0efe071e7a7c48bf881d167de5a06b62",
    "kanda_reasoner_app/engineering_diagnostics/_store_baseline_ops.py": "18d038f8302906b291f70de3fa89c5a2148dd0b971271457776963e98012e1e1",
    "kanda_reasoner_app/engineering_diagnostics/_store_database.py": "bbf6a57ef1d65bf05f4cd173ab34a91fd6f5eb4ec33ea90c3df931f44cfb75b8",
    "kanda_reasoner_app/engineering_diagnostics/baseline.py": "5a4806826572c9334e034818f88ec3517d4c684a4338ab76f0cb57047695da3e",
    "kanda_reasoner_app/engineering_diagnostics/bom_adapter.py": "ceeb930aa9713c63205d1d6c60aad286abc60dfa246e11492ce88846190fef25",
    "kanda_reasoner_app/engineering_diagnostics/fingerprinting.py": "7e262b06c167ea315fe8e26258428090a4271400a62c77cf7ec616bebcade69b",
    "kanda_reasoner_app/engineering_diagnostics/models.py": "2053c3dfcaa8d08939d99626c9b18a1d1d887bc24a163d974db36dc93d7d2184",
    "kanda_reasoner_app/engineering_diagnostics/paths.py": "95640db89ef725b160cbbe6784599f9ab9f5c1cf01814602b1121c924d48c48d",
    "kanda_reasoner_app/engineering_diagnostics/store.py": "b40d07897501051b4318ad50577769c1df86481a8cd88f08f8374cd3e766272e",
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _check_hashes(root: Path, expected: dict[str, str], marker: str) -> None:
    for relative, digest in expected.items():
        path = root / relative
        _require(path.is_file(), "VALIDATED_FILE_MISSING:" + relative)
        _require(_sha256(path) == digest, "VALIDATED_FILE_HASH_MISMATCH:" + relative)
    print(marker)


def _run(
    command: list[str],
    *,
    cwd: Path,
    markers: Iterable[str],
) -> str:
    completed = subprocess.run(
        command,
        cwd=str(cwd),
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    output = completed.stdout + completed.stderr
    print(output, end="" if output.endswith("\n") else "\n")
    _require(completed.returncode == 0, "VALIDATION_COMMAND_FAILED:" + " ".join(command))
    for marker in markers:
        _require(marker in output, "VALIDATION_MARKER_MISSING:" + marker)
    return output


def _registry_digest(root: Path) -> tuple[Path, str]:
    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry

    registry = ProjectSelectionRegistry(tool_source_root=root)
    path = registry.registry_path
    digest = _sha256(path) if path.is_file() else "ABSENT"
    return path, digest


def _check_gui_smoke(root: Path) -> None:
    package = importlib.import_module("kanda_reasoner_app.engineering_diagnostics_gui")
    _require(
        callable(getattr(package, "create_engineering_diagnostics_panel", None)),
        "ENGINEERING_DIAGNOSTICS_GUI_FACTORY_MISSING",
    )
    print("ENGINEERING DIAGNOSTICS GUI COMPLETE IMPORT GRAPH: PASS")
    try:
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
        from PySide6.QtWidgets import QApplication
    except ImportError as exc:
        raise RuntimeError("PYSIDE6_REQUIRED_FOR_GUI_VALIDATION") from exc
    app = QApplication.instance() or QApplication([])
    panel = package.create_engineering_diagnostics_panel(
        project_root_provider=lambda: str(root),
        defer_initial_refresh=True,
    )
    _require(panel.objectName() == "engineering_diagnostics_page", "GUI_PANEL_OBJECT_NAME")
    _require(hasattr(panel, "set_project_root"), "GUI_PROJECT_ROOT_SYNC_MISSING")
    panel.deleteLater()
    app.processEvents()
    print("ENGINEERING DIAGNOSTICS GUI FACTORY SMOKE: PASS")


def _check_host_import() -> None:
    module = importlib.import_module(
        "kanda_reasoner_app.manage_architecture.architecture_review_subtabs"
    )
    _require(
        callable(getattr(module, "build_architecture_review_ui", None)),
        "AUDIT_PROJECT_HOST_IMPORT_FAILED",
    )
    print("AUDIT PROJECT ENGINEERING DIAGNOSTICS HOST IMPORT: PASS")


def _run_tests(root: Path) -> None:
    _run(
        [
            sys.executable,
            "-m",
            "unittest",
            "-v",
            "tests.test_engineering_diagnostics_wave2ob",
        ],
        cwd=root,
        markers=("Ran 8 tests", "OK"),
    )
    print("FOCUSED PUBLIC CONTRACT TESTS: 8/8 PASS")
    print("WAVE2OB TOKEN-BOUND SUPPORT FIXTURE: PASS")


def _run_previous_wave(root: Path) -> None:
    _run(
        [
            sys.executable,
            str(root / "tools/validate_engineering_diagnostics_wave2oa_v1.py"),
            "--project-root",
            str(root),
        ],
        cwd=root,
        markers=(
            "VALIDATION OK: kanda-reasoner-engineering-diagnostics-backend-foundation-wave2oa-v1",
            "STATUS: IN_SYNC",
        ),
    )
    print("WAVE2OA VALIDATOR PROJECT ROOT ARGUMENT: PASS")
    print("WAVE2OA FROZEN CONTRACT PRESERVED: PASS")


def _run_architecture(root: Path) -> None:
    output = _run(
        [
            sys.executable,
            str(root / "kanda_reasoner_app/manage_architecture/manage_architecture.py"),
            "--root",
            str(root),
            "--validate",
        ],
        cwd=root,
        markers=("ARCHITECTURE VALIDATION SUMMARY",),
    )
    validate_engineering_diagnostics_wave2ob_architecture_non_regression(output)


def _write_evidence(root: Path, lines: list[str]) -> Path:
    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry

    boundary = ProjectSelectionRegistry(tool_source_root=root).resolve_boundary_for_root(root)
    target = (
        boundary.active_project_support_root
        / "project_validation_evidence"
        / "engineering_diagnostics_wave2ob"
        / "engineering_diagnostics_wave2ob_v1.txt"
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return target


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    root = Path(args.root).expanduser().resolve(strict=True)
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    print("PACKAGE REVISION: " + PACKAGE_REVISION)
    print("VALIDATOR PROJECT ROOT IMPORT PATH: PASS")
    registry_path, registry_before = _registry_digest(root)
    _check_hashes(root, _FROZEN_BACKEND_HASHES, "WAVE2OA FROZEN BACKEND HASHES: PASS")
    validate_engineering_diagnostics_wave2ob_public_boundary(root)
    _run_tests(root)
    _check_gui_smoke(root)
    _check_host_import()
    _run_previous_wave(root)
    _run_architecture(root)
    registry_after = _sha256(registry_path) if registry_path.is_file() else "ABSENT"
    _require(registry_before == registry_after, "PROJECT_SELECTION_REGISTRY_MUTATED")
    print("PROJECT SELECTION REGISTRY MUTATED: NO")
    print("TOOL PROJECT LOGICAL ROLE SEPARATION: PASS")
    evidence_lines = [
        "PACKAGE REVISION: " + PACKAGE_REVISION,
        "WAVE2OA FROZEN BACKEND HASHES: PASS",
        "ENGINEERING DIAGNOSTICS GUI PUBLIC-CONTRACT-ONLY COMMUNICATION: PASS",
        "ENGINEERING DIAGNOSTICS GUI DIRECT SQLITE ACCESS: 0",
        "ENGINEERING DIAGNOSTICS GUI BACKEND PRIVATE REACH-IN: 0",
        "FOCUSED PUBLIC CONTRACT TESTS: 8/8 PASS",
        "WAVE2OB TOKEN-BOUND SUPPORT FIXTURE: PASS",
        "ENGINEERING DIAGNOSTICS GUI FACTORY SMOKE: PASS",
        "AUDIT PROJECT ENGINEERING DIAGNOSTICS HOST IMPORT: PASS",
        "WAVE2OA VALIDATOR PROJECT ROOT ARGUMENT: PASS",
        "WAVE2OA FROZEN CONTRACT PRESERVED: PASS",
        "WAVE2OB NEW ARCHITECTURE ISSUES: 0",
        "WAVE2OB TOUCHED PATH ARCHITECTURE ISSUES: 0",
        "PROJECT SELECTION REGISTRY MUTATED: NO",
        "TOOL PROJECT LOGICAL ROLE SEPARATION: PASS",
        "VALIDATION OK: " + FEATURE_ID,
        "STATUS: IN_SYNC",
    ]
    evidence = _write_evidence(root, evidence_lines)
    print("VALIDATION EVIDENCE WRITTEN: " + str(evidence))
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
