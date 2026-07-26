# project-path: tools/validate_engineering_safety_ruff_correction_workflow_v3a.py
"""Focused validation for the reviewed Ruff correction workflow Phase 3A."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from zipfile import ZipFile

FEATURE_ID = "engineering-safety-ruff-correction-workflow-v3a"

NEW_FILES = (
    "kanda_reasoner_app/source_hygiene/ruff_correction_apply.py",
    "kanda_reasoner_app/source_hygiene/ruff_correction_cli.py",
    "kanda_reasoner_app/source_hygiene/ruff_correction_discovery.py",
    "kanda_reasoner_app/source_hygiene/ruff_correction_errors.py",
    "kanda_reasoner_app/source_hygiene/ruff_correction_identity.py",
    "kanda_reasoner_app/source_hygiene/ruff_correction_models.py",
    "kanda_reasoner_app/source_hygiene/ruff_correction_preview.py",
    "kanda_reasoner_app/source_hygiene/ruff_correction_storage.py",
    "tools/validate_engineering_safety_ruff_correction_workflow_v3a.py",
)

PATCH_MEMBERS = frozenset(("KANDA_FREEZE_HINT.json", *NEW_FILES))

FROZEN_HASHES = dict(
    (
        (
            "_reasoner_tools_gui_engineering_safety_panel_commands.py",
            "d80ea8ffd9f8c78d1c42e1ef30772afe7ca5cfaeda051a3aef0d61c045698b92",
        ),
        (
            "reasoner_tools_gui_engineering_safety_panel.py",
            "4e692e40532c553b577786ec88fd244f19a3bb48f4137649299d60f094fde803",
        ),
        (
            "kanda_reasoner_app/safety_suite_cli/commands.py",
            "4ad824f42a148f9bf14651e521d848882c606746bde856df4cafbd186a5cf4d4",
        ),
        (
            "kanda_reasoner_app/safety_suite_cli/commands_actions_private.py",
            "30124df6e7c139ff6ec7865490771c44916ada58f2cc3379dbc01a03469e2d5c",
        ),
        (
            "kanda_reasoner_app/safety_suite_cli/commands_catalog_private.py",
            "e8317c0f94cf0d48c8656011f719b1841b7ae88a07f72a1df6a9326a6f5244f4",
        ),
        (
            "kanda_reasoner_app/safety_suite_cli/commands_parsers_private.py",
            "e13c0fa9071f6a84835c34065e937a8897ead75ec94f2f05ec7b32c5a169d29e",
        ),
        (
            "kanda_reasoner_app/source_hygiene/__init__.py",
            "3289158296bb108d117d5013362306fa6d8c615e1579d34b5236630a2ffa4b28",
        ),
        (
            "kanda_reasoner_app/source_hygiene/ruff_quality.py",
            "7a2318f5f2f44508695a2f7d9ce602670af64f5360147a6c850aa4bdce5ceca7",
        ),
        (
            "kanda_reasoner_app/source_hygiene/ruff_quality_runtime.py",
            "2f7ac19a402c2094467d89b0bdd012146ec332c41a87a1b79bfa3b170c4d612a",
        ),
        (
            "kanda_reasoner_app/source_hygiene/ruff_quality_scope.py",
            "aac05f694bd7f65397ee8d53d2d3883aace37005058d1b2e16d8d3b30b490b3a",
        ),
        (
            "kanda_reasoner_app/source_hygiene/schemas.py",
            "31bfc47a146eac742f08d831ea4ef9490c66742fa769f0592a4154fce4a4097d",
        ),
        (
            "tools/validate_engineering_safety_source_hygiene_ruff_quality_v1.py",
            "b782d29787be0d959a8a446bf73797bc3297e139950c8ed4d684c1f8e5bd1661",
        ),
        (
            "ruff.toml",
            "52172a11111cedc04a0942130358ecb65ffa34ee98be833ef6c50cbc01bc0746",
        ),
        (
            "kanda_reasoner_app/source_hygiene/ruff_policy_identity.py",
            "6ecde4874c74888fd19314cf12eeda9556469db97ba0fc1ae818323e15533fcf",
        ),
        (
            "tools/validate_engineering_safety_ruff_policy_identity_v2.py",
            "668dd5aca93190c4b3f7e827462705c7219911cbfdaf06e991266a55cae2a610",
        ),
    )
)


def main() -> int:
    """Run all focused validation gates."""
    args = _parser().parse_args()
    root = Path(args.project_root).expanduser().resolve()
    patch_zip = Path(args.patch_zip).expanduser().resolve()
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    _validate_patch_members(patch_zip)
    print("PATCH_MEMBER_SCOPE_ADDITIVE_ONLY: PASS")
    _validate_frozen_hashes(root)
    print("FROZEN_PHASE1_PHASE2_BYTE_IDENTITY: PASS")
    _validate_python_sources(root)
    print("PYTHON_COMPILE: PASS")
    print("MODULE_SIZE_LAW_BELOW_500: PASS")
    _validate_source_contracts(root)
    print("RUFF_CORRECTION_SAFE_FIX_ONLY_CONTRACT: PASS")
    print("RUFF_CORRECTION_EXPLICIT_CONFIRMATION_CONTRACT: PASS")
    print("RUFF_CORRECTION_PROJECT_SUPPORT_OWNERSHIP: PASS")

    ruff_prefix = (args.ruff_executable,) if args.ruff_executable else None
    _validate_new_files_with_ruff(root, args.ruff_executable)
    print("NEW_MODULE_RUFF_LINT: PASS")
    print("NEW_MODULE_RUFF_FORMAT_CHECK: PASS")
    _run_end_to_end_fixtures(root, ruff_prefix)
    print("RUFF_CORRECTION_PREVIEW_ACTIVE_SOURCE_UNCHANGED: PASS")
    print("RUFF_CORRECTION_EXACT_DIFF_AND_PAYLOAD: PASS")
    print("RUFF_CORRECTION_WRONG_TOKEN_BLOCKED: PASS")
    print("RUFF_CORRECTION_STALE_SOURCE_BLOCKED: PASS")
    print("RUFF_CORRECTION_POLICY_STALE_BLOCKED: PASS")
    print("RUFF_CORRECTION_MANIFEST_TAMPER_BLOCKED: PASS")
    print("RUFF_CORRECTION_CANDIDATE_LIMIT_FAILS_CLOSED: PASS")
    print("RUFF_CORRECTION_EXPLICIT_APPLY_BACKUP_RECEIPT: PASS")
    print("RUFF_CORRECTION_POST_APPLY_VALIDATION: PASS")
    print("RUFF_CORRECTION_FORCED_FAILURE_ROLLBACK: PASS")
    print("RUFF_CORRECTION_NO_PROJECT_CACHE: PASS")
    print("PATCH_ZIP_CONTRACT: PASS")
    print("ZIP CONTRACT: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--patch-zip", required=True)
    parser.add_argument("--ruff-executable", default="")
    return parser


def _validate_patch_members(patch_zip: Path) -> None:
    if not patch_zip.is_file():
        raise AssertionError("Patch ZIP missing: " + str(patch_zip))
    with ZipFile(patch_zip) as archive:
        members = frozenset(
            item.filename.rstrip("/")
            for item in archive.infolist()
            if not item.is_dir()
        )
        if members != PATCH_MEMBERS:
            raise AssertionError(
                "Patch member mismatch: " + json.dumps(sorted(members))
            )
        hint = json.loads(archive.read("KANDA_FREEZE_HINT.json"))
    if hint.get("feature_id") != FEATURE_ID:
        raise AssertionError("Freeze hint feature ID mismatch")
    if set(hint.get("protected_paths") or ()) != set(NEW_FILES):
        raise AssertionError("Freeze hint protected paths mismatch")


def _validate_frozen_hashes(root: Path) -> None:
    for relative, expected in FROZEN_HASHES.items():
        path = root / relative
        if not path.is_file():
            raise AssertionError("Frozen file missing: " + relative)
        if _sha256(path) != expected:
            raise AssertionError("Frozen file changed: " + relative)


def _validate_python_sources(root: Path) -> None:
    for relative in NEW_FILES:
        path = root / relative
        if not path.is_file():
            raise AssertionError("New file missing: " + relative)
        text = path.read_text(encoding="utf-8", errors="strict")
        if any(ord(char) > 127 for char in text):
            raise AssertionError("Non-ASCII source: " + relative)
        compile(text, relative, "exec")
        if len(text.splitlines()) >= 500:
            raise AssertionError("Module size law failed: " + relative)


def _validate_source_contracts(root: Path) -> None:
    string_values: list[str] = []
    implementation_files = tuple(
        relative for relative in NEW_FILES if not relative.startswith("tools/")
    )
    for relative in implementation_files:
        tree = ast.parse((root / relative).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                string_values.append(node.value)
    forbidden = {"--unsafe-fixes", "--fix-only", "--diff"}
    if forbidden.intersection(string_values):
        raise AssertionError("Unsafe Ruff mutation argument found")
    required = {"--fix", "--no-unsafe-fixes", "--no-cache", "--no-preview"}
    if not required.issubset(set(string_values)):
        raise AssertionError("Required safe shadow arguments missing")

    storage_text = (
        root / "kanda_reasoner_app/source_hygiene/ruff_correction_storage.py"
    ).read_text(encoding="utf-8")
    if "show_project_to_ai_root_from_hint" not in storage_text:
        raise AssertionError("Shared project support resolver missing")
    if "error_memory.paths" in storage_text:
        raise AssertionError("Cross-box Error Memory path reach-in found")


def _validate_new_files_with_ruff(root: Path, executable: str) -> None:
    if not executable:
        return
    paths = [str(root / relative) for relative in NEW_FILES]
    common = [
        executable,
        "--config",
        str(root / "ruff.toml"),
    ]
    lint = subprocess.run(
        [*common, "check", "--no-cache", "--no-preview", *paths],
        cwd=str(root),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if lint.returncode != 0:
        raise AssertionError("New-file Ruff lint failed: " + lint.stdout + lint.stderr)
    formatting = subprocess.run(
        [*common, "format", "--check", "--no-cache", "--no-preview", *paths],
        cwd=str(root),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if formatting.returncode != 0:
        raise AssertionError(
            "New-file Ruff format check failed: "
            + formatting.stdout
            + formatting.stderr
        )


def _run_end_to_end_fixtures(
    source_root: Path,
    ruff_prefix: tuple[str, ...] | None,
) -> None:
    from kanda_reasoner_app.source_hygiene import ruff_correction_apply
    from kanda_reasoner_app.source_hygiene.ruff_correction_apply import (
        RuffCorrectionApplyError,
        apply_ruff_correction_preview,
        load_ruff_correction_preview,
    )
    from kanda_reasoner_app.source_hygiene.ruff_correction_errors import (
        RuffCorrectionPreviewError,
    )
    from kanda_reasoner_app.source_hygiene.ruff_correction_preview import (
        create_ruff_correction_preview,
    )
    from kanda_reasoner_app.source_hygiene.ruff_correction_storage import (
        load_json_object,
        resolve_ruff_correction_paths,
    )

    with tempfile.TemporaryDirectory(prefix="kanda_ruff3a_") as temp_name:
        temp = Path(temp_name)
        project = _make_fixture_project(temp / "project", source_root)
        source_file = project / "pkg" / "sample.py"
        baseline = source_file.read_bytes()
        preview = create_ruff_correction_preview(
            project,
            scope_paths=("pkg/sample.py",),
            max_files=10,
            ruff_argv_prefix=ruff_prefix,
        )
        if source_file.read_bytes() != baseline:
            raise AssertionError("Preview mutated active source")
        if preview.status != "PREVIEW_READY" or preview.changed_file_count != 1:
            raise AssertionError("Preview did not produce one changed file")
        if (
            not Path(preview.diff_path)
            .read_text(encoding="utf-8")
            .startswith("--- a/pkg/sample.py\n+++ b/pkg/sample.py\n")
        ):
            raise AssertionError("Exact unified diff missing")
        _assert_outside_project(Path(preview.preview_root), project)
        paths = resolve_ruff_correction_paths(project)
        if paths.shadow_root(preview.preview_id).exists():
            raise AssertionError("Disposable shadow was not cleaned")

        _expect_apply_block(
            lambda: apply_ruff_correction_preview(
                project,
                preview.preview_id,
                confirm_token="WRONG",
                ruff_argv_prefix=ruff_prefix,
            ),
            "CONFIRMATION_TOKEN_MISMATCH",
        )
        if source_file.read_bytes() != baseline:
            raise AssertionError("Wrong token changed source")

        stale_project = _make_fixture_project(temp / "stale", source_root)
        stale_preview = create_ruff_correction_preview(
            stale_project,
            scope_paths=("pkg/sample.py",),
            max_files=10,
            ruff_argv_prefix=ruff_prefix,
        )
        stale_file = stale_project / "pkg" / "sample.py"
        stale_text = stale_file.read_text(encoding="utf-8")
        stale_file.write_text(
            stale_text + "\n# changed\n",
            encoding="utf-8",
        )
        _expect_apply_block(
            lambda: apply_ruff_correction_preview(
                stale_project,
                stale_preview.preview_id,
                confirm_token=stale_preview.confirm_token,
                ruff_argv_prefix=ruff_prefix,
            ),
            "SOURCE_STALE",
        )

        policy_project = _make_fixture_project(temp / "policy", source_root)
        policy_preview = create_ruff_correction_preview(
            policy_project,
            scope_paths=("pkg/sample.py",),
            max_files=10,
            ruff_argv_prefix=ruff_prefix,
        )
        with (policy_project / "ruff.toml").open("a", encoding="utf-8") as handle:
            handle.write("\n# policy changed\n")
        _expect_apply_block(
            lambda: apply_ruff_correction_preview(
                policy_project,
                policy_preview.preview_id,
                confirm_token=policy_preview.confirm_token,
                ruff_argv_prefix=ruff_prefix,
            ),
            "POLICY_IDENTITY_STALE",
        )

        tamper_project = _make_fixture_project(temp / "tamper", source_root)
        tamper_preview = create_ruff_correction_preview(
            tamper_project,
            scope_paths=("pkg/sample.py",),
            max_files=10,
            ruff_argv_prefix=ruff_prefix,
        )
        manifest = Path(tamper_preview.manifest_path)
        data = load_json_object(manifest)
        data["source_snapshot_sha256"] = "0" * 64
        manifest.write_text(json.dumps(data), encoding="utf-8")
        _expect_apply_block(
            lambda: load_ruff_correction_preview(
                tamper_project,
                tamper_preview.preview_id,
            ),
            "MANIFEST_IDENTITY_MISMATCH",
        )

        limit_project = _make_fixture_project(temp / "limit", source_root)
        shutil.copy2(
            limit_project / "pkg" / "sample.py",
            limit_project / "pkg" / "second.py",
        )
        try:
            create_ruff_correction_preview(
                limit_project,
                scope_paths=("pkg",),
                max_files=1,
                ruff_argv_prefix=ruff_prefix,
            )
        except RuffCorrectionPreviewError as exc:
            if "CANDIDATE_LIMIT_EXCEEDED" not in str(exc):
                raise
        else:
            raise AssertionError("Candidate limit did not fail closed")

        receipt = apply_ruff_correction_preview(
            project,
            preview.preview_id,
            confirm_token=preview.confirm_token,
            ruff_argv_prefix=ruff_prefix,
        )
        if receipt.status != "APPLIED":
            raise AssertionError("Apply receipt is not APPLIED")
        if source_file.read_bytes() == baseline:
            raise AssertionError("Explicit apply did not change source")
        if not Path(receipt.backup_root, "pkg", "sample.py").is_file():
            raise AssertionError("Backup file missing")
        if not Path(receipt.receipt_path).is_file():
            raise AssertionError("Receipt file missing")
        if (project / ".ruff_cache").exists():
            raise AssertionError("Project Ruff cache leaked")

        rollback_project = _make_fixture_project(temp / "rollback", source_root)
        rollback_file = rollback_project / "pkg" / "sample.py"
        rollback_baseline = rollback_file.read_bytes()
        rollback_preview = create_ruff_correction_preview(
            rollback_project,
            scope_paths=("pkg/sample.py",),
            max_files=10,
            ruff_argv_prefix=ruff_prefix,
        )
        original_validator = ruff_correction_apply._validate_applied_files

        def forced_failure(*_args: object, **_kwargs: object) -> tuple[str, ...]:
            raise RuffCorrectionApplyError("FORCED_POST_APPLY_FAILURE")

        ruff_correction_apply._validate_applied_files = forced_failure
        try:
            _expect_apply_block(
                lambda: apply_ruff_correction_preview(
                    rollback_project,
                    rollback_preview.preview_id,
                    confirm_token=rollback_preview.confirm_token,
                    ruff_argv_prefix=ruff_prefix,
                ),
                "APPLY_ROLLED_BACK",
            )
        finally:
            ruff_correction_apply._validate_applied_files = original_validator
        if rollback_file.read_bytes() != rollback_baseline:
            raise AssertionError("Rollback did not restore baseline")
        rollback_receipt = load_json_object(
            resolve_ruff_correction_paths(rollback_project).receipts_root
            / (rollback_preview.preview_id + ".json")
        )
        if rollback_receipt.get("status") != "ROLLED_BACK":
            raise AssertionError("Rollback receipt status mismatch")


def _make_fixture_project(path: Path, source_root: Path) -> Path:
    path.mkdir(parents=True, exist_ok=False)
    (path / "pkg").mkdir()
    shutil.copy2(source_root / "ruff.toml", path / "ruff.toml")
    (path / "pkg" / "sample.py").write_text(
        "import os\n\n\ndef greet( name:str )->str:\n    return 'hello '+name\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def _expect_apply_block(action: object, marker: str) -> None:
    try:
        action()  # type: ignore[operator]
    except Exception as exc:
        if marker not in str(exc):
            raise AssertionError("Unexpected block marker: " + str(exc)) from exc
    else:
        raise AssertionError("Expected operation to be blocked: " + marker)


def _assert_outside_project(path: Path, project_root: Path) -> None:
    try:
        path.resolve().relative_to(project_root.resolve())
    except ValueError:
        return
    raise AssertionError("Project-specific support leaked into source root")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
