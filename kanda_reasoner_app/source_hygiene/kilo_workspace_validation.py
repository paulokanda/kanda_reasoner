"""Focused fixtures for the exact Kilo workspace source-hygiene policy."""

from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

from .tool_archive_policy import (
    ToolArchivePolicyError,
    ToolPathClassification,
    classify_tool_source_path,
)

__all__ = ["validate_kilo_workspace_policy"]


def _gate(marker: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(marker)
    print(marker + ": PASS")


def _copy_contract(source_root: Path, target_root: Path) -> None:
    source = source_root / "kanda_reasoner_app" / "source_hygiene"
    target = target_root / "kanda_reasoner_app" / "source_hygiene"
    target.mkdir(parents=True, exist_ok=True)
    for relative in (
        "TOOL_SOURCE_CLASSIFICATION.json",
        "SYNTHETIC_FIXTURE_MANIFEST.json",
        "fixtures/static_context_smoke_minimal.json",
    ):
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / relative, destination)


def _write_workspace(root: Path) -> Path:
    workspace = root / ".kilo"
    plugin_root = workspace / "node_modules" / "@kilocode" / "plugin"
    plugin_root.mkdir(parents=True)
    (workspace / "plans").mkdir()
    dependencies = {"@kilocode/plugin": "7.4.5"}
    (workspace / ".gitignore").write_text(
        "node_modules\npackage.json\npackage-lock.json\n.gitignore\n",
        encoding="utf-8",
    )
    (workspace / "package.json").write_text(
        json.dumps({"dependencies": dependencies}), encoding="utf-8"
    )
    lockfile = {
        "name": ".kilo",
        "lockfileVersion": 3,
        "requires": True,
        "packages": {
            "": {"dependencies": dependencies},
            "node_modules/@kilocode/plugin": {"version": "7.4.5"},
        },
    }
    (workspace / "package-lock.json").write_text(
        json.dumps(lockfile), encoding="utf-8"
    )
    (plugin_root / "index.js").write_text("export {};", encoding="utf-8")
    (workspace / "plans/plan.md").write_text("# plan\n", encoding="utf-8")
    return workspace


def _expect_rejected(root: Path, workspace: Path, relative: str, content: str) -> None:
    path = workspace / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    try:
        classify_tool_source_path(root, workspace)
    except ToolArchivePolicyError:
        return
    raise AssertionError("KILO_UNEXPECTED_MEMBER_NOT_REJECTED:" + relative)


def _positive_decisions(root: Path, workspace: Path) -> tuple[object, object, object]:
    root_decision = classify_tool_source_path(root, workspace)
    cache_decision = classify_tool_source_path(
        root, workspace / "node_modules/@kilocode/plugin/index.js"
    )
    plan_decision = classify_tool_source_path(root, workspace / "plans/plan.md")
    return root_decision, cache_decision, plan_decision


def validate_kilo_workspace_policy(project_root: Path) -> None:
    """Validate current Kilo signature, subtree ownership, and fail-closed rules."""
    with tempfile.TemporaryDirectory(prefix="kanda_kilo_policy_") as raw:
        fixture_root = Path(raw)
        _copy_contract(project_root, fixture_root)
        workspace = _write_workspace(fixture_root)
        root_decision, cache_decision, plan_decision = _positive_decisions(
            fixture_root, workspace
        )
        _gate(
            "KILO_WORKSPACE_SIGNATURE_VERIFIED",
            root_decision.classification
            is ToolPathClassification.GENERATED_TOOL_EVIDENCE
            and not root_decision.include_in_tool_archive,
        )
        _gate(
            "KILO_NODE_MODULES_CACHE_CLASSIFIED",
            cache_decision.classification is ToolPathClassification.CACHE
            and not cache_decision.include_in_tool_archive,
        )
        _gate(
            "KILO_PROJECT_PLAN_EVIDENCE_EXCLUDED",
            plan_decision.classification
            is ToolPathClassification.GENERATED_TOOL_EVIDENCE
            and not plan_decision.include_in_tool_archive,
        )
        _expect_rejected(fixture_root, workspace, "unexpected.py", "VALUE = 1\n")
        _gate("KILO_UNEXPECTED_MEMBER_REJECTED", True)

        shutil.rmtree(workspace)
        workspace = _write_workspace(fixture_root)
        package = json.loads((workspace / "package.json").read_text(encoding="utf-8"))
        package["dependencies"]["unexpected-package"] = "1.0.0"
        (workspace / "package.json").write_text(json.dumps(package), encoding="utf-8")
        try:
            classify_tool_source_path(fixture_root, workspace)
        except ToolArchivePolicyError:
            mismatch_rejected = True
        else:
            mismatch_rejected = False
        _gate("KILO_PACKAGE_IDENTITY_MISMATCH_REJECTED", mismatch_rejected)
