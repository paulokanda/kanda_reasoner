"""Live and functional validation for Portable governed-root exact rollback."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path

from portable.constants import (
    PORTABLE_HARDENING_FEATURES,
    PRODUCTION_PORTABLE_ENABLED,
)
from portable.errors import PortableBuildError
from portable.governed_root_rollback import prepare_governed_root_rollback
from portable.models import BuildPaths, ProtectedRoot, RegistryBoundary
from portable.registry_boundary import load_registry_boundary

FEATURE_ID = "portable-governed-root-rollback-v1"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _protected(
    label: str,
    owner_id: str,
    owner_slug: str,
    root_kind: str,
    path: Path,
) -> ProtectedRoot:
    return ProtectedRoot(
        label=label,
        owner_id=owner_id,
        owner_slug=owner_slug,
        root_kind=root_kind,
        path=path.resolve(),
    )


def _fixture_paths(root: Path) -> tuple[BuildPaths, dict[str, Path]]:
    tool = root / "kanda_reasoner"
    tool_support = root / "kanda_reasoner_show_project_to_AI"
    tool_transient = root / "kanda_reasoner_delete_after_daily_work"
    other = root / "eeg_kanda"
    other_support = root / "eeg_kanda_show_project_to_AI"
    other_transient = root / "eeg_kanda_delete_after_daily_work"
    run_root = tool_transient / "portable_build" / "fixture_run"
    registry = tool_support / "tool_project_registry" / "projects.json"

    _write(tool / "source" / "main.py", "print('tool baseline')\n")
    _write(tool / "source" / "keep.txt", "tool keep\n")
    _write(tool / ".venv" / "ignored.txt", "ignored cache lane\n")
    _write(tool_support / "memory" / "owner.json", '{"owner":"tool"}\n')
    _write(tool_transient / "outside_build_lane.txt", "transient baseline\n")
    _write(other / "eeg" / "engine.py", "EEG = 'baseline'\n")
    _write(other_support / "memory" / "project.json", '{"owner":"eeg"}\n')
    _write(other_transient / "job" / "state.txt", "state baseline\n")
    run_root.mkdir(parents=True)

    registry_payload = {
        "current_project_id": "tool-id",
        "projects": {
            "tool-id": {
                "stable_project_id": "tool-id",
                "owner_slug": "kanda_reasoner",
                "project_root": str(tool.resolve()),
                "project_support_root": str(tool_support.resolve()),
                "project_transient_root": str(tool_transient.resolve()),
                "selection_mode": "EXPLICIT_SELF_HOSTING",
            },
            "eeg-id": {
                "stable_project_id": "eeg-id",
                "owner_slug": "eeg_kanda",
                "project_root": str(other.resolve()),
                "project_support_root": str(other_support.resolve()),
                "project_transient_root": str(other_transient.resolve()),
                "selection_mode": "EXPLICIT_EXTERNAL_PROJECT",
            },
        },
    }
    _write(registry, json.dumps(registry_payload, indent=2, sort_keys=True) + "\n")

    protected_roots = (
        _protected("Tool source", "tool-id", "kanda_reasoner", "PROJECT_ROOT", tool),
        _protected(
            "Tool Support",
            "tool-id",
            "kanda_reasoner",
            "PROJECT_SUPPORT_ROOT",
            tool_support,
        ),
        _protected(
            "Tool transient",
            "tool-id",
            "kanda_reasoner",
            "PROJECT_TRANSIENT_ROOT",
            tool_transient,
        ),
        _protected("EEG source", "eeg-id", "eeg_kanda", "PROJECT_ROOT", other),
        _protected(
            "EEG Support",
            "eeg-id",
            "eeg_kanda",
            "PROJECT_SUPPORT_ROOT",
            other_support,
        ),
        _protected(
            "EEG transient",
            "eeg-id",
            "eeg_kanda",
            "PROJECT_TRANSIENT_ROOT",
            other_transient,
        ),
    )
    boundary = RegistryBoundary(
        registry_path=registry.resolve(),
        registry_sha256=_sha256(registry),
        current_project_id="tool-id",
        selection_mode="EXPLICIT_SELF_HOSTING",
        tool_root=tool.resolve(),
        tool_support_root=tool_support.resolve(),
        tool_transient_root=tool_transient.resolve(),
        protected_roots=protected_roots,
    )
    paths = BuildPaths(
        project_root=tool.resolve(),
        drive_root=root.resolve(),
        project_support_root=tool_support.resolve(),
        transient_root=tool_transient.resolve(),
        run_root=run_root.resolve(),
        pyinstaller_work=run_root / "pyinstaller_work",
        pyinstaller_dist=run_root / "pyinstaller_dist",
        pyinstaller_config=run_root / "pyinstaller_config",
        temporary_root=run_root / "temp",
        stage_parent=run_root / "release_stage",
        candidate_zip=run_root / "KandaReasoner-Windows-Portable.zip",
        clean_extract_root=run_root / "clean_extract",
        final_zip=root / "output" / "KandaReasoner-Windows-Portable.zip",
        spec_path=tool / "KandaReasonerWindows.spec",
        governed_python=Path(os.sys.executable).resolve(),
        zip_helper=tool / "portable" / "create_windows_zip.ps1",
        registry_boundary=boundary,
    )
    return paths, {
        "tool": tool,
        "tool_support": tool_support,
        "tool_transient": tool_transient,
        "other": other,
        "other_support": other_support,
        "other_transient": other_transient,
        "run_root": run_root,
        "registry": registry,
    }


def _assert_restored(paths: dict[str, Path]) -> None:
    if (paths["tool"] / "source" / "main.py").read_text(encoding="utf-8") != "print('tool baseline')\n":
        raise RuntimeError("Tool source was not restored exactly.")
    if (paths["tool_support"] / "memory" / "owner.json").read_text(encoding="utf-8") != '{"owner":"tool"}\n':
        raise RuntimeError("Tool Support was not restored exactly.")
    if (paths["other"] / "eeg" / "engine.py").read_text(encoding="utf-8") != "EEG = 'baseline'\n":
        raise RuntimeError("Other Project source was not restored exactly.")
    if (paths["other_support"] / "memory" / "project.json").read_text(encoding="utf-8") != '{"owner":"eeg"}\n':
        raise RuntimeError("Other Project Support was not restored exactly.")
    if (paths["other_transient"] / "job" / "state.txt").read_text(encoding="utf-8") != "state baseline\n":
        raise RuntimeError("Other Project transient state was not restored exactly.")
    if (paths["tool_transient"] / "outside_build_lane.txt").read_text(encoding="utf-8") != "transient baseline\n":
        raise RuntimeError("Tool transient protected view was not restored exactly.")
    if (paths["tool"] / "source" / "new_file.txt").exists():
        raise RuntimeError("New Tool source file survived rollback.")
    if (paths["other_support"] / "memory" / "new.json").exists():
        raise RuntimeError("New Project Support file survived rollback.")


def _functional_fixture() -> None:
    with tempfile.TemporaryDirectory(prefix="kanda_portable_rollback_v1_") as temporary:
        paths, roots = _fixture_paths(Path(temporary))
        guard = prepare_governed_root_rollback(paths)
        evidence = guard.evidence()
        if evidence["protected_root_count"] != 6:
            raise RuntimeError("Not all registered governed roots were backed up.")
        if not all(item["archive_sha256"] for item in evidence["roots"]):
            raise RuntimeError("One or more exact rollback archives are missing.")

        _write(roots["tool"] / "source" / "main.py", "mutated\n")
        _write(roots["tool"] / "source" / "new_file.txt", "new\n")
        (roots["tool_support"] / "memory" / "owner.json").unlink()
        _write(roots["other"] / "eeg" / "engine.py", "mutated\n")
        _write(roots["other_support"] / "memory" / "project.json", "mutated\n")
        _write(roots["other_support"] / "memory" / "new.json", "{}\n")
        (roots["other_transient"] / "job" / "state.txt").unlink()
        _write(roots["tool_transient"] / "outside_build_lane.txt", "mutated\n")

        try:
            guard.checkpoint("PORTABLE FIXTURE MUTATION CHECK")
        except PortableBuildError as exc:
            if "restored the exact baseline tree" not in str(exc):
                raise
        else:
            raise RuntimeError("Governed-root mutation did not fail closed.")
        _assert_restored(roots)
        guard.checkpoint("PORTABLE FIXTURE POST-ROLLBACK CHECK")

        _write(roots["run_root"] / "diagnostic.json", "{}\n")
        guard.checkpoint("PORTABLE FIXTURE BUILD LANE CHECK")

        _write(roots["other"] / "eeg" / "engine.py", "failure path mutation\n")
        failure = guard.restore_if_changed("PORTABLE FIXTURE FAILURE ROLLBACK")
        if failure["status"] != "RESTORED":
            raise RuntimeError("Exception-path rollback did not report restoration.")
        _assert_restored(roots)

        original_registry = roots["registry"].read_bytes()
        _write(roots["registry"], "{}\n")
        try:
            guard.checkpoint("PORTABLE FIXTURE REGISTRY TOCTOU")
        except PortableBuildError:
            pass
        else:
            raise RuntimeError("Registry TOCTOU change was not rejected.")
        roots["registry"].write_bytes(original_registry)

    print("PORTABLE ROLLBACK ALL REGISTERED ROOTS COVERED: PASS")
    print("PORTABLE ROLLBACK EXACT BACKUP ARCHIVES: PASS")
    print("PORTABLE ROLLBACK BACKUP RESTORE PROOF: PASS")
    print("PORTABLE ROLLBACK TOOL SOURCE MUTATION RESTORED: PASS")
    print("PORTABLE ROLLBACK TOOL SUPPORT MUTATION RESTORED: PASS")
    print("PORTABLE ROLLBACK OTHER PROJECT SOURCE RESTORED: PASS")
    print("PORTABLE ROLLBACK OTHER PROJECT SUPPORT RESTORED: PASS")
    print("PORTABLE ROLLBACK PROJECT TRANSIENT RESTORED: PASS")
    print("PORTABLE ROLLBACK TOOL TRANSIENT BUILD LANE EXCLUDED: PASS")
    print("PORTABLE ROLLBACK FAILURE PATH RESTORE: PASS")
    print("PORTABLE ROLLBACK REGISTRY TOCTOU REJECTED: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    if os.name != "nt":
        raise RuntimeError("Portable governed-root live validation requires Windows.")
    if "governed-root-exact-rollback" not in PORTABLE_HARDENING_FEATURES:
        raise RuntimeError("GOVERNED_ROOT_ROLLBACK_CAPABILITY_MISSING")
    print("PORTABLE GOVERNED ROOT ROLLBACK CAPABILITY IDENTITY: PASS")
    live = load_registry_boundary(project_root)
    if live.tool_root != project_root:
        raise RuntimeError("Live Tool root does not match the requested Project root.")
    if live.selection_mode != "EXPLICIT_SELF_HOSTING":
        raise RuntimeError("Live Portable validation requires explicit self-hosting.")
    if len(live.protected_roots) < 3:
        raise RuntimeError("Live registry did not expose all governed root kinds.")
    print("PORTABLE ROLLBACK LIVE EXPLICIT SELF-HOSTING AUTHORITY: PASS")
    print("PORTABLE ROLLBACK LIVE REGISTERED ROOTS LOADED: PASS")

    _functional_fixture()

    workflow = (project_root / "portable" / "workflow.py").read_text(encoding="utf-8")
    required = (
        "prepare_governed_root_rollback",
        "PORTABLE GOVERNED ROOTS UNCHANGED AFTER BUILD",
        "PORTABLE GOVERNED ROOTS UNCHANGED AFTER SMOKE",
        "PORTABLE GOVERNED ROOTS UNCHANGED AFTER PUBLICATION",
        "PORTABLE FAILURE GOVERNED ROOT EXACT ROLLBACK",
    )
    missing = [token for token in required if token not in workflow]
    if missing:
        raise RuntimeError(f"Portable workflow rollback integration missing: {missing}")
    print("PORTABLE ROLLBACK WORKFLOW CHECKPOINT INTEGRATION: PASS")

    if PRODUCTION_PORTABLE_ENABLED is not False:
        raise RuntimeError("Production Portable gate must remain closed.")
    print("PORTABLE PRODUCTION BUILD GATE CLOSED: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
