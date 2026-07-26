"""Validate Heuristic replay renderer runtime fix and freeze identity separation."""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
import zipfile

__all__ = [
    "main",
]

ROOT = Path(__file__).resolve().parents[1]
GUI = ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_stage_correction_gui.py"
FEATURE_ID = "architecture-review-workbench-heuristic-replay-renderer-runtime-fix-v1"


def require(condition: bool, marker: str) -> None:
    if not condition:
        raise AssertionError(marker)
    print(f"{marker}: PASS")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--patch-zip", required=True)
    return parser.parse_args()


def _read_root_freeze_hint(patch_zip: Path) -> dict:
    if not patch_zip.is_file():
        raise AssertionError(f"PATCH_ZIP_NOT_FOUND: {patch_zip}")
    with zipfile.ZipFile(patch_zip, "r") as archive:
        names = archive.namelist()
        if names.count("KANDA_FREEZE_HINT.json") != 1:
            raise AssertionError("ROOT_FREEZE_HINT_EXACTLY_ONCE")
        return json.loads(archive.read("KANDA_FREEZE_HINT.json").decode("utf-8-sig"))


def main() -> None:
    args = _parse_args()
    source = GUI.read_text(encoding="utf-8")
    tree = ast.parse(source)
    defs = {n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    require("_render_replay_evidence" in defs, "REPLAY_RENDERER_FUNCTION_DEFINED")
    require("render_replay=_render_replay_evidence" in source.replace(" ", ""), "REPLAY_RENDERER_BOUND_TO_CONTROLLER")
    for token in (
        "format_workbench_dependency_readiness",
        "format_real_preview_result",
        "format_real_preview_structural_validation",
        "format_preflight_backup_readiness",
        "format_source_apply_payload_readiness",
    ):
        require(token in source, f"REPLAY_RENDERER_USES_{token.upper()}")

    hint = _read_root_freeze_hint(Path(args.patch_zip).resolve())
    require(hint.get("feature_id") == FEATURE_ID, "UNIQUE_FREEZE_FEATURE_ID")
    require(bool(hint.get("validated_files")), "FREEZE_HINT_VALIDATED_FILES_PRESENT")
    require(bool(str(hint.get("validation_evidence_summary") or "").strip()), "FREEZE_HINT_VALIDATION_EVIDENCE_SUMMARY_PRESENT")
    require(old_feature_not_present(hint), "NO_REUSE_OF_CONSUMED_V3_FREEZE_ID")
    print("FREEZE_HINT_READ_FROM_STAGED_PATCH_ZIP: PASS")

    print("WORKBENCH_HEURISTIC_REPLAY_RENDERER_RUNTIME_FIX: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")


def old_feature_not_present(hint: dict) -> bool:
    return str(hint.get("feature_id") or "") != "architecture-review-workbench-heuristic-feedback-replay-transaction-v3"


if __name__ == "__main__":
    main()
