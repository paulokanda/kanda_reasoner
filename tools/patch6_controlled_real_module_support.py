# project-path: tools/patch6_controlled_real_module_support.py
"""Controlled-project setup helpers for the Patch 6 real-module proof."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
import os
import shutil
import stat

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.ast_analysis import (
    analyze_python_file,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_bounded_refinement import (
    apply_bounded_plan_reassignments,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.split_planner import (
    build_split_plan,
)
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_patch5_executor_proof import (
    PATCH5_EXECUTOR_PROOF_FEATURE_ID,
    PATCH5_FREEZE_FEATURE_TITLE,
)

__all__ = [
    "CONTROLLED_TARGET_HASH",
    "ControlledProofPaths",
    "build_approved_controlled_plan",
    "prepare_controlled_project",
    "validate_readonly_cleanup_fixture",
]

CONTROLLED_TARGET_HASH = (
    "6637b1dde8639665f37f948d1bf7ba0711ecbe4d418ce304a01503f291f99f55"
)


@dataclass(frozen=True)
class ControlledProofPaths:
    """All roots and target files used by the isolated real-module proof."""

    live_project_root: Path
    work_root: Path
    controlled_project_root: Path
    controlled_target: Path
    characterization_test: Path
    shadow_root: Path
    proof_summary: Path


def sha256_file(path: Path) -> str:
    """Return exact-byte SHA-256 for one file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare_controlled_project(live_project_root: Path) -> ControlledProofPaths:
    """Create a full controlled project copy and deterministic behavior fixture."""
    live_root = live_project_root.resolve()
    work_root = live_root.parent / f"{live_root.name}_delete_after_daily_work"
    controlled = work_root / "patch6_controlled_real"
    shadow = work_root / "patch6_controlled_shadow"
    support_root = (
        live_root.parent
        / f"{live_root.name}_show_project_to_AI"
        / "large_file_refactor_workbench"
        / "final_validation"
    )
    proof_summary = support_root / "PATCH6_CONTROLLED_REAL_MODULE_PROOF.json"
    _remove_if_exists(controlled)
    _remove_if_exists(shadow)
    _remove_if_exists(controlled.parent / f"{controlled.name}_delete_after_daily_work")
    _remove_if_exists(controlled.parent / f"{controlled.name}_workbench_transactions")
    _remove_if_exists(controlled.parent / f"{controlled.name}_show_project_to_AI")
    proof_summary.unlink(missing_ok=True)
    support_root.mkdir(parents=True, exist_ok=True)
    work_root.mkdir(parents=True, exist_ok=True)
    if controlled.parent != work_root or shadow.parent != work_root:
        raise AssertionError("CONTROLLED_VALIDATION_FIXTURE_OUTSIDE_TRANSIENT_GARBAGE_ROOT")
    shutil.copytree(
        live_root,
        controlled,
        ignore=shutil.ignore_patterns(
            ".git",
            ".hg",
            ".svn",
            "__pycache__",
            "*.pyc",
            ".pytest_cache",
            ".mypy_cache",
            ".ruff_cache",
        ),
    )
    (controlled / "__init__.py").unlink(missing_ok=True)
    _ensure_reference_folder_policy_fixture(controlled)
    test_file = controlled / "tests" / "test_patch6_main_helper_mapper_characterization.py"
    test_file.parent.mkdir(parents=True, exist_ok=True)
    test_file.write_text(_characterization_test_text(), encoding="utf-8")
    _write_patch5_freeze_proof(controlled)
    target = controlled / "kanda_reasoner_app" / "reasoner_symbol_atlas" / "main_helper_mapper.py"
    if not target.is_file():
        raise AssertionError("PATCH6_CONTROLLED_TARGET_MISSING:" + str(target))
    return ControlledProofPaths(
        live_project_root=live_root,
        work_root=work_root,
        controlled_project_root=controlled,
        controlled_target=target,
        characterization_test=test_file,
        shadow_root=shadow,
        proof_summary=proof_summary,
    )



def validate_readonly_cleanup_fixture(work_root: Path) -> None:
    """Prove disposable cleanup can remove one Windows read-only fixture."""
    probe_root = work_root / "patch6_readonly_cleanup_probe"
    _remove_if_exists(probe_root)
    probe_root.mkdir(parents=True, exist_ok=True)
    probe_file = probe_root / "readonly_probe.txt"
    probe_file.write_text("readonly cleanup probe\n", encoding="utf-8")
    os.chmod(probe_file, stat.S_IREAD)
    _remove_if_exists(probe_root)
    if probe_root.exists():
        raise AssertionError("PATCH6_READONLY_CLEANUP_PROBE_REMAINS")

def build_approved_controlled_plan(target: Path):
    """Build the approved 197/145/429 plan for the real mapper target."""
    analysis = analyze_python_file(target)
    heuristic = build_split_plan(analysis)
    helpers = [module for module in heuristic.proposed_modules if module.role != "public_facade"]
    if len(helpers) != 2:
        raise AssertionError("PATCH6_EXPECTED_TWO_HELPERS")
    path_resolution = min(helpers, key=lambda module: module.estimated_lines)
    plan = apply_bounded_plan_reassignments(
        analysis,
        heuristic,
        [
            {
                "symbol": "_related_tests_to_run",
                "target_module": path_resolution.filename,
            }
        ],
    )
    expected = [145, 197, 429]
    actual = sorted(module.estimated_lines for module in plan.proposed_modules)
    if actual != expected:
        raise AssertionError(f"PATCH6_APPROVED_PLAN_SIZE_MISMATCH:{actual}")
    return analysis, plan


def _remove_if_exists(path: Path) -> None:
    """Remove one disposable path, clearing Windows read-only file attributes."""
    if path.is_dir():
        shutil.rmtree(path, onerror=_remove_readonly_and_retry)
    elif path.exists():
        try:
            path.unlink()
        except PermissionError:
            os.chmod(path, stat.S_IWRITE | stat.S_IREAD)
            path.unlink()


def _remove_readonly_and_retry(function, path: str, exc_info) -> None:
    """Clear read-only mode for one disposable path and retry its failed removal."""
    del exc_info
    os.chmod(path, stat.S_IWRITE | stat.S_IREAD)
    function(path)


def _write_patch5_freeze_proof(controlled_root: Path) -> None:
    """Mirror the required read-only executor proof into the controlled copy context."""
    entries = (
        controlled_root.parent
        / f"{controlled_root.name}_show_project_to_AI"
        / "project_freeze_after_update"
        / "frozen_features_memory"
        / "entries"
    )
    entries.mkdir(parents=True, exist_ok=True)
    entry = entries / "freeze-patch5-journaled-apply-adversarial-proof.md"
    entry.write_text(
        "---\nstatus: \"frozen\"\n---\n"
        f"# {PATCH5_FREEZE_FEATURE_TITLE}\n"
        f"feature_id: {PATCH5_EXECUTOR_PROOF_FEATURE_ID}\n"
        "Journaled sealed payload apply with rollback and recovery proof.\n",
        encoding="utf-8",
    )


def _ensure_reference_folder_policy_fixture(controlled_root: Path) -> None:
    """Add a controlled-copy compatibility fixture when the archive omitted it."""
    path = controlled_root / "kanda_reasoner_app" / "reasoner_symbol_atlas" / "reference_folder_policy.py"
    if path.exists():
        return
    path.write_text(
        '''"""Controlled-proof compatibility fixture for an omitted archive dependency."""\n'''
        "from __future__ import annotations\n"
        "from pathlib import Path\n"
        "PROJECT_SYMBOL_ATLAS_INACTIVE_REFERENCE_FOLDERS = (\"_project_reference\", \"project_reference\")\n"
        "def build_reasoner_symbol_atlas_reference_path_markers():\n"
        "    return tuple(item + \"/\" for item in PROJECT_SYMBOL_ATLAS_INACTIVE_REFERENCE_FOLDERS)\n"
        "def is_reasoner_symbol_atlas_reference_path(path):\n"
        "    text = str(path).replace('\\\\', '/').lower()\n"
        "    return any('/' + item.lower() + '/' in '/' + text.strip('/') + '/' for item in PROJECT_SYMBOL_ATLAS_INACTIVE_REFERENCE_FOLDERS)\n"
        "def iter_reasoner_symbol_atlas_reference_evidence_dirs(project_root):\n"
        "    root = Path(project_root)\n"
        "    return tuple(root / name for name in PROJECT_SYMBOL_ATLAS_INACTIVE_REFERENCE_FOLDERS if (root / name).is_dir())\n"
        "def normalize_reasoner_symbol_atlas_policy_path(path):\n"
        "    return str(path).replace('\\\\', '/').strip()\n",
        encoding="utf-8",
    )


def _characterization_test_text() -> str:
    """Return focused behavior characterization for the controlled real target."""
    return r'''from __future__ import annotations
from types import SimpleNamespace
from kanda_reasoner_app.reasoner_symbol_atlas import main_helper_mapper as mapper
from kanda_reasoner_app.reasoner_symbol_atlas.schemas import ProjectModuleRecord, ProjectSymbol, ProjectSymbolAtlasReport

def _report(tmp_path):
    main = ProjectModuleRecord(module="pkg.service", path="pkg/service.py", line_count=140, owner_role="canonical_owner", symbols=(ProjectSymbol(name="run", kind="function", module="pkg.service", path="pkg/service.py"),), imports=("pkg.service_helper",), evidence=("active source",))
    helper = ProjectModuleRecord(module="pkg.service_helper", path="pkg/service_helper.py", line_count=120, owner_role="private_helper", symbols=(ProjectSymbol(name="help_value", kind="function", module="pkg.service_helper", path="pkg/service_helper.py", is_public=False),), imports=(), evidence=("private_helper",))
    unrelated = ProjectModuleRecord(module="pkg.other", path="pkg/other.py", line_count=110, owner_role="canonical_owner", symbols=(), imports=())
    return ProjectSymbolAtlasReport(project_root=str(tmp_path), modules=(main, helper, unrelated))

def _install(monkeypatch, tmp_path):
    report = _report(tmp_path)
    monkeypatch.setattr(mapper, "merge_reasoner_symbol_atlas_live_and_json_evidence", lambda _options: (report, SimpleNamespace(status="live_only")))

def test_main_target_maps_private_helper(monkeypatch, tmp_path):
    _install(monkeypatch, tmp_path)
    d = mapper.map_reasoner_symbol_atlas_main_helpers(mapper.ProjectSymbolAtlasMainHelperOptions(project_root=str(tmp_path), target_path="pkg/service.py", include_private=True))
    assert d.status == mapper.PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_READY
    assert d.target_role == "main" and d.main_path == "pkg/service.py"
    assert d.helper_paths == ("pkg/service_helper.py",) and d.private_helper_paths == ("pkg/service_helper.py",)
    assert d.public_api_owner_path == "pkg/service.py" and d.tests_to_run == ()

def test_helper_target_resolves_main_owner(monkeypatch, tmp_path):
    _install(monkeypatch, tmp_path)
    d = mapper.map_reasoner_symbol_atlas_main_helpers(mapper.ProjectSymbolAtlasMainHelperOptions(project_root=str(tmp_path), target_path="pkg/service_helper.py", include_private=True))
    assert d.status == mapper.PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_READY
    assert d.target_role == "helper" and d.main_path == "pkg/service.py"
    assert d.helper_paths == ("pkg/service_helper.py",)

def test_missing_target_is_fail_closed(monkeypatch, tmp_path):
    _install(monkeypatch, tmp_path)
    d = mapper.map_reasoner_symbol_atlas_main_helpers(mapper.ProjectSymbolAtlasMainHelperOptions(project_root=str(tmp_path), target_path="pkg/missing.py"))
    assert d.status == mapper.PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_TARGET_NOT_FOUND
    assert d.confidence == "high"

def test_report_preserves_public_summary_contract(monkeypatch, tmp_path):
    _install(monkeypatch, tmp_path)
    r = mapper.build_reasoner_symbol_atlas_main_helper_report(mapper.ProjectSymbolAtlasMainHelperOptions(project_root=str(tmp_path), target_path="pkg/service.py", include_private=True))
    assert r.report_type == "reasoner_symbol_atlas"
    assert r.summary.startswith("Main/helper map status=ready")
    assert [s.name for s in r.symbols] == ["main_file", "helper_file"]
'''
